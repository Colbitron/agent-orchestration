---
name: bridge-implement
description: Hand a bounded, well-specified implementation task to another model through its CLI bridge on a fresh git worktree, then verify the branch yourself and bring back a reviewed diff (or a PR, if the user's permissions allow). Use when the routing row for the task (often `bulk` or `quick-fix`) points at a bridged model, when a cheaper model fits a clear spec (GPT for mechanical work, or Claude from a non-Claude harness), or when the user names another model to make the change. Not for open-ended or taste-sensitive work without a checkable done state.
user-invocable: true
argument-hint: "[model] <task with done condition>"
---

# Bridge implement

The kit root is `${CLAUDE_PLUGIN_ROOT}`, also announced in the
`<agent-orchestration>` block at session start. Read
`${CLAUDE_PLUGIN_ROOT}/core/bridges/README.md` and
`core/strategies/delegation-prompting.md` (§2, §8, §12, §14) if you have not
this session.

## 1. Check the task fits

Bridge it only if you can write a checkable done state in one or two
sentences and the change is bounded (named behaviour, a known area, no
product calls). Otherwise keep it native or split it first. Check the
standing permissions: `create_worktrees` must be allowed.

## 2. Pick the bridge

Take the model from the routing row for this task (or the one the user
named). If it runs natively here, use a subagent with `isolation: worktree`
instead of a bridge. Otherwise resolve its bridge id from the routing table
("Reach it via" / `## Bridges`) or the profile's `access.invoke_via`, and
read `${CLAUDE_PLUGIN_ROOT}/core/bridges/<id>.md`. Use its **One-shot,
write-enabled** template exactly. If the bridge is not live (detect fails or
not smoke-tested), say so and offer to do the task natively; do not guess
flags.

## 3. Create the worktree

```
base=$(git rev-parse --abbrev-ref HEAD)        # or the branch the user named
branch=<model>/<short-task-slug>
wt="$(git rev-parse --show-toplevel)/../$(basename "$(git rev-parse --show-toplevel)")-wt-<slug>"
git worktree add -b "$branch" "$wt" "$base"
```

If the build needs untracked files (`.env`, local config), copy them into the
worktree yourself; never paste their contents into the prompt. Run the
project's install step there if the callee will need it.

## 4. Build the prompt

Self-contained, in the callee's dialect from the bridge file (GPT: short,
literal, imperative). Required parts:

```
In <worktree path>, <task>. Make the smallest possible changes.
Done means <checkable condition>, and `<test/lint command>` passes.
If while working you find pre-existing bugs or things the task doesn't
mention, don't fix them; list them as follow-ups.
Do not touch <files/areas out of scope>. Do not add dependencies.
Commit your work on branch <branch> with a clear message. Do not push.
If you make no progress after 3 attempts, stop and report what blocks you.
End with: Changed (files), Tests run (command and result), Not verified,
Follow-ups.
```

A linked worktree keeps its git metadata in the main repo's
`.git/worktrees/`, outside the worktree. Sandboxes that only allow writes in
the working dir may block the commit; follow the bridge file (e.g. an extra
writable dir) or let the callee leave changes uncommitted and commit them
yourself after review.

## 5. Run it

Write the prompt to `<artifact dir>/impl-<model>-prompt.md` (artifact dir:
session scratchpad, else `/tmp/agent-orchestration/`), output to
`impl-<model>.md`, working dir = the worktree, 45-minute timeout per the
bridges README. Run in the background (the Bash tool caps foreground at 10
minutes). Inside a workflow, hand this step to the `bridge-runner` agent,
named `[<model>] implement <slug>`. A timeout is "no result"; inspect the
worktree for partial work before deciding anything.

## 6. Verify the branch yourself

Do not trust the callee's report, least of all "committed" or "pushed".

```
git -C "$wt" status --short                 # anything left uncommitted?
git -C "$wt" log --oneline "$base..$branch" # the commits that exist
git -C "$wt" diff --stat "$base...$branch"  # which files changed
git -C "$wt" diff "$base...$branch"         # read it
```

Then run the done-state check (tests, lint, build) in the worktree yourself.
Read the whole diff for scope creep: changes outside the task get reverted
or flagged. If the work is close but not done, either fix it yourself or
re-run once with a narrower prompt; if it misses the bar, escalate to a
smarter model per the standing rules.

For anything that will merge, get a cross-family review: if a GPT model
wrote it, review it yourself or with a Claude subagent; if Claude wrote it,
use `/agent-orchestration:bridge-review`.

## 7. Hand back

Push and open a PR only if the standing permissions allow `open_prs` and the
user wants one; then confirm with `git ls-remote origin "$branch"` and
`gh pr view`. Report, prefixed with the model:

```
[<model>] <slug>: <done | partial | failed>
Branch: <branch>  Worktree: <path>  Commits: <n>  PR: <link or none>
Diff: <files changed, +/->   Tests: <command → result, run by me>
Scope: <clean | reverted X | flagged Y>
Not verified: <…>   Follow-ups: <…>
```

## 8. Clean up

- Keep the worktree until the branch is merged, abandoned, or the user says.
- Remove with `git worktree remove "$wt"`; never `--force` over uncommitted
  changes without asking.
- If the run produced nothing usable, remove the worktree and delete the
  branch only with `git branch -d` (refuses unmerged commits); ask before
  `-D`.

## 9. Log

If `logging.enabled` in `~/.agent-orchestration/config.yaml`, append one JSON
line to `logging.path` per `core/strategies/improvement-loop.md` §8:
`task_type`, `model`, `effort`, `harness`, `mechanism: "bridge:<id>"`,
`wall_clock_minutes`, `human_interventions`, `outcome`, `escalated_to`,
`notes`. If a flag or command was wrong, run `/agent-orchestration:lesson`.
