---
id: grok-cli
harness: grokbuild
binary: grok                     # ~/.grok/bin/grok (also installs ~/.grok/bin/agent, which shadows Cursor's `agent`)
reaches: [grok-4-7]
auth: "grok login (grok.com; SuperGrok / X Premium+ [2nd]; --device-auth for headless; tokens in ~/.grok/auth.json, 7-day expiry) or XAI_API_KEY (takes precedence; recommended for headless)"
verified: local                  # grok --help, grok login --help, ~/.grok/README.md, grok 1.0.0; smoke test NOT run (not logged in)
as_of: 2026-10-02
---

## Install
`curl -fsSL https://x.ai/cli/install.sh | bash`; update with `grok update`. Installs both
`grok` and `agent` into `~/.grok/bin`. Verified against `grok 1.0.0 (3cd0d0cbcebe) [stable]`.

## Detect
```sh
command -v grok >/dev/null 2>&1 && { [ -n "$XAI_API_KEY" ] || [ -s "$HOME/.grok/auth.json" ]; }
```
There is no login-status subcommand in 1.0.0. On 2026-10-02 this machine had neither
`XAI_API_KEY` nor `~/.grok/auth.json`, so the bridge is **not live** until `grok login`.

## One-shot, read-only
```sh
perl -e 'alarm shift; exec @ARGV' 1200 \
  grok -p "<P>" -m <M> --reasoning-effort <E> --sandbox read-only --permission-mode plan \
    --output-format json --cwd <D> < /dev/null > <OUT>.json 2> <OUT>.err
jq -r '.text' <OUT>.json > <OUT>
```
`--sandbox read-only` is OS-enforced (Seatbelt on macOS): reads everywhere, writes only to
`~/.grok/`, child network blocked. Alternative or extra guard: `--tools read_file,grep,list_dir`
(headless only; removes the shell). If plan mode produces a plan instead of findings, swap
`--permission-mode plan` for `--always-approve`: the sandbox still blocks writes.

## One-shot, write-enabled
Only on a worktree. `--always-approve` auto-approves every tool; `--sandbox workspace` limits
writes to cwd + `/tmp` + `~/.grok/`.
```sh
perl -e 'alarm shift; exec @ARGV' 2700 \
  grok -p "<P>" -m <M> --reasoning-effort <E> --always-approve --sandbox workspace \
    --max-turns 200 --output-format json --cwd <WORKTREE> < /dev/null > <OUT>.json 2> <OUT>.err
```
UNVERIFIED: whether `--sandbox workspace` lets `git commit` in a linked worktree write to the
main repo's `.git`. Default: the orchestrator commits after the callee finishes.

## Flags
| Need | Flag (all in 1.0.0 `--help`) |
|---|---|
| One-shot | `-p, --single "<P>"`; `--prompt-file <PATH>`; `--prompt-json <JSON>`; stdin pipes in |
| Model | `-m, --model <id>`; profile id -> `grok-4.7`. `grok models` lists what the account has |
| Effort | `--reasoning-effort` (alias `--effort`) `none\|minimal\|low\|medium\|high\|xhigh\|max` (+ per-model ids like `deep`) |
| Output | `--output-format plain\|json\|streaming-json\|streaming-messages-json` (default `plain`) |
| Structured | `--json-schema '<schema>'` (implies json) |
| Sandbox | `--sandbox off\|workspace\|read-only\|strict` (env `GROK_SANDBOX`; values from README) |
| Permissions | `--permission-mode default\|acceptEdits\|auto\|dontAsk\|bypassPermissions\|plan`; `--always-approve`; `--allow`/`--deny "<rule>"` |
| Tools | `--tools a,b` / `--disallowed-tools a,b` (headless only; `Agent` blocks subagents) |
| Turn cap | `--max-turns N` (headless only) |
| Working dir | `--cwd <CWD>` |

## Prompting this model family
The kit has no Grok-specific prompting evidence; the README groups Grok with GPT: simple,
literal prompts. Name the review target (diff, branch, PR) and the question, ask it to mark
what it could not confirm, make "nothing found" a valid answer, and cap effort at `high`
with a bounded scope: Grok 4.7 is token-hungry.

Review:
> Review the uncommitted changes in this repository (`git diff`). Report correctness bugs only.
> For each: file:line, what breaks, how to trigger it, and whether you confirmed it by reading
> the code. Do not edit files. If you find nothing, say so explicitly and list what you inspected.

Bounded implementation:
> Make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make the smallest
> possible changes. Run `npm test`; it must pass. Do not commit. If you make no progress after
> 3 attempts, stop and report what blocks you. List the files you changed. If you find nothing
> to change, say so explicitly and list what you inspected.

## Smoke test
```sh
perl -e 'alarm shift; exec @ARGV' 120 grok -p "Reply with the single word OK" -m grok-4.7 \
  --reasoning-effort low --sandbox read-only --tools read_file --output-format json \
  --cwd "$TMPDIR" < /dev/null | jq -r '.text'
```
Expected (README, **not run**: not logged in on 2026-10-02): `OK`, exit 0. JSON shape:
`{text, stopReason, sessionId, requestId}`. Whether `grok-4.7` is offered to this account in
CLI 1.0.0 is UNVERIFIED (the local models cache lists only `grok-4.5`); run `grok models` first.

## Gotchas
- **`agent` on PATH is Grok.** `~/.grok/bin/agent` and `~/.local/bin/agent` both resolve to the
  grok binary and shadow Cursor's CLI. Call this bridge as `grok`, never `agent`.
- **Exit codes:** not documented for headless; treat non-zero as failure and check `.text`.
- **Timeout:** no wall-clock flag; the bash tool defaults to 120 s (`[toolset.bash] timeout_secs`).
  Perl alarm kills with SIGALRM (exit 142, no JSON). Prefer
  `. core/bridges/_timeout.sh; with_timeout 1200 grok -p ...` (exit 124). Either is "no result".
- **Always set a permission mode or `--always-approve`.** Headless behaviour with neither is UNVERIFIED.
- **JSON:** answer in `.text` (not `.result`); `.sessionId` for follow-ups.
- **cwd:** `--cwd <D>`; rules discovery scans repo root down to cwd.
- **`-p` is `--single`** (one-shot prompt). In `codex`, `-p` is `--profile`. **`-s` is
  `--session-id` for a new conversation only**; resume needs `--resume`/`-c`.
- `--no-auto-update` is not in 1.0.0 help; set `[cli] auto_update = false` in `~/.grok/config.toml`.
- Grok loads `CLAUDE.md`, `.claude/skills`, `.claude/agents`, `.mcp.json` and `~/.claude.json`
  MCP servers: a broken Claude MCP config can slow or break Grok startup.
