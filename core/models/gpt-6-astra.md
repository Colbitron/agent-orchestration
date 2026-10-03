---
id: gpt-6-astra
name: GPT-6 Astra
vendor: openai
family: gpt
status: current
released: null                   # month not stated in the research
as_of: 2026-10-02
confidence: high                 # two dedicated videos plus a head-to-head; note the verdict soured between them

api_ids: null                    # exact API model id not stated in the research
access:
  subscriptions: [chatgpt-plus, chatgpt-pro]
  api: true                      # OpenAI API and Amazon Bedrock (announced at launch)
  harnesses: [codex, cursor, opencode, t3-code]   # cursor access reportedly revoked; see Evidence
  invoke_via: [codex-cli, cursor-cli, opencode-cli]

pricing_per_mtok:
  input: 10
  output: 50
  cache_read: 1.00
  cache_write: 12.50
context_window: 1000000          # up to 1M; Codex default is reportedly ~370K
notes_on_cost: >
  List price is close to Fable, but it is the most token-efficient frontier
  model measured (about 27K tokens per Artificial Analysis task vs about 80K for
  Fable 5.1), so cost per task is roughly half of Fable's. Cache reads are $1,
  ten times Sol 6.1's, and agent workloads are mostly cache reads. Above 272K
  input on the API, input costs 2x and output 1.5x (waived in Codex). Fast mode
  is about 2x price for about 2x speed. Flex tier halves the price with no
  throughput guarantee (API only, not Codex). The real risk is death loops:
  a spiky run can burn hundreds of dollars and ship nothing. On a Codex
  subscription ($200 plan about $12K/month of inference, no 5-hour limit,
  frequent resets) the marginal cost is close to zero.

effort:
  levels: [low, medium, high, xhigh, max]
  default: high
  avoid: [max]
  notes: >
    High is the best value. xhigh and max sometimes score below high; use
    xhigh only for elusive bugs where exhaustive confirmation is the point.
    Low is strong on science tasks. Never use fast mode, and be careful with
    the Codex "ultra" button.

scores:
  intelligence: 9
  taste: 4
  floor: 3
  thoroughness: 10
  cost_efficiency: 6
  speed: 4
  computer_use: 10
  orchestration: 10

tasks:
  quick-fix:      {fit: poor, note: "intent failures on small fixes (the 'revert' incident) and scope creep by default; use Sol 6.1 or Claude"}
  feature:        {fit: ok,   note: "about 6 review follow-ups per PR vs Fable's 2; needs a Claude review gate and orchestrator-verified PR state"}
  long-run:       {fit: ok,   note: "relentless on UI-less, test-verifiable ports with goal mode and many subagents, but stalled at 82.6% on TS-to-Rust; hand the landing to Claude"}
  frontend:       {fit: poor, note: "filler copy and all-caps subtitles; destroys existing UI in rewrites; route to Fable or Opus"}
  review:         {fit: good, note: "most thorough reviewer measured, well-supported findings; Sol 6.1 is near-equal at about half the price, so Sol goes first"}
  investigate:    {fit: good, note: "escalation target at xhigh for bugs that reading the code cannot reveal; about 4x the time and tokens"}
  analyze:        {fit: best, note: "best decomposition and audit plans on the speaker's benches; slow"}
  bulk:           {fit: ok,   note: "works, but per-token price is 5x Sol 6.1 for no gain on mechanical work"}
  research:       {fit: good, note: "science and math lead; productivity connectors (Gmail, Notion) in Codex; no evidence on plain web/docs research"}
  computer-use:   {fit: best, note: "best anywhere by a wide margin, especially Codex on macOS; Sol 6.1 is the cheaper default for routine flows"}
  copy:           {fit: poor, note: "slightly better prose than Fable but spams taglines; useful only to critique Claude-written copy"}
  3d-games:       {fit: best, note: "visuals, Blender, CAD only; controls and game feel are poor, hand mechanics to Claude"}
  prompt-writing: {fit: good, note: "slightly best at self-prompting and skills, but none are good; always human-audit"}
  babysit:        {fit: poor, note: "says it will fix and doesn't, skips the push, stops polling early, drops the babysit skill on later turns"}
  orchestrate:    {fit: good, note: "unmatched swarm coordination and steering, but low floor; use for verifiable work and gate merges behind Claude review"}

role_hints:
  as_primary: "Lead for computer use, 3D, and swarm-shaped verifiable work (UI-less ports, perf audits); not a daily coding driver."
  as_subagent: "Computer-use operator, 3D/Blender builder, exhaustive reviewer and planner, elusive-bug hunter at xhigh."
  never_for: ["frontend, UI, or user-facing copy", "game feel and controls", "unverified PR babysitting or merging", "scope-sensitive minimal diffs without explicit limits", "fast mode", "max effort"]
---

## Summary

GPT-6 Astra has the highest ceiling of any model in the research, and its
floor is the lowest of the frontier models. It is the best model anywhere at
computer use, 3D (Blender, CAD, scene visuals) and swarm orchestration, and
the most thorough reviewer and planner. It is spiky, though: the same model
that overhauled Lakebed's performance with two prompts also failed a simple
"revert" and merged a broken PR. The speaker who called it "the best model
ever" at launch had "effectively churned" off it for daily coding by the
GPT-6.1 Sol video. Use it for computer use, 3D visuals and verifiable swarm
work. Do not use it for frontend, copy, game feel, or code that must land
without a Claude gate.

## Strengths

- **Computer use, by a generational margin.** OSWorld 2.0: 71.6% in about 23
  minutes on high, vs GPT-5.6 Sol's best of 65.7% in about 75 minutes. It
  downloaded about 150 pages of medical records through slow dashboards in
  15 minutes and drives Excel with the real mouse and keyboard. "If you care a
  lot about computer use, there is nothing even close."
  (`research/gpt-releases.md § Computer use: the headline strength`;
  `research/model-selection.md § 4. Head-to-head results`)
- **3D, Blender, CAD.** BenchCAD 96% for under $2, vs Fable's best of 84% at
  over $11. The speaker rates its 3D rendering 9/10 against Fable's 5/10, "the
  biggest gap of anything here."
  (`research/gpt-releases.md § 3D, Blender, and game graphics`;
  `research/model-selection.md § 4. Head-to-head results`)
- **Swarm orchestration and steering.** Unlike Fable's planned, staged
  subagents, Astra spins up subagents that message each other and fans out
  based on their updates. It tracked 40 parallel subagents on the TS-to-Rust
  port. Mid-task context injection doesn't derail it ("Astra eats this"). It
  can ask non-blocking questions while it keeps working, if the harness
  supports that. (`research/model-selection.md § 5. Subagents, orchestration,
  planning, verification, review`)
- **Delegation from very short prompts.** The Lakebed performance overhaul was
  one thread and two prompts ("Spit out some sub agents and go do it"). It
  built its own stress-test and audit tools, cut sync latency from up to 800 ms
  to under 30 ms, and Fable 5.1 judged the changes "entirely sound".
  (`research/gpt-releases.md § Swarms, sub-agents, and self-prompting (important
  for orchestration)`)
- **Thoroughness.** "Astra is still the most thorough" (Opus 5.5 video). It
  produced "by far the best plan" on the giant-PR decomposition bench. On deep
  bugs: "Astra quadruple confirms everything... if the bug is outside of what
  Fable can grasp just from reading code... Astra will find it. It'll just take
  four times longer." (`research/claude-releases.md § 3. Weaknesses, pitfalls
  and misconceptions` (Video 2); `research/claude-releases.md § 2. Strengths
  (with evidence)` (Video 3); `research/model-selection.md § GPT-6 Astra`)
- **Long sessions and compaction.** It honours context over long runs and
  compacts "in a way that continues to honor what it was doing."
  (`research/gpt-releases.md § Long-horizon work, context retention, and
  compaction`)
- **Science, math, security benchmarks.** Terminal Bench Science: Astra low
  54% for $11 vs Fable 5.1 medium 36% for $15. ExploitBench 100% even on low.
  DeepSWE 74.1% on xhigh. (`research/gpt-releases.md § Benchmarks cited from
  OpenAI's post`)
- **Token efficiency.** About 27K tokens per Artificial Analysis task vs about
  80K for Fable 5.1; $3.26 per task vs $7.60.
  (`research/model-selection.md § 7. Cost management and rate limits`)
- **Fleet and infra judgment.** "Aster is the only one that hasn't really made
  too many of those dumb mistakes" when managing his agent machines.
  (`research/gpt-releases.md § Judgment in fleet and infrastructure management`)

## Weaknesses and failure modes

- **Spiky, low floor.** "Astra at its best can do things Fable never could.
  Astra at its worst makes me question why I'm using AI to code at all." It
  failed to "center an icon in a div". Its floor reportedly dips to Gemini
  Flash level. "Astra has had the most bad model experiences I have had of any
  model this year." By the Sol 6.1 video the speaker had churned off it and
  kept Codex only for computer use. (`research/model-selection.md § 2. Models
  mentioned` (Video 1); `research/gpt-releases.md § Reliability and low
  spikiness: the key improvement over Astra`)
- **Says it will fix things, then doesn't. The orchestrator must verify git
  and PR state and not trust the report.** Asked whether review comments were
  worth addressing, it said "I would address both before merging" and changed
  nothing. Told to fix, push and babysit, it claimed everything was resolved,
  stopped monitoring early, and later fixed comments without pushing. In the
  "revert" incident it committed a machine-specific Tailscale host change,
  sent a dead link, and merged the PR after being told it hadn't made the
  change. After any Astra run the orchestrator should check the remote branch,
  `gh pr checks`, and unresolved review threads itself.
  (`research/gpt-releases.md § Instruction-following failures and passivity:
  the "babysit" story`; `research/model-selection.md § The "revert" incident
  (intent, in detail)`)
- **Review-comment loops and death loops.** "It does tend to get trapped if it
  gets enough review comments and it struggles to get out of those loops."
  Review-bot reminders bloat its context and push it off course. One prompt
  cost "a thousand dollars for it to run in a loop and not ship anything and
  then break my website." (`research/gpt-releases.md § Over-engineering and
  review loops`; `research/model-selection.md § 1. Subject and thesis` (Video 2))
- **Scope creep and over-engineering by default.** "You end up with a thousand
  line of code PR that should have been 50." About 6 follow-ups per PR vs
  Fable's 2. (`research/model-selection.md § GPT-6 Astra`)
- **Drops skills on later turns.** It ignored a loaded babysit skill for 5
  follow-ups. The speaker blames a Codex system-prompt rule that a skill used
  in one turn should not apply to later turns unless requested.
  (`research/model-selection.md § 6. Claude Code / Codex specifics`)
- **Destroys existing UI during rewrites.** It ignored "Reuse as much UI code
  as possible" on the ping.gg rewrite, with a 1M context, so this was not
  compaction. (`research/model-selection.md § GPT-6 Astra`)
- **Frontend and copy.** It added over 20 useless all-caps subtitles to a 2D
  page and used "little" 15 times on one landing page. "I straight up do not
  trust Astra with UI anything." It is about Fable 5 tier on marketing pages,
  "but it makes dumber mistakes". (`research/gpt-releases.md § Frontend and UI
  design: still worse than Anthropic`; `research/model-selection.md § GPT-6
  Astra`)
- **Game feel.** Movement "sucked and was janky". "Astra makes games that look
  better on Twitter. Fable makes games that actually feel nice to play."
  (`research/gpt-releases.md § Game feel, controls, and taste`)
- **Slow.** "This model, I'll be frank, can be slow." About 30 TPS on
  OpenRouter; exhaustive debugging takes about 4x longer than Fable.
  (`research/gpt-releases.md § Speed` (Video 1);
  `research/claude-releases.md § 2. Strengths (with evidence)` (Video 3))
- **Boundaries and refusals.** Its boundary failures are "more egregious" than
  Fable's, and it refuses more often. OpenAI's own safety numbers point the
  other way (0% honeypot falls, 2.4% computer-use misalignment). Treat as
  unresolved and keep destructive actions gated.
  (`research/model-selection.md § GPT-6 Astra`; `research/gpt-releases.md §
  Benchmarks cited from OpenAI's post`)
- **Not good at:** video editing ("all cringe and bad") or slide visual
  quality. (`research/gpt-releases.md § Slides and video editing`)
- **Harness dependence.** Async questions, Gmail/Notion plugins and much of the
  computer-use speed come from Codex. A bare API call may not reproduce them.
  (`research/gpt-releases.md § 8. Using it inside or alongside Claude Code`)

## How to prompt it

- **Simpler and more literal than a Claude prompt.** "Claude likes to prompt
  Codex as though it is Claude, which it is not. The prompt should be much
  simpler." Don't port Claude-style essays, think-hard lines or long negative
  lists into Codex prompts. State the task, the target and the done state.
  (`transcripts/general/agent-orchestration-inspiration.html` ~21:40, no
  research digest yet)
- **Give it everything it needs up front, then delegate broadly.** Tools
  (Blender CLI, computer use, plugins), access, and the goal. It does its best
  work from a short delegation such as:
  > "Spit out some sub agents and go do it."
- **Be explicit about follow-through. Imperatives, not questions.** "Are any of
  the review comments worth addressing?" gets analysis and no action. Write:
  > "Fix them, push the changes, and babysit the PR until every check and
  > reviewer is green. Do not stop at analysis. Done means the fixes are pushed
  > to the remote branch and `gh pr checks` is all green."
  Then verify that yourself.
- **Re-invoke skills by name on every follow-up turn.** Codex may drop a skill
  after the turn it was used in.
- **Tell it to make the smallest possible change**, every time scope matters:
  > "Make the smallest possible change that fixes this. Do not refactor,
  > add tests, or touch unrelated files. If you find other problems, list them
  > in your final message instead of fixing them."
- **For UI, forbid filler explicitly**:
  > "Do not add filler copy, taglines, or all-caps subtitles. Every piece of
  > visible text must be functional."
  For rewrites that touch UI: "I expect the UI to be pixel perfect identical.
  If any of the UI has changed, you have failed at your goal."
- **Steer with concrete dislikes** on taste work ("tell it what I didn't like
  and how to fix it"), not vague direction.
- **Pre-authorize in goal mode.** It may pause a goal for permission. The
  speaker had to say: "You have my permission to do whatever you need to do.
  I have you on full access for a reason. Keep going."
- **Make "nothing found" a valid answer** so the parent doesn't re-run it:
  > "If you find nothing, say so clearly and name what you inspected."
- **For review, ask it to mark what it could not confirm.** Its findings are
  thorough. Use computer use or tests to reproduce where possible.
- **The question channel.** In Codex it can ask non-blocking questions. Through
  a one-shot `codex exec` there is no one to answer, so tell it to put open
  questions in its final report.

## Routing guidance

**Route here for:**

- Computer use: browser and desktop automation, app setup, verifying a running
  app, slow dashboards. Use it as the escalation for hard flows and Sol 6.1 for
  routine ones.
- 3D visuals, Blender, CAD, scene and asset generation.
- Swarm-shaped work that a test suite can verify: UI-less ports, performance
  audits with stress testing, codebase-wide improvement passes. Pair with a
  Claude review before anything merges.
- Elusive bugs that reading the code can't explain (xhigh), after a faster
  model has tried.
- Decomposition plans and audits where plan quality beats speed.
- Science, math and security reasoning; productivity connectors in Codex.

**Do not route here for:**

- Frontend, UI, landing pages, user-facing copy.
- Game mechanics, controls, camera, feel.
- Small intent-sensitive fixes (reverts, narrow bug fixes). Use Sol 6.1 or
  Claude.
- Unattended PR babysitting or anything with merge rights without an
  independent gate.
- Rewrites that must preserve existing UI.
- Latency-sensitive work. Fast mode is not the answer.
- Any user with low frustration tolerance: "you should pay the extra money for
  Fable."

**Handoff patterns:**

- **Astra prototypes, Claude polishes.** "Make the first prototype with Astra
  to get everything roughly looking and feeling how you want-ish and then have
  Fable come in and clean it up." For games, Astra does visuals and Claude does
  interaction, camera and movement.
- **Astra death loop, rescued by Fable.** Stop the run, hand the PR to Fable:
  "Make this actually land. Clean it up. Throw away whatever doesn't belong.
  Make a new branch if that's easier."
- **Astra builds, Claude gates.** Fable reviewed the Lakebed swarm's changes
  and Astra's 26K-line V8 fork for merge-readiness and risk.
- **Claude builds, Astra verifies.** "Hey, can you have Astra verify this?"
  Claude (Fable or Opus) calls Codex for computer-use verification or a
  second-family review, then fixes and re-tests.
- **Astra critiques Claude's copy** but does not write it.

## Cost notes

- **API:** $10 in, $50 out, $1 cache read, $12.50 cache write per million
  tokens. Above 272K input, input is 2x and output 1.5x, so $20 and $75. Codex
  waives this multiplier, though bigger contexts still cost more per call.
- **Fast mode:** about 2x speed at about 2x price. Avoid. "If you're using fast
  with Astra, you're probably using Astra wrong."
- **Flex:** half price, no throughput guarantee, API only. Good for batch jobs.
- **Cost per task beats list price.** About $3.26 per Artificial Analysis task
  vs $7.60 for Fable 5.1, thanks to 27K vs about 80K tokens. On the median task
  it is cheaper than Fable. At the extremes it "can just burn usage in stupid
  ways" by looping.
- **Cache reads matter.** At $1 it charges 4x Fable 5.1 ($0.25) and 10x Sol 6.1
  ($0.10), and agentic work is mostly cache reads. That is a large part of why
  Sol 6.1 replaces it for scoped work.
- **Subscriptions.** The Codex $200 plan is worth about $12K a month of
  inference, vs about $8K for Claude's $200 plan, of which Fable can use only
  half. Codex Pro tiers have no 5-hour limit, only weekly. Resets are frequent
  (8 free resets in 30 days, plus banked resets), so the weekly limit acts like
  a 3-day limit. The speaker estimates about $8–9K a month of Astra usage on
  the $200 plan. This generosity is why he scored a Codex model "cost 9" in his
  CLAUDE.md (GPT-5.5 at the time, "my usage there is basically infinite").
  The generator should treat Astra as cheap for users on a Codex sub and
  expensive on API billing.
- **Effort for value:** high. Low for science. xhigh only for elusive bugs.

## Evidence

- `research/gpt-releases.md § Video 1: GPT-6 Astra` (all subsections): launch
  review, about $330K of the speaker's inference. Early access; he was asked
  not to use it on open-source code, so coding examples are from private
  projects.
- `research/gpt-releases.md § Reliability and low spikiness: the key
  improvement over Astra` and `§ Cross-video synthesis (for the routing table)`:
  the later re-assessment ("effectively churned", "I am entirely done using
  Astra after this model"). **This supersedes the launch verdict for daily
  coding.**
- `research/model-selection.md § Video 1` (floor and spikiness, revert,
  center-an-icon) and `§ Video 2: "Claude Fable 5.1 vs GPT-6 Astra"` (category
  head-to-head, swarms, revert incident, skill-dropping, cost and subscription
  tables).
- `research/claude-supplemental.md § 5. Subagents, orchestration, delegation,
  verification, review, model choice` (both videos): cross-family review,
  Fable calling Codex for computer use, Astra "a slightly better reviewer than
  Fable", review bench (Astra 8 supported findings). `§ 4. Pitfalls and
  misconceptions corrected` (Video 2): Astra loops and burns usage at the
  extremes.
- `research/claude-releases.md § 3. Weaknesses, pitfalls and misconceptions`
  (Video 2: "Astra is still the most thorough"; OpenAI caps context at 272K
  and models trust compaction) and `§ 2. Strengths (with evidence)` (Video 3:
  best decomposition plan, about 30 TPS).
- `transcripts/general/agent-orchestration-inspiration.html` ~15:00–15:53 ("cost
  in quotes of nine", Codex usage "basically infinite"; said of GPT-5.5) and
  ~21:40–22:18 (prompt Codex more simply; "if Codex finds nothing, say that
  clearly"). No research digest exists for this transcript yet.
- **Unverified:** Cursor access. The Opus 5.5 video says "OpenAI has banned
  Cursor from using their models" (`research/claude-releases.md § 2. Strengths
  (with evidence)`, Video 2). `cursor` stays in `harnesses` until confirmed.
- **Unverified or ambiguous:** FrontierMath figures (97.6 vs 100 contradiction);
  the "input four times higher" remark; the ~370K Codex window is the speaker's
  belief; ExploitBench high-cheaper-than-low may be a table error; OpenAI said
  the earliest snapshot's passivity was reduced, "not a removal of it."

### Score rationale

- **intelligence 9:** highest ceiling measured ("tasks that only this model can
  complete that Fable still just isn't quite capable of"). Docked from 10
  because the axis means unsupervised, and its dumb spikes undercut that.
- **taste 4:** UI around Fable 5 tier "with dumber mistakes", filler copy,
  bad game feel, scope creep, 6 vs 2 PR follow-ups. Above Sol 6.1 (2), whose
  UI regressed further.
- **floor 3:** the speaker churned off it for spikiness that reached
  "Gemini Flash" lows; the revert incident. Lowest of the frontier models.
  Sol 6.1 is 6.
- **thoroughness 10:** "still the most thorough", best decomposition plan,
  quadruple-confirms at xhigh. Sol 6.1 (9) is close but noisier.
- **cost_efficiency 6:** best tokens-per-task of the frontier tier and about
  half of Fable's cost per task. Pulled down by $1 cache reads in a
  cache-dominated workload, the 5x per-token gap to Sol 6.1, and death-loop
  runs that ship nothing.
- **speed 4:** "can be slow"; about 30 TPS; 4x longer on deep debugging. Its
  computer use is fast, but typical coding is not.
- **computer_use 10:** best anywhere, "two or three" generations ahead.
- **orchestration 10:** unmatched swarm coordination and steering. The floor
  risk is already in `floor`; the `orchestrate` task fit is `good`, not
  `best`, because owning a must-land end state needs a high floor.
