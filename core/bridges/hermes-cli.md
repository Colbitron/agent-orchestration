---
id: hermes-cli
harness: hermes
binary: hermes                   # ~/.local/bin/hermes (checkout in ~/.hermes/hermes-agent/)
reaches: [claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5, gpt-6-astra, gpt-6-1-sol, gpt-6-luna, gemini-3-8-flash, grok-4-7, qwen3-8-27b, gpt-oss-20b, deepseek-v4-1-flash, mimo-v2-6-pro, glm-5-3]   # providers: anthropic, openai-api, openai-codex (ChatGPT OAuth), gemini, xai, openrouter, custom (Ollama/vLLM/LM Studio), plus Nous Portal models that have no kit profile. Which exact models each provider exposes is unverified
auth: "keys in ~/.hermes/.env (ANTHROPIC_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY, XAI_API_KEY, ...; `hermes config set OPENROUTER_API_KEY sk-...` writes them), OAuth via `hermes model` or `hermes auth add <provider>`. Claude Pro cannot use the Anthropic OAuth path and Claude Max draws only on extra-usage credits through it; use ANTHROPIC_API_KEY for Claude"
api_key_only: [anthropic]        # Claude Pro cannot use the Anthropic OAuth path; Max draws only extra-usage credits (auth above)
verified: docs                   # plus source: hermes-agent.nousresearch.com docs (reference/cli-commands, user-guide/cli, security, configuration) and hermes_cli/_parser.py, oneshot.py on main, read 2026-10-19 (v0.22.x); not tested against an install, nothing below has been run
as_of: 2026-10-19
---
Hermes Agent (Nous Research) is a Python assistant runtime: terminal agent, messaging
gateway, cron, subagents, and a learning loop that writes its own skills. Every CLI run,
including the one-shots below, is a **gateway client**: it discovers or starts the profile's
gateway (`hermes gateway ensure`), creates the session there, and attaches over a local
WebSocket. Two one-shot entry points exist: `hermes -z "<P>"` (final text only, approvals
auto-bypassed) and `hermes chat --oneshot -q|--query-file` (JSONL with tool events, approvals
denied by default). There is **no read-only file toolset**: `file` includes `write_file` and
`patch`, and `safe` has no file tools at all.

## Install
`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` (provisions its own
Python 3.14; `--non-interactive` skips the setup wizard), reload the shell, then run `hermes`
or `hermes setup` once and `hermes model` to add a provider. Update with `hermes update`.
Not tested against an install.

## Detect
```sh
command -v hermes >/dev/null 2>&1 && hermes config get model.default >/dev/null 2>&1
```
For a Claude id also require `ANTHROPIC_API_KEY` in `~/.hermes/.env` or the environment:
subscription OAuth is not usable here (see Subscriptions under Gotchas).
`hermes status` shows the active provider and model; `hermes gateway ensure --timeout 60`
prints one JSON object and exits 0 when the local runtime is ready; `hermes doctor` checks
the install.

## One-shot, read-only
Hard read-only means no `file` and no `terminal` toolset, so the callee cannot read the repo:
pipe what it must see in through `--query-file -` (nothing on stdin is shell-interpreted).
`git diff HEAD` covers staged and unstaged changes; use `git diff main...HEAD` for a branch,
and `git add -N` new files first or they are invisible.
```sh
. core/bridges/_timeout.sh
{ printf '%s\n\n' "<P>"; git -C <D> diff HEAD; } |
  with_timeout 1300 hermes chat --in <D> --oneshot -Q --ignore-rules --source tool \
    --toolsets safe -m <M> --provider <provider> --reasoning <E> --max-turns 60 \
    --format stream-json --query-file - > <OUT>.jsonl 2> <OUT>.err
tail -n 1 <OUT>.jsonl | jq -e '.type == "result" and .exit_code == 0' >/dev/null &&
  tail -n 1 <OUT>.jsonl | jq -r '.text' > <OUT>
```
`--toolsets safe` is `web_search`, `web_extract`, `vision_analyze`, `image_generate` only.
`--ignore-rules` skips `SOUL.md`, memory, preloaded skills and the repo's `AGENTS.md`, so the
callee starts clean and does not try to load the kit's own routing files. `--source tool`
keeps the session out of the user's session pickers.

`hermes -z "<P>"` is the simplest entry point when nothing has to be piped in: it prints the
final text and nothing else. It does **not** read stdin (source: `gateway_chat.py` reads stdin
only for `--query-file -`, and `-z` replaces the query; the docs' `hermes -z "summarize this"
< file.txt` example is misleading), so `git diff | hermes -z ...` would review nothing. Put the
content in the argument instead (one argument is capped at 128 KiB on Linux, about 256 KiB on
macOS), or use `--query-file -` above for anything large:
```sh
. core/bridges/_timeout.sh
with_timeout 1300 hermes -z "$(printf '%s\n\n' "<P>"; git -C <D> diff HEAD)" --in <D> -t safe \
    --ignore-rules -m <M> --provider <provider> --reasoning <E> > <OUT> 2> <OUT>.err < /dev/null
```
There is no soft read-only variant. `HERMES_WRITE_SAFE_ROOT` would guard `write_file` and
`patch`, but it is read by the gateway process (`agent/file_safety.py`), and the client forwards
only an allowlist of variables and drops every `HERMES_*` name (`agent/session_client_env.py`),
so setting it on the bridge command does nothing; set at gateway start it applies to every
session on that profile. A callee that must browse the tree gets `--toolsets file,terminal`
on a worktree, with `git status` checked afterwards (source-derived, not run).

## One-shot, write-enabled
Only on a worktree. `hermes chat -q` denies every approval instead of asking
(`approvals.single_query_mode: deny`), so pass `--yolo`; `hermes -z` already implies it.
```sh
. core/bridges/_timeout.sh
printf '%s\n' "<P>" |
  with_timeout 2800 hermes chat --in <WORKTREE> --oneshot -Q --ignore-rules --source tool --yolo \
    --toolsets file,terminal,web -m <M> --provider <provider> --reasoning <E> --max-turns 200 \
    --format stream-json --query-file - > <OUT>.jsonl 2> <OUT>.err
```

## Flags
| Need | Flag |
|---|---|
| One-shot | `hermes chat -q "<P>"` (`--query`; on a TTY it seeds an interactive session, so add `--oneshot` or `-Q`; non-TTY stdio implies it); `--query-file <path\|->` (exclusive with `-q`); `hermes -z "<P>"` = final text only, stdin ignored, approvals bypassed |
| Model | `-m, --model <M>` (`provider/model` as `hermes model` lists it, or a bare name the provider resolves); `--provider <id>` (`anthropic`, `openai-api`, `openai-codex`, `openrouter`, `gemini`, `xai`, `nous`, `custom` with `--base-url`/`--api-key`, or a name from `providers:` in config); with `-z`, `--provider` requires `-m`. `HERMES_INFERENCE_MODEL` is the env twin |
| Effort | `--reasoning none\|minimal\|low\|medium\|high\|xhigh\|max\|ultra` (source: `_parser.py`); an unknown value logs a warning and keeps the configured level. Config `agent.reasoning_effort`, default medium |
| Tools | `-t, --toolsets <csv>`: `safe`, `file`, `terminal`, `web`, `search`, `session_search`, `vision`, `delegation`, `all`, ...; unset = the profile's CLI toolsets |
| Approvals | `chat -q`: denied by default; `--yolo` (`HERMES_YOLO_MODE=1`) approves everything except `approvals.deny` globs and the hardline blocklist; `--accept-hooks` (`HERMES_ACCEPT_HOOKS=1`) for unseen shell hooks. `-z` sets both |
| Output | `--format stream-json` (`chat` only; needs `-q` or `--query-file`, implies `-Q`): JSONL, events `system`/`text`/`tool_use`/`tool_result`, last line `result` with `text`, `exit_code`, `session_id`, `tokens`, `duration_ms`, `error`. `-Q` plain: final text on stdout, `session_id:` on stderr. `-z`: text only |
| Working dir | `--in <D>` (client-side `cd`; the directory is frozen into the session). `-w` is refused in gateway mode |
| Limits | `--max-turns <N>` (tool iterations per turn, default 500). **No wall clock inside Hermes:** `--run-budget` is refused by the gateway client (exit 2), so the outer `with_timeout` is the only deadline |
| Context | `--ignore-rules` (no `SOUL.md`, memory, `AGENTS.md`, `CLAUDE.md`, preloaded skills); `--ignore-user-config` (built-in defaults, `.env` keys still load); `--safe-mode` (both, plus no plugins, hooks or MCP; needs an explicit `--provider` and `-m`); `-p, --profile <name>`; `-s <skill>` preloads a skill |
| Persistence | every run lands in `~/.hermes/state.db` and in the gateway's session list; `--source tool` (or the one-shot default `oneshot`) hides it from pickers; `-z --usage-file <path>` writes a JSON cost report |

## Prompting this model family
Hermes is a harness, not a model family: prompt in the dialect of the model you pick
(`claude-cli.md` style for `anthropic`, the literal style for GPT, Gemini, Grok and
open-weights ids). With `--ignore-rules` the callee has no repo rules, so state the repo path,
test command and output format in the prompt. The diff arrives on stdin, so say so.

Review (literal style; the diff is piped in, see above):
> Review the uncommitted changes in this repository (`git diff` output follows this prompt).
> Report correctness bugs only. For each: file:line, what breaks, how to trigger it. You have
> no file or shell tools; judge from the diff. If you find nothing, say so explicitly and list
> what you inspected.

Bounded implementation (literal style):
> Make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make the smallest
> possible changes. Run `npm test`; it must pass. Do not commit. If you make no progress after
> 3 attempts, stop and report what blocks you. List the files you changed. If you find nothing
> to change, say so explicitly and list what you inspected.

## Smoke test
```sh
cd "$TMPDIR" && . core/bridges/_timeout.sh && with_timeout 120 hermes -z "Reply with the single word OK" \
  -t safe --ignore-rules -m <M> --provider <provider> < /dev/null
```
Expected (docs, not run): `OK` on stdout, nothing on stderr, exit 0. The JSONL path:
`hermes chat --oneshot -Q --format stream-json -q "Reply with the single word OK" | tail -n 1 | jq -r .text`.

## Gotchas
- **Every call is a gateway client.** The first run starts the profile's gateway if none is
  up (`hermes gateway ensure`); it is a local process, not an installed service, and whether
  it exits when idle is UNVERIFIED (`hermes gateway stop` stops it). Options that need an
  in-process agent are refused with exit 2: `--run-budget`, `-w`/`--worktree`, `--image`,
  `-v`, `--compact`, `--no-restore-cwd`.
- **A timeout does not cancel the turn.** The gateway client's interrupt handler prints
  `Detached; accepted work continues at the gateway.` and exits 130 (source:
  `gateway_chat.py`); cancelling is an interactive-only action. `with_timeout` sends TERM
  (gtimeout path) or INT (perl path), then KILL, so a wrapper exit of 124 means "no result"
  **and the turn is probably still running at the gateway**. Always check
  `hermes sessions list` after a 124 and stop the work (`hermes gateway stop` stops everything
  on that profile) before re-running, or two callees will race on the same worktree.
- **No read-only file toolset.** `file` always includes `write_file` and `patch`. Pipe the
  content in, or use the soft variant on a worktree.
- **Approvals are denied, not asked, in `chat -q`** (`approvals.single_query_mode: deny`), so
  a write run without `--yolo` fails on the first flagged command instead of hanging. `-z`
  bypasses approvals and hooks on its own, so never use `-z` with `file`/`terminal` on a
  checkout you care about.
- **Exit codes** differ by entry point. `chat` one-shot: 0 ok; 1 failed, partial, turn budget
  hit, or never ran (credentials, init, `--resume` miss); 2 unsupported option; 3 input
  required (a `clarify` or approval prompt in a finite run: the client detaches without
  cancelling, so the turn stays pending at the gateway, as after a wrapper 124; source:
  `gateway_chat_view.py`); 130 interrupted; 75 provider rate limit or quota (Kanban workers
  only). `hermes -z`: 0 ok; 1 completed but no text; 2 failed, partial or bad flags; 130
  interrupted. Judge by the exit code, not by stdout being non-empty. Wrapper exit 124 is
  "no result".
- **Flag collisions:** `-p` is `--profile` (not prompt); `-q` is the prompt; `-Q` is quiet;
  `-z` is the scripted one-shot; `-s` is `--skills`; `-c` is `--continue`; `-r` is `--resume`;
  `-t` is `--toolsets`; `-w` is `--worktree` (refused here).
- **Subscriptions.** Claude Pro cannot use the Anthropic OAuth path and Claude Max only spends
  extra-usage credits through it (community reports of "out of extra usage" errors even then);
  use `ANTHROPIC_API_KEY`, or prefer `claude-cli` for Claude. The docs carry no equivalent
  warning for ChatGPT/Codex OAuth.
- The user's `hooks:` block in `~/.hermes/config.yaml` runs for bridged calls too; shell hooks
  that have not been consented to prompt (or fail headless) unless `--accept-hooks` is passed.
