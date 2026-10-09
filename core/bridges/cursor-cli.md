---
id: cursor-cli
harness: cursor
binary: agent                    # AMBIGUOUS: Grok Build also installs `agent`. Call Cursor by absolute path ($CURSOR_AGENT)
reaches: [claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5, gpt-6-astra, gpt-6-1-sol, gpt-6-luna, gemini-3-8-flash, grok-4-7]
auth: "agent login (Cursor account/plan) or CURSOR_API_KEY / --api-key"
verified: docs                   # Cursor CLI is not installed on this machine
as_of: 2026-10-02
---
`reaches` lists profiles whose `access.harnesses` include `cursor`; none of them list
`cursor-cli` in `invoke_via` yet. Cursor uses its own model slugs (`agent models`). GPT-6 Astra
and 6.1 Sol access in Cursor is reportedly revoked (see those profiles).

## Install
`curl https://cursor.com/install -fsS | bash`; auto-updates, or `agent update`. Not installed here.

## Detect
Find an `agent` that is not Grok's, and export it for the templates:
```sh
CURSOR_AGENT=
for a in $(which -a agent 2>/dev/null); do
  case "$(realpath "$a" 2>/dev/null)" in *"/.grok/"*) continue ;; esac
  "$a" --version 2>/dev/null | grep -qi '^grok' && continue
  CURSOR_AGENT=$a; break
done
[ -n "$CURSOR_AGENT" ] && export CURSOR_AGENT
```
Login check: `[ -n "$CURSOR_API_KEY" ]`, else run the smoke test (no documented status command).

## One-shot, read-only
```sh
perl -e 'alarm shift; exec @ARGV' 1200 \
  "$CURSOR_AGENT" -p "<P>" --model <M> --mode ask --output-format json \
    --workspace <D> --trust < /dev/null > <OUT>.json 2> <OUT>.err
jq -e '.is_error == false' <OUT>.json >/dev/null && jq -r '.result' <OUT>.json > <OUT>
```
`--mode ask` is read-only Q&A (`--mode plan` / `--plan` also). Docs also say print mode
without `--force` only proposes changes, but another page says non-interactive has "full write
access"; pass `--mode ask` explicitly.

## One-shot, write-enabled
Only on a worktree. `-f/--force` (alias `--yolo`) applies edits and runs commands unprompted.
```sh
perl -e 'alarm shift; exec @ARGV' 2700 \
  "$CURSOR_AGENT" -p "<P>" --model <M> --force --output-format json \
    --workspace <WORKTREE> --trust < /dev/null > <OUT>.json 2> <OUT>.err
```

## Flags
| Need | Flag |
|---|---|
| One-shot | `-p, --print "<P>"` |
| Model | `--model <slug>`; list with `agent models` / `--list-models` |
| Effort | **none.** `<slug>[effort=high]` is documented for subagent `model:` only; CLI UNVERIFIED |
| Read-only | `--mode ask` (or `plan`) |
| Writes | `-f, --force` / `--yolo`; `--sandbox enabled\|disabled` |
| Output | `--output-format text\|json\|stream-json`; `--stream-partial-output` |
| Working dir | `--workspace <path>` |
| Headless trust | `--trust`; `--approve-mcps` |

## Prompting this model family
Cursor is a harness, not a model family: prompt in the dialect of the model you pick. For
`claude-*` slugs follow `claude-cli.md` (wide, context-rich, scope-control block). For GPT,
Gemini and Grok slugs use the literal style: short imperatives, exact output, stop condition.
Cursor loads `.cursor/rules`, root `AGENTS.md` and root `CLAUDE.md`, so repo rules apply.

Review (literal style, for a GPT/Grok slug):
> Review the uncommitted changes in this workspace. Report correctness bugs only. For each:
> file:line, what breaks, how to trigger it. Do not edit files. If you find nothing, say so
> explicitly and list what you inspected.

Bounded implementation (literal style):
> Make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make the smallest
> possible changes. Run `npm test`; it must pass. Do not commit. If you make no progress after
> 3 attempts, stop and report what blocks you. List the files you changed. If you find
> nothing to change, say so explicitly and list what you inspected.

## Smoke test
```sh
cd "$TMPDIR" && perl -e 'alarm shift; exec @ARGV' 120 "$CURSOR_AGENT" -p "Reply with the single word OK" \
  --mode ask --output-format json --trust < /dev/null | jq -r '.result'
```
Expected (docs, not run): `OK`, exit 0. JSON shape per docs:
`{type:"result", subtype, is_error, duration_ms, duration_api_ms, result, session_id, request_id?}`.

## Gotchas
- **PATH collision.** Grok Build installs `~/.grok/bin/agent -> grok`. On this machine both
  `agent` entries on PATH (`~/.grok/bin/agent`, `~/.local/bin/agent -> ~/.grok/bin/agent`) are
  Grok, and `agent --version` prints `grok 1.0.0 ...`. Never call bare `agent`; use the absolute
  path found by Detect. Cursor's installer location, and whether it would overwrite the
  existing `~/.local/bin/agent` symlink: UNVERIFIED. Whether a `cursor-agent` alias still
  exists: UNVERIFIED.
- `-p` means `--print` here (as in Claude); in `codex`, `-p` is `--profile`.
- **Exit codes:** non-zero means failure; specific codes are not documented.
- **Timeout:** none documented. Perl alarm kills with SIGALRM (exit 142, no JSON). Prefer
  `. core/bridges/_timeout.sh; with_timeout 1200 "$CURSOR_AGENT" -p ...` (exit 124).
- **JSON:** answer in `.result`; check `.is_error` (Claude's CLI reports errors with
  `subtype:"success"`; Cursor's behaviour here is UNVERIFIED, so do not trust `.subtype`).
- **cwd:** `--workspace <D>`; without it the process cwd is used. `--trust` avoids the
  headless workspace-trust prompt.
- `agent worker start --computer-use` lets cloud agents drive this desktop; it is not a
  one-shot path and not part of this bridge.
