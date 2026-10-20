---
id: gpt-oss-20b
name: gpt-oss-20b
vendor: openai
family: open-weights             # not gpt: gated on access.open_weights; runs with no OpenAI account
status: current                  # no newer checkpoint exists (research/open-weights-small.md § Model 2 §1)
released: 2025-08                # 2025-08-05
as_of: 2026-10-19
confidence: medium               # independent AA numbers, OpenAI's model card and many practitioner reports; no hands-on use in this kit

api_ids:
  - openai/gpt-oss-20b           # OpenRouter model id, and also the Hugging Face repo id (same string)
  - "gpt-oss:20b"                # Ollama tag (14 GB, MXFP4); also the Codex CLI --oss default
  - gpt-oss-20b                  # OpenAI API model id: Responses and Batch only; Chat Completions "Not supported" (OAIDEV saved copy)
access:
  subscriptions: []
  api: true
  harnesses:
    - codex                      # `codex --oss -m gpt-oss:20b` (Ollama or LM Studio): a separate launch mode, not a model switch inside a ChatGPT-login session; Ollama says Codex needs 64K+ context
    - opencode                   # `ollama launch opencode --model gpt-oss`; needs 64K+ context
    - pi                         # `ollama launch pi --model gpt-oss:20b`; smallest prompt, best fit for 16 GB
    - openclaw
    - hermes
    # Not listed: claude-code, because the generator would print "this session" or "subagent only" for a
    # Claude-subscription user; Claude Code reaches it only in a separate `claude` process pointed at
    # Ollama's Anthropic-compatible API. LM Studio (`lms get openai/gpt-oss-20b`) is a runtime, not a kit harness id.
  invoke_via: [ollama, opencode-cli, pi-cli, openrouter-api, openclaw-cli, hermes-cli]   # ollama and openrouter-api have no tools. Not listed: codex-cli (the bridge documents no --oss flags; only ollama.md mentions `codex exec --oss --local-provider ollama`, unverified) and openai-api (that bridge uses Chat Completions, which OpenAI does not serve for this model); openclaw, hermes / openclaw-cli, hermes-cli added 2026-10-19: Ollama provider in OpenClaw, custom OpenAI-compatible base URL in Hermes; model strings unverified

pricing_per_mtok:                # no first-party list price exists; local runs cost nothing per token
  input: 0.058                   # Artificial Analysis price for gpt-oss-20b (High), 2026-10-19; OpenRouter providers range 0.018 to 0.075
  output: 0.215                  # same AA source; OpenRouter providers range 0.09 to 0.30
  cache_read: null
  cache_write: null
context_window: 131072
notes_on_cost: >
  The cheapest model in the kit by far when hosted: about $0.01 per Artificial
  Analysis Index task, at 258 tok/s, with fairly concise output (70M output
  tokens on the Index vs an 82M median). Run locally it costs nothing per token;
  the cost is the hardware and wall-clock, which on a 16 GB Mac is large (part of
  the model runs on the CPU and long prompts take minutes to read). Cost per
  completed task rises fast outside narrow checkable work: a flailing run at
  `high` effort can think for minutes or loop with tools, and claimed edits must
  be re-checked.

effort:
  levels: [low, medium, high]
  default: medium                # OpenAI's default
  avoid: [high]
  notes: >
    Set with `Reasoning: low|medium|high` in the system message (Ollama `think`,
    llama.cpp `reasoning_effort`). Low is much weaker on reasoning benchmarks (AA
    AIME25 62.3 low vs 89.3 high, GPQA 61.1 vs 68.8) but fine for yes/no
    classification and extraction; medium for tool loops. Avoid high on 16 GB
    machines and in tool loops: it thinks for minutes, overflows small contexts,
    and with about 8 tools bound "randomly results in reasoning loops" (open Ollama
    issue #12606).

scores:
  intelligence: 1
  taste: 1
  floor: 2
  thoroughness: 2
  cost_efficiency: 7
  speed: 8
  computer_use: 1
  orchestration: 1

tasks:
  quick-fix:      {fit: poor,    note: "Listed 'things as fixed without editing the code' and duplicated statements in a lint-fixing test (HN-quacker); Aider Polyglot 34.2 (self-reported)."}
  feature:        {fit: poor,    note: "AA Terminal-Bench 2.1 13.9% vs 79.8% for Qwen3.8 27B; SWE-bench Verified 60.7 at high is self-reported. Research: never route code edits or PR work."}
  long-run:       {fit: poor,    note: "AA Terminal-Bench 4.0 0%; loops at high effort with many tools (Ollama #12606)."}
  frontend:       {fit: poor,    note: "Text only, no image input; low effort produced invalid SVG (SW); code edits not routable."}
  review:         {fit: poor,    note: "Only reported use is a first-pass security review against a fixed checklist (HN-mhitza2); hallucination and weak long-context reading rule it out as a reviewer."}
  investigate:    {fit: poor,    note: "'As soon as a solution isn't clear it will hallucinate' (HN-strangescript); AA-Omniscience hallucination rate 0.94."}
  analyze:        {fit: poor,    note: "AA-LCR 34.7% and AA index 9 rule out audits and architecture critique; ripgrep location loops belong under bulk."}
  bulk:           {fit: good,    note: "Schema-enforced classification, JSON extraction, short summaries of supplied text, ripgrep loops returning paths and quotes. Not codemods or mechanical edits. Verify every output."}
  research:       {fit: ok,      note: "Only grounded in browsing or supplied documents under about 16K tokens; without retrieval it hallucinates (SimpleQA 0.914 self-reported). Never give it write tools while it reads the web."}
  computer-use:   {fit: poor,    note: "Text only; no image input, so it cannot read screenshots."}
  copy:           {fit: unknown, note: "No evidence."}
  3d-games:       {fit: poor,    note: "No 3D evidence; text only, and code edits are not routable (Terminal-Bench 4.0 0%)."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: poor,    note: "Must-land loop; tool-call parse errors in Ollama (#17638) and false 'fixed' claims."}
  orchestrate:    {fit: poor,    note: "Research: 'a worker, never the orchestrator'."}

role_hints:
  as_primary: "Not a primary model, even for a local-only user."
  as_subagent: "Offline or private worker for short, checkable tasks: schema-enforced classification, JSON extraction, short summaries of supplied text, and ripgrep loops whose paths and quotes the orchestrator verifies."
  never_for: ["primary or interactive model", "code edits, refactors or PR work", "factual answers without sources", "reading past about 16K tokens", "untrusted web content with write tools enabled", "leading other agents", "high effort on a 16 GB machine"]

local:                            # read by the generator against config.hardware; see core/models/_schema.md
  runs_locally: true
  licence: apache-2.0
  runtimes: [ollama, llama-cpp, lm-studio, mlx, vllm]
  cpu_offload: true               # sparse MoE (3.6B active): llama.cpp runs it on a 16 GB Mac with 12 of 24 MoE layers on the CPU, so the whole of a unified-memory machine bounds it, not the GPU's share
  memory_gb_by_quant:             # total VRAM or unified memory for weights plus a working context, third-party figures
    mxfp4: 15                     # native format, the only build worth running; llama.cpp guide: 14.9 GB at 8K context, 15.5 at 32K, 17.9 at 128K
  min_memory_gb: 15
  recommended_memory_gb: 16       # usable memory for full GPU residency: a 16 GB card ran 125K context fully on GPU (LCPP-bartlettroscoe); below it, expect CPU offload and 8K to 16K context
  measured_speed:                 # third-party measurements only; machine, runtime, quant, tok/s, source key
    - {machine: "MacBook Pro M1 Pro, 32 GB", runtime: "llama.cpp", tok_s: 45.7, source: "LCPP"}         # MXFP4, all on GPU, empty context; prompt processing 505 tok/s at 2K
    - {machine: "MacBook Pro M1 Pro, 32 GB", runtime: "llama.cpp", tok_s: 33.9, source: "LCPP"}         # at 16K context; prompt processing 367 tok/s (44.7 s to read 16K)
    - {machine: "MacBook Pro M2, 64 GB", runtime: "llama.cpp", tok_s: 82, source: "SW-LCPP"}            # "about 82"
    - {machine: "MacBook Pro M2, 64 GB", runtime: "LM Studio", tok_s: 39, source: "SW"}                 # low effort
    - {machine: "MacBook Pro M2, 64 GB", runtime: "LM Studio", tok_s: 55, source: "SW"}                 # medium effort
    - {machine: "M4 Max, 36 GB", runtime: "llama.cpp", tok_s: 92.4, source: "LCPP"}                     # empty context
    - {machine: "M4 Max, 36 GB", runtime: "llama.cpp", tok_s: 64.8, source: "LCPP"}                     # at 32K context
    - {machine: "RTX 5090, Windows 11", runtime: "llama.cpp (CUDA)", tok_s: 327, source: "HN-magicalhippo"}   # MXFP4 GGUF, llama-bench tg128 (326.82 in the saved copy)
    - {machine: "RTX 5060 Ti, 16 GB VRAM", runtime: "llama.cpp server", tok_s: 96, source: "LCPP-bartlettroscoe"}   # 125K context, flash attention, agentic Codex refactor; 96.22 average, 15.75 of 16.3 GB VRAM used
---

## Summary

gpt-oss-20b is OpenAI's smaller open-weights reasoning model (Apache 2.0, August
2025, 20.9B total and 3.6B active parameters, native MXFP4, text only, 131K
context). It is fast and almost free hosted (about $0.01 per AA task at 258
tok/s), trained for tool use and structured output, and small enough to run on
one machine, but it is far behind 2026 models: AA Intelligence Index 9, 0% on
AA Terminal-Bench 4.0, and a 0.94 AA-Omniscience hallucination rate. In this kit
it is an offline or private worker for short, checkable tasks (classification,
extraction, short summaries, grep loops) whose output the orchestrator verifies;
it is not for code edits, unsourced facts or anything that must land. This
profile comes from research only; nothing here was run by this kit.

## Strengths

- **Fits one machine.** The checkpoint is 12.8 GiB and the Ollama tag 14 GB; Simon
  Willison saw "just 11.72GB of my system RAM" in LM Studio
  (`research/open-weights-small.md § Model 2 §2`;
  [SW](https://simonwillison.net/2025/Aug/5/gpt-oss/)). It ships in MXFP4, so
  further quantization buys little: "Always use the original MXFP4 model files"
  ([LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396)).
- **Fast and cheap hosted.** AA: 258 tok/s, $0.058 / $0.215 per MTok, about
  $0.01 per Index task, "fairly concise" at 70M output tokens on the Index vs an
  82M median ([AA](https://artificialanalysis.ai/models/gpt-oss-20b);
  `§ Model 2 §2`).
- **Math and STEM at high effort.** AIME 2025 89.3 and GPQA Diamond 68.8 (AA,
  independent) vs 91.7 and 71.5 (OpenAI, self-reported); LiveCodeBench 77.7 (AA)
  ([CARD](https://arxiv.org/abs/2508.10925) Table 3;
  [AA](https://artificialanalysis.ai/models/gpt-oss-20b); `§ Model 2 §2`).
- **Trained for tools and structured output.** Post-trained on browsing, Python
  and "arbitrary developer functions" ([CARD](https://arxiv.org/abs/2508.10925)).
  AA tau2 60.2 at high and 50.3 at low (independent); Tau-Bench Retail 54.8
  (self-reported). Practitioners: "a tool calling god" for a ripgrep loop
  ([HN-postalcoder](https://news.ycombinator.com/item?id=46628688)), "had no
  trouble in Pi" ([HN-accrual](https://news.ycombinator.com/item?id=48928098)),
  "capable of operating tools like bash in a reasonably useful way" on a 32 GB
  laptop ([HN-simonw2](https://news.ycombinator.com/item?id=45844631)).
- **Classification.** Best local model, 95.6%, in one user's spam-filter
  benchmark (August 2025), ahead of gemma3:27b (94.3%) and qwen3:32b (89.2%)
  ([HN-jwr](https://news.ycombinator.com/item?id=44815446)). Single benchmark,
  unverified.
- **Configurable effort, open licence.** Low, medium and high set "with one
  sentence in the system message"; Apache 2.0 plus a short usage policy
  ([OAI](https://openai.com/index/introducing-gpt-oss/);
  [HFCARD](https://huggingface.co/openai/gpt-oss-20b)).

## Weaknesses and failure modes

- **Hallucinates facts heavily.** SimpleQA accuracy 0.067 with a 0.914
  hallucination rate (self-reported, [CARD](https://arxiv.org/abs/2508.10925)
  Table 9); AA-Omniscience index -63.05 with a 0.941 hallucination rate
  ([AA](https://artificialanalysis.ai/models/gpt-oss-20b)), vs 0.303 for Qwen3.8
  27B. "As soon as a solution isn't clear it will hallucinate"
  ([HN-strangescript](https://news.ycombinator.com/item?id=46680313)). Never use
  it as a knowledge source without retrieval (`§ Model 2 §3`).
- **Reports edits it did not make.** In a 24 GB M4 lint-fixing test it
  "frequently made mistakes like adding or duplicating statements unnecessarily,
  listing things as fixed without editing the code"
  ([HN-quacker](https://news.ycombinator.com/item?id=48089940)). Its "done"
  counts for nothing; diff and re-run tests.
- **Weak at agentic coding.** AA Terminal-Bench 4.0 0%, Terminal-Bench 2.1 13.9%
  (vs 26.2% for gpt-oss-120b and 79.8% for Qwen3.8 27B); Aider Polyglot 34.2
  (self-reported) ([AA](https://artificialanalysis.ai/models/gpt-oss-20b);
  `§ Model 2 §3`).
- **Loops at high effort with many tools.** "Randomly results in reasoning loops
  where the model keeps repeating itself" with about 8 tools bound; open issue
  ([OLISS-12606](https://github.com/ollama/ollama/issues/12606)). High also
  "thought for 5 minutes and 50 seconds" and overflowed LM Studio's default
  4096-token context in one test ([SW](https://simonwillison.net/2025/Aug/5/gpt-oss/)).
- **Weak long-context reading.** AA-LCR 34.7% vs 82% for Qwen3.8 27B despite the
  131K window ([AA](https://artificialanalysis.ai/models/gpt-oss-20b)). In one
  hash-recall test, "Past 32k characters the response contained hallucinations"
  ([HN-mhitza](https://news.ycombinator.com/item?id=49097572); unverified).
  Keep inputs under about 16K tokens.
- **Weaker instruction hierarchy, so prompt-injection risk.** "gpt-oss-120b and
  gpt-oss-20b generally underperform OpenAI o4-mini on our instruction hierarchy
  evaluations" ([CARD](https://arxiv.org/abs/2508.10925)). Do not give it write
  tools while it reads untrusted pages or files.
- **Tool calling depends on the runtime.** Providers differed: old vLLM on Azure
  "didn't respect reasoning_effort", and "Tool calling is particularly vulnerable
  to these differences" ([SW-PROV](https://simonwillison.net/2025/Aug/15/inconsistent-performance/)).
  Open Ollama bugs: HTTP 500 "error parsing tool call" on "roughly 2 in 5" calls
  with an `apply_patch`-style tool ([OLISS-17638](https://github.com/ollama/ollama/issues/17638)),
  `enum` values dropped from tool schemas ([OLISS-12763](https://github.com/ollama/ollama/issues/12763)),
  tool calls not completing in Open WebUI on macOS
  ([OLISS-12187](https://github.com/ollama/ollama/issues/12187)). At launch, in
  Cline, "Tools calling doesn't work" ([HN-NicoJuicy](https://news.ycombinator.com/item?id=44803073);
  day-one software, may be fixed).
- **Template bugs.** Unsloth found four jinja-template bugs (backslashed strings in
  tool calls, extra newlines, wrong `final` and `analysis` tags), and the HF repo
  changed its chat template twice in August 2025
  ([UNSLOTH](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune);
  [HFCARD](https://huggingface.co/openai/gpt-oss-20b)).
- **Effort levels are uneven.** Low is much weaker (AA AIME25 62.3 vs 89.3 at
  high). AA shows Low's index as an estimated "10*", above High's 9; every
  measured low score is lower, so treat that as an artefact (`§ Model 2 §3`).
- **Stale and text only.** Knowledge cutoff June 2024 per OpenAI, May 31 2024 per
  AA ([OAIDEV](https://developers.openai.com/api/docs/models/gpt-oss-20b)).
- **Misconceptions to ignore.** "Runs in 16 GB" does not mean a 16 GB Mac runs it
  well (see Cost notes). There is no 2026 "gpt-oss-20b-a3b" with 256K context;
  that claim traces to one low-trust content site
  ([FAN](https://freeainews.com/open-source/openai-gpt-oss-open-weight-2026/);
  `§ Model 2 §1`).

## How to prompt it

No hands-on prompting in this kit; everything below is from OpenAI's docs and
practitioners (`research/open-weights-small.md § Model 2 §5, §7`).

- **Harmony format only.** The model "should only be used with the harmony
  format as it will not work correctly otherwise"
  ([HFCARD](https://huggingface.co/openai/gpt-oss-20b)). Ollama, llama.cpp
  (`--jinja`), LM Studio and the hosted providers apply it for you; check the
  template version if tool calls misparse.
- **Roles.** The system message carries effort, dates and built-in tools. The
  developer message is "what is commonly considered the 'system prompt'": task
  rules, function definitions and response formats
  ([HARMONY](https://cookbook.openai.com/articles/openai-harmony)). Hierarchy is
  system over developer over user, but do not rely on it against injected text.
- **Effort in the system message:** `Reasoning: low`, `Reasoning: medium`
  (default) or `Reasoning: high`. Ollama: `"think": "low"` on `/api/chat`, or
  `ollama run gpt-oss:20b --think=low --hidethinking`. llama.cpp:
  `--chat-template-kwargs '{"reasoning_effort": "low"}'`. Low for classification
  and extraction, medium for tool loops, high only for math or logic with 16K+
  context and a loop guard.
- **Channels.** `analysis` holds the chain of thought, `commentary` carries
  function calls and occasional preambles, `final` is the answer. Parse only
  `final` as the deliverable. Drop the previous chain of thought after a `final`
  message, but pass it back between tool calls in the same turn
  ([HARMONY](https://cookbook.openai.com/articles/openai-harmony)).
- **Never show the chain of thought to users.** "Developers should not directly
  show CoTs to users"; they "may contain hallucinated or harmful content"
  ([OAI](https://openai.com/index/introducing-gpt-oss/)).
- **Sampling.** `temperature=1.0`, `top_p=1.0`. "**Do not use repetition
  penalties!**" ([LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396)).
  Unsloth adds `top_k=0` and a "recommended minimum context: 16,384".
- **Enforce schemas in the runtime.** A schema in the prompt "doesn't guarantee
  the full adherence to the schema" ([HARMONY](https://cookbook.openai.com/articles/openai-harmony)).
  Declare it under `# Response Formats` in the developer message and also pass it
  as Ollama's `"format": {<JSON schema>}` on `POST /api/chat` (Ollama: "It is
  ideal to also pass the JSON schema as a string in the prompt"). The `ollama`
  bridge's `/v1` body has no effort or schema field; use `/api/chat` for both
  (unverified here: no model pulled).
- **Ground facts.** Supply the documents or give it a browsing or search tool;
  "browsing or gathering external information tends to reduce instances of
  hallucination" ([CARD](https://arxiv.org/abs/2508.10925)). Treat any fact
  without a quoted source as unverified.
- **Keep prompts short.** Pi's initial prompt is about 1.5K tokens vs 7-10K for
  other CLIs ([HN-abhikul0](https://news.ycombinator.com/item?id=47134991));
  Claude Code's is 15-40K ([HN-d4rkp4ttern](https://news.ycombinator.com/item?id=47620689)).
  On a small machine, use Pi or a direct API call, one task per call, with an
  example of the expected output.
- **Ids by route:** Ollama `gpt-oss:20b`; OpenCode `-m ollama/gpt-oss:20b`
  (bridge format; exact string unverified, check `opencode models`); OpenRouter
  `openai/gpt-oss-20b`; llama.cpp `-hf ggml-org/gpt-oss-20b-GGUF`; MLX
  `mlx-community/gpt-oss-20b-MXFP4-Q4`; Codex `codex --oss -m gpt-oss:20b`
  (pulls the 14 GB model automatically if missing,
  [CODEX](https://github.com/openai/codex/blob/main/codex-rs/ollama/src/lib.rs)).

## Routing guidance

**For a user with frontier access** (any hosted Claude, GPT, Gemini or cheap
2026 API model):
- Route here only as an offline or private tier: data that cannot leave the
  machine, or no network. Hosted cheap models dominate it on capability
  (`§ Model 2 §8`; `research/model-gaps.md § 4f`, update 2026-10-19).
- For non-private bulk work, prefer the profiled cheap tier: GPT-6 Luna, DeepSeek
  V4.1 Flash, Gemini 3.8 Flash, or Claude Haiku 5.5 for an Anthropic-only user
  (`research/model-gaps.md § Suggested routing-table shortlist`). If the user
  specifically wants gpt-oss, a hosted 20b or 120b on OpenRouter costs a few
  cents per MTok and is far faster than a laptop
  ([OR](https://openrouter.ai/openai/gpt-oss-20b)).

**For a local-only user:**
- On a 16 GB machine this is the model that fits. Use it for checkable bulk
  work with the orchestrator verifying: Ollama or llama.cpp at 8K to 16K context,
  `low` or `medium` effort, schema enforced by the runtime, one request at a time
  (`§ Cross-model synthesis › Routing shortlist`).
- With 24 GB or more, the stronger local option is Qwen3.8 27B (AA 34, 18 GB at
  Q4); on 16 GB, practitioners prefer Qwen 3.5 9B for coding (unverified, no
  profile) (`§ Model 2 §8`). gpt-oss-120b needs 65 GB in Ollama.

Route here for:
- Classification and triage with a schema enforced by Ollama `format`.
- Extraction to JSON.
- Short summaries of supplied text (under about 16K tokens).
- grep or ripgrep tool loops that return file paths and quotes for the
  orchestrator to check.

Do not route here for:
- Code edits, refactors or PR work (Terminal-Bench 4.0 0%, false "fixed" claims).
- Factual Q&A without sources (hallucination rate 0.94).
- Long-document reading over about 16K tokens (AA-LCR 34.7%).
- Claude Code, OpenCode or Codex on a 16 GB Mac (all need 64K+ context).
- Reading untrusted web content with write tools enabled.
- High effort on 16 GB, or with many tools bound.
- Leading or coordinating other agents.

Handoff patterns:
- **Local worker, frontier verifier.** gpt-oss labels, extracts or locates; the
  orchestrator (or a script) checks every output and reruns misses on a stronger
  model rather than retrying this one.
- **Moderation pipelines:** use **gpt-oss-safeguard-20b**, the safety fine-tune
  that classifies content against "a developer-provided policy at inference time"
  and fits 16 GB of VRAM; its own card says "For other applications, we recommend
  using gpt-oss models" ([SAFEGUARD](https://openai.com/index/introducing-gpt-oss-safeguard/);
  [HF card](https://huggingface.co/openai/gpt-oss-safeguard-20b)).
  Not profiled.
- **Check the provider first.** Run OpenAI's compatibility test before trusting a
  new host or runtime; a correct one shows "0 invalid requests and over 90% on
  both pass@k and pass^k" ([VERIFY](https://cookbook.openai.com/articles/gpt-oss/verifying-implementations)).

## Cost notes

- **Hosted:** AA prices it at $0.058 in / $0.215 out per MTok and about $0.01 per
  Index task ([AA](https://artificialanalysis.ai/models/gpt-oss-20b)). OpenRouter
  endpoints range from $0.018 / $0.09 (Darkbloom fp8, 32,768 max output) to
  $0.075 / $0.30 (Groq); DeepInfra $0.03 / $0.14, Bedrock $0.07 / $0.15
  ([OR](https://openrouter.ai/openai/gpt-oss-20b)). No first-party price exists:
  OpenAI's API page lists the model (Responses and Batch only) with no price
  ([OAIDEV](https://developers.openai.com/api/docs/models/gpt-oss-20b)). No cache
  pricing found.
- **Local:** free per token; the cost is hardware, memory pressure on everything
  else running, and wall-clock.
- **Effort:** returns are "log-linear", "at a relatively large increase in final
  response latency and cost"; it uses "over 20k CoT tokens per problem on average
  for AIME" at high ([CARD](https://arxiv.org/abs/2508.10925)). Thinking time in
  one test: 0.07 s low, 4.44 s medium, 5 min 50 s high
  ([SW](https://simonwillison.net/2025/Aug/5/gpt-oss/)). Low or medium gives the
  value; high costs more than it returns outside math.
- **Retries:** cheap per token is not cheap per task. Count attempts to a verified
  answer; escalate on a miss instead of looping.
- **Parallelism costs memory:** Ollama "Required RAM will scale by
  `OLLAMA_NUM_PARALLEL` * `OLLAMA_CONTEXT_LENGTH`"; on 16 GB run one slot.

### Local hardware

None of this was measured by this kit. All figures are third-party, from
`research/open-weights-small.md § Model 2 §4` and §7.

Memory by context length (llama.cpp guide, decimal GB, f16 KV cache, `-ub 2048`;
[LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396)):

| Context | Model data | Compute buffers | KV cache | Total |
|---|---|---|---|---|
| 8,192 | 12.0 | 2.7 | 0.2 | **14.9** |
| 32,768 | 12.0 | 2.7 | 0.8 | **15.5** |
| 131,072 | 12.0 | 2.7 | 3.2 | **17.9** |

Larger `-ub`/`-b` values grow the compute buffers. Ollama's
`OLLAMA_KV_CACHE_TYPE=q8_0` halves the KV cache, but one user found KV
quantization on gpt-oss "bad, performance was halved" on an AMD GPU
([LCPP-SteelPh0enix](https://github.com/ggml-org/llama.cpp/discussions/15396#discussioncomment-14143427)); test it.

Third-party measured speeds (generation unless marked):

| Machine | Runtime | Setting | Result | Source |
|---|---|---|---|---|
| MacBook Pro M1, 16 GB | LM Studio | ctx 7,990; 8/24 layers on GPU; low effort | "runs slow and still fine"; with MCP tools "the tool calls instruction follow is quite good" | [HN-vinhnx](https://news.ycombinator.com/item?id=44811891) |
| MacBook Air M4, 16 GB | Ollama (Aug 2025) | defaults | "hello" took "a little more than five minutes"; one question about 43 minutes | [9TO5](https://9to5mac.com/2025/08/06/how-to-run-gpt-oss-20b-on-mac/) |
| "16GB Mac" (model not stated) | Ollama vs llama.cpp (Mar 2026) | not stated | runs with Ollama; "out of memory" with latest llama.cpp | [HN-0xbadcafebee](https://news.ycombinator.com/item?id=47370473) |
| MacBook Pro M1 Pro, 32 GB | llama.cpp | all on GPU, empty context / 16K context | 45.7 / 33.9 tok/s | [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396) |
| MacBook Pro M1 Pro, 32 GB | llama.cpp | prompt processing at 2K / 16K | 505 / 367 tok/s (44.7 s to read 16K) | [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396) |
| M2 Pro, 32 GB | not stated | not stated | "quite good"; "around 30k" context practical | [HN-mixermachine](https://news.ycombinator.com/item?id=46932292) |
| M4 Max, 36 GB | llama.cpp | empty context / 32K context | 92.4 / 64.8 tok/s | [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396) |
| MacBook Pro M2, 64 GB | llama.cpp | not stated | about 82 tok/s | [SW-LCPP](https://simonwillison.net/2025/Aug/19/gpt-oss-with-llama-cpp/) |
| MacBook Pro M2, 64 GB | LM Studio | low / medium effort | 39 / 55 tok/s | [SW](https://simonwillison.net/2025/Aug/5/gpt-oss/) |
| RTX 5060 Ti, 16 GB VRAM | llama.cpp server, Codex agentic refactor | 125K context, flash attention | about 96 tok/s; 15.75 of 16.3 GB VRAM used | [LCPP-bartlettroscoe](https://github.com/ggml-org/llama.cpp/discussions/15396#discussioncomment-14388222) |
| RTX 5090, Windows 11 | llama.cpp (CUDA), MXFP4 | llama-bench tg128 | about 327 tok/s (53 for a Qwen3.5 27B Q6_K) | [HN-magicalhippo](https://news.ycombinator.com/item?id=47942148) |

What fits:
- **16 GB Mac:** it runs, but not well, and only at short context. Metal's GPU
  budget on an M2 16 GB machine is about 12.7 GB
  ([LCPP-20704](https://github.com/ggml-org/llama.cpp/issues/20704)), and the
  model data alone is 12.0 GB, so part of the model must run on the CPU.
  llama.cpp's 16 GB recipe keeps 12 of 24 MoE layers on the CPU and caps context
  at 32K (`--n-cpu-moe 12 -c 32768`); 8K to 16K is the practical range. No tok/s
  figure exists for an M2 Pro 16 GB; expect less than the M1 Pro 32 GB's 34 to
  46 tok/s. Ollama defaults to 4K context below 24 GiB of VRAM; set
  `OLLAMA_CONTEXT_LENGTH=16384`. Ollama says Claude Code, OpenCode and Codex need
  64K or more context, so none of them fits; since Ollama v0.40.2, `ollama launch
  claude` uses the full 131K context (about 17.9 GB by the table). Use Pi or a
  direct Ollama or llama.cpp API call. One report fit 125K context on a 16 GB
  NVIDIA card with flash attention and ran Codex at about 96 tok/s (single
  source, unverified); a 16 GB Mac shares that memory with macOS and cannot.
- **24 GB:** full GPU residency with 32K+ context (15.5 GB at 32K). On a 24 GB
  Mac, the guide's 70%-of-memory rule gives about 16.8 GB (arithmetic from the
  guide, not measured), so 32K fits and the full 131K (17.9 GB) is tight; a 24 GB
  GPU holds the full context. A 24 GB M4 ran a lint-fixing test with it but it made
  repeated mistakes ([HN-quacker](https://news.ycombinator.com/item?id=48089940)).
- **32 GB:** comfortable. An M1 Pro 32 GB runs it fully on the GPU at 34 to 46
  tok/s, and the 70% rule gives about 22.4 GB (arithmetic, not measured), enough
  for the 64K those harnesses need. One M2 Pro 32 GB user found "around 30k"
  context practical, so test before relying on 64K+.

## Evidence

- `research/open-weights-small.md`: header (as of 2026-10-19, nothing run
  hands-on, reference machine M2 Pro 16 GB); `§ Model 2 §1` (no newer
  checkpoint, false June 2026 refresh, corrections to model-gaps), `§2`
  strengths, `§3` weaknesses, `§4` specs, memory and speed tables and hosted
  prices, `§5` prompting, `§6` delegation and verification, `§7` harness
  commands, `§8` routing implications; `§ Cross-model synthesis` and its routing
  shortlist.
- `research/model-gaps.md § 4f. MiniMax M3 and gpt-oss` (with the 2026-10-19
  update note: AA 9, 131,072 context, no newer checkpoint) and `§ Suggested
  routing-table shortlist` (Local / offline tier).
- Saved copy of OpenAI's API page (`articles/gpt-oss/openai-platform-gpt-oss-20b-and-open-models.md`
  in the private sources repo): endpoint table showing Responses and Batch
  supported and Chat Completions "Not supported"; no price listed. This detail is
  not in the digest itself.
- Saved copies of the HN-magicalhippo and LCPP-bartlettroscoe comments for the GPU
  model and runtime of those two speed rows.
- Primary URLs: [OAI](https://openai.com/index/introducing-gpt-oss/),
  [CARD](https://arxiv.org/abs/2508.10925),
  [HFCARD](https://huggingface.co/openai/gpt-oss-20b),
  [OAIDEV](https://developers.openai.com/api/docs/models/gpt-oss-20b),
  [HARMONY](https://cookbook.openai.com/articles/openai-harmony),
  [VERIFY](https://cookbook.openai.com/articles/gpt-oss/verifying-implementations),
  [SAFEGUARD](https://openai.com/index/introducing-gpt-oss-safeguard/),
  [AA](https://artificialanalysis.ai/models/gpt-oss-20b),
  [AA-LOW](https://artificialanalysis.ai/models/gpt-oss-20b-low),
  [OR](https://openrouter.ai/openai/gpt-oss-20b),
  [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396),
  [OLLIB](https://ollama.com/library/gpt-oss),
  [OLDOCS](https://github.com/ollama/ollama/tree/main/docs),
  [CODEX](https://github.com/openai/codex/blob/main/codex-rs/ollama/src/lib.rs),
  [UNSLOTH](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune).
- **Self-reported:** every OpenAI model-card number (AIME, GPQA, SWE-bench
  Verified, Tau-Bench, Aider Polyglot, SimpleQA, instruction hierarchy).
- **Unverified (single source):** the spam-filter benchmark (HN-jwr), the
  hash-recall 32K limit (HN-mhitza), the lint-test behaviour (HN-quacker), the
  RTX 5060 Ti 125K-context run, the RTX 5090 figure, and every forum speed or
  "runs slow" report. AA figures are independent but from one aggregator.
- **Not found:** a tok/s figure for an M2 Pro 16 GB; a measured MLX speed on
  Apple silicon; per-level output-token counts for low and medium; any
  first-party price; any computer-use, frontend, copy or prompt-writing evidence.
- **Not tested in this kit:** everything. Ollama is installed on the reference
  machine with no model pulled (`core/bridges/ollama.md`).

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 1 | AA index 9, below Claude Haiku 4.5 (AA 17, scored 2) and far below Qwen3.8 27B (34) and Opus 5.5 (54); AA Terminal-Bench 4.0 0%. Strong AIME at high (89.3, AA) does not carry over to unsupervised work. |
| taste | 1 | Text only; low effort produced invalid SVG; duplicated statements in a lint test; no copy or UI evidence. |
| floor | 2 | Reports edits it did not make, hallucinates (0.94 AA-Omniscience), loops at high effort, Ollama tool-call parse errors; holds up only on short schema-enforced tasks (95.6% spam-filter, unverified). |
| thoroughness | 2 | AA-LCR 34.7% and hallucinations past 32K characters; the only review use reported is a fixed-checklist first pass. |
| cost_efficiency | 7 | About $0.01 per AA task hosted and free per token locally, the cheapest in the kit; held below Luna's 8 because outside narrow checkable work its success rate is low and retries and verification dominate cost. |
| speed | 8 | Its strongest axis: 258 tok/s hosted with concise output, 82 to 92 tok/s on 36 to 64 GB Macs and about 327 on an RTX 5090; on a 16 GB Mac it is slow (CPU offload, minutes for long prompts), and high effort thinks for minutes. |
| computer_use | 1 | Text only; cannot read screenshots. |
| orchestration | 1 | Research: "a worker, never the orchestrator"; weak instruction hierarchy and tool loops at high effort. |
