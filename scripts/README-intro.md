# Free Agent Tools

A maintained catalog of APIs, free tiers and credits for AI agents. Search, scraping and browsers are only the start: the directory also covers models, speech, documents, compute, memory, integrations and specialized data.

**[Browse the directory](https://manishiitg.github.io/free-agent-tools/)** · [JSON](https://manishiitg.github.io/free-agent-tools/catalog.json) · [CSV](https://manishiitg.github.io/free-agent-tools/catalog.csv) · [Maintenance reports](https://github.com/manishiitg/free-agent-tools/actions/workflows/review.yml)

Each entry records the published allowance, offer type, eligibility, official evidence, review date and documented MCP support. The catalog is a starting point, not an exhaustive list or a guarantee that a particular account qualifies. It does not know your balance or provision accounts.

## Use the discovery MCP

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.10+. Add this stdio server to a client that supports local MCP servers:

```json
{
  "mcpServers": {
    "free-agent-tools": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/manishiitg/free-agent-tools@v0.1.0",
        "free-agent-tools-mcp"
      ]
    }
  }
}
```

The release tag pins a reproducible snapshot. For the latest reviewed data, install from `@main` instead and run `uvx --refresh --from git+https://github.com/manishiitg/free-agent-tools@main free-agent-tools-mcp` when updating your client. Restart the server after an update. Running servers use bundled data; they do not silently fetch new data.

Tools:

- `search_free_tools`: filter by capability, category, offer type, freshness or documented MCP; results include source URLs and pagination.
- `get_free_tool`: read a provider's allowance, conditions and setup evidence.
- `list_tool_categories`: get supported categories and the snapshot date.

The `catalog://free-agent-tools` resource exposes the full snapshot. All tools are read-only. Example request: “Find recurring free transcription APIs, show eligibility and official sources.” Search matches all query words; use short capabilities such as `transcription`, `pdf` or `browser`.

The server discovers tools; provider execution and credit routing are separate work. MCP support marked `unknown` means it has not been researched, not that no MCP exists. An AgentWorks catalog name is a registry mapping, not proof that a connection is installed or working. This stdio server can run in local MCP clients; the hosted AgentWorks connector gateway needs a separate compatible connection configuration.

## CLI

```sh
uvx --from git+https://github.com/manishiitg/free-agent-tools@main free-agent-tools transcription --free-only
uvx --from git+https://github.com/manishiitg/free-agent-tools@main free-agent-tools --category compute --offer-kind recurring
```

## What “free” means

| Label | Meaning |
|---|---|
| Recurring | An included allowance resets, usually monthly or daily. |
| Trial | Initial credits or evaluation access; not a renewable production allowance. |
| Grant | Conditional offer that requires eligibility or application. |
| Open source | Self-hostable software; infrastructure may still cost money. |
| Unconfirmed | An offer is advertised but its allowance, reset or eligibility needs review. |
| Paid | Useful API included for comparison; no universal free allowance confirmed. |

`free_only` includes recurring tiers, trials, grants and open source. It excludes paid and unconfirmed offers. Numeric allowances have different units and cannot be directly compared as equal work. Some free plans restrict commercial use, require a card, have rate limits or charge for overages; read each entry's conditions and the provider's current source.

“Verified” means the listed public offer was reviewed against official evidence on the recorded date; it does not mean signup or execution was tested. After 30 days, the website and MCP mark a verified entry stale. `verified_only` excludes stale and review-needed entries. The raw JSON preserves the original evidence date.

## Maintenance

The single editable data source is [`src/free_agent_tools/catalog.json`](src/free_agent_tools/catalog.json), governed by the [schema](schema/catalog.schema.json). The README table and `docs/` site/data exports are generated.

Weekly GitHub Actions compare official source responses with a reviewed content-hash baseline and report unreachable links, changed pages and overdue reviews. Reports are downloadable workflow artifacts and job summaries. A changed page is a review signal, not proof that pricing changed. Dynamic pages and bot restrictions can cause false positives. The workflow never rewrites allowances or verification dates automatically.

Review the official offer, correct the data and date, then generate the site and source baseline as described in [CONTRIBUTING.md](CONTRIBUTING.md). Community contributions are welcome through pull requests. MIT licensed; provider names belong to their respective owners.

## Develop and verify

```sh
uv venv
uv pip install -e '.[dev]'
uv run python scripts/validate.py
uv run python scripts/build.py
uv run python scripts/smoke_mcp.py
uv run python scripts/build.py --check
python3 -m http.server 8080 --directory docs
```

CI validates the schema, generated artifacts and real stdio MCP protocol before publishing GitHub Pages. The MCP smoke check starts a server, lists and calls the discovery tools, reads the resource, and checks the freshness boundary.
