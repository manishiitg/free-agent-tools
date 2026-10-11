"""Shared catalog search for the CLI and MCP, with explicit freshness."""

import argparse
import copy
import json
import re
from datetime import date, datetime, timezone
from importlib.resources import files

FRESH_DAYS = 30
FREE_KINDS = {"recurring", "trial", "grant", "open_source"}
KINDS = FREE_KINDS | {"paid", "unconfirmed"}


def load_catalog() -> dict:
    return json.loads(files("free_agent_tools").joinpath("catalog.json").read_text(encoding="utf-8"))


def project(entry: dict, today: date | None = None) -> dict:
    result = copy.deepcopy(entry)
    today = today or datetime.now(timezone.utc).date()
    verified = result["last_verified"]
    age = (today - date.fromisoformat(verified)).days if verified else None
    result["days_since_verified"] = age
    result["effective_status"] = (
        "stale" if age is not None and age > FRESH_DAYS and result["status"] == "verified"
        else result["status"]
    )
    return result


def search_catalog(query: str = "", category: str = "", offer_kind: str = "",
                   free_only: bool = False, mcp_only: bool = False,
                   verified_only: bool = False, limit: int = 20, offset: int = 0) -> dict:
    doc = load_catalog()
    if category and category not in {c["id"] for c in doc["categories"]}:
        raise ValueError("Unknown category; use list_tool_categories to find supported IDs")
    if offer_kind and offer_kind not in KINDS:
        raise ValueError("Unknown offer_kind")
    if not 1 <= limit <= 100 or offset < 0 or offset > 10000:
        raise ValueError("limit must be 1–100 and offset 0–10000")
    terms = re.findall(r"[a-z0-9]+", query.lower())
    matches = []
    for raw in doc["providers"]:
        entry = project(raw)
        if category and category not in entry["categories"]:
            continue
        if offer_kind and entry["offer"]["kind"] != offer_kind:
            continue
        if free_only and entry["offer"]["kind"] not in FREE_KINDS:
            continue
        if mcp_only and entry["mcp"]["support"] not in {"official", "community"}:
            continue
        if verified_only and entry["effective_status"] != "verified":
            continue
        haystack = " ".join([entry["name"], entry["description"], *entry["categories"],
                             *entry["capabilities"], entry["offer"]["summary"]]).lower()
        if all(term in haystack for term in terms):
            matches.append(entry)
    matches.sort(key=lambda e: (e["effective_status"] != "verified", e["name"].lower()))
    return {"catalog_version": doc["version"], "total": len(matches), "offset": offset,
            "next_offset": offset + limit if offset + limit < len(matches) else None,
            "providers": matches[offset:offset + limit]}


def get_provider(provider_id: str) -> dict:
    for entry in load_catalog()["providers"]:
        if entry["id"] == provider_id:
            return project(entry)
    raise ValueError("Provider not found")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--offer-kind", default="")
    parser.add_argument("--free-only", action="store_true")
    parser.add_argument("--mcp-only", action="store_true")
    parser.add_argument("--verified-only", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--offset", type=int, default=0)
    args = vars(parser.parse_args())
    try:
        print(json.dumps(search_catalog(**args), ensure_ascii=False, indent=2))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
