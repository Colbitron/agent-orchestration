---
id: deepseek-v4-1-flash
name: DeepSeek V4.1 Flash
vendor: deepseek
family: open-weights
status: current
released: 2026-09                # 2026-09-10
as_of: 2026-10-19
confidence: medium               # price and limits from DeepSeek docs; benchmarks mostly vendor; one hands-on comparison

api_ids: [deepseek-flash]        # legacy deepseek-v4-flash is deprecated and routes here; OpenRouter/OpenCode model strings unverified
access:
  subscriptions: []
  api: true                      # OpenAI- and Anthropic-compatible endpoints; $5 minimum prepaid balance
  harnesses: [opencode, pi, cursor, openclaw, hermes]
  invoke_via: [openrouter-api, opencode-cli, openclaw-cli, hermes-cli]   # no ollama: 552B total parameters does not fit on typical local hardware; openclaw, hermes / openclaw-cli, hermes-cli added 2026-10-19: via each runtime's OpenRouter provider; model strings unverified

pricing_per_mtok:
  input: 0.15                    # off-peak; 2x at peak (01:00-04:00 and 06:00-10:00 UTC, Mon-Fri)
  output: 0.60                   # off-peak; 2x at peak
  cache_read: 0.003              # off-peak; 2x at peak
  cache_write: null
context_window: 1000000          # max output 384K
notes_on_cost: >
  The cheapest capable bulk worker in the research. Cache hits at $0.003 are
  about 25x cheaper than Gemini 3.8 Flash's, so repeated passes over the same
  large repo context are nearly free. Peak hours (UTC weekday mornings) double
  every price, which complicates forecasts. AA cost per task is unverified. On
  agentic work, cheap per token is not cheap per task: OpenRouter's cost router
  sent about 60% of requests here, took 104 steps vs 19 for Astra low, and cost
  more than Astra low.

effort:
  levels: []
  default: null
  avoid: []
  notes: >
    No effort control. Thinking is on by default; a non-thinking mode also
    exists. Keep thinking on for code.

scores:
  intelligence: 4
  taste: 3
  floor: 3
  thoroughness: 3
  cost_efficiency: 7
  speed: 5
  computer_use: 1
  orchestration: 2

tasks:
  quick-fix:      {fit: ok,      note: "Narrow, fully specified edits with a test; beat Gemini 3.8 Flash on one hands-on task (2 turns vs 4). Review before merge."}
  feature:        {fit: poor,    note: "Must-land and wide; big drop on hard multi-step suites (Terminal-Bench 4.0 31.2 vs 51.8 for Opus 5)."}
  long-run:       {fit: poor,    note: "Research: not for long unattended builds; the cost-router test took 104 steps per task."}
  frontend:       {fit: poor,    note: "No evidence of taste; image input only, no audio, video or PDF."}
  review:         {fit: poor,    note: "No evidence; use Sol, Astra or Grok 4.7."}
  investigate:    {fit: poor,    note: "No evidence; low index on hard multi-step work."}
  analyze:        {fit: ok,      note: "Cheap repeated passes over a cached repo (summaries, inventories); not architecture or planning."}
  bulk:           {fit: good,    note: "Mechanical edits, test generation, summarising many files, log triage; 384K output fits full-file regeneration. Verify programmatically."}
  research:       {fit: ok,      note: "Cheap summarisation of supplied documents; no evidence on web research."}
  computer-use:   {fit: poor,    note: "No evidence of computer-use support."}
  copy:           {fit: unknown, note: "No evidence."}
  3d-games:       {fit: unknown, note: "No evidence."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: poor,    note: "Must-land loop; low floor."}
  orchestrate:    {fit: poor,    note: "Not a lead model."}

role_hints:
  as_primary: "Not a primary model."
  as_subagent: "Cheapest bulk worker for repeated passes over the same large context, long generated outputs, and log or file triage, with output verified programmatically."
  never_for: ["anything that must land without review", "architecture or planning", "long unattended runs", "frontend, UI or copy", "leading other agents", "work under data-jurisdiction restrictions without sign-off"]
---

## Summary

DeepSeek V4.1 Flash is the cheapest capable bulk worker in the research: AA
index 39, $0.15 / $0.60 per MTok off-peak, cache reads at $0.003, a 1M context and
a 384K output cap, with MIT-licensed weights. In this kit it does mechanical,
verifiable work: repeated passes over the same large repo, test generation, file
and log summarisation, and long generated artefacts. It is not for planning,
review or anything that must land. This profile comes from vendor docs and
aggregators, not hands-on testing; test it on your own tasks before trusting it.

## Strengths

- **Cache economics.** $0.003 cached input, about 25x cheaper than Gemini 3.8
  Flash's; repeated passes over a cached repo cost almost nothing
  (`research/model-gaps.md § 4c. DeepSeek V4.1 Flash (and V4 Pro)`).
- **Largest output cap in the research.** 384K tokens; suits full-file
  regeneration and long generated artefacts.
- **Short terminal tasks (vendor).** Terminal-Bench 2.1 90.6 (up from 82.7),
  DeepSWE v1.1 74.2.
- **One hands-on win.** DataCamp: beat Gemini 3.8 Flash on a scheduler task in 2
  turns vs 4 (single task, single source).
- **Compatible endpoints.** OpenAI- and Anthropic-compatible APIs, so it can sit
  behind `claude -p` via base-URL override (unverified beyond the vendor's
  claim; `research/model-gaps.md § 4 › How to run them from a terminal`).
- **Open weights (MIT).** 552B total, about 8B active for input and 16B for output;
  native image input.

## Weaknesses and failure modes

- **Collapses on hard multi-step agent suites.** Terminal-Bench 3.0 30.0 and 4.0
  31.2 vs 43.3 and 51.8 for Opus 5 (vendor).
- **The cost-router lesson.** OpenRouter's cost-optimising router sent about 60%
  of requests to DeepSeek V4.1 Flash. It took 104 steps and 20 minutes per task
  vs 19 steps and 4.6 minutes for Astra low, and cost more than Astra low; 6.1
  Sol at low got the same score for 1/8 the price. "A model that cannot reason,
  that is given a prompt and no context, cannot make a good decision around how
  hard the problem is" ([SOL61 19:56](https://youtu.be/vu8X3YroB-w?t=1196)). The router's choices are not a clean test of the model, but they
  show that this model is cheap per token, not per hard agentic task.
- **Inputs.** No audio, video or PDF.
- **Peak pricing.** 2x during 01:00–04:00 and 06:00–10:00 UTC on weekdays.
- **Jurisdiction.** Possible data-jurisdiction and policy concerns for some
  organisations; check before sending proprietary code to the first-party API.
- **Lower floor expected** for labs outside Anthropic/OpenAI
  ([MODELS 5:41](https://youtu.be/iBrAWpjXNxs?t=341)).

## How to prompt it

No hands-on prompting evidence. Inferred from its profile:

- One mechanical task per call, files named, output format fixed.
- Put the large shared context (repo files, schema, style guide) at the start of
  the prompt and keep it identical across calls so cache hits apply.
- Prefer giving it the whole file to regenerate when that is simpler to verify
  than a patch; the 384K output cap allows it.
- Keep thinking on for code.
- Run through OpenCode or Pi: `opencode run -m <provider>/<model> --format json
  "<task>"`; check the exact model string with `opencode models`
  (`research/model-gaps.md § 4 › How to run them from a terminal`).

## Routing guidance

Route here for:
- Bulk mechanical edits and test generation over one large repo context.
- Summarising many files; log triage; large-document reading.
- Full-file regeneration and long generated artefacts.
- Cheap subagent fan-out where the output is checked by tests or a stronger
  model.

Do not route here for:
- Architecture, planning, review, investigation.
- Long unattended builds or anything that must land.
- Hard multi-step agent tasks where step count drives cost (use 6.1 Sol at low).

Handoff patterns:
- **DeepSeek digests, frontier decides.** It reads and summarises; Opus or Sol
  acts.
- **Route by task type, not by price.** Never put it behind a per-request
  cheapest-model router; assign it task classes that are known to be mechanical.
- **Pick among cheap tiers by pattern:** DeepSeek for cached repeated passes and
  long outputs; Gemini 3.8 Flash for speed and multimodal input; Luna for lowest
  measured cost per task.
- **Skip V4 Pro.** `deepseek-v4-pro` scores lower on AA (36) and costs more.

## When this beats the frontier

- Many passes over the same large cached context, where $0.003 cache reads make
  the frontier's cache price the dominant cost.
- Single outputs longer than 128K tokens.
- Verifiable, mechanical, high-volume work on an API budget, run off-peak.

## Cost notes

- Off-peak $0.15 / $0.003 / $0.60 per MTok; peak is exactly 2x. $5 minimum
  prepaid balance.
- AA cost per task is unverified (not listed).
- Schedule large batch jobs outside 01:00–04:00 and 06:00–10:00 UTC on weekdays.
- Third-party hosts (OpenRouter) set their own prices and may not offer the
  first-party cache discount; check before relying on it.

## Evidence

- `research/model-gaps.md § Naming corrections` (DeepSeek V3.x/R-series names are
  stale; V4.1 Flash is current), `§ At-a-glance comparison`, `§ 4. Open-weights
  models for OpenCode / Pi › How to run them from a terminal`, `§ 4c. DeepSeek
  V4.1 Flash (and V4 Pro)`, `§ Suggested routing-table shortlist`.
- [SOL61 20:13](https://youtu.be/vu8X3YroB-w?t=1213) (60% of router
  traffic, 104 steps).
- [MODELS 5:41](https://youtu.be/iBrAWpjXNxs?t=341) (open-weight
  floors).
- URLs: [DeepSeek pricing docs](https://api-docs.deepseek.com/quick_start/pricing),
  [BuildFastWithAI review](https://blog.buildfastwithai.com/deepseek-v4-1-flash-review),
  [DataCamp comparison](https://www.datacamp.com/blog/deepseek-v4-1-flash-vs-gemini-3-8-flash),
  [NVIDIA model card](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash/modelcard),
  [Activepieces](https://www.activepieces.com/blog/deepseek-v4-1-flash-api-pricing-docs-2026),
  [AA leaderboard](https://artificialanalysis.ai/leaderboards/models),
  [kingy.ai open-weights shortlist](https://kingy.ai/news/best-open-weight-ai-models-in-2026-glm-5-2-vs-deepseek-v4-vs-kimi-k2-6-vs-qwen-vs-mistral/),
  [OpenCode providers](https://opencode.ai/docs/providers/).
- **Unverified:** AA speed and cost per task (not listed); the DataCamp turn count
  (one task); Anthropic-compatible use behind `claude -p`; OpenRouter and OpenCode
  model strings; Pi flag names. Terminal-Bench and DeepSWE figures are vendor.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 4 | AA 39 vs 54 for Opus 5.5; strong on short terminal tasks but Terminal-Bench 4.0 31.2 vs 51.8. |
| taste | 3 | No evidence. |
| floor | 3 | No hands-on long-run evidence; 104 steps per task in the router test; Theo expects lower floors from open weights. |
| thoroughness | 3 | No review or audit evidence. |
| cost_efficiency | 7 | Lowest list and cache prices in the research and a 2-vs-4-turn win over Gemini Flash, but AA $/task is unknown, peak pricing doubles cost, and the router test cost more than Astra low. |
| speed | 5 | No measured speed; the router test averaged 20 minutes per task. |
| computer_use | 1 | No evidence of support. |
| orchestration | 2 | No evidence; not a lead model. |
