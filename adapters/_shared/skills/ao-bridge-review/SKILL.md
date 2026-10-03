---
name: ao-bridge-review
description: Get a read-only code review from a model in a different lab's family by calling its CLI one-shot from the shell, then verify its findings before showing them. Use after implementing non-trivial changes, before opening or merging a PR, or when the user asks for a second opinion or cross-family review. Not for fixing code.
---

# Bridge: review

Cross-family review: the reviewer must come from a different lab than the
model that wrote the code. Claude-written code goes to an OpenAI or Grok
model; OpenAI-written code goes to Claude. Kit root: `KIT_ROOT`.

## 1. Pick the reviewer

1. Use the `review` row of `~/.agent-orchestration/routing.md`. If no
   routing table exists, stop and run the `ao-setup` skill.
2. Default preference (`KIT_ROOT/core/bridges/README.md`): `codex-cli`
   (Sol), else `grok-cli`, else `agy-cli`, for Claude-written code;
   `claude-cli` for GPT-written code. Use only bridges the routing table
   marks live.
3. Inside T3 Code, if a `delegate_task` tool from the `t3-code` MCP server
   is available, prefer it with `role: review`, `mode: wait`, and
   `interactionMode: plan`. The child sees only your task text.
4. Read `KIT_ROOT/core/bridges/<id>.md`. Use its read-only command template
   exactly. If the file is missing, say so and stop; never compose CLI flags
   from memory.

## 2. Write the prompt

Self-contained and literal (GPT and Grok want simpler prompts than Claude;
see `KIT_ROOT/core/strategies/delegation-prompting.md` §12). Fill in:

```
Review <uncommitted diff | branch X vs main | PR #N | commit SHA> in <absolute repo path>.
Focus: <correctness, regressions, edge cases, security>. Do not edit files.
Verify findings by running the code or tests where you can. For each finding
give file:line, what is wrong, how you confirmed it, and severity. Mark any
finding you could not confirm as UNCONFIRMED with the reason.
If you find nothing, say so clearly and name what you inspected.
```

Never put secrets in the prompt.

## 3. Run it

- Read-only flags from the bridge file. Run from the repo directory or pass
  the bridge's working-dir flag.
- Timeout: 20 minutes, via the kit's helper (macOS has no `timeout`):
  `sh KIT_ROOT/core/bridges/_timeout.sh 1200 <cmd>`.
  Exit 124 means it timed out. Stdin must not be a terminal: pipe the
  prompt in or redirect from `/dev/null`.
- Capture output to `/tmp/agent-orchestration/review-<model>.md` (create
  the dir), then read that file.
- Run it in the background if your harness allows, and keep working.

## 4. Handle the result

1. A timeout or non-zero exit is "no result", not "nothing found". Check
   the file for partial output before rerunning once.
2. Verify each important claim against the code before presenting it. Drop
   contradicted claims; keep unconfirmed ones, labelled.
3. Present, prefixed with the bridge id (`[codex-cli/sol]`): confirmed
   findings (file:line, how confirmed), then unconfirmed, then "inspected
   but found nothing in: ...".
4. An explicit "nothing found" is accepted once. Do not re-run.
5. Do not fix findings inside this skill. If fixes are wanted, hand them to
   the implementer per the routing table, then re-review.

If the reviewer misbehaved (wrong flags, ignored read-only, rambled), run
the `ao-lesson` skill.
