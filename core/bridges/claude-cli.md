---
id: claude-cli
harness: claude-code
binary: claude                   # ~/.local/bin/claude -> ~/.local/share/claude/versions/<ver>
reaches: [claude-fable-5-1, claude-opus-5-5, claude-sonnet-5-5, claude-haiku-4-5]
auth: "claude auth login (Pro/Max subscription or Console), or ANTHROPIC_API_KEY (the only option with --bare)"
verified: local                  # claude --help 2.1.288, smoke test run 2026-10-02
as_of: 2026-10-02
---

## Install
Native installer, then `claude install [stable|latest|<ver>]`; update with `claude update`.
Verified against `2.1.288 (Claude Code)`.

## Detect
```sh
command -v claude >/dev/null 2>&1 && \
  { claude auth status 2>/dev/null | jq -e '.loggedIn == true' >/dev/null || [ -n "$ANTHROPIC_API_KEY" ]; }
```
`claude auth status` prints JSON: `loggedIn`, `authMethod` (`claude.ai` here), `apiProvider`, `subscriptionType`.

## One-shot, read-only
No `--cwd` flag: `cd` first. Answer is `.result` of a single JSON object on stdout.
```sh
cd <D> && perl -e 'alarm shift; exec @ARGV' 1200 \
  claude -p "<P>" --model <M> --effort <E> \
    --permission-mode dontAsk --tools "Read,Grep,Glob" \
    --output-format json --no-session-persistence \
    < /dev/null > <OUT>.json 2> <OUT>.err
jq -e '.is_error == false' <OUT>.json >/dev/null && jq -r '.result' <OUT>.json > <OUT>
```
`dontAsk` auto-denies anything that would prompt; reads in the working dirs and the
read-only Bash set still run. `--tools "Read,Grep,Glob"` makes it a hard guarantee (drop
it if the callee needs `git diff` etc.; `dontAsk` alone still blocks writes).

## One-shot, write-enabled
Only on a worktree (`git worktree add ...`, or `claude -w <name>` creates one).
```sh
cd <WORKTREE> && perl -e 'alarm shift; exec @ARGV' 2700 \
  claude -p "<P>" --model <M> --effort <E> \
    --permission-mode acceptEdits --allowedTools "Bash(git *)" "Bash(npm test *)" \
    --max-budget-usd 5.00 --output-format json --no-session-persistence \
    < /dev/null > <OUT>.json 2> <OUT>.err
```
`acceptEdits` auto-approves file edits; Bash runs only for rules in `--allowedTools`
(permission-rule syntax). `auto` / `bypassPermissions` widen this; avoid outside sandboxes.

## Flags
| Need | Flag (checked in `--help` unless noted) |
|---|---|
| Model | `--model fable\|opus\|sonnet\|haiku\|<full id>`; `--fallback-model a,b` |
| Effort | `--effort low\|medium\|high\|xhigh\|max` (model-dependent) |
| Output | `--output-format text\|json\|stream-json` (`stream-json` needs `--verbose`) |
| Structured | `--json-schema '<schema>'` -> `.structured_output` |
| Read-only | `--permission-mode dontAsk` (+ `--tools "Read,Grep,Glob"`) |
| Unattended | `--permission-prompts none` (auto-deny every prompt) |
| Turn cap | `--max-turns N` (docs only; **not in `--help`**) |
| Spend cap | `--max-budget-usd <amount>` (print only) |
| Working dir | none; `cd <D>`. `--add-dir <dirs...>` for extra access |
| Reproducible | `--bare` (no CLAUDE.md/hooks/skills/MCP; **API key only**) |

## Prompting this model family
Claude takes wide, context-rich prompts: goal, done conditions, constraints and
negatives, and an "out" (when to stop and ask). It tends to do more than asked, so add the
scope-control block for narrow tasks. Do not micro-specify method or say "think hard";
effort is the `--effort` flag. Ask for the report headings so the last message stands alone.

Review:
> Review the uncommitted changes in /repo (run `git diff` to see them) for correctness bugs
> and regressions in the auth flow. Prioritise issues that would break login or leak
> sessions; style is out of scope. For each finding give file:line, the failure scenario,
> and your confidence. Mark anything you could not confirm by reading the code. Do not edit
> files. If you find nothing, say so explicitly and list what you inspected.

Bounded implementation:
> In /repo-wt (a git worktree on branch fix/date-parse), make `parseDate` in
> src/util/date.ts accept ISO week dates. Done means the new cases in date.test.ts pass and
> `npm test` is green. If while working you find pre-existing bugs or behaviours the task
> doesn't mention, don't fix them; report them as follow-ups. Commit on the branch; do not
> push. End with headings Changed / Found / Not verified. If you find nothing to change,
> say so explicitly and list what you inspected.

## Smoke test
```sh
cd "$TMPDIR" && perl -e 'alarm shift; exec @ARGV' 120 claude -p "Reply with the single word OK" \
  --model sonnet --effort low --permission-mode dontAsk --output-format json \
  --no-session-persistence < /dev/null | jq -r '.result'
```
Success: prints `OK`, exit 0. Run 2026-10-02: exit 0, ~1.4 s, `total_cost_usd` 0.0498.
Result shape (values elided):
```
{ type:"result", subtype:"success", is_error:false, result:"OK", session_id, uuid,
  num_turns:1, stop_reason:"end_turn", terminal_reason:"completed", api_error_status:null,
  duration_ms, duration_api_ms, ttft_ms, total_cost_usd,
  usage:{input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens,...},
  modelUsage:{"claude-sonnet-5-5":{costUSD, contextWindow, maxOutputTokens,...}},
  permission_denials:[], subagent_stats:{...}, fast_mode_state, ... }
```

## Gotchas
- **Exit codes:** 0 on success; 1 on error (bad model gave exit 1). SIGTERM exits **143 with
  no result**; SIGINT ends the turn cleanly.
- **Errors still say `subtype:"success"`.** A bad `--model` returned `subtype:"success"`,
  `is_error:true`, `terminal_reason:"api_error"`, `api_error_status:404` and the error text in
  `.result`. Check `.is_error`, never `.subtype`. A stderr line like
  `[claude-code:unrecognized_model]` may precede the JSON when `2>&1` is used; keep stderr separate.
- **Timeout:** the bare perl alarm sends SIGALRM (shell sees exit 142) and leaves no JSON.
  Prefer `. core/bridges/_timeout.sh; with_timeout 1200 claude -p ...`: it sends SIGINT to the
  process group first, then KILL after 10 s, and exits 124. Treat 124/142/143 as "no result".
- `-p` waits up to 10 min idle for background subagents (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`).
- **cwd:** there is no `--cwd`; the process cwd is the project. `-p` skips the workspace
  trust dialog, so only run in directories you trust.
- `--bare` ignores subscription OAuth; without `ANTHROPIC_API_KEY` it fails to auth.
- `--max-turns` is documented but absent from `--help`; it exits with an error at the limit.
- `plan` permission mode in `-p`: exit-plan approval is denied; result shape UNVERIFIED.
- `--permission-mode default` is in the research list but not in 2.1.288 `--help` choices
  (`acceptEdits, auto, bypassPermissions, manual, dontAsk, plan`).
- Stdin is prepended to the prompt (10 MB cap); redirect `< /dev/null` when not piping.
- `-p` means `--print` here. Do not carry it over to `codex`, where `-p` is `--profile`.
