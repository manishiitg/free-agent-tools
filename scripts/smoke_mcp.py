#!/usr/bin/env python3
"""Exercise the actual stdio MCP protocol and a dated-offer regression."""
import asyncio
import json
import sys
from datetime import date
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from free_agent_tools.catalog import get_provider, project


async def main():
    params = StdioServerParameters(command=sys.executable, args=["-m", "free_agent_tools.server"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert {t.name for t in tools.tools} == {"search_free_tools", "get_free_tool", "list_tool_categories"}
            assert all(t.annotations.readOnlyHint and not t.annotations.destructiveHint for t in tools.tools)
            async def call(name, args):
                result = await session.call_tool(name, args)
                assert not result.isError, result
                # FastMCP emits both JSON text and structured content for dict results.
                return json.loads(result.content[0].text)
            categories = await call("list_tool_categories", {})
            assert categories["provider_count"] >= 80 and len(categories["categories"]) >= 20
            default = await call("search_free_tools", {"limit": 100})
            assert all(p["offer"]["kind"] not in {"paid", "unconfirmed"} for p in default["providers"])
            models = await call("search_free_tools", {"category": "inference", "limit": 1})
            assert models["next_offset"] == 1 and len(models["providers"]) == 1
            mcp = await call("search_free_tools", {"mcp_only": True, "free_only": False})
            assert mcp["total"] >= 3 and all(p["mcp"]["setup_url"] for p in mcp["providers"])
            tool = await call("get_free_tool", {"provider_id": "deepgram"})
            assert tool["offer"]["kind"] == "trial" and tool["offer"]["conditions"] and tool["sources"]
            unknown = await session.call_tool("get_free_tool", {"provider_id": "not-a-provider"})
            assert unknown.isError, "Unknown IDs must fail rather than guess"
            resource = await session.read_resource("catalog://free-agent-tools")
            assert len(json.loads(resource.contents[0].text)["providers"]) == categories["provider_count"]
    entry = get_provider("deepgram")
    entry["last_verified"] = "2026-01-01"
    assert project(entry, date(2026, 1, 31))["effective_status"] == "verified"
    assert project(entry, date(2026, 2, 1))["effective_status"] == "stale"
    assert entry["last_verified"] == "2026-01-01", "Freshness cannot rewrite evidence"
    print("Passed: real MCP discovery, filters, pagination, resource, errors and 30-day freshness")


if __name__ == "__main__":
    asyncio.run(main())
