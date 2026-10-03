---
id: gemini-cli
harness: gemini-cli
binary: gemini
reaches: [gemini-3-8-flash]
auth: "PAID only since 2026-06-18: GEMINI_API_KEY, or Vertex (GOOGLE_CLOUD_PROJECT + GOOGLE_CLOUD_LOCATION + ADC/GOOGLE_APPLICATION_CREDENTIALS/GOOGLE_API_KEY), or Code Assist Standard/Enterprise"
verified: docs                   # gemini is not installed on this machine
as_of: 2026-10-02
---
Legacy. On 2026-06-18 Google stopped serving free, AI Pro and AI Ultra sign-ins in Gemini
CLI and moved consumers to Antigravity (`agy-cli.md`). Use this bridge only with a paid API
key or Vertex; a consumer Google login no longer serves requests.

## Install
`npm install -g @google/gemini-cli` (or `brew install gemini-cli`, `npx @google/gemini-cli`).
Not installed here.

## Detect
```sh
command -v gemini >/dev/null 2>&1 && \
  { [ -n "$GEMINI_API_KEY" ] || { [ -n "$GOOGLE_CLOUD_PROJECT" ] && [ -n "$GOOGLE_CLOUD_LOCATION" ]; }; }
```

## One-shot, read-only
No cwd flag: `cd` first. Answer is `.response`.
```sh
cd <D> && perl -e 'alarm shift; exec @ARGV' 1200 \
  gemini -p "<P>" -m <M> --approval-mode plan -o json \
    < /dev/null > <OUT>.json 2> <OUT>.err
jq -e '.error == null' <OUT>.json >/dev/null && jq -r '.response' <OUT>.json > <OUT>
```
`--approval-mode plan` is the read-only mode. `--include-directories <dirs>` adds directories.

## One-shot, write-enabled
Only on a worktree. `auto_edit` auto-approves edits; `yolo` approves everything.
```sh
cd <WORKTREE> && perl -e 'alarm shift; exec @ARGV' 2700 \
  gemini -p "<P>" -m <M> --approval-mode auto_edit -o json < /dev/null > <OUT>.json 2> <OUT>.err
```

## Flags
| Need | Flag |
|---|---|
| One-shot | `-p "<P>"` (headless also triggers with no TTY; prompt is appended to stdin) |
| Model | `-m, --model <id>` (default `auto`); profile id -> `gemini-3.8-flash` |
| Effort | **none.** Define a `modelConfigs` alias with `thinkingConfig.thinkingLevel` in settings.json, select it with `-m`. Exact JSON UNVERIFIED |
| Approval | `--approval-mode default\|auto_edit\|yolo\|plan` (`-y/--yolo` deprecated) |
| Output | `-o, --output-format text\|json\|stream-json` |
| Working dir | none; `cd`. `--include-directories <dirs>` |
| Trust / sandbox | `--skip-trust`; `-s, --sandbox` |

## Prompting this model family
The kit has no Gemini-specific prompting evidence. Use the literal style the README gives
for non-Claude models: short imperatives, the exact target, the exact output format, and a
stop condition. Gemini CLI reads `GEMINI.md` (not `AGENTS.md` unless `context.fileName` is
set), so put anything the repo rules would say into the prompt.

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
cd "$TMPDIR" && perl -e 'alarm shift; exec @ARGV' 120 gemini -p "Reply with the single word OK" \
  -m gemini-3.8-flash --approval-mode plan -o json < /dev/null | jq -r '.response'
```
Expected (docs, not run): `OK`, exit 0. JSON shape: `{response, stats, error?}`.

## Gotchas
- **Auth:** needs a paid key or Vertex since 2026-06-18. A cached consumer login may still be
  found but will not serve requests; expect an auth error, not a model answer.
- **Exit codes:** `0` ok, `1` error, `42` input error, `53` turn limit exceeded.
- **Timeout:** no wall-clock flag (subagents default to 10 min via `timeout_mins`). Perl alarm
  kills with SIGALRM (exit 142, no JSON). Prefer
  `. core/bridges/_timeout.sh; with_timeout 1200 gemini -p ...` (exit 124). Either is "no result".
- **JSON:** answer in `.response`; check `.error` first. `stats` holds usage.
- **cwd:** no flag; the process cwd is the workspace.
- `-p` means prompt here; in `codex`, `-p` is `--profile`.
- Effort cannot be set per call from the CLI; route effort-sensitive work elsewhere or
  pre-define aliases in settings.json.
