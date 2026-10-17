---
name: bridge-implement
description: Hand a bounded, well-specified implementation task to another model through its CLI bridge on a fresh git worktree, then verify the branch yourself and bring back a reviewed diff (or a PR, if the user's permissions allow). Use when the routing row for the task (often `bulk` or `quick-fix`) points at a bridged model, when a cheaper model fits a clear spec (GPT for mechanical work, or Claude from a non-Claude harness), or when the user names another model to make the change. Not for open-ended or taste-sensitive work without a checkable done state.
user-invocable: true
argument-hint: "[model] <task with done condition>"
---

# Bridge implement

The kit root is `${CLAUDE_PLUGIN_ROOT}`, also announced in the
`<agent-orchestration>` block at session start. Read
`core/bridges/README.md` and `core/strategies/delegation-prompting.md`
(§2, §8, §12, §14) from it if you have not this session.

## 1. Check the task fits

Bridge it only if the done state is checkable in a sentence or two and the
change is bounded (no product calls); otherwise keep it native or split it.
The standing permissions must allow `create_worktrees`.

## 2. Pick the bridge

Take the model from the routing row for this task (or the one the user
named). If it runs natively here, use a subagent with `isolation: worktree`
instead. Otherwise resolve its bridge id from the routing table ("Reach it
via" / `## Bridges`) or the profile's `access.invoke_via`, read
`${CLAUDE_PLUGIN_ROOT}/core/bridges/<id>.md`, and use its **One-shot,
write-enabled** template exactly. If the bridge is not live (detect fails or
not smoke-tested), say so and offer to do the task natively; never guess flags.

## 3. Create the worktree

Base `<base>` is the current branch unless the user named one; branch
`<branch>` is `<model>/<slug>`; `<wt>` is a sibling directory of the repo.

```
top=$(git rev-parse --show-toplevel)
git worktree add -b <branch> "$top/../$(basename "$top")-wt-<slug>" <base>
```

Copy untracked files the build needs (`.env`, local config) into `<wt>`
yourself; never paste their contents into the prompt. Run the project's
install step there if the callee will need it.

## 4. Build the prompt

Self-contained, in the callee's dialect from the bridge file (GPT: short,
literal, imperative). Required parts:

```
In <wt>, <task>. Make the smallest possible changes.
Done means <checkable condition>, and `<test/lint command>` passes.
If while working you find pre-existing bugs or things the task doesn't
mention, don't fix them; list them as follow-ups.
Do not touch <files/areas out of scope>. Do not add dependencies.
Commit your work on branch <branch> with a clear message. Do not push.
If you make no progress after 3 attempts, stop and report what blocks you.
End with: Changed, Tests run (command, result), Not verified, Follow-ups.
```

A linked worktree's git metadata lives in the main repo's `.git/worktrees/`,
so a sandbox that only writes inside `<wt>` may block the commit. Follow the
bridge file, or commit the callee's changes yourself after review.

## 5. Run it

Prompt to `<artifact dir>/impl-<model>-prompt.md` (artifact dir: session
scratchpad, else `/tmp/agent-orchestration/`), output to `impl-<model>.md`,
working dir = the worktree, 45-minute timeout
(`sh ${CLAUDE_PLUGIN_ROOT}/core/bridges/_timeout.sh 2700 <cmd>`). Run in the
background (the Bash tool caps foreground at 10 minutes). In a workflow, use
the `bridge-runner` agent, named `[<model>] implement <slug>`. Exit 124 is a
timeout: "no result"; inspect the worktree for partial work first.

## 6. Verify the branch yourself

Do not trust the callee's report, least of all "committed" or "pushed".

```
git -C <wt> status --short                # anything left uncommitted?
git -C <wt> log --oneline <base>..<branch> # the commits that exist
git -C <wt> diff <base>...<branch>         # read all of it (--stat first)
```

Run the done-state check (tests, lint, build) in the worktree yourself. Read
the whole diff for scope creep; revert or flag changes outside the task. If
it is close, finish it yourself or re-run once with a narrower prompt; if it
misses the bar, escalate to a smarter model per the standing rules. For
anything that will merge, get a cross-family review: GPT-written code gets a
Claude review (you or a subagent); Claude-written code goes through
`/agent-orchestration:bridge-review`.

## 7. Hand back

Push and open a PR only if the standing permissions allow `open_prs` and the
user wants one; then confirm with `git ls-remote origin <branch>` and
`gh pr view`. Report, prefixed with the model:

```
[<model>] <slug>: <done | partial | failed>
Branch: <branch>  Worktree: <path>  Commits: <n>  PR: <link or none>
Diff: <files changed, +/->   Tests: <command → result, run by me>
Scope: <clean | reverted X | flagged Y>
Not verified: <…>   Follow-ups: <…>
```

## 8. Clean up

Keep the worktree until the branch is merged or abandoned, or the user says.
Remove it with `git worktree remove <wt>`; never `--force` over uncommitted
changes without asking. If the run produced nothing usable, delete the
branch only with `git branch -d`; ask before `-D`.

## 9. Log

If `logging.enabled` in `~/.agent-orchestration/config.yaml`, append one JSON
line to `logging.path`: the canonical record in
`core/strategies/improvement-loop.md` §8, with `model` as the implementer's
profile id (the `core/models/` file name, never a short name) and
`mechanism: "bridge:<id>"`. If a command was wrong, run
`/agent-orchestration:lesson`.
