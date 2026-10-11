#!/usr/bin/env python3
"""Flag source reachability, visible-content changes and overdue offer reviews."""
import argparse
import hashlib
import json
import re
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "maintenance/source-baseline.json"


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip = max(0, self.skip - 1)

    def handle_data(self, value):
        if not self.skip:
            self.parts.append(value)


def observe(url):
    try:
        request = Request(url, headers={"User-Agent": "FreeAgentToolsCatalog/0.1 (+https://github.com/manishiitg/free-agent-tools)", "Accept": "text/html,text/plain,application/json"})
        with urlopen(request, timeout=15, context=ssl.create_default_context()) as response:
            raw = response.read(8_000_001)
            if len(raw) > 8_000_000:
                return {"status": "oversized", "http_status": response.status}
            text = raw.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            if "html" in response.headers.get("Content-Type", ""):
                parser = VisibleText()
                parser.feed(text)
                text = " ".join(parser.parts)
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) < 80:
                return {"status": "insufficient_text", "http_status": response.status}
            # Never store provider page text. Hashes are review signals, not offer evidence.
            return {"status": "ok", "http_status": response.status, "final_url": response.url,
                    "sha256": hashlib.sha256(text.encode()).hexdigest()}
    except HTTPError as error:
        return {"status": "fetch_failed", "http_status": error.code}
    except Exception as error:
        # Type only: avoid persisting request internals or untrusted exception strings.
        return {"status": "fetch_failed", "error_type": type(error).__name__}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=".maintenance")
    parser.add_argument("--initialize", action="store_true")
    parser.add_argument("--accept-reviewed", nargs="+", default=[])
    parser.add_argument("--accept-observed", type=Path, help="Use a downloaded workflow observation file after reviewing named providers")
    args = parser.parse_args()
    assert not (args.initialize and args.accept_reviewed), "Choose one baseline update mode"
    assert not args.accept_observed or args.accept_reviewed, "Downloaded observations require named reviewed providers"
    assert not (args.initialize and BASELINE.exists()), "Baseline exists; accept specific reviewed providers"
    doc = json.loads((ROOT / "src/free_agent_tools/catalog.json").read_text())
    baseline = json.loads(BASELINE.read_text()) if BASELINE.exists() else {"sources": {}}
    baseline.setdefault("known_limitations", {})
    ids = {p["id"] for p in doc["providers"]}
    assert set(args.accept_reviewed) <= ids, "Unknown reviewed provider ID"
    urls_by_provider = {p["id"]: {s["url"] for s in p["sources"]} | ({p["mcp"]["setup_url"]} if p["mcp"]["setup_url"] else set()) for p in doc["providers"]}
    urls = sorted(set().union(*urls_by_provider.values()))
    observed = json.loads(args.accept_observed.read_text()) if args.accept_observed else {}
    observed = {url: value for url, value in observed.items() if url in urls}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(observe, url): url for url in urls if url not in observed}
        for future in as_completed(futures):
            observed[futures[future]] = future.result()
    today = date.today()
    # Baseline updates are explicit and never touch source data or review dates.
    approved_ids = ids if args.initialize else set(args.accept_reviewed)
    approved_urls = set().union(*(urls_by_provider[i] for i in approved_ids)) if approved_ids else set()
    for url in approved_urls:
        if observed[url]["status"] == "ok":
            assert re.fullmatch(r"[a-f0-9]{64}", observed[url]["sha256"]), "Invalid observed content hash"
            baseline["sources"][url] = {"sha256": observed[url]["sha256"], "baseline_recorded": str(today)}
            baseline["known_limitations"].pop(url, None)
        else:
            baseline["known_limitations"][url] = observed[url]
    if approved_ids:
        baseline["sources"] = {url: value for url, value in sorted(baseline["sources"].items()) if url in urls}
        baseline["known_limitations"] = {url: value for url, value in sorted(baseline["known_limitations"].items()) if url in urls}
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(baseline, indent=2) + "\n")
    flags = []
    limitations = []
    for p in doc["providers"]:
        reasons = []
        if p["last_verified"] and (today - date.fromisoformat(p["last_verified"])).days > doc["freshness_days"]:
            reasons.append("Offer verification overdue")
        for url in sorted(urls_by_provider[p["id"]]):
            observation = observed[url]
            if observation["status"] != "ok":
                if observation == baseline["known_limitations"].get(url):
                    limitations.append({"provider_id": p["id"], "url": url, "status": observation["status"]})
                else:
                    reasons.append(f"Source {observation['status']}: {url}")
            elif url not in baseline["sources"]:
                reasons.append(f"Source baseline missing: {url}")
            elif observation["sha256"] != baseline["sources"][url]["sha256"]:
                reasons.append(f"Visible source content changed: {url}")
        if reasons:
            flags.append({"provider_id": p["id"], "name": p["name"], "reasons": reasons})
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "catalog_version": doc["version"],
              "sources_checked": len(urls), "flagged_providers": flags,
              "known_needs_review": [p["id"] for p in doc["providers"] if p["status"] == "needs_review"],
              "known_source_limitations": limitations}
    lines = ["# Catalog maintenance report", "", f"{len(urls)} official sources checked. {len(flags)} providers flagged. {len(report['known_needs_review'])} entries already marked needs review.", "", "A changed hash is a review signal, not proof that pricing changed. Review official pages before updating offers or dates.", ""]
    for flag in flags:
        lines += [f"## {flag['name']}", ""] + [f"- {r}" for r in flag["reasons"]] + [""]
    if report["known_needs_review"]:
        lines += ["## Already awaiting confirmation", "", ", ".join(report["known_needs_review"]), ""]
    if limitations:
        lines += ["## Known source-check limitations", "", "These pages need manual review; their unchanged fetch limitation does not repeatedly fail the workflow.", ""]
        lines += [f"- {item['provider_id']}: {item['status']} — {item['url']}" for item in limitations] + [""]
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "observed.json").write_text(json.dumps(observed, indent=2, sort_keys=True) + "\n")
    (output / "report.md").write_text("\n".join(lines))
    print(f"Checked {len(urls)} sources; {len(flags)} providers flagged; report: {output / 'report.md'}")
    if flags and not approved_ids:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
