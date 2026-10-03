---
id: openai-api
harness: none                    # raw HTTP, one-shot chat completion, no tools
binary: curl                     # plus jq to build the body and read the answer
reaches: [gpt-6-luna]            # Astra / 6.1 Sol have api: true but no confirmed API id (api_ids: null)
auth: "OPENAI_API_KEY env var (Bearer header). Never paste the key into a prompt or file"
verified: unverified             # endpoint/body are the standard OpenAI chat-completions shape; not in research/harnesses.md; not run (no key set)
as_of: 2026-10-02
---
For bulk, cheap fan-out with programmatic verification (Luna: about $0.10 / $0.50 per MTok).
The callee sees only the text you send: no files, no shell, no repo. Inline everything.

## Install
Nothing to install: `curl` and `jq` (`/opt/homebrew/bin/jq` here).

## Detect
```sh
command -v curl >/dev/null && command -v jq >/dev/null && [ -n "$OPENAI_API_KEY" ]
```
Unset on this machine on 2026-10-02.

## One-shot, read-only
```sh
jq -n --arg m "<M>" --rawfile p <PFILE> \
  '{model:$m, messages:[{role:"user", content:$p}]}' > <OUT>.req.json
perl -e 'alarm shift; exec @ARGV' 600 \
  curl -sS --fail-with-body https://api.openai.com/v1/chat/completions \
    -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" \
    --data @<OUT>.req.json > <OUT>.json 2> <OUT>.err
jq -r '.choices[0].message.content' <OUT>.json > <OUT>
```
`<PFILE>` holds the prompt plus any inlined code or diff. `--rawfile` avoids shell quoting.

## One-shot, write-enabled
Not applicable: no tools. Ask for a unified diff or replacement text, apply it yourself on a
worktree, and run the checks yourself.

## Flags
| Need | Body field / option |
|---|---|
| Model | `"model": "gpt-6-luna"` |
| Effort | `"reasoning_effort": "<E>"` (OpenAI-compatible convention; values for Luna UNVERIFIED) |
| Output cap | `"max_completion_tokens": N` (UNVERIFIED for Luna) |
| Answer | `.choices[0].message.content`; usage in `.usage` |
| Timeout | perl alarm, or `curl --max-time <s>` (curl exit 28) |

## Prompting this model family
GPT literal style: short imperatives, exact output format, nothing implied. Luna is the cheap
tier: one narrow task per call, machine-checkable output, escalate misses to 6.1 Sol via
`codex-cli` instead of retrying Luna.

Review:
> Below is a diff. Report correctness bugs only, as JSON lines `{"file","line","bug"}`. Do not
> report style. If you find nothing, say so explicitly and list what you inspected.

Bounded implementation:
> Below is the function parseDate. Rewrite it to also accept ISO week dates (2026-W40-5).
> Return only the full new function in one code block. Change nothing else. If you find
> nothing to change, say so explicitly and list what you inspected.

## Smoke test
```sh
jq -n '{model:"gpt-6-luna", messages:[{role:"user",content:"Reply with the single word OK"}]}' |
  perl -e 'alarm shift; exec @ARGV' 60 curl -sS --fail-with-body https://api.openai.com/v1/chat/completions \
    -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" --data @- |
  jq -r '.choices[0].message.content'
```
Expected (not run, no key): `OK`, exit 0.

## Gotchas
- **Exit codes:** without `--fail-with-body`, curl exits 0 on HTTP 4xx/5xx. With it, exit 22
  and the error JSON (`.error.message`) is still written to `<OUT>.json`.
- **Timeout:** perl alarm kills curl with SIGALRM (exit 142); `curl --max-time` exits 28;
  `. core/bridges/_timeout.sh; with_timeout 600 curl ...` exits 124. All mean "no result".
- **JSON:** answer is `.choices[0].message.content` (not `.result`/`.response`/`.text`).
  `null` content plus `finish_reason:"length"` means the output cap was hit.
- **cwd:** irrelevant; the model cannot read files. Inline the code or diff.
- `curl -p` is `--proxytunnel`, `codex -p` is `--profile`: never assume `-p` means prompt.
- Model id `gpt-6-luna` is from the profile's `api_ids`; Astra and 6.1 Sol API ids are not
  stated anywhere in the research, so do not guess them here.
