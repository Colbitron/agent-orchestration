# Verification and review

Load this when work needs checking: before you report a task as done, when
you dispatch a reviewer, when you babysit a PR, and before anything merges.
Verification is part of the task, not an optional extra, and the cheapest
verifier is usually a different model from the one that wrote the code.

Sources:
- FABG: "So I was using Fable wrong...", Theo (t3.gg), YouTube, https://youtu.be/-XWSJM-Ue-o
- MODELS: "Please stop using stupid models", Theo (t3.gg), YouTube, https://youtu.be/iBrAWpjXNxs
- INSP: "A proper guide to Fable 5", Theo (t3.gg), YouTube, https://youtu.be/8GRmLR__OGQ (recorded in the Fable 5 / GPT-5.5 / Opus 4.8 era)
- OPUSG: "Getting the most out of Opus 5.5", Theo (t3.gg), YouTube, https://youtu.be/ejjBbaq9RmY
- SOL61: "OpenAI fights back", Theo (t3.gg), YouTube, https://youtu.be/vu8X3YroB-w
- ASTRA: "It's Here.", Theo (t3.gg), YouTube, https://youtu.be/XFWpf0wLbh0
- OPUS55: "My new favorite model.", Theo (t3.gg), YouTube, https://youtu.be/jgGyX7MPPVg
- FVA: "Fable Vs Astra Debate Is Over", Theo (t3.gg), YouTube, https://youtu.be/P7bxbDSnZRM
- SON55: "OpenAI should be scared of this one", Theo (t3.gg), YouTube, https://youtu.be/8WbW_n95wc4
- FAB51: "My New Favorite Model", Theo (t3.gg), YouTube, https://youtu.be/r_dw-1109Ag

`[KEY m:ss]` links to the video at that timestamp; the auto-generated captions
often mishear model names (Sol as "Soul", Fable as "Able").

---

## 1. Principles

1. **The implementer verifies its own work first.** Done includes "verify that
   it's fixed, film a video showing the results, put up a pull request,
   monitor it to address all the review comments"
   ([FABG 29:12](https://youtu.be/-XWSJM-Ue-o?t=1752)).
2. **A different lab reviews.** Claude writes, OpenAI or Grok reviews; and the
   reverse. Same-family review misses what cross-family review catches.
3. **Reviewers run things.** "Agents know a lot more about code when they can
   actually run it than they can possibly guess by just staring at it"
   ([MODELS 2:01](https://youtu.be/iBrAWpjXNxs?t=121)).
4. **Unconfirmed claims are labelled.** Every reviewer and investigator says
   what it could not confirm.
5. **The orchestrator checks objective state itself** (git, CI, PR status)
   and does not redo the worker's reasoning.
6. **Spending more on verification than on doing is acceptable.** "I burned
   way more tokens trying to verify the work that Fable did here than I burned
   getting Fable to do the work here" ([INSP 34:22](https://youtu.be/8GRmLR__OGQ?t=2062)).

## 2. Cross-family review

Why: models from one lab share blind spots. Evidence:

- "When I have Opus code being reviewed, I don't want just Opus reviewing it.
  I would like for Astra or even like Sol to give it a review as well"
  ([OPUSG 23:01](https://youtu.be/ejjBbaq9RmY?t=1381)). He also suggests Grok.
- GPT-6.1 Sol reviewed a Claude-written T3 Code fix and "found real problems
  that were entirely missed by Fable and by Opus", preventing a real
  regression ([SOL61 26:53](https://youtu.be/vu8X3YroB-w?t=1613)).
- Sol found 1.3M of 1.8M lines unused in a port that Opus had rewritten
  without deleting the old code ([SOL61 28:48](https://youtu.be/vu8X3YroB-w?t=1728)).
- In reverse, Fable reviewed Astra's 26K-line runtime fork and said it was not
  ready to merge, with concrete reasons (one-way-door migration, three features
  in one PR, default flipped, headline number not proving live queries)
  ([FABG 19:40](https://youtu.be/-XWSJM-Ue-o?t=1180)). Fable also audited Astra's
  Lakebed performance changes as "entirely sound"
  ([ASTRA 33:41](https://youtu.be/XFWpf0wLbh0?t=2021)).

Who reviews whom (defaults; the user's routing table overrides):

| Author | Primary reviewer | Second opinion / filter |
|---|---|---|
| Claude (Fable, Opus, Sonnet) | OpenAI (GPT-6.1 Sol, or Astra) | Grok 4.7; then a Claude model filters noise |
| OpenAI (Astra, Sol) | Claude (Fable or Opus) for merge-readiness and risk | Automated reviewer bots |
| Anything that ships | Automated reviewer bots as a gate (§8) | Human for product calls |

Reviewer character ([OPUSG 22:44](https://youtu.be/ejjBbaq9RmY?t=1364); [OPUSG 24:27](https://youtu.be/ejjBbaq9RmY?t=1467);
[OPUS55 22:02](https://youtu.be/jgGyX7MPPVg?t=1322)):

- **OpenAI models dig hard and are noisy.** "They just really dig into the
  details and won't let go... It'll report more stuff that doesn't matter,
  but it will occasionally find things that do matter that the Claude models
  just miss entirely." Sol's "Rottweiler nature"
  ([SOL61 13:05](https://youtu.be/vu8X3YroB-w?t=785)).
- **Claude models find less but vet it.** Fable's findings "all matter... but
  it just didn't find as much." Opus 5.5 had no contradicted findings on
  Theo's bench. Use a Claude model to filter an OpenAI reviewer's list.
- **Theo's informal review bench** (supported findings): Astra 8, Grok 4.7 8
  (second overall), Sol 9 but lower validity, Fable 5 across two runs, Opus 5
  "4 supported, 2 not" ([OPUSG 23:18](https://youtu.be/ejjBbaq9RmY?t=1398)). A later
  "find improvement opportunities" task: Sol 87.4, Astra 83.8, Grok 4.7 80.7
  ([SOL61 14:05](https://youtu.be/vu8X3YroB-w?t=845)). The two runs differ; both put OpenAI
  and Grok above Claude for exhaustive review.

## 3. Writing the review prompt

Use the `review` template in `delegation-prompting.md` §14. Non-negotiable
elements:

- **A precise target:** uncommitted diff, branch vs base, a commit, or a PR
  number. Theo's review bridge starts by identifying the review target ([INSP 21:00](https://youtu.be/8GRmLR__OGQ?t=1260)).
- **Mark what could not be confirmed.** "You should ask the model to mark the
  things that it can't confirm... If you ask the model to let you know what
  things it can't verify, it will" ([OPUSG 24:41](https://youtu.be/ejjBbaq9RmY?t=1481)).
  Some things cannot be verified at all (other hardware, a missing env var, a
  subjective call); you want those named, not silently assumed.
- **The nothing-found case.** "If [the reviewer] finds nothing, say that
  clearly and mention what the review target is that it inspected." Without
  this, empty results confused the parent and it reran ([INSP 21:58](https://youtu.be/8GRmLR__OGQ?t=1318)).
- **Read-only by default.** Reviewers do not edit. Use a read-only sandbox
  where the harness offers one.
- **Simple prompts for GPT reviewers.** Do not prompt a GPT model as if it
  were Claude (`delegation-prompting.md` §12).
- **Safe wording.** Ask "are there bugs in this?" rather than compile-probing
  phrasing ([FABG 33:10](https://youtu.be/-XWSJM-Ue-o?t=1990)).

## 4. Give the reviewer tools

A reviewer that can run the system finds bugs that reading cannot.

- **Tests:** let it run the suite, or write a failing test for its claim.
- **A running app and a browser or computer use:** Sol found its regressions
  through "a combination of reading the code and analyzing it as well as
  computer use" ([SOL61 27:10](https://youtu.be/vu8X3YroB-w?t=1630)).
- **Sandboxes per hypothesis.** The Greptile pattern: a reviewer orchestrator
  "can spin up and run sandboxes with sub agents for whatever theories it has
  about what might be wrong. Some reviews might need no sandboxes, some
  reviews might need 10," returning images and videos as proof
  ([MODELS 2:32](https://youtu.be/iBrAWpjXNxs?t=152)). "Code breaks in ways that are not
  clearly visible just from reading code."
- **For big PRs, pull it down and play with it:** "ask your agent on your
  machine to pull it down, play with it, test it, and make sure everything
  works" ([MODELS 1:31](https://youtu.be/iBrAWpjXNxs?t=91)).

## 5. Handling reviewer output

The caller of a review bridge does this before showing anything to the user
(Theo's codex-review skill, [INSP 21:06](https://youtu.be/8GRmLR__OGQ?t=1266)):

1. Read the reviewer's report from its artifact file.
2. **Verify each important claim against the code** before presenting it.
3. Drop claims that are contradicted. Keep unconfirmed ones, labelled.
4. Present: confirmed findings (with file:line and how confirmed), then
   unconfirmed, then "inspected but found nothing in: ...".

The fix loop ([SOL61 27:17](https://youtu.be/vu8X3YroB-w?t=1637); [SOL61 27:47](https://youtu.be/vu8X3YroB-w?t=1667)):

```
Claude implements → OpenAI reviews (read + run) → orchestrator verifies
findings → Claude fixes → OpenAI re-reviews ("better, but I'll still fix two
small gaps") → Claude fixes → merge gate.
```

Delegate this loop rather than relaying by hand: "Hey, can you have Astra
verify this?" Fable then "will update the code accordingly, then test it again
and not come back to me until it has results it's happy with"
([FABG 26:03](https://youtu.be/-XWSJM-Ue-o?t=1563)).

## 6. Plan review across models

Review the plan before the build when the work is wide.

- Theo had two models "review each other's plans separately" before a large
  rewrite, then committed the plan to a branch in a worktree and built it
  ([FVA 28:11](https://youtu.be/P7bxbDSnZRM?t=1691)).
- For decomposition questions ("how do we split this giant PR?"), Astra gave
  the best plan, Sonnet 5.5 the best value at about half Opus's cost, and Sol
  was fast "but at like half the score" ([SON55 22:13](https://youtu.be/8WbW_n95wc4?t=1333)).
- His model roster said: "Reviews of plans and implementations, Fable 5 or
  Opus 48. Optionally [GPT] is an extra independent perspective" ([INSP 18:55](https://youtu.be/8GRmLR__OGQ?t=1135)).
- Plans should link to the PRs or code they are based on, say where the
  existing implementation is, and decompose into bounded PRs ([INSP 27:25](https://youtu.be/8GRmLR__OGQ?t=1645)).

## 7. The orchestrator verifies state

Do not trust a worker's report about objective state. Check it.

Why: Astra said review comments were valid and made no changes; later fixed
them but did not push; claimed everything was resolved and stopped monitoring
early ([ASTRA 36:53](https://youtu.be/XFWpf0wLbh0?t=2213)). An orchestrator should check the
git and PR state rather than trust its report ([ASTRA 38:59](https://youtu.be/XFWpf0wLbh0?t=2339)).
Opus 5.5 once had "almost three hours" of changes still local and uncommitted
([OPUS55 34:38](https://youtu.be/jgGyX7MPPVg?t=2078)).

After any worker claims it committed, pushed, opened, or merged, confirm:

- The branch exists on the remote and its head matches the claimed commit.
- The working tree is clean (nothing important left uncommitted).
- The PR exists, targets the right base, and contains the claimed changes.
- CI status and reviewer-bot status are what the worker says.
- For merges: the PR is merged and the todo item is marked done.

Example (GitHub CLI; adapt to the user's forge):

```
git -C <worktree> status --short
git -C <worktree> log -1 --oneline
git ls-remote origin <branch>
gh pr view <N> --json state,headRefOid,baseRefName,mergeable,statusCheckRollup
gh pr checks <N>
```

**Do not redo the model's reasoning.** Re-deriving a fix the model already
tested is "the person who would write the type check after the type check"
([FABG 29:25](https://youtu.be/-XWSJM-Ue-o?t=1765)). Check cheap objective facts; leave
judgment to the reviewer step.

## 8. Merge gates

- **Kit default: propose PRs, never merge.** Merging is enabled only in the
  user's config (`docs/ARCHITECTURE.md`).
- **When merging is enabled, automated reviewers gate it.** "Do not merge code
  until my automated code reviewers have approved it" ([INSP 32:33](https://youtu.be/8GRmLR__OGQ?t=1953)). Theo's set:
  Bugbot, Macroscope, CodeRabbit. All Fable 5.1 audit PRs merged with "every
  bot thread answered or fixed before merge" ([FAB51 44:05](https://youtu.be/r_dw-1109Ag?t=2645)).
- **Path-scoped review agents** defined as markdown in the repo (e.g. a
  "service conventions" agent and a "UI consistency" agent), each approving only
  if its condition holds, plus a top-level approval. "You could add all of
  these things into your agent MD, but that only guarantees that your agent
  knows about them, not that it's actually going to follow"
  ([FVA 2:03](https://youtu.be/P7bxbDSnZRM?t=123)).
- **Prod stays human.** Merge-to-main is safe only when main deploys to
  staging and prod deploys need a person ([INSP 33:16](https://youtu.be/8GRmLR__OGQ?t=1996); [FAB51 43:58](https://youtu.be/r_dw-1109Ag?t=2638)).
- **Product-opinion changes stay with the human.** Theo lets the model merge
  bug fixes and performance work; product calls are his
  ([FAB51 53:46](https://youtu.be/r_dw-1109Ag?t=3226)).
- Merge-readiness pickiness varies by model. Theo trusts Fable 5.1 to decide
  ("I've yet to be burned by that, despite it doing it dozens of times")
  ([FAB51 46:38](https://youtu.be/r_dw-1109Ag?t=2798)) and tested Astra's merges himself
  after being burned by Sol ([ASTRA 34:09](https://youtu.be/XFWpf0wLbh0?t=2049)). Route the
  merge decision to the model with the highest floor.

## 9. Babysitting a PR

Use the `babysit` template (`delegation-prompting.md` §14). The procedure,
from Theo's skill ([FABG 14:34](https://youtu.be/-XWSJM-Ue-o?t=874)):

1. **Monitor.** If the harness offers a PR-monitoring tool, use it so you
   respond when comments arrive; otherwise poll for new comments and checks.
2. **Only act on checks and comments newer than the latest push.**
3. **Verify every bot finding against the source before changing anything.**
   Bots are "helpful even if they're not always right."
4. **Fix real findings and CI failures.** Commit, push, and confirm the push
   (§7).
5. **Reply and resolve** findings not worth addressing, with a short written
   reason. Use the user's PR-comment conventions (Theo's adds a disclaimer
   that an AI agent wrote the comment).
6. **Rebase on main when needed.**
7. **No scope creep, no filler comments.** "Please don't scope creep. Stop
   adding new things. Only address real shortcomings." Added because Sol
   drifted.
8. **Stop if superseded.** If an overlapping PR makes this one obsolete, stop
   monitoring, report it, and ask before closing unless closure was
   authorised.
9. **Do not stop until everything is green** ([ASTRA 37:52](https://youtu.be/XFWpf0wLbh0?t=2272)),
   then report or merge per config.

Known failure: review-bot comments can push a model into fix loops; "30
commits later you have way more code than you intended and nothing actually
ends up shipping" ([FAB51 40:56](https://youtu.be/r_dw-1109Ag?t=2456)). If a babysit run
exceeds a few rounds on the same thread of feedback, stop and hand the PR to
a higher-floor model with the takeover prompt (`parallelism.md` §10), or ask
the human.

## 10. Honest-assessment checkpoints

Ask these at gates. They produce structured, usable judgments, especially from
Claude models ([OPUSG 21:48](https://youtu.be/ejjBbaq9RmY?t=1308); [FABG 19:47](https://youtu.be/-XWSJM-Ue-o?t=1187)):

```
Is this ready to merge? Give me your honest thoughts.
What are the risks of merging this code today?
What's the worst thing that would happen if we merge this right now?
How can we de-risk this or test the changes to make sure it's relatively safe?
Would you confidently be able to debug <failure class> in <environment>?
What's the status of this work? What do you need from me?
How do you feel about these changes in the end? Was this a good thing to merge?
```

Use them as follows:

- "What are the risks of merging this today?" decides whether a ~300-line
  agent PR needs a human read ([OPUSG 21:57](https://youtu.be/ejjBbaq9RmY?t=1317)).
- The capability-boundary question exposed what Fable could not verify in
  staging (wrong query results) and led it to propose shadow mode, structured
  failure reasons, synthetic traffic, and runtime counters
  ([FABG 20:44](https://youtu.be/-XWSJM-Ue-o?t=1244)). Then have it build those
  confidence measures on a new branch.
- Pair a question with a conditional action to keep momentum: "Do you think
  that's all we need? If so, merge it."
- Never phrase these as "show your reasoning" (`delegation-prompting.md` §11).

## 11. Computer-use verification

- Route UI and runtime verification that needs a browser, desktop, simulator,
  or screenshots to the strongest computer-use model the user has, through a
  bridge. As of the research, OpenAI models via Codex lead, "especially on
  macOS" ([FABG 25:15](https://youtu.be/-XWSJM-Ue-o?t=1515); [ASTRA 11:43](https://youtu.be/XFWpf0wLbh0?t=703)).
- Theo's bridge description ([INSP 24:05](https://youtu.be/8GRmLR__OGQ?t=1445)), adapted to be the default for testing:
  "Use when the user asks Claude to test a flow, verify UI behavior, inspect a
  running app, capture screenshots, or report confirmation and feedback of
  implemented behavior that benefits from computer use functionality."
- Use the `computer-use` template: expected behaviour per step, screenshots at
  named points, pass/fail per step, explicit negatives (don't touch other
  apps, don't submit payments).
- Run it on a machine the user is not working on
  ([OPUSG 7:26](https://youtu.be/ejjBbaq9RmY?t=446)).
- For money or irreversible actions, the human makes the final click. Theo let
  Sol prepare wires and left the send to him ([SOL61 11:29](https://youtu.be/vu8X3YroB-w?t=689)).

## 12. Post-merge and pre-prod verification

After a large autonomous batch lands on staging ([INSP 34:00](https://youtu.be/8GRmLR__OGQ?t=2040)):

- Spin up agents to exercise all new features and a sample of old ones,
  including apps built the old way.
- Have agents diff prod vs main and list what needs de-risking, then write
  tests for those items.
- The human stress-tests too, then decides on the prod deploy.

## 13. When to escalate instead of verifying more

- A reviewer and an implementer disagree twice on the same point: ask a
  third model (different family) or the human.
- The task took an hour or more: treat it as an architecture signal, not just
  a review problem (`parallelism.md` §12).
- The fix is in a degraded-state area (stuck jobs, slow paths) on Opus: Opus's
  discernment weakens there; consider Fable ([OPUS55 35:28](https://youtu.be/jgGyX7MPPVg?t=2128)).
