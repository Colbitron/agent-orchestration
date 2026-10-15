# Model gaps: profiles for models missing from the routing table

**As of 2026-10-02.** Web research done on that date. Haiku entries updated 2026-10-08 for the Haiku 5.5 launch (official pricing page plus `research/claude-releases.md` Video 4).

## How to read this

- These profiles come from **web research only**: vendor docs, pricing pages, model cards, launch posts and third-party benchmark sites. None of the models were run hands-on. The other profiles in this folder come from video transcripts of people using the models; treat these as lower-fidelity.
- **Vendor benchmark numbers are self-reported.** Where an independent number exists (mostly Artificial Analysis, "AA"), it is given next to the vendor number.
- **"unverified"** means only one non-vendor source gave the number, sources disagreed, or no source was found. Do not hard-code these numbers into routing logic without checking them.
- **Baseline for routing advice:** Claude Opus 5.5 (`claude-opus-5-5`, $4 / $20 per MTok, cache hit $0.20 (unchanged at the Haiku 5.5 launch, which cut only Sonnet 5.5's cache reads), 1M context, 128K output; AA Intelligence Index 54 at `high`, about 80 tok/s, about $1.82 per AA task). [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), [AA leaderboard](https://artificialanalysis.ai/leaderboards/models)
- **About AA "cost per task":** this is AA's measured USD cost to run one Intelligence Index task at the prices in force on the measurement date. It includes each model's token verbosity, so it shows real cost better than list price does. Promotional prices skew it.

---

## Naming corrections (read first)

| What our notes say | What is current (2026-10-02) | Source |
|---|---|---|
| "Claude Haiku 4.5 / Haiku 5.x" | **Haiku 5.5 shipped about 2026-10-07** with ID `claude-haiku-5-5` and is now the current Haiku. Haiku 4.5 is superseded; its retirement date is "not sooner than **October 15, 2026**". There was never a Haiku 5. (Updated 2026-10-08; Haiku 5.5 was announced 2026-09-22 as coming "in the coming weeks".) | [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [Mike Krieger on X](https://x.com/mikeyk/status/2102441803253535060), [cellcog](https://cellcog.ai/blog/claude-haiku-5-5-release-date/) |
| "Gemini 3.x Pro" | The best *generally available* Gemini for coding is **Gemini 3.8 Flash** (GA 2026-09-02). **Gemini 3.5 Pro was announced at I/O in May and never shipped.** **Gemini 3.1 Pro is still "preview"** and now scores below 3.8 Flash. **Gemini 4 Argon** was announced 2026-09-30 and is in restricted access only. | [Gemini models](https://ai.google.dev/gemini-api/docs/models), [Google blog: 3.8 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/), [Google blog: Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) |
| "Grok 4.7" / "GrokBuild" | **Grok 4.7** (`grok-4.7`, 2026-09-21) is current. **Grok Build** is the terminal agent (CLI binary `grok`). **grok-build-0.1** is a separate, cheaper coding model. xAI now brands itself "SpaceXAI" in places. | [xAI Grok 4.7 docs](https://docs.x.ai/developers/grok-4-7), [Grok Build docs](https://docs.x.ai/build/overview) |
| "GPT-5.6 Sol vs GPT-6.1 Sol" | **Both exist.** GPT-5.6 Sol (`gpt-5.6-sol`, released 2026-07-09, $4/$20) is the **previous** generation. Then came **GPT-6 Sol** (2026-09-22) and **GPT-6.1 Sol** (`gpt-6.1-sol`, 2026-09-29, $2/$10). **GPT-6.1 Sol is the current Sol.** "Sol" is often mis-captioned as "Soul". | [OpenAI models](https://developers.openai.com/api/docs/models), [OpenAI gpt-6.1-sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [OpenAI gpt-5.6-sol model page](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-gpt-6-1-sol-says-it-nearly-matches-gpt-6-astra-and-costs-less/), [Wikipedia: GPT-5.6](https://en.wikipedia.org/wiki/GPT-5.6) |
| "Qwen3-Coder", "DeepSeek V3.x / R-series", "Kimi K2.x", "GLM 5.x" | These are now **Qwen3.8-Max** (open weights since 2026-08-13), **DeepSeek V4.1 Flash** (`deepseek-flash`, 2026-09-10) and **V4 Pro**, **Kimi K3** (2026-07-16), and **GLM-5.3** (2026-08-14). The open-weights leader on AA is a newcomer, **Xiaomi MiMo-V2.6-Pro** (2026-09-21). | see each profile |
| "gpt-oss" | Still the **August 2025** gpt-oss-120b / gpt-oss-20b. There is no new generation (one source claims a June 2026 refresh; not confirmed). It is far behind the 2026 open-weights models. | [frankx.ai](https://www.frankx.ai/blog/gpt-oss-analysis-2026) |
| (not in our notes) | **GPT-6 Luna** (`gpt-6-luna`, $0.10/$0.50, AA 38 at about $0.07 per task) is a very cheap OpenAI tier worth a profile of its own. | [OpenAI models](https://developers.openai.com/api/docs/models), [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) |

---

## At-a-glance comparison

Prices are list prices in USD per 1M tokens (input / cached input / output). "AA II" is the Artificial Analysis Intelligence Index, and "AA $/task" is AA's measured cost per index task. AA numbers come from the [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) on 2026-10-02.

| Model | Open weights? | Price in / cache / out | Context / max out | AA II | AA tok/s | AA $/task |
|---|---|---|---|---|---|---|
| *Baseline: Claude Opus 5.5 (high)* | no | 4 / 0.20 / 20 | 1M / 128K | 54 | 80 | 1.82 |
| *Ref: GPT-6.1 Sol (high)* | no | 2 / 0.10 / 10 | 1.05M / 128K | 50 | 50 | 0.32 |
| Claude Haiku 4.5 (superseded) | no | 1 / 0.10 / 5 | 200K / 64K | 17 | 103 | 0.28 |
| Claude Haiku 5.5 | no | 0.10 / 0.01 / 0.50 for prompts ≤100K tokens; 5x above 100K (0.50 / 0.05 / 2.50) | 1M / 128K | not found | 100-200 (reported, provider-dependent; not an AA figure) | unverified |
| Gemini 3.8 Flash (high) | no | 0.75 / 0.075 / 3.75 (intro, until 2026-12-31; then 1.50 / 0.15 / 7.50) | 1M / 64K | 41 | 305 (AA, via Vellum) | unverified |
| Gemini 4 Argon (high) | no | 2 / 0.10 / 10 (intro; standard 4 / 20) | 1M output limit; context unverified | 53 | not listed | 1.99 |
| Gemini 3.1 Pro Preview | no | 2 / 0.20 / 12 (≤200K) | unverified | 30 | 116 | 0.67 |
| Grok 4.7 (xhigh) | no | 2 / 0.50 / 6 (doubles ≥200K) | 500K / no stated limit | 46 | 79 (AA article says 188; conflict) | 3.74 |
| grok-build-0.1 | no | 1 / 0.20 / 2 | 256K | not listed | "100+" (vendor) | not listed |
| GPT-6 Luna (max) | no | 0.10 / unverified / 0.50 | 1.05M / 128K | 38 | unverified | 0.07 |
| MiMo-V2.6-Pro (Xiaomi) | yes (MIT) | 0.435 / 0.0036 / 0.87 | 1M | 46 | 45 | 0.13 |
| GLM-5.3 (max) | yes (custom licence) | 1.40 / 0.26 / 4.40 | 1M / 128K | 45 | 74 | 2.01 |
| GLM-5.3-Flash | yes | 0.15 / 0.03 / 0.50 | 1M (unverified) | 42 (AA open-weights page) | unverified | about 0.1 (unverified) |
| Qwen3.8-Max | yes (custom, revenue share) | unverified | API 1M (unverified); weights smaller | 45 | 38 | 5.41 |
| Kimi K3 (max) | yes (modified MIT) | 3.00 / 0.30 / 15.00 | 1M / 1M (default 131K) | 44 | 36 | 2.00 |
| DeepSeek V4.1 Flash | yes (MIT) | 0.15 / 0.003 / 0.60 off-peak; ×2 at peak | 1M / 384K | 39 | unverified | unverified |
| DeepSeek V4 Pro | yes (MIT) | 0.66 / 0.022 / 1.98 off-peak; ×2 at peak | 1M / 384K | 36 | 109 | 0.67 |
| MiniMax M3 | yes (licence conflicts) | unverified (0.28 / 0.056 / 1.10 or 0.60 / — / 2.40) | 1M / 524K (unverified) | 29 | 84 | 0.51 |
| gpt-oss-120b (high) | yes (Apache 2.0) | host-dependent | 128K (unverified) | 12 | 160 | 0.11 |

**Main takeaway from the table:** at about $0.32 per task and AA 50, **GPT-6.1 Sol beats every open-weights model on capability and most of them on measured cost.** The open-weights models that stay cheaper per task than Sol are **MiMo-V2.6-Pro**, **GLM-5.3-Flash** and **DeepSeek V4.1 Flash**. **GPT-6 Luna** ($0.07 per task at AA 38) undercuts most of them. This rests on one benchmark aggregator, so check it on your own tasks.

---

## 1. Claude Haiku 4.5 (superseded) and Claude Haiku 5.5

**Confidence: HIGH** for the specs (Anthropic docs). **MEDIUM** for routing advice: no hands-on use here, and the Haiku 5.5 advice rests on one launch-day video (`research/claude-releases.md` Video 4).

The Haiku 4.5 facts below are kept for history. Haiku 5.5 replaced it on about 2026-10-07.

- **Model IDs:** `claude-haiku-4-5-20251001` (pinned) and alias `claude-haiku-4-5`. Bedrock: `anthropic.claude-haiku-4-5`. Vertex: `claude-haiku-4-5@20251001`.
- **Released:** 2025-10-15. **Retirement:** "not sooner than October 15, 2026", so it could be retired from about two weeks from now.
- **Pricing:** $1 input, $0.10 cache hit, $1.25 for a 5-minute cache write, $2 for a 1-hour cache write, $5 output. Batch: $0.50 / $2.50.
- **Subscriptions:** available in claude.ai apps and Claude Code at launch (per the Anthropic announcement). Exact plan gating today is unverified.
- **Context / output:** 200K context and 64K max output. That is the smallest window in the Claude lineup; Opus, Sonnet and Fable have 1M.
- **Knowledge cutoff:** reliable to Feb 2025 (training data to Jul 2025). This is old, so it will not know 2026 APIs.
- **Speed:** "Fastest" in Anthropic's lineup. AA measures 103 tok/s.
- **Reasoning:** uses *extended* thinking (`thinking: {type: "enabled", budget_tokens: N}`). The `effort` parameter is **not supported**.
- **Strengths:** cheap, fast sub-agent work (Anthropic names sub-agent orchestration, pair programming and real-time apps). It reached 73.3% on SWE-bench Verified at launch (vendor, Oct 2025). That is now an old benchmark generation.
- **Weaknesses:** AA Intelligence Index **17**, far below Gemini 3.8 Flash (41), GPT-6 Luna (38) and DeepSeek V4.1 Flash (39). Its AA cost per task ($0.28) is about the same as GPT-6.1 Sol's ($0.32), which scores 50. The old knowledge cutoff and 200K context also hurt on large repos.
- **Invocation:**
  - Claude Code one-shot: `claude -p "summarise the changes in src/auth" --model haiku` (the alias `haiku` resolves to the current Haiku; non-interactive with `-p`).
  - API: `curl https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-haiku-4-5","max_tokens":4096,"messages":[{"role":"user","content":"..."}]}'`
  - Scriptable: yes.
- **Haiku 5.5:** announced 2026-09-22 alongside Opus 5.5, shipped about 2026-10-07. Values from the official pricing page and the Claude API reference (fetched 2026-10-06 to 2026-10-08):
  - ID: `claude-haiku-5-5` | Price (≤100K prompt tokens): $0.10 input / $0.01 cache hit / $0.50 output; 5-minute cache write $0.125, 1-hour $0.20; batch $0.05 / $0.25 | Price (>100K prompt tokens): 5x, i.e. $0.50 / $0.05 / $2.50, cache writes $0.625 / $1.00, batch $0.25 / $1.25 | Context: 1M | Max out: 128K | Effort support: low / medium / high / xhigh / max, default `medium`; adaptive thinking on by default, can be disabled only at `high` or below; `budget_tokens` returns 400 | AA II: not found
  - **100K rule (official):** the prompt length counts all input tokens, including cache reads and cache writes, and each request is priced on its own. A request over 100K pays the higher prices even when part of its prompt is a cache hit. Haiku 5.5 is the only current Anthropic model without flat 1M-context pricing.
  - Newer tokenizer: about 30% more tokens than Haiku 4.5 for the same text. No server-side refusal fallback. Supports compaction, task budgets and computer use.
  - Speed: 100 to 200 tok/s depending on provider (reported); about 180 tok/s in Claude Code on one subscription ([H55 11:34](https://youtu.be/38_6C0dkKmU?t=694)).
  - Vendor benchmarks (not independently verified): Terminal-Bench 4.0 39.2% (Haiku 4.5 0.0%, GPT-6 Luna 16.4%, Sonnet 5.5 70.6%); OSWorld 2.1 72.4% partial credit at max (strict pass 37.1%). Anthropic says Sonnet and Opus remain better for complex agentic coding.
  - On the release, Anthropic cut Sonnet 5.5 cache reads from $0.20 to $0.10. Opus 5.5 stays at $0.20.
- **Haiku 5.5 routing suggestion** (from Theo's launch video, [H55](https://youtu.be/38_6C0dkKmU), digested in `research/claude-releases.md`, Video 4, section 8):
  - Use it as a **subagent** under Opus, not as a primary or interactive model: codebase search where grep is not enough, data gathering, reading docs or logs, vetting several hypotheses, categorisation, summaries.
  - Use it for many-attempts work that has a cheap, objective verifier (tests, a simulator, a script).
  - Do **not** give it implementation, code review, merge decisions or PR-readiness audits. In the video it trusted green CI as proof of readiness and cornered itself on a GitHub rate limit.
  - Never disable thinking. For reasoning-off classification, prefer GPT-6 Luna or another OpenAI cheap model.
  - Keep requests under 100K prompt tokens; above that every price rises 5x. Long Claude Code sessions cross it quickly (47 of 51 requests in one game build). A Claude Code autocompact window of 100K for Haiku is reported to help (unverified).
  - If cross-vendor routing is allowed, GPT-6 Luna is slightly better value per dollar on AA. Haiku 5.5 is the pick for Anthropic-only setups.
- **Routing suggestion for Haiku 4.5 (vs Opus 5.5, historical):**
  - Use it only inside Claude Code / Agent SDK flows where staying on Anthropic matters: Explore-style file search, grep summaries, commit-message and changelog drafting, classification.
  - Do **not** give it multi-file implementation, review or planning. On independent indexes it is now clearly below non-Anthropic cheap models.
  - If cross-vendor routing is allowed, prefer Gemini 3.8 Flash, GPT-6 Luna or DeepSeek V4.1 Flash for cheap bulk work.
  - Re-evaluate when Haiku 5.5 ships. It is likely to replace this profile entirely. [Update 2026-10-08: Haiku 5.5 has shipped; see the Haiku 5.5 bullets above.]
- **Sources:** [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview) · [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Anthropic Haiku 4.5 launch](https://www.anthropic.com/news/claude-haiku-4-5) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · Haiku 5.5: [Mike Krieger on X](https://x.com/mikeyk/status/2102441803253535060), [cellcog](https://cellcog.ai/blog/claude-haiku-5-5-release-date/), [docsbot](https://docsbot.ai/models/claude-haiku-5-5), `research/claude-releases.md` Video 4

---

## 2. Google Gemini

### 2a. Gemini 3.8 Flash (best generally available Gemini for coding)

**Confidence: HIGH** for ID, price and limits (Google docs). **MEDIUM** for benchmarks (vendor plus third-party summaries).

- **Model ID:** `gemini-3.8-flash`. **GA:** 2026-09-02. It is the third Flash release in about six weeks (3.6, then 3.7, then 3.8).
- **Pricing (introductory until 2026-12-31):** $0.75 input, $0.075 cached input, $3.75 output, plus cache storage at $0.50 per MTok per hour. **From 2027-01-01:** $1.50 / $0.15 / $7.50. Batch is half price, and priority is $1.35 / $6.75. A free API tier exists.
- **Subscriptions:** Gemini app for Google AI Pro ($19.99/mo) and Ultra (from $99.99/mo). Also used in Gemini CLI (free OAuth tier and Pro/Ultra quotas), Antigravity, Android Studio and AI Studio.
- **Context / output:** 1,048,576 input and **65,536 output**. The output cap is small next to Claude/GPT (128K) and DeepSeek (384K).
- **Speed:** about **305 output tok/s**, the fastest AA has measured (per Vellum's citation of AA). It uses about 30% more output tokens per task than 3.7 Flash at high effort (Emergent analysis, via Vellum; unverified).
- **Reasoning:** thinking levels `low`, `medium` and `high` (`minimal` is not supported). Use `high` for agentic coding and `low` for bulk transforms.
- **Capabilities:** function calling, code execution, caching, computer use (preview). Inputs are text, image, video, audio and PDF.
- **Benchmarks (vendor-run, per Vellum and DataCamp):**
  - DeepSWE v1.1: 73.7% (Opus 5: 74.0%)
  - Terminal-bench 2.1: 89.4% (Opus 5: 89.1%; GPT-5.6 Sol: 88.8%)
  - SWE-Bench Pro: 61.6%
  - **Terminal-bench 4.0 (harder, general agent): 19.1% vs Opus 5's 51.8%**
  - OSWorld-2.0: 59.0% vs Opus 5's 75.4%
  - GDPVal-AA v2: 1545 vs 1824 Elo
  - AA Intelligence Index: 41
- **Strengths:** very fast and very cheap. Strong on short-to-medium terminal coding tasks, multimodal input (screenshots, video, PDFs), chart reading, and security patching (Google says CWE-Bench 47.2%).
- **Weaknesses:** collapses on hard, long-horizon agent tasks (Terminal-bench 4.0), weaker computer use and knowledge work, and a 64K output cap. Price doubles in January. In a DataCamp hands-on test it took more turns than DeepSeek V4.1 Flash on the same task.
- **Invocation:**
  - Gemini CLI (install: `npm i -g @google/gemini-cli` or `brew install gemini-cli`):
    `gemini -p "add input validation to api/users.ts" -m gemini-3.8-flash --output-format json --approval-mode auto_edit`
    - Output formats: `text`, `json`, `stream-json`.
    - Approval modes: `default`, `auto_edit`, `plan`, `yolo` (`--yolo` is the CLI-only shortcut for auto-approving everything).
    - Exit codes: 0 OK, 1 error, 42 input error, 53 turn limit.
    - Headless mode also starts automatically when stdin is not a TTY.
  - API: `curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent" -H "x-goog-api-key: $GEMINI_API_KEY" -H 'Content-Type: application/json' -d '{"contents":[{"parts":[{"text":"..."}]}]}'`
  - Scriptable: yes.
- **Gemini CLI notes:** latest release found was v0.61.0 (2026-09-23); a PR and a DEV post reference v0.62. The default routes between Flash and Pro by task complexity. 3.8 Flash is the default Flash model. It has subagents (codebase investigator, browser, research), plan mode, MCP and Google Search grounding. Free limits with a Google account: 60 requests/min and 1,000/day. AI Pro/Ultra get higher quotas.
- **Routing suggestion (vs Opus 5.5):**
  - Good fit: **bulk mechanical work** (codemods, renames, test scaffolding, lint fixes), log and file summarisation, screenshot/PDF/video reading, and fast first-pass drafts. It is about 5x cheaper on input and output than Opus 5.5 at intro prices, and 3-4x faster.
  - Good fit: parallel "fan-out" subagents where many short tasks matter more than depth.
  - Avoid for long unattended builds, multi-hour refactors, or anything resembling Terminal-bench 4.0. Opus 5.5 is far ahead there.
  - Avoid when a single response must be longer than 64K tokens (for example, a full-file regeneration of large files).
  - Re-price after 2027-01-01, when the cost advantage halves.
- **Sources:** [Gemini models](https://ai.google.dev/gemini-api/docs/models) · [gemini-3.8-flash model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Google blog: 3.8 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · [Vellum benchmarks](https://www.vellum.ai/blog/gemini-3-8-flash-benchmarks-explained) · [DataCamp: DeepSeek V4.1 Flash vs Gemini 3.8 Flash](https://www.datacamp.com/blog/deepseek-v4-1-flash-vs-gemini-3-8-flash) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · Gemini CLI: [GitHub](https://github.com/google-gemini/gemini-cli), [headless docs](https://geminicli.com/docs/cli/headless/), [changelog](https://geminicli.com/docs/changelogs/), [config reference](https://geminicli.com/docs/reference/configuration/), [3.8 Flash default PR](https://github.com/google-gemini/gemini-cli/pull/29172) · Subscription prices: [eesel](https://www.eesel.ai/blog/gemini-pricing)

### 2b. Gemini 4 Argon (new frontier model, restricted access)

**Confidence: MEDIUM** for announced facts. **LOW** for anything about practical use, because almost nobody has access.

- **Announced:** 2026-09-30. **Access:** for now, only "trusted cyber defenders" in Google's Fairwind Program. Broader release is "as soon as possible", starting with paid API customers and **Google AI Ultra** subscribers.
- **Model ID:** unverified (not published in the sources found).
- **Pricing:** introductory $2 input / $10 output with cached input at a 95% discount ($0.10). The later standard price is $4 / $20. How long the 50% discount lasts is unconfirmed.
- **Context / output:** 1M tokens context (AA). **1M output token limit** (Google: "up from 64K").
- **Benchmarks:**
  - Vendor: DeepSWE v1.1 77.9%, AutomationBench 51.3% (#1), CWE-bench 68%.
  - AA: Intelligence Index **53** (ties GPT-6 Astra max), Terminal-Bench 4 57%, lowest hallucination rate AA has measured (15%).
  - Uses about 62K output tokens per task (verbose), versus 27K for Astra.
- **Weaknesses (AA):** accuracy down 5 points from the previous generation and 13 points behind Astra. Lower presentation and analytical quality scores.
- **Invocation:** once released, expect `gemini -p ... -m <argon-id>` and the same API as above. **Template:** ID ___ | GA date ___ | Gemini CLI support ___ | thinking levels ___.
- **Routing suggestion:**
  - Do not route to it yet; it is not generally available.
  - When it opens up, test it as a **cheaper Opus 5.5 / Astra peer** for long-horizon coding and security review. At intro prices it is half Opus 5.5's list price, with a 95% cache discount.
  - Its low hallucination rate makes it a candidate for research and summarisation that needs factual accuracy.
- **Sources:** [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) · [AA article](https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs) · [CNBC](https://www.cnbc.com/2026/09/30/google-gemini-4-argon-ai.html) · [9to5Google](https://9to5google.com/2026/09/30/gemini-4-argon-announcement/)

### 2c. Gemini 3.1 Pro Preview (do not route)

**Confidence: HIGH** that it is outclassed.

- `gemini-3.1-pro-preview`, launched 2026-02-19 and still in preview. Price: $2 / $12 (≤200K tokens), $4 / $18 above. Caching: $0.20 / $0.40 per MTok plus $4.50 per MTok per hour of storage. No free tier.
- AA Intelligence Index **30**, below 3.8 Flash (41), which costs much less.
- **Gemini 3.5 Pro** was announced in May 2026 and slipped past June, July and August. As of 2026-09-23 it was still "coming soon". Rumours say Gemini 4 Pro will arrive in October 2026 (unverified).
- **Routing:** none. Use 3.8 Flash now and Argon later.
- **Sources:** [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [eesel on 3.5 Pro](https://www.eesel.ai/blog/gemini-3-5-pro) · [AIToolsReview](https://aitoolsreview.co.uk/insights/gemini-3-5-pro)

---

## 3. xAI Grok

### 3a. Grok 4.7

**Confidence: HIGH** for ID, price and context (xAI docs). **MEDIUM** for benchmarks and speed (sources conflict).

- **Model ID:** `grok-4.7` (no aliases). **Released:** 2026-09-21. Knowledge cutoff May 2026.
- **Pricing:** $2 input, $0.50 cached input, $6 output for requests under 200K tokens; **double that at 200K tokens or more**. US regional endpoint adds 10%. A "fast" variant is available only in Cursor and Grok Build, at 2x the price (1.5x for long context).
- **Subscriptions:** Grok Build (see 3b), **Cursor (all plans)**, and **GitHub Copilot** Pro / Pro+ / Max / Business / Enterprise from launch day. Consumer SuperGrok tiers are covered in 3b.
- **Context / output:** 500K context. xAI docs say "no text output limit". Prompt caching and context compaction are supported.
- **Speed:** AA leaderboard shows **79 tok/s** at xhigh. AA's launch article says about 188 tok/s. **Conflict; unverified.**
- **Token use:** very verbose, about **81K output tokens per AA task** at xhigh (+125% vs Grok 4.6, +196% vs GPT-6 Astra). AA cost per task is $3.74, about 2x Opus 5.5 at high.
- **Reasoning:** `low`, `medium`, `high` (default), `xhigh`.
- **Benchmarks:**
  - AA Intelligence Index 46.
  - AA Coding Agent Index **56** when run in Grok Build, ranking **4th** behind Fable 5.1, GPT-6 Astra and Opus 5 (AA).
  - DeepSWE about 71-73%, Terminal-Bench 4.0 33%, Senior SWE-Bench pass@3 40.0% (Snorkel, ranked 6th), CursorBench 4.0 46.3%.
  - Our transcripts: 80.7 on the "improve T3 Code" task, versus 87.4 for 6.1 Sol and 83.8 for Astra.
- **Strengths:** long multi-hour coding runs (xAI trained it on "work that takes many hours"), agentic knowledge work (AA-Briefcase just behind Opus 5 and Fable 5.1), and a cheap per-token list price.
- **Weaknesses:**
  - Token-hungry, so the cheap list price does not mean cheap tasks.
  - Regressions on long-document reasoning (AA-LCR −3.7 points) and presentation quality.
  - Single-pass accuracy trails Claude Code and Codex (third-party review).
- **Invocation:**
  - Grok Build: `grok -p "fix the failing auth tests" -m grok-4.7 --output-format streaming-json`
  - API (OpenAI-compatible): `curl https://api.x.ai/v1/chat/completions -H "Authorization: Bearer $XAI_API_KEY" -H "Content-Type: application/json" -d '{"model":"grok-4.7","reasoning_effort":"high","messages":[{"role":"user","content":"..."}]}'` (the `reasoning_effort` field name follows the OpenAI-compatible convention; unverified for xAI).
  - OpenCode and Pi both support xAI as a provider.
  - Scriptable: yes.
- **Routing suggestion (vs Opus 5.5):**
  - Use as a **second-opinion implementer** or an "arena" competitor on hard bugs, where a different model family adds diversity. It ranks just below the Opus/Fable/Astra tier on coding-agent indexes.
  - Do not use for bulk or cheap work. Its verbosity makes it about 2x Opus 5.5's cost per task on AA.
  - Do not use for long-document reading or review of large specs (LCR regression).
  - Reasonable for long unattended runs if you already pay for Cursor or Copilot, where per-token cost is hidden.
- **Sources:** [xAI Grok 4.7 docs](https://docs.x.ai/developers/grok-4-7) · [xAI models and pricing](https://docs.x.ai/docs/models) · [AA: Benchmarking Grok 4.7](https://artificialanalysis.ai/articles/benchmarking-grok-4-7) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [WinBuzzer](https://winbuzzer.com/2026/09/23/grok-4-7-coding-gains-higher-token-use-a004-xcxwbn/) · [Snorkel Senior SWE-Bench](https://snorkel.ai/blog/grok-4-7-on-senior-swe-bench-strong-pass3-cheaper-cost/) · [Oracle OCI model page](https://docs.oracle.com/en-us/iaas/Content/generative-ai/x-ai-grok-4-7.htm) · [ai-tldr](https://ai-tldr.dev/models/grok-4-7/)

### 3b. Grok Build (agent CLI) and grok-build-0.1 (model)

**Confidence: MEDIUM.** The CLI usage comes from xAI docs; subscription tiers come from a third party only.

- **Grok Build CLI:**
  - Beta since 2026-05-14. Written in Rust. Binary `grok`.
  - Install: `curl -fsSL https://x.ai/cli/install.sh | bash`.
  - Auth: browser login on first launch, or `XAI_API_KEY`.
  - Headless: `grok -p "..." [-m model] [--output-format streaming-json]`.
  - Custom models (including non-xAI ones) can be added in `~/.grok/config.toml`.
  - Features: skills, plugins and marketplaces; Agent Client Protocol; Plan Mode; subagent view. Default model is now Grok 4.7.
  - One third-party guide also lists `grok exec`, `grok plan`, `grok goal` and `grok arena` subcommands (**unverified**; not in xAI docs).
- **Subscription access (unverified, third-party):** X Premium+ ($40/mo) basic, SuperGrok ($30/mo) standard, SuperGrok Heavy ($299/mo) for full 8-way parallel agents. OpenCode's docs say xAI auth supports SuperGrok OAuth.
- **grok-build-0.1 model:**
  - ID `grok-build-0.1`, API beta from 2026-05-29.
  - $1 input / $0.20 cached / $2 output (doubles at 200K tokens or more). 256K context. "100+ tok/s" (vendor).
  - Text and image input. Tuned for web development, debugging and MCP.
  - No independent benchmarks found. A third-party Terminal-Bench 2.1 figure of 70.8% for "Grok Build" vs 83.1% for Claude Code is **unverified**.
- **Routing suggestion:**
  - grok-build-0.1 is a possible **cheap, fast mid-tier** for web front-end tweaks and debugging loops. With no independent scores, it needs an in-house trial before it enters the table.
  - Treat the Grok Build CLI as a harness option, not a reason to pick the model.
- **Sources:** [Grok Build docs](https://docs.x.ai/build/overview) · [xAI: Grok Build 0.1 on API](https://x.ai/news/grok-build-0-1) · [xAI models and pricing](https://docs.x.ai/docs/models) · [Developers Digest guide](https://www.developersdigest.tech/blog/grok-build-developer-guide-2026) · [OpenCode providers](https://opencode.ai/docs/providers/)

---

## 4. Open-weights models for OpenCode / Pi

### How to run them from a terminal (applies to all models below)

- **OpenCode:**
  - `opencode run -m <provider>/<model> --format json "your task"`
  - Authenticate with `/connect` in the TUI or with env vars.
  - Providers include Z.AI (with GLM Coding Plan), Moonshot AI, DeepSeek, MiniMax, xAI, OpenRouter and OpenCode Zen.
  - **Exact provider/model strings change often.** Run `opencode models` and grep for them; the docs' examples are stale, for instance `z-ai/glm-4.7` and `moonshot/kimi-k2`.
- **Pi (pi-mono, `@mariozechner/pi-coding-agent`):**
  - Non-interactive: `pi -p "your task"`. Add `--mode json` for NDJSON events.
  - It supports 15+ providers, including DeepSeek, xAI, OpenRouter, Groq, Cerebras and Bedrock.
  - Choose the model with `--provider <p> --model <m>`. These flag names come from the pi README and are **unverified**, because the npm page returned 403.
- **Vendor CLIs:**
  - Kimi Code: `kimi --print "..."` (auto-approves all tools). Options: `--output-format=stream-json`, `--final-message-only`, `--quiet`.
  - Qwen Code: `npm i -g @qwen-code/qwen-code`, then `qwen -p "..." --output-format json|stream-json`.
- **Anthropic-compatible endpoints:** DeepSeek's API accepts the Anthropic format, and the GLM Coding Plan plugs into Claude Code. Either can sit behind `claude -p` via base-URL override. That route is unverified per vendor beyond these two.

### 4a. Xiaomi MiMo-V2.6-Pro (and V2.6-Flash): top open-weights model on AA

**Confidence: MEDIUM.** The model is new (11 days old) and the price may be promotional.

- **IDs:** OpenRouter `xiaomi/mimo-v2.6-pro`. Xiaomi first-party API ID unverified. Released 2026-09-21.
- **Weights:** MIT licence. 1.02T total parameters, 42B active. Flash: 310B total, 15B active. A "Pro-UltraSpeed" variant (claimed 20x faster) and a distilled Qwen-9B variant also exist.
- **Pricing:** Pro $0.435 input / $0.0036 cached / $0.87 output. Flash $0.14 / $0.28. Third-party sources only; **unverified on a Xiaomi page**.
- **Context:** 1M tokens. Inputs: text, image, audio and video.
- **Benchmarks:**
  - AA Intelligence Index **46**, #1 among open weights and tied with Grok 4.7, at **about $0.13 per task**. Speed is 45 tok/s (slow).
  - DeepSWE v1.1 71.9 vs 74.0 for Opus 5 and Astra.
  - Terminal-Bench 4.0 **34.9** vs 49.0 for Opus 5 and 59.6 for Astra.
- **Weaknesses:** trails clearly on the hardest long-horizon coding. Vendor-reported numbers dominate. Very new, so there are no independent harness reports.
- **Routing:**
  - Best "intelligence per dollar" in the open-weights set. Candidate for cheap mid-tier review passes, research and summarisation, and mid-size implementation tasks.
  - Not for long unattended builds.
  - Slow output, so avoid latency-sensitive interactive loops.
- **Sources:** [VentureBeat](https://venturebeat.com/technology/better-than-deepseek-xiaomis-mimo-v2-6-pro-debuts-as-the-top-open-weights-model-in-the-world-alongside-cheaper-v2-6-flash) · [AA open-weights page](https://artificialanalysis.ai/models/open-source) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [OpenRouter](https://openrouter.ai/xiaomi/mimo-v2.6-pro) · [kingy.ai benchmarks](https://kingy.ai/blog/mimo-v2-6-pro-benchmarks-specs-comparison/)

### 4b. GLM-5.3 and GLM-5.3-Flash (Z.ai / Zhipu)

**Confidence: MEDIUM-HIGH.** Prices come from Z.ai docs; benchmarks are vendor-only.

- **IDs:** `glm-5.3`, `glm-5.3-flash`, `glm-5.3-flashx`. GLM-5.3 released 2026-08-14. Weights on Hugging Face about 2026-08-28 under a **bespoke GLM-5.3 licence**; some sources say MIT, which is a conflict. GLM-5.3-Flash followed on 2026-08-27.
- **Size:** about 744-753B total, about 40B active (same base as GLM-5.2; all gains come from post-training). GLM-5.3-Flash is 320B total, 18B active (AA).
- **Pricing (Z.ai docs):**
  - GLM-5.3: $1.40 input / $0.26 cached / $4.40 output
  - GLM-5.3-Flash: $0.15 / $0.03 / $0.50
  - GLM-5.3-FlashX: $0.37 / $0.075 / $1.25
- **GLM Coding Plan (third-party, unverified):** Lite $18, Pro $80, Max $168 per month. Credit-based, with half credits off-peak. Works with Claude Code, Cline, Roo, OpenCode and about 20 other tools.
- **Context / output:** 1M / 128K (EvoLink). One source says 200K for the open-weights architecture (unverified).
- **Reasoning:** thinking is **always on** (`thinking.type: "disabled"` no longer works). `reasoning_effort` takes `low`, `high` or `max`; Z.ai recommends `max` for coding.
- **Benchmarks:**
  - Vendor-only, no independent replication at launch: DeepSWE v1.1 66.9, FrontierSWE 78.1, Terminal Bench 3.0 28.3, SWE-Marathon 42.5, CyberGym 84.5.
  - AA Intelligence Index **45** at max, 74 tok/s, **$2.01 per task**. GLM-5.3-Flash: **42**.
- **Weaknesses:** Z.ai itself says it is behind Claude Fable 5. Text-only. At max effort its AA cost per task is above Opus 5.5 at high.
- **Routing:**
  - **GLM-5.3-Flash is the interesting one.** AA 42 at Gemini-Flash-like prices makes it a strong cheap-tier bulk worker, and it is self-hostable.
  - Full GLM-5.3 suits a flat-rate Coding Plan inside Claude Code, where the per-token cost disappears. Per token it is not cheaper than GPT-6.1 Sol per task.
  - Avoid for front-end and visual work (no vision).
- **Sources:** [Z.ai pricing docs](https://docs.z.ai/guides/overview/pricing) · [EvoLink: GLM-5.3 release](https://evolink.ai/blog/glm-5-3-release) · [AA open-weights page](https://artificialanalysis.ai/models/open-source) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [Baidu Cloud article on licence](https://intl.cloud.baidu.com/en/article/8754873) · [GLM Coding Plan guide](https://www.aieatingtheworld.com/articles/glm-coding-plan-guide-z-ai-glm-5-2) · [Developer Puter pricing](https://developer.puter.com/tutorials/zai-glm-api-pricing/)

### 4c. DeepSeek V4.1 Flash (and V4 Pro)

**Confidence: HIGH** for price and limits (DeepSeek docs). **MEDIUM** for benchmarks.

- **IDs:** `deepseek-flash` = DeepSeek-V4.1-Flash (released 2026-09-10). `deepseek-v4-pro` = V4 Pro. The legacy `deepseek-v4-flash` is deprecated and routes to Flash.
- **Weights:** MIT licence. V4.1 Flash is 552B total, about 8B active for input and 16B for output, with native image input. V4 Pro is 1.6T total, 49B active.
- **Pricing (off-peak; peak is exactly 2x):**
  - Flash: $0.15 input / **$0.003 cached** / $0.60 output
  - V4 Pro: $0.66 / $0.022 / $1.98
  - **Peak hours:** 01:00-04:00 and 06:00-10:00 UTC, Monday to Friday. Requires a minimum $5 prepaid balance.
- **Context / output:** 1M / **384K**, the largest output limit in this report. Thinking is on by default and both modes are supported.
- **API format:** OpenAI- and **Anthropic-compatible** endpoints.
- **Benchmarks:**
  - Vendor: Terminal-Bench 2.1 90.6 (up from 82.7), DeepSWE v1.1 74.2.
  - Vendor, harder suites: Terminal-Bench 3.0 30.0 and 4.0 31.2, vs 43.3 and 51.8 for Opus 5.
  - AA Intelligence Index: Flash **39**, V4 Pro **36**. Oddly, Pro scores below Flash.
  - DataCamp hands-on: beat Gemini 3.8 Flash on one scheduler task (2 turns vs 4).
- **Weaknesses:** big drop on hard multi-step agent suites. No audio, video or PDF input. Possible data-jurisdiction and policy concerns for some organisations. Peak-hour pricing complicates cost forecasts.
- **Routing:**
  - **The cheapest capable bulk worker in this report.** Cache hits are about 25x cheaper than Gemini 3.8 Flash's, so it suits repeated passes over the same large repo context: mechanical edits, test generation, summarising many files, and log triage.
  - Its large output cap suits full-file regeneration and long generated artefacts.
  - Not for architecture, planning, or long unattended builds.
  - Skip V4 Pro; Flash scores higher on AA and costs less.
- **Sources:** [DeepSeek pricing docs](https://api-docs.deepseek.com/quick_start/pricing) · [BuildFastWithAI review](https://blog.buildfastwithai.com/deepseek-v4-1-flash-review) · [DataCamp comparison](https://www.datacamp.com/blog/deepseek-v4-1-flash-vs-gemini-3-8-flash) · [NVIDIA model card](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash/modelcard) · [Activepieces](https://www.activepieces.com/blog/deepseek-v4-1-flash-api-pricing-docs-2026) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [kingy.ai open-weights shortlist](https://kingy.ai/news/best-open-weight-ai-models-in-2026-glm-5-2-vs-deepseek-v4-vs-kimi-k2-6-vs-qwen-vs-mistral/)

### 4d. Kimi K3 (Moonshot AI)

**Confidence: MEDIUM.** Benchmark sources disagree.

- **ID:** `kimi-k3`. API went live 2026-07-16; weights 2026-07-27 under a modified MIT licence.
- **Size:** 2.8T total, the largest open-weights model to date; 16 of 896 experts active (about 104B active per AA).
- **Pricing:** $3.00 input / $0.30 cached / $15.00 output, flat across the 1M context. Free on kimi.com. Moonshot also sells **K2.7 Code** and **K2.6** at $0.95 / $4 (unverified).
- **Context / output:** 1M / up to 1M (default 131K).
- **Reasoning:** always on. `reasoning_effort` currently accepts **only `max`**. Temperature and top_p are fixed. The full reasoning trace must be passed back each turn, or quality degrades.
- **Benchmarks:**
  - Vendor and third-party: Terminal-Bench 2.1 88.3. Leads on Program Bench and SWE Marathon; trails on DeepSWE and FrontierSWE.
  - **AA Intelligence Index 44**, 36 tok/s (slowest here), **$2.00 per task**.
  - DataCamp quotes an index of "57" on a different scale. A Chinese ranking site gives "74.4". **Do not mix these.**
- **Strengths:** front-end and visual work (screenshot-driven iteration), long agentic sessions, agent-swarm and sub-agent parallelism.
- **Weaknesses:** slow and expensive for open weights. Makes autonomous decisions on ambiguous tasks. Reviews describe a "noticeable gap in user experience" vs frontier closed models. Web search is flagged as unstable. Self-hosting needs a full rack.
- **Invocation:** Kimi Code `kimi --print "..."`; OpenCode/Pi with the Moonshot provider; or the OpenAI-compatible API at platform.moonshot.ai.
- **Routing:**
  - Only for **front-end/UI work with screenshots** when you want a non-Claude, non-OpenAI option. It is not cheaper per task than Opus 5.5 at high.
  - Not for bulk or interactive work (slow, max effort only).
  - Low priority for the routing table.
- **Sources:** [DataCamp: Kimi K3](https://www.datacamp.com/blog/kimi-k3) · [VentureBeat](https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems) · [codersera guide](https://codersera.com/blog/kimi-k3-complete-guide-2026/) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [AA open-weights page](https://artificialanalysis.ai/models/open-source) · [Kimi CLI print mode](https://moonshotai.github.io/kimi-cli/en/customization/print-mode.html) · [kingy.ai](https://kingy.ai/news/best-open-weight-ai-models-in-2026-glm-5-2-vs-deepseek-v4-vs-kimi-k2-6-vs-qwen-vs-mistral/)

### 4e. Qwen3.8-Max (Alibaba)

**Confidence: LOW-MEDIUM.** No official pricing was found, and the qwen.ai blog would not render.

- **IDs:** open weights `Qwen/Qwen3.8-2.4T-A95B` (plus FP8). Hosted API on Alibaba QwenCloud; API model string **unverified** (probably `qwen3.8-max`).
- **Dates:** API 2026-08-02. Open weights 2026-08-12/13.
- **Size and licence:** 2.4T total, 95B active. **Custom licence with a revenue-share requirement** for large commercial users (thresholds unpublished).
- **Open weights vs hosted:** the open weights are **text-only, thinking-only, and lack the native 1M context** of the hosted API. Running BF16 needs about 4.9 TB (reference deployment: GB300 NVL72).
- **Pricing:** **unverified / not found.**
- **Benchmarks:** AA Intelligence Index **45**, 38 tok/s, **$5.41 per task**, the most expensive per task in this report. One headline claims "86.6, near Opus 5" (unverified).
- **Smaller siblings:** Qwen3.8-27B (dense; release status conflicts between sources) and Qwen3-Coder-Next (80B total, 3B active, Apache 2.0, 262K context). Coder-Next is the practical **local** coding model.
- **Invocation:** `qwen -p "..." --output-format json` (Qwen Code), or OpenCode/Pi via OpenRouter or OpenCode Zen.
- **Routing:**
  - Skip Qwen3.8-Max for API routing; it is the most expensive per task with no edge in capability.
  - Consider **Qwen3-Coder-Next** only for an offline or local tier (laptop or single-GPU) doing simple edits.
- **Template blanks:** API ID ___ | price in/cache/out ___ | hosted context ___ | max output ___
- **Sources:** [explainx.ai](https://www.explainx.ai/blog/qwen3-8-max-open-weights-live-hugging-face-august-2026) · [Qwen blog (did not render)](https://qwen.ai/blog?id=qwen3.8) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [kingy.ai](https://kingy.ai/news/best-open-weight-ai-models-in-2026-glm-5-2-vs-deepseek-v4-vs-kimi-k2-6-vs-qwen-vs-mistral/) · [Qwen Code headless docs](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/)

### 4f. MiniMax M3 and gpt-oss (brief; low priority)

**Confidence: LOW-MEDIUM.**

- **MiniMax M3:**
  - ID `minimax-m3`, released 2026-06-01. 428B total, about 23B active. 1M context, 524K output (unverified). Multimodal.
  - Licence conflicts: MIT vs a custom minimax-community licence.
  - Price conflicts: $0.28 / $0.056 / $1.10 vs $0.60 / $2.40 at launch on OpenRouter.
  - Vendor SWE-bench Verified 80.5%. **AA Intelligence Index 29**, the lowest of the 2026 open models here.
  - Token plans are $20 / $50 / $120 per month.
  - **Routing:** do not include. DeepSeek V4.1 Flash and GLM-5.3-Flash dominate it.
  - Sources: [llm-stats](https://llm-stats.com/models/minimax-m3) · [datanorth](https://datanorth.ai/news/minimax-launches-m3) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models)
- **gpt-oss-120b / 20b:**
  - Released August 2025, Apache 2.0. 120b is about 117B total, 5.1B active, and fits on one 80 GB GPU. 20b is about 21B total, 3.6B active, and runs in 16 GB.
  - Context 128K per the original launch; one 2026 source says 256K (unverified). No new generation confirmed.
  - **AA Intelligence Index 12**, 160 tok/s.
  - **Routing:** only for an air-gapped or offline tier doing trivial transforms. Otherwise exclude.
  - Sources: [OpenAI: Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/) · [frankx.ai](https://www.frankx.ai/blog/gpt-oss-analysis-2026) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models)

---

## 5. OpenAI Sol naming: GPT-5.6 Sol vs GPT-6.1 Sol (plus GPT-6 Luna)

**Confidence: HIGH** (OpenAI docs and TechCrunch).

- **GPT-5.6 Sol** (`gpt-5.6-sol`):
  - Released 2026-07-09 as part of the GPT-5.6 family (Luna, Terra, Sol). It was OpenAI's flagship until GPT-6 Astra.
  - $4 input / $0.40 cached / $20 output, with promotional pricing "at least through November 21, 2026". 1.05M context, 128K output.
  - Effort: `none`, `low`, `medium` (default), `high`, `xhigh`, `max`.
  - Still listed and not marked deprecated, but **superseded**.
- **GPT-6 Sol:** released 2026-09-22 with GPT-6 Luna. Our transcripts call both "not that good". Replaced a week later.
- **GPT-6.1 Sol** (`gpt-6.1-sol`): **current.**
  - Released 2026-09-29 at DevDay.
  - **$2 input / $0.10 cached (95% discount) / $10 output.** Cache writes cost $2.50. Prompts over 272K input tokens cost 2x on input and cache.
  - 1.05M context (922K max input), 128K output. Knowledge cutoff 2026-04-30.
  - Effort: `low`, `medium` (default), `high`, `xhigh`, `max` (`none` and `minimal` are not supported).
  - Tools: hosted shell, apply_patch, computer use, MCP, skills, tool search.
  - Available in ChatGPT Plus, Pro, Business, Enterprise and Edu (ChatGPT Work) and in **Codex**.
  - An "Ultrafast" `service_tier` costs 6x for up to 300 tok/s. Sol Ultrafast was announced as "coming in days" (unverified whether it is live).
  - AA: 50 at high ($0.32 per task), 52 at max ($0.72 per task).
  - Note: OpenAI scrapped "GPT-6.1 Astra" over safety concerns (TechCrunch).
- **GPT-6 Luna** (`gpt-6-luna`):
  - $0.10 input / $0.50 output (cached price unverified). 1.05M context, 128K output.
  - Effort: `none` through `max`.
  - AA **38** at max for **about $0.07 per task**, the cheapest decent model measured.
  - Release date about 2026-09-22 (from transcripts). Not covered in our video notes beyond "not that good".
- **Invocation:**
  - Codex: `codex exec -m gpt-6.1-sol -c model_reasoning_effort="high" --json --sandbox workspace-write "review this diff"`. The `-m` and `-c model_reasoning_effort` flags follow Codex CLI conventions but were not re-confirmed on the current docs page. `--json`, `--sandbox`, `-o` and `--output-schema` were confirmed.
  - API: Responses API, `model: "gpt-6.1-sol"`, `reasoning: {effort: "medium"}`.
- **Routing:** see `gpt-releases.md` for hands-on detail. On these numbers:
  - GPT-6.1 Sol is the **strongest mid-tier option overall**: reviewer, investigator, and second opinion.
  - GPT-6 Luna is a serious **cheap-tier** candidate to test against DeepSeek V4.1 Flash and Gemini 3.8 Flash.
- **Sources:** [OpenAI models](https://developers.openai.com/api/docs/models) · [gpt-6.1-sol page](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · [gpt-5.6-sol page](https://developers.openai.com/api/docs/models/gpt-5.6-sol) · [TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-gpt-6-1-sol-says-it-nearly-matches-gpt-6-astra-and-costs-less/) · [VentureBeat on Ultrafast](https://venturebeat.com/technology/openais-gpt-6-1-sol-offers-astra-like-performance-at-1-5th-price-a-new-ultrafast-tier-clocks-at-300-tokens-per-second) · [Wikipedia: GPT-5.6](https://en.wikipedia.org/wiki/GPT-5.6) · [Codex non-interactive docs](https://learn.chatgpt.com/docs/non-interactive-mode) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models)

---

## Suggested routing-table shortlist

| Tier | Include | Why | Exclude / defer |
|---|---|---|---|
| Frontier | (existing: Fable 5.1, Opus 5.5, GPT-6 Astra) + **Gemini 4 Argon** when generally available | AA 53, cheap at intro price, low hallucination | Gemini 3.1 Pro, 3.5 Pro (unreleased) |
| Mid / second opinion | **GPT-6.1 Sol** (already profiled), **Grok 4.7** (diversity), **MiMo-V2.6-Pro** (cheapest AA-46) | Different model families for review and arena runs | Qwen3.8-Max (cost), Kimi K3 (slow and costly), GLM-5.3 at max (cost, unless on Coding Plan) |
| Cheap / bulk | **DeepSeek V4.1 Flash**, **Gemini 3.8 Flash**, **GPT-6 Luna**, **GLM-5.3-Flash** | AA 38-42 at a few cents per task; pick by cache pattern, speed and output length | Claude Haiku 4.5 (AA 17; superseded), MiniMax M3. **Anthropic-only option: Claude Haiku 5.5** for cheap bulk, subagent search and categorisation, if prompts stay under 100K tokens (5x price above) |
| Local / offline | Qwen3-Coder-Next, gpt-oss-20b/120b | Run on one GPU | anything 700B+ |
