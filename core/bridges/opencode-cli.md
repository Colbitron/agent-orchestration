---
id: opencode-cli
harness: opencode
binary: opencode
reaches: []                      # mainly open-weights models with no core/models profile; any provider/model it has auth for
auth: "opencode auth login (API keys, ChatGPT Plus/Pro, GitHub Copilot, GitLab Duo, OpenCode Zen/Go) or provider env vars. NOT Claude Pro/Max"
verified: docs                   # opencode is not installed on this machine
as_of: 2026-10-02
---
Use OpenCode to reach open-weights models (OpenRouter, Together, Groq, Fireworks, Cerebras,
DeepInfra, Ollama, LM Studio, llama.cpp, Moonshot/Kimi, Z.AI/GLM, MiniMax, DeepSeek) with tools.
**Claude Pro/Max subscription login is not supported**: the docs say "Anthropic explicitly
prohibits" it and the bundled plugins were removed in 1.3.0. Claude via OpenCode needs an
API key; prefer `claude-cli` for Claude.

## Install
`curl -fsSL https://opencode.ai/install | bash`, `npm install -g opencode-ai`, or
`brew install anomalyco/tap/opencode`. Not installed here.

## Detect
```sh
command -v opencode >/dev/null 2>&1
```
Provider auth is per model; a passing smoke test on the target `provider/model` is the check.

## One-shot, read-only
```sh
perl -e 'alarm shift; exec @ARGV' 1200 \
  opencode run "<P>" -m <provider/model> --variant <E> --agent plan --dir <D> \
    < /dev/null > <OUT> 2> <OUT>.err
```
Default `--format` prints text to stdout; whether that includes tool/progress lines besides
the final answer is UNVERIFIED. `--agent plan` is the built-in analysis-only primary agent;
how strictly it blocks edits is UNVERIFIED. For a hard read-only guarantee, also deny edits
inline: `OPENCODE_PERMISSION='<json>'` (schema per opencode.ai/docs/permissions; not tested).

## One-shot, write-enabled
Only on a worktree. The default `build` agent may edit; `--auto` approves every permission
that is not explicitly denied.
```sh
perl -e 'alarm shift; exec @ARGV' 2700 \
  opencode run "<P>" -m <provider/model> --variant <E> --auto --dir <WORKTREE> \
    < /dev/null > <OUT> 2> <OUT>.err
```

## Flags
| Need | Flag |
|---|---|
| One-shot | `opencode run "<P>"` (or `--command <cmd>` with message args) |
| Model | `-m, --model provider/model`: `openrouter/xiaomi/mimo-v2.6-pro`, `ollama/<id>` |
| Effort | `--variant <name>` (provider-specific; values depend on the model) |
| Agent | `--agent plan` (read-only intent) / default `build` |
| Approve all | `--auto` |
| Output | `--format default\|json` (json = raw event stream, not one object) |
| Working dir | `--dir <path>` |
| Reproducible | `--pure` (no external plugins) |
| Server reuse | `--attach http://localhost:4096`, `--port` |

Provider/model ids are `<provider>/<model-id>` as listed on models.dev / the provider. The
OpenRouter id above is from `research/model-gaps.md`; other open-weights ids are unverified.

## Prompting this model family
Open-weights models get the literal style: short imperatives, exact target, exact output,
stop condition, escape hatch. Smaller models lose track of long prompts; keep one task per
call and verify output programmatically. OpenCode loads `AGENTS.md` (or `CLAUDE.md` fallback).

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
perl -e 'alarm shift; exec @ARGV' 120 opencode run "Reply with the single word OK" \
  -m <provider/model> --agent plan --dir "$TMPDIR" < /dev/null
```
Expected (docs, not run): output ending in `OK`, exit 0. Exact stdout shape: UNVERIFIED.

## Gotchas
- **Not Claude Pro/Max.** Do not plan on a Claude subscription through OpenCode.
- **Exit codes:** not documented; treat non-zero as failure and also check `<OUT>` is non-empty.
- **Timeout:** none documented. Perl alarm kills with SIGALRM (exit 142). Prefer
  `. core/bridges/_timeout.sh; with_timeout 1200 opencode run ...` (exit 124). Either is "no result".
- **Possible silent hang:** default permissions are mostly `allow`, but `doom_loop` and
  `external_directory` are `ask`. What `run` does with an `ask` and no `--auto` is UNVERIFIED;
  it may wait forever, so the timeout wrapper is mandatory.
- **JSON:** `--format json` is a raw event stream; extracting the last assistant text has an
  UNVERIFIED shape. Prefer default text output captured to a file.
- **cwd:** `--dir <D>`; config and `AGENTS.md` discovery walk up from that dir.
- `-p` is not a prompt flag here (prompt is positional after `run`); in `codex`, `-p` is `--profile`.
- `.env` reads are denied by default.
