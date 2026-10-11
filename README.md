# Free Agent Tools

A maintained catalog of APIs, free tiers and credits for AI agents. Search, scraping and browsers are only the start: the directory also covers models, speech, documents, compute, memory, integrations and specialized data.

**[Browse the directory](https://agentworkshq.com/free-tools/)** · [JSON](https://agentworkshq.com/free-tools/catalog.json) · [CSV](https://agentworkshq.com/free-tools/catalog.csv) · [Maintenance reports](https://github.com/manishiitg/free-agent-tools/actions/workflows/review.yml)

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

CI validates the schema, generated artifacts, browser behavior and real stdio MCP protocol. The catalog is hosted only on AgentWorks HQ; GitHub holds its source data and MCP package. The MCP smoke check starts a server, lists and calls the discovery tools, reads the resource, and checks the freshness boundary.

## Catalog

85 providers across 20 categories. Snapshot: 2026-10-11. 76 offers reviewed against official evidence; 9 need further confirmation. Review dates below do not update themselves.

### Search & research

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Brave Search](https://brave.com/search/api/) | recurring | $5 free credits per month | Verified 2026-10-11 |
| [Exa](https://exa.ai/pricing) | recurring | $10 monthly credits plus $10 onboarding bonus | Verified 2026-10-11 |
| [Keenable](https://keenable.ai/) | unconfirmed | 100,000 free requests advertised; reset and expiry unclear | Needs review |
| [Linkup](https://www.linkup.so/pricing) | unconfirmed | 4,000 free queries advertised; reset unclear | Needs review |
| [Parallel](https://parallel.ai/blog/free-tier-parallel) | recurring | $5 monthly credits for eligible organizations | Verified 2026-10-11 |
| [Perplexity API](https://docs.perplexity.ai/docs/getting-started/pricing) | paid | Paid API; universal free allowance not confirmed | Verified 2026-10-11 |
| [SearchApi](https://www.searchapi.io/) | trial | 100 starting requests | Verified 2026-10-11 |
| [SerpApi](https://serpapi.com/pricing) | recurring | 250 searches per month | Verified 2026-10-11 |
| [Serper](https://serper.dev/) | trial | 2,500 starting queries | Verified 2026-10-11 |
| [Tavily](https://www.tavily.com/pricing) | recurring | 1,000 API credits per month | Verified 2026-10-11 |
| [Valyu](https://www.valyu.ai/pricing) | trial | $10 signup credits | Verified 2026-10-11 |
| [You.com](https://you.com/pricing) | recurring | 100 free search queries per day plus advertised $100 starting credit | Verified 2026-10-11 |

### Scraping & extraction

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Apify](https://apify.com/pricing) | recurring | $5 platform usage per month | Verified 2026-10-11 |
| [Bright Data](https://brightdata.com/pricing/web-scraper) | recurring | 5,000 Web Scraper API records per month | Verified 2026-10-11 |
| [Firecrawl](https://www.firecrawl.dev/pricing) | recurring | 1,000 credits per month | Verified 2026-10-11 |
| [Jina Reader](https://jina.ai/reader/) | trial | Free rate-limited access; 10 million starting tokens with a new key | Verified 2026-10-11 |
| [Olostep](https://www.olostep.com/pricing) | trial | 500 successful trial requests | Verified 2026-10-11 |
| [Oxylabs](https://developers.oxylabs.io/scraping-solutions/web-scraper-api/usage-and-billing/rate-limits) | unconfirmed | Trial available; documentation lists 2,000 results | Needs review |
| [Scrape.do](https://scrape.do/pricing/) | recurring | 1,000 successful API calls per month | Verified 2026-10-11 |
| [ScrapeGraphAI](https://scrapegraphai.com/pricing) | trial | 500 one-time credits | Verified 2026-10-11 |
| [ScraperAPI](https://www.scraperapi.com/pricing/) | unconfirmed | 1,000 free credits; reset unclear on pricing page | Needs review |
| [ScrapingAnt](https://scrapingant.com/price-scraping-api) | unconfirmed | 10,000 starting credits advertised; reset unclear | Needs review |
| [ScrapingBee](https://www.scrapingbee.com/pricing/) | trial | 1,000 trial credits | Verified 2026-10-11 |
| [Scrapingdog](https://www.scrapingdog.com/pricing/) | trial | 100 trial credits | Verified 2026-10-11 |
| [ZenRows](https://www.zenrows.com/blog/zenrows-mcp) | trial | Trial advertises 1,000 basic URLs and 40 protected URLs | Verified 2026-10-11 |
| [Zyte](https://docs.zyte.com/zyte-api/pricing.html) | trial | $5 initial credit, for first billing month | Verified 2026-10-11 |

### Browser automation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [AgentQL](https://www.agentql.com/pricing) | recurring | 50 API calls per month; separate 300-call trial | Verified 2026-10-11 |
| [Airtop](https://www.airtop.ai/pricing) | unconfirmed | Free plan advertises 1,000 credits and a 10,000-credit trial bonus | Needs review |
| [Anchor Browser](https://anchorbrowser.io/) | recurring | 5 credits per month | Verified 2026-10-11 |
| [Browser Use Cloud](https://browser-use.com/pricing) | trial | $1 one-time credit for eligible signups | Verified 2026-10-11 |
| [Browserbase](https://www.browserbase.com/pricing) | unconfirmed | Free plan includes 1 browser hour, 3 agent runs, 1,000 search calls and 1,000 fetch calls | Needs review |
| [Browserless](https://www.browserless.io/pricing) | recurring | 1,000 units per month | Verified 2026-10-11 |
| [Hyperbrowser](https://www.hyperbrowser.ai/pricing) | unconfirmed | Free plan advertises 5,000 credits; reset unclear | Needs review |
| [Notte](https://www.notte.cc/pricing) | trial | $10 one-time credits with no expiry | Verified 2026-10-11 |
| [Steel](https://steel.dev/pricing) | trial | $30 one-time credits | Verified 2026-10-11 |

### Model inference

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/) | recurring | 10,000 neurons per day | Verified 2026-10-11 |
| [Cohere](https://docs.cohere.com/docs/rate-limits) | trial | Free evaluation API keys with usage limits | Verified 2026-10-11 |
| [Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | recurring | Free tier for selected models with usage limits | Verified 2026-10-11 |
| [Groq](https://community.groq.com/t/do-i-get-charged-for-anything-on-the-groq-free-plan/832) | recurring | Free API plan with model-specific rate limits | Verified 2026-10-11 |
| [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/main/pricing) | recurring | $0.10 monthly credit for free users | Verified 2026-10-11 |
| [OpenRouter](https://openrouter.ai/support) | recurring | Free model variants with low rate limits | Verified 2026-10-11 |

### Speech & voice

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [AssemblyAI](https://support.assemblyai.com/articles/5370767329-can-i-sign-up-for-free) | trial | $50 trial credits | Verified 2026-10-11 |
| [Cartesia](https://www.cartesia.ai/pricing) | recurring | 20,000 model credits per month plus $1 monthly agent allowance | Verified 2026-10-11 |
| [Deepgram](https://deepgram.com/pricing) | trial | $200 starting credit | Verified 2026-10-11 |
| [ElevenLabs](https://elevenlabs.io/pricing/api) | recurring | Free plan includes API access; endpoint allowance varies | Verified 2026-10-11 |

### Realtime audio & video

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Daily](https://www.daily.co/pricing/video-sdk/) | recurring | First 10,000 participant minutes per month free | Verified 2026-10-11 |

### Image & video generation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [fal](https://fal.ai/builder-grant) | grant | Builder grants by application; no universal signup credit confirmed | Verified 2026-10-11 |
| [Replicate](https://replicate.com/pricing) | paid | Usage-based API; universal free credit not confirmed | Verified 2026-10-11 |
| [Runware](https://runware.ai/pricing) | trial | $2 starting credits for business-email signups | Verified 2026-10-11 |
| [Runway API](https://docs.dev.runwayml.com/guides/setup/) | paid | Paid API; $10 minimum starting payment | Verified 2026-10-11 |

### Document parsing & OCR

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [LandingAI](https://landing.ai/pricing-agentic-apis) | trial | 1,000 starting credits advertised | Verified 2026-10-11 |
| [LlamaParse](https://www.llamaindex.ai/pricing) | recurring | Free document-processing tier; mode-dependent credits | Verified 2026-10-11 |
| [Reducto](https://reducto.ai/pricing) | trial | $150 free starting usage on Standard | Verified 2026-10-11 |
| [Unstructured](https://unstructured.io/pricing) | trial | 10,000 free starting pages | Verified 2026-10-11 |

### Screenshots, PDFs & rendering

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Bannerbear](https://www.bannerbear.com/pricing/) | trial | 30 trial API credits | Verified 2026-10-11 |
| [PDFShift](https://pdfshift.io/pricing/) | recurring | 50 conversion credits per month | Verified 2026-10-11 |
| [ScreenshotOne](https://screenshotone.com/ai-information/) | recurring | 100 screenshots per month | Verified 2026-10-11 |
| [Shotstack](https://shotstack.io/docs/guide/getting-started/request-api-keys/) | trial | 10 starting credits valid for 30 days | Verified 2026-10-11 |

### Sandboxes & compute

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Blaxel](https://blaxel.ai/pricing) | trial | Up to $200 starting credits | Verified 2026-10-11 |
| [Daytona](https://www.daytona.io/pricing) | trial | $200 starting compute credit | Verified 2026-10-11 |
| [E2B](https://e2b.dev/pricing) | trial | $100 one-time usage credit | Verified 2026-10-11 |
| [Modal](https://modal.com/pricing) | recurring | $30 compute credit per month | Verified 2026-10-11 |

### Agent memory

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Mem0](https://mem0.ai/pricing) | recurring | 10,000 add requests and 1,000 retrieval requests per month | Verified 2026-10-11 |
| [Supermemory](https://supermemory.ai/pricing/) | recurring | $5 credits per month | Verified 2026-10-11 |
| [Zep](https://www.getzep.com/pricing/) | unconfirmed | Free memory tier; limits require confirmation | Needs review |

### Embeddings & vector databases

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Pinecone](https://www.pinecone.io/pricing/) | recurring | Free Starter plan with included usage | Verified 2026-10-11 |
| [Qdrant](https://qdrant.tech/cloud/) | recurring | Free single-node cluster: 1 GB RAM and 4 GB disk | Verified 2026-10-11 |
| [Voyage AI](https://docs.voyageai.com/docs/pricing) | trial | 200 million free tokens for selected current models; other models differ | Verified 2026-10-11 |
| [Weaviate](https://weaviate.io/pricing) | recurring | Always-free shared tier with 100,000 objects and one collection | Verified 2026-10-11 |

### App integrations & auth

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Arcade](https://www.arcade.dev/pricing/) | recurring | 2,000 auth events and 2,000 tool calls per month | Verified 2026-10-11 |
| [Composio](https://composio.dev/pricing) | recurring | 100,000 tool calls and 50,000 triggers per month | Verified 2026-10-11 |
| [Nango](https://nango.dev/pricing) | recurring | Free plan with hard-capped monthly limits | Verified 2026-10-11 |
| [Pipedream](https://pipedream.com/pricing) | trial | Free development access; production is paid | Verified 2026-10-11 |

### Email

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Brevo](https://www.brevo.com/products/transactional-email/) | recurring | 300 emails per day through API/SMTP | Verified 2026-10-11 |
| [Resend](https://resend.com/pricing) | recurring | 3,000 emails per month with 100-per-day limit | Verified 2026-10-11 |

### Data enrichment

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Hunter](https://help.hunter.io/en/articles/11131690-pricing-plans-and-feature-faqs) | recurring | 50 credits per month | Verified 2026-10-11 |
| [People Data Labs](https://www.peopledatalabs.com/pricing/person) | recurring | Up to 100 person records per month | Verified 2026-10-11 |

### Tracing & evaluation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Braintrust](https://www.braintrust.dev/pricing) | recurring | Free included trace/evaluation usage | Verified 2026-10-11 |
| [Helicone](https://www.helicone.ai/pricing) | recurring | 10,000 monitored requests per month on Hobby | Verified 2026-10-11 |
| [Langfuse](https://langfuse.com/pricing) | recurring | 50,000 units per month | Verified 2026-10-11 |
| [LangSmith](https://www.langchain.com/pricing) | recurring | 5,000 base traces per month and one seat | Verified 2026-10-11 |

### Translation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [DeepL](https://support.deepl.com/hc/en-us/articles/360021200939-DeepL-API-plans) | recurring | 500,000 characters per month | Verified 2026-10-11 |

### Maps & geocoding

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Geoapify](https://www.geoapify.com/pricing/) | recurring | 3,000 credits per day | Verified 2026-10-11 |

### Weather

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [OpenWeather](https://openweathermap.org/api/one-call-3) | recurring | One Call: first 1,000 calls per day free | Verified 2026-10-11 |

### Financial data

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Alpha Vantage](https://www.alphavantage.co/support/) | recurring | 25 requests per day for most datasets | Verified 2026-10-11 |

