---
name: ao-setup
description: Interview the user about their harnesses, model subscriptions, priorities, and autonomy comfort, then generate their personal routing table and glossary under ~/.agent-orchestration. Use when the user asks to set up, configure, re-run, or update agent orchestration or model routing, or when no routing table exists at ~/.agent-orchestration/routing.md. For an existing config that only needs a new table (a profile was added or edited, or config.yaml was edited), use the ao-refresh skill instead.
---

# Setup

You are running the agent-orchestration setup interview. The kit root is
`KIT_ROOT`. Every `core/...` path below is relative to it.

Read these three files before asking anything:

1. `KIT_ROOT/core/interview/setup-interview.md` (the script; follow it step
   by step, steps 0 to 9, in order)
2. `KIT_ROOT/core/interview/config-schema.md` (what you write)
3. `KIT_ROOT/core/interview/routing-generator.md` (the table spec; the
   generator script implements it)

Then run the interview. For the option-style questions in steps 1 to 4, use
your harness's question tool if it has one that allows several answers at
once; otherwise ask in plain text, list the options, and parse the reply.
Use plain text for the free-form questions in step 5. Let the user answer
several questions in one message.

Rules that are easy to get wrong:

- Do not write or show a routing table until steps 1 to 4 are answered.
- Read every `KIT_ROOT/core/models/*.md` frontmatter before step 6 so the
  `models` block is complete. Read a profile body only when a routing
  decision needs it.
- Write to `~/.agent-orchestration/` (create it). Never write into any
  harness config without the user saying yes to that specific change in
  step 8.
- In step 7, generate with the script, not by hand:
  `python3 "KIT_ROOT/core/interview/generate.py" --kit-root "KIT_ROOT"`
  with `--write`. It writes `routing.md`, `glossary.md` and
  `routing.stamp`. If it exits 2 (no YAML parser), show its message, then
  follow `KIT_ROOT/core/interview/routing-generator.md` by hand and say so.
- If `~/.agent-orchestration/routing.md` already exists, run the script
  with `--diff` first and show what would be lost.
- Never touch `lessons.md`.
- When step 8 wires a bridge, run the smoke test from the matching
  `KIT_ROOT/core/bridges/<id>.md` and report pass or fail; do not claim a
  bridge is live without running it. If that bridge file does not exist,
  report the bridge as not wired.

## Step 8 on this harness

The kit's `adapters/install.sh` has usually already appended an
instructions block (marked `<!-- agent-orchestration -->`) to this
harness's global instructions file. That block tells every session to read
`routing.md`, `glossary.md`, and `lessons.md`. Check for the marker before
offering to wire anything:

- Marker present: say the harness is already wired and skip to bridges.
- Marker absent: show the user `KIT_ROOT/adapters/<harness>/README.md` for
  their harness and offer to run
  `sh KIT_ROOT/adapters/install.sh <harness>` (show `--dry-run` output
  first).

If the harness supports subagent definitions with a pinned model (see the
adapter README), offer to write them from the routing table, one change at
a time, each with the user's yes.

Finish with the short closing summary from step 9, and tell the user that
the table loads at the start of the next session, not this one.
