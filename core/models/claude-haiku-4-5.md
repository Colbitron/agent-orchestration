---
id: claude-haiku-4-5
name: Claude Haiku 4.5
vendor: anthropic
family: claude
status: current                  # retirement "not sooner than 2026-10-15"; Haiku 5.5 announced, unreleased
released: 2025-10
as_of: 2026-10-02
confidence: medium               # specs from Anthropic docs (high); routing from web research plus one Theo rule, no hands-on use

api_ids: [claude-haiku-4-5, claude-haiku-4-5-20251001]   # Bedrock anthropic.claude-haiku-4-5; Vertex claude-haiku-4-5@20251001
access:
  subscriptions: [claude-pro, claude-max]   # unverified: available in Claude Code at launch; current plan gating not confirmed
  api: true
  harnesses: [claude-code, cursor, opencode, t3-code]
  invoke_via: [claude-cli, cursor-cli]

pricing_per_mtok:
  input: 1
  output: 5
  cache_read: 0.10
  cache_write: 1.25              # 5-minute write; 1-hour write is $2
context_window: 200000
notes_on_cost: >
  Cheap per token ($1 / $5) but not cheap per completed task: Artificial Analysis
  measures about $0.28 per index task at an Intelligence Index of 17, about the
  same cost as GPT-6.1 Sol ($0.32) at 50. Cheaper non-Anthropic tiers (GPT-6 Luna,
  DeepSeek V4.1 Flash, Gemini 3.8 Flash) score more than twice as high for less.
  Batch is half price. The only cost argument for it is staying inside an
  Anthropic-only flow.

effort:
  levels: []
  default: null
  avoid: []
  notes: >
    No effort control: the effort parameter is not supported. Reasoning uses
    extended thinking with an explicit budget_tokens value instead.

scores:
  intelligence: 2
  taste: 3
  floor: 3
  thoroughness: 2
  cost_efficiency: 3
  speed: 7
  computer_use: 2
  orchestration: 1

tasks:
  quick-fix:      {fit: poor, note: "AA 17 and a Feb 2025 knowledge cutoff; Luna, DeepSeek Flash or Opus at medium are better value even for narrow tickets."}
  feature:        {fit: poor, note: "Never for work that must merge (Theo: 'not useful for anything real')."}
  long-run:       {fit: poor, note: "200K context, lowest index in the roster; no evidence it can hold a multi-hour run."}
  frontend:       {fit: poor, note: "No evidence; taste-sensitive work belongs to Fable."}
  review:         {fit: poor, note: "Research explicitly says not to give it review; use Sol, Astra or Grok 4.7."}
  investigate:    {fit: poor, note: "No evidence; low index and old knowledge make it a poor root-causer."}
  analyze:        {fit: poor, note: "Research says not to give it planning; Sonnet or Sol for analysis."}
  bulk:           {fit: ok,   note: "Only trivial Claude-only chores (grep summaries, commit messages, classification) when leaving Anthropic is not allowed; otherwise Luna, DeepSeek Flash or Gemini Flash."}
  research:       {fit: poor, note: "Knowledge reliable only to Feb 2025; it will not know 2026 APIs."}
  computer-use:   {fit: poor, note: "No evidence; Opus 5.5 already scores 4 here and OpenAI models lead."}
  copy:           {fit: poor, note: "No evidence; Opus 5.5 is the copy model."}
  3d-games:       {fit: poor, note: "No evidence."}
  prompt-writing: {fit: poor, note: "No evidence; prompts and skills should come from a frontier model."}
  babysit:        {fit: poor, note: "Must-land, long and narrow; needs a higher floor."}
  orchestrate:    {fit: poor, note: "Not a lead model."}

role_hints:
  as_primary: "Never. Don't route real work here; wait for Haiku 5.5 and re-profile."
  as_subagent: "Only for trivial, verifiable chores inside an Anthropic-only flow (file search summaries, commit messages, classification)."
  never_for: ["anything that must land", "code review", "planning or analysis", "investigation", "work that needs post-2025 API knowledge", "repos that exceed a 200K context", "leading other agents"]
---

## Summary

Don't use it, at least until Haiku 5.5 ships. Haiku 4.5 is Anthropic's current
small model. Its Artificial Analysis Intelligence Index is 17, far below the cheap
tiers from other labs, and Theo's roster says "Never use haiku ... It's not useful
for anything real." This profile comes from vendor docs and aggregators, not
hands-on testing; test it on your own tasks before trusting any of it. It is
likely to be replaced within weeks: Haiku 5.5 is announced but unreleased, and
4.5 can be retired from 2026-10-15.

## Strengths

- **Fast.** "Fastest" in Anthropic's lineup; AA measures about 103 output tok/s
  (`research/model-gaps.md § 1. Claude Haiku 4.5`).
- **Cheap per token.** $1 in / $5 out, $0.10 cache reads, batch at half price
  (same section).
- **Stays inside Anthropic.** Reachable with `claude -p ... --model haiku` and on
  Bedrock and Vertex. That matters only where policy forbids other vendors.
- **Vendor-named uses.** Anthropic pitched it for sub-agent orchestration, pair
  programming and real-time apps, with 73.3% on SWE-bench Verified at launch
  (vendor, Oct 2025; an old benchmark generation) (same section).

## Weaknesses and failure modes

- **Far behind on independent measures.** AA Intelligence Index 17, vs 38–41
  for GPT-6 Luna, DeepSeek V4.1 Flash and Gemini 3.8 Flash, and 54 for Opus 5.5
  (`research/model-gaps.md § At-a-glance comparison`).
- **Not cheap per task.** About $0.28 per AA task, about the same as GPT-6.1 Sol
  ($0.32), which scores 50 (same section).
- **Old knowledge.** Reliable to Feb 2025 (training data to Jul 2025). It will not
  know 2026 APIs, SDKs or models.
- **Small context.** 200K context and 64K max output, the smallest window in the
  Claude lineup; large repos will not fit.
- **No effort control.** Only an extended-thinking token budget.
- **Theo's rule.** "Never use haiku. Just don't at this point. It's not useful
  for anything real, especially with [GPT-5.5] being effectively free"
  (`transcripts/general/agent-orchestration-inspiration.html` ~19:00; quoted in
  `core/strategies/cost-model.md § 11`). That was said of Haiku before the 2026
  cheap tiers, and nothing since has improved its relative position.
- **About to be retired.** Retirement "not sooner than October 15, 2026". A
  routing table that pins it may break soon after that.

## How to prompt it

There is no evidence on prompting it well. If it must be used:

- Give it one closed, checkable task with the exact files named and the output
  format fixed (a list, a JSON object, a one-line commit message).
- Do not rely on it for anything that needs current API knowledge; paste the
  relevant docs.
- Set a thinking budget explicitly (`thinking: {type: "enabled", budget_tokens: N}`)
  rather than an effort level, which it rejects.
- Verify its output programmatically or with a stronger model before using it.

## Routing guidance

Route here for:
- Nothing by default. The kit rule (`core/strategies/cost-model.md § 11`) is "do
  not route real work to Haiku".
- At most, trivial Claude-only chores where no other vendor is allowed: file
  search summaries, commit-message and changelog drafts, classification
  (`research/model-gaps.md § 1 › Routing suggestion`).

Do not route here for:
- Multi-file implementation, review, planning, investigation, or anything that
  must land.
- Cheap bulk work when cross-vendor routing is allowed: use GPT-6 Luna, DeepSeek
  V4.1 Flash, GLM-5.3-Flash or Gemini 3.8 Flash.
- Anything that needs more than 200K tokens of context.

Handoff patterns:
- **Replace it, don't hand off to it.** In a Claude-only kit, Sonnet 5.5 or Opus
  5.5 at medium takes the cheap slot; in a mixed kit, 6.1 Sol or a cheap-tier
  model does.
- **Re-profile on Haiku 5.5.** Anthropic says Haiku 5.5 is "built for high volume
  and cost-sensitive applications", "our first Haiku release in a year", with
  "many of the same improvements" as Opus 5.5 (`research/claude-releases.md`
  transcription notes and `§ Video 2: Claude Opus 5.5 › 4. Pricing, speed,
  context and limits`). When it ships, write a new profile; it will likely
  replace this one.

## When this beats the frontier

Rarely; use only when the frontier models are unavailable or the task is
verifiable and bulk, and even then a cheap non-Anthropic model is usually the
better choice. The one real case is an Anthropic-only environment where a
trivial, checkable chore must run fast.

## Cost notes

- $1 / $5 per M in/out; cache read $0.10; cache write $1.25 (5 min) or $2 (1 h);
  batch $0.50 / $2.50.
- AA cost per task about $0.28. Cheap per token is not cheap per completed task:
  a low-index model that needs retries or a stronger model's cleanup costs more
  than a capable model that finishes (`research/gpt-releases.md § Critique of
  naive cost routers`).
- On a Claude subscription its quota use is not documented in the research.
- **Alias caveat:** `--model haiku` resolves to the current Haiku. When Haiku 5.5
  ships, the alias should move to it; pin `claude-haiku-4-5-20251001` only if you
  need the old model until retirement.

## Evidence

- `research/model-gaps.md § Naming corrections` (Haiku 4.5 is still current;
  no Haiku 5 ever; Haiku 5.5 announced 2026-09-22, no ID or price yet; retirement
  not sooner than 2026-10-15).
- `research/model-gaps.md § 1. Claude Haiku 4.5 (and Haiku 5.5 status)`: IDs,
  pricing, 200K/64K, knowledge cutoff, no effort parameter, AA 17, 103 tok/s,
  $0.28 per task, routing suggestion.
- `research/model-gaps.md § At-a-glance comparison` and `§ Suggested routing-table
  shortlist` ("Claude Haiku 4.5 (AA 17; wait for Haiku 5.5)").
- URLs: [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview),
  [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing),
  [Anthropic Haiku 4.5 launch](https://www.anthropic.com/news/claude-haiku-4-5),
  [AA leaderboard](https://artificialanalysis.ai/leaderboards/models). Haiku 5.5:
  [Mike Krieger on X](https://x.com/mikeyk/status/2102441803253535060),
  [cellcog](https://cellcog.ai/blog/claude-haiku-5-5-release-date/),
  [docsbot](https://docsbot.ai/models/claude-haiku-5-5).
- `transcripts/general/agent-orchestration-inspiration.html` ~19:00 (Theo's
  "never use haiku" rule) and `core/strategies/cost-model.md § 11`.
- `research/claude-releases.md` (Haiku 5.5 "coming in the next few weeks"; none
  of the videos evaluates Haiku 4.5).
- **Unverified:** current subscription-plan gating (launch announcement only);
  AA figures are from one aggregator; SWE-bench 73.3% is a vendor number from
  Oct 2025.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 2 | AA 17, less than half of the cheap tiers (38–41) and a third of Opus 5.5 (54); old knowledge cutoff. |
| taste | 3 | No evidence; an old small model with no design or copy track record. |
| floor | 3 | No hands-on evidence; Theo's "not useful for anything real" and the low index argue against trusting it on anything wide. |
| thoroughness | 2 | Research says not to give it review or planning; 200K context limits how much it can read. |
| cost_efficiency | 3 | Cheap per token, but about the same AA cost per task as 6.1 Sol at a third of the index; cheaper tiers beat it. |
| speed | 7 | Fastest Anthropic model (about 103 tok/s on AA); Gemini 3.8 Flash is about 3x faster. |
| computer_use | 2 | No evidence for this model; the stronger Claude models only reach 4. |
| orchestration | 1 | No evidence and not designed as a lead. |
