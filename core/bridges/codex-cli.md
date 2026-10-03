---
id: codex-cli
harness: codex
binary: codex                    # ~/.local/bin/codex -> ~/.codex/packages/standalone/current/bin/codex
reaches: [gpt-6-astra, gpt-6-1-sol, gpt-6-luna]
auth: "ChatGPT login (codex login; --device-auth for headless) or CODEX_API_KEY"
verified: local                  # codex exec --help / exec review --help / review --help 0.160.0, smoke test run 2026-10-02
as_of: 2026-10-02
---

## Install
`curl -fsSL https://chatgpt.com/codex/install.sh | sh`, `npm install -g @openai/codex`, or
`brew install --cask codex`; update with `codex update`. Verified against `codex-cli 0.160.0`.

## Detect
```sh
command -v codex >/dev/null 2>&1 && { codex login status >/dev/null 2>&1 || [ -n "$CODEX_API_KEY" ]; }
```
Logged in prints `Logged in using ChatGPT`, exit 0 (local). Exit code when logged out: UNVERIFIED.

## One-shot, read-only
Prompt is **positional** after `exec`. Final message goes to stdout and to `-o <OUT>`;
progress goes to stderr.
```sh
perl -e 'alarm shift; exec @ARGV' 1200 \
  codex exec -C <D> -m <M> -c model_reasoning_effort="<E>" \
    --sandbox read-only --ephemeral -o <OUT> "<P>" \
    < /dev/null > /dev/null 2> <OUT>.err
```
Add `--skip-git-repo-check` when `<D>` is not a git repo. `read-only` is also the `exec` default.

## One-shot, write-enabled
Only on a worktree. `workspace-write` lets the agent edit files in `-C <D>` (and `--add-dir`
dirs) and run commands inside the sandbox.
```sh
perl -e 'alarm shift; exec @ARGV' 2700 \
  codex exec -C <WORKTREE> -m <M> -c model_reasoning_effort="<E>" \
    --sandbox workspace-write --ephemeral -o <OUT> "<P>" < /dev/null > /dev/null 2> <OUT>.err
```
Afterwards check `git -C <WORKTREE> status` and the diff yourself.

**Worktrees and `git commit`.** A linked worktree's `.git` is a file pointing at
`<main>/.git/worktrees/<name>`; commits write objects and refs under the main repo's `.git`,
which is outside a sandbox scoped to `<WORKTREE>`, so `git commit` may be blocked.
Default policy: **tell the callee not to commit; the orchestrator commits after it finishes**
(`git -C <WORKTREE> add -A && git -C <WORKTREE> commit`). If the callee must commit, add the
common git dir as a writable root (`--add-dir` is in 0.160.0 help: "Additional directories
that should be writable alongside the primary workspace"):
```sh
  ... --sandbox workspace-write --add-dir "$(git -C <WORKTREE> rev-parse --path-format=absolute --git-common-dir)" ...
```
UNVERIFIED: whether this is enough for `git commit` (Codex may keep `.git` read-only inside
writable roots), and the equivalent `-c sandbox_workspace_write.writable_roots=[...]` key.

## Review mode
`codex exec review` is the scriptable form: unlike `codex review` it accepts `-m`, `--json`,
`-o`, `--ephemeral`, `--skip-git-repo-check` (local help). It has **no `-C` and no `--sandbox`**.
```sh
cd <D> && perl -e 'alarm shift; exec @ARGV' 1200 \
  codex exec review --uncommitted -m <M> -c model_reasoning_effort="<E>" \
    -c sandbox_mode="read-only" --ephemeral -o <OUT> < /dev/null > /dev/null 2> <OUT>.err
```
Targets: `--uncommitted` | `--base <BRANCH>` | `--commit <SHA>` (`--title T` optional).
Plain `codex review [target] -c model="<M>" -c model_reasoning_effort="<E>"` also works but has
no `-m`, `--json` or `-o`; capture stdout. Sandbox default for either review form, and whether a
custom `[PROMPT]` combines with a target flag: UNVERIFIED. `sandbox_mode` is the config key
named in the research; passing it explicitly is the safe choice.

## Flags
| Need | Flag |
|---|---|
| Model | `-m <id>`: `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-luna` (local models cache) |
| Effort | `-c model_reasoning_effort="low\|medium\|high\|xhigh\|max\|ultra"`; `ultra` on Sol/Astra only |
| Sandbox | `-s, --sandbox read-only\|workspace-write\|danger-full-access` |
| Output | stdout = final message; `-o <FILE>`; `--json` = JSONL; `--output-schema <FILE>` |
| Working dir | `-C, --cd <DIR>`; `--add-dir <DIR>`; `--skip-git-repo-check` outside git |
| No persistence | `--ephemeral`; `--ignore-user-config`, `--ignore-rules` |
| Profile | `-p, --profile <name>` (**not** prompt) |

## Prompting this model family
GPT models do what the text says, or less. Keep prompts short, literal, imperative. State
the target, the exact output, and the stop condition. No personality, no method coaching.
Astra scope-creeps when implementing: say "Make the smallest possible changes." Sol keeps
following process rules when stuck: give an escape hatch. Put any procedure in the prompt
(skills may be dropped). Write the action you want, not a question ("Fix them", not "are
these worth fixing?"). Verify git state yourself; do not trust "I pushed".

Review:
> Review the uncommitted changes in /repo. Report correctness bugs only. For each: file:line,
> what breaks, how to trigger it. Do not edit files. If you find nothing, say so explicitly
> and list what you inspected.

Bounded implementation:
> In /repo-wt, make parseDate in src/util/date.ts accept ISO week dates (2026-W40-5). Make
> the smallest possible changes. Run `npm test`; it must pass. Do not commit or push.
> If you make no progress after 3 attempts, stop and report what blocks you.
> Report the files you changed. If you find nothing to change, say so explicitly and list
> what you inspected.

## Smoke test
```sh
cd "$TMPDIR" && perl -e 'alarm shift; exec @ARGV' 120 codex exec -m gpt-6.1-sol \
  -c model_reasoning_effort="low" --sandbox read-only --skip-git-repo-check --ephemeral \
  "Reply with the single word OK" < /dev/null 2>/dev/null
```
Success: stdout `OK`, exit 0. Run 2026-10-02: exit 0, 2,336 tokens; stderr header showed
`model: gpt-6.1-sol`, `approval: never`, `sandbox: read-only`, `reasoning effort: low`.
With `--json`: `{"type":"thread.started","thread_id"}`, `{"type":"turn.started"}`,
`{"type":"item.completed","item":{"id","type":"agent_message","text":"OK"}}`,
`{"type":"turn.completed","usage":{...}}`.

## Gotchas
- **`-p` is `--profile`, not prompt.** The prompt is the positional arg (or stdin / `-`).
- **Always `< /dev/null`.** `exec` prints `Reading additional input from stdin...` and appends
  piped stdin to the prompt; an open, never-closed pipe can block it.
- **Exit codes:** 0 success; 1 on error (bad `-m` gave exit 1 with a 400
  `invalid_request_error` on stderr). Unknown model ids print a metadata warning first.
- **Timeout:** no wall-clock flag (`stream_idle_timeout_ms` 300000, 4 retries). The perl alarm
  kills with SIGALRM (exit 142); `-o` may then be missing or empty. Prefer
  `. core/bridges/_timeout.sh; with_timeout 1200 codex exec ...` (exit 124). Either is "no result".
- **JSON:** with `--json`, the answer is `.item.text` of the last `item.completed` whose
  `.item.type == "agent_message"`; failures arrive as `turn.failed` / `error` events. Simpler:
  read `-o <OUT>`.
- **cwd:** use `-C <D>`; `exec review` has no `-C`, so `cd` first. Outside a git repo every
  form needs `--skip-git-repo-check`.
- **Computer use is not reachable from the CLI.** It runs only in the ChatGPT desktop app
  (Codex merged into it 2026-07-09). `codex features list` shows `computer_use`, but CLI
  exposure is UNVERIFIED; do not route computer-use work here.
- `--full-auto` is deprecated and absent from 0.160.0 help; use `--sandbox workspace-write`.
- 0.160.0 help also lists `--worktree` (managed git worktree) and `--approve-for-me`; not in
  the research, semantics UNVERIFIED.
- MCP servers marked `required = true` abort `exec` if they fail to start; add
  `--ignore-user-config` if a broken user MCP blocks runs.
