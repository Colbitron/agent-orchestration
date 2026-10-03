# Delegation prompting

Load this before you write any prompt that leaves your context: a subagent
task, a workflow stage, a shell-out to another CLI, or a thread on another
machine. The receiver sees only what you write, cannot ask what you meant,
and you will usually read only its last message.

Citations: `research/<file>.md § V1.3` means Video 1, section 3 of that file.
`INSP` means `transcripts/general/agent-orchestration-inspiration.html`
(Theo's orchestration video, recorded when the models were Fable 5, GPT-5.5
and Opus 4.8).

---

## 1. The shape: want, done, out

Every delegated prompt has three parts. Do not dispatch a prompt missing one.

1. **What you want.** The goal, stated wide enough that the model can start
   early and go far (find the files, fix, test, verify, file the PR).
2. **What "done" means.** Concrete, checkable conditions.
3. **The out.** When the model may stop and ask instead of pushing through.

The canonical example, from Anthropic's Opus 5.5 guide
(`research/claude-supplemental.md § V1.3`):

```
Migrate the payments endpoint from the old client to the new one. Done means
every endpoint uses the new client, the old one is deleted, and the test suite
passes. Stop and ask me only if a test fails for a reason that you can't
explain.
```

The out is "what might be the most important piece": models are trained hard
not to give up, so without one they answer their own question and push on
(`research/claude-supplemental.md § V1.2`).

## 2. Done states

Write done as observable facts, not activities.

| Weak | Checkable |
|---|---|
| "Start working on the feature" | "Done means it has A, B and C, there is a screenshot of it, and a PR is up that includes the screenshot." |
| "Fix the bug" | "Done means a test reproduces the old failure and now passes, and the PR link is in your final message." |
| "Get it running on the server" | "Don't report until you have a Tailscale link I can click." |
| "Look at the PR" | "Babysit it until every check and review bot is green." |

- **"Make sure X" means do X and validate X**, and report if it fails
  (`research/claude-supplemental.md § V1.2`).
- **Prefer one-click artifacts:** PR link, screenshot, video in the PR,
  preview link, file path. Push delivery to the agent: not "tell me so I can
  build it" but "run it in the simulator, verify it, then push the build"
  (`research/model-selection.md § V1.3`).
- **Say whether to open a PR.** Theo's 60-minute run built everything and
  opened no PR because he had not asked (`research/claude-supplemental.md § V2.2`).
- **Say whether to merge.** The kit default is "propose PRs, never merge"
  (`docs/ARCHITECTURE.md`). Write a merge end state only when the user's config
  enables it.
- **Phrasings known to work:** "File the PR and tell me when it's up." "Babysit
  it till everything is green." "Merge it once you've got everything green and
  you're happy with your changes." (`research/claude-supplemental.md § V2.3`)

## 3. Branching end states

When the right path depends on what the model finds, give it the branches and
the data, not a fixed path. Either outcome then ends somewhere useful
(`research/claude-supplemental.md § V2.2`):

```
Someone is claiming their PR that we closed might be better than mine. Take a
look and see if that's the case. If so, reopen it and finish it or take the
commits and start something new. If ours is better, finish modernizing it and
get ready to go. Babysit whatever ends up being put up.
```

A question plus a conditional also works: "Do you think that's all we need?
If so, merge 28 into 200 and then merge it all the way in."

## 4. Explicit negatives

"Being explicit about what you want is great, but being explicit about what
you don't want is even better" (`research/claude-supplemental.md § V1.2`).

- **Name specific things to avoid.** "Avoid generic looks" swaps one default
  for another; a list works (`research/claude-supplemental.md § V1.3`):
  `Don't use a cream or off-white background, italic accent words in headings,
  numbered 1, 2, 3 section labels, monospace labels, or pill-shaped buttons.`
- **Operational negatives and non-goals:** "I don't want you spamming my
  machine with computer use requests"; "Don't worry about how it's hosted."
- **When it does something you dislike, add it to the list and ask again.**

## 5. Environment, connection, pre-authorisation

State where the model is and how it reaches anything outside. Pre-authorise
the sensitive actions you expect, so it neither stalls for permission nor
improvises something sketchy (`research/claude-supplemental.md § V1.2`).

- **How to connect:** "You should be able to see how to connect through the
  fleet repo on this machine." Stops it inventing a method that trips a
  security check.
- **Expected sensitive steps:** copying env vars, creating worktrees,
  rebasing, force-pushing its own branch, closing superseded PRs. Otherwise it
  "might be concerned when it goes to do that and then stop and ask me."
- **Where heavy work runs.** One run hammered Theo's home IP until told to use
  a container (`research/claude-supplemental.md § V2.8b`).
- **What is reversible.** Staging that cannot reach prod is what makes "merge
  when happy" safe (INSP; `research/claude-releases.md § V1.5`).
- **If the UI hides tool outputs, say so**, or the model will not repeat
  results it expects the UI to show (`research/claude-supplemental.md § V2.3`).
- **Attach context:** annotated screenshots, thread IDs, run links, PR
  numbers, log paths, and definitions of terms the task hinges on. Fable 5.1's
  one recorded miss read "auto-linking" too narrowly
  (`research/claude-releases.md § V1.3`).

## 6. Multi-phase and long runs

Claude models sometimes stop to report instead of continuing: "a summary that
names the next step without taking it, an offer to continue, or a list of
choices that don't actually block the work"
(`research/claude-supplemental.md § V1.4`). "Follow its phase 0 to 7 in order"
still stopped after phase 0. Theo's working follow-up
(`research/claude-supplemental.md § V1.2`):

```
I want you to hold off on all questions until the very end when you get
through to phase 7 in completion. I don't want you to stop after every phase
to ask for permission to continue. I want you to do the whole thing. Continue
working on this port until the entirety of it is completed and don't inform
me until you have a Tailscale link I can click on.
```

For an unattended worker, add Anthropic's autonomy block
(`research/claude-releases.md § V1.5`):

```
You are operating autonomously. The user is not watching in real time and
cannot answer questions mid task. So asking "want me to" or "shall I" will
block the work. Reversible actions that follow from the original request
proceed without asking. Stop only for destructive actions or genuine scope
changes the user must decide on.
```

Or the shorter named-stops rule (`research/claude-supplemental.md § V1.6`):

```
When a step doesn't need my input, keep going. Put status notes in the same
message as your next action. Stop and ask only when you can't continue without
me or before anything destructive: deleting data, force pushing, or changing
anything outside of this repo.
```

Keep the last sentence: a keep-going rule removes stops, so keep the ones
before risky steps. If a worker still ends with "Want me to continue?" and
nothing blocks it, reply `continue`. Fable may also "describe what it would do
next instead of doing it" on async work; add "Do not end your turn until the
work is complete" (`research/claude-supplemental.md § V2.3`).

## 7. Subagent grant

Opus 5.5 is reluctant to spawn subagents unless told it may
(`research/claude-supplemental.md § V1.5`). Append to every lead-agent prompt:

```
Use subagents and workflows however you choose. I trust your judgment there.
```

For work known to parallelise (PR piles, audits), say "Use subagents for
this." Pin subagent models; an Opus run spawned a Fable subagent unasked
(`research/claude-releases.md § V3.6`).

## 8. Scope control

Add to any narrowly scoped task, especially subagent tasks. Anthropic reports
it cut unrequested additions and committed test code "substantially with no
measurable change in task success" (`research/claude-supplemental.md § V2.3`):

```
If while working or testing you find pre-existing bugs, performance concerns,
or behaviors the task doesn't mention, don't fix, optimize, or extend it in
this change unless the requested behavior cannot work without it. Report it as
a follow-up in your summary.
```

Additions by situation:

- Babysit / review-response loops (Sol drifted here): `Please don't scope
  creep. Stop adding new things. Only address real shortcomings. Don't post
  filler comments.` (`research/claude-supplemental.md § V2.2`)
- GPT implementers (Astra creeps by default): `Make the smallest possible
  changes.` (`research/model-selection.md § V2.3`)
- Rewrites that carry UI over (Astra discarded UI despite "reuse as much UI
  code as possible"): `I expect the UI to be pixel perfect identical. If any of
  the UI has changed, you have failed at your goal, so keep going until the UI
  looks identical.` (`research/model-selection.md § V2.3`)
- Cap test sprawl when it matters: "add at most one test file"
  (`research/claude-releases.md § V1.5`).

## 9. Reporting: the closing recap

You usually read only the worker's last message. Fable 5.1 writes few progress
updates by default; Theo saw ~150 tool calls with no text
(`research/claude-supplemental.md § V2.3`). Anthropic's block, verbatim:

```
Before you start, say in a line what you're about to do. Brief updates while
you work help the user follow along. Close with a short recap that stands on
its own — what you found, what you did, and what's next — so a reader who only
sees the last message has the full picture.
```

For results you will parse, require the guide's headings plus a verification
line (`research/claude-supplemental.md § V1.5`):

```
End your final message with these headings, in this order:
Blocked on me: decisions or approvals you need from me (or "nothing").
Changed: what you changed, with PR links, branches, and file paths.
Found: what you learned, including follow-ups you did not act on.
Not verified: anything you claim but could not confirm, and why.
```

Read **Blocked on me** first.

## 10. Compaction hint

Claude writes its own compaction summaries and keeps what you ask it to
(`research/claude-supplemental.md § V2.3`). For any run likely to compact:

```
If your context is compacted, preserve: the task goal, the done conditions,
the constraints and negatives, the branch/worktree/PR identifiers, and any
open blockers.
```

Compaction is reliable now; do not let a worker fret about being "10% from
autocompact" (`research/claude-releases.md § V2.3`).

## 11. What not to say

- **No "think hard / deeply / carefully".** The model already sizes its own
  thinking (`research/claude-supplemental.md § V1.3`). Effort is a parameter,
  not prose (`effort-levels.md`).
- **No "show your reasoning" or "what was your reasoning".** That wording risks
  safeguard flags on Claude. Ask "Explain why you made these changes"
  (`research/claude-supplemental.md § V1.3, § V1.8b`).
- **No base64 blobs in context**; they trigger safeguards. Phrase checks as
  "Are there bugs in the program?" rather than compile-probing wording. For
  little-known languages, put the docs in context
  (`research/claude-supplemental.md § V2.3`).
- **No behavioural or formatting rules by default** ("be concise", "no
  bullets", "hold all findings for the end"). On current Claude models they
  over-correct: a 10% habit cut to 1% (`research/claude-supplemental.md § V2.3`).
  Add one only to fix an observed problem. Exception: for user-facing prose,
  `Please remove all mannered prose.` in the user message.
- **Don't micro-specify method.** Give environment and finish line. Put long
  plans in a file and point to it (`research/claude-supplemental.md § V1.3`).
- **Don't do the model's search for it.** Describe the problem and let it find
  the files; pass known locations as context, not as a fence
  (`research/model-selection.md § V1.3`, rule 8).
- **Don't edit earlier turns** of a Claude thread; it drops reasoning state
  (`research/claude-releases.md § V1.3`). Steer with a new message. Current
  models treat mid-run messages as additions, not replacements
  (`research/claude-supplemental.md § V1.3`).

## 12. Prompting GPT models vs Claude models

Claude tends to do more than asked; GPT does what the text says, or less.

| | Claude (Fable, Opus, Sonnet) | GPT (Astra, Sol) |
|---|---|---|
| Length | Context-rich: environment, negatives, permissions. | Much simpler. "Claude likes to prompt Codex as though it is Claude, which it is not" (INSP). |
| Restraint | Needs the scope-control block. | Older GPT did only what it was told (INSP), but Astra scope-creeps when implementing and Sol when babysitting. Add "smallest possible changes". |
| Follow-through | Acts on implied next steps. | Write imperatives. Asked "are any of the review comments worth addressing?", Astra said yes and changed nothing (`research/gpt-releases.md § V1.3`). Write "Fix them, push, and babysit until green." |
| Getting stuck | Asks when given an out. | Sol "follows its process rules even when they stop all progress and it does not ask for help" (`research/gpt-releases.md § V2.3`). Give an escape hatch: "If you make no progress after N attempts, stop and report what blocks you." |
| Empty results | — | "If you find nothing, say so clearly and name what you inspected." Without it, an empty result made Theo's parent model rerun (INSP). |
| Procedures | Skills are pulled in reliably. | Put the procedure in the prompt; Codex may drop a skill on later turns (`research/model-selection.md § V2.6`). |
| Trust | Normal. | Verify git/PR state yourself after it claims to have pushed or merged (`research/gpt-releases.md § V1.9`). |

**Harness note (Codex CLI).** Shell out one-shot with a self-contained prompt;
read-only sandbox for review/investigation. Commands live in `core/bridges/`.

## 13. Checklist

Goal stated wide · checkable done conditions · the out (GPT: escape hatch) ·
negatives and "don't worry about" · environment, connection, pre-authorised
actions · PR/merge policy matching config · phase instruction if phased ·
subagent grant or model pins · scope-control block for narrow tasks · closing
recap with report headings · no "think hard", no "show your reasoning", no
unmotivated style rules.

## 14. Templates by task type

Fill `<...>` slots; delete lines that do not apply. Ids are from `core/tasks.md`.
Append the §9 report block to each except `review`, which has its own.

```
--- quick-fix ---
<Problem in one or two sentences; screenshot/link.> Fix it with the smallest
change that makes it correct. Done means <behaviour> works, existing tests
pass, and <PR filed | committed on branch X>. <Scope-control block.>
Stop and ask only if the fix needs a change to <public API | schema | another package>.

--- feature ---
Build <feature> so that it <A>, <B>, <C>. Find the relevant code yourself.
Done means all three work, tests cover them, you verified them by <running it |
screenshot | video>, and a PR is up with that evidence. Then babysit the PR
until CI and review bots are green. <Merge policy.> Don't <negatives>.
You may <pre-authorised actions>. Stop and ask only if <product decision the spec doesn't answer>.

--- long-run ---
Read <plan file> in full before you start. Do every phase, 0 through <N>, in
order; don't stop between phases; hold questions until the end.
Environment: <machine, how to connect, where heavy work runs>.
You have permission to <create worktrees, rebase, branch, open PRs...>.
Mark each item in <todo.md> done as you finish it and commit that change.
Done means <artifact, e.g. all tests pass and a link I can click>; don't report
until it exists. <Autonomy block.> <Compaction hint.>
Use subagents and workflows however you choose. I trust your judgment there.
Stop and ask only if <blocker you cannot route around> or before <destructive actions>.

--- frontend ---
Build <screen/page> for <audience/purpose>. It should feel <direction; reference image>.
Don't use: <specific patterns: pill buttons, filler subtitles, all-caps labels, cream backgrounds>.
Done means it renders at <breakpoints>, you have screenshots of each, and <PR | preview link>.

--- review ---  (second-family model; uses this report, not §9)
Review <uncommitted diff | branch X vs main | PR #N | commit SHA>.
Focus: <correctness, regressions, edge cases, security>. Do not edit files.
Verify findings by running the code or tests where you can. For each finding
give file:line, what is wrong, how you confirmed it, and severity. Mark any
finding you could not confirm as UNCONFIRMED with the reason.
If you find nothing, say so clearly and name what you inspected.

--- investigate ---
<Symptom, repro steps, logs, screenshot, run link.> Find the root cause and
reproduce it before you claim it. <Do not fix it yet | Then fix it and add a
regression test.> Done means a root cause with evidence (repro, failing test,
or trace) and the file:line where it originates. List what you ruled out.
If you cannot find it after <bound>, stop and report what you tried.

--- analyze ---
<Question, e.g. how could this change be split into landable PRs?> Read
whatever you need; do not change code. Done means <plan | ranked list | map>
with file references per claim. Mark claims you could not confirm. If
something is fine, say so rather than inventing work.

--- bulk ---
Apply <transformation> to <set>. The spec is complete; there are no judgment
calls. If a case isn't covered, skip it and list it. Done means every item is
done or listed as skipped, and <tests | linter> pass.

--- research ---
Find out <question> using <docs | web | APIs>; prefer primary sources. Done
means a short report: the answer, a source link per claim, and what you could
not determine. Mark quotations as quotations.

--- computer-use ---
On <machine | simulator | browser>, open <app/URL> and <flow>. Expected:
<behaviour>. Capture a screenshot <or video> at <points>. Don't <touch other
apps | log in | submit payments>. Done means pass/fail per step, the
screenshots, and exact notes on any mismatch. If you can't reach the app, stop
and say what failed.

--- copy ---
Write <UI text | docs page> for <audience> so they can <do/know X>.
Constraints: <length, tone, terms>. No taglines, subtitles, or filler copy.
Please remove all mannered prose. Done means the text, plus one alternative
for any line you are unsure of.

--- 3d-games ---
Build <scene | mechanic>. Tools: <Blender CLI | engine>. Priority: <visual
fidelity | how it feels to control>: <controls, camera, movement targets>.
Done means it runs at <fps> and you have <screenshots | video> of <states>.

--- prompt-writing ---  (always human-audited)
Draft <skill | agent definition | prompt> for <purpose>. The description must
say when to use it and when not to. Include exact commands where it shells
out. Keep it short; no style rules. Mark anything you guessed. I will audit it.

--- babysit ---
Babysit PR <#N> until every check and review bot is green. Only act on checks
and comments newer than the latest push. Verify every bot finding against the
source before changing anything; fix real findings and CI failures. If a
finding isn't worth addressing, reply with a short written reason and resolve
it. Rebase on main when needed. Please don't scope creep: only address real
shortcomings, and don't post filler comments. If an overlapping PR makes this
one obsolete, stop, report it, and ask before closing.
<Report when green | Merge when green and you're happy.>

--- orchestrate ---
<Goal, wide.> Plan the work, then run it. Use subagents, workflows, and
worktrees however you choose; I trust your judgment. Keep working while
subagents run: test their findings and plan the next step. Subagent models:
<pins from routing table>; prefix subagent names with the model.
<Merge policy and reviewer-bot gate.> Done means <every item in todo.md done |
all PRs merged or listed with blockers>. Stop and ask only for product
decisions or destructive actions.
```
