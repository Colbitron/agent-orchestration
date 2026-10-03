---
name: ao-bridge-implement
description: Hand a bounded implementation task to a model in another harness by calling its CLI one-shot with write access on a dedicated git worktree, then verify the diff yourself. Use when the routing table assigns an implementation task (quick-fix, feature, frontend, bulk) to a model this harness cannot run. Not for open-ended or checkpoint-driven work.
---

# Bridge: implement

Kit root: `KIT_ROOT`. This is the only bridge that writes, and it writes
only on a worktree.

## 1. Pick the implementer

1. Use the matching task row of `~/.agent-orchestration/routing.md`. If no
   routing table exists, stop and run the `ao-setup` skill.
2. Default preference (`KIT_ROOT/core/bridges/README.md`): `claude-cli`
   from non-Claude harnesses, else `codex-cli`. Use only bridges the
   routing table marks live.
3. Inside T3 Code, if a `delegate_task` tool from the `t3-code` MCP server
   is available, prefer it with `role: implementation`. The child sees only
   your task text.
4. Read `KIT_ROOT/core/bridges/<id>.md` and use its write-enabled command
   template exactly. If the file is missing, say so and stop; never compose
   CLI flags from memory.

## 2. Prepare the worktree

```
git -C <repo> worktree add <repo>-wt-<task> -b <branch>
```

Pass the worktree's absolute path as the working directory. Never point a
write-enabled bridge at the user's main checkout.

## 3. Write the prompt

Use the task-type template from
`KIT_ROOT/core/strategies/delegation-prompting.md` §14 (quick-fix, feature,
frontend, or bulk). It must state what you want, what "done" means in
checkable terms, and when to stop and ask. For GPT-family callees: write
imperatives, add "make the smallest possible change", and give an escape
hatch ("if you make no progress after N attempts, stop and report what
blocks you"). End with the closing recap block (§9). Include the user's
style rules from the routing table. Never put secrets in the prompt.

## 4. Run it

- Timeout: 45 minutes:
  `sh KIT_ROOT/core/bridges/_timeout.sh 2700 <cmd>`
  (exit 124 = timed out). Pipe the prompt in or redirect stdin from
  `/dev/null`; it must not be a terminal.
- Capture output to `/tmp/agent-orchestration/implement-<task>-<model>.md`.
- Run it in the background if your harness allows; keep working.

## 5. Verify before trusting

1. A timeout is "no result". Inspect the worktree for partial work before
   deciding to rerun.
2. Check objective state yourself: `git -C <wt> status --short`,
   `git -C <wt> log --oneline <base>..`, and the diff. Do not trust "I
   committed" or "I pushed", especially from GPT-family models.
3. Run the tests or the done-check from the prompt.
4. If the output misses the bar, rerun with the fallback or a smarter model
   without asking.
5. Send non-trivial results through `ao-bridge-review` (different family from
   this implementer) before proposing a PR. Follow the routing table's
   permissions: never merge, force-push, or deploy unless it says you may.

Report with the bridge id prefix (`[claude-cli/opus] implement auth`). If
the callee misbehaved, run the `ao-lesson` skill.
