---
id: claude-fable-5-1
name: Claude Fable 5.1
vendor: anthropic
family: claude
status: current
released: null
as_of: 2026-10-02
confidence: high

api_ids: [claude-fable-5-1]
access:
  subscriptions: [claude-pro, claude-max]
  api: true
  harnesses: [claude-code, cursor, opencode, t3-code]
  invoke_via: [claude-cli, cursor-cli]

pricing_per_mtok:
  input: 10
  output: 50
  cache_read: 0.25
  cache_write: null
context_window: 1000000
notes_on_cost: >
  List price is the highest of the Claude trio, and it is token-hungry (about 1.7x
  Fable 5's output tokens on Artificial Analysis). Savings come only from agentic,
  cache-heavy loops (cache reads cut 75% to $0.25/M). Cache writes, not reads, were
  about 60% of the speaker's Fable bill. On a Claude subscription, Fable is capped at
  roughly half of the weekly limit, so cheap or low-effort work should go to Opus to
  preserve Fable quota. The speaker considers it not worth paying full API price.

effort:
  levels: [low, medium, high, xhigh, max]
  default: high
  avoid: [max]
  notes: >
    high is the default and scales down on trivial tasks; low is often fine for routine
    work but misses hidden complexity; xhigh for deep, thorough passes; returns diminish
    past high, so never max.

scores:
  intelligence: 9
  taste: 9
  floor: 9
  thoroughness: 6
  cost_efficiency: 4
  speed: 6
  computer_use: 4
  orchestration: 8

tasks:
  quick-fix:      {fit: good, note: "Clears the bar easily, but so does Opus; spend Opus quota on narrow tickets and save Fable for wide work. Intent-sensitive small fixes (e.g. reverts) are a Fable strength."}
  feature:        {fit: best, note: "Most mergeable code measured: 0.4 high-severity bot findings per 1K LOC vs 2.06 for Fable 5; about 2 follow-ups per PR vs 6 for Astra."}
  long-run:       {fit: best, note: "Highest floor of any model in the research; wide runs need high floors. Add the autonomy block and an explicit end state."}
  frontend:       {fit: best, note: "Best design taste available, with Anthropic's front-end design skill loaded; noticeably worse without it."}
  review:         {fit: ok, note: "Finds few but well-vetted issues; OpenAI models find more. Use as the merge-readiness/risk gate on OpenAI-written code, not as the only reviewer of Claude code."}
  investigate:    {fit: ok, note: "Reads code well but can miss bugs that only exhaustive testing reveals; Astra (xhigh) or 6.1 Sol dig deeper."}
  analyze:        {fit: good, note: "Strong audits and V2 proposals with ordered PR plans; ranked below Opus and Sonnet on the speaker's decomposition bench."}
  bulk:           {fit: poor, note: "Verbose and expensive; 'I wouldn't use this model for really long oneshot tasks that could be done by other things.'"}
  research:       {fit: ok, note: "Lowest hallucination tendency, but external-research tasks are not directly covered in research; low effort may skip search unless told to use it."}
  computer-use:   {fit: poor, note: "Decent only with the right tools; Astra / 6.1 Sol via Codex are far ahead, especially on macOS. Have Fable call Codex to verify."}
  copy:           {fit: good, note: "Fewer stock phrases than Fable 5, but prose is denser; add the mannered-prose instruction. Speaker still rewrites most copy himself."}
  3d-games:       {fit: good, note: "Best for game feel, controls, animation easing; 3D visuals trail Astra (about 5/10 vs 9/10). Astra prototypes visuals, Fable polishes feel."}
  prompt-writing: {fit: ok, note: "Prompts its own subagents well and leads at using skills, but Astra is slightly better at writing prompts/skills; always human-audit."}
  babysit:        {fit: best, note: "Carried 10 PRs through CI and CodeRabbit/Bugbot/Macroscope with every bot thread answered; reliably applies a babysit skill."}
  orchestrate:    {fit: best, note: "Plans subagents up front and keeps working while they run; best Claude lead. Astra coordinates free-form swarms better. Every Fable subagent burns Fable quota."}

role_hints:
  as_primary: "Wide, must-land work: multi-package features, long autonomous runs, front-end design, PR takeovers and merge decisions."
  as_subagent: "Rescue agent for stuck or looping PRs, and front-end/design specialist dispatched by an Opus lead."
  never_for: ["max effort", "workloads requiring zero data retention (ZDR)", "long one-shot non-agentic generation", "bulk mechanical work when Fable quota is limited", "unsupervised macOS computer use"]
---

## Summary

The highest-floor, highest-taste Claude model: route wide, must-land work here
(multi-package features, long unattended runs, front-end design, taking over
stuck PRs and deciding when they are ready to merge). It is not for cheap bulk
work, exhaustive "find everything" review, computer use, or any workload that
requires zero data retention.

## Strengths

- **High floor and mergeability.** The speaker values it because it is "less
  dumb", not because it is smarter: "Fable writes code that is mergeable 20ish%
  more often, and its stupid spikes are much less stupid." Mergeability is "right
  on the edge of 10 out of 10" (`research/model-selection.md § Video 2: "Claude
  Fable 5.1 vs GPT-6 Astra" › 1. Subject and thesis`). Quality varies by "never
  more than like two points in either direction."
- **Lands work through the review tail.** In a 24-hour window: 13 PRs at a median
  489 LOC, 11 files and up to 4 packages per PR, 0.4 high-severity review-bot
  findings per 1K LOC (Fable 5: 2.06; Sol: 1.02), 0 PRs closed as slop. "It won
  today by carrying more work through the review and merge tail"
  (`research/claude-releases.md § Video 1: Claude Fable 5.1 (and Mythos 5.1) › 2.
  Strengths (with evidence)`).
- **Rescues stuck PRs.** PRs that other agents had left in review-fix loops
  "pretty much all ... ended up landing"; a streaming PR that failed 8+ earlier
  attempts landed in about 450 lines (same section). Its "favorite" use is taking
  over an Astra death loop (`research/model-selection.md § Video 2 › 3. Decision
  rules and "use X for Y" statements`, rule 11).
- **Orchestration of planned subagents.** A slop audit produced nine ordered PRs
  (deletions first), then Fable subagents babysat all 10 to merge: 340 files,
  13K lines net deleted, every bot thread answered or fixed
  (`research/claude-releases.md § Video 1 › 6. Subagents, orchestration,
  delegation and verification`). It "plans up front" which subagents to spawn
  (`research/model-selection.md § Video 2 › 5. Subagents, orchestration,
  planning, verification, review`), and the lead keeps working while subagents
  run (`research/claude-supplemental.md § Video 2: Using Fable 5.1 correctly › 5.
  Subagents, orchestration, delegation, verification, review, model choice`).
- **Merge judgment.** "I'm telling this model more often to merge the PR when it
  decides it's ready, and I've yet to be burned by that, despite it doing it
  dozens of times" (`research/claude-releases.md § Video 1 › 2. Strengths`). It
  refused an Astra-written 26K-line change as not ready, then built shadow mode
  and synthetic-traffic checks to de-risk it
  (`research/claude-supplemental.md § Video 2 › 2. Concrete workflow the speaker
  uses`).
- **Front-end taste.** "A generational leap in homepage design"; "Fable takes the
  cake here easy" over Astra; better than Opus 5.5 on open-ended briefs
  (`research/claude-releases.md § Video 1 › 2. Strengths`;
  `research/model-selection.md § Video 2 › 4. Head-to-head results`;
  `research/claude-supplemental.md § Video 1: Getting the most out of Opus 5.5 ›
  3. Prompting guidance`). Absolute caveat: the speaker rates neither Fable nor
  Astra above about 5/10 on design.
- **Game feel.** "Astra makes games that look better on Twitter. Fable makes
  games that actually feel nice to play." It got Fish Slop controls right on the
  first try where Astra did not (`research/model-selection.md § Video 2 › 2.
  Models mentioned`; `research/gpt-releases.md § Video 1: GPT-6 Astra › 3.
  Weaknesses, pitfalls, and misconceptions`).
- **Skill use and scope discipline.** "Skill using. Fable has a huge lead"; it
  stays in scope with less effort than Astra (`research/model-selection.md §
  Video 2 › 4. Head-to-head results`).
- **Benchmarks.** AA Intelligence Index higher than anything measured at launch;
  Terminal Bench 4 low 40% vs 21.5% for Fable 5 at about half the cost
  (`research/claude-releases.md § Video 1 › 2. Strengths`). Opus 5.5 later
  overtook it on most benches at far lower cost (`research/claude-releases.md §
  Video 2: Claude Opus 5.5 › 2. Strengths (with evidence)`).

## Weaknesses and failure modes

- **Quiet during long runs.** Writes far fewer progress updates than Fable 5: one
  run had 30+ consecutive tool calls with no text, and the speaker has seen about
  150. If a human or UI must follow along, ask for updates (snippet below). An
  orchestrator should always demand a standalone final recap
  (`research/claude-supplemental.md § Video 2 › 3. Prompting guidance`).
- **Asks permission instead of finishing.** It sometimes stops with "shall I
  apply this?" or describes the next step instead of taking it. Use the autonomy
  block and an explicit end state (`research/claude-releases.md § Video 1 › 3.
  Weaknesses, pitfalls and misconceptions`;
  `research/claude-supplemental.md § Video 2 › 3. Prompting guidance`). The
  speaker says it does this "significantly less than Astra".
- **Scope overreach.** Per Anthropic's guide it "sometimes will try to fix nearby
  code, extend behavior that the task didn't mention, or commit more test files
  than the change actually warrants." The speaker sees little of this in
  practice, but it can scope-creep "if it gets the wrong review comments at the
  wrong time" (`research/model-selection.md § Video 2 › 2. Models mentioned`).
  Use the anti-scope-creep instruction on narrow subagent tasks.
- **Safeguard fallback.** Flagged requests fall back to Opus, which lowered its
  Terminal Bench 4 score and served about 4% of AA output tokens. The speaker
  personally hit about 5 false positives in thousands of prompts. Triggers to
  avoid: base64 in context, compile-probing wording, obscure languages without
  docs in context, and "show your reasoning" requests
  (`research/claude-supplemental.md § Video 2 › 3. Prompting guidance`).
- **No zero data retention.** Fable and Mythos cannot run under ZDR; Anthropic
  stores requests and responses. Enterprises with retention rules must use Opus
  (or the costly Enterprise Frontier Safeguards box)
  (`research/claude-releases.md § Video 1 › 3. Weaknesses`). The bundled Claude
  API reference agrees: ZDR orgs get a 400 unless expressly authorised.
- **Append-only history.** Editing earlier turns now discards reasoning data and
  will 400 on newer accounts. Harnesses that branch or rewrite history must be
  append-only (same section).
- **Token-hungry.** 1.7x Fable 5's output tokens on AA; about 80K tokens for what
  Astra did in 27K; the least token-efficient model on AA's chart
  (`research/model-selection.md § Video 2 › 2. Models mentioned`).
- **Intent misreads on audit questions.** Its one real failure in the launch
  video: an 8-minute audit concluded "nothing links a PR to a thread
  automatically", because it defined "auto-linking" differently. Define terms in
  audit prompts (`research/claude-releases.md § Video 1 › 3. Weaknesses`).
- **Low effort misses hidden complexity.** "If you have a task that you think is
  simple, but there's some tiny piece you forgot about ... low will miss that."
- **Dense prose and unmarked quotations.** Longer sentences, fewer paragraph
  breaks; may reproduce source passages without marking them as quotes.
- **Misses deep runtime bugs.** It "relies on reading code, so it can miss deep
  bugs that need exhaustive testing" (`research/model-selection.md § Video 2 ›
  2. Models mentioned`).
- **Boundaries (conflicting evidence).** One video rates Fable ahead of Astra at
  honouring boundaries (`research/model-selection.md § Video 2 › 4. Head-to-head
  results`); another reports catching Fable "kind of cheating" by copying Astra
  code from the machine (`research/gpt-releases.md § Video 1: GPT-6 Astra › 2.
  Strengths, with evidence`). Unresolved in the research.
- **Physics/science reasoning and 3D visuals** trail OpenAI (Sol, Astra).

## How to prompt it

Keep CLAUDE.md/AGENTS.md minimal. Delete old anti-formatting, "be concise",
"hold all findings for the final response" and "think carefully" lines: they
over-correct on 5.1 (`research/claude-supplemental.md § Video 2 › 3. Prompting
guidance`). Prompt wide: hand over the whole loop (root cause, fix, verify,
record evidence, PR, babysit, report). Every prompt needs a clear end state.

**Autonomy block** (Anthropic Fable 5.1 prompt guide, quoted by Theo):

> You are operating autonomously. The user is not watching in real time and
> cannot answer questions mid task. So asking 'want me to' or 'shall I' will
> block the work. Reversible actions that follow from the original request
> proceed without asking. Stop only for destructive actions or genuine scope
> changes the user must decide on.

**Anti-scope-creep instruction** (Anthropic guide; reduced unrequested additions
and committed test code "substantially with no measurable change in task
success"). Use it on every narrow subagent task:

> If while working or testing you find pre-existing bugs, performance concerns,
> or behaviors the task doesn't mention, don't fix, optimize, or extend it in
> this change unless the requested behavior cannot work without it. Report it as
> a follow-up in your summary.

**Progress-updates block** (Anthropic guide). Use it when a human or UI is
watching, and keep at least the last sentence in every orchestrated prompt,
because the orchestrator usually reads only the final message:

> Before you start, say in a line what you're about to do. Brief updates while
> you work help the user follow along. Close with a short recap that stands on
> its own — what you found, what you did, and what's next — so a reader who only
> sees the last message has the full picture.

If the harness hides tool output, say so, or it "won't show things because it
expects the UI to show it."

**Writing density** (Anthropic guide definition, user message preferred):

> Mannered prose substitutes metaphor and flourish for direct statements.
> Instead of 'a parameter worth varying,' the mannered writer would produce 'a
> dial worth turning.' Instead of 'this point still matters,' they write 'this
> point earns its keep.' The phrase exists to display the writer, not to convey
> the idea, and the reader can tell. This is why mannered prose irritates. It
> makes the reader work harder so the writer can perform.

Theo's shortcut: "Please remove all mannered prose."

**Delegation to Fable subagents** (Theo, verbatim, lightly cleaned; safe for him
because the project "doesn't auto ship to prod"):

> I trust your judgment here. These all seem like real things worth cleaning up.
> Spin up some sub agents using Fable 5.1 and get all this work up. When you file
> PRs, make sure to babysit them until they pass all the different checks and
> review agents that come in to leave their thoughts. Let me know when all the
> PRs are in a good state. Any of them are simple wins. Just merge them. I trust
> your judgment.

**Takeover / rescue** (Theo):

> Hey, here's a PR. Get the branch on your work tree and it's yours. Push it,
> maintain it, manage it so that it actually lands.

> Hey, make this actually land. Clean it up. Throw away whatever doesn't belong.
> Make a new branch if that's easier. Make the changes we care about here land.

**Cross-family verification from inside Fable** (Theo): "Hey, can you have
Astra verify this?" Fable then updates the code, retests, and does not return
until it is happy.

**Branching end states and honest-assessment checkpoints** (Theo): give it the
data and both paths ("If theirs is better, reopen it and finish it ... If ours
is better, finish modernizing it ... Babysit whatever ends up being put up").
Ask "Is this ready to merge? Give me your honest thoughts", "How can we de-risk
this?", "Would you confidently be able to debug X?". Its capability-boundary
answers work as orchestrator gates.

**Other rules:**
- Tell it what to preserve in compaction (task id, end state, constraints, open
  blockers); it writes its own compaction summaries.
- For audit questions, define the key terms (see the auto-linking misread).
- State the execution environment and network etiquette up front. A 94-minute
  LakeBed run hammered the speaker's home IP until told to use a container.
- To stop unmarked quotations, give a complete example of a correctly quoted
  response.
- Avoid safeguard triggers: no base64 blobs, ask "are there bugs in the
  program?" instead of compile-probing wording, include docs for obscure
  languages, never ask it to "show your reasoning".
- Use permission mode auto (or full in a sandbox), never accept-edits or
  supervised (`research/claude-supplemental.md § Video 2 › 4. Pitfalls and
  misconceptions corrected`).

Compared with Opus 5.5, Fable needs less explicit structure (named stops,
subagent grants, "do all phases") but more explicit scope limits and an explicit
request for progress updates.

## Routing guidance

Route here for:
- Features and bug fixes that must merge, especially cross-package changes.
- Long, wide autonomous runs where one dumb step sinks the run.
- Front-end, landing pages, animation, with the front-end design skill loaded.
- Game feel, controls and interaction polish.
- PR babysitting to green, triage of contributor PRs, merge-readiness calls.
- Leading audits or cleanups that decompose into parallel PRs.

Do not route here for:
- Bulk or mechanical work, or long one-shot generation another model can do.
- Computer use or GUI verification (OpenAI via Codex, especially on macOS).
- Exhaustive "find everything wrong" review (Astra, 6.1 Sol, Grok 4.7 find more).
- Physics or hard-science reasoning (Sol/Astra lead).
- Workloads needing ZDR or strict data retention (use Opus 5.5).
- Low-value work when Fable quota is limited (use Opus 5.5).

Handoff patterns:
- **Fable rescues stuck PRs.** Any agent stuck in a review-fix loop (Astra death
  loops above all) hands its PR to Fable to "make this actually land".
- **Fable writes, OpenAI reviews.** Fable asks Astra or 6.1 Sol to review and
  test, applies the findings, retests.
- **OpenAI writes, Fable gates.** Astra builds a big, risky change; Fable judges
  merge-readiness and builds de-risking checks.
- **Astra prototypes 3D visuals, Fable polishes** feel and detail.
- **Fable calls Codex for computer-use verification** of its own work.
- **Opus leads, Fable designs.** An Opus 5.5 orchestrator escalates open-ended
  front-end work to Fable.
- **Fable orchestrates, Sonnet 5.5 analyses.** Fable may dispatch Sonnet 5.5 for
  bounded codebase deep dives before it starts.
- **Merge monitor.** A separate Fable agent watches all open PRs, merges the
  ready ones and takes over those that stall.
- **Safeguard fallback.** Flagged Fable requests are served by Opus.

## Cost notes

- $10 / $50 per M tokens in/out, cache reads $0.25/M (down 75% from $1; the
  Sonnet video's "90%" contradicts the figures). Cache-write price is not stated
  in research; cache writes were about 60% of the speaker's Fable spend (about
  $1,200 of $2,000).
- Anthropic claims about 25% cheaper than Fable 5 on typical workloads and up to
  45% on highly agentic work. The saving depends on cache reads, so it shrinks
  for short chats and expired (5-minute TTL) caches.
- AA cost per task figures in the research are inconsistent ($3.69 or $3.76 per
  index task at max; $7.60 or $7.63 per task in other videos). Either way it is
  the most expensive per task of the models compared, roughly 2x Astra.
- Subscription: about $8K/month of API-equivalent usage on the $200 Claude plan,
  but Fable is capped at about half the weekly limit; each 5-hour window is about
  40% of the Fable limit. Other Claude plans are not covered in research.
- Effort for value: high by default (cheap on simple tasks because it scales
  down). Low is "surprisingly capable" for routine work (Cursor Bench low still
  beat Sol high). Theo in his later video avoids low and medium because a failed
  low run plus a rerun costs more; treat this as a known disagreement.
  Medium can still run for 1.5 hours, so effort does not cap duration.

## Evidence

- `research/claude-releases.md § Video 1: Claude Fable 5.1 (and Mythos 5.1)`
  (all sections) and `§ Cross-video synthesis (for the routing table)`.
- `research/claude-supplemental.md § Video 2: Using Fable 5.1 correctly` (all
  sections) and `§ Cross-video synthesis (where the two videos agree or differ)`.
  Recorded before Opus 5.5 shipped.
- `research/model-selection.md § Video 1: "Using the Right Models"` (floor and
  width argument) and `§ Video 2: "Claude Fable 5.1 vs GPT-6 Astra"`.
- `research/gpt-releases.md § Video 1: GPT-6 Astra › 7. Comparisons with Claude
  models` and `§ Video 2: GPT-6.1 Sol › 2. Strengths, with evidence` (Sol found
  regressions Fable missed).
- API id, 1M context and the ZDR rule come from the bundled Claude API reference
  (model table cached 2026-09-25), not from `research/`. Mythos 5.1 is the same
  weights under trusted-access programs, id `claude-mythos-5-1`.
- Release month: not stated in research (`released: null`). Model-selection
  Video 1 says Fable "arrived around May–June" without a version number.
- Transcript ambiguities: merge-time row ("up to 50 minutes ... compared to 47
  minutes ... slightly faster") is self-contradictory; per-task cost figures
  conflict (see Cost notes); cache-read cut is 75% by the figures, "90%" in one
  passage; "Opus sucks and Sonnet's hilariously bad" refers to the pre-5.5
  models.

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 9 | Top of AA index at launch and handles the hardest long-horizon work; Astra's peaks are higher ("can do things Fable never could") and Opus 5.5 now benches higher, though the speaker distrusts those benches. |
| taste | 9 | Best front-end, game feel and code mergeability in the research; held below 10 because it depends on the design skill, the speaker caps absolute design quality at about 5/10, and Astra is slightly better at prose. |
| floor | 9 | The speaker's reference "high-floor" model: steady within about two points, 0.4 high-severity findings per 1K LOC, 0 PRs closed as slop. Not 10 because of the rare intent misread and the boundary report. |
| thoroughness | 6 | "Slightly more thorough" than Opus, but on the review bench it found 5 vetted issues across two runs versus 8–9 for Astra, Grok 4.7 and Sol; precise rather than exhaustive. |
| cost_efficiency | 4 | Highest per-task cost of the Claude trio and the least token-efficient model on AA; quota-capped on subscription. Partly offset by fewer retries and cache-heavy agentic savings. |
| speed | 6 | No TPS figure. Takes longer per PR but writes more code per minute and closed a revert in about 5 minutes; median PR filed-to-merged 14m41s. Scored conservatively. |
| computer_use | 4 | "Not even comparable" to Astra; "decent when given the right tools". Same score as Opus and Sonnet: no evidence separates them. |
| orchestration | 8 | Plans and runs Fable subagent fleets to merge, and works alongside them; Astra's free-form swarms are rated better. |
