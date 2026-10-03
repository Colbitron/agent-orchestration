# Delegation prompting

Load this before you write any prompt that leaves your context: a subagent
task, a workflow stage, a shell-out to another model's CLI, or a fresh thread
on another machine. The receiving model sees only what you write. It cannot
ask you what you meant mid-run, and you will usually read only its last
message.

Citations: `research/<file>.md § V1.3` means Video 1, section 3 of that file;
`§ X` means its cross-video synthesis. `INSP` means
`transcripts/general/agent-orchestration-inspiration.html` (Theo's orchestration
video, recorded when the models were Fable 5, GPT-5.5 and Opus 4.8).

---

## 1. The shape: want, done, out

Every delegated prompt has three parts. Do not dispatch a prompt that is
missing one.

1. **What you want.** The goal in plain words, wide enough that the model can
   start early and go far (find the files, fix, test, verify, file the PR).
2. **What "done" means.** Concrete, checkable conditions. The task is not done
   until each one holds.
3. **The out.** When the model may stop and ask instead of pushing through.

The canonical example, from Anthropic's Opus 5.5 guide
(`research/claude-supplemental.md § V1.3`):

```
Migrate the payments endpoint from the old client to the new one. Done means
every endpoint uses the new client, the old one is deleted, and the test suite
passes. Stop and ask me only if a test fails for a reason that you can't
explain.
```

Why the out matters: current models are trained hard not to give up. Without
an explicit out they answer their own question and push on. With one, they
stop when they are actually confused (`research/claude-supplemental.md § V1.2`).
Theo calls it "what might be the most important piece".

## 2. Done states

Write done as observable facts, not activities.

| Weak | Checkable |
|---|---|
| "Start working on the feature" | "Done means the feature has A, B and C, there is a screenshot of it, and a PR is up that includes the screenshot." |
| "Fix the bug" | "Done means the root cause is fixed, a test reproduces the old failure and now passes, and the PR link is in your final message." |
| "Get it running on the server" | "Don't report until you have a Tailscale link I can click." |
| "Look at the PR" | "Babysit it until every check and review bot is green." |

Rules:

- **"Make sure X" means do X and validate X.** Use it when you want the model
  to confirm the step worked and tell you if it did not
  (`research/claude-supplemental.md § V1.2`).
- **Prefer artifacts a human can check in one click:** PR link, screenshot,
  video in the PR, deployed preview link, a file path. "Tell it to throw a
  video in the pull request so you know it worked"
  (`research/model-selection.md § V1.3`).
- **Push delivery to the agent.** Not "tell me when it's done so I can build
  it", but "run it in the simulator, verify it, then push the build"
  (`research/model-selection.md § V1.3`).
- **Say whether to open a PR.** Theo's 60-minute run built everything and
  opened no PR because he had not asked (`research/claude-supplemental.md § V2.2`).
- **Say whether to merge.** The kit default is "propose PRs, never merge"
  (`docs/ARCHITECTURE.md`). Only write a merge end state when the user's config
  enables it.

End-state phrasings known to work (`research/claude-supplemental.md § V2.3`):

```
File the PR and tell me when it's up.
Babysit it till everything is green.
Wait till it's green, then merge it.
Merge it once you've got everything green and you're happy with your changes.
```

## 3. Branching end states

When the right path depends on what the model finds, give it the branches and
the data, not a fixed path. Either outcome then ends somewhere useful.

```
Someone is claiming their PR that we closed might be better than mine. Take a
look and see if that's the case. If so, reopen it and finish it or take the
commits and start something new. If ours is better, finish modernizing it and
get ready to go. Babysit whatever ends up being put up.
```

(`research/claude-supplemental.md § V2.2`.) The question-plus-conditional form
also works: "Do you think that's all we need? If so, merge 28 into 200 and
then merge it all the way in." A branch is a complete end state, not "report
back and I'll decide", unless reporting back is what you want.

## 4. Explicit negatives

"Being explicit about what you want is great, but being explicit about what
you don't want is even better" (`research/claude-supplemental.md § V1.2`).

- **Name the specific things to avoid.** A general negative ("avoid generic
  looks") swaps one default for another. A list works:
  ```
  Don't use a cream or off-white background, italic accent words in headings,
  numbered 1, 2, 3 section labels, monospace labels, or pill-shaped buttons.
  ```
  (`research/claude-supplemental.md § V1.3`.)
- **Name operational negatives.** "I don't want you spamming my machine with
  computer use requests and browser control while I'm using it."
- **Name what not to worry about**, so the model does not spend effort there:
  "Don't worry about how it's hosted. Don't worry about how it's built."
- **When the model does something you dislike, add it to the list and ask
  again** (`research/claude-supplemental.md § V1.2`).

## 5. Environment, connection, and pre-authorisation

State the environment the model is in and how it reaches anything outside it.
Pre-authorise the sensitive actions you expect it to need, so it neither
stalls for permission nor improvises something sketchy.

- **How to connect:** "You should be able to see how to connect through the
  fleet repo on this machine." This stops the model from inventing a
  connection method that trips a security check
  (`research/claude-supplemental.md § V1.2`).
- **Pre-authorise expected sensitive steps:** copying env vars, creating
  worktrees, rebasing, force-pushing its own branch, closing superseded PRs.
  If you do not, it "might be concerned when it goes to do that and then stop
  and ask me."
- **Execution and network etiquette.** One long run hammered Theo's home IP
  until told to use a container (`research/claude-supplemental.md § V2.8b`).
  Say where heavy work runs: container, staging, remote box.
- **Say what is reversible.** Staging that cannot reach prod is what makes
  "merge when happy" safe (INSP; `research/claude-releases.md § V1.5`).
- **If your UI hides tool outputs, say so.** Otherwise the model will not
  repeat results it expects the UI to show (`research/claude-supplemental.md § V2.3`).

## 6. Multi-phase and long runs

Claude models sometimes stop to report instead of continuing: "a summary that
names the next step without taking it, an offer to continue, or a list of
choices that don't actually block the work"
(`research/claude-supplemental.md § V1.4`). A prompt that said "Follow its
phase 0 to 7 in order" still stopped after phase 0. For any plan with phases,
say all of this:

```
Do every phase, 0 through N, in order. Don't stop between phases to ask
permission to continue. Hold all questions until the very end. Don't report
until <concrete artifact> exists.
```

Theo's working follow-up, verbatim (`research/claude-supplemental.md § V1.2`):

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

Or the shorter "named stops" rule (`research/claude-supplemental.md § V1.6`):

```
When a step doesn't need my input, keep going. Put status notes in the same
message as your next action. Stop and ask only when you can't continue without
me or before anything destructive: deleting data, force pushing, or changing
anything outside of this repo.
```

Keep the last sentence. A keep-going rule removes stops, so you must keep the
ones before risky or irreversible steps. If a worker still ends with "Want me
to continue?" and nothing actually blocks it, reply `continue`.

## 7. Subagent grant

Opus 5.5 is reluctant to spawn subagents unless told it may
(`research/claude-supplemental.md § V1.5`). Append to every lead-agent prompt:

```
Use subagents and workflows however you choose. I trust your judgment there.
```

When the task is known to parallelise (a pile of PR reviews, a codebase audit,
a migration across many packages), do not leave it to judgment: "Use subagents
for this." Pin the subagent model when cost matters; an Opus run once spawned
a Fable subagent unasked and inflated its cost
(`research/claude-releases.md § V3.6`). See `parallelism.md`.

## 8. Scope control

Add this block to any narrowly scoped task, especially subagent tasks. Anthropic
reports it cut unrequested additions and committed test code "substantially
with no measurable change in task success"
(`research/claude-supplemental.md § V2.3`):

```
If while working or testing you find pre-existing bugs, performance concerns,
or behaviors the task doesn't mention, don't fix, optimize, or extend it in
this change unless the requested behavior cannot work without it. Report it as
a follow-up in your summary.
```

Additions by situation:

- Babysitting or review-response loops (Sol drifted here):
  `Please don't scope creep. Stop adding new things. Only address real
  shortcomings. Don't post filler comments.`
  (`research/claude-supplemental.md § V2.2`)
- GPT implementers (Astra creeps by default): `Make the smallest possible
  changes.` (`research/model-selection.md § V2.3`)
- Rewrites that carry UI over (Astra discarded the UI despite "reuse as much
  UI code as possible"): `I expect the UI to be pixel perfect identical. If any
  of the UI has changed, you have failed at your goal, so keep going until the
  UI looks identical.` (`research/model-selection.md § V2.3`)
- Limit test-file sprawl explicitly when it matters ("add at most one test
  file") (`research/claude-releases.md § V1.5`).

## 9. Reporting: the closing recap

You, the orchestrator, usually read only the worker's last message. Fable 5.1
writes few progress updates by default; Theo saw about 150 tool calls with no
text (`research/claude-supplemental.md § V2.3`). Always require a closing recap
that stands on its own. Anthropic's block, verbatim:

```
Before you start, say in a line what you're about to do. Brief updates while
you work help the user follow along. Close with a short recap that stands on
its own — what you found, what you did, and what's next — so a reader who only
sees the last message has the full picture.
```

For headless workers, keep only the last sentence. For results the
orchestrator will parse, require the guide's three headings
(`research/claude-supplemental.md § V1.5`) plus a verification line:

```
End your final message with these headings, in this order:
Blocked on me: decisions or approvals you need from me (or "nothing").
Changed: what you changed, with PR links, branches, and file paths.
Found: what you learned, including follow-ups you did not act on.
Not verified: anything you claim but could not confirm, and why.
```

Read **Blocked on me** first, then the rest
(`research/claude-supplemental.md § V1.5`). Add `Not verified` to every review
and investigation prompt (see `verification-and-review.md`).

## 10. Compaction hint

For any run likely to compact, name what must survive. Claude writes its own
compaction summaries and will keep what you ask for
(`research/claude-supplemental.md § V2.3`):

```
If your context is compacted, preserve: the task goal, the done conditions
above, the constraints and negatives, the branch/worktree/PR identifiers, and
any open blockers.
```

Do not lower compaction thresholds to save money; more compaction means more
cache rewriting (`research/claude-supplemental.md § V2.4`). Do not let a worker
spend effort on context anxiety ("10% from autocompact... work would be
lost"); compaction is reliable now (`research/claude-releases.md § V2.3`).

## 11. What not to say

- **No "think hard / think deeply / think carefully".** The model already
  reasons and sizes its own thinking (`research/claude-supplemental.md § V1.3`).
  Effort is set by parameter, not prose (`effort-levels.md`).
- **No "show your reasoning" or "what was your reasoning".** Reasoning-extraction
  wording risks safeguard flags on Claude. Ask "Explain why you made these
  changes" instead (`research/claude-supplemental.md § V1.3, § V1.8b`).
- **No base64 blobs in context.** They trigger safeguards
  (`research/claude-supplemental.md § V2.3`).
- **Phrase checks as quality questions.** "Are there bugs in the program?"
  rather than compile-probing wording. For little-known languages, put the
  docs in context so the model does not try to reverse-engineer a binary
  (`research/claude-supplemental.md § V2.3`).
- **No behavioural or formatting rules by default** ("be concise", "no
  bullets", "no bold", "hold all findings for the end"). On current Claude
  models they over-correct: a 10% habit cut to 1%
  (`research/claude-supplemental.md § V2.3`). Add one only to fix an observed
  problem. Exception: for user-facing prose, `Please remove all mannered
  prose.` in the user message is cheap and safe.
- **Don't micro-specify method.** Give the environment and the finish line;
  leave the path to the model. Put long plans in a file and point to it
  (`research/claude-supplemental.md § V1.3`).
- **Don't do the model's search for it.** Describe the problem and let it find
  the files. Pass along locations you already know as context, not as a fence
  (`research/model-selection.md § V1.3`, rule 8).
- **Don't edit earlier turns** of a Claude thread you are steering. It drops
  reasoning continuity (`research/claude-releases.md § V1.3`). Steer with a new
  message instead.

## 12. Context worth including

- Screenshots of the bug or the bad UI, annotated if possible. "I don't copy
  paste the error. I just screenshot the browser and paste that"
  (`research/claude-supplemental.md § V1.3`).
- Thread IDs, run links, PR numbers, log paths the model can read itself.
- Definitions of any term the task hinges on. Fable 5.1's one recorded miss was
  reading "auto-linking" narrower than intended (`research/claude-releases.md § V1.3`).
- The user's glossary terms (intelligence, taste, floor, wide), which the
  adapters load at session start.

## 13. Prompting GPT models vs Claude models

Claude models tend to do more than asked. GPT models tend to do exactly what
the text says, and sometimes less. Prompt them differently.

| | Claude (Fable, Opus, Sonnet) | GPT (Astra, Sol, older GPT) |
|---|---|---|
| Length | Context-rich: environment, negatives, permissions. | Much simpler. "Claude likes to prompt Codex as though it is Claude, which it is not" (INSP). |
| Restraint | Needs scope-control block. | Usually does only what it is told (INSP), but Astra scope-creeps in implementation and Sol in babysit loops. Add "smallest possible changes" for implementers. |
| Follow-through | Usually acts on implied next steps. | Write imperatives. A question gets analysis, not action: Astra said both review comments were valid and changed nothing (`research/gpt-releases.md § V1.3`). Write "Fix them, push, and babysit until green", not "Are these worth addressing?" |
| Getting stuck | Asks when given an out. | Sol "follows its process rules even when they stop all progress and it does not ask for help" (`research/gpt-releases.md § V2.3`). Give a concrete escape hatch: "If you make no progress for N attempts, stop and report what blocks you." |
| Empty results | — | State the nothing-found case: "If you find nothing, say so clearly and name what you inspected." Without it, an empty result confused Theo's parent model into rerunning (INSP). |
| Report back | Closing recap block. | Ask for a plain list; keep it in the prompt, not a skill, since Codex may drop a skill on later turns (`research/model-selection.md § V2.6`). |
| Trust | Normal. | Verify git/PR state yourself after any GPT run that claims to have pushed or merged (`research/gpt-releases.md § V1.9`). |

Theo's example of an appropriately simple Codex review prompt was shown on
screen but not read out (INSP). The template in §15 (`review`) follows the
same idea.

**Harness note (Codex CLI).** Shell-outs go through the CLI's one-shot
non-interactive mode with a self-contained prompt; use a read-only sandbox for
review and investigation. Exact commands live in `core/bridges/`, not here.

## 14. Assembly checklist

Before dispatching, confirm the prompt has:

- [ ] Goal, stated wide.
- [ ] Done conditions that a third party could check.
- [ ] The out (or, for GPT, an escape hatch).
- [ ] Negatives and "don't worry about".
- [ ] Environment, connection method, and pre-authorised actions.
- [ ] Merge/PR policy matching the user's config.
- [ ] Phase instruction if the plan has phases.
- [ ] Subagent grant (lead agents) or subagent model pin.
- [ ] Scope-control block (narrow tasks).
- [ ] Closing recap requirement with the report headings.
- [ ] Nothing that says "think hard", "show your reasoning", or a style rule
      you have not seen a reason for.

## 15. Templates by task type

Fill the `<...>` slots. Delete lines that do not apply. Task ids are from
`core/tasks.md`. Append §9's report block to every template unless noted.

**quick-fix**
```
<Problem in one or two sentences; screenshot/link if any.>
Fix it with the smallest change that makes it correct.
Done means: <behaviour> works, existing tests pass, and <PR is filed / change
is committed on branch X>.
<Scope-control block.>
Stop and ask only if the fix needs a change to <public API / schema / another package>.
```

**feature**
```
Build <feature> so that it <A>, <B>, <C>. Find the relevant code yourself.
Done means: all three work, tests cover them, you have verified them by
<running it / screenshot / video>, and a PR is up that includes the evidence.
Then babysit the PR until CI and the review bots are green. <Merge policy.>
Don't <negatives>. You may <pre-authorised actions>.
Stop and ask only if <a product decision the spec doesn't answer>.
```

**long-run**
```
Read <plan file> in full before you start. Do every phase, 0 through <N>, in
order. Don't stop between phases; hold questions until the end.
Environment: <machine, how to connect, where heavy work runs>.
You have permission to <create worktrees, rebase, branch, open PRs...>.
Mark each item in <todo.md> done as you finish it and commit that change.
Done means: <final artifact, e.g. all tests pass and a link I can click>.
Don't report until that exists. <Autonomy block.> <Compaction hint.>
Use subagents and workflows however you choose. I trust your judgment there.
Stop and ask only if <a blocker you cannot route around> or before <destructive actions>.
```

**frontend**
```
Build <screen/page> for <audience/purpose>. It should feel <positive direction;
reference screenshot if any>.
Don't use: <specific list of patterns, e.g. pill buttons, filler subtitles,
all-caps labels, cream backgrounds>.
Done means: it renders at <breakpoints>, you have taken screenshots of each,
and <PR/preview link>.
```

**review** (to a second-family model; do not append §9, use this report)
```
Review <target: uncommitted diff / branch X vs main / PR #N / commit SHA>.
Focus: <correctness, regressions, edge cases, security, whatever matters>.
Do not edit files.
Verify findings by running the code or tests where you can.
For each finding give: file:line, what is wrong, how you confirmed it, and
severity. Mark any finding you could not confirm as UNCONFIRMED with the reason.
If you find nothing, say so clearly and name what you inspected.
```

**investigate**
```
<Symptom, with repro steps, logs, screenshot, run link.>
Find the root cause. Reproduce it before you claim it. Do not fix it yet
<or: then fix it and add a regression test>.
Done means: a root cause with evidence (repro, failing test, or trace) and the
file:line where it originates.
List what you ruled out. Mark anything you could not confirm. If you cannot
find it after <bound>, stop and report what you tried.
```

**analyze**
```
<Question: e.g. how could this change be split into landable PRs? what is the
real blast radius of X?>
Read whatever you need. Do not change code.
Done means: <a written plan / ranked list / map> with file references for each claim.
Mark claims you could not confirm. If something is fine, say so rather than
inventing work.
```

**bulk**
```
Apply <transformation> to <set: files matching X / every endpoint in Y>.
The spec is complete; there are no judgment calls. If you hit a case the spec
doesn't cover, skip it and list it.
Done means: every item is done or listed as skipped, and <tests/linter> pass.
```

**research**
```
Find out <question>. Use <docs/web/APIs>. Prefer primary sources.
Done means: a short report with the answer, a source link per claim, and what
you could not determine. Quote sources with quotation marks.
```

**computer-use**
```
On <machine/simulator/browser>, open <app/URL> and <flow to exercise>.
Expected: <behaviour>. Capture a screenshot <or video> at <points>.
Don't <touch other apps / log in to anything / submit payments>.
Done means: a pass/fail per step, the screenshots, and exact notes on any mismatch.
If you cannot reach the app, stop and say what failed.
```

**copy**
```
Write <UI text / docs page> for <audience>. Purpose: <what the reader must do or know>.
Constraints: <length, tone, terms to use>. Don't add taglines, subtitles, or
filler copy. Please remove all mannered prose.
Done means: the text, plus one alternative for any line you are unsure of.
```

**3d-games**
```
Build <scene/mechanic>. Tools available: <Blender CLI / engine>.
Priority is <visual fidelity | how it feels to control>: <specific controls,
camera, movement targets>.
Done means: it runs at <fps target>, and you have <screenshots/video> of <states>.
```

**prompt-writing** (always human-audited)
```
Draft <skill / agent definition / prompt> for <purpose>. The description must
say when to use it and when not to. Include exact commands where it shells out.
Keep it short; no style rules. Mark anything you guessed.
I will audit it before it is used.
```

**babysit**
```
Babysit PR <#N> until every check and review bot is green.
Only act on checks and comments newer than the latest push. Verify every bot
finding against the source before changing anything; fix real findings and CI
failures. If a finding isn't worth addressing, reply with a short written
reason and resolve it. Rebase on main when needed. Please don't scope creep:
only address real shortcomings, and don't post filler comments.
If an overlapping PR makes this one obsolete, stop, report it, and ask before
closing. <Merge policy: report when green | merge when green and you're happy.>
```

**orchestrate**
```
<Goal, wide.> Plan the work, then run it. Use subagents, workflows, and
worktrees however you choose; I trust your judgment. Keep working yourself
while subagents run: test their findings and plan the next step.
Subagent models: <pins from routing table>. Prefix subagent names with the model.
<Merge policy and reviewer-bot gate.>
Done means: <every item in todo.md marked done / all PRs merged or listed with blockers>.
Stop and ask only for product decisions or destructive actions.
```
