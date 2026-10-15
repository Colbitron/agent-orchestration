# Claude 5.x Release Videos: Detailed Summaries

Research note on four launch-review videos for the Claude 5.x models, by the same speaker (Theo, t3.gg; he builds T3 Code and Lakebed). It records the conclusions, numbers and decision rules this kit uses, not a summary of each video. Prices and benchmark figures are as the speaker read them on launch day unless marked as checked elsewhere.

## Sources

- FAB51: "My New Favorite Model", Theo (t3.gg), YouTube, https://youtu.be/r_dw-1109Ag
- OPUS55: "My new favorite model.", Theo (t3.gg), YouTube, https://youtu.be/jgGyX7MPPVg
- SON55: "OpenAI should be scared of this one", Theo (t3.gg), YouTube, https://youtu.be/8WbW_n95wc4
- H55: "finally a good small model", Theo (t3.gg), YouTube, https://youtu.be/38_6C0dkKmU

Each `[KEY m:ss]` citation links to that video at that timestamp. Timestamps come from the auto-generated captions and may be a few seconds early or late.

## Transcription notes (read first)

The captions are speech-to-text and contain systematic mis-hearings. This document reads them as follows:

| Transcript text | Interpreted as |
|---|---|
| "cash", "cashed", "cash reads/rights" | cache, cached, cache reads/writes |
| "Soul", "5.6 soul", "GPT6 Soul" | OpenAI's "Sol" model. The Fable video says "5.6 soul" and the Opus/Sonnet videos say "GPT6 Soul". The exact version is ambiguous: it may be GPT-5.6 Sol in the Fable video and GPT-6/6.1 Sol later. |
| "Astra", "Aster", "Astro", "GBD6 Astra" | GPT-6 Astra (OpenAI) |
| "Luna" | an OpenAI cheap model released alongside GPT-6 Sol ("GPT6 Soul and Luna") |
| "Halo 5.1" (one occurrence), "Babel 5.1", "table 5.1", "Able 5" | Fable 5.1 / Fable 5 |
| "Sonet 55", "Opus 55", "Haiku 55" | Sonnet 5.5, Opus 5.5, Haiku 5.5 |
| "Gro/Grock/Rock 4.7" | Grok 4.7 (xAI) |
| "Gemini 38 Flash" | probably Gemini 3.8 Flash |
| "Cloud Code", "quad code", "CloudMD", "Claude MD" | Claude Code, CLAUDE.md |
| "X high", "XH high", "XI", "Xigh" | the `xhigh` effort level |
| "codeex" | Codex (OpenAI) |
| "Witchai" | a design-comparison site made by someone called "Dra" (name uncertain) |
| "fish slop" / "Fishlop 3D" | the speaker's personal game-generation test |
| "3JS" | three.js |
| "Raichu", "Hiku", "ha coup", "haik coup", "Hike" | Haiku (Video 4) |
| "Jev" | an OpenAI cheap model he recommends for reasoning-off categorisation (Video 4). The exact model name is uncertain. |
| "Slopalytics", "Sloppytics" | the speaker's cost/intelligence dashboard, fed by Artificial Analysis data |
| "Prime" | ThePrimeagen |
| "Pto line", "proto line" | the Pareto line on his charts |
| "Son of 55", "Sonic 55" | Sonnet 5.5 |
| "61 soul", "GPT61 Soul" | GPT-6.1 Sol |
| "Lydia" | an Anthropic employee quoted on autocompact settings (name uncertain) |
| Code Rabbit sponsor segment (Video 4, about 2:18 to 3:40) | skipped |

Caveats:

- Quotes are lightly cleaned ("cache" for "cash" and similar). Square brackets mark words we corrected or inserted; some model names inside quotes keep the caption spelling and should be read per the table.
- Benchmark figures are the speaker's readings of vendor or Artificial Analysis (AA) charts on launch day, not independent measurements.
- Videos 1 to 3 do not evaluate Haiku 4.5; the Opus 5.5 and Sonnet 5.5 videos say Haiku 5.5 is "coming in the next few weeks". **Video 4 covers Haiku 5.5's launch** (about 2026-10-07), including the Sonnet 5.5 cache-read cut that shipped with it.

---

# Video 1: Claude Fable 5.1 (and Mythos 5.1)

## 1. Subject and overall thesis

- Launch review of **Claude Fable 5.1 / Mythos 5.1** after about 24 hours of heavy use: "a meaningful jump from Fable 5" [FAB51 0:17](https://youtu.be/r_dw-1109Ag?t=17), "a universal easy to agree on huge win" [FAB51 54:32](https://youtu.be/r_dw-1109Ag?t=3272). Mixed in detail: more expensive in some ways and cheaper in others, instruction following better and worse, benches higher with "a couple strange exceptions" [FAB51 0:23](https://youtu.be/r_dw-1109Ag?t=23).
- **Central claim: 5.1 "changed the unit of work"** [FAB51 51:20](https://youtu.be/r_dw-1109Ag?t=3080). It behaves like a maintainer that audits, takes over, corrects and lands several lines of work in one session, winning by "carrying more work through the review and merge tail", not by a faster first response [FAB51 51:44](https://youtu.be/r_dw-1109Ag?t=3104). (This framing comes from a GPT/Sol-written analysis of his PR data that he endorses.)
- Scale: 89 PRs in 24 hours [FAB51 1:16](https://youtu.be/r_dw-1109Ag?t=76) (later "90 PRs land in a 24-hour window" [FAB51 46:11](https://youtu.be/r_dw-1109Ag?t=2771)). Judge models by what lands: Opus 5 "killed it in the benchmarks" but its merged code was "nowhere near as nice to use" [FAB51 1:11](https://youtu.be/r_dw-1109Ag?t=71).
- **Fable vs Mythos:** the same weights; "different doors to the same model" [FAB51 4:47](https://youtu.be/r_dw-1109Ag?t=287). Fable is generally available with filters on requests and responses; Mythos is for trusted-access programs, with safeguards tuned for cybersecurity and life-sciences work [FAB51 5:23](https://youtu.be/r_dw-1109Ag?t=323).

## 2. Strengths (with evidence)

**Long-running, maintainer-style agentic coding**

- **PR takeovers:** PRs other agents had left looping on review-bot feedback almost all landed [FAB51 41:14](https://youtu.be/r_dw-1109Ag?t=2474); it is "just barely better enough to push through that friction" [FAB51 41:37](https://youtu.be/r_dw-1109Ag?t=2497). One had failed more than 8 earlier attempts and landed in about 450 lines [FAB51 42:24](https://youtu.be/r_dw-1109Ag?t=2544); it also fixed integration bugs other agents missed [FAB51 42:30](https://youtu.be/r_dw-1109Ag?t=2550).
- **Audit, then parallel PRs:** a cleanup audit produced nine PRs ordered deletions-first, so each later PR is smaller [FAB51 43:21](https://youtu.be/r_dw-1109Ag?t=2601). Fable 5.1 subagents got all 10 merged, green on CI, CodeRabbit, Cursor Bugbot and Macroscope, with every bot thread answered or fixed [FAB51 44:05](https://youtu.be/r_dw-1109Ag?t=2645); net 340 files and 13K lines deleted [FAB51 44:18](https://youtu.be/r_dw-1109Ag?t=2658), and agents seemed to contribute better afterwards [FAB51 44:25](https://youtu.be/r_dw-1109Ag?t=2665).
- **Quality audit:** a 5.8/10 codebase score [FAB51 44:37](https://youtu.be/r_dw-1109Ag?t=2677) became 7 parallel subagent PRs, merged or taken over by a separate monitor agent [FAB51 44:59](https://youtu.be/r_dw-1109Ag?t=2699); some worst-case paths got 85 to 90% faster [FAB51 45:18](https://youtu.be/r_dw-1109Ag?t=2718), merged without him reading the code [FAB51 45:05](https://youtu.be/r_dw-1109Ag?t=2705). A from-scratch "V2" audit gave "great suggestions" [FAB51 45:41](https://youtu.be/r_dw-1109Ag?t=2741).
- **Merge judgment:** it has merged PRs on its own judgment "dozens of times" without burning him; it is "picky enough" to trust [FAB51 46:38](https://youtu.be/r_dw-1109Ag?t=2798).

**His PR metrics** (the model's own comparison of its first 24 hours against his *best* 24-hour windows with Fable 5 and 5.6 Sol, across T3 Code and Lakebed [FAB51 48:42](https://youtu.be/r_dw-1109Ag?t=2922)):

| Metric | Fable 5.1 | Fable 5 | Sol |
|---|---|---|---|
| PRs in the window | 13, median 489 LOC | (fewer, smaller) | |
| Packages touched per PR | up to 4 ("would make the changes in all the places it mattered") | usually 1 | usually 1 |
| Files per PR (avg) | 11 | 4 | 4 |
| High-severity review-bot findings per 1K LOC | **0.4** | 2.06 | 1.02 |
| Commits pushed after PR opened | 24 | 60+ | n/a |
| PRs closed as slop or superseded | 0 | n/a | n/a |
| Time to merge | "up to 50 minutes" | 47 min | 30 min ("the whole loop was just closed more") |
| PR filed to merged, after clear implementation instructions | median 14m41s | | |

Row sources: packages [FAB51 48:47](https://youtu.be/r_dw-1109Ag?t=2927), findings [FAB51 49:30](https://youtu.be/r_dw-1109Ag?t=2970), commits [FAB51 50:42](https://youtu.be/r_dw-1109Ag?t=3042), superseded [FAB51 49:56](https://youtu.be/r_dw-1109Ag?t=2996), merge time [FAB51 50:07](https://youtu.be/r_dw-1109Ag?t=3007), files [FAB51 50:18](https://youtu.be/r_dw-1109Ag?t=3018), filed-to-merged [FAB51 51:50](https://youtu.be/r_dw-1109Ag?t=3110). The merge-time row is self-contradictory in the captions: "up to 50 minutes" against 47 for Fable 5, described as "slightly faster".

- More code per minute but longer per PR [FAB51 49:12](https://youtu.be/r_dw-1109Ag?t=2952); "quality signal stayed strong" as PRs grew [FAB51 49:25](https://youtu.be/r_dw-1109Ag?t=2965). Sol "could go deep but often turn into scope creep" [FAB51 52:06](https://youtu.be/r_dw-1109Ag?t=3126); Fable 5 was faster to first draft and Sol could solve hard mechanisms [FAB51 51:32](https://youtu.be/r_dw-1109Ag?t=3092).

**Benchmarks cited from the official post**

- **Terminal Bench (Science, v0.1):** "almost twice as well at any given level", and cheaper because of the cache-read cut [FAB51 12:34](https://youtu.be/r_dw-1109Ag?t=754).
- **Terminal Bench 4:** low 40% vs 21.5% for Fable 5, at $5.70 vs $12.30 [FAB51 12:46](https://youtu.be/r_dw-1109Ag?t=766); max 55.8 vs 45.8, "under $20 instead of over 26" [FAB51 13:07](https://youtu.be/r_dw-1109Ag?t=787). Mythos scores higher because Fable 5.1 flags some tasks and falls back to Opus [FAB51 13:31](https://youtu.be/r_dw-1109Ag?t=811).
- **Humanity's Last Exam:** better and slightly cheaper, but "it doesn't seem to benefit as much going beyond high" [FAB51 13:53](https://youtu.be/r_dw-1109Ag?t=833).
- **Cursor Bench:** about 73% vs just over 70 for Fable 5's peak; the most expensive run fell to $9.64 per task from $17.32 [FAB51 14:25](https://youtu.be/r_dw-1109Ag?t=865). Low still costs more than Sol on high but scores better, "a very compelling option for a lot of work" [FAB51 14:50](https://youtu.be/r_dw-1109Ag?t=890).
- **AA Intelligence Index:** "higher than they've ever measured before", ahead of Opus 5, Fable 5, 5.6 Sol and Grok 4.6; about 4% of output tokens came from an Opus 5 fallback [FAB51 20:09](https://youtu.be/r_dw-1109Ag?t=1209).
- **AA intelligence vs output tokens:** every variant above 5.6 Sol medium is matched or beaten by some Fable 5.1 effort level "on both intelligence and token usage" (output tokens, not cost) [FAB51 21:41](https://youtu.be/r_dw-1109Ag?t=1301).
- **AA Omniscience (hallucination):** Anthropic holds every spot above Sol, which is in the 60% range [FAB51 22:51](https://youtu.be/r_dw-1109Ag?t=1371). His reading: Anthropic wants the model "to always be accurate"; OpenAI wants it to find and create new information "a little more readily" [FAB51 23:50](https://youtu.be/r_dw-1109Ag?t=1430).

- **Science (Mythos 5.1, Anthropic's claims):** protein-binder hit rate 10 times the best competition submissions on 3 targets, and nearly 50% across 12 targets against a typical 10 to 15% [FAB51 16:09](https://youtu.be/r_dw-1109Ag?t=969); a Venus map from 30-year-old NASA radar data, more accurate than existing maps and released under Creative Commons [FAB51 16:28](https://youtu.be/r_dw-1109Ag?t=988); a GPU kernel speeding open-source computational-biology models up to 2.5x at the same output quality [FAB51 17:02](https://youtu.be/r_dw-1109Ag?t=1022).

**Front end, 3D and writing**

- **Front end:** homepage design is "a generational leap" [FAB51 24:39](https://youtu.be/r_dw-1109Ag?t=1479), but only with Anthropic's front-end design skill: without it, "so much uglier" [FAB51 25:35](https://youtu.be/r_dw-1109Ag?t=1535), and "taste skill" output was "all pretty bad and boring" [FAB51 25:56](https://youtu.be/r_dw-1109Ag?t=1556). The design skill "is really back" [FAB51 25:56](https://youtu.be/r_dw-1109Ag?t=1556) after he had dropped it for hurting "as much as it helped" [FAB51 25:35](https://youtu.be/r_dw-1109Ag?t=1535). He had not pushed front end himself yet [FAB51 25:16](https://youtu.be/r_dw-1109Ag?t=1516).
- **Games and 3D:** polished 2D fish slop [FAB51 26:20](https://youtu.be/r_dw-1109Ag?t=1580); with Blender as a tool, 3D output was "way better than I've seen from existing models" [FAB51 27:48](https://youtu.be/r_dw-1109Ag?t=1668) and "the most workable starting point" despite mis-mapped controls [FAB51 28:19](https://youtu.be/r_dw-1109Ag?t=1699). He credits improved tool use such as Blender [FAB51 29:00](https://youtu.be/r_dw-1109Ag?t=1740).
- **Writing:** less "weird technical jargon", "much more readable" [FAB51 5:41](https://youtu.be/r_dw-1109Ag?t=341); the prompt guide claims "fewer stock phrases and less unexplained jargon" [FAB51 35:20](https://youtu.be/r_dw-1109Ag?t=2120).

## 3. Weaknesses, pitfalls and misconceptions

- **Misconception:** Fable and Mythos are not different models (section 1).
- **Safeguard fallback to Opus** lowers some scores (Terminal Bench 4; about 4% of AA output tokens). He hit a safeguard flag only once while draining most of five accounts' limits in 24 hours; Anthropic claims a 60% reduction in false positives [FAB51 11:52](https://youtu.be/r_dw-1109Ag?t=712).
- **Token-hungry.** "This model yaps a bit more": AA measured 1.7x Fable 5's output tokens; max cost $3.76 per index task, "20% more than Fable 5" [FAB51 20:41](https://youtu.be/r_dw-1109Ag?t=1241). Elsewhere he reads $3.69 per task vs $3.14 for Fable 5 and "95" for 5.6 Sol on max [FAB51 22:04](https://youtu.be/r_dw-1109Ag?t=1324); the transcript's numbers are inconsistent. It is "nowhere near" OpenAI's token efficiency: its high goes further than Sol's max, and medium further than Sol's xhigh [FAB51 15:02](https://youtu.be/r_dw-1109Ag?t=902).
- **Not for long one-shot work** that "could be done by other things" [FAB51 22:13](https://youtu.be/r_dw-1109Ag?t=1333). Its savings come from cache-heavy agentic loops.
- **Physics reasoning:** Sol still leads; "even 5.5 Pro is tied with Fable 5.1" [FAB51 22:45](https://youtu.be/r_dw-1109Ag?t=1365).
- **Low hallucination costs experimentation:** it is "less able to experiment and try things that aren't in its weights" [FAB51 23:28](https://youtu.be/r_dw-1109Ag?t=1408).
- **Computer use:** "nowhere near as far along as OpenAI stuff" [FAB51 15:33](https://youtu.be/r_dw-1109Ag?t=933).
- **Intent misread (his only real failure example):** on `high`, after 8 minutes, it wrongly reported "nothing links a PR to a thread automatically", because it did not count branch lookup as auto-linking [FAB51 39:02](https://youtu.be/r_dw-1109Ag?t=2342); "it just didn't get my intent" [FAB51 39:22](https://youtu.be/r_dw-1109Ag?t=2362).
- **Low effort misses hidden complexity:** if a simple-looking task has "some tiny piece you forgot about", "low will miss that" [FAB51 32:29](https://youtu.be/r_dw-1109Ag?t=1949).
- **Quirks from the official prompt guide:** fewer progress updates in long tool-call turns [FAB51 32:58](https://youtu.be/r_dw-1109Ag?t=1978) (one of his runs: 24m28s, over 60 tool calls, more than 30 in a row with no text [FAB51 33:35](https://youtu.be/r_dw-1109Ag?t=2015)); denser prose with longer sentences and fewer paragraph breaks [FAB51 35:27](https://youtu.be/r_dw-1109Ag?t=2127); unmarked reproduction of source passages in summaries [FAB51 36:29](https://youtu.be/r_dw-1109Ag?t=2189); stopping to ask "shall I apply this?" instead of finishing [FAB51 36:48](https://youtu.be/r_dw-1109Ag?t=2208); scope overreach: fixing nearby code, extending unrequested behaviour, committing more test files than warranted [FAB51 37:45](https://youtu.be/r_dw-1109Ag?t=2265).
- **Append-only history (API):** for new accounts, editing earlier turns "breaks the thread entirely and will kill all of the reasoning data" [FAB51 35:06](https://youtu.be/r_dw-1109Ag?t=2106). An anti-distillation measure, rolling out gradually to "all accounts" [FAB51 19:33](https://youtu.be/r_dw-1109Ag?t=1173); it hurts products with branching (he names "the PI team") [FAB51 19:21](https://youtu.be/r_dw-1109Ag?t=1161).
- **No zero data retention (ZDR)** for Fable or Mythos, so many enterprises use Opus or OpenAI instead [FAB51 10:32](https://youtu.be/r_dw-1109Ag?t=632). "Enterprise Frontier Safeguards" is a provisioned box run on the customer's own infrastructure (AWS etc.) to perform Anthropic's checks; he expects it to be expensive [FAB51 10:52](https://youtu.be/r_dw-1109Ag?t=652).
- **Watermarks** for EU AI Act compliance, with an API to detect Claude-generated text coming [FAB51 19:48](https://youtu.be/r_dw-1109Ag?t=1188).

## 4. Pricing, speed, context and limits

- **Price:** $10 per million input, $50 per million output (unchanged). **Cache reads $0.25/M, down from $1, a 75% cut** [FAB51 6:54](https://youtu.be/r_dw-1109Ag?t=414). The Sonnet video later calls this a "90%" drop; the figures ($1 to $0.25) support 75%.
- **Official claims:** about 25% less than Fable 5 for typical token-billed workloads, "up to 45%" for highly agentic work [FAB51 5:54](https://youtu.be/r_dw-1109Ag?t=354).
- **Why caching dominates:** every tool call restarts generation and re-reads the whole history [FAB51 9:11](https://youtu.be/r_dw-1109Ag?t=551). His Claude Code usage over the period: 42.8B cached input tokens vs 710M uncached [FAB51 8:22](https://youtu.be/r_dw-1109Ag?t=502); about $15K at API prices, about $25K total; without caching, "135,000 additional dollars" [FAB51 8:16](https://youtu.be/r_dw-1109Ag?t=496).
- **His Fable 5.1 spend** (about $2,000): cache writes about $1,200 (nearly 60%), outputs about $500, cache reads $264, uncached input $4 [FAB51 8:53](https://youtu.be/r_dw-1109Ag?t=533). "Writing to cache costs money" [FAB51 8:35](https://youtu.be/r_dw-1109Ag?t=515).
- **Cache TTL:** "5 minutes by default"; longer is "way more expensive" [FAB51 9:58](https://youtu.be/r_dw-1109Ag?t=598). Single-shot chat with one or two tool calls gains much less from the cache discount.
- **Subscriptions:** a $200/month Claude Code plan "can get you up to $8,000 a month of usage" [FAB51 6:41](https://youtu.be/r_dw-1109Ag?t=401). Expect to burn limits faster, "not because it's less efficient, but because you're going to have it do more" [FAB51 53:59](https://youtu.be/r_dw-1109Ag?t=3239).
- **Effort levels:** low, medium, high (default), xhigh, max.
- **Speed:** no TPS figure; longer per PR, more code per minute. **Context window:** not stated; compaction steering in section 5.

## 5. Recommended prompting style and workflow

From Anthropic's Fable 5.1 prompting guide, which he endorses, plus his own practice:

- **Prune CLAUDE.md:** look for what is deletable; "try deleting everything, see how it behaves, and then add parts back" [FAB51 32:11](https://youtu.be/r_dw-1109Ag?t=1931).
- **Effort:** start at `high`, then test others on your own evals. "High is a great default. Low is surprisingly capable" [FAB51 32:44](https://youtu.be/r_dw-1109Ag?t=1964). Returns diminish beyond `high`.
- **Progress updates:** ask for them explicitly when a human is watching, and remove old anti-chatter lines such as "hold all findings for the final response", which may now suppress output you want [FAB51 34:28](https://youtu.be/r_dw-1109Ag?t=2068). The guide's example asks for a one-line plan before starting, brief updates while working, and a short recap that stands on its own [FAB51 34:45](https://youtu.be/r_dw-1109Ag?t=2085).
- **Prose density:** tell it to drop "mannered prose" and use a literal phrase where one is available [FAB51 35:43](https://youtu.be/r_dw-1109Ag?t=2143); the guide's short form is "Please remove all mannered prose" [FAB51 35:48](https://youtu.be/r_dw-1109Ag?t=2148). His own unslop skill plus 5.1's defaults were already readable.
- **Formatting:** 5.1 uses less bold and fewer bullets; with old anti-formatting rules in CLAUDE.md "it's basically never going to do it", so remove them if you want formatting [FAB51 36:18](https://youtu.be/r_dw-1109Ag?t=2178).
- **Quotations:** give a complete example of a correct response in the system prompt to stop unmarked reproduction [FAB51 36:35](https://youtu.be/r_dw-1109Ag?t=2195).
- **Autonomy and finishing:** set a clear end point. The guide's autonomy block tells the model it is operating autonomously, the user cannot answer mid-task, so "want me to" / "shall I" questions block the work; reversible actions that follow from the request proceed without asking; stop only for destructive actions or genuine scope changes [FAB51 36:59](https://youtu.be/r_dw-1109Ag?t=2219).
- **Compaction steering:** tell the model what its compaction summaries must preserve, in user prompts or the system prompt; useful for client-side compaction [FAB51 37:22](https://youtu.be/r_dw-1109Ag?t=2242).
- **Scope control:** "it responds well to explicit instructions about what to leave out", for example limiting test files [FAB51 37:52](https://youtu.be/r_dw-1109Ag?t=2272).
- **Append-only histories** when building on the API (section 3).
- **His delegation prompt** gives the model his trust, tells it to spin up Fable 5.1 subagents, to "babysit them until they pass all the different checks and review agents", and: "Any of them are simple wins. Just merge them. I trust your judgment" [FAB51 43:34](https://youtu.be/r_dw-1109Ag?t=2614). Safe for him because the project "doesn't auto ship to prod" [FAB51 43:58](https://youtu.be/r_dw-1109Ag?t=2638).
- **"Takeover" skill:** instead of copying review feedback between agents, hand the PR to a new agent: "Get the branch on your work tree and it's yours", then push, maintain and manage it "so that it actually lands" [FAB51 40:09](https://youtu.be/r_dw-1109Ag?t=2409). Optionally ask the original agent afterwards what it thinks of the changes.

## 6. Subagents, orchestration, delegation and verification

- **Fable 5.1 as orchestrator:** it orchestrates subagents better "because it prompts itself better too", and burns more because it does more [FAB51 54:06](https://youtu.be/r_dw-1109Ag?t=3246).
- **Pattern 1:** audit, then a written plan ("proposed order of work", deletions first), then human approval, then parallel Fable 5.1 subagents each owning a PR, then babysitting CI and review bots (CodeRabbit, Cursor Bugbot, Macroscope), then merge [FAB51 43:27](https://youtu.be/r_dw-1109Ag?t=2607).
- **Pattern 2:** a separate merge-monitor agent watches all PRs on the repo, merges ready ones and takes over "if they weren't progressing fast enough" [FAB51 44:59](https://youtu.be/r_dw-1109Ag?t=2699).
- **Trust ladder (conclusion):** he now tells it to "find them, fix them, and merge them for me" [FAB51 53:30](https://youtu.be/r_dw-1109Ag?t=3210), especially "bug fixes and performance improvements"; product-opinion changes stay with the human [FAB51 53:52](https://youtu.be/r_dw-1109Ag?t=3232).
- **Verification** is CI plus third-party review bots, with every bot thread answered or fixed before merge. The model comparison in section 2 was itself done by Sol (implied) from PR history.

## 7. Claude Code specifics

- CLAUDE.md: prune it; remove anti-update and anti-formatting rules (section 5).
- Skills: Anthropic's front-end design skill markedly improves 5.1's designs; the "taste skill" does not. He uses his own "unslop" and "takeover" skills. The Claude Agent SDK "fights you every step" on `$`-invoked user skills [FAB51 41:55](https://youtu.be/r_dw-1109Ag?t=2515).
- Subscription economics: $200/month gives up to about $8K/month of API-equivalent usage. Hooks, MCP and plugins: not discussed.

## 8. Routing-table implications (Fable 5.1)

- **Route to Fable 5.1:** long-horizon, multi-package agentic coding that must survive review and land, including taking over stuck or looping PRs and cross-cutting changes (11 files and 4 packages per PR on average) with low high-severity defect rates.
- **Route to Fable 5.1 as orchestrator** for large cleanups and audits that decompose into parallel PRs: it plans well (ordered PRs, deletions first) and prompts its own subagents well.
- **Route to Fable 5.1:** PR triage, vetting and merge decisions for bug fixes and performance work, where its pickiness is an asset.
- **Route to Fable 5.1 (with the design skill loaded):** front-end, marketing-page and animation-heavy design, and 3D or Blender-assisted creative builds.
- **Default effort `high`.** Try `low` for routine tasks ("surprisingly capable"), not where hidden complexity is likely. Avoid going beyond `high` without evidence.
- **Do not route to Fable 5.1:** long one-shot, non-agentic generation another model could do. Its cost advantage is cache reads in agentic loops, and it is verbose (1.7x output tokens).
- **Do not route to Fable 5.1:** computer use (OpenAI models are better) or physics-heavy reasoning (Sol leads).
- **Do not route to Fable/Mythos:** workloads needing ZDR or strict data retention; use Opus unless Enterprise Frontier Safeguards is in place. Expect occasional safeguard fallbacks to Opus on security- or bio-adjacent tasks.
- **Prompting rules:** state an explicit end condition and the autonomy policy, ask for progress updates if a human is watching, state what is out of scope (no nearby fixes, limited test files), and keep histories append-only.
- **Ambiguous intent:** its rare failures are definitional misreads. For audit-style questions, define terms precisely in the prompt.

---

# Video 2: Claude Opus 5.5

## 1. Subject and overall thesis

- Day-one review of **Claude Opus 5.5**. Opus 5 had felt "more like a liability than an actual thing you could rely on" [OPUS55 0:54](https://youtu.be/jgGyX7MPPVg?t=54); 5.5 is cheaper, "less bad at writing", and "way better at code and following instructions" [OPUS55 1:41](https://youtu.be/jgGyX7MPPVg?t=101). Too early to call it a "Fable killer" [OPUS55 1:41](https://youtu.be/jgGyX7MPPVg?t=101).
- Anthropic's headline: it performs at Fable 5.1's level on most work and "costs 40% less to run than Opus 5" [OPUS55 3:53](https://youtu.be/jgGyX7MPPVg?t=233).
- **Bottom line:** Opus is "probably the right default for the vast majority of stuff", but don't be "scared to reach to Fable for front end" [OPUS55 26:00](https://youtu.be/jgGyX7MPPVg?t=1560). Caveat: "this model is smaller. It is dumber"; Fable makes mistakes too, "just less so" [OPUS55 37:41](https://youtu.be/jgGyX7MPPVg?t=2261).
- Context: four major model drops in two days (Grok 4.7, Opus 5.5, GPT-6 Sol and Luna) [OPUS55 3:24](https://youtu.be/jgGyX7MPPVg?t=204); the first Anthropic release since it called for "pacing the frontier" [OPUS55 3:58](https://youtu.be/jgGyX7MPPVg?t=238).

## 2. Strengths (with evidence)

- **Anthropic claims:** a tester did "a 680,000 line of code migration in less than a day" [OPUS55 4:11](https://youtu.be/jgGyX7MPPVg?t=251); strong at fixing software inefficiencies, which he confirms on "pretty brutal" performance work [OPUS55 4:17](https://youtu.be/jgGyX7MPPVg?t=257).
- **Benchmarks:** wins almost all of Anthropic's charts except Terminal Bench Science (agentic scientific research) [OPUS55 6:07](https://youtu.be/jgGyX7MPPVg?t=367) and Automation Bench (business workflows) [OPUS55 6:13](https://youtu.be/jgGyX7MPPVg?t=373).
  - **Terminal Bench 4:** Opus 5.5 medium beats Fable 5.1 max, at **$2.94 vs $20** [OPUS55 6:42](https://youtu.be/jgGyX7MPPVg?t=402), with "a slight dip on max" [OPUS55 6:50](https://youtu.be/jgGyX7MPPVg?t=410).
  - **Frontier Code:** new all-time highs at medium and max; best score at medium. He calls the bench "weird" [OPUS55 6:56](https://youtu.be/jgGyX7MPPVg?t=416).
  - **Cursor Bench:** medium beats Fable 5.1 max. Astra is absent because "OpenAI has banned Cursor from using their models" [OPUS55 7:18](https://youtu.be/jgGyX7MPPVg?t=438).
  - **AA Intelligence Index:** "a massive lead", 5 points over Fable 5.1 [OPUS55 13:12](https://youtu.be/jgGyX7MPPVg?t=792), which he thinks "more so showcases how bad these benchmarks are" [OPUS55 13:40](https://youtu.be/jgGyX7MPPVg?t=820).
  - **AA at high:** 53 vs 50.9 for GPT-6 Astra on high, at a higher cost [OPUS55 8:19](https://youtu.be/jgGyX7MPPVg?t=499).
  - **AA Pareto frontier:** "Opus 5.5 has swept this line", the best price for every score "in the 50 plus range" [OPUS55 15:42](https://youtu.be/jgGyX7MPPVg?t=942). Edwin's claim that medium is "Fable 5.1 level intelligence" is "a bit of a reach", but medium costs $1.34 per task vs "6 plus for Fable" [OPUS55 17:17](https://youtu.be/jgGyX7MPPVg?t=1037).
  - **Knowledge work** (Excel etc.): improved; he does not care much [OPUS55 8:48](https://youtu.be/jgGyX7MPPVg?t=528).
- **Communication and writing: "my favorite change by far"** [OPUS55 5:17](https://youtu.be/jgGyX7MPPVg?t=317): "the most important information up front" [OPUS55 5:30](https://youtu.be/jgGyX7MPPVg?t=330), and a tester said "it writes the way I do" [OPUS55 5:37](https://youtu.be/jgGyX7MPPVg?t=337) (Anthropic's example: a clear, dollar-attributed billing-bug explanation where Opus 5 produced jargon and em dashes). He **deleted his "unslop" instructions from CLAUDE.md** and does not plan to re-add them [OPUS55 10:03](https://youtu.be/jgGyX7MPPVg?t=603).
- **Agentic day-one work:** it built an AA data visualizer and verified it with computer use [OPUS55 15:59](https://youtu.be/jgGyX7MPPVg?t=959) [OPUS55 20:06](https://youtu.be/jgGyX7MPPVg?t=1206). From a one-line "find the repo, and make a PR" request it located the repo, refreshed the stale clone, used a worktree, verified and merged the fix [OPUS55 20:13](https://youtu.be/jgGyX7MPPVg?t=1213), for "1% of my weekly" usage [OPUS55 20:25](https://youtu.be/jgGyX7MPPVg?t=1225).
- **3D and games:** fish-slop 3D at 120 FPS on default `medium` [OPUS55 30:48](https://youtu.be/jgGyX7MPPVg?t=1848); an `xhigh` polish pass [OPUS55 31:16](https://youtu.be/jgGyX7MPPVg?t=1876) produced the first version he had to remind himself was "just a demo" [OPUS55 32:26](https://youtu.be/jgGyX7MPPVg?t=1946). Strong community demos (a Dark Souls clone, a flight sim, an engine-less C++ skater) [OPUS55 28:02](https://youtu.be/jgGyX7MPPVg?t=1682) [OPUS55 28:19](https://youtu.be/jgGyX7MPPVg?t=1699) [OPUS55 29:11](https://youtu.be/jgGyX7MPPVg?t=1751). Better at three.js than native tech; computer use catches visual flicker, "but not always" [OPUS55 30:16](https://youtu.be/jgGyX7MPPVg?t=1816).
- **His code-review / deep-audit bench:** Opus 5.5 nearly doubled Opus 5's "accuracy and reliability of its findings" [OPUS55 22:15](https://youtu.be/jgGyX7MPPVg?t=1335), but still trails Grok 4.7 and Sol (section 3).
- **PR quality** (about 5 PRs, limited data): similar to lower rates of "egregious high severity issues" and a similar to slightly higher number of nitpicks vs Fable 5.1 [OPUS55 36:52](https://youtu.be/jgGyX7MPPVg?t=2212). Gut feel: very similar to Fable 5.1 with slightly higher overall quality, especially prose, but its spikes "go a little lower than fables do" [OPUS55 37:23](https://youtu.be/jgGyX7MPPVg?t=2243).
- **HTML generation:** Mia ran 100 page generations and called it "the best model that she's ever tested" [OPUS55 26:26](https://youtu.be/jgGyX7MPPVg?t=1586); he partly disagrees (section 3).

## 3. Weaknesses, pitfalls and misconceptions

- **Cheaper, but less token-efficient:** "it's not because it's more efficient"; it is "meaningfully less efficient than Opus 5" [OPUS55 13:58](https://youtu.be/jgGyX7MPPVg?t=838).
  - AA tokens per task at max: Opus 5 73K, Fable 78K, **Opus 5.5 about 120K**, GPT-6 Astra 27K; "really a 4x gap in efficiency" [OPUS55 14:19](https://youtu.be/jgGyX7MPPVg?t=859).
  - AA cost per run at max: Opus 5 $5.86, Opus 5.5 "almost six bucks", Fable $7.63 [OPUS55 14:44](https://youtu.be/jgGyX7MPPVg?t=884); it "comes close to being the most expensive model that artificial analysis has run" [OPUS55 14:37](https://youtu.be/jgGyX7MPPVg?t=877). AA says it would have been 80% more expensive without the price and cache cuts [OPUS55 16:59](https://youtu.be/jgGyX7MPPVg?t=1019).
- **Effort hazards: avoid `low` and `max`.**
  - "Low is really bad" [OPUS55 8:27](https://youtu.be/jgGyX7MPPVg?t=507), "just not that capable considering the price" [OPUS55 15:31](https://youtu.be/jgGyX7MPPVg?t=931). Low and max are "dangerous and generally best avoided"; medium, high and xhigh "have seemed really good" [OPUS55 8:36](https://youtu.be/jgGyX7MPPVg?t=516).
  - **Runaway max:** a thread ran "6 hours and 30 minutes writing a markdown plan" on max, in loops [OPUS55 17:39](https://youtu.be/jgGyX7MPPVg?t=1059); he stopped it, switched to xhigh, asked for an update, and it was about halfway done [OPUS55 17:52](https://youtu.be/jgGyX7MPPVg?t=1072).
  - **Skatebench:** xhigh about 330 reasoning tokens per question, max almost 5,000, "over a 10x gap" for about a 1% score gain [OPUS55 18:27](https://youtu.be/jgGyX7MPPVg?t=1107); it also scored worse than Opus 5 on Skatebench [OPUS55 18:16](https://youtu.be/jgGyX7MPPVg?t=1096).
  - "Don't use Max on this model", unless you "want to watch tokens burn" [OPUS55 19:03](https://youtu.be/jgGyX7MPPVg?t=1143).
- **Exhaustive code review and sweeping audits are weaker than OpenAI's.** On his bench for finding real quality improvements in big codebases, Grok 4.7 (likely helped by Cursor/Bugbot review data [OPUS55 21:51](https://youtu.be/jgGyX7MPPVg?t=1311)) and Sol do better, "Opus and Fable less" [OPUS55 22:02](https://youtu.be/jgGyX7MPPVg?t=1322). It "might not be as strong at those things as OpenAI's Frontier is" [OPUS55 22:32](https://youtu.be/jgGyX7MPPVg?t=1352); for him this is an occasional task, "once every two or so weeks" [OPUS55 22:39](https://youtu.be/jgGyX7MPPVg?t=1359).
- **Thoroughness ranking:** Fable is "still slightly more thorough"; Astra is "the most thorough" but "very spiky and weird" [OPUS55 25:54](https://youtu.be/jgGyX7MPPVg?t=1554).
- **Front-end design is weaker than Fable 5.1:** "a little sloppy" [OPUS55 25:04](https://youtu.be/jgGyX7MPPVg?t=1504), half Tailwind templates [OPUS55 25:22](https://youtu.be/jgGyX7MPPVg?t=1522), half pastel with big shadows [OPUS55 25:28](https://youtu.be/jgGyX7MPPVg?t=1528). The official design skill makes little difference (slightly better without) [OPUS55 25:10](https://youtu.be/jgGyX7MPPVg?t=1510). "Fable still is the GOAT for a handful of things" [OPUS55 25:47](https://youtu.be/jgGyX7MPPVg?t=1547). Mia's 100-generation result is a dissenting data point.
- **Context-window anxiety**, "one of the most frustrating" quirks: while monitoring another instance it worried its context was "10% from autocompact" and work would be lost [OPUS55 34:45](https://youtu.be/jgGyX7MPPVg?t=2085); "none of this is stuff the model should think about or care about" [OPUS55 34:58](https://youtu.be/jgGyX7MPPVg?t=2098). "OpenAI has entirely beat this out of the models" so they trust compaction; Anthropic leaned on the 1M-token window where OpenAI caps at 272K [OPUS55 33:54](https://youtu.be/jgGyX7MPPVg?t=2034).
- **Dumb spikes, "small model feel"** at the edges [OPUS55 35:47](https://youtu.be/jgGyX7MPPVg?t=2147); Fable would not say such nonsense, "Astra perhaps" [OPUS55 35:53](https://youtu.be/jgGyX7MPPVg?t=2153). Discernment weakens when things are "already in a bad state", e.g. auditing why a job is slow [OPUS55 35:28](https://youtu.be/jgGyX7MPPVg?t=2128).
- **Failure risk grows with job length** ("goes up, not down") [OPUS55 37:47](https://youtu.be/jgGyX7MPPVg?t=2267); on performance work it may repair things it doesn't need to [OPUS55 37:55](https://youtu.be/jgGyX7MPPVg?t=2275). **Slow to commit:** one run held "almost three hours" of changes uncommitted [OPUS55 34:38](https://youtu.be/jgGyX7MPPVg?t=2078). 3D visual bugs persist (lighting blend [OPUS55 31:58](https://youtu.be/jgGyX7MPPVg?t=1918), transparency [OPUS55 36:15](https://youtu.be/jgGyX7MPPVg?t=2175)).

## 4. Pricing, speed, context and limits

- **Price:** "$4 per mill in and $20 per mill out" (20% less than Opus 5) [OPUS55 4:45](https://youtu.be/jgGyX7MPPVg?t=285). **Cache reads $0.20/M**, "60% cheaper" [OPUS55 4:59](https://youtu.be/jgGyX7MPPVg?t=299). Cache writes $5/M (from the Sonnet video, section V3.4).
- **Cost vs Opus 5:** 40% less on typical workloads at default settings [OPUS55 3:53](https://youtu.be/jgGyX7MPPVg?t=233).
- **AA cost per task by effort** [OPUS55 15:11](https://youtu.be/jgGyX7MPPVg?t=911): medium about **$1.34** vs $3.26 for Astra (max) and about $6 for Opus 5.5 max; high "about half the price of Astra on Max"; xhigh "a lot closer to Astra's costs".
- **Speed:** "about 30% faster" than Opus 5 [OPUS55 5:05](https://youtu.be/jgGyX7MPPVg?t=305). The Sonnet video adds about 70 TPS via OpenRouter (Anthropic) and about 100 TPS on his subscription (section V3.4).
- **Context:** Anthropic leans on a 1M-token window (OpenAI usually caps at 272K) [OPUS55 34:06](https://youtu.be/jgGyX7MPPVg?t=2046). Compaction is "way faster" now and works well [OPUS55 35:03](https://youtu.be/jgGyX7MPPVg?t=2103).
- **Cache-friendly effort switching:** "Now you can change reasoning levels midsession without busting [cache]"; previously the effort level sat in the system prompt and invalidated the cache [OPUS55 13:01](https://youtu.be/jgGyX7MPPVg?t=781).
- **Default effort appears to be `medium`:** "this is the default reasoning level for the model" [OPUS55 31:09](https://youtu.be/jgGyX7MPPVg?t=1869).
- **Usage limits:** a full day of heavy use cost about 20% of one account's weekly limit [OPUS55 19:49](https://youtu.be/jgGyX7MPPVg?t=1189); the bug-fix PR cost 1%. Anthropic bumped the five-hour limit, which he has not come close to hitting [OPUS55 38:44](https://youtu.be/jgGyX7MPPVg?t=2324). The $200 Claude sub "is running laps around" OpenAI for subscription value, "maybe not in the pure API prices" [OPUS55 38:37](https://youtu.be/jgGyX7MPPVg?t=2317).
- **ZDR:** zero data retention is available on Opus, not Fable/Mythos; from this detail alone it will become "the most popular for coding with AI by far" [OPUS55 10:20](https://youtu.be/jgGyX7MPPVg?t=620) [OPUS55 10:54](https://youtu.be/jgGyX7MPPVg?t=654).
- Sonnet 5.5 and Haiku 5.5 were announced for the "coming weeks"; Haiku 5.5 would be the "first Haiku release in a year" [OPUS55 5:48](https://youtu.be/jgGyX7MPPVg?t=348).

## 5. Recommended prompting style and workflow

- **Use `medium`, `high` or `xhigh`; never `low` or `max`.** Medium is the cost-efficiency sweet spot; raise to xhigh for refinement passes (the "as visually appealing as possible" pass used xhigh).
- **Refinement loop:** draft at the default, then polish at higher effort. Effort can change mid-session without losing the cache, so escalate or de-escalate within a thread rather than starting over (section 4).
- **Drop anti-slop instructions** from CLAUDE.md [OPUS55 10:03](https://youtu.be/jgGyX7MPPVg?t=603).
- **A run that seems stuck on max:** stop it, switch to xhigh, ask for a status update [OPUS55 17:52](https://youtu.be/jgGyX7MPPVg?t=1072).
- **Performance work and long jobs:** watch for unnecessary repair loops and context anxiety. Telling it to commit frequently may help; that is our inference from the slow-to-commit complaint, not a stated tip.
- **Front end:** give explicit design direction, or use Fable. (The Sonnet video says Opus is "relatively steerable towards good designs" [SON55 20:19](https://youtu.be/8WbW_n95wc4?t=1219).)

## 6. Subagents, orchestration, delegation and verification

- **Cross-machine orchestration:** Claude Code on his machine SSHed into another machine to launch Claude Code there, then monitored it; the context-anxiety report came from this [OPUS55 34:25](https://youtu.be/jgGyX7MPPVg?t=2065).
- **Self-verification:** it checked the visualizer and visual fixes with computer use, and verified its own PR fix before merge (section 2).
- **Model choice:** Opus as the default for most work; Fable for front end, marketing pages, big design overhauls, when thoroughness matters, and in degraded states where Opus may produce nonsense; Astra (or Grok/Sol) for exhaustive review and sweeping-improvement audits.
- **Cost:** his Opus fish-slop run "did actually use a Fable 5.1 sub agent at some point" (Sonnet video) [SON55 26:32](https://youtu.be/8WbW_n95wc4?t=1592), so Opus will spawn Fable subagents if allowed.

## 7. Claude Code specifics

- CLAUDE.md: he removed his "unslop" instructions.
- The official Claude Code design skill gives Opus 5.5 only marginal gains.
- Effort switching mid-session no longer busts the cache, because the effort level moved out of the cached system-prompt prefix.
- He used the Claude Code desktop app [OPUS55 19:35](https://youtu.be/jgGyX7MPPVg?t=1175); Claude Code can SSH into another machine and launch Claude Code there (section 6).
- Auto-compaction works, but the model is anxious about it. Hooks, MCP and plugins: not discussed.

## 8. Routing-table implications (Opus 5.5)

- **Default workhorse.** Route most day-to-day coding, bug fixing, feature work, migrations and performance optimisation to Opus 5.5 at `medium`/`high`. On many coding benches medium matches or beats Fable 5.1 max at a fraction of the cost.
- **Enterprise / ZDR-constrained workloads** must route to Opus, not Fable or Mythos.
- **Effort policy:** default `medium`; `high` for normal complex work; `xhigh` for refinement or quality passes. **Never `low`** (poor value) and **never `max`** (over 10x tokens, loops, 6.5-hour runaway plan).
- **User-facing writing, explanations and status reports** go to Opus 5.5: clear, leads with the most important information, needs no anti-slop prompting.
- **3D, three.js and web-game builds:** strong, especially in the browser.
- **Do not route** exhaustive code review, "find everything wrong" audits or sweeping architecture critiques to Opus. Prefer Astra, Sol or Grok 4.7, or Sonnet 5.5 for cheap deep-dive analysis (Video 3).
- **Do not route** high-taste front-end or marketing-page design to Opus when Fable is available.
- **Very long or degraded-state jobs** (multi-hour performance work, auditing why something is stuck): consider Fable or add guardrails. Opus has dumb spikes, context anxiety and unnecessary repair loops, and failure probability rises with job length.
- **Cost control:** watch for Opus spawning Fable subagents; pin the subagent model in the routing config.
- **Prefer a subscription over API billing** for Opus-heavy use: the value comes from subscription limits, because Opus 5.5 is token-hungry (about 120K tokens per AA task at max vs 27K for Astra).

---

# Video 3: Claude Sonnet 5.5

## 1. Subject and overall thesis

- Review of **Claude Sonnet 5.5**, "the second model in the 5.5 family" [SON55 3:19](https://youtu.be/8WbW_n95wc4?t=199). On AA it "comes out as more expensive and dumber than Opus 5.5 at every single level" [SON55 0:53](https://youtu.be/8WbW_n95wc4?t=53), yet he calls it "an incredible model" [SON55 0:41](https://youtu.be/8WbW_n95wc4?t=41), **as a tool other models call, not one a human selects**:
  - Offered Fable, Opus and Sonnet in Claude Code, "I really don't think many people should be picking Sonnet" [SON55 21:14](https://youtu.be/8WbW_n95wc4?t=1274).
  - "Its strengths come as a tool for our other models to use", one of the things Opus or Fable orchestrate on complex work [SON55 21:44](https://youtu.be/8WbW_n95wc4?t=1304).
  - "This model is useful as long as you're not the one sending it prompts" [SON55 31:05](https://youtu.be/8WbW_n95wc4?t=1865).
- He has not "chosen Fable for any tasks for over a week" because Opus 5.5 took over his workflows [SON55 0:07](https://youtu.be/8WbW_n95wc4?t=7). He reads the release as aimed at OpenAI [SON55 0:12](https://youtu.be/8WbW_n95wc4?t=12), specifically GPT-6 Sol, which he considers "kind of just DOA" [SON55 15:04](https://youtu.be/8WbW_n95wc4?t=904).

## 2. Strengths (with evidence)

- **Anthropic positioning:** "Opus is built for complex work requiring careful judgment. Sonnet 5.5 is strongest at well scoped everyday tasks" [SON55 4:05](https://youtu.be/8WbW_n95wc4?t=245); also good "for fixing bugs and creating polished documents, slides, and spreadsheets" [SON55 4:24](https://youtu.be/8WbW_n95wc4?t=264). It claims a "sharp eye" for design, which he disputes (section 3) [SON55 4:54](https://youtu.be/8WbW_n95wc4?t=294).
- **Benchmarks:**
  - **Terminal Bench 4:** 70.6%, up from 10.3% for Sonnet 5 [SON55 5:24](https://youtu.be/8WbW_n95wc4?t=324) ("seven times better" [SON55 5:54](https://youtu.be/8WbW_n95wc4?t=354)), the highest score yet, which makes him "skeptical of terminal bench" [SON55 5:37](https://youtu.be/8WbW_n95wc4?t=337). Sonnet max outperformed Opus max there, but Sonnet max is also more expensive than Opus max [SON55 15:46](https://youtu.be/8WbW_n95wc4?t=946).
  - **GDPval:** slightly below Opus 5.5 [SON55 6:00](https://youtu.be/8WbW_n95wc4?t=360).
  - Strong on "long horizon work and image understanding"; the first Sonnet to beat Pokémon Red from screenshots alone [SON55 6:06](https://youtu.be/8WbW_n95wc4?t=366).
  - **OS World computer use:** much better than before, neck and neck with Opus 5.5; he still uses Astra "almost exclusively for computer use" [SON55 15:15](https://youtu.be/8WbW_n95wc4?t=915).
  - **Frontier Code:** xhigh scored *higher* than max; max put it below Sol, xhigh above Sol [SON55 14:50](https://youtu.be/8WbW_n95wc4?t=890).
  - **Cursor Bench:** Sonnet on high "does complement the Opus 5.5 curve relatively well" [SON55 17:07](https://youtu.be/8WbW_n95wc4?t=1027).
- **Feel:** "slightly dumber, way faster versions of Fable" [SON55 6:37](https://youtu.be/8WbW_n95wc4?t=397). He speculates Anthropic has got better at distilling its own models [SON55 6:50](https://youtu.be/8WbW_n95wc4?t=410).
- **Writing:** "writes way more clearly than their previous generation" [SON55 7:13](https://youtu.be/8WbW_n95wc4?t=433), with the "clawisms" (Claude-isms) gone [SON55 7:07](https://youtu.be/8WbW_n95wc4?t=427).
- **Deep-dive codebase analysis (key strength).** His audit bench asks how to land a huge PR (hundreds of thousands of LOC) in pieces [SON55 22:08](https://youtu.be/8WbW_n95wc4?t=1328), scored by "my automated judging panel" [SON55 23:16](https://youtu.be/8WbW_n95wc4?t=1396); it tests architectural analysis and comprehension, "not traditional code work" [SON55 23:22](https://youtu.be/8WbW_n95wc4?t=1402).
  - Astra produced "by far the best plan" [SON55 22:58](https://youtu.be/8WbW_n95wc4?t=1378). **Sonnet scored slightly above Opus at about half the price** [SON55 23:04](https://youtu.be/8WbW_n95wc4?t=1384), **in about 5 minutes** [SON55 23:57](https://youtu.be/8WbW_n95wc4?t=1437); Opus took "almost twice as long", Astra "almost three times as long", and Sol was faster "but at like half the score" [SON55 24:03](https://youtu.be/8WbW_n95wc4?t=1443). Fable stayed below Opus even after a judging overhaul [SON55 22:39](https://youtu.be/8WbW_n95wc4?t=1359). "The best value I've seen in this bench by far" [SON55 23:46](https://youtu.be/8WbW_n95wc4?t=1426).
- **Context tracking:** it reads an ambiguous follow-up in the frame of the current thread, "a pretty logical decision" [SON55 25:52](https://youtu.be/8WbW_n95wc4?t=1552).
- **Fish-slop 3D:** "one of the best I've ever seen" [SON55 27:04](https://youtu.be/8WbW_n95wc4?t=1624), better than Opus's in some ways and Astra's in all [SON55 27:18](https://youtu.be/8WbW_n95wc4?t=1638); 120 FPS [SON55 28:30](https://youtu.be/8WbW_n95wc4?t=1710); about 40 minutes, about $16 at API prices [SON55 28:44](https://youtu.be/8WbW_n95wc4?t=1724).
- He would take Sonnet over Astra for day-to-day code because it "does have fewer dumb spikes" [SON55 14:09](https://youtu.be/8WbW_n95wc4?t=849), but "I would just use Opus" [SON55 14:20](https://youtu.be/8WbW_n95wc4?t=860).

## 3. Weaknesses, pitfalls and misconceptions

- **Misconception: Sonnet is cheaper than Opus in practice.** For agentic coding it usually isn't.
  - The cache-read price **was not cut**: $0.20/M, the same as Opus 5.5, while input, output and cache writes are half of Opus's [SON55 8:05](https://youtu.be/8WbW_n95wc4?t=485). [Update 2026-10-08: cache reads cut to $0.10 at the Haiku 5.5 launch; see § V4.4.]
  - In agentic work cache reads dominate: uncached input is "barely touched" and output a small portion [SON55 10:34](https://youtu.be/8WbW_n95wc4?t=634). The cache-read share of cost is under 5% with Fable, "closer to 20% with Opus" and "like 50 plus with Sonnet" [SON55 10:09](https://youtu.be/8WbW_n95wc4?t=609).
  - "Sonnet consistently comes out as if not more expensive than opus does" on like-for-like code tasks [SON55 10:50](https://youtu.be/8WbW_n95wc4?t=650).
  - On AA, "Sonnet 5.5 cost roughly the same as Fable 5.1" [SON55 10:58](https://youtu.be/8WbW_n95wc4?t=658), neck and neck with Fable 5.1 "for the most expensive run they've ever done", mostly because of `max` [SON55 11:12](https://youtu.be/8WbW_n95wc4?t=672).
  - In fish slop, Sonnet used more than 3.5x Opus's input tokens at similar total cost; the Opus run was inflated by an accidental Fable subagent, so Opus "would have even been cheaper" [SON55 26:51](https://youtu.be/8WbW_n95wc4?t=1611).
- **Not token-efficient.** On Cursor Bench, 271,920 tokens per task, the most ever recorded, vs Opus 218K [SON55 17:41](https://youtu.be/8WbW_n95wc4?t=1061) and Gemini 3.8 Flash 162K; "more than 5x the number of tokens" of GPT 5.6 Sol and GPT-6 Astra [SON55 17:49](https://youtu.be/8WbW_n95wc4?t=1069).
- **Faster TPS, slower wall clock.** Fish slop: 43 min on Sonnet vs 36 on Opus [SON55 18:38](https://youtu.be/8WbW_n95wc4?t=1118); generation time 39 vs 27 min [SON55 18:49](https://youtu.be/8WbW_n95wc4?t=1129). "It's faster, but actually slower because of the token differences" [SON55 20:51](https://youtu.be/8WbW_n95wc4?t=1251).
- **Weak front-end design:** "opinionated" [SON55 19:18](https://youtu.be/8WbW_n95wc4?t=1158), "hideous" [SON55 19:42](https://youtu.be/8WbW_n95wc4?t=1182), "awful" animations [SON55 19:49](https://youtu.be/8WbW_n95wc4?t=1189), scroll bugs; worse than Opus, "significantly worse" than Fable [SON55 20:07](https://youtu.be/8WbW_n95wc4?t=1207), and like-for-like Opus costs about the same [SON55 20:38](https://youtu.be/8WbW_n95wc4?t=1238).
- **Medium is weaker on Sonnet:** "medium is a lot stronger with Opus than it is with Sonnet" [SON55 16:48](https://youtu.be/8WbW_n95wc4?t=1008); Frontier Code shows "pretty big drops" at medium and low [SON55 16:17](https://youtu.be/8WbW_n95wc4?t=977).
- **Effort warnings for all Anthropic models:**
  - **Max:** "Pretend it doesn't exist" [SON55 14:31](https://youtu.be/8WbW_n95wc4?t=871). Effort levels are budgets (ceilings), but max effectively raises the *floor*: "it's not done until it does a certain number of reasoning tokens" [SON55 12:21](https://youtu.be/8WbW_n95wc4?t=741).
  - On some benches low to xhigh added about 5 to 8% tokens [SON55 11:57](https://youtu.be/8WbW_n95wc4?t=717), while xhigh to max added "a 1,500% increase" [SON55 12:34](https://youtu.be/8WbW_n95wc4?t=754). Max "can often actually hurt performance", because the model starts "second guessing itself" [SON55 12:45](https://youtu.be/8WbW_n95wc4?t=765).
  - **Low:** "I don't think you should use any anthropic model on low right now" [SON55 16:22](https://youtu.be/8WbW_n95wc4?t=982). Anthropic removed the no-reasoning (instant) option on Opus, and presumably Sonnet [SON55 16:29](https://youtu.be/8WbW_n95wc4?t=989), "because these models suck without reasoning" [SON55 16:40](https://youtu.be/8WbW_n95wc4?t=1000).
  - "Generally avoid low, avoid max. And for the most part, medium's fine-ish" [SON55 16:48](https://youtu.be/8WbW_n95wc4?t=1008).
- Anthropic's charts show score vs cost, never score vs tokens; he implies this is deliberate [SON55 17:22](https://youtu.be/8WbW_n95wc4?t=1042).
- Anthropic's "30% faster / up to 30% cheaper" claims vs Sonnet 5 are "intentionally dancing around" max effort and cache-read realities [SON55 7:51](https://youtu.be/8WbW_n95wc4?t=471).

## 4. Pricing, speed, context and limits

- **Price:** $2/M input, $10/M output (same as Sonnet 5), cache reads $0.20/M [SON55 7:32](https://youtu.be/8WbW_n95wc4?t=452), cache writes $2.50/M. [Update 2026-10-08: cache reads cut to $0.10 at the Haiku 5.5 launch; see § V4.4.]
  - For comparison he gives Opus 5.5 at $4 / $20 / cache read $0.20 / cache write $5 [SON55 9:00](https://youtu.be/8WbW_n95wc4?t=540) and Fable 5.1 at $10 / $50 / cache read $0.25, Fable's cache read being "only 25% more" than Opus's [SON55 9:44](https://youtu.be/8WbW_n95wc4?t=584).
- **Claims vs Sonnet 5:** "30% faster and up to 30% cheaper for most work" [SON55 3:25](https://youtu.be/8WbW_n95wc4?t=205).
- **AA cost per run:** max $7.60 [SON55 13:09](https://youtu.be/8WbW_n95wc4?t=789) vs Astra max $3.26 [SON55 13:17](https://youtu.be/8WbW_n95wc4?t=797); xhigh "pretty close to Astra's price", cheaper [SON55 13:39](https://youtu.be/8WbW_n95wc4?t=819); high and medium "crazy low prices, $18 and 59 respectively" [SON55 13:46](https://youtu.be/8WbW_n95wc4?t=826) (probably $1.18 and $0.59; the transcript is ambiguous). At xhigh it is "roughly Astra level" on intelligence; at max about 3 points above Astra [SON55 13:58](https://youtu.be/8WbW_n95wc4?t=838).
- **TPS:** about 94 on OpenRouter (Anthropic) vs Opus 5.5 about 70 and Astra about 30 [SON55 18:10](https://youtu.be/8WbW_n95wc4?t=1090); on his subscription about 150 vs about 100 for Opus [SON55 18:26](https://youtu.be/8WbW_n95wc4?t=1106).
- **Subscription value:** "around $2,300 a week of usage" on the $200 plan, "almost 10 grand a month" [SON55 29:32](https://youtu.be/8WbW_n95wc4?t=1772). He now has six Claude accounts and "killed three accounts in the past few days" [SON55 29:32](https://youtu.be/8WbW_n95wc4?t=1772). Compare the Fable video's up to about $8K a month.
- Context window: not stated.
- Haiku 5.5 is coming "in the next few weeks" for "high volume and cost-sensitive applications" [SON55 5:06](https://youtu.be/8WbW_n95wc4?t=306).

## 5. Recommended prompting style and workflow

- **Don't prompt it yourself; have Opus or Fable call it.** "Set Opus up properly to use Sonnet at the right times" and Opus will feel "way faster" and get real work done slightly cheaper [SON55 30:17](https://youtu.be/8WbW_n95wc4?t=1817).
- **Effort:** `high` or `xhigh`; avoid `max` and `low`; medium is "fine-ish" but weaker than on Opus.
- **Give it well-scoped, investigatory tasks with a clear deliverable:** "deep dives into your codebase to find specific behaviors or characteristics", "confirming a hunch" about an API [SON55 30:05](https://youtu.be/8WbW_n95wc4?t=1805), and analysis that helps the orchestrator "plan and scope work" [SON55 24:16](https://youtu.be/8WbW_n95wc4?t=1456).
- **It reads the thread's context faithfully**, so be explicit when changing topic in a long-running Sonnet thread (section 2).

## 6. Subagents, orchestration, delegation and verification

- **Sonnet 5.5 is a subagent / research tool for Opus or Fable orchestrators:** when they want to analyse the codebase before a big task, "they can now call on Sonnet to do that" and be happy with the results; "This is huge" [SON55 24:22](https://youtu.be/8WbW_n95wc4?t=1462).
- **Suitable subagent jobs:** codebase deep dives, behaviour finding, hunch confirmation, scoping and planning research, and "real world documents, office, and all that type of stuff" [SON55 30:54](https://youtu.be/8WbW_n95wc4?t=1854). **Not** front-end building or day-to-day coding.
- **Planning/decomposition bench** (section 2): Astra best plan; Sonnet best value and speed, slightly above Opus; Fable below Opus; Sol fast but weak. Grok 4.7 once beat Fable on an earlier version [SON55 22:33](https://youtu.be/8WbW_n95wc4?t=1353). The judging panel is model-graded, scoring proposals "on various axes" [SON55 23:16](https://youtu.be/8WbW_n95wc4?t=1396).
- **Opus as orchestrator in practice:** Opus 5.5 "has fully unblocked" his TypeScript-compiler-in-Rust (WASM) rewrite after Astra and Sol left "millions of lines" of slop [SON55 25:11](https://youtu.be/8WbW_n95wc4?t=1511); told to clean up the legacy slop, it deleted about 1.6M lines during filming [SON55 26:10](https://youtu.be/8WbW_n95wc4?t=1570), monitored from a separate T3 Code thread [SON55 25:17](https://youtu.be/8WbW_n95wc4?t=1517).
- **Cost caution:** the Opus fish-slop run spawned a Fable 5.1 subagent unintentionally, inflating its cost [SON55 26:32](https://youtu.be/8WbW_n95wc4?t=1592).
- He claims Anthropic now leads in "the best model for calling other models" [SON55 31:17](https://youtu.be/8WbW_n95wc4?t=1877).

## 7. Claude Code specifics

- Model picker: humans should not pick Sonnet in Claude Code; let Opus or Fable delegate to it. Subscription value: about $2,300 a week on the $200 plan.
- No subagent configuration syntax, skills, hooks, MCP or plugins discussed. The recommendation is conceptual: configure Opus to use Sonnet subagents "at the right times".

## 8. Routing-table implications (Sonnet 5.5)

- **Route to Sonnet 5.5 as a subagent** dispatched by an Opus or Fable orchestrator, not as a primary or interactive model.
- **Route to Sonnet:** codebase exploration and deep-dive analysis, architectural comprehension, decomposition research ("how could this giant change be split?"), locating specific behaviours, and verifying hunches about APIs or code. Best cost per point and about 2x faster than Opus on his audit bench.
- **Route to Sonnet:** document, slide and spreadsheet generation, and image or screenshot understanding (claimed strengths, lightly evidenced).
- **Do not route** main implementation or day-to-day coding to Sonnet when Opus is available. Like-for-like it costs about the same or more, because cache reads cost the same $0.20 and it uses about 25% more tokens than Opus on Cursor Bench (272K vs 218K); wall-clock time is also worse. [Update 2026-10-08: cache reads cut to $0.10 at the Haiku 5.5 launch; see § V4.4.]
- **Do not route** front-end or UI design to Sonnet: the weakest of the three Claude models there; use Fable first, then Opus.
- **Effort:** `high` (or `xhigh` for harder analysis). **Never `max`**: the most expensive setting, and on Frontier Code xhigh beat max. **Never `low`**. Treat `medium` as weaker than Opus-medium.
- **Cost model caveat:** Sonnet's per-token discount applies to uncached input, output and cache writes, not cache reads. Long, tool-heavy loops, where cache reads dominate, erode its savings. It is most cost-effective for **short, bounded investigations** (about 5 minutes in his bench), not multi-hour agent loops. [Update 2026-10-08: cache reads cut to $0.10 at the Haiku 5.5 launch; see § V4.4.]
- **For exhaustive code review or a "best possible plan"**, Astra still leads. Use Sonnet when cost and speed of analysis matter more than the last bit of thoroughness.
- **Future slot:** Haiku 5.5 (not yet released) is intended for high-volume, cost-sensitive work. None of the transcripts evaluates Haiku 4.5. [Update 2026-10-08: Haiku 5.5 shipped; see Video 4.]

---

# Video 4: Claude Haiku 5.5

The Code Rabbit sponsor segment (about 2:18 to 3:40) is skipped. Figures marked "official" come from Anthropic's announcement or pricing page (fetched 2026-10-08), not from the video.

## 1. Subject and overall thesis

- Launch-day review of **Claude Haiku 5.5** (API ID `claude-haiku-5-5`), released about 2026-10-07.
- **Before:** "Anthropic has no small models worth using right now"; Haiku 4.5 is "now... just laughable" [H55 0:16](https://youtu.be/38_6C0dkKmU?t=16), his agents were told to avoid it "at all costs" [H55 0:31](https://youtu.be/38_6C0dkKmU?t=31), and Claude called Sol instead to save money [H55 1:53](https://youtu.be/38_6C0dkKmU?t=113).
- **What a small model is for:** "the model the other models use to search for files, to triple check changes" [H55 1:36](https://youtu.be/38_6C0dkKmU?t=96).
- **Verdict:** "The price is right, the performance seems solid" [H55 2:01](https://youtu.be/38_6C0dkKmU?t=121); Anthropic "now has one small model that is sometimes worth using" [H55 40:16](https://youtu.be/38_6C0dkKmU?t=2416).
- **Central claim:** the best uses "aren't clicking it in the UI or selecting it in [Claude] Code", but "letting your agents use it and letting your applications use it" [H55 22:00](https://youtu.be/38_6C0dkKmU?t=1320).
- He would not use it to write code [H55 31:29](https://youtu.be/38_6C0dkKmU?t=1889) (section 3). The same release cut Sonnet 5.5's cache-read price, which "might actually be my favorite thing about this release" [H55 4:44](https://youtu.be/38_6C0dkKmU?t=284).

## 2. Strengths (with evidence)

- **Anthropic positioning** (read from the announcement [H55 3:58](https://youtu.be/38_6C0dkKmU?t=238)): "the cheapest, fastest, and most capable small model we've ever released"; "designed for high volume cost-sensitive tasks" such as "summaries, compactions, database queries, and classification requests"; it "pairs well with Opus and Sonnet as a sub [agent] on coding work" and suits "speed sensitive tasks like live customer support and browser use"; about 75% less money to run than Haiku 4.5 [H55 4:29](https://youtu.be/38_6C0dkKmU?t=269).
- **Benchmarks (Anthropic's numbers, not independently verified):**
  - More than double Haiku 4.5's score "in the vast majority of things" [H55 9:03](https://youtu.be/38_6C0dkKmU?t=543).
  - **Terminal-Bench 4.0:** "from zero to almost 40%" [H55 9:18](https://youtu.be/38_6C0dkKmU?t=558) (official: 39.2% vs 0.0% for Haiku 4.5). GPT-6 Luna scored 16.4%; anyone who "thought Luna was decent at code" earns his "I question your judgment" [H55 9:30](https://youtu.be/38_6C0dkKmU?t=570).
  - **Computer use (OSWorld 2.1):** "it did way better than [GPT-6] Luna" [H55 9:55](https://youtu.be/38_6C0dkKmU?t=595). Official: 72.4% partial credit at max effort (53.3% at medium) vs 48.9% for Luna; strict pass rate 37.1%, vs 48.8% for Sonnet 5.5 and 53.2% for Opus 5.5. He has not tried it ("I've heard good things") [H55 10:09](https://youtu.be/38_6C0dkKmU?t=609). This matters because earlier videos say OpenAI leads computer use.
- **Speed:** "100 to 200 TPS depending on the provider" [H55 10:16](https://youtu.be/38_6C0dkKmU?t=616); about 180 tokens per second in Claude Code on his subscription [H55 11:34](https://youtu.be/38_6C0dkKmU?t=694).
- **Not a token waster** on AA tokens per task, unlike OpenAI's small models [H55 11:58](https://youtu.be/38_6C0dkKmU?t=718). He gives no tokens-per-task figure.
- **Cost vs intelligence** (his Slopalytics dashboard, AA data):
  - With max points hidden it is "cheaper than anything else" [H55 12:46](https://youtu.be/38_6C0dkKmU?t=766) (AA had then published only xhigh and max). At close scores, "Opus was almost five times as expensive" (effort levels not stated) [H55 13:43](https://youtu.be/38_6C0dkKmU?t=823). Haiku xhigh and max are "the best value in that range within Anthropic's line of models" [H55 14:01](https://youtu.be/38_6C0dkKmU?t=841).
  - It dominates other cheap closed models: Gemini 4 Argon and Gemini 3.8 Flash sit to the right and below the Haiku line [H55 15:25](https://youtu.be/38_6C0dkKmU?t=925), and Grok 4.7 is "still below all of this" [H55 15:38](https://youtu.be/38_6C0dkKmU?t=938).
  - With all effort levels published it is "neck and neck with Luna" [H55 39:49](https://youtu.be/38_6C0dkKmU?t=2389), so the small-model gap "no longer feels like a big missing piece" [H55 40:05](https://youtu.be/38_6C0dkKmU?t=2405).
- **Egg-drop demo** (Anthropic's single run [H55 22:17](https://youtu.be/38_6C0dkKmU?t=1337)): Opus 5.5 alone vs Opus 5.5 orchestrating 10 Haiku 5.5 subagents designing a safe egg drop in a physics emulation.

  | Setup | Time | Attempts | Cost |
  |---|---|---|---|
  | Opus 5.5 alone | about 3 min (3 min 37 s on Anthropic's chart) | 25 | $0.47 |
  | Opus 5.5 + 10 Haiku 5.5 subagents | "under a minute" (58 s) | 86 | $0.14 |

  Opus alone runs single-threaded, and multithreaded Opus "would end up wasting way more money" [H55 22:43](https://youtu.be/38_6C0dkKmU?t=1363); the Haiku setup tries more in parallel, costs less and finishes sooner [H55 22:54](https://youtu.be/38_6C0dkKmU?t=1374).
- **Search where most guesses are wrong** (one file among many, when grep can't find it): "way cheaper and faster because it can do a lot of things at once" [H55 23:27](https://youtu.be/38_6C0dkKmU?t=1407).
- **Taste for its size:** a community video demo cost 60 cents and took under 20 minutes [H55 24:52](https://youtu.be/38_6C0dkKmU?t=1492); he credits Anthropic's built-in taste [H55 25:08](https://youtu.be/38_6C0dkKmU?t=1508). With the Claude design skill it was "comically better than [Grok]" on Witchai [H55 25:25](https://youtu.be/38_6C0dkKmU?t=1525) with fewer "cringe fonts" [H55 26:00](https://youtu.be/38_6C0dkKmU?t=1560). For cost-sensitive users, "this is usable. It's not great" [H55 27:08](https://youtu.be/38_6C0dkKmU?t=1628); it might make the $20 Claude sub usable for code (untested) [H55 27:25](https://youtu.be/38_6C0dkKmU?t=1645).
- **Few outright bad decisions in Fish Slop**, "just not making impressive ones" [H55 29:30](https://youtu.be/38_6C0dkKmU?t=1770) (partly retracted, section 3).
- **Single-provider value** [H55 17:48](https://youtu.be/38_6C0dkKmU?t=1068): even if Sol and Luna are usually slightly better per dollar, an Anthropic small model suits an Anthropic spend commitment, a Claude Code-only subscription (no Codex), or possibly better same-family prompting ("I don't know how true that is"). "It's no longer irresponsible to use Haiku" [H55 18:12](https://youtu.be/38_6C0dkKmU?t=1092).

## 3. Weaknesses, pitfalls and misconceptions

- **Misconception: a cheap model makes coding cheap.** Asked whether he would use it for code: "No" [H55 31:29](https://youtu.be/38_6C0dkKmU?t=1889). "Coding is not what makes LLMs expensive": gathering context, verifying, and regenerating after wrong attempts are [H55 31:37](https://youtu.be/38_6C0dkKmU?t=1897).
  - Generating code once the context is cached costs "a few pennies", even on Fable; 500 output tokens on a cached prompt is cheap [H55 32:30](https://youtu.be/38_6C0dkKmU?t=1950).
  - "The code is cheap"; the expense is "all of the prep" before writing and "all the verification after" [H55 32:37](https://youtu.be/38_6C0dkKmU?t=1957).
  - Exception: when you want several versions and "you know if it worked or not trivially", Haiku generating five or eight versions "could be worth it" [H55 33:01](https://youtu.be/38_6C0dkKmU?t=1981).
  - Having Haiku implement a smart model's plan: it may manage parts, but "you already spent the money on the plan" [H55 33:34](https://youtu.be/38_6C0dkKmU?t=2014).
- **Cost inversion when it flails:** if Opus solves a problem in 100k tokens and Haiku burns a million before giving up, Haiku costs more; "Haiku will cost more money as it fails to do it" [H55 36:23](https://youtu.be/38_6C0dkKmU?t=2183).
- **Bad with reasoning off.** ThePrimeagen (secondhand, via a tweet) swapped GPT-6 Luna for Haiku 5.5 with reasoning off and saw a worse pass rate, a much higher fail rate, and slower runs [H55 10:23](https://youtu.be/38_6C0dkKmU?t=623). The speaker: OpenAI trained its models to be good at that and Anthropic trained its models "to be bad at that" [H55 10:47](https://youtu.be/38_6C0dkKmU?t=647). Anthropic removed no-reasoning on Opus (and, he thinks, Sonnet); "you always have to let it reason at least a little bit". Haiku kept the option for quick responses, "but it's not very good at that" [H55 11:00](https://youtu.be/38_6C0dkKmU?t=660).
- **Small models corner themselves** (his Haiku audit of T3 Code's roughly 1,500 open PRs [H55 27:40](https://youtu.be/38_6C0dkKmU?t=1660)). Failure modes to plan for:
  - **Trusts surface signals:** of 40 performance PRs, it called the top ones merge-ready because GitHub checks were green, without auditing them [H55 30:47](https://youtu.be/38_6C0dkKmU?t=1847).
  - **Burns shared rate limits:** parallel fetches used most of a 5,000-requests-per-hour GitHub quota, and the script stored error bodies as data and then failed [H55 33:46](https://youtu.be/38_6C0dkKmU?t=2026) (partly his own load, he says).
  - **Promises waits it cannot keep:** it said it would refetch 181 PRs after the quota reset, but scheduled no wake-up, so the thread simply stopped [H55 34:26](https://youtu.be/38_6C0dkKmU?t=2066).
  - **Harms the human's tools:** small models make things "harder for not just themselves, but for me" [H55 34:48](https://youtu.be/38_6C0dkKmU?t=2088); he lost T3 Code's GitHub integration "for at least the next 50 minutes" [H55 34:56](https://youtu.be/38_6C0dkKmU?t=2096).
- **Fish Slop 3D build is weak** [H55 28:23](https://youtu.be/38_6C0dkKmU?t=1703): no mouse look, no sound, broken corner geometry, a too-early second alien attack, "not honoring the original source" [H55 29:51](https://youtu.be/38_6C0dkKmU?t=1791). "Roughly the same tier as the [Grok] version, which was offensively bad" [H55 28:49](https://youtu.be/38_6C0dkKmU?t=1729), minus Grok's outright wrong decisions; vs GPT-6 Astra, "its lows aren't as low... but its highs are a tenth as high" [H55 29:56](https://youtu.be/38_6C0dkKmU?t=1796).
- **Front end needs the design skill:** without it, "we're back into classic [LLM] design" [H55 26:15](https://youtu.be/38_6C0dkKmU?t=1575); even with it, several designs were "not my favorite".
- **The 100K price cliff:** above 100K input tokens every price rises 5x (section 4), "very small especially for like longunning agentic work" [H55 6:58](https://youtu.be/38_6C0dkKmU?t=418). Claude Code sessions cross it quickly: 47 of 51 Fish Slop requests did [H55 30:26](https://youtu.be/38_6C0dkKmU?t=1826).
- **It barely pushes the Pareto line:** "I do wish this model pushed the [Pareto] line a bit more" [H55 19:00](https://youtu.be/38_6C0dkKmU?t=1140).
  - "Haiku is slightly smarter for meaningfully more money" than Luna [H55 16:44](https://youtu.be/38_6C0dkKmU?t=1004); Luna "is cheaper than Haiku always. It's also dumber always" [H55 16:00](https://youtu.be/38_6C0dkKmU?t=960).
  - With GPT-6.1 Sol added, "going from 21.3 cents to 21.4 cents you get a huge jump in intelligence" [H55 16:52](https://youtu.be/38_6C0dkKmU?t=1012): a Haiku point and a Sol point at almost the same cost per task, Sol much smarter (the transcript does not name each point). "If we were to turn Haiku off here oh that's a much smoother line."
  - Sol "on low is as cheap as [Haiku] on low", thanks to token efficiency [H55 12:58](https://youtu.be/38_6C0dkKmU?t=778).
  - AA's own chart "is a bit more brutal showing it is not on the Pareto line" [H55 21:37](https://youtu.be/38_6C0dkKmU?t=1297).
- **Max effort** is "still pretty cheap, but more than I would want it to be" [H55 12:51](https://youtu.be/38_6C0dkKmU?t=771).

## 4. Pricing, speed, context and limits

- **Price.** He reads 1 cent per million cache reads, 12.5 cents cache writes, 10 cents input, 50 cents output [H55 6:07](https://youtu.be/38_6C0dkKmU?t=367). The official pricing page (fetched 2026-10-08) matches, in USD per million tokens:

  | Model | Input | Output | Cache read | 5m cache write | 1h cache write | Batch in / out |
  |---|---|---|---|---|---|---|
  | Haiku 5.5, prompt ≤ 100K tokens | 0.10 | 0.50 | 0.01 | 0.125 | 0.20 | 0.05 / 0.25 |
  | Haiku 5.5, prompt > 100K tokens | 0.50 | 2.50 | 0.05 | 0.625 | 1.00 | 0.25 / 1.25 |
  | Haiku 4.5 (for comparison) | 1 | 5 | 0.10 | 1.25 | 2 | 0.50 / 2.50 |
  | Sonnet 5.5 (after the cut) | 2 | 10 | 0.10 | 2.50 | 4 | 1 / 5 |
  | Opus 5.5 (unchanged) | 4 | 20 | 0.20 | 5 | 8 | 2 / 10 |

  - Against Sonnet 5.5: "20x cheaper in output tokens and input tokens", about 20x on cache writes, and cache reads "a tenth the price" [H55 6:23](https://youtu.be/38_6C0dkKmU?t=383).
  - Haiku 4.5 had the same cache-read price as the new Sonnet 5.5 price and half of Sonnet's other prices [H55 5:58](https://youtu.be/38_6C0dkKmU?t=358).
- **The 100K rule:** "If you go over 100k tokens, the price doesn't double. It 5x's" [H55 7:04](https://youtu.be/38_6C0dkKmU?t=424). Official: prompt length counts all input tokens, including cache reads and writes; each request is priced on its own, and one over the threshold pays the higher prices even when part of it is a cache hit. Haiku 5.5 is the only current Anthropic model excluded from flat 1M-context pricing. Anthropic used to double prices past roughly 200K to 270K and "stopped doing that somewhat recently" [H55 6:40](https://youtu.be/38_6C0dkKmU?t=400).
- **His reading of the two tiers** [H55 7:21](https://youtu.be/38_6C0dkKmU?t=441): big contexts need more RAM; the sub-100K tier is probably "eating some of their own margin" to make quick reads and categorisation "as absurdly cheap as possible" against OpenAI's cheap model ("Jev"), while the upper tier keeps Claude Code use from bankrupting Anthropic. Above 100K it is "still half the price [it] was before", i.e. half of Haiku 4.5.
- **Sonnet 5.5 cache-read cut** [H55 4:36](https://youtu.be/38_6C0dkKmU?t=276): halved, "from 20 cents per million [cache] reads to 10 cents", the same as GPT-6.1 Sol.
  - Why it matters to Video 3's critique (§ V3.3): cache reads were "about 30 to 50% of your bill" and cost the same on Sonnet and Opus, so the two were barely different in price for agentic work [H55 5:08](https://youtu.be/38_6C0dkKmU?t=308). "A huge change" that "makes the whole lineup make way more sense" [H55 4:44](https://youtu.be/38_6C0dkKmU?t=284).
  - After AA repriced: Sonnet shifted left on the Pareto chart, "actually not that much more" compelling, but it "feels less bad now by quite a bit" [H55 19:14](https://youtu.be/38_6C0dkKmU?t=1154).
  - Official footnote: cache hits and refreshes on Opus 5.5 and Sonnet 5.5 cost 0.05x the base input price, i.e. $0.10 on Sonnet 5.5 and $0.20 on Opus 5.5. Sonnet's cache reads are now half of Opus's, like its other prices. Its higher token use (§ V3.3) is unchanged.
- **AA cost points:**
  - Sonnet 5.5 at max did "almost 200,000 tokens per task", "2.5 times" Fable 5.1's 78K, at a cost "slightly higher than Fable 51" [H55 12:05](https://youtu.be/38_6C0dkKmU?t=725).
  - Sonnet xhigh is "a fine value at 2.75 per task"; Sonnet max "makes literally no sense at $[7.86] per task" [H55 15:01](https://youtu.be/38_6C0dkKmU?t=901). Video 3 gave $7.60; these are probably pre-cut prices.
  - The price gap between Opus 5.5 low and Haiku 5.5 max "is not as big as you would think": "20 cents to 55", "around 2x more money for Opus" [H55 36:56](https://youtu.be/38_6C0dkKmU?t=2216). That is Haiku 5.5 at max about $0.21 per AA task vs Opus 5.5 at low about $0.55 (checked 2026-10-08; "Opus 5" in the captions is Opus 5.5, and the spoken order is easy to misread). Haiku at its most expensive setting costs well under half of Opus at its cheapest.
- **Speed:** 100 to 200 tok/s depending on provider; about 180 tok/s in Claude Code on his subscription.
- **Fish Slop cost breakdown** [H55 30:11](https://youtu.be/38_6C0dkKmU?t=1811): about $1 total. 9.73 million cache-read tokens; many 1-hour cache writes "because it always writes 1 hour, which is annoying"; uncached input "only 102 tokens"; output about 30 cents; "47 [of] 51 requests exceeded 100k input tokens" and paid the higher tier. Capping the context would have made the game "much worse" but "way cheaper" [H55 30:35](https://youtu.be/38_6C0dkKmU?t=1835).
- **Context and output (official, not in the video):** 1M context, 128K max output. The practical cheap window is 100K.
- **Effort and thinking (official, not in the video):** low, medium, high, xhigh and max; default `medium`. Adaptive thinking is on by default. Thinking can be disabled only at `high` or below; `budget_tokens` is rejected. The newer tokenizer produces about 30% more tokens than Haiku 4.5 for the same text.
- **Subscription API credit (reported, unverified).** He says the launch notes give 20x subscribers "$200 in API credit every month" and 5x subscribers "$100", effectively a preloaded API key [H55 20:12](https://youtu.be/38_6C0dkKmU?t=1212), for building apps with Haiku or Sonnet built in. He was relieved that subscriptions still work in tools like T3 Code [H55 19:48](https://youtu.be/38_6C0dkKmU?t=1188). A secondary source (the-decoder) describes the same amounts as a credit for programmatic use (Agent SDK, `claude -p`, Claude Code GitHub Actions, third-party apps signed in with the subscription), billed at API rates and dated to 2026-06-15. Check the account before relying on it.
- **SDKs:** the Anthropic Python and TypeScript SDKs gain computer-use and browser-use support [H55 21:12](https://youtu.be/38_6C0dkKmU?t=1272).

## 5. Recommended prompting style and workflow

- **Let the orchestrator pick it:** he trusts Opus to pick it "at the times where it makes sense" [H55 39:15](https://youtu.be/38_6C0dkKmU?t=2355). On the $200 tier he "would rather just use Opus" himself [H55 36:15](https://youtu.be/38_6C0dkKmU?t=2175).
- **Keep reasoning on** [H55 11:00](https://youtu.be/38_6C0dkKmU?t=660). For reasoning-off categorisation, "just use Jev unless you need like vision", then Haiku or Luna, "probably Luna cuz it's cheaper" [H55 11:08](https://youtu.be/38_6C0dkKmU?t=668).
- **Give it breadth, not depth:** vetting four things to confirm a theory, comparing against eight external projects, or reading a pile of documentation to establish facts; "that is when haiku is incredible" [H55 33:16](https://youtu.be/38_6C0dkKmU?t=1996).
- **Many cheap attempts plus a verifier:** for "the subset of tasks where more attempts is more valuable than smart attempts", where you would rather try 10 times and verify each, and a dumb try is not far from a smart one, "Haiku 55 is going to slaughter. This is a small subset of work" [H55 23:34](https://youtu.be/38_6C0dkKmU?t=1414).
- **His orchestrator prompt** [H55 35:13](https://youtu.be/38_6C0dkKmU?t=2113): the same audit prompt, run on Opus instead of Haiku, asking for "lots of sub [agents] and workflows", "Haiku 55 for all sub [agents]", and to "minimize work that you do yourself" beyond gathering data and orchestrating.
- **Hand findings to a smart model to land:** for a PR the Haiku audit flagged, he asks Opus to check whether it is worth landing, fix what needs fixing, and merge "if you're confident it's ready to go. Full send" [H55 31:04](https://youtu.be/38_6C0dkKmU?t=1864).
- **Load the Claude design skill** for front-end work; he had uninstalled it and will "bring it back" [H55 26:24](https://youtu.be/38_6C0dkKmU?t=1584).
- **Cap context when cost matters more than quality:** keep Haiku prompts under 100K, for example with the autocompact setting in section 7 (unverified).
- **Guard API-heavy scripts** (our inference from the PR-audit failure, not a stated tip): when Haiku drives scripts against rate-limited APIs, cap concurrency, have the script reject error bodies, and confirm a real scheduled wake-up instead of trusting "I'll wait".

## 6. Subagents, orchestration, delegation and verification

- **Core pattern: Opus orchestrates, Haiku gathers:** when Opus needs to collect data, read through large volumes or categorise, Haiku is "an incredible addition to my portfolio of models" [H55 39:08](https://youtu.be/38_6C0dkKmU?t=2348).
- **In applications:** Haiku audits and categorises incoming data, or Sonnet/Opus call Haiku to test things and explore the codebase [H55 22:10](https://youtu.be/38_6C0dkKmU?t=1330).
- **Parallel attempts beat one careful serial attempt** when checking a result is cheap. The egg-drop demo (section 2) shows 3.4x the attempts at about 30% of the cost in about a quarter of the time, with the simulator as an objective pass/fail.
- **His CLAUDE.md change:** stop forcing every subagent to be Opus or Sol, "because this is cheap enough that it would make real sense" [H55 24:06](https://youtu.be/38_6C0dkKmU?t=1446). He hopes Opus knows which subset of work fits and has not tested it hard yet [H55 23:58](https://youtu.be/38_6C0dkKmU?t=1438).
- **Opus re-run of the PR audit** [H55 35:42](https://youtu.be/38_6C0dkKmU?t=2142): Opus planned about 15 PRs per Haiku agent across 1495 open PRs, roughly 100 agents, beyond typical workflow guidelines but as asked; he called it "actually being thoughtful" and expected it to avoid or work around his rate limits [H55 35:27](https://youtu.be/38_6C0dkKmU?t=2127). The result was never shown [H55 39:31](https://youtu.be/38_6C0dkKmU?t=2371).
- **Verification stays with smart models.** Haiku's audit treated green GitHub checks as proof of readiness; Opus then vets, fixes and merges.
- **His duo: Opus plus GPT-6.1 Sol.** "I personally am sticking to my Opus and [Sol] duo" [H55 39:08](https://youtu.be/38_6C0dkKmU?t=2348). Opus codes, and his agents consult Sol before opening a PR because "[Sol] catches all the dumb things opus might miss" [H55 38:50](https://youtu.be/38_6C0dkKmU?t=2330); "I love [6.1 Sol] as an auditor" [H55 38:42](https://youtu.be/38_6C0dkKmU?t=2322).
  - Sol is not the middle tier between Haiku and Opus despite its chart position: think of it "as a different family with similar intelligence" [H55 38:02](https://youtu.be/38_6C0dkKmU?t=2282), like asking "your friend who works at a different company" [H55 38:33](https://youtu.be/38_6C0dkKmU?t=2313).
  - Haiku's role in the duo is the cheap gatherer under Opus.
- **Same-family prompting:** he repeats a claim that Opus prompts Haiku better than Sol, adding "I don't know how true that is" [H55 18:04](https://youtu.be/38_6C0dkKmU?t=1084).

## 7. Claude Code specifics

- **Model picker:** do not select Haiku interactively; let Opus delegate to it [H55 22:00](https://youtu.be/38_6C0dkKmU?t=1320) [H55 36:15](https://youtu.be/38_6C0dkKmU?t=2175). Drop CLAUDE.md rules forcing every subagent to be Opus or Sol [H55 24:06](https://youtu.be/38_6C0dkKmU?t=1446); reinstall the design skill for front end [H55 26:24](https://youtu.be/38_6C0dkKmU?t=1584).
- **Autocompact at 100K (unverified).** He relays that Anthropic employees ("Lydia", name uncertain) suggest setting Haiku 5.5's autocompact window to 100K to stay in the cheap tier, apparently saved per model and so applying to Haiku subagents too [H55 8:31](https://youtu.be/38_6C0dkKmU?t=511), useful on API billing or Bedrock. Not verified: Claude Code's `/autocompact` sets an auto-compact window between 100K and 1M, but per-model persistence and coverage of subagents are not confirmed.
- **Cache writes are always 1-hour in Claude Code** ("which is annoying") [H55 30:20](https://youtu.be/38_6C0dkKmU?t=1820). On Haiku's ≤100K tier that is $0.20/M instead of $0.125/M for a 5-minute write.
- **Subscription credit:** if the reported credit applies to `claude -p` (section 4), programmatic runs such as this repo's claude-cli bridge may bill against it at API rates rather than plan limits. Unverified.
- **Long waits:** in T3 Code, Haiku said it would wait for a rate limit to reset but "didn't trigger a wait" [H55 34:34](https://youtu.be/38_6C0dkKmU?t=2074); the thread stalled until he intervened.
- Throughput about 180 tok/s on his subscription; the "$20 Claude sub might be usable for code" idea is untested [H55 27:25](https://youtu.be/38_6C0dkKmU?t=1645). Hooks, MCP and plugins: not discussed.

## 8. Routing-table implications (Haiku 5.5)

- **Route to Haiku 5.5 as a subagent**, dispatched by Opus (or Sonnet), not as a primary or interactive model when Opus is available.
- **Route to Haiku:** codebase search where grep is not enough, data collection, reading large volumes of documentation or logs, surveying external projects, vetting several hypotheses in parallel, categorisation and triage, summaries and compaction.
- **Route to Haiku for many-attempts work** with a cheap, objective verifier (tests, a simulator, a script). The egg-drop demo is the evidence, from a single vendor run.
- **Do not route** implementation, code review, merge decisions or PR-readiness audits to Haiku. It trusted green CI as proof of readiness. Execution and verification stay with Opus, with Sol as the cross-family auditor.
- **Do not route** unattended long loops or API-heavy scripts against external rate limits to Haiku without guards. It cornered itself, broke the human's GitHub integration for about 50 minutes, and stalled.
- **Do not route** tasks Opus would finish in far fewer tokens. A flailing Haiku can cost more than Opus.
- **Never turn reasoning off.** For reasoning-off classification, prefer OpenAI's cheap model or GPT-6 Luna unless vision is needed.
- **Keep Haiku requests under 100K input tokens.** Above that every token costs 5x. Short subagent tasks with fresh context fit; long Claude Code sessions do not (47 of 51 Fish Slop requests crossed it). The autocompact cap may help (unverified).
- **Effort:** official default `medium`. His AA chart shows xhigh and max as the best value in Anthropic's lineup and still cheap in absolute terms. That is one aggregate benchmark, so the cross-video "never `max`" rule should stand for Haiku until tested on your own tasks.
- **Cross-vendor:** if OpenAI models are allowed, the best value per dollar on AA is GPT-6 Luna, then GPT-6.1 Sol, then Opus 5.5. Haiku 5.5 is "neck and neck" with Luna but slightly worse per dollar. Haiku's case is a single-provider setup: an Anthropic spend commitment, a Claude Code-only subscription, or (unverified) better Opus-to-Haiku prompting.
- **Anthropic-only lineup:** the Pareto line is now "all of Haiku for the cheap and most of Opus for the less cheap" [H55 37:22](https://youtu.be/38_6C0dkKmU?t=2242). Sonnet "offers nothing now. Maybe just barely on high" [H55 37:37](https://youtu.be/38_6C0dkKmU?t=2257); "I think you can avoid Sonnet entirely and just use Opus and [Haiku]" [H55 37:45](https://youtu.be/38_6C0dkKmU?t=2265). This weakens Video 3's case for Sonnet as the analysis subagent, which rested on one deep-audit bench; the cache-read cut helps Sonnet, but on AA it is still barely on the line.
- **Computer use and browser use:** Anthropic's OSWorld numbers make Haiku a cheap candidate, but the speaker has not tested it. Keep the existing computer-use route until it is tested.
- **Front end:** only for cost-sensitive work, and only with the design skill loaded: "usable... not great".

---
# Cross-video synthesis (for the routing table)

| Dimension | Fable 5.1 | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|---|---|
| Price in / out / cache read / cache write ($/M) | 10 / 50 / 0.25 / not stated | 4 / 20 / 0.20 / 5 | 2 / 10 / 0.10 (cut from 0.20 at the Haiku 5.5 launch) / 2.50 | 0.10 / 0.50 / 0.01 / 0.125 at ≤100K prompt tokens; 5x (0.50 / 2.50 / 0.05 / 0.625) above 100K |
| Speaker's role for it | Hardest long-horizon work, PR takeovers, orchestration, front-end design | **Default daily driver**; ZDR-compliant | **Subagent for analysis / research**; not human-selected | **Subagent and app component** for search, data gathering, categorisation and many cheap attempts; not human-selected; not for writing code |
| Effort guidance | Default `high`; `low` often fine; little gain beyond `high` | `medium` (default) / `high` / `xhigh`; avoid `low` and `max` | `high` / `xhigh`; avoid `low` and `max`; `medium` weaker than Opus's | Never turn reasoning off; xhigh and max are Anthropic's best value on his AA chart (untested hands-on); official default `medium` |
| Token efficiency | Poor vs OpenAI; 1.7x Fable 5 output | Poor: about 120K tokens per AA task at max (vs Astra 27K) | Worst: 272K tokens per Cursor Bench task | "Not the usual wasteful" small model on AA (no figure); Fish Slop used 9.73M cache-read tokens for about $1 |
| Front-end taste | Best (with design skill) | OK and steerable; design skill doesn't help | Weak | "Usable... not great" with the design skill; "classic LLM design" without |
| Exhaustive review / audit | Better than Opus, below Astra | Below Fable, Astra, Sol, Grok 4.7 | Slightly above Opus on his decomposition bench, at half the cost | Weak: called PRs merge-ready because GitHub checks were green |
| Known quirks | Few progress updates; dense prose; asks permission; scope creep (nearby fixes, extra tests); safeguard fallback to Opus | Context-window anxiety; dumb spikes; repair loops; slow to commit; runaway at `max` | Faster TPS but slower wall-clock; cache-read pricing makes it no cheaper for long agentic loops [Update 2026-10-08: cache reads cut to $0.10; see § V4.4.] | Bad with reasoning off; corners itself (rate limits, stalled thread); 100K price cliff; can cost more than Opus when it flails |
| Data retention | No ZDR (Enterprise Frontier Safeguards option) | ZDR available | Not discussed | Not discussed |

Points stated across videos:

- **Never use `max`** on any of these models. In both later videos it is shown to raise the reasoning *floor*, causing more than 10x token blowups and loops, sometimes with worse scores. Video 4 is a partial exception: Haiku 5.5 max is still cheap per AA task and sits on Anthropic's value line, but he still calls Sonnet max senseless. Keep the rule until Haiku max is tested on your own tasks.
- **Never turn reasoning off** on Anthropic models. Video 4 extends the "avoid `low`" advice: Haiku 5.5 with reasoning off did worse than GPT-6 Luna with reasoning off (ThePrimeagen's result, secondhand).
- Cache-read pricing, not headline input/output price, decides cost in agentic loops. Video 4 adds the Haiku 5.5 100K tier: above 100K prompt tokens every Haiku price rises 5x, cache reads included.
- **Anthropic-only stack:** after Video 4 he says "you can avoid Sonnet entirely and just use Opus and [Haiku]", with Haiku as the cheap subagent tier. Across vendors his value line is GPT-6 Luna, GPT-6.1 Sol, Opus 5.5, and his working duo is Opus plus Sol as auditor.
- Computer use is better routed to OpenAI (Astra). Anthropic models lag there per the speaker, though Sonnet and Opus are now "neck and neck" on OS World. Anthropic's OSWorld numbers put Haiku 5.5 well above GPT-6 Luna, but he has not tried it.
- The best exhaustive planner/reviewer in his tests is GPT-6 Astra: "most thorough" but "spiky and weird".
