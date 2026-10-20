---
id: openrouter-api
harness: none                    # raw HTTP, one-shot chat completion, no tools
binary: curl                     # plus jq
reaches: [qwen3-8-27b, gpt-oss-20b]   # hosted ids qwen/qwen3.8-27b and openai/gpt-oss-20b; MiMo, GLM and DeepSeek profiles list this bridge too
auth: "OPENROUTER_API_KEY env var (Bearer header). Never paste the key into a prompt or file"
verified: unverified             # OpenAI-compatible endpoint shape; not in research/harnesses.md; not run (no key set)
as_of: 2026-10-02
---
For bulk, cheap fan-out to open-weights models (MiMo-V2.6-Pro, GLM-5.3-Flash, DeepSeek V4.1
Flash...) with programmatic verification. No tools: inline everything. For open-weights
models *with* tools, use `opencode-cli` or `pi-cli` instead.

## Install
Nothing to install: `curl` and `jq`.

## Detect
```sh
command -v curl >/dev/null && command -v jq >/dev/null && [ -n "$OPENROUTER_API_KEY" ]
```

## One-shot, read-only
```sh
jq -n --arg m "<M>" --rawfile p <PFILE> \
  '{model:$m, messages:[{role:"user", content:$p}]}' > <OUT>.req.json
perl -e 'alarm shift; exec @ARGV' 600 \
  curl -sS --fail-with-body https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" -H "Content-Type: application/json" \
    --data @<OUT>.req.json > <OUT>.json 2> <OUT>.err
jq -r '.choices[0].message.content' <OUT>.json > <OUT>
```

## One-shot, write-enabled
Not applicable: no tools. Ask for a diff or replacement text; apply and verify it yourself on
a worktree.

## Flags
| Need | Body field / option |
|---|---|
| Model | `"model": "<vendor>/<id>"`, e.g. `xiaomi/mimo-v2.6-pro` (from `research/model-gaps.md`; other ids UNVERIFIED) |
| Effort | provider-specific; `reasoning_effort` acceptance per model UNVERIFIED |
| Output cap | `"max_tokens": N` |
| Answer | `.choices[0].message.content`; usage in `.usage` |
| Timeout | perl alarm, or `curl --max-time <s>` (curl exit 28) |

## Prompting this model family
Open-weights models: literal style, one narrow task per call, a strict machine-checkable output
format, short context. Check every answer programmatically; on a miss, escalate to a stronger
model rather than retrying the same one.

Review:
> Below is a diff. Report correctness bugs only, as JSON lines `{"file","line","bug"}`. Do not
> report style. If you find nothing, say so explicitly and list what you inspected.

Bounded implementation:
> Below is the function parseDate. Rewrite it to also accept ISO week dates (2026-W40-5).
> Return only the full new function in one code block. Change nothing else. If you find
> nothing to change, say so explicitly and list what you inspected.

## Smoke test
```sh
jq -n '{model:"xiaomi/mimo-v2.6-pro", messages:[{role:"user",content:"Reply with the single word OK"}]}' |
  perl -e 'alarm shift; exec @ARGV' 90 curl -sS --fail-with-body https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" -H "Content-Type: application/json" --data @- |
  jq -r '.choices[0].message.content'
```
Expected (not run, no key): `OK`, exit 0. MiMo is slow (~45 tok/s); allow the full 90 s.

## Gotchas
- **Exit codes:** with `--fail-with-body`, HTTP errors exit 22 and the error JSON stays in
  `<OUT>.json`; without it curl exits 0 on errors.
- **Timeout:** perl alarm kills curl with SIGALRM (exit 142); `curl --max-time` exits 28;
  `. core/bridges/_timeout.sh; with_timeout 600 curl ...` exits 124. All mean "no result".
- **JSON:** answer is `.choices[0].message.content`. Empty content with
  `finish_reason:"length"` means the cap was hit; some reasoning models spend the cap thinking.
- **cwd:** irrelevant; the model cannot read files.
- `curl -p` is `--proxytunnel`, `codex -p` is `--profile`: never assume `-p` means prompt.
- Cheap per token is not cheap per task: count attempts to a verified answer, not list price.
