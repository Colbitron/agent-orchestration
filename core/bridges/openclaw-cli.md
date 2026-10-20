---
id: openclaw-cli
harness: openclaw
binary: openclaw
reaches: [claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5, gpt-6-astra, gpt-6-1-sol, gpt-6-luna, gemini-3-8-flash, qwen3-8-27b, gpt-oss-20b, deepseek-v4-1-flash, mimo-v2-6-pro, glm-5-3]   # any provider/model its provider plugins and auth profiles cover (Anthropic, OpenAI, Google, OpenRouter, Ollama, ...); which exact models each provider exposes is unverified
auth: "stored auth profiles in ~/.openclaw (openclaw onboard, openclaw models auth login --provider <id>, or openclaw models auth setup-token --provider <id> on a TTY), reuse of an existing Claude Code login (agentRuntime claude-cli), or ANTHROPIC_API_KEY / OPENAI_API_KEY in the environment (--auth-env-only forces env and loads no config). Docs recommend an API key over subscription tokens for automation"
api_key_only: [anthropic]        # docs recommend an API key over subscription tokens for automation (auth above)
verified: docs                   # docs.openclaw.ai cli/agent, gateway/config-tools/tool-policy, providers/anthropic, install, read 2026-10-19 (about v2026.10.5); the openclaw binary is not on PATH here (~/.openclaw is from 2026.3.x), nothing below has been run
as_of: 2026-10-19
---
OpenClaw is a self-hosted assistant runtime: a Gateway that joins chat channels to an
embedded agent with tools, skills, sub-agents, MCP and ACP dispatch to coding harnesses.
`openclaw agent exec` is its headless entry point: one embedded turn, no Gateway, a temporary
state dir it cleans up afterwards, your ordinary config and stored credentials, and a working
directory per call. `<D>/AGENTS.md` is injected as project context.

## Install
`curl -fsSL https://openclaw.ai/install.sh | bash`, or
`npm install -g openclaw@latest --allow-scripts=openclaw` (Node 24.16+ or 26.1+; with an older
Node under nvm, run `nvm install 24` first), then `openclaw onboard` (`--install-daemon`
only if you want the Gateway as a service; the bridge does not need it). Update with
`openclaw update`; installs older than July 2026 must step through `2026.9.5` first
(https://docs.openclaw.ai/install/updating). Not on PATH here.

## Detect
```sh
command -v openclaw >/dev/null 2>&1 && { openclaw models status --check >/dev/null 2>&1; [ $? -ne 1 ]; }
```
`models status --check` exits 0 ok, 1 missing or expired credentials, 2 expiring (still
usable). Model ids for a provider: `openclaw models list --provider anthropic`. For a Claude id
also require `ANTHROPIC_API_KEY` or a stored key: subscription OAuth is not usable here (see
Subscriptions under Gotchas).

## One-shot, read-only
The prompt goes in on stdin (`--message-file -`), so quoting cannot break it. The deny list
removes `exec`, so the callee cannot run `git diff` itself: pipe the diff in after the prompt.
`git diff HEAD` covers staged and unstaged changes; use `git diff main...HEAD` for a branch,
and `git add -N` new files first or they are invisible.
```sh
. core/bridges/_timeout.sh
{ printf '%s\n\n' "<P>"; git -C <D> diff HEAD; } |
  with_timeout 1300 openclaw agent exec --cwd <D> --model <provider/model> --thinking <E> \
    --json --timeout 1200 \
    --config-override '{"tools":{"profile":"coding","deny":["group:runtime","group:sessions","group:automation","write","edit","apply_patch"]}}' \
    --message-file - > <OUT>.json 2> <OUT>.err
jq -e '.ok == true' <OUT>.json >/dev/null && jq -r '.final' <OUT>.json > <OUT>
```
There is no read-only flag, so the override is the guard. `profile` is pinned because exec's
`coding` default applies only where the config leaves `tools.profile` unset, and local
onboarding sets `full` (no core filtering: messaging, ui, nodes, automation and plugin tools
included); the docs say a configured profile "is never downgraded" by exec. Deny always wins
over profile and allow: `group:runtime` is `exec`, `process`, `code_execution`;
`group:sessions` holds `sessions_spawn`, which can start a write-capable ACP harness;
`group:automation` is cron, hooks, gateway and plugin management; `write`, `edit` and
`apply_patch` are the three mutating file tools (separate ids, so all three are needed) and
`read` stays. Each piece is documented, the combination has not been run end to end
(UNVERIFIED), so run reviews on a worktree anyway and check `git status` afterwards.

## One-shot, write-enabled
Only on a worktree. Under the `coding` profile (exec's default where the config sets none) or
onboarding's `full`, `exec` already allows writes under `--cwd` and host exec.
```sh
. core/bridges/_timeout.sh
printf '%s\n' "<P>" |
  with_timeout 2800 openclaw agent exec --cwd <WORKTREE> --model <provider/model> --thinking <E> \
    --json --timeout 2700 --message-file - > <OUT>.json 2> <OUT>.err
```

## Flags
| Need | Flag |
|---|---|
| One-shot | `openclaw agent exec "<P>"` (positional), or `--message-file <path\|->` (`-` = stdin; the 4 MiB file cap is documented on `openclaw agent`, which `exec` shares). Use `--model`; whether `exec` also takes `-m` is an open question (research §9) |
| Model | `--model <provider/model>` (`anthropic/claude-opus-5-5`, `openai/gpt-6-astra`, `google/gemini-3.1-pro-preview`, `ollama/qwen3.5:9b`); `--fallback <provider/model>` repeatable, requires `--model` |
| Effort | `--thinking off\|minimal\|low\|medium\|high`, plus provider levels such as `xhigh`, `adaptive`, `max`, `ultra` (unsupported levels are clamped with a notice; the value list is on the `openclaw agent` page, `exec` lists the flag without values) |
| Read-only | none; `--config-override '{"tools":{"deny":[...]}}'` as above. Overrides merge into the ordinary config: objects merge, arrays and scalars replace; repeat the flag to layer |
| Writes | the `exec` default; `--config-override '{"tools":{"profile":"full"}}'` for everything incl. plugin tools |
| Output | `--json` → one object on stdout: `ok`, `status` (`ok\|error\|timeout`), `final`, `payloads[]`, `model`, `provider`, `sessionId`, optional `usage`, `costUsd`, `assistantTurns`, `toolSummary`; failures add `error{message,kind}` |
| Working dir | `--cwd <D>` (agent workspace and tool cwd, default `$PWD`; `<D>/AGENTS.md` injected; `agents.defaults.contextInjection: "never"` turns that off) |
| Timeout | `--timeout <seconds>`, default 600 per model attempt, `0` disables; each `--fallback` gets a fresh budget |
| Config | default: your ordinary config plus stored credentials; `--config <path>` pins a file; `--isolated` ignores the ambient config and uses exec defaults only; `--auth-env-only` uses env keys only and loads no config (cannot combine with `--config` or `--config-override`) |
| State | temp dir by default, deleted after the run; `--state-dir <existing dir>` retains sessions but then needs exclusive ownership |
| Local models | `--code-mode direct\|auto\|code`, `--local-model-lean` (reduced tool surface) |
| Via the Gateway | `openclaw agent --agent <id> -m "<P>" --json [--session-id <id>] [--model ...] [--thinking ...]`: needs a running Gateway, no cwd flag, uses the agent's workspace; `--local` runs embedded but then needs the state dir |

## Prompting this model family
OpenClaw is a harness, not a model family: prompt in the dialect of the model you pick
(`claude-cli.md` style for `anthropic/*`, the literal style for GPT, Gemini and open-weights
ids). The callee sees the OpenClaw system prompt plus `<D>/AGENTS.md`, not the user's workspace
`SOUL.md`/`USER.md`, so state the task, repository and output format in full.

Review (literal style):
> Review the uncommitted changes in this repository (`git diff` output follows this prompt).
> Report correctness bugs only. For each: file:line, what breaks, how to trigger it. You have
> no shell and cannot edit; judge from the diff and the files you can read. If you find
> nothing, say so explicitly and list what you inspected.

Bounded implementation (literal style):
> Make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make the smallest
> possible changes. Run `npm test`; it must pass. Do not commit. If you make no progress after
> 3 attempts, stop and report what blocks you. List the files you changed. If you find nothing
> to change, say so explicitly and list what you inspected.

## Smoke test
```sh
cd "$TMPDIR" && . core/bridges/_timeout.sh && with_timeout 120 openclaw agent exec --cwd "$PWD" \
  --model <provider/model> --thinking low --json --timeout 90 "Reply with the single word OK" \
  < /dev/null | jq -r '.final'
```
Expected (docs, not run): `OK`, exit 0.

## Gotchas
- **`exec` does not need the Gateway stopped.** It creates its own temporary state dir and
  still reaches the stored logins. Only `--state-dir <dir>` (and `openclaw agent --local`)
  demand exclusive ownership and refuse to start while a Gateway owns that dir
  (`openclaw gateway stop` first).
- **Exit codes:** `exec` 0 ok, 1 model or result error (or cleanup failure after success),
  2 timeout, 130 SIGINT, 143 SIGTERM. The Gateway path returns 1 for a timeout. Also check
  `.ok` in the JSON. Exit 124 from the wrapper is "no result".
- **Timeout:** `--timeout` is per model attempt and each `--fallback` gets a fresh budget, so
  keep the outer `with_timeout` above the sum.
- **Read-only and env-only auth do not combine:** `--auth-env-only` rejects
  `--config-override`, so a review run with the deny list needs stored credentials.
- **Old installs.** `agent exec` is documented on the live docs (about 2026.10); whether it
  exists in builds from early 2026 is UNVERIFIED. Run `openclaw update` first, and
  `openclaw doctor --fix` to migrate an old state dir.
- **No sandbox.** File-tool limits stop at `--cwd`, but host `exec` is on by default and the
  docs say the restrictions "do not isolate broad shell access". Deny `group:runtime` or use a
  worktree.
- **Subscriptions.** The Claude CLI runtime and `claude setup-token` draw on the signed-in
  subscription; the docs recommend an API key for automation and warn that setup tokens
  expire and can be revoked.
- **No workspace bootstrap.** `--cwd <D>` makes `<D>` the run's workspace and `skipBootstrap`
  stops exec from creating bootstrap files there, so the user's workspace `AGENTS.md` and
  `SOUL.md` are not in the callee's prompt; only `<D>/AGENTS.md` is.
- **File tools stop at `<D>`.** The exec defaults set `tools.fs.workspaceOnly: true` where the
  config leaves it unset (a configured value is never downgraded). Whether
  `--config-override '{"tools":{"fs":{"workspaceOnly":false}}}'` lifts that is UNVERIFIED.
- `--json` puts one object on stdout; logs go to stderr. Do not parse `<OUT>.err`.
