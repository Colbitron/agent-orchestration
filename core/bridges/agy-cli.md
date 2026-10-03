---
id: agy-cli
harness: antigravity
binary: agy
reaches: [gemini-3-8-flash]      # the gemini-3-8-flash profile lists only gemini-cli in invoke_via so far
auth: "Google sign-in (free / AI Pro / Ultra; OS keyring, browser over SSH), or GEMINI_API_KEY with \"modelProvider\": \"gemini\" in ~/.gemini/antigravity-cli/settings.json [2nd]"
verified: docs                   # agy is not installed on this machine; some flags are from a secondary source
as_of: 2026-10-02
---
Antigravity CLI is Google's closed-source successor to Gemini CLI (released 2026-05-19). It is
the path for consumer Google plans after 2026-06-18. It is the only harness with a built-in
wall clock, `--print-timeout`, and its **default is 5m**: always raise it.

## Install
`curl -fsSL https://antigravity.google/cli/install.sh | bash`; self-updates. Not installed here.

## Detect
```sh
command -v agy >/dev/null 2>&1
```
No documented login-status command; a passing smoke test is the login check.
Do not use `agy models` as a probe without `< /dev/null` (hangs on an open non-TTY stdin).

## One-shot, read-only
```sh
perl -e 'alarm shift; exec @ARGV' 1860 \
  agy -p "<P>" --model <M> --effort <E> --mode plan --output-format json \
    --cwd <D> --print-timeout 30m < /dev/null > <OUT>.json 2> <OUT>.err
jq -r '.status' <OUT>.json; jq -r '.response' <OUT>.json > <OUT>
```
The outer alarm (31 min) is a backstop set just above `--print-timeout` so agy's own timeout
fires first and can still report `status`. `--mode plan` as read-only: semantics UNVERIFIED.

## One-shot, write-enabled
Only on a worktree. `accept-edits` auto-accepts edits [2nd]; `--dangerously-skip-permissions`
approves everything.
```sh
perl -e 'alarm shift; exec @ARGV' 2760 \
  agy -p "<P>" --model <M> --effort <E> --mode accept-edits --output-format json \
    --cwd <WORKTREE> --print-timeout 45m < /dev/null > <OUT>.json 2> <OUT>.err
```
Fine-grained allow/ask/deny lists live in `~/.gemini/antigravity-cli/settings.json`
(`read_file`, `write_file`, `read_url`, `execute_url`, `command`, `unsandboxed`, `mcp`; Deny > Ask > Allow).

## Flags
| Need | Flag |
|---|---|
| One-shot | `-p, --print, --prompt "<P>"`; `--input-format text\|stream-json` |
| Model | `--model <slug>`, e.g. `gemini-3.8-flash-high`. **Persists across sessions: always pass it** |
| Effort | `--effort low\|medium\|high` |
| Mode | `--mode accept-edits\|plan` [2nd]; `--dangerously-skip-permissions` |
| Output | `--output-format text\|json\|stream-json`; `--json-schema <schema\|file\|type>` [2nd] |
| Working dir | `--cwd` / `--workspace <D>`; `--add-dir <path>` |
| Timeout | `--print-timeout <dur>` (default `5m`) |
| Resume | `-c/--continue`, `--conversation <id>` |

## Prompting this model family
No Gemini-specific prompting evidence in the kit. Use the literal non-Claude style: short
imperatives, exact target, exact output, stop condition. Agy reads `GEMINI.md` and `AGENTS.md`,
but put anything critical in the prompt anyway.

Review:
> Review the uncommitted changes in this repository (`git diff`). Report correctness bugs only.
> For each: file:line, what breaks, how to trigger it. Do not edit files. If you find nothing,
> say so explicitly and list what you inspected.

Bounded implementation:
> Make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make the smallest
> possible changes. Run `npm test`; it must pass. Do not commit. If you make no progress after
> 3 attempts, stop and report what blocks you. List the files you changed. If you find nothing
> to change, say so explicitly and list what you inspected.

## Smoke test
```sh
perl -e 'alarm shift; exec @ARGV' 150 agy -p "Reply with the single word OK" \
  --model gemini-3.8-flash-high --effort low --output-format json --cwd "$TMPDIR" \
  --print-timeout 2m < /dev/null | jq -r '.status, .response'
```
Expected (docs, not run): a success `status` then `OK`, exit 0. JSON shape:
`{conversation_id, status, response, duration_seconds, num_turns, usage{...}}`.
Exact `status` values: UNVERIFIED.

## Gotchas
- **Always raise `--print-timeout`.** The 5m default silently cuts real reviews short. Use
  20m/30m/45m to match the README defaults and keep the outer wrapper ~1 min longer.
- **Always redirect stdin** (`< /dev/null`): agy can hang when stdin is a held-open non-TTY
  pipe (issue #882, reported for `agy models`) [2nd]. `_timeout.sh`'s perl path also needs it.
- **Exit codes:** 0 success, non-zero on error with the reason on stderr and in `.status`.
  The exit code and `status` value when `--print-timeout` fires: UNVERIFIED.
- **Timeout:** if the outer perl alarm fires first, SIGALRM kills agy (exit 142, no JSON).
  `. core/bridges/_timeout.sh; with_timeout 1860 agy -p ...` exits 124. Either is "no result".
- **JSON:** answer in `.response`; check `.status`. Not `.result` (Claude/Cursor) or `.text` (Grok).
- **cwd:** `--cwd <D>` (or `--workspace`); otherwise the process cwd.
- `-p` means print/prompt here; in `codex`, `-p` is `--profile`.
- `--model` persists: a call without it reuses whatever the last session picked.
- Global config moved to `~/.gemini/antigravity-cli/`; MCP to `mcp_config.json` (`serverUrl`).
