---
id: ollama
harness: none                    # local HTTP server, one-shot chat completion, no tools
binary: curl                     # plus jq; server is `ollama` (installed here: /usr/local/bin/ollama 0.35.1)
reaches: [qwen3-8-27b, gpt-oss-20b]   # local open-weights models with a core/models profile (tags "qwen3.8:27b", "gpt-oss:20b")
auth: "none (local server on 127.0.0.1:11434; override with OLLAMA_HOST)"
verified: local                  # endpoints probed 2026-10-02 (error shape only); no model pulled, so no completion run
as_of: 2026-10-02
---
Free, private, local fan-out for small mechanical tasks. No tools: inline everything. Quality
depends entirely on the pulled model and the machine's memory; verify every answer. Profiles
with a `local` block (`core/models/qwen3-8-27b.md`, `core/models/gpt-oss-20b.md`) say which
quantized build fits which machine; the generator checks that against `config.hardware`.
Agent harnesses driving a local model need `OLLAMA_CONTEXT_LENGTH=65536` or more (Ollama
defaults to 4K below 24 GiB), and the first request after a model loads can take minutes.

## Install
`ollama` app or CLI, then `ollama pull <model>`. Here: `ollama version is 0.35.1`, server
running, **no models pulled** (`/api/tags` returned `{"models":[]}`).

## Detect
```sh
command -v curl >/dev/null && command -v jq >/dev/null && \
  curl -s -m 3 http://localhost:11434/api/tags | jq -e '.models | length > 0' >/dev/null
```

## One-shot, read-only
OpenAI-compatible endpoint:
```sh
jq -n --arg m "<M>" --rawfile p <PFILE> \
  '{model:$m, messages:[{role:"user", content:$p}]}' > <OUT>.req.json
perl -e 'alarm shift; exec @ARGV' 900 \
  curl -sS --fail-with-body http://localhost:11434/v1/chat/completions \
    -H "Content-Type: application/json" --data @<OUT>.req.json > <OUT>.json 2> <OUT>.err
jq -r '.choices[0].message.content' <OUT>.json > <OUT>
```
Native alternative: `POST /api/chat` with `"stream": false`; answer in `.message.content`
(UNVERIFIED here: no model to run). Or the CLI: `ollama run <M> "<P>"` (`--think` for
thinking models, `--hidethinking` to drop it from stdout).

## One-shot, write-enabled
Not applicable: no tools. For local models with tools, use `opencode-cli` (`-m ollama/<id>`)
or `codex exec --oss --local-provider ollama`.

## Flags
| Need | Body field / option |
|---|---|
| Model | `"model": "<name:tag>"` as shown by `ollama list` |
| Effort | none in the OpenAI body; CLI `--think high\|medium\|low` for supported models |
| Answer | `/v1`: `.choices[0].message.content`; `/api/chat`: `.message.content` |
| Keep loaded | CLI `--keepalive 5m` |
| Timeout | perl alarm, or `curl --max-time <s>` |

## Prompting this model family
Small local models: literal style, one task, a few lines of instructions, a strict output
format, tiny context. Give an example of the expected output. Never use them for judgement
calls; use them where a script can check the answer.

Review:
> Below is a diff. List lines that call a function that is not defined in the diff, as
> `file:line name`. Nothing else. If you find nothing, say so explicitly and list what you inspected.

Bounded implementation:
> Below is a JSON object. Rename every key from snake_case to camelCase. Return only the new
> JSON. If you find nothing to change, say so explicitly and list what you inspected.

## Smoke test
```sh
jq -n --arg m "<M>" '{model:$m, messages:[{role:"user",content:"Reply with the single word OK"}]}' |
  perl -e 'alarm shift; exec @ARGV' 180 curl -sS --fail-with-body http://localhost:11434/v1/chat/completions \
    -H "Content-Type: application/json" --data @- | jq -r '.choices[0].message.content'
```
Expected: `OK`, exit 0. Run here with model `nope`: exit 22, body
`{"error":{"message":"model 'nope' not found","type":"not_found_error",...}}`.

## Gotchas
- **Exit codes:** with `--fail-with-body`, a missing model is HTTP 404 -> curl exit 22 (seen
  locally); curl exit 7 means the server is not running.
- **Timeout:** the first call loads the model into memory and can take minutes. Perl alarm kills
  curl with SIGALRM (exit 142); `. core/bridges/_timeout.sh; with_timeout 900 curl ...` exits 124.
  Either is "no result".
- **JSON:** `/v1/...` -> `.choices[0].message.content`; `/api/chat` -> `.message.content`;
  `/api/*` errors are `{"error":"..."}` (a string), `/v1` errors are `{"error":{"message":...}}`.
- **cwd:** irrelevant; the model cannot read files.
- `curl -p` is `--proxytunnel`, `codex -p` is `--profile`: never assume `-p` means prompt.
- Running several large models in parallel can exhaust memory; fan out with a small concurrency.
