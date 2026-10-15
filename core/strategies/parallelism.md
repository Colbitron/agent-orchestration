# Parallelism

Load this when work could be split: before you spawn a subagent, write a
workflow, create a worktree, start a goal loop, or open a thread on another
machine. It covers which primitive to use, when to split at all, and how to
keep parallel work visible and bounded.

Sources:
- INSP: "A proper guide to Fable 5", Theo (t3.gg), YouTube, https://youtu.be/8GRmLR__OGQ (recorded in the Fable 5 / GPT-5.5 / Opus 4.8 era)
- FAB51: "My New Favorite Model", Theo (t3.gg), YouTube, https://youtu.be/r_dw-1109Ag
- OPUSG: "Getting the most out of Opus 5.5", Theo (t3.gg), YouTube, https://youtu.be/ejjBbaq9RmY
- H55: "finally a good small model", Theo (t3.gg), YouTube, https://youtu.be/38_6C0dkKmU
- FABG: "So I was using Fable wrong...", Theo (t3.gg), YouTube, https://youtu.be/-XWSJM-Ue-o
- FVA: "Fable Vs Astra Debate Is Over", Theo (t3.gg), YouTube, https://youtu.be/P7bxbDSnZRM
- SOL61: "OpenAI fights back", Theo (t3.gg), YouTube, https://youtu.be/vu8X3YroB-w
- OPUS55: "My new favorite model.", Theo (t3.gg), YouTube, https://youtu.be/jgGyX7MPPVg
- MODELS: "Please stop using stupid models", Theo (t3.gg), YouTube, https://youtu.be/iBrAWpjXNxs
- SON55: "OpenAI should be scared of this one", Theo (t3.gg), YouTube, https://youtu.be/8WbW_n95wc4

`[KEY m:ss]` links to the video at that timestamp; the auto-generated captions
often mishear model names (Sol as "Soul", Fable as "Able").

---

## 1. The primitives

| Primitive | What it is | Use it for | Do not use it for |
|---|---|---|---|
| **Subagent** | You call a tool to spawn another agent with a self-contained prompt; it returns one result. | Independent, bounded units: analyse five files, investigate one PR, review one diff, deep-dive a subsystem. | Work that needs back-and-forth with you or with other workers mid-run. |
| **Workflow** | A script (Theo: "a big JavaScript file the model will write") that defines stages; results of one stage queue work in the next. | **Fan-out and verify.** Triage 16 PRs, then stress-test each verdict with a judge panel. Multi-reviewer passes before merge. | Checkpoint-driven programs where each step waits on CI, a human call, or a merge. |
| **Worktree** | A separate checkout of the repo on its own branch. | Isolating implementations that run concurrently so they do not collide; one worktree per PR-sized stream. | Read-only analysis (no need to isolate). |
| **Separate thread / session** | A new top-level agent, often on another machine. | Unrelated work, long runs you do not want on your laptop, computer use that would take over your screen. | Work that shares state with the current session. |
| **Goal mode** | An autonomous loop that keeps going until stated conditions hold. | Draining a written todo list over hours once the plan is agreed and gates exist. | Anything without hard gates (reviewer bots, staging-only deploys). Off by default in this kit. |
| **Shell-out** | A one-shot call to another model's CLI with a self-contained prompt; read its output back. | Cross-family review, computer use, token-heavy reading on a cheaper subscription. | Anything needing the other model to hold a conversation. |
| **Swarm** | Many subagents that message each other and the lead while running. | Very large ports/rewrites without UI, when the lead model supports it (Astra). | Models or harnesses without inter-agent messaging. |

Definitions of subagents vs workflows are from [INSP 12:49](https://youtu.be/8GRmLR__OGQ?t=769). The swarm description is
[FVA 50:26](https://youtu.be/P7bxbDSnZRM?t=3026).

**Harness notes.**
- *Claude Code:* subagents via its subagent tool; workflows are scripts the
  model writes and runs, and only Claude models can be named as workflow
  stages ([INSP 19:25](https://youtu.be/8GRmLR__OGQ?t=1165)); worktrees can be created by the agent itself.
- *Codex:* goal mode, `ultra` with unbounded subagents ("40 sub agents each
  can run"), and a "more rudimentary implementation of sub agents" that the
  model coordinates itself ([FVA 52:10](https://youtu.be/P7bxbDSnZRM?t=3130); [FVA 1:05:42](https://youtu.be/P7bxbDSnZRM?t=3942)).

## 2. The rule that decides between them

From the session where Fable planned eight-odd PRs across five plans ([INSP 29:24](https://youtu.be/8GRmLR__OGQ?t=1764)),
verbatim:

> "A single workflow is the wrong tool for the umbrella. Workflows are
> deterministic scripts that shine for fan out and verify. But this program is
> checkpoint driven. Each PR needs CI, your review, and a merge before the next
> rebase. In midstream, you'll make product calls... that a script can't
> anticipate. One giant workflow would either barrel past those checkpoints or
> stall at the first one."

Its recommendation, which this kit adopts:

1. **Orchestrate checkpoint-driven programs from the session** you are in.
2. **Spawn worktrees yourself** for the implementations.
3. **Use workflows only where they are strong:** multi-agent review passes
   before merge, and fan-out triage.
4. **Run streams in parallel only when they do not touch each other's code**,
   to avoid merge conflicts.

You do not need the human to create worktrees by hand
([INSP 29:19](https://youtu.be/8GRmLR__OGQ?t=1759): "you don't need to make a work tree by hand either").

## 3. Deciding whether to parallelise

Parallelise when all of these hold:

- The units are **independent**: no shared files, or a merge order you can
  state up front.
- Each unit has its own **checkable done state** (see `delegation-prompting.md`).
- The **result is worth the extra spend.** Parallel agents burn more: "It's
  going to burn more because it's just doing more"
  ([FAB51 54:06](https://youtu.be/r_dw-1109Ag?t=3246)).
- You can **verify** each result, or a later stage will.

Strong signals to parallelise ([OPUSG 20:24](https://youtu.be/ejjBbaq9RmY?t=1224)):
audits, migrations, mass PR review, codebase-wide improvement passes, anything
too big for one context window. Early testers ran Opus 5.5 "coordinat[ing]
parallel subagents on long audits with little oversight" successfully.

Signals not to:

- The work is narrow (minutes). Spawning costs more than doing.
- Every step depends on the previous one's outcome.
- The streams edit the same files. Serialise them, or order them so later
  PRs rebase onto earlier ones. Fable's audit plan ordered "deletions first
  [so] each later PR is a smaller PR" ([FAB51 43:21](https://youtu.be/r_dw-1109Ag?t=2601)).
- The task is taste-sensitive UI where one coherent hand matters more than speed.

### Many cheap attempts with cheap verification

A fan-out of cheap workers beats one smart worker only when both hold:

- A random try from a cheap model is nearly as good as a thoughtful try from a
  smart model. "If the gap between a random try from a dumb model and a
  thoughtful try from a smart model isn't that big, Haiku 5.5 is going to
  slaughter" ([H55 23:34](https://youtu.be/38_6C0dkKmU?t=1414)).
- Each attempt can be verified by running code, so a wrong try costs little.

Anthropic's egg-drop demo (a single vendor run, [H55 22:17-23:20](https://youtu.be/38_6C0dkKmU?t=1337)): Opus 5.5 alone
took 3 min 37 s, 25 attempts, $0.47. Opus 5.5 plus 10 Haiku 5.5 subagents took
58 s, 86 attempts, $0.14. Theo's caution: "This is a small subset of work."

Required controls:

- **Cap the number of agents.** Told to "use lots of subagents and use Haiku 5.5
  for all subagents", Opus proposed about 100 Haiku agents for 1,495 PRs
  ([H55 35:13-35:58](https://youtu.be/38_6C0dkKmU?t=2113)). The orchestrator sets the ceiling, not the lead.
- **Keep each Haiku request under about 100K prompt tokens.** Above that, every
  request pays the higher price tier, cache hits included (`cost-model.md` §10).
- **Share one rate-limit budget** when agents hit the same external API. Parallel
  fetches hit GitHub's 5,000 requests per hour limit and locked Theo's GitHub
  integration out for about 50 minutes ([H55 33:46-34:56](https://youtu.be/38_6C0dkKmU?t=2026)).
- **Make "cannot" or "nothing found" a valid return.** The same run saved error
  bodies as data, said it would wait for the quota reset, and never resumed.

## 4. Lead behaviour while subagents run

- **Keep working.** Do not idle while subagents run. Test their findings as
  they arrive, message them if your harness allows, and plan the next stage
  ([FABG 34:13](https://youtu.be/-XWSJM-Ue-o?t=2053)). "Both Astra and Fable 5.1 are
  really good at this."
- **Invent the archetypes you need.** Do not rely on fixed "review agent /
  adversarial agent / explorer" templates; define the roles this task needs.
  "That was all stupid and never made sense. Now it makes even less sense
  because Fable can invent those different archetypes depending on the needs
  for your specific task" ([INSP 14:00](https://youtu.be/8GRmLR__OGQ?t=840)).
- **Use a judge panel for contested verdicts.** Theo's triage workflow: "16
  investigators, one per PR. Each verdict then stress tested by Fable plus Opus
  judge panel. 14 of 16 calls were unanimous. I resolved the two contested
  ones" ([INSP 25:51](https://youtu.be/8GRmLR__OGQ?t=1551)).
- **You own the end state.** Collect each worker's closing recap, read
  "Blocked on me" first, and verify claims about git and PR state yourself
  (`verification-and-review.md`).

## 5. Planned subagents vs swarms

- **Claude (planned, staged).** "Fable... plans up front. It decides, I want
  these four sub agents for this. I want this type of sub agent next. And if
  these four find things, they can spin up the next type"
  ([FVA 50:26](https://youtu.be/P7bxbDSnZRM?t=3026)). This maps cleanly onto workflows.
- **Astra (swarm).** It "can just spin up a bunch of sub agents that are doing
  whatever and then pass messages to them, let them pass messages to each
  other... receive updates from those sub agents and use that to fan things
  out" ([FVA 50:44](https://youtu.be/P7bxbDSnZRM?t=3044)). Theo ran 40 in parallel on a
  TS→Rust port.
- **Caveat on swarms for long unattended builds.** That same port later
  stalled; Opus 5.5 restarted it and got it working in a day, and Theo
  concluded "for unattended long like heavy rewrite type stuff, Anthropic is
  just comically far ahead right now" ([SOL61 16:01](https://youtu.be/vu8X3YroB-w?t=961); [SOL61 16:31](https://youtu.be/vu8X3YroB-w?t=991)).
  **Kit rule:** use a swarm-capable GPT lead for exploratory, test-measured
  fan-out; use a Claude lead for long unattended work that must land.
- **Opus needs permission to fan out.** Add the subagent grant
  (`delegation-prompting.md` §7).

## 6. Make parallel work visible

- **Prefix subagent names with the model.** Theo could not tell which workflow
  subagents were calling GPT and asked for a prefix: "that ended up helping a
  ton" ([INSP 19:51](https://youtu.be/8GRmLR__OGQ?t=1191)). Convention for this kit: `[<model-short>] <task>`, e.g.
  `[sol] review PR 212`, `[sonnet] map auth module`.
- **Name streams after their PR or todo item** so the human can match threads
  to GitHub on a phone.
- **Give each subagent a one-line purpose** in its name, not "agent-3".
- Swarm-style naming works too: Astra's messages were addressed like
  `root/independent reviewer` ([FVA 51:38](https://youtu.be/P7bxbDSnZRM?t=3098)).

## 7. Timeouts

"The tasks can time out so I called this out" ([INSP 19:56](https://youtu.be/8GRmLR__OGQ?t=1196)). Rules:

- Assume any subagent, workflow stage, or shell-out can be killed by a
  harness timeout. Size units so each finishes well inside it.
- For long shell-outs, have the callee write its report to a file in a
  temporary artifact directory, then read the file. A timeout then loses the
  wait, not the work. (Theo's review bridge creates a "temporary artifact
  directory for the Codex report" ([INSP 21:00](https://youtu.be/8GRmLR__OGQ?t=1260)).)
- If a stage times out, check for partial output before rerunning.
- Do not treat a timeout as "nothing found".

## 8. Calling a non-native model from inside a workflow

Workflow stages can usually only be the harness's own models. To use another
lab's model in a stage, make the stage a **cheap native subagent that only
shells out** to the other CLI, waits, and relays the result. Theo: "You have to
call the claude model when using cloud codes workflows. So I gave it some
instructions here that it can use sonnet on low in order to spawn [GPT] get
its results and then report those back. It ends up being really cheap" ([INSP 19:32](https://youtu.be/8GRmLR__OGQ?t=1172)).

Wrapper prompt shape:

```
You are a wrapper. Run exactly this command and wait for it to finish:
<bridge command with self-contained prompt; output to <artifact path>>
Then read <artifact path> and return its contents verbatim, followed by one
line: the exit status and whether the output was empty. Do not edit files,
do not interpret or fix anything, do not rerun on an empty result.
```

Use the cheapest native model at its lowest viable effort for the wrapper
(see `effort-levels.md` §7). Prefix its name with the callee's model (§6).

## 9. Todo files and goal loops

For a program larger than one session's attention, write the plan down and
drain it.

1. **Agree the plan first.** Theo had Fable triage, close dead PRs, write
   plans (with links to the PRs that inspired them), and only then decide
   streams ([INSP 26:55](https://youtu.be/8GRmLR__OGQ?t=1615)).
2. **Ask the lead how to run it.** "If I wanted you to implement all of the
   plans you made, would it be best to do that as a single workflow or to make
   multiple work trees and threads by hand myself?" ([INSP 28:37](https://youtu.be/8GRmLR__OGQ?t=1717)). Let it answer;
   that is how the checkpoint rule in §2 surfaced.
3. **Write `todo.md` in the repo.** One line per bounded PR. Plans should
   "deliberately decompose into bounded PRs" ([INSP 29:02](https://youtu.be/8GRmLR__OGQ?t=1742)).
4. **Start the goal with explicit permissions and gates.** Theo's goal, close
   to verbatim ([INSP 30:21](https://youtu.be/8GRmLR__OGQ?t=1821)):
   ```
   Complete all of the work we have discussed here. You have permission to
   create worktrees, rebase, branch, merge PRs, close PRs, etc. Go through
   the work step by step and mark each to-do in todo.md done when completed.
   The todo.md changes should be committed and merged as you go. Use the tools
   available to you to break this work up logically. Review it thoroughly and
   merge with confidence. Do not merge code until my automated code reviewers
   have approved it.
   ```
   It ran five hours and landed roughly a month of roadmap.
5. **Preconditions before any merge-enabled goal** (this kit's rule; goal mode
   is off by default per `docs/ARCHITECTURE.md`):
   - The user enabled it in config.
   - Merging to main deploys at most to staging; prod deploys keep a human
     in the loop ([INSP 33:22](https://youtu.be/8GRmLR__OGQ?t=2002): "the model cannot ship or touch prod").
   - Automated reviewers gate merges.
   - Staging is in a state the user is happy to build on. Theo had Fable fix
     staging first.
6. **Verify after.** Theo spun up other agents to exercise new and old
   features and to diff prod vs main for risk: "I burned way more tokens
   trying to verify the work that Fable did here than I burned getting Fable
   to do the work" ([INSP 34:22](https://youtu.be/8GRmLR__OGQ?t=2062)). See `verification-and-review.md`.

If a GPT model pauses its goal, a plain permission restatement worked: "You
have my permission to do whatever you need to do. I have you on full access
for a reason. Keep going." ([FVA 25:47](https://youtu.be/P7bxbDSnZRM?t=1547)).

## 10. Worktree hygiene

- One worktree per stream or PR. Name the branch after the todo item.
- Spawn exploratory fixes freely; most need not merge. "I don't expect the
  majority of the code I spawn this way to be ever used or merged" ([INSP 40:14](https://youtu.be/8GRmLR__OGQ?t=2414)).
- **Combining worktrees** is a valid task: "Can you access all these work
  trees on my machine? I'd love to pull the changes from all of them into one
  branch with conflicts handled so I can test them all at once." Five minutes
  later it had ([INSP 39:52](https://youtu.be/8GRmLR__OGQ?t=2392)).
- **Takeover instead of copy-paste.** To move a stuck PR to a new agent: "Here's
  a PR. Get the branch on your work tree and it's yours. Push it, maintain it,
  manage it so that it actually lands" ([FAB51 40:09](https://youtu.be/r_dw-1109Ag?t=2409)).
- A separate **merge-monitor** agent can watch all PRs on a repo and merge or
  take over stalled ones ([FAB51 44:59](https://youtu.be/r_dw-1109Ag?t=2699)).

## 11. Remote machines and separate threads

- Run long and computer-use agents off the user's main machine. Pop-up windows
  are disruptive, and moving agents to remote boxes made Theo "like computer
  use a lot more" ([OPUSG 7:13](https://youtu.be/ejjBbaq9RmY?t=433)).
- Have the agent set up the remote run itself, with connection method and
  pre-authorisation in the prompt (`delegation-prompting.md` §5). Theo's
  handoff took ~17 minutes and surfaced real connection issues
  ([OPUSG 9:21](https://youtu.be/ejjBbaq9RmY?t=561)).
- One agent can SSH to another machine and launch and monitor an agent there
  ([OPUS55 34:25](https://youtu.be/jgGyX7MPPVg?t=2065)).

## 12. Time to complete is a diagnostic

Wall-clock time on a delegated fix tells you about the codebase, not just the
model ([INSP 40:20](https://youtu.be/8GRmLR__OGQ?t=2420)):

| Time to complete | Read it as | Do |
|---|---|---|
| Under ~3 minutes | Probably a simple fix. | File the PR; normal review. |
| ~15 minutes | "A little scary." | Pay more attention to the diff and the explanation. |
| An hour or more | "Something's wrong with our architecture." | Do not blindly merge. Go deeper; find the structural cause. Theo's 1.5-hour scroll-jump fix got far more scrutiny than a 2 min 20 s gesture fix. |

Also read the **number of files and packages touched**. And sanity-check fast
answers: the 2-minute fix mentioned a drawer component Theo thought was gone;
he asked "Do we even have a drawer anymore?" before trusting it ([INSP 41:23](https://youtu.be/8GRmLR__OGQ?t=2483)).

Log time-to-complete for every delegated run (`improvement-loop.md` §8).

## 13. Fix the codebase, not just the prompt

"You should adjust your prompts a little, but you should adjust your codebase
a lot. If agents are screwing up in your codebase, then a new dev would, too"
([MODELS 12:54](https://youtu.be/iBrAWpjXNxs?t=774), rule 7).

- Long unattended runs hit **speed bumps** in the codebase faster: one that
  agents hit every two hours gets hit two to three times in five hours
  ([MODELS 12:38](https://youtu.be/iBrAWpjXNxs?t=758)). Use long runs as a probe, fix the
  bumps, then work in shorter loops.
- When a fix takes an hour (§12), the follow-up task is the architecture, not
  a better prompt.
- When agents repeatedly fail in one area, either smooth it out in code or stop
  routing that area to agents ([MODELS 14:44](https://youtu.be/iBrAWpjXNxs?t=884)).
- Deleting slop helps agents too: after a 13K-line net deletion, the codebase
  "seems to have actually improved how agents contribute"
  ([FAB51 44:25](https://youtu.be/r_dw-1109Ag?t=2665)).

## 14. Cost controls for parallel runs

- **Pin subagent models.** An Opus 5.5 run spawned a Fable subagent unasked and
  inflated its cost ([SON55 26:32](https://youtu.be/8WbW_n95wc4?t=1592)).
- **Route reading-heavy stages to token-efficient or subscription-cheap
  models** via shell-out: log digging, giant PDFs and specs, hundreds of
  screenshots during computer use ([INSP 10:38](https://youtu.be/8GRmLR__OGQ?t=638)). Theo's five-and-a-half-hour Fable
  loop plus all the models it called cost "around 150 bucks" with this routing.
- **Do not enable unbounded fan-out modes casually** (Codex `ultra`, Claude
  Code `ultracode`); see `effort-levels.md` §7.
- **Sonnet as a subagent should be short and bounded.** Its cost edge vanishes
  in long cache-heavy loops (`cost-model.md`).
