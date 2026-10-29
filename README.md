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

107 providers across 25 categories. Snapshot: 2026-10-29. 103 offers reviewed against official evidence; 4 need further confirmation. Review dates below do not update themselves.

### Search & research

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Brave Search](https://brave.com/search/api/) | recurring | $5 monthly credits listed for Search and $5 for Answers; broader headline advertises up to $20 | Verified 2026-10-26 |
| [Exa](https://exa.ai/pricing) | recurring | $10 monthly credits plus $10 onboarding bonus | Verified 2026-10-20 |
| [Hyperbrowser](https://www.hyperbrowser.ai/pricing) | unconfirmed | 5,000 credits included with a free account; free-plan renewal period unclear | Needs review |
| [Keenable](https://keenable.ai/pricing) | recurring | 100,000 free search requests per month | Verified 2026-10-26 |
| [Linkup](https://www.linkup.so/pricing) | unconfirmed | 4,000 free queries advertised; reset and expiry unclear | Needs review |
| [Parallel](https://parallel.ai/blog/free-tier-parallel) | recurring | $5 monthly credits for eligible organizations | Verified 2026-10-26 |
| [Perplexity API](https://docs.perplexity.ai/docs/getting-started/pricing) | paid | Paid API; universal free allowance not confirmed | Verified 2026-10-26 |
| [SearchApi](https://www.searchapi.io/) | trial | 100 starting requests | Verified 2026-10-29 |
| [SerpApi](https://serpapi.com/pricing) | recurring | 250 searches per month | Verified 2026-10-23 |
| [Serper](https://serper.dev/) | trial | 2,500 starting queries | Verified 2026-10-11 |
| [Tavily](https://www.tavily.com/pricing) | recurring | 1,000 API credits per month | Verified 2026-10-23 |
| [Valyu](https://www.valyu.ai/pricing) | trial | $10 signup credit, or $20 with a work email | Verified 2026-10-26 |
| [You.com](https://you.com/product/web-search-api) | recurring | 100 keyless MCP search queries per day; separate $100 signup credit | Verified 2026-10-26 |

### Scraping & extraction

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Apify](https://apify.com/pricing) | recurring | $5 platform usage per month | Verified 2026-10-26 |
| [Bright Data](https://brightdata.com/pricing/web-scraper) | recurring | 5,000 Web Scraper API records per month | Verified 2026-10-29 |
| [Cloudflare Browser Run](https://developers.cloudflare.com/browser-run/pricing/) | recurring | 10 browser minutes per day on Workers Free; 3 concurrent browser sessions | Verified 2026-10-29 |
| [Firecrawl](https://www.firecrawl.dev/pricing) | recurring | 1,000 credits per month | Verified 2026-10-26 |
| [Hyperbrowser](https://www.hyperbrowser.ai/pricing) | unconfirmed | 5,000 credits included with a free account; free-plan renewal period unclear | Needs review |
| [Jina Reader](https://jina.ai/reader/) | trial | Free rate-limited access; 10 million starting tokens with a new key | Verified 2026-10-20 |
| [Olostep](https://www.olostep.com/pricing) | trial | 500 successful trial requests | Verified 2026-10-26 |
| [Oxylabs](https://oxylabs.io/products/web-api/scrape/web) | trial | $5 one-time welcome credit per new team | Verified 2026-10-26 |
| [Scrape.do](https://scrape.do/pricing/) | recurring | 1,000 successful API credits per month | Verified 2026-10-17 |
| [ScrapeGraphAI](https://scrapegraphai.com/pricing) | trial | 500 one-time credits | Verified 2026-10-17 |
| [ScraperAPI](https://www.scraperapi.com/pricing/) | trial | 5,000 API credits for a 7-day trial | Verified 2026-10-14 |
| [ScrapingAnt](https://scrapingant.com/price-scraping-api) | recurring | 10,000 free API credits per month | Verified 2026-10-23 |
| [ScrapingBee](https://www.scrapingbee.com/pricing/) | trial | 1,000 trial credits | Verified 2026-10-17 |
| [Scrapingdog](https://www.scrapingdog.com/pricing/) | unconfirmed | 100 free credits; provider calls this a trial and monthly renewal is unclear | Needs review |
| [ZenRows](https://www.zenrows.com/pricing) | recurring | 5,000 credits per month on Free | Verified 2026-10-23 |
| [Zyte](https://docs.zyte.com/zyte-api/pricing.html) | trial | $5 initial credit, for first billing month | Verified 2026-10-26 |

### Browser automation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [AgentQL](https://www.agentql.com/pricing) | recurring | 50 API calls per month; separate 300-call trial | Verified 2026-10-11 |
| [Airtop](https://www.airtop.ai/pricing) | unconfirmed | Shutdown announced for November 13; advertised free-credit terms remain unconfirmed | Needs review |
| [Anchor Browser](https://anchorbrowser.io/) | recurring | 5 credits per month | Verified 2026-10-29 |
| [Browser Use Cloud](https://browser-use.com/pricing) | trial | $1 one-time credit for eligible signups | Verified 2026-10-26 |
| [Browserbase](https://www.browserbase.com/pricing) | recurring | 1 browser hour per month; Free plan also lists 3 agent runs, 1,000 search calls and 1,000 fetch calls | Verified 2026-10-20 |
| [Browserless](https://www.browserless.io/pricing) | recurring | 1,000 units per month | Verified 2026-10-26 |
| [Cloudflare Browser Run](https://developers.cloudflare.com/browser-run/pricing/) | recurring | 10 browser minutes per day on Workers Free; 3 concurrent browser sessions | Verified 2026-10-29 |
| [Hyperbrowser](https://www.hyperbrowser.ai/pricing) | unconfirmed | 5,000 credits included with a free account; free-plan renewal period unclear | Needs review |
| [Notte](https://www.notte.cc/pricing) | trial | $10 one-time credits with no expiry | Verified 2026-10-23 |
| [Steel](https://steel.dev/pricing) | trial | $30 one-time credits | Verified 2026-10-29 |

### Model inference

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Cerebras Inference](https://www.cerebras.ai/pricing) | trial | $5 one-time promotional credit, valid for 30 days | Verified 2026-10-23 |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/) | recurring | 10,000 neurons per day | Verified 2026-10-26 |
| [Cohere](https://docs.cohere.com/docs/rate-limits) | trial | Free evaluation API keys with usage limits | Verified 2026-10-11 |
| [Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | recurring | Free tier for selected models with usage limits | Verified 2026-10-26 |
| [Groq](https://community.groq.com/t/do-i-get-charged-for-anything-on-the-groq-free-plan/832) | recurring | Free API plan with model-specific rate limits | Verified 2026-10-11 |
| [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/main/pricing) | paid | No monthly inference credit for free accounts; credit purchase or a paid subscription required | Verified 2026-10-26 |
| [Mistral API](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key) | recurring | Default Free mode with limited API usage; no fixed universal token grant published | Verified 2026-10-23 |
| [OpenRouter](https://openrouter.ai/support) | recurring | Free model variants with low rate limits | Verified 2026-10-26 |

### Speech & voice

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [AssemblyAI](https://support.assemblyai.com/articles/5370767329-can-i-sign-up-for-free) | trial | $50 trial credits | Verified 2026-10-29 |
| [Cartesia](https://www.cartesia.ai/pricing) | recurring | 20,000 model credits per month plus $1 monthly agent allowance | Verified 2026-10-26 |
| [Deepgram](https://deepgram.com/pricing) | trial | $200 starting credit | Verified 2026-10-20 |
| [ElevenLabs](https://elevenlabs.io/pricing/api) | recurring | Free plan includes API access; endpoint allowance varies | Verified 2026-10-23 |
| [Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | recurring | Free tier for selected models with usage limits | Verified 2026-10-26 |
| [Speechmatics](https://www.speechmatics.com/pricing) | trial | $100 starting transcription credits | Verified 2026-10-14 |
| [Twilio](https://www.twilio.com/docs/usage/trials) | trial | 30-day trial: 100 SMS, 100 WhatsApp messages, 75 voice minutes and 3,000 emails | Verified 2026-10-26 |

### Realtime audio & video

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Daily](https://www.daily.co/pricing/video-sdk/) | recurring | First 10,000 participant minutes per month free | Verified 2026-10-11 |

### Image & video generation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [fal](https://fal.ai/startup-program) | grant | $1,000 startup grant on approval, with conditional growth to $5,000 | Verified 2026-10-23 |
| [Replicate](https://replicate.com/pricing) | paid | Usage-based API; universal free credit not confirmed | Verified 2026-10-11 |
| [Runware](https://runware.ai/pricing) | trial | $2 starting credits for business-email signups | Verified 2026-10-26 |
| [Runway API](https://docs.dev.runwayml.com/guides/setup/) | paid | Paid API; $10 minimum starting payment | Verified 2026-10-11 |

### Document parsing & OCR

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Google Sheets API](https://developers.google.com/workspace/sheets/api/limits) | recurring | Standard API use at no extra cost; 300 reads and 300 writes per minute per project | Verified 2026-10-17 |
| [LandingAI](https://landing.ai/pricing-agentic-apis) | trial | 1,000 starting credits advertised | Verified 2026-10-11 |
| [LlamaParse](https://www.llamaindex.ai/pricing) | recurring | 10,000 document-processing credits per month; 5 concurrent parse jobs | Verified 2026-10-26 |
| [Reducto](https://reducto.ai/pricing) | trial | $150 free starting usage on Standard | Verified 2026-10-11 |
| [ScrapeGraphAI](https://scrapegraphai.com/pricing) | trial | 500 one-time credits | Verified 2026-10-17 |
| [Unstructured](https://unstructured.io/pricing) | trial | 10,000 free starting pages | Verified 2026-10-26 |

### Screenshots, PDFs & rendering

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Bannerbear](https://www.bannerbear.com/pricing/) | trial | 30 trial API credits | Verified 2026-10-23 |
| [Cloudflare Browser Run](https://developers.cloudflare.com/browser-run/pricing/) | recurring | 10 browser minutes per day on Workers Free; 3 concurrent browser sessions | Verified 2026-10-29 |
| [PDFShift](https://pdfshift.io/pricing/) | recurring | 50 conversion credits per month | Verified 2026-10-29 |
| [ScreenshotOne](https://screenshotone.com/ai-information/) | recurring | 100 screenshots per month | Verified 2026-10-11 |
| [Shotstack](https://shotstack.io/docs/guide/getting-started/request-api-keys/) | trial | 10 starting credits valid for 30 days | Verified 2026-10-11 |

### Sandboxes & compute

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Blaxel](https://blaxel.ai/pricing) | trial | Up to $200 starting credits | Verified 2026-10-20 |
| [Cloudflare Workers](https://developers.cloudflare.com/workers/platform/pricing/) | recurring | 100,000 requests per day with 10 ms CPU time per invocation | Verified 2026-10-17 |
| [Daytona](https://www.daytona.io/pricing) | trial | $200 starting compute credit | Verified 2026-10-11 |
| [E2B](https://e2b.dev/pricing) | trial | $100 one-time usage credit | Verified 2026-10-29 |
| [Hyperbrowser](https://www.hyperbrowser.ai/pricing) | unconfirmed | 5,000 credits included with a free account; free-plan renewal period unclear | Needs review |
| [Modal](https://modal.com/pricing) | recurring | $30 compute credit per month | Verified 2026-10-26 |

### Agent memory

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Mem0](https://mem0.ai/pricing) | recurring | 10,000 add requests and 1,000 retrieval requests per month | Verified 2026-10-11 |
| [Supermemory](https://supermemory.ai/pricing/) | recurring | $5 credits per month | Verified 2026-10-29 |
| [Zep](https://www.getzep.com/pricing/) | recurring | 10,000 credits per month | Verified 2026-10-23 |

### Embeddings & vector databases

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | recurring | Free tier for selected models with usage limits | Verified 2026-10-26 |
| [Pinecone](https://www.pinecone.io/pricing/) | recurring | Free Starter: 2 GB database storage, 1M read units and 2M write units per month | Verified 2026-10-17 |
| [Qdrant](https://qdrant.tech/cloud/) | recurring | Free single-node cluster: 1 GB RAM and 4 GB disk | Verified 2026-10-26 |
| [Voyage AI](https://docs.voyageai.com/docs/pricing) | trial | 200 million free tokens for selected current models; other models differ | Verified 2026-10-23 |
| [Weaviate](https://weaviate.io/pricing) | recurring | Always-free cluster: 100,000 objects, 1 GB memory and 10 GB disk; separate embedding and Query Agent quotas | Verified 2026-10-20 |

### App integrations & auth

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Arcade](https://www.arcade.dev/pricing/) | recurring | 2,000 auth events and 2,000 tool calls per month | Verified 2026-10-20 |
| [Composio](https://composio.dev/pricing) | recurring | 100,000 tool calls and 50,000 triggers per month | Verified 2026-10-29 |
| [Nango](https://nango.dev/pricing) | recurring | 10 connected accounts, plus 10 compute hours and 10 GB data transfer per month | Verified 2026-10-26 |
| [Pipedream](https://pipedream.com/pricing) | trial | Free development access; production is paid | Verified 2026-10-11 |

### Email

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Brevo](https://www.brevo.com/products/transactional-email/) | recurring | 300 emails per day through API/SMTP | Verified 2026-10-23 |
| [Loops](https://loops.so/pricing) | recurring | 4,000 combined marketing and transactional sends per rolling 30 days | Verified 2026-10-29 |
| [Resend](https://resend.com/pricing) | recurring | 3,000 emails per month with 100-per-day limit | Verified 2026-10-20 |
| [Twilio](https://www.twilio.com/docs/usage/trials) | trial | 30-day trial: 100 SMS, 100 WhatsApp messages, 75 voice minutes and 3,000 emails | Verified 2026-10-26 |

### Data enrichment

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Abstract API](https://www.abstractapi.com/pricing) | recurring | 100 email validations, 100 phone validations and 1,000 IP geolocation requests per month | Verified 2026-10-20 |
| [Hunter](https://help.hunter.io/en/articles/11131690-pricing-plans-and-feature-faqs) | recurring | 50 credits per month | Verified 2026-10-11 |
| [People Data Labs](https://www.peopledatalabs.com/pricing/person) | recurring | Up to 100 person records per month | Verified 2026-10-11 |

### Tracing & evaluation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Braintrust](https://www.braintrust.dev/pricing) | recurring | Free included trace/evaluation usage | Verified 2026-10-11 |
| [Helicone](https://www.helicone.ai/pricing) | recurring | 10,000 monitored requests per month on Hobby | Verified 2026-10-23 |
| [Langfuse](https://langfuse.com/pricing) | recurring | 50,000 units per month | Verified 2026-10-29 |
| [LangSmith](https://www.langchain.com/pricing) | recurring | 5,000 base traces per month and one seat | Verified 2026-10-11 |
| [PostHog](https://posthog.com/pricing) | recurring | Monthly: 1 million analytics events, 1 million feature-flag requests, 5,000 replays and 100,000 exceptions | Verified 2026-10-26 |

### Translation

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [DeepL](https://support.deepl.com/hc/en-us/articles/360021200939-DeepL-API-plans) | trial | 1,000,000 one-time translation characters; does not reset | Verified 2026-10-29 |

### Maps & geocoding

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Geoapify](https://www.geoapify.com/pricing/) | recurring | 3,000 credits per day | Verified 2026-10-11 |

### Weather

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [OpenWeather](https://openweathermap.org/api/one-call-3) | recurring | One Call: first 1,000 calls per day free | Verified 2026-10-26 |

### Financial data

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Alpha Vantage](https://www.alphavantage.co/support/) | recurring | 25 requests per day for most datasets | Verified 2026-10-26 |

### Object storage

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Backblaze B2](https://www.backblaze.com/cloud-storage/pricing) | recurring | First 10 GB of storage free; monthly egress up to 3 times average stored data | Verified 2026-10-23 |
| [Cloudflare R2](https://developers.cloudflare.com/r2/pricing/) | recurring | 10 GB-month storage, 1 million Class A operations and 10 million Class B operations per month | Verified 2026-10-14 |
| [Cloudinary](https://cloudinary.com/pricing) | recurring | 25 shared credits with rolling 30-day usage accounting | Verified 2026-10-23 |
| [ImageKit](https://imagekit.io/plans/) | recurring | 20 GB bandwidth, 500 video units and 650 extension units per month; 3 GB storage | Verified 2026-10-23 |
| [Tigris](https://www.tigrisdata.com/pricing/) | recurring | Monthly: 5 GB of Standard storage, 10,000 Class A and 100,000 Class B requests | Verified 2026-10-23 |

### Databases & cache

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Airtable](https://support.airtable.com/articles/7735693959-managing-api-call-limits-in-airtable) | recurring | 1,000 API calls per workspace per calendar month on Free | Verified 2026-10-29 |
| [Cloud Firestore](https://firebase.google.com/docs/firestore/pricing) | recurring | 1 GiB storage; 50,000 reads, 20,000 writes and 20,000 deletes per day; 10 GiB outbound per month | Verified 2026-10-26 |
| [Cloudflare D1](https://developers.cloudflare.com/d1/platform/pricing/) | recurring | 5M rows read and 100,000 rows written per day; 5 GB total storage | Verified 2026-10-17 |
| [Neon](https://neon.com/pricing) | recurring | 100 CU-hours per project per month and 1 GB database storage per project; up to 100 projects | Verified 2026-10-26 |
| [Turso](https://turso.tech/pricing) | recurring | 500M rows read and 10M rows written per month; 5 GB storage and 100 databases | Verified 2026-10-26 |
| [Upstash Redis](https://upstash.com/pricing/redis) | recurring | 250 MB database storage, 500,000 commands and 10 GB bandwidth per month | Verified 2026-10-26 |

### Developer tools

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Cloudflare Workers](https://developers.cloudflare.com/workers/platform/pricing/) | recurring | 100,000 requests per day with 10 ms CPU time per invocation | Verified 2026-10-17 |
| [GitHub API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) | recurring | 5,000 REST requests per hour for ordinary authenticated user access; 60 per hour for unauthenticated public access | Verified 2026-10-26 |
| [PostHog](https://posthog.com/pricing) | recurring | Monthly: 1 million analytics events, 1 million feature-flag requests, 5,000 replays and 100,000 exceptions | Verified 2026-10-26 |

### Business APIs

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Abstract API](https://www.abstractapi.com/pricing) | recurring | 100 email validations, 100 phone validations and 1,000 IP geolocation requests per month | Verified 2026-10-20 |
| [Airtable](https://support.airtable.com/articles/7735693959-managing-api-call-limits-in-airtable) | recurring | 1,000 API calls per workspace per calendar month on Free | Verified 2026-10-29 |
| [Google Sheets API](https://developers.google.com/workspace/sheets/api/limits) | recurring | Standard API use at no extra cost; 300 reads and 300 writes per minute per project | Verified 2026-10-17 |
| [Loops](https://loops.so/pricing) | recurring | 4,000 combined marketing and transactional sends per rolling 30 days | Verified 2026-10-29 |
| [Twilio](https://www.twilio.com/docs/usage/trials) | trial | 30-day trial: 100 SMS, 100 WhatsApp messages, 75 voice minutes and 3,000 emails | Verified 2026-10-26 |

### Image & video processing

| Provider | Offer | Published allowance | Evidence / review |
|---|---|---|---|
| [Cloudinary](https://cloudinary.com/pricing) | recurring | 25 shared credits with rolling 30-day usage accounting | Verified 2026-10-23 |
| [ImageKit](https://imagekit.io/plans/) | recurring | 20 GB bandwidth, 500 video units and 650 extension units per month; 3 GB storage | Verified 2026-10-23 |

