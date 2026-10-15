---
id: mimo-v2-6-pro
name: Xiaomi MiMo-V2.6-Pro
vendor: xiaomi
family: open-weights
status: current
released: 2026-09                # 2026-09-21
as_of: 2026-10-02
confidence: low                  # 11 days old at research time; prices third-party only and possibly promotional; benchmarks mostly vendor

api_ids: [xiaomi/mimo-v2.6-pro]  # OpenRouter id; Xiaomi first-party API id unverified
access:
  subscriptions: []
  api: true
  harnesses: [opencode, pi, cursor]
  invoke_via: [openrouter-api, opencode-cli]   # no ollama: 1.02T total parameters does not fit locally (V2.6-Flash is 310B, also too large for typical machines)

pricing_per_mtok:
  input: 0.435                   # unverified: third-party sources only, may be promotional
  output: 0.87                   # unverified
  cache_read: 0.0036             # unverified
  cache_write: null
context_window: 1000000
notes_on_cost: >
  Best intelligence per dollar in the open-weights set: Artificial Analysis index
  46 (tied with Grok 4.7) at about $0.13 per index task, vs $0.32 for GPT-6.1 Sol
  (50) and $3.74 for Grok 4.7. Prices come from third parties, not a Xiaomi page,
  and may be promotional for a model this new. Slow output (45 tok/s) costs
  wall-clock, not money.

effort:
  levels: []
  default: null
  avoid: []
  notes: >
    No effort control documented in the research.

scores:
  intelligence: 5
  taste: 3
  floor: 4
  thoroughness: 4
  cost_efficiency: 8
  speed: 3
  computer_use: 2
  orchestration: 2

tasks:
  quick-fix:      {fit: ok,      note: "Narrow, specified edits with a test; slow output makes interactive loops tedious."}
  feature:        {fit: ok,      note: "Research: candidate for mid-size implementation (DeepSWE 71.9 vs Opus 5's 74.0, vendor). Never merge without Opus/Sol review."}
  long-run:       {fit: poor,    note: "Trails clearly on the hardest long-horizon work (Terminal-Bench 4.0 34.9 vs 49.0 Opus 5, 59.6 Astra)."}
  frontend:       {fit: unknown, note: "Accepts image input; no evidence on design quality."}
  review:         {fit: ok,      note: "Research names it a candidate for cheap mid-tier review passes; untested. Not the reviewer of record."}
  investigate:    {fit: unknown, note: "No evidence."}
  analyze:        {fit: good,    note: "Strongest cheap option for audits, inventories and decomposition drafts at AA 46; verify findings with a frontier model."}
  bulk:           {fit: good,    note: "Cheap per task at a higher index than the Flash tiers; best where throughput matters more than latency (45 tok/s)."}
  research:       {fit: good,    note: "Research and summarisation named as a fit; text, image, audio and video input."}
  computer-use:   {fit: unknown, note: "No evidence."}
  copy:           {fit: unknown, note: "No evidence."}
  3d-games:       {fit: unknown, note: "No evidence."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: poor,    note: "Must-land loop; slow and floor unproven."}
  orchestrate:    {fit: poor,    note: "Not a lead model."}

role_hints:
  as_primary: "Not a primary model."
  as_subagent: "Strongest cheap open-weights worker: analysis, research, bulk and mid-size implementation subagent whose output a frontier model verifies."
  never_for: ["long unattended runs", "latency-sensitive interactive loops", "code that merges without review", "leading other agents"]
---

## Summary

MiMo-V2.6-Pro is Xiaomi's MIT-licensed model and the top open-weights model on
Artificial Analysis (index 46, tied with Grok 4.7) at about $0.13 per task. In
this kit it is the strongest cheap open-weights option: analysis, research and
summarisation, bulk work, and mid-size implementation that a frontier model
reviews. It is slow (45 tok/s) and trails clearly on hard long-horizon coding.
This profile comes from vendor docs and aggregators, not hands-on testing, and
the model was 11 days old when researched; test it on your own tasks before
trusting it.

## Strengths

- **Intelligence per dollar.** AA index 46, #1 among open weights, at about $0.13
  per task (`research/model-gaps.md § 4a. Xiaomi MiMo-V2.6-Pro (and V2.6-Flash)`;
  `§ At-a-glance comparison`). Of the open-weights models, only MiMo-V2.6-Pro,
  GLM-5.3-Flash and DeepSeek V4.1 Flash stay cheaper per task than 6.1 Sol, and
  MiMo has the highest index of the three.
- **Mid-size coding (vendor).** DeepSWE v1.1 71.9 vs 74.0 for Opus 5 and Astra.
- **Multimodal input.** Text, image, audio and video; 1M context.
- **Open weights, MIT licence.** 1.02T total, 42B active.
- **Variants.** V2.6-Flash (310B total, 15B active; $0.14 / $0.28, unverified), a
  "Pro-UltraSpeed" variant claimed 20x faster, and a distilled Qwen-9B variant.
  None are profiled.

## Weaknesses and failure modes

- **Hard long-horizon coding.** Terminal-Bench 4.0 34.9 vs 49.0 for Opus 5 and
  59.6 for Astra. Research: "Not for long unattended builds."
- **Slow.** 45 tok/s on AA; avoid latency-sensitive interactive loops.
- **Thin, vendor-dominated evidence.** Very new; no independent harness reports.
- **Price may be promotional** and is not confirmed on a Xiaomi page.
- **First-party API id unknown**; OpenRouter is the confirmed route.
- **Lower floor expected** outside Anthropic/OpenAI
  ([MODELS 5:41](https://youtu.be/iBrAWpjXNxs?t=341)).

## How to prompt it

No hands-on prompting evidence. Inferred:

- Scope each task to one bounded question or change with a clear done state.
- Run it in parallel and in the background rather than interactively, because
  of its output speed.
- For analysis and review passes, ask it to mark what it could not confirm and
  make "nothing found" a valid answer, then have a frontier model verify.
- Run through OpenCode or Pi: `opencode run -m openrouter/xiaomi/mimo-v2.6-pro
  --format json "<task>"` (exact provider string unverified; check `opencode
  models`).

## Routing guidance

Route here for:
- Cheap analysis: codebase audits, inventories, decomposition drafts.
- Research and summarisation, including image, audio and video inputs.
- Bulk work where a higher index than the Flash tiers matters.
- Mid-size implementation subagents whose work Opus or Sol reviews.
- A cheap extra review pass beside Sol (untested).

Do not route here for:
- Long unattended builds or anything resembling Terminal-Bench 4.0.
- Interactive, latency-sensitive loops.
- Code that merges without frontier review; leading agents.

Handoff patterns:
- **MiMo drafts, frontier verifies.** MiMo produces the audit, plan draft or
  implementation; Opus or Sol checks it before anything lands.
- **The open-weights pick.** When a user wants one open-weights model in the
  middle tier, this is it (`research/model-gaps.md § Suggested routing-table
  shortlist`); the Flash tiers stay the cheaper choice for purely mechanical
  work.

## When this beats the frontier

- Analysis and research runs at a fraction of frontier cost where a frontier
  model will verify the result.
- Large background fan-out of mid-difficulty subagent tasks on an API budget.
- Deployments that require open weights at the highest available index.

## Cost notes

- $0.435 / $0.0036 / $0.87 per MTok (third-party, unverified; possibly
  promotional). Re-check before relying on it.
- About $0.13 per AA task, about 40% of 6.1 Sol's $0.32.
- Cache reads at $0.0036 are close to DeepSeek V4.1 Flash's $0.003, so repeated
  passes over a cached repo are cheap.
- Slow output means wall-clock, not money, is the cost to watch.

## Evidence

- `research/model-gaps.md § Naming corrections` (MiMo-V2.6-Pro is the open-weights
  leader on AA), `§ At-a-glance comparison` and its main takeaway, `§ 4.
  Open-weights models for OpenCode / Pi › How to run them from a terminal`,
  `§ 4a. Xiaomi MiMo-V2.6-Pro (and V2.6-Flash)`, `§ Suggested routing-table
  shortlist` (mid / second-opinion tier, "cheapest AA-46").
- [MODELS 5:41](https://youtu.be/iBrAWpjXNxs?t=341) (open-weight
  floors; general, not about MiMo).
- URLs: [VentureBeat](https://venturebeat.com/technology/better-than-deepseek-xiaomis-mimo-v2-6-pro-debuts-as-the-top-open-weights-model-in-the-world-alongside-cheaper-v2-6-flash),
  [AA open-weights page](https://artificialanalysis.ai/models/open-source),
  [AA leaderboard](https://artificialanalysis.ai/leaderboards/models),
  [OpenRouter](https://openrouter.ai/xiaomi/mimo-v2.6-pro),
  [kingy.ai benchmarks](https://kingy.ai/blog/mimo-v2-6-pro-benchmarks-specs-comparison/),
  [OpenCode providers](https://opencode.ai/docs/providers/).
- **Unverified:** all prices (third-party only); first-party API id; Flash and
  UltraSpeed variant claims. DeepSWE and Terminal-Bench numbers are vendor; only
  the AA index, speed and cost per task are independent, from one aggregator.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 5 | AA 46 (vs 54 for Opus 5.5), highest of the cheap models, but Terminal-Bench 4.0 34.9 vs 49.0 for Opus 5. |
| taste | 3 | No evidence. |
| floor | 4 | No hands-on evidence; brand-new model; Theo expects lower floors from open weights. |
| thoroughness | 4 | Named as a review-pass candidate, untested. |
| cost_efficiency | 8 | About $0.13 per AA task at index 46, the best intelligence per dollar in the open-weights set; prices unverified and possibly promotional, so below Sol's 10. |
| speed | 3 | 45 tok/s on AA, slow. |
| computer_use | 2 | Multimodal input but no computer-use evidence. |
| orchestration | 2 | No evidence; not a lead model. |
