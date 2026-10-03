---
name: orchestrate
description: How to delegate work using the user's routing table. Use before spawning subagents, launching a workflow, or shelling out to another model for any non-trivial task: picks the model and effort per task type, shapes the delegated prompt (what / done / out), and applies the standing rules and permissions.
user-invocable: true
---

# Orchestrate

The user's routing table, glossary, and lessons were injected at session
start inside the `<agent-orchestration>` block. If that block says no table
exists, stop and run `/agent-orchestration:setup` first; do not guess which
models the user can afford.

## Before delegating anything

1. Classify the task against the task ids in the routing table (one of:
   quick-fix, feature, long-run, frontend, review, investigate, analyze,
   bulk, research, computer-use, copy, 3d-games, prompt-writing, babysit,
   orchestrate). If a task spans two, split it.
2. Take the primary model and effort from the table row. Use the fallback
   only when the primary is unavailable, rate-limited, or has already
   failed the task once.
3. Read `core/strategies/delegation-prompting.md` from the kit root if you
   have not already this session, and write the prompt in its shape:
   what you want, what "done" means (checkable), and when to stop and ask.
   Add the task-type template's extras (anti-scope-creep block, closing
   recap, explicit negatives).
4. Decide the mechanism per `core/strategies/parallelism.md`:
   - a subagent for bounded, independent pieces
   - a workflow for fan-out-then-verify with many pieces
   - a worktree plus a separate thread for checkpointed work that needs CI
     and review between steps
   - a bridge skill (`/agent-orchestration:bridge-*`) when the model lives
     in another harness
5. Name the subagent or stage with the model prefix (`[opus] implement
   auth`, `[sol] review auth`) so the user can see who ran what.

## While work runs

- Keep working on the top-level task while subagents run; test their
  findings, plan the next step, message them if the harness allows it.
- Do not poll bridged CLIs in a tight loop; respect the timeout in the
  bridge skill.

## When work comes back

- Verify state yourself (git log, PR status, test output) rather than
  trusting the worker's summary, especially from GPT-family workers.
- If a cheaper model's output misses the bar, rerun with the fallback or a
  smarter model without asking. Judge the output, not the price tag.
- If a reviewer or bridge reports "nothing found", accept it once; do not
  re-run on an empty result.
- Apply the standing permissions block literally: never merge, close,
  force-push, or deploy unless the table says you may.
- Log the delegation if logging is enabled: one JSON line with task id,
  model, effort, mechanism, duration, outcome, and follow-ups needed.

## When something goes wrong

Run `/agent-orchestration:lesson` with what you expected and what happened,
so the improvement loop records it.
