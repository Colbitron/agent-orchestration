---
id: xai-api
harness: none                    # raw HTTP, one-shot chat completion, no tools
binary: curl                     # plus jq
reaches: [grok-4-7]
auth: "XAI_API_KEY env var from console.x.ai (Bearer header). Never paste the key into a prompt or file"
verified: docs                   # endpoint and body from research/model-gaps.md and core/models/grok-4-7.md; not run (no key set)
as_of: 2026-10-02
---
One-shot Grok 4.7 completions without the Grok Build harness. No tools: inline everything.
Grok 4.7 is token-hungry (about 2x Opus 5.5 per task on AA), so this is not the bulk bridge;
use it for a third-family opinion on inlined code when `grok-cli` is not logged in.

## Install
Nothing to install: `curl` and `jq`.

## Detect
```sh
command -v curl >/dev/null && command -v jq >/dev/null && [ -n "$XAI_API_KEY" ]
```

## One-shot, read-only
```sh
jq -n --arg m "grok-4.7" --arg e "<E>" --rawfile p <PFILE> \
  '{model:$m, reasoning_effort:$e, messages:[{role:"user", content:$p}]}' > <OUT>.req.json
perl -e 'alarm shift; exec @ARGV' 900 \
  curl -sS --fail-with-body https://api.x.ai/v1/chat/completions \
    -H "Authorization: Bearer $XAI_API_KEY" -H "Content-Type: application/json" \
    --data @<OUT>.req.json > <OUT>.json 2> <OUT>.err
jq -r '.choices[0].message.content' <OUT>.json > <OUT>
```
Drop `reasoning_effort` if the API rejects it: the field name follows the OpenAI-compatible
convention and is UNVERIFIED for xAI.

## One-shot, write-enabled
Not applicable: no tools. For Grok with tools and writes, use `grok-cli` on a worktree.

## Flags
| Need | Body field / option |
|---|---|
| Model | `"model": "grok-4.7"` (profile `api_ids`; no aliases) |
| Effort | `"reasoning_effort": "<E>"` (UNVERIFIED for xAI); cap at `high` |
| Answer | `.choices[0].message.content`; usage in `.usage` |
| Timeout | perl alarm, or `curl --max-time <s>` (curl exit 28) |

## Prompting this model family
Literal style, as for GPT: name the target and the question, require a strict output format,
make "nothing found" valid, ask it to mark what it could not confirm. Bound the scope: Grok
4.7 is verbose and regresses on long-document reasoning, so do not send large specs.

Review:
> Below is a diff. Report correctness bugs only, as JSON lines `{"file","line","bug","confirmed"}`
> where confirmed is true only if the diff itself shows the bug. If you find nothing, say so
> explicitly and list what you inspected.

Bounded implementation:
> Below is the function parseDate. Rewrite it to also accept ISO week dates (2026-W40-5).
> Return only the full new function in one code block. Change nothing else. If you find
> nothing to change, say so explicitly and list what you inspected.

## Smoke test
```sh
jq -n '{model:"grok-4.7", messages:[{role:"user",content:"Reply with the single word OK"}]}' |
  perl -e 'alarm shift; exec @ARGV' 90 curl -sS --fail-with-body https://api.x.ai/v1/chat/completions \
    -H "Authorization: Bearer $XAI_API_KEY" -H "Content-Type: application/json" --data @- |
  jq -r '.choices[0].message.content'
```
Expected (not run, no key): `OK`, exit 0.

## Gotchas
- **Exit codes:** with `--fail-with-body`, HTTP errors exit 22 and the error JSON stays in
  `<OUT>.json`; without it curl exits 0 on errors.
- **Timeout:** perl alarm kills curl with SIGALRM (exit 142); `curl --max-time` exits 28;
  `. core/bridges/_timeout.sh; with_timeout 900 curl ...` exits 124. All mean "no result".
- **JSON:** answer is `.choices[0].message.content` (Grok Build's CLI uses `.text`; the API does not).
- **cwd:** irrelevant; the model cannot read files.
- `curl -p` is `--proxytunnel`, `codex -p` is `--profile`, `grok -p` is `--single`.
- Pricing doubles at 200K+ input tokens; keep inlined context small.
- A `grok login` session token in `~/.grok/auth.json` can also authenticate API calls (Grok
  README "Using auth.json for API Access"); prefer `XAI_API_KEY` for scripts.
