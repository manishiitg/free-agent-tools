# Keep the catalog useful

Edit only `src/free_agent_tools/catalog.json` for provider data. Use official pricing, eligibility or API documentation. Marketing claims with an unclear reset or eligibility belong under `unconfirmed` / `needs_review`. Paid products can be included for comparison. Consumer app allowances are not proof of API credits.

Record the precise unit, reset, expiry and eligibility when known. Mention restrictions and possible overages in `offer.conditions`. Set `last_reviewed` whenever you inspect an entry; set `last_verified` only after checking its offer against official evidence. Keep `updated_at` and `version` current with the reviewed snapshot. Do not refresh dates merely because a link returns HTTP 200. Mark entries needing confirmation `needs_review`.

Documented MCP support needs a setup source. Use `unknown` if unresearched. An `agentworks_connector` mapping means a catalog entry exists; it does not mean a live connection works. Add no API keys, private URLs, customer details or account balances.

From a virtual environment with `.[dev]` installed:

```sh
python scripts/validate.py
python scripts/build.py
python scripts/smoke_mcp.py
python scripts/build.py --check
node --check docs/assets/app.js
```

Commit the data, regenerated README and `docs/` outputs together. Pull requests run the same checks. AgentWorks HQ serves the reviewed data from main; verification dates are preserved. The website build synchronizes the directory UI from this repository, with a committed copy for offline builds.

## Review reports

The weekly workflow emits `report.json`, `report.md`, and `observed.json` as a downloadable artifact. A page hash change, blocked fetch or overdue date requests human review. Content hashes represent normalized visible text; JavaScript-rendered pricing may not be visible and dynamic text can produce false positives. They are not pricing parsers or a guarantee of unchanged offers.

Run the check locally to inspect current evidence:

```sh
python scripts/check_sources.py --output .maintenance
```

After reviewing a provider's published offer and updating its data/date, refresh only its source baseline:

```sh
python scripts/check_sources.py --output .maintenance --accept-reviewed deepgram
```

This records successful source hashes only for the named provider. Use the same process for every provider reviewed; do not approve changes solely from a source response. For first publication, `--initialize` creates a baseline for all successful responses without changing any verification dates. Blocked pages stay explicitly flagged; add a better official source when available.

If a GitHub runner sees different regional content, download its report artifact and inspect the official offer before accepting the runner's observations:

```sh
python scripts/check_sources.py --output .maintenance --accept-reviewed apify --accept-observed path/to/downloaded/observed.json
```

The baseline separately records known blocked or browser-only sources. An unchanged known limitation is reported without repeatedly failing the workflow. New failures still flag review. These pages require manual checks; a successful fetch alone is never verification.

No automated edits to offers or verification dates. GitHub Actions' native failure notifications and reports are the maintenance channel; no messages or accounts are created on other services.
