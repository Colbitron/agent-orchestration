---
id: gemini-3-8-flash
name: Gemini 3.8 Flash
vendor: google
family: gemini
status: current
released: 2026-09                # GA 2026-09-02
as_of: 2026-10-19
confidence: medium               # ID, price, limits from Google docs; benchmarks vendor-run; Theo's remarks are dismissive asides

api_ids: [gemini-3.8-flash]
access:
  subscriptions: [google-ai-pro, google-ai-ultra]   # plus a free Gemini CLI OAuth tier (60 req/min, 1,000/day)
  api: true
  harnesses: [gemini-cli, cursor, opencode, openclaw, hermes]
  invoke_via: [gemini-cli, agy-cli, openclaw-cli, hermes-cli]   # openclaw, hermes / openclaw-cli, hermes-cli added 2026-10-19: Google provider with GEMINI_API_KEY; availability of this model there unverified

pricing_per_mtok:
  input: 0.75                    # introductory until 2026-12-31; 1.50 from 2027-01-01
  output: 3.75                   # introductory; 7.50 from 2027-01-01
  cache_read: 0.075              # introductory; 0.15 from 2027-01-01
  cache_write: null              # cache storage billed at $0.50 per MTok per hour instead
context_window: 1048576          # max output 65,536
notes_on_cost: >
  About 5x cheaper than Opus 5.5 per token at the introductory price, which ends
  2026-12-31; then the price doubles. Cached input is a 90% discount but still
  about 25x DeepSeek V4.1 Flash's cache-read price, and cache storage is billed
  per hour. It uses about 30% more output tokens per task than 3.7 Flash
  (unverified) and took more turns than DeepSeek V4.1 Flash in one hands-on test.
  AA cost per task is unverified. A free API tier and free Gemini CLI quota exist.

effort:
  levels: [low, medium, high]    # "thinking levels"; minimal is not supported
  default: high
  avoid: []
  notes: >
    high for agentic coding, low for bulk transforms (Google's guidance as
    summarised in research). No kit-specific evidence.

scores:
  intelligence: 4
  taste: 3
  floor: 3
  thoroughness: 3
  cost_efficiency: 6
  speed: 9
  computer_use: 3
  orchestration: 2

tasks:
  quick-fix:      {fit: ok,      note: "Theo: on a narrow ticket 'even a Gemini model' clears the bar; review before merge."}
  feature:        {fit: poor,    note: "Low floor ('read the same file 26 times'); collapses on hard agent tasks (Terminal-bench 4.0: 19.1% vs Opus 5's 51.8%)."}
  long-run:       {fit: poor,    note: "Research: avoid for long unattended builds and multi-hour refactors."}
  frontend:       {fit: poor,    note: "No evidence of taste; Theo: 'no one should be using a Gemini thing'."}
  review:         {fit: poor,    note: "No evidence; use Sol, Astra or Grok 4.7 for a cross-family review."}
  investigate:    {fit: poor,    note: "Re-reads files and loses long multi-step tasks; poor root-causer."}
  analyze:        {fit: ok,      note: "Fast first-pass summaries of large codebases (1M context); verify with a stronger model."}
  bulk:           {fit: good,    note: "Codemods, renames, test scaffolding, lint fixes, log and file summarisation, at about 305 tok/s. Verify programmatically; no single output over 64K tokens."}
  research:       {fit: good,    note: "Reads screenshots, PDFs and video; Gemini CLI has Google Search grounding and a research subagent. Low-stakes summaries only."}
  computer-use:   {fit: poor,    note: "Computer use is preview; OSWorld-2.0 59.0% vs Opus 5's 75.4% (vendor)."}
  copy:           {fit: unknown, note: "No evidence."}
  3d-games:       {fit: unknown, note: "No evidence."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: poor,    note: "Must-land loop; low floor."}
  orchestrate:    {fit: poor,    note: "Not a lead model."}

role_hints:
  as_primary: "Not a primary model."
  as_subagent: "Fast, cheap fan-out worker for bulk mechanical work, log and document reading, and multimodal input (screenshots, PDFs, video), with output verified programmatically."
  never_for: ["anything that must land without review", "long unattended runs", "frontend or UI", "single responses longer than 64K tokens", "computer use", "leading other agents"]
---

## Summary

Gemini 3.8 Flash is Google's best generally available coding model and the
fastest model Artificial Analysis has measured (about 305 tok/s), at AA index 41
and an introductory price about 5x below Opus 5.5. In this kit it is a fast bulk
worker: mechanical edits, log and file summarisation, reading screenshots, PDFs
and video, and cheap fan-out. It collapses on hard long-horizon agent tasks and
has a 64K output cap. This profile comes from vendor docs and aggregators, not
hands-on testing; test it on your own tasks before trusting it. Theo's few
remarks on it are dismissive ("meme tier").

## Strengths

- **Speed.** About 305 output tok/s, the fastest AA has measured (per Vellum's
  citation of AA; single source) (`research/model-gaps.md § 2a. Gemini 3.8
  Flash`).
- **Price.** $0.75 / $0.075 / $3.75 per MTok until 2026-12-31; batch half price;
  free API tier (same section).
- **Short-to-medium terminal coding (vendor-run).** Terminal-bench 2.1 89.4% (Opus
  5: 89.1%), DeepSWE v1.1 73.7% (Opus 5: 74.0%), SWE-Bench Pro 61.6%. Theo's Astra
  video also cites 73.8% on DeepSWE ([ASTRA 20:38](https://youtu.be/XFWpf0wLbh0?t=1238)).
- **Multimodal input.** Text, image, video, audio and PDF; good at chart reading.
- **Token-lean on one bench.** Cursor Bench: 162K tokens per task vs 218K for
  Opus 5.5 and 272K for Sonnet 5.5 ([SON55 17:41](https://youtu.be/8WbW_n95wc4?t=1061)).
- **Harness.** Gemini CLI is scriptable (`gemini -p ... -m gemini-3.8-flash
  --output-format json`), has subagents (codebase investigator, browser,
  research), plan mode, MCP and Google Search grounding.

## Weaknesses and failure modes

- **Collapses on hard agent tasks.** Terminal-bench 4.0: 19.1% vs 51.8% for Opus
  5. GDPVal-AA v2: 1545 vs 1824 Elo. "Avoid ... anything resembling
  Terminal-bench 4.0" (`research/model-gaps.md § 2a`).
- **Low floor (Theo).** "It'll read the same file 26 times before making a
  change ... But sometimes it can name skateboard tricks really well." A spike
  in his diagram is "why Flash had those couple of good benchmarks that made it
  look really good when it wasn't." "No one should be using a Gemini thing"
  ([MODELS 5:18](https://youtu.be/iBrAWpjXNxs?t=318); [MODELS 7:00](https://youtu.be/iBrAWpjXNxs?t=420); [MODELS 7:09](https://youtu.be/iBrAWpjXNxs?t=429)). "Meme tier"
  ([FVA 49:27](https://youtu.be/P7bxbDSnZRM?t=2967)). These are asides, not tests.
- **64K output cap.** Smaller than Claude/GPT (128K) and DeepSeek (384K); it
  cannot regenerate a large file in one response.
- **More turns.** In a DataCamp hands-on test it took 4 turns where DeepSeek V4.1
  Flash took 2 (single source).
- **Price doubles on 2027-01-01** to $1.50 / $0.15 / $7.50.
- **Computer use is preview** and well behind (OSWorld-2.0 59.0% vs 75.4%).
- **Gemini CLI auto-routing.** The CLI's default routes between Flash and Pro by
  task complexity; pin `-m gemini-3.8-flash` so the routing table controls the
  model.

## How to prompt it

No hands-on evidence. Inferred from the failure modes:

- Name the exact files and the exact change; don't let it explore. Re-reading
  loops are the known failure.
- Keep each task short and single-step. Split anything that looks like a
  multi-phase agent task.
- Ask for diffs or patches, not whole regenerated files, to stay under 64K
  output.
- Use thinking level `high` for code edits, `low` for pure transforms and
  summaries.
- Run headless: `gemini -p "<task>" -m gemini-3.8-flash --output-format json
  --approval-mode auto_edit`. Exit code 53 means it hit the turn limit; treat
  that as failure and escalate, not retry.
- Feed it screenshots, PDFs and video directly when the task is reading them.

## Routing guidance

Route here for:
- Bulk mechanical work: codemods, renames, test scaffolding, lint fixes.
- Log and file summarisation; large-document reading (1M context).
- Multimodal reading: screenshots, PDFs, charts, video.
- Fast, cheap fan-out subagents where many short tasks matter more than depth
  and the output is verified programmatically.

Do not route here for:
- Long unattended builds, multi-hour refactors, wide features.
- Review, investigation, planning, frontend, computer use.
- Any response that must exceed 64K tokens.

Handoff patterns:
- **Flash reads, frontier decides.** Flash digests logs, PDFs or screenshots and
  hands a summary to Opus, Sol or Fable.
- **Flash drafts mechanical edits, tests judge.** Failures go to 6.1 Sol or Opus,
  not back to Flash.
- **Pick among cheap tiers by pattern** (`research/model-gaps.md § Suggested
  routing-table shortlist`): Flash for raw speed and multimodal input; DeepSeek
  V4.1 Flash for repeated passes over a cached repo and long outputs; Luna for
  lowest measured cost per task.
- **Gemini 4 Argon is not this model.** Announced 2026-09-30 in restricted
  access; profile it separately when it is generally available.

## When this beats the frontier

- Latency-bound bulk work: about 3–4x faster than Opus 5.5 on output speed.
- Reading multimodal inputs (screenshots, PDFs, video) in volume.
- Free-tier or Google AI Pro/Ultra quota that would otherwise go unused.

## Cost notes

- Introductory $0.75 / $0.075 / $3.75 per MTok until 2026-12-31; then $1.50 /
  $0.15 / $7.50. Batch half price; priority $1.35 / $6.75. Cache storage $0.50
  per MTok per hour. Re-score `cost_efficiency` after 2027-01-01.
- Cache reads are about 25x DeepSeek V4.1 Flash's, so DeepSeek wins on repeated
  passes over the same large context.
- Gemini CLI's free OAuth tier (60 requests/min, 1,000/day) and Pro/Ultra quotas
  can make it effectively free for light bulk use.
- Uses about 30% more output tokens than 3.7 Flash at high (unverified).

## Evidence

- `research/model-gaps.md § Naming corrections` (3.8 Flash is the best GA Gemini;
  3.5 Pro never shipped; 3.1 Pro still preview and below 3.8 Flash; Gemini 4
  Argon restricted), `§ At-a-glance comparison`, `§ 2a. Gemini 3.8 Flash`, and
  `§ Suggested routing-table shortlist`.
- [MODELS 5:18](https://youtu.be/iBrAWpjXNxs?t=318) and [FVA 49:27](https://youtu.be/P7bxbDSnZRM?t=2967),
  [MODELS 7:09](https://youtu.be/iBrAWpjXNxs?t=429) (Theo's low-floor remarks).
- [SON55 17:41](https://youtu.be/8WbW_n95wc4?t=1061) (Cursor Bench 162K tokens per task).
- [ASTRA 20:38](https://youtu.be/XFWpf0wLbh0?t=1238) (DeepSWE
  73.8%).
- URLs: [Gemini models](https://ai.google.dev/gemini-api/docs/models),
  [gemini-3.8-flash model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash),
  [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing),
  [Google blog: 3.8 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/),
  [Vellum benchmarks](https://www.vellum.ai/blog/gemini-3-8-flash-benchmarks-explained),
  [DataCamp: DeepSeek V4.1 Flash vs Gemini 3.8 Flash](https://www.datacamp.com/blog/deepseek-v4-1-flash-vs-gemini-3-8-flash),
  [AA leaderboard](https://artificialanalysis.ai/leaderboards/models),
  [Gemini CLI](https://github.com/google-gemini/gemini-cli),
  [headless docs](https://geminicli.com/docs/cli/headless/),
  [3.8 Flash default PR](https://github.com/google-gemini/gemini-cli/pull/29172),
  [eesel subscription prices](https://www.eesel.ai/blog/gemini-pricing).
- **Unverified:** 305 tok/s (Vellum citing AA); +30% output tokens vs 3.7 Flash
  (Emergent via Vellum); AA cost per task (not found); the DataCamp turn count
  (one task); all benchmark numbers except AA's index are vendor-run.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 4 | AA 41 vs 54 for Opus 5.5; matches Opus 5 on short terminal benches but 19.1% vs 51.8% on Terminal-bench 4.0. |
| taste | 3 | No evidence of design or copy quality; Theo dismisses Gemini for real work. |
| floor | 3 | Theo's canonical low-floor example ("read the same file 26 times"); spiky benchmark wins. |
| thoroughness | 3 | No review evidence; re-reading is not the same as digging. |
| cost_efficiency | 6 | Cheap at introductory prices and token-lean on Cursor Bench, but takes more turns than DeepSeek, cache reads cost more, AA $/task unknown, and the price doubles in January. |
| speed | 9 | About 305 tok/s, fastest measured; held below 10 because extra turns eat wall-clock. |
| computer_use | 3 | Preview only; OSWorld-2.0 59.0% vs Opus 5's 75.4% (Opus 5.5 scores 4). |
| orchestration | 2 | No evidence; Gemini CLI's subagents are the harness, not the model. |
