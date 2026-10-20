---
id: glm-5-3
name: GLM-5.3-Flash                # frontmatter describes GLM-5.3-Flash; full GLM-5.3 is covered in the body
vendor: zhipu                      # Z.ai
family: open-weights
status: current
released: 2026-08                  # GLM-5.3-Flash 2026-08-27 (GLM-5.3 2026-08-14)
as_of: 2026-10-19
confidence: low                    # prices from Z.ai docs; benchmarks vendor-only plus one AA index; one Theo anecdote

api_ids: [glm-5.3-flash]           # siblings: glm-5.3 (full), glm-5.3-flashx; OpenRouter/OpenCode strings unverified
access:
  subscriptions: [glm-coding-plan]   # unverified: plan tiers are third-party, and whether the plan serves Flash or only GLM-5.3 is not stated
  api: true
  harnesses: [opencode, pi, cursor, openclaw, hermes]
  invoke_via: [openrouter-api, opencode-cli, openclaw-cli, hermes-cli]   # no ollama: 320B total parameters needs a 256GB+ workstation even quantised; openclaw, hermes / openclaw-cli, hermes-cli added 2026-10-19: via each runtime's OpenRouter provider; model strings unverified

pricing_per_mtok:
  input: 0.15
  output: 0.50
  cache_read: 0.03
  cache_write: null
context_window: 1000000            # unverified for Flash; one source says 200K for the open-weights architecture
notes_on_cost: >
  Gemini-Flash-like prices ($0.15 / $0.03 / $0.50) at an Artificial Analysis
  index of 42; AA cost per task about $0.10 (unverified). Full GLM-5.3 is a
  different price class ($1.40 / $0.26 / $4.40, $2.01 per AA task at max, above
  Opus 5.5 at high) and is only good value on a flat-rate GLM Coding Plan.

effort:
  levels: [low, high, max]         # reasoning_effort values documented for GLM-5.3; unverified for Flash
  default: high
  avoid: [max]
  notes: >
    Thinking is always on (disabling it no longer works). Z.ai recommends max for
    coding and AA measured the family at max; the kit's never-max rule says start
    at high and test max on your own tasks, since Flash's per-token cost is small.

scores:
  intelligence: 4
  taste: 3
  floor: 4
  thoroughness: 3
  cost_efficiency: 7
  speed: 5
  computer_use: 1
  orchestration: 2

tasks:
  quick-fix:      {fit: ok,      note: "Narrow, fully specified edits with a test; review before merge."}
  feature:        {fit: ok,      note: "Theo suggests it for cost-constrained users ('go off the rails less than Astra'); single anecdote and AA 42, so only where Opus/Sol are unavailable, with review."}
  long-run:       {fit: poor,    note: "No evidence; vendor SWE-Marathon 42.5 is for full GLM-5.3."}
  frontend:       {fit: poor,    note: "Text-only: no vision input for screenshots or designs."}
  review:         {fit: poor,    note: "No evidence; use Sol, Astra or Grok 4.7."}
  investigate:    {fit: poor,    note: "No evidence."}
  analyze:        {fit: ok,      note: "Cheap first-pass codebase summaries and inventories; verify conclusions."}
  bulk:           {fit: good,    note: "Strong cheap-tier bulk worker per research (AA 42 at Flash prices); verify programmatically."}
  research:       {fit: ok,      note: "Cheap summarisation of supplied text; no evidence on web research."}
  computer-use:   {fit: poor,    note: "Text-only; cannot see a screen."}
  copy:           {fit: unknown, note: "No evidence."}
  3d-games:       {fit: poor,    note: "Text-only; no visual feedback."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: poor,    note: "Must-land loop; floor unproven."}
  orchestrate:    {fit: poor,    note: "Not a lead model."}

role_hints:
  as_primary: "Only for cost-constrained users without Opus/Sol access, per Theo's suggestion; otherwise not a primary."
  as_subagent: "Cheap, self-hostable bulk worker for mechanical text and code work with programmatic verification."
  never_for: ["frontend, UI or anything visual", "computer use", "long unattended runs", "code review of record", "leading other agents", "full GLM-5.3 at max effort on per-token billing"]
---

## Summary

**This profile's frontmatter describes GLM-5.3-Flash**, not full GLM-5.3. The
research gives them separate IDs, prices and AA scores, and Flash is the one
Theo called pleasant. GLM-5.3-Flash is Z.ai's cheap open-weights tier: AA index
42 at $0.15 / $0.50 per MTok, text-only. In this kit it is a cheap bulk worker
and, for users without frontier access, a tolerable general model. Full GLM-5.3
(AA 45) only makes sense on the flat-rate GLM Coding Plan. This profile comes
from vendor docs and aggregators plus one remark from Theo, not hands-on testing;
test it on your own tasks before trusting it.

### Variants

| Model | ID | Price in / cache / out | AA index | Notes |
|---|---|---|---|---|
| GLM-5.3 | `glm-5.3` | 1.40 / 0.26 / 4.40 | 45 (max), $2.01/task, 74 tok/s | 744–753B total, about 40B active; released 2026-08-14 |
| **GLM-5.3-Flash** | `glm-5.3-flash` | 0.15 / 0.03 / 0.50 | 42, about $0.10/task (unverified) | 320B total, 18B active; released 2026-08-27 |
| GLM-5.3-FlashX | `glm-5.3-flashx` | 0.37 / 0.075 / 1.25 | not listed | No benchmarks found |

Source: `research/model-gaps.md § 4b. GLM-5.3 and GLM-5.3-Flash (Z.ai /
Zhipu)` and `§ At-a-glance comparison`.

## Strengths

- **Price for the index.** AA 42 at Gemini-Flash-like prices; "GLM-5.3-Flash is
  the interesting one ... a strong cheap-tier bulk worker, and it is
  self-hostable" (`research/model-gaps.md § 4b › Routing`).
- **Theo's remark.** "A more pleasant model to use arguably than Astra. I've seen
  GLM53 Flash go off the rails less than Astra for similar work." He suggests it,
  or an open-source plan, "if cost is the main concern"
  ([FVA 1:14:10](https://youtu.be/P7bxbDSnZRM?t=4450), [FVA 1:09:43](https://youtu.be/P7bxbDSnZRM?t=4183),
  [FVA 1:14:04](https://youtu.be/P7bxbDSnZRM?t=4444)). Astra's floor is
  scored 3 in this kit, so this is praise relative to a low bar.
- **Open weights.** Self-hostable for teams that need to keep code in-house.
- **Harness reach.** The GLM Coding Plan plugs into Claude Code (via base-URL
  override), Cline, Roo, OpenCode and about 20 other tools (third-party,
  unverified).

## Weaknesses and failure modes

- **Text-only.** No vision; useless for screenshots, designs or computer use.
- **Vendor-only benchmarks.** GLM-5.3's DeepSWE 66.9, FrontierSWE 78.1,
  Terminal Bench 3.0 28.3 and SWE-Marathon 42.5 have no independent replication,
  and are for the full model, not Flash.
- **Behind the frontier by its maker's own account.** Z.ai says GLM-5.3 is behind
  Claude Fable 5.
- **Thinking always on.** No way to switch it off for trivial transforms.
- **Licence conflict.** GLM-5.3 weights use a bespoke licence; some sources say
  MIT. Flash's licence is not separately stated. Check before self-hosting
  commercially.
- **Context uncertainty.** 1M per one source; 200K for the open-weights
  architecture per another.
- **Lower floor expected** outside Anthropic/OpenAI
  ([MODELS 5:41](https://youtu.be/iBrAWpjXNxs?t=341)).

## How to prompt it

No hands-on prompting evidence. Inferred:

- Text-only, so paste error output and file contents; never rely on
  screenshots.
- One mechanical task per call, files named, output format fixed.
- Start at `reasoning_effort: high`; try `max` if quality misses (Z.ai's
  recommendation for coding) and compare cost.
- Run through OpenCode or Pi: `opencode run -m <provider>/<model> --format json
  "<task>"`; the OpenCode docs' example `z-ai/glm-4.7` is stale, so check
  `opencode models` for the current string.

## Routing guidance

Route here for:
- Bulk mechanical text and code work with programmatic verification.
- Cheap subagent fan-out, log digging and large-document reading (text only).
- A cost-constrained user's general model when Opus and Sol are not available
  (Theo's suggestion), with review on anything that merges.
- Full GLM-5.3 only on a flat-rate Coding Plan, e.g. inside Claude Code.

Do not route here for:
- Anything visual: frontend, screenshots, computer use, 3D.
- Review, investigation, planning, long runs, leading agents.
- Full GLM-5.3 at `max` on per-token billing: $2.01 per AA task, above Opus 5.5
  at high.

Handoff patterns:
- **GLM Flash gathers, frontier ships**, as with the other cheap tiers.
- **Pick among cheap tiers by pattern:** GLM-5.3-Flash when self-hosting or a
  Coding Plan matters; DeepSeek V4.1 Flash for cached repeated passes and long
  outputs; Gemini 3.8 Flash for speed and multimodal input; Luna for lowest
  measured cost per task.

## When this beats the frontier

- Cost-constrained general use where the frontier is unaffordable (Theo's case).
- Self-hosted or in-house deployments that cannot send code to a closed API.
- Verifiable, mechanical, high-volume text work on an API budget.

## Cost notes

- GLM-5.3-Flash: $0.15 / $0.03 / $0.50 per MTok (Z.ai docs); AA about $0.10 per
  task (unverified).
- GLM-5.3: $1.40 / $0.26 / $4.40; $2.01 per AA task at max. Not cheaper per task
  than 6.1 Sol ($0.32).
- GLM-5.3-FlashX: $0.37 / $0.075 / $1.25.
- GLM Coding Plan (unverified, third-party): Lite $18, Pro $80, Max $168 per
  month; credit-based, half credits off-peak. This is where full GLM-5.3's cost
  disappears.

## Evidence

- `research/model-gaps.md § Naming corrections` ("GLM 5.x" is now GLM-5.3),
  `§ At-a-glance comparison`, `§ 4. Open-weights models for OpenCode / Pi › How to
  run them from a terminal`, `§ 4b. GLM-5.3 and GLM-5.3-Flash (Z.ai / Zhipu)`,
  `§ Suggested routing-table shortlist` (GLM-5.3-Flash in the cheap tier; GLM-5.3
  at max excluded on cost unless on Coding Plan).
- [FVA 1:14:10](https://youtu.be/P7bxbDSnZRM?t=4450), [FVA 1:09:43](https://youtu.be/P7bxbDSnZRM?t=4183) (rule 24), [FVA 1:14:04](https://youtu.be/P7bxbDSnZRM?t=4444),
  [FVA 1:14:17](https://youtu.be/P7bxbDSnZRM?t=4457), and [FVA 1:14:10](https://youtu.be/P7bxbDSnZRM?t=4450)
  (GLM 5.3 Flash as a cheaper, more pleasant alternative to Astra).
- URLs: [Z.ai pricing docs](https://docs.z.ai/guides/overview/pricing),
  [EvoLink: GLM-5.3 release](https://evolink.ai/blog/glm-5-3-release),
  [AA open-weights page](https://artificialanalysis.ai/models/open-source),
  [AA leaderboard](https://artificialanalysis.ai/leaderboards/models),
  [Baidu Cloud article on licence](https://intl.cloud.baidu.com/en/article/8754873),
  [GLM Coding Plan guide](https://www.aieatingtheworld.com/articles/glm-coding-plan-guide-z-ai-glm-5-2),
  [Developer Puter pricing](https://developer.puter.com/tutorials/zai-glm-api-pricing/),
  [OpenCode providers](https://opencode.ai/docs/providers/).
- **Unverified:** Flash's 1M context; Flash's AA cost per task and speed; Coding
  Plan tiers and whether they include Flash; licence (bespoke vs MIT); effort
  levels for Flash specifically. Theo's "off the rails less than Astra" is one
  anecdote from one video.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 4 | AA 42 vs 54 for Opus 5.5; the full model's vendor benches are well below the frontier and Z.ai says it trails Fable 5. |
| taste | 3 | No evidence; text-only. |
| floor | 4 | Theo: goes "off the rails less than Astra" (floor 3), one anecdote; otherwise unproven. |
| thoroughness | 3 | No review or audit evidence. |
| cost_efficiency | 7 | About $0.10 per AA task (unverified) at index 42; held below Luna and MiMo because the per-task figure is unconfirmed and thinking cannot be switched off. |
| speed | 5 | Not measured for Flash; full GLM-5.3 is 74 tok/s. |
| computer_use | 1 | Text-only. |
| orchestration | 2 | No evidence; not a lead model. |
