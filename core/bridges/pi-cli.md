---
id: pi-cli
harness: pi
binary: pi
reaches: []                      # no core/models profile lists pi; reaches any provider/id it has a key or login for
auth: "/login in the TUI (OAuth or API key, saved to ~/.pi/agent/auth.json), or per-provider env vars (ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, XAI_API_KEY, OPENROUTER_API_KEY, ...)"
verified: docs                   # pi is not installed on this machine
as_of: 2026-10-02
---
Pi is Mario Zechner's minimal terminal coding agent (now Earendil Inc., pi.dev). It has **no
approval system**: it "does not ask for approval before every tool call". The only read-only
guard is restricting tools with `--tools`. No subagents, no plan mode, by design.

## Install
`curl -fsSL https://pi.dev/install.sh | sh` or
`npm install -g --ignore-scripts @earendil-works/pi-coding-agent`; update with `pi update`.
Not installed here.

## Detect
```sh
command -v pi >/dev/null 2>&1 && pi auth check --provider <provider> --json >/dev/null 2>&1
```
`pi auth check` exits 0 ready, 1 not_ready, 2 invalid.

## One-shot, read-only
No cwd flag: `cd` first. `-p` prints the final assistant text to stdout.
```sh
cd <D> && perl -e 'alarm shift; exec @ARGV' 1200 \
  pi -p "<P>" --model <provider/id> --thinking <E> \
    --tools read,grep,find,ls --no-session --no-approve \
    < /dev/null > <OUT> 2> <OUT>.err
```
`--tools read,grep,find,ls` removes `bash`, `edit`, `write`: this is the **only** read-only
guard. `--no-approve` (`-na`) declines project trust, so project `.pi/` resources (SYSTEM.md,
extensions, MCP) are skipped; context files (`AGENTS.md`/`CLAUDE.md`) still load.

## One-shot, write-enabled
Only on a worktree. Default tools are `read,bash,edit,write` and nothing asks first: bash can
run anything the user can.
```sh
cd <WORKTREE> && perl -e 'alarm shift; exec @ARGV' 2700 \
  pi -p "<P>" --model <provider/id> --thinking <E> --no-session --no-approve \
    < /dev/null > <OUT> 2> <OUT>.err
```

## Flags
| Need | Flag |
|---|---|
| One-shot | `-p, --print "<P>"`; piped stdin is prepended; use `--` before a prompt starting with `-` |
| Model | `--model <pattern>`: `provider/id`, optional `:thinking` suffix (`sonnet:high`); `--provider` needs `--model` |
| Effort | `--thinking off\|minimal\|low\|medium\|high\|xhigh\|max` (clamped to the model) |
| Tools | `--tools read,grep,find,ls` (read-only); default `read,bash,edit,write` |
| Output | `-p` = plain final text; `--mode json` = JSONL events; `--mode rpc` long-lived |
| Working dir | none; `cd` (cwd drives config, discovery and sessions) |
| Project trust | `-a/--approve`, `-na/--no-approve` (default `ask` skips project `.pi/`) |
| Persistence | `--no-session` |
| Prompt | `--system-prompt`, `--append-system-prompt` (`<text\|path>`); `-nc` no context files |

## Prompting this model family
Pi is a harness; prompt in the dialect of the model you pick: `claude-cli.md` style for
`anthropic/*`, the literal style for GPT, Gemini, Grok and open-weights ids. Pi's system
prompt is minimal, so state the environment (repo path, test command) explicitly.

Review (literal style):
> Review the uncommitted changes in this repository (`git diff` output is below). Report
> correctness bugs only. For each: file:line, what breaks, how to trigger it. If you find
> nothing, say so explicitly and list what you inspected.

(With `--tools read,grep,find,ls` there is no bash, so pipe the diff in:
`git diff | pi -p "<P>" ...`, or name the files to read.)

Bounded implementation (literal style):
> Make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make the smallest
> possible changes. Run `npm test`; it must pass. Do not commit. If you make no progress after
> 3 attempts, stop and report what blocks you. List the files you changed. If you find nothing
> to change, say so explicitly and list what you inspected.

## Smoke test
```sh
cd "$TMPDIR" && perl -e 'alarm shift; exec @ARGV' 120 pi -p "Reply with the single word OK" \
  --model <provider/id> --thinking low --tools read --no-session --no-approve < /dev/null
```
Expected (docs, not run): stdout `OK`, exit 0.

## Gotchas
- **No approvals at all.** Forgetting `--tools` on a review gives the callee full write and
  shell access. Never run the write variant outside a worktree.
- **Exit codes:** for `-p`, not documented beyond `pi auth check` (0/1/2); treat non-zero as
  failure and check `<OUT>` is non-empty.
- **Timeout:** no wall-clock flag (`httpIdleTimeoutMs` 300000). Perl alarm kills with SIGALRM
  (exit 142). Prefer `. core/bridges/_timeout.sh; with_timeout 1200 pi -p ...` (exit 124).
  Either is "no result".
- **JSON:** `--mode json` is an event stream (session header, `agent_start`, `turn_start`,
  `message_*`...), no single result field. Use `-p` plain text for bridging.
- **cwd:** no flag; always `cd <D>` first.
- `-p` means print here; in `codex`, `-p` is `--profile`.
- Which consumer subscriptions `/login` supports is UNVERIFIED; Anthropic prohibits using
  Claude Pro/Max in third-party harnesses (see `opencode-cli.md`). Use `ANTHROPIC_API_KEY`.
