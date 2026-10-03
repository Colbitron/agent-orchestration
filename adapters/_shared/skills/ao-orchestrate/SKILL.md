---
name: ao-orchestrate
description: How to delegate work using the user's routing table. Use before spawning subagents or shelling out to another model for any non-trivial task; picks the model and effort per task type, shapes the delegated prompt (what / done / out), and applies the standing rules and permissions.
---

# Orchestrate

The kit root is `KIT_ROOT`. The user's routing table should already be in
your context: your global instructions tell you to read
`~/.agent-orchestration/routing.md`, `glossary.md`, and `lessons.md` at
session start. If you have not, read them now. If `routing.md` does not
exist, stop and run the `ao-setup` skill first; do not guess which models the
user can afford.

## Before delegating anything

1. Classify the task against the task ids in the routing table (one of:
   quick-fix, feature, long-run, frontend, review, investigate, analyze,
   bulk, research, computer-use, copy, 3d-games, prompt-writing, babysit,
   orchestrate). If a task spans two, split it.
2. Take the primary model and effort from the table row. Use the fallback
   only when the primary is unavailable, rate-limited, or has already
   failed the task once.
3. Read `KIT_ROOT/core/strategies/delegation-prompting.md` if you have not
   already this session, and write the prompt in its shape: what you want,
   what "done" means (checkable), and when to stop and ask. Add the
   task-type template's extras from its §14.
4. Decide the mechanism per `KIT_ROOT/core/strategies/parallelism.md`:
   - your harness's subagent mechanism, if any, for bounded, independent
     pieces whose model this harness can run
   - a worktree plus a separate session for checkpointed work that needs
     CI and review between steps
   - an `ao-bridge-*` skill when the model lives in another harness
     (`ao-bridge-review`, `ao-bridge-implement`, `ao-bridge-investigate`,
     `ao-bridge-verify`)
   - if your harness has no subagents, do the bounded piece yourself or
     bridge it; do not pretend to spawn one
5. Name the subagent, stage, or bridge call with the model prefix
   (`[opus] implement auth`, `[sol] review auth`) so the user can see who
   ran what.

## While work runs

- Keep working on the top-level task while delegated work runs: test
  findings, plan the next step.
- Do not poll bridged CLIs in a tight loop; respect the bridge timeout.

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

Use the `ao-lesson` skill with what you expected and what happened, so the
improvement loop records it.
