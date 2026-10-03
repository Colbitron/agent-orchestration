# Bridges

A bridge is the recipe for calling one model or harness from a shell,
one-shot, with a self-contained prompt, and reading the answer back. The
orchestrator uses bridges when the routing table points at a model that
lives outside the harness it is running in (Claude Code calling Codex for a
review, Codex calling Claude for a UI fix, either calling a cheap API for
bulk work).

Each bridge is one file, `core/bridges/<id>.md`, named by the id that model
profiles list under `access.invoke_via`. The file is read by the agent at
the moment it needs to shell out, so it must be exact: the one or two times
a flag is wrong are the expensive ones (Theo's lesson from the codex skills).

## Common rules for every bridge call

1. **Self-contained prompt.** The callee has none of your context. Include
   the goal, the done state, the scope boundary, the repository path, and
   the output format you want. Do not reference "the PR we discussed".
2. **Prompt in the callee's dialect.** GPT-family and Grok models want
   simpler, more literal prompts than Claude. Say exactly what to do and
   what to report; don't give personality or method. Claude models accept
   wider prompts with judgment calls. The bridge file says which.
3. **Read-only unless the task is implementation.** Review, investigation,
   analysis, and verification run with the bridge's read-only flags. Only
   `bridge-implement` uses the write variant, and only on a worktree.
4. **Timeout every call.** macOS has no `timeout`. Use
   `perl -e 'alarm shift; exec @ARGV' <seconds> <cmd...>` unless
   `gtimeout` is installed. Defaults: review and investigation 20 min,
   implementation 45 min, verification 30 min. Treat a timeout as "no
   result", not as "nothing found".
5. **Capture to a file.** Write the callee's output to a temp file under
   the scratchpad or `/tmp/agent-orchestration/<task>-<model>.md`, then
   read it. Several CLIs stream events to stdout; the file is the stable
   artifact.
6. **Empty results are results.** Every prompt ends with: "If you find
   nothing, say so explicitly and list what you inspected." The caller
   accepts that once and does not re-run.
7. **Verify claims before relaying.** Before presenting a bridged review or
   investigation to the user, check the important claims against the code.
   Before trusting a bridged implementation, check `git status` and the
   diff; do not trust "I pushed" from a GPT-family model.
8. **Name the model in whatever you report.** Prefix findings with the
   bridge id so the human can see which model said what.
9. **Never pass secrets in prompts.** Auth comes from the callee's own login
   or env var, documented per bridge.

## Bridge file format

```markdown
---
id: codex-cli
harness: codex                   # which harness this reaches
binary: codex                    # executable name; absolute path notes if ambiguous
reaches: [gpt-6-astra, gpt-6-1-sol, gpt-6-luna]   # model ids from core/models
auth: "ChatGPT login (codex login) or CODEX_API_KEY"
verified: local | docs | unverified   # how the flags were confirmed, with date
as_of: 2026-10-02
---

## Install
One or two lines, plus the version this was verified against.

## Detect
A shell snippet that returns 0 if the bridge is usable (binary present,
logged in). Used by the setup interview.

## One-shot, read-only
The exact command template with placeholders <P> <M> <E> <D> <OUT>,
including working-directory handling, the read-only flags, and how the
answer comes back (stdout, a file, a JSON field).

## One-shot, write-enabled
Same, for implementation on a worktree. State what the write flags allow.

## Flags
A small table: model, effort (and the accepted values), output format,
working dir, turn or budget limits, anything model-dependent.

## Prompting this model family
Five to ten lines: how prompts to this callee differ from prompts to
Claude. Include a short example prompt for a review and one for a bounded
implementation.

## Smoke test
A command that proves the bridge works in under a minute, and what output
means success.

## Gotchas
Bullets. Flag collisions, defaults that surprise, timeouts, exit codes,
things that are UNVERIFIED.
```

## Which bridge for which job

| Need | Preferred bridge | Notes |
|---|---|---|
| Second-family review of Claude-written code | `codex-cli` (Sol), else `grok-cli`, else `agy-cli` | Only if the user has that access |
| Deep root-cause investigation | `codex-cli` (Sol high) | Astra as escalation |
| Computer-use verification | `t3-code-mcp` if inside T3 Code; otherwise none from a CLI | Codex computer use is desktop-app only; say so rather than pretend |
| Bounded implementation on another model | `claude-cli` (from non-Claude harnesses), `codex-cli` | Always on a worktree |
| Bulk / cheap fan-out with programmatic verification | `openai-api` (Luna), `openrouter-api`, `ollama` | No tools; one-shot completions |
| Delegation from inside T3 Code | `t3-code-mcp` | Uses `delegate_task`, no shell needed |

The setup interview marks a bridge live only after its smoke test passes.
