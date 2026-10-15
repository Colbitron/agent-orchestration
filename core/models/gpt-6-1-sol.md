---
id: gpt-6-1-sol
name: GPT-6.1 Sol
vendor: openai
family: gpt
status: current
released: null                   # month not stated; about one week after GPT-6 Sol
as_of: 2026-10-02
confidence: medium               # one dedicated video; other "Sol" mentions are ambiguous between 5.6, 6.0 and 6.1

api_ids: null                    # exact API model id not stated in the research
access:
  subscriptions: [chatgpt-plus, chatgpt-pro]
  api: true
  harnesses: [codex, cursor, opencode, t3-code]   # cursor access reportedly revoked; see Evidence
  invoke_via: [codex-cli, cursor-cli, opencode-cli]

pricing_per_mtok:
  input: 2
  output: 10
  cache_read: 0.10
  cache_write: null
context_window: null             # not stated for 6.1 Sol
notes_on_cost: >
  Cache reads at $0.10 (a 95% discount) dominate: agent workloads are about
  96% cache reads, so this matters more than the $2/$10 headline. It is also
  lean, at about 110K tokens per request vs about 360K for Sonnet 5.5. On
  DeepSWE, low effort matched Opus 5.5 max at about 1/70 of the cost ($0.21
  vs $14.65 per task). It burns more tokens than Claude on audits but still
  costs less. The one cost trap is long unattended loops, which stall and burn
  tokens with no progress. On a Codex subscription the marginal cost is close
  to zero.

effort:
  levels: [low, medium, high, xhigh, max]
  default: low
  avoid: [xhigh, max]
  notes: >
    Low and high score the same on DeepSWE and xhigh/max score lower. Low is
    the cost star for scoped implementation and bulk work. Use high for review,
    investigation and anything ambiguous; it is still cheap.

scores:
  intelligence: 7
  taste: 2
  floor: 6
  thoroughness: 9
  cost_efficiency: 10
  speed: 8
  computer_use: 8
  orchestration: 4

tasks:
  quick-fix:      {fit: good, note: "cheapest strong option for scoped, specified changes; first drafts have real bugs, so keep review bots or a Claude review before merge"}
  feature:        {fit: ok,   note: "harder to justify merging than Opus code and won't ask for help when blocked; prefer Opus or Fable"}
  long-run:       {fit: poor, note: "stalls on long unattended builds (4 days, no progress on the TS-to-Rust port) and never escalates"}
  frontend:       {fit: poor, note: "'unacceptably garbage' at UI, filler copy everywhere, regressed vs earlier OpenAI models"}
  review:         {fit: best, note: "default second-family reviewer for Claude-written code; caught regressions Fable and Opus missed; ask it to mark unconfirmed findings"}
  investigate:    {fit: best, note: "root-causing, repro via code reading plus computer use, triage; escalate to Astra xhigh only if it stalls"}
  analyze:        {fit: good, note: "topped the T3 Code improvement bench (87.4) and matched Astra on an audit at half price; earlier Sol scored poorly on decomposition plans"}
  bulk:           {fit: best, note: "clear-spec, mechanical, high-volume work at the lowest cost per completed task"}
  research:       {fit: ok,   note: "no direct evidence for web/docs research; inferred from thoroughness and price"}
  computer-use:   {fit: good, note: "trusted with email triage and payment prep; cheaper default for routine flows, escalate hard flows to Astra"}
  copy:           {fit: poor, note: "filler copy 'worse than almost any' model the speaker has seen"}
  3d-games:       {fit: ok,   note: "good Blender modeling from a screenshot via CLI and strong graphics, but jank mechanics; slightly below Opus 5.5 for 3D overall"}
  prompt-writing: {fit: unknown, note: "no evidence"}
  babysit:        {fit: ok,   note: "needs explicit anti-scope-creep and no-filler-comment rules and an escape hatch; verify PR state"}
  orchestrate:    {fit: poor, note: "no evidence of leading agents; rigid process-following and no escalation make it a poor lead"}

role_hints:
  as_primary: "Primary only if the user's work is mostly review, investigation, and scoped or bulk tasks; otherwise keep a Claude driver that calls it."
  as_subagent: "Default cross-family reviewer and investigator for Claude-written code; cheap scoped implementer and routine computer-use operator."
  never_for: ["frontend, UI, or user-facing copy", "game mechanics and feel", "long unattended builds or heavy rewrites", "leading other agents", "xhigh or max effort"]
---

## Summary

GPT-6.1 Sol is the cost-efficiency leader and the best-value reviewer and
investigator in the research. It is a scoped-work model with a much steadier
floor than Astra. On DeepSWE it matched Opus 5.5 max at about 1/70 of the
cost and a tenth of the time, and it found regressions in Claude-written PRs
that Fable and Opus both missed. Its frontend output is "unacceptably
garbage", it stalls on long unattended builds without asking for help, and
its code is harder to merge than Opus's. The speaker keeps Opus 5.5 as the
implementer and has it call Sol to review, investigate and triage.

## Strengths

- **Cost per completed task.** $2 in, $10 out, $0.10 cache read. DeepSWE on
  low cost $0.21 per task, taking 4.8 minutes, vs Opus 5.5 max at $14.65 and
  50 minutes for the same score: "a tenth the time and a 70th the price."
  Re-priced, the speaker's whole session history came to $1,550 vs $5,700 at
  Opus's guessed price. ([SOL61 21:18](https://youtu.be/vu8X3YroB-w?t=1278);
  [SOL61 18:05](https://youtu.be/vu8X3YroB-w?t=1085))
- **Lean context.** About 110K tokens read per request vs about 360K for Sonnet
  5.5. "Did three rounds of work for about half the cost of Sonnet's single
  round." ([SOL61 18:58](https://youtu.be/vu8X3YroB-w?t=1138))
- **Deep review and auditing ("Rottweiler").** "Dig into a problem and shake it
  and tear it to pieces until they find every single thing wrong with it."
  - On a real T3 Code PR written by Claude Code, it found two regressions
    (blocked follow-up messages, setup progress disappearing too early) "that
    were entirely missed by Fable and by Opus", by reading the code and
    reproducing with computer use.
  - "Find opportunities to improve T3 Code": Sol 87.4, Astra 83.8, Grok 4.7
    80.7. Sol cost $2.15, Opus 5.5 $5, Sonnet 5.5 almost $9.
  - The orchestrator v2 audit was "nearly identical to Astra" at about half
    the price.
  - It found 1.3M of 1.8M lines unused after a TS-to-Rust rewrite that Opus
    had left behind.
  "I absolutely trust it to review things."
  ([SOL61 13:12](https://youtu.be/vu8X3YroB-w?t=792))
- **Steadier floor than Astra.** Asked whether it fixes Astra's spikes: "mostly,
  not entirely, but for the most part, yeah." Testers called it "incredible"
  and "incredibly boring." ([SOL61 10:51](https://youtu.be/vu8X3YroB-w?t=651))
- **Computer use good enough to trust with money.** It went through his email
  for unpaid invoices and set up a Chrome tab per wire with the details filled
  in, leaving him to click send. "It didn't get a single thing wrong." It is
  "still not quite as good as Astra" but worth it for the price.
  ([SOL61 11:29](https://youtu.be/vu8X3YroB-w?t=689))
- **Blind evaluation by Opus 5.5.** It placed first (87.4) in a blind 10-model
  bench. Opus's verdict: "incredible for scoped work, top of the frontier...
  about level with Opus." ([SOL61 15:38](https://youtu.be/vu8X3YroB-w?t=938))
- **Blender.** "If you give it like a screenshot... and say, 'you have Blender
  over the CLI, go make this,' it will." Its fish-game graphics beat Sonnet
  5.5's. ([SOL61 24:57](https://youtu.be/vu8X3YroB-w?t=1497))
- **Fast to completion.** Opus judged "its speed should add a premium because
  it is quite fast", consistent with 4.8-minute DeepSWE tasks.
  ([SOL61 17:13](https://youtu.be/vu8X3YroB-w?t=1033))

## Weaknesses and failure modes

- **Frontend and UI.** "This model is unacceptably garbage at UI. It has
  regressed again... It has no taste and you're going to have to bring your
  taste yourself." The fish game had 20+ pieces of filler copy ("take a
  breather", "Your little world can wait"), "worse than almost any I've ever
  seen." ([SOL61 24:41](https://youtu.be/vu8X3YroB-w?t=1481))
- **Game mechanics.** Movement was jank, the frame rate worse, the loop thin,
  and the game ended at random within 30 seconds. "I would never have it make
  the actual mechanics for my games." ([SOL61 25:08](https://youtu.be/vu8X3YroB-w?t=1508))
- **Stalls on long unattended builds.** On the TS-to-Rust port, "it made no
  progress. It burned a shitload of tokens." Per Opus, it "wasted 4 days."
  Opus restarted the port and got it working in a day.
  ([SOL61 16:07](https://youtu.be/vu8X3YroB-w?t=967))
- **Doesn't ask for help.** It "follows its process rules even when they stop
  all progress and it does not ask for help." The speaker: "This I absolutely
  noticed." An orchestrator cannot rely on it to escalate and must give it
  escape hatches and time or step budgets. ([SOL61 15:49](https://youtu.be/vu8X3YroB-w?t=949))
- **Merge-worthiness.** "It is harder to justify merging this code than it is
  for code from Opus." Its first drafts had real bugs that review bots caught.
  ([SOL61 27:38](https://youtu.be/vu8X3YroB-w?t=1658))
- **Edge-of-capability weirdness.** "Some tasks that are just at the edge of its
  capability that it will start to do weirder stuff on." It also made "a couple
  dumb mistakes" managing his agent fleet. ([SOL61 12:19](https://youtu.be/vu8X3YroB-w?t=739);
  [SOL61 16:50](https://youtu.be/vu8X3YroB-w?t=1010))
- **Noisy findings.** OpenAI reviewers "report more stuff that doesn't matter."
  On one review bench Sol's 9 findings were judged less valid than Astra's or
  Grok's 8 (which Sol version is unclear, see Evidence). The orchestrator or a
  Claude model should filter and verify its findings before acting.
  ([OPUSG 22:46](https://youtu.be/ejjBbaq9RmY?t=1366))
- **Scope creep and review-comment loops when babysitting.** The speaker added
  "Please don't scope creep. Stop adding new things. Only address real
  shortcomings" and "don't post filler comments" to his babysit skill because
  Sol scope-crept during babysitting. GPT-5.6 Sol bloated PRs and got stuck in
  review loops. These observations are from earlier Sol versions; keep the
  guardrails for 6.1. ([FABG 15:42](https://youtu.be/-XWSJM-Ue-o?t=942);
  [FAB51 52:06](https://youtu.be/r_dw-1109Ag?t=3126))
- **Verify git and PR state.** Astra's "says it fixed, didn't push" behaviour
  hasn't been reported for 6.1 Sol. The precaution still applies to any Codex
  run: check the remote branch, `gh pr checks` and open review threads, not the
  model's summary.
- **Skill-dropping on later turns.** Codex's system prompt says a skill used in
  one turn shouldn't apply to later turns unless requested. This was observed
  with Astra, and Sol inherits the harness. Re-invoke skills by name each turn.
  ([FVA 55:43](https://youtu.be/P7bxbDSnZRM?t=3343))
- **Lower ceiling than Astra** for computer use and 3D, and slightly below Opus
  5.5 for 3D overall. ([SOL61 11:10](https://youtu.be/vu8X3YroB-w?t=670))

## How to prompt it

- **Simpler and more literal than a Claude prompt.** "Claude likes to prompt
  Codex as though it is Claude, which it is not. The prompt should be much
  simpler." A Codex model "is not going to do things you don't tell it to,
  unlike Claude models", so leave out Claude-style guardrail essays and
  "think hard" lines, and give the target, the task and the done state.
  ([INSP 21:40](https://youtu.be/8GRmLR__OGQ?t=1300), said of
  GPT-5.5 in Codex)
- **Scope it tightly.** "Incredible for scoped work." Name the review target
  (diff, branch, PR), the question, and the output format.
- **Give it explicit escape hatches, because it won't ask for help:**
  > "If you are blocked, or a process rule stops progress, stop and report
  > what blocked you and what you tried. Do not keep retrying. Stop after
  > <N> attempts or <T> minutes without progress."
- **Be explicit about follow-through** whenever it must act, not just report:
  > "Fix them, push, and babysit until every check is green."
  The orchestrator still verifies the push.
- **Tell it to make the smallest possible change**, and in babysit loops add
  the speaker's lines: "Please don't scope creep. Stop adding new things. Only
  address real shortcomings." and "Don't post filler comments."
- **Make "nothing found" a valid, explicit answer** so the parent doesn't
  re-run it:
  > "If you find nothing, say so clearly and name what you inspected."
- **For review, ask it to mark what it could not confirm**, and give it a way
  to reproduce (tests, a running app, computer use). Its regressions were found
  "through a combination of reading the code... as well as computer use."
- **For any UI it must touch,** forbid filler:
  > "Do not add filler copy, taglines, or all-caps subtitles."
  Better still, keep UI away from it.
- **For 3D,** give a screenshot or reference plus Blender over the CLI.

## Routing guidance

**Route here for:**

- Review of Claude-written code before merge (the default second-family
  reviewer).
- Root-cause investigation, bug repro, triage ("what needs to be touched and
  why").
- Improvement sweeps, dead-code and mess detection after big rewrites.
- Scoped, well-specified implementation and bulk work where cost matters. It
  takes the slot Sonnet-tier models used to fill: "I have almost no reason to
  use Sonnet anymore."
- Routine computer use: email triage, form filling, payment prep with a human
  final click.
- Blender modeling from references.

**Do not route here for:**

- Frontend, UI, design, copy.
- Game mechanics, controls, playability. Its graphics can be handed to Claude
  to "make this play better."
- Long unattended building, heavy rewrites, multi-day loops. Use Opus 5.5 or
  Fable.
- Code meant to land without review.
- Leading other agents.
- Edge-of-capability tasks. Escalate to Opus, or to Astra for computer use
  and 3D.

**Handoff patterns:**

- **Claude builds, Sol reviews, findings are pasted back.** Opus implements,
  Sol reviews (code reading plus computer-use repro), and its findings go back
  to Claude. Claude fixes, Sol re-reviews ("better, but I'll still fix two
  small gaps"), then merge. The orchestrator should send Sol's raw findings to
  the implementer and let the implementer judge them.
- **Opus orchestrates, Sol investigates.** "Opus 5.5 can call 6.1 Sol to do
  investigation work... root cause bugs... analysis of code bases... triage...
  review the work that Opus does."
- **Sol cleans up after big rewrites.** It audits what the implementer left
  behind (1.3M dead lines after Opus's port).
- **Cheap models gather information, expensive models ship.** Sol explores and
  verifies; the work that must land moves to Opus or Fable.

**Caution for the routing generator: the naive cost router.** OpenRouter's
cost-optimizing router (transcribed as "Jev Router") sent about 60% of requests
to DeepSeek v4.1 Flash. It took 104 steps and 20 minutes per task, vs 19 steps
and 4.6 minutes for Astra low, and ended up costing more than Astra low. 6.1
Sol on low got the same score for 1/8 of the price. "A model that cannot
reason, that is given a prompt and no context, cannot make a good decision
around how hard the problem is." Route by task type and context, and count
steps-to-completion and cache-read price, not per-token list price. Sol wins
on cost because it finishes in few steps, not because it is cheap per token.
([SOL61 19:42](https://youtu.be/vu8X3YroB-w?t=1182))

## Cost notes

- **API:** $2 in, $10 out, $0.10 cache read per million tokens. That is 1/5 of
  Astra, and the cache-read price is the first change OpenAI has made there.
  Cache-write price and long-context surcharge are not stated.
- **Cache reads decide the bill.** "Agent workloads are 96% cache reads. So 10
  cents for cache reads matters more than the $2 and $10 headline prices."
  Heavy PR reviews of tens of thousands of lines cost up to about $3. Per Opus,
  "bloated system prompts barely matter anymore because of the cache pricing."
- **Long loops are still a bad idea, "but not because of money."** They stall.
- **Subscriptions.** The Codex $200 Pro plan is back, worth over $12K a month
  of inference by the speaker's estimate, vs about $8–9K on Claude Code's $200
  plan. Codex Pro tiers have no 5-hour limit, only weekly, and resets are
  frequent (8 free resets in 30 days, plus banked resets). This generosity is
  why the speaker scored a Codex model "cost 9" in his CLAUDE.md (GPT-5.5 at
  the time: "my usage there is basically infinite"). Tibo announced a usage
  accounting change that "will net out at half the dollar in API spend
  compared to the old pro $200 plan", which the speaker reads as "the start of
  the end of the subsidization era."
- **Effort for value:** low for scoped implementation and bulk; high for review
  and investigation. Never xhigh or max: they cost more and scored lower on
  DeepSWE.

## Evidence

**From the GPT-6.1 Sol video (primary; the basis of this profile):**
SOL61: "OpenAI fights back", Theo (t3.gg), YouTube, https://youtu.be/vu8X3YroB-w:
pricing, the 96% cache-read figure, DeepSWE and Terminal Bench 4 runs, the
review and audit results (87.4, the two T3 Code regressions, 1.3M dead lines),
the blind Opus evaluation, computer-use invoice story, frontend verdict, the
TS-to-Rust stall, "does not ask for help", the naive cost-router test, the
subscription figures, and the Opus-calls-Sol setup. Also ASTRA: "It's Here.", Theo (t3.gg), YouTube, https://youtu.be/XFWpf0wLbh0. Caveats:
- The transcript says "6.1 Sonnet" once, almost certainly a slip for Sol.
- "I told Soul to come in and it got it from 83.7% to 100%" is almost certainly
  Opus, per context.
- Benchmarks are the speaker's own runs, with dropped tasks and backfilled max
  results.
- Speed claims conflict: slower tokens per second than GPT-6 Sol, but fast
  task completion.
- "297 vs 584" is read as $2.97 vs $5.84, and "$512" as $5.12.

**From earlier Sol versions (not 6.1; used only for guardrails, not scores):**
- GPT-5.6 Sol: [FVA 35:18](https://youtu.be/P7bxbDSnZRM?t=2118); [FVA 54:11](https://youtu.be/P7bxbDSnZRM?t=3251); [FVA 37:36](https://youtu.be/P7bxbDSnZRM?t=2256)
  (mergeability 2–3/10, "would just get lost if you tried to
  steer it", exploratory-only rule, AA $1.99 per task);
  [ASTRA 20:02](https://youtu.be/XFWpf0wLbh0?t=1202); [ASTRA 34:09](https://youtu.be/XFWpf0wLbh0?t=2049)
  (bloated PRs, unneeded tests, yolo-merge burns);
  [FAB51 52:06](https://youtu.be/r_dw-1109Ag?t=3126); [FAB51 50:13](https://youtu.be/r_dw-1109Ag?t=3013); [FAB51 22:45](https://youtu.be/r_dw-1109Ag?t=1365)
  (scope creep, 30-minute merge loop, physics lead).
- Most likely GPT-5.6 Sol: the babysit-skill scope-creep lines in
  [FABG 15:42](https://youtu.be/-XWSJM-Ue-o?t=942). That digest maps "Soul" to 6.1, but notes the Fable video was
  recorded before Opus 5.5 shipped, which predates GPT-6 and 6.1 Sol.
- GPT-6 Sol (6.0): [OPUS55 3:29](https://youtu.be/jgGyX7MPPVg?t=209); [SON55 15:04](https://youtu.be/8WbW_n95wc4?t=904); [SON55 24:03](https://youtu.be/8WbW_n95wc4?t=1443). "GPT6 Soul" was
  released alongside Opus 5.5. The Sonnet video called it "kind of just DOA"
  and scored it "faster but at like half the score" on the decomposition
  bench. The 6.1 video says 6.0 Sol and Luna "weren't that good."
- **Ambiguous version:** [OPUSG 23:47](https://youtu.be/ejjBbaq9RmY?t=1427) (the Opus 5.5 guide video). Sol had 9 findings judged less valid on the
  review bench. The caption says "GB6 Soul", so this may be GPT-6 Sol (6.0) rather than 6.1.

**Other sources:**
- [INSP 15:00–15:53](https://youtu.be/8GRmLR__OGQ?t=900)
  ("cost in quotes of nine", said of GPT-5.5 on a Codex sub) and [INSP 21:40–22:18](https://youtu.be/8GRmLR__OGQ?t=1300)
  (prompt Codex more simply; "if Codex finds nothing, say that clearly and
  mention what the review target is").
- **Unverified:** Cursor access. The Opus 5.5 video says "OpenAI has banned
  Cursor from using their models" ([OPUS55 7:18](https://youtu.be/jgGyX7MPPVg?t=438)). `cursor` stays in `harnesses` until confirmed.
- **Not stated anywhere:** context window, cache-write price, release month,
  API model id.

### Score rationale

- **intelligence 7:** matched Opus 5.5 max on DeepSWE and topped a blind
  10-model bench. It has a lower ceiling than Astra, and it is "below
  Frontier" for long unattended building and weird at the edge of its
  capability.
- **taste 2:** "unacceptably garbage at UI", regressed, filler copy "worse
  than almost any", jank game feel, code harder to merge than Opus. Below
  Astra (4).
- **floor 6:** "mostly, not entirely" fixes Astra's spikes and was trusted to
  prep wire transfers. It still makes occasional dumb mistakes (fleet
  management) and stalls silently on long runs.
- **thoroughness 9:** "Rottweiler" reviewer, 87.4 vs Astra's 83.8, caught
  regressions Fable and Opus missed. One below Astra because findings are
  noisier and Astra is still called "the most thorough".
- **cost_efficiency 10:** $0.10 cache reads, lean context, DeepSWE parity
  with Opus max at about 1/70 the cost. It is cheapest per completed task on
  scoped work. This does not hold for long loops, which the task fits
  already exclude.
- **speed 8:** 4.8 minutes per DeepSWE task vs 50 for Opus max. Raw tokens
  per second are slower than GPT-6 Sol.
- **computer_use 8:** trusted with money and used for review repro, but "not
  quite as good as Astra" (10).
- **orchestration 4:** no evidence of it leading agents. It follows process
  rules into dead ends and doesn't ask for help, and earlier Sol "would just
  get lost if you tried to steer it."
