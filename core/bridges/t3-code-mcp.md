---
id: t3-code-mcp
harness: t3-code
binary: null                     # not a CLI: the `t3-code` MCP server T3 Code injects into every provider session
reaches: [claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5, gpt-6-astra, gpt-6-1-sol]
auth: "none from the caller: the MCP server is authenticated by T3 Code; each target provider uses its own login (claude auth login, codex login, agent login, grok login, opencode auth login)"
verified: docs                   # T3 Code repo docs (docs/orchestration-v2/orchestrator-mcp-server.md); not run here
as_of: 2026-10-02
---
Use this bridge only when the orchestrator itself is running **inside T3 Code**. Delegation is
native and durable there: the callee runs in a visible child thread, with no shell-out.
`reaches` lists profiles whose `access.harnesses` include `t3-code`; T3 can also drive Cursor,
Grok Build, OpenCode, Pi and Antigravity, so ask `orchestrator_capabilities` what is live.

## Install
Not installed by the kit. T3 Code: `curl -fsSL https://t3.codes/install.sh | sh`, desktop
builds, or `npx t3@latest`. The MCP server comes with it.

## Detect
The orchestrator is inside T3 Code when its tool list contains the `t3-code` server's tools:
in Claude, `mcp__t3-code__delegate_task` and `mcp__t3-code__orchestrator_capabilities`. In
Codex the server is injected via `-c mcp_servers.t3-code.url=http://127.0.0.1:<port>/mcp`.
No shell check exists; if those tools are absent, this bridge is not usable.

## One-shot, read-only
Call the MCP tool (no shell). Shape of the arguments:
```json
{ "task": "<P>",
  "target": { "driverKind": "<codex|claude|...>", "model": "<M>" },
  "role": "review",
  "mode": "wait",
  "timeoutMs": 1200000,
  "runtimeMode": "approval-required",
  "interactionMode": "plan" }
```
`target` takes `providerInstanceId` **or** `driverKind`, plus `model`. Accepted `driverKind`
strings and model ids: get them from `orchestrator_capabilities` (UNVERIFIED list).
`interactionMode: "plan"` + `runtimeMode: "approval-required"` is the closest read-only
setting; how strictly it blocks edits is UNVERIFIED. The answer comes back in the tool result
(`mode: "wait"`); its exact shape is UNVERIFIED.

## One-shot, write-enabled
```json
{ "task": "<P>", "target": { "driverKind": "<kind>", "model": "<M>" },
  "role": "implementation", "mode": "async", "timeoutMs": 2700000,
  "runtimeMode": "auto-accept-edits", "interactionMode": "default" }
```
With `mode: "async"`, poll `task_status` until done. Use a T3 worktree thread for writes
(T3 manages worktrees; `t3_thread_launch` exists, parameters UNVERIFIED). `full-access`
equals T3's default "Full access" mode; do not use it for delegated work.

## Flags
| Param | Values |
|---|---|
| `task` | the full self-contained prompt |
| `target` | `{providerInstanceId \| driverKind, model}` |
| `role` | `implementation\|research\|review\|design\|test\|general` |
| `mode` | `wait` (block for result) \| `async` (poll `task_status`) |
| `timeoutMs` | wall clock in ms: 1200000 review, 2700000 implementation, 1800000 verification |
| `runtimeMode` | `inherit\|approval-required\|auto-accept-edits\|full-access` |
| `interactionMode` | `inherit\|plan\|default` |
Other tools on the server (11 total): `orchestrator_capabilities`, `task_status`, cancel,
`t3_thread_launch`, thread list/read/send. Exact names besides the quoted ones: UNVERIFIED.

## Prompting this model family
Prompt in the target model's dialect: `claude-cli.md` for Claude targets, `codex-cli.md` for
GPT targets. The child gets **only** `task`, no parent history, so it must be self-contained.
It runs with the user's native config (CLAUDE.md, AGENTS.md, skills).

Review (GPT target, literal):
> Review the uncommitted changes in /repo. Report correctness bugs only. For each: file:line,
> what breaks, how to trigger it. Do not edit files. If you find nothing, say so explicitly
> and list what you inspected.

Bounded implementation (GPT target, literal):
> In /repo-wt, make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make the
> smallest possible changes. Run `npm test`; it must pass. Do not commit or push. If you make no
> progress after 3 attempts, stop and report what blocks you. List the files you changed. If you
> find nothing to change, say so explicitly and list what you inspected.

## Smoke test
1. Call `orchestrator_capabilities`; success = a list of provider instances/drivers.
2. Call `delegate_task` with `task: "Reply with the single word OK"`, `role: "general"`,
   `mode: "wait"`, `timeoutMs: 120000`, `interactionMode: "plan"` and a cheap target.
Success: the result contains `OK` and a child thread appears in T3. Not run (UNVERIFIED shape).

## Gotchas
- **Not a CLI:** no `-p`, no exit codes, no stdout. (`-p` collisions such as `codex -p` =
  `--profile` are irrelevant here, but matter if you fall back to a CLI bridge.)
- **Timeout:** `timeoutMs` replaces the shell wrapper (`perl -e 'alarm ...'` /
  `core/bridges/_timeout.sh` do not apply). What a timed-out task returns is UNVERIFIED; treat
  it as "no result" and check `task_status`.
- **Results:** a JSON field name for the answer is not documented; read the tool result text
  and, if needed, the child thread via the thread-read tool.
- **cwd:** the child runs in the thread's project/worktree chosen by T3, not the caller's cwd.
  State the absolute repo path in `task` anyway.
- **Default permission mode in T3 is Full access.** Always pass `runtimeMode` explicitly; never
  rely on `inherit` for review work.
- ACP providers (Grok, Antigravity) have no native subagents; T3 substitutes child threads.
- The README routes computer-use verification here, but the research documents no
  computer-use path through `delegate_task`; whether any T3 target can drive a desktop is
  UNVERIFIED. Codex computer use itself is ChatGPT-desktop-app only.
