---
name: setup
description: Interview the user about their harnesses, model subscriptions, priorities, and autonomy comfort, then generate their personal routing table and glossary under ~/.agent-orchestration. Use when the user asks to set up, configure, re-run, or update agent orchestration or model routing, or when no routing table is loaded. For an existing config that only needs a new table (a profile was added or edited, or config.yaml was edited), use /agent-orchestration:refresh instead.
disable-model-invocation: false
---

# Setup

You are running the agent-orchestration setup interview. The kit root is
announced at session start inside the `<agent-orchestration>` block; it is
also available as `${CLAUDE_PLUGIN_ROOT}`.

Read these three files from the kit root before asking anything:

1. `core/interview/setup-interview.md` (the script; follow it step by step)
2. `core/interview/config-schema.md` (what you write)
3. `core/interview/routing-generator.md` (the table spec; the generator
   script implements it)

Then run the interview. Use `AskUserQuestion` for the option-style questions
in steps 1 to 4; it lets the user pick several answers at once. Use plain
text for the free-form questions in step 5.

Rules that are easy to get wrong:

- Do not write or show a routing table until steps 1 to 4 are answered.
- Read every `core/models/*.md` frontmatter before step 6 so the `models`
  block is complete. Read a profile body only when a routing decision needs
  it.
- Write to `~/.agent-orchestration/` (create it). Never write into
  `~/.claude/` or any harness config without the user saying yes to that
  specific change in step 8.
- In step 7, generate with the script, not by hand:
  `python3 "${CLAUDE_PLUGIN_ROOT}/core/interview/generate.py" --kit-root "${CLAUDE_PLUGIN_ROOT}"`
  with `--write`. It writes `routing.md`, `glossary.md` and
  `routing.stamp`. If it exits 2 (no YAML parser), show its message, then
  follow `core/interview/routing-generator.md` by hand and say so.
- If `~/.agent-orchestration/routing.md` already exists, run the script
  with `--diff` first and show what would be lost.
- Never touch `lessons.md`.
- When step 8 wires a bridge, run the smoke test from the matching
  `core/bridges/<id>.md` and report pass or fail; do not claim a bridge is
  live without running it.

Finish with the short closing summary from step 9.
