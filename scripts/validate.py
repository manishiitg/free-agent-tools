#!/usr/bin/env python3
"""Validate the data contract and evidence relationships."""
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT / "src/free_agent_tools/catalog.json").read_text())
    schema = json.loads((ROOT / "schema/catalog.schema.json").read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)
    categories = [c["id"] for c in data["categories"]]
    ids = [p["id"] for p in data["providers"]]
    assert len(categories) == len(set(categories)), "Duplicate categories"
    assert len(ids) == len(set(ids)), "Duplicate provider IDs"
    today = date.today()
    assert date.fromisoformat(data["updated_at"]) <= today, "Future snapshot"
    for p in data["providers"]:
        assert set(p["categories"]) <= set(categories), f"{p['id']}: unknown category"
        reviewed = date.fromisoformat(p["last_reviewed"])
        assert reviewed <= date.fromisoformat(data["updated_at"]), f"{p['id']}: snapshot predates review"
        if p["status"] == "verified":
            assert p["last_verified"], f"{p['id']}: verification date required"
            assert p["offer"]["kind"] != "unconfirmed", f"{p['id']}: unconfirmed offer cannot be verified"
        if p["last_verified"]:
            assert date.fromisoformat(p["last_verified"]) <= reviewed, f"{p['id']}: invalid verification date"
        if p["mcp"]["support"] in {"official", "community"}:
            assert p["mcp"]["setup_url"], f"{p['id']}: documented MCP setup required"
        urls = [s["url"] for s in p["sources"]]
        if p["mcp"]["setup_url"]:
            urls.append(p["mcp"]["setup_url"])
        for url in urls:
            parsed = urlsplit(url)
            assert parsed.hostname and not parsed.username and not parsed.password, f"{p['id']}: invalid public URL"
            assert not parsed.query, f"{p['id']}: source URLs must not contain query credentials"
    print(f"Catalog valid: {len(ids)} providers, {len(categories)} categories")


if __name__ == "__main__":
    main()
