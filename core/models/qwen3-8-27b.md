---
id: qwen3-8-27b
name: Qwen3.8-27B
vendor: alibaba
family: open-weights
status: current
released: 2026-08                # 2026-08-14 (QwenLM GitHub news, HF repo timestamp, AA)
as_of: 2026-10-19
confidence: medium               # independent AA index and Quesma quant runs plus several practitioners (Simon Willison, HN, Paul Brown); no hands-on use in this kit, and every local speed is third-party

api_ids:
  - qwen3.8-27b                  # QwenCloud (official hosted API, OpenAI-compatible)
  - qwen/qwen3.8-27b             # OpenRouter (20 endpoints, prices vary widely)
  - "qwen3.8:27b"                # Ollama library tag (Q4_K_M, 18 GB); other tags: 27b-mlx, 27b-mtp-q4_K_M, 27b-q8_0, 27b-bf16. Quoted: the colon would otherwise be read as a mapping
  - Qwen/Qwen3.8-27B             # Hugging Face weights (BF16); FP8 build is Qwen/Qwen3.8-27B-FP8; GGUFs from unsloth/ and ggml-org/
access:
  subscriptions: []
  api: true
  harnesses: [opencode, pi]      # the practitioner-reported coding agents. Not listed: claude-code, because the generator would print "this session" for a Claude-subscription user; Claude Code reaches this model only in a separate session pointed at Ollama's Anthropic API (`ollama launch claude --model qwen3.8`) or MTPLX. Qwen Code and LM Studio also drive it but are not kit harness ids
  invoke_via: [ollama, opencode-cli, pi-cli, openrouter-api]   # ollama: one-shot, no tools, needs the 18 GB tag; opencode-cli: `-m ollama/qwen3.8` locally or OpenRouter hosted (provider strings unverified); pi-cli: custom models.json provider (Simon Willison's config) or OpenRouter; openrouter-api: `qwen/qwen3.8-27b`, no tools

pricing_per_mtok:                # QwenCloud official hosted price; running locally costs nothing per token
  input: 0.50
  output: 3.00
  cache_read: 0.10               # implicit cache; explicit cache read is 0.05
  cache_write: 0.625             # explicit cache write
context_window: 262144           # native open-weights context; QwenCloud and OpenRouter's Alibaba endpoint serve 1M; 1M locally needs YaRN, which Qwen says may hurt short texts
notes_on_cost: >
  Hosted, it is expensive for its class: Artificial Analysis measures $1.01 per index
  task at the default xhigh effort (AA 34), against $0.37 for the hosted sibling
  Qwen3.8-Flash-Next (AA 40, $0.15 / $0.47 per MTok), $0.07 for GPT-6 Luna (AA 38) and
  $0.01 for gpt-oss-20b. AA says it is "particularly expensive when comparing to other
  open weight models of similar size". The driver is verbosity: 200M output tokens to
  run the index at xhigh (25th of 27), and lower effort does not make it cheaper per
  task ($1.13 medium, $1.05 low). OpenRouter endpoints range from $0.50 to $3.20 per
  MTok output, some with capped context, so check the endpoint before routing. Run
  locally, the cost is hardware and wall-clock, not dollars: 10 to 45 tok/s on Apple
  silicon, and a single xhigh answer has taken 17 to 21 minutes. Users running it
  locally should set a high `cost` for it in config.yaml; the cost_efficiency score
  below is the hosted view.

effort:
  levels: [none, low, medium, xhigh]   # Qwen's own levels: thinking off (none), low, medium, xhigh; there is no "high"
  default: medium                # kit default (research Model 1 §8: medium for agent loops); Qwen's own default is xhigh, which the kit never leaves unexamined
  avoid: [xhigh]
  notes: >
    Qwen ships xhigh as the default and it over-thinks badly (21 minutes and 22,276
    reasoning tokens for one SVG; Simon Willison: "a hilarious default"), so never leave
    it unexamined; use xhigh only for a hard, instruction-heavy one-shot you can wait
    for. Use none or low for classification, extraction, short summaries and bounding
    boxes, medium for agent loops and exact multi-step answers. Qwen warns that in
    multi-turn agentic tasks lower effort "can also lead to insufficient analysis, more
    failures, and repeated retries", and IFBench drops from 81.7% at xhigh to 65.3%
    medium and 60.5% low (Quesma), so test low before using it in an agent loop.

scores:
  intelligence: 3
  taste: 2
  floor: 3
  thoroughness: 4
  cost_efficiency: 3
  speed: 2
  computer_use: 2
  orchestration: 2

tasks:
  quick-fix:      {fit: ok,      note: "Local-only users: a credible coding agent at Q4 on 32 GB+ through Pi or OpenCode (Simon Willison built and tested a converter; Quesma Terminal-Bench 2.1 70.8%, independent). Verify with tests; slow interactive loop."}
  feature:        {fit: ok,      note: "Local-only users on 32 GB+ with tests and review: one-shotted a web app and a Rust rewrite with one bug (anecdotal). DeepSWE 42.2 (self-reported) is far below the frontier; frontier users route elsewhere."}
  long-run:       {fit: poor,    note: "Agent context overflows at 64K, xhigh answers take 17-21 minutes, Qwen looping reported at medium; one 10+ hour debugging success is a single anecdote."}
  frontend:       {fit: unknown, note: "No evidence on design quality; gold-plates at high effort (an unrequested animated circle, a 'massively over-engineered' tool)."}
  review:         {fit: unknown, note: "No evidence on diff review. AA-Omniscience hallucination rate 0.30 is low, but untested as a reviewer."}
  investigate:    {fit: ok,      note: "Anecdotal: found a Next.js framework bug after 10+ hours unattended on a 48 GB Mac, and a real repo bug with GitHub MCP tools. Slow; confirm every finding."}
  analyze:        {fit: good,    note: "Codebase Q&A with tool calls was 'very solid' (Simon Willison, 'how does auth work?'); AA-LCR 82%. Best local generalist for this; a frontier model checks conclusions."}
  bulk:           {fit: good,    note: "Private or local classification, JSON extraction, image labelling and summaries of noisy output at none or low effort ('near-perfect' spam benchmark, unverified). Hosted, Flash-Next is smarter and about 3x cheaper per task."}
  research:       {fit: ok,      note: "Long-context reading (AA-LCR 82%) and a low hallucination rate (0.30) suit summarisation; no evidence on web research runs. Slow; verify sources."}
  computer-use:   {fit: unknown, note: "OSWorld-Verified 84.3 is self-reported with no independent number; good bounding-box JSON from images, but no harness evidence and speed makes driving a UI impractical."}
  copy:           {fit: unknown, note: "No evidence."}
  3d-games:       {fit: unknown, note: "No evidence."}
  prompt-writing: {fit: unknown, note: "No evidence."}
  babysit:        {fit: poor,    note: "Must-land polling loop; slow, low floor, and context fills fast."}
  orchestrate:    {fit: poor,    note: "No evidence of leading agents; subagent context overflowed a 64K window in opencode."}

role_hints:
  as_primary: "For a local-only user on a 32 GB+ Mac or 24 GB GPU: the primary local coding agent and generalist (Q4_K_M, medium effort, 64K+ context, Pi or OpenCode), good for codebase Q&A, bounded edits checked by tests, image and document reading. Not a primary for anyone with frontier access, and not on 16 GB."
  as_subagent: "Cheap private subagent for codebase Q&A, classification, JSON extraction, image and long-document reading, and summarising noisy output, at none, low or medium effort, with output checked by tests or a frontier model."
  never_for: ["xhigh as an unexamined default", "1-bit quants", "interactive coding on a 16 GB machine", "long unattended runs", "hosted bulk work (Flash-Next is smarter and cheaper)", "code that merges without tests and review", "leading other agents"]

local:                            # read by the generator against config.hardware; see core/models/_schema.md
  runs_locally: true
  licence: apache-2.0
  runtimes: [ollama, llama-cpp, lm-studio, mlx, vllm]
  runtimes_by_quant:              # which runtimes ship a build this small; Ollama's smallest tag is Q4 (18 GB), LM Studio and MLX 16 GB
    q3: [llama-cpp]
    q2: [llama-cpp]
    q1: [llama-cpp]
  memory_gb_by_quant:             # total VRAM or unified memory for weights plus a working context, third-party figures
    bf16: 56
    q8: 31
    q4: 18                        # Ollama qwen3.8:27b tag; Unsloth says 16-19 GB, Quesma: Q4_K_M matches BF16 on Terminal-Bench 2.1
    q3: 13
    q2: 11                        # UD-Q2_K_XL; Terminal-Bench 2.1 drops to 64%
    q1: 7                         # unusable: GPQA near chance
  min_memory_gb: 11
  preferred_quant: q4             # Quesma: Q4_K_M matches BF16 on Terminal-Bench 2.1, so spend spare memory on context, not Q8
  recommended_memory_gb: 24       # usable memory for Q4 with 64K context: a 24 GB GPU or a 32 GB Mac
  measured_speed:                 # third-party measurements only; machine, runtime, quant, tok/s, source key
    - {machine: "M5 Max 128 GB MacBook Pro; DGX Spark", runtime: "LM Studio, Q4_K_M (17 GB)", tok_s: "15-30", source: "SW"}
    - {machine: "M4 Pro Mac mini 64 GB", runtime: "LM Studio", tok_s: 12.75, source: "HNREL"}
    - {machine: "M1 Max", runtime: "not stated", tok_s: 9.5, source: "HNREL"}
    - {machine: "M1 Max", runtime: "not stated, 'Reasoning level: low' in the prompt", tok_s: "10-13", source: "HNSW"}
    - {machine: "M1 64 GB", runtime: "oMLX, 4-bit, Pi (65 tok/s prompt processing)", tok_s: 11, source: "HNSW"}
    - {machine: "M4 MacBook Pro 64 GB", runtime: "Ollama qwen3.8:27b-mlx", tok_s: 45, source: "HNREL"}
    - {machine: "M5 Pro 48 GB", runtime: "Ollama", tok_s: 20, source: "HNREL"}
    - {machine: "M4 Max 48 GB", runtime: "mtplx", tok_s: 25, source: "HNSW"}
    - {machine: "M5 Max", runtime: "MTPLX (vendor figure, self-reported)", tok_s: "35-88", source: "MTPLX"}
    - {machine: "RTX 5060 Ti 16 GB", runtime: "llama.cpp, UD-IQ4_XS, 64K context, q4_0 KV (888 tok/s prompt processing)", tok_s: 24.9, source: "PAUL"}
    - {machine: "RTX 5070 Ti 16 GB", runtime: "UD-Q2_K_XL, 128K context, q4 KV (runtime not stated)", tok_s: "50-60", source: "HNREL"}
    - {machine: "RTX 3060 12 GB (spills to system RAM)", runtime: "Ollama", tok_s: 2.41, source: "HNREL"}
---

## Summary

Qwen3.8-27B is Alibaba's dense 27B open-weights model (Apache 2.0, released
2026-08-14): one hybrid-thinking checkpoint with vision and video input and a
262K native context. It is the smartest open model in its size class (AA 34,
#1 of 141 in AA's 4B-40B class) and drives coding agents, but it is slow
because it is dense and wildly verbose at its default `xhigh` effort. For a
user who runs models locally on a 32 GB+ Mac or a 24 GB GPU it is the best
local generalist and coding agent, verified by tests; for a user with frontier
access it is at most a cheap private subagent, and hosted it loses to
Qwen3.8-Flash-Next on both price and score. Nothing here was run by this kit;
every number is from `research/open-weights-small.md` Model 1.

## Strengths

- **Best in its class on an independent index.** AA Intelligence Index 34 at
  the default `xhigh`, #1 of 141 open-weights models in AA's 4B-40B "Small"
  class (`research/open-weights-small.md § Model 1 §1`, §2;
  [AA](https://artificialanalysis.ai/models/qwen3-8-27b)). Its predecessor
  Qwen3.6-27B scores 21 and Qwen3-Coder-Next 9.
- **Vendor benchmarks replicate where checked.** Quesma's independent BF16 run
  gives Terminal-Bench 2.1 70.8% (self-reported 73.0), GPQA Diamond 89.9%
  (self-reported 89.2) and IFBench 81.7% strict (self-reported 79.5) at xhigh.
  Piotr Migdał: "I was happy I replicated the official results" (§2;
  [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/)). AA
  lists Terminal-Bench 2.1 at 79.8%. SWE-bench Pro 61.7, DeepSWE 42.2,
  OSWorld-Verified 84.3 and LiveCodeBench v6 90.3 are self-reported with no
  independent number found.
- **Drives a coding agent.** Simon Willison: "Yes, it can drive coding
  agents... My initial experiments with Pi have been very promising." Its
  answer to "how does auth work?" in the Datasette repo was "very solid", and
  it "built and tested" a JSONL-to-Markdown converter "which did exactly what I
  needed" (§2; [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/)).
  Anecdotal reports: a Next.js framework bug found after "10+ hours of digging"
  on a 48 GB M4 MacBook Pro with llama.cpp and Pi
  ([HNSW](https://news.ycombinator.com/item?id=49328527)); "It one-shotted the
  Web app, had no bug. The Rust rewrite only had one bug" through OpenCode
  ([HNREL](https://news.ycombinator.com/item?id=49308246)); a real repo bug
  found with GitHub MCP tools
  ([PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html)).
- **Quantization-robust down to 4-bit.** Q4_K_M (17 GB) matches BF16 on
  Terminal-Bench 2.1 (70.8% both) and GPQA (90.4% vs 89.9%); IFBench shows "no
  change between models, down to a decent 2-bit one" (§2, §4; QUESMA).
- **Long context and honesty.** AA-LCR 82% (gpt-oss-20b 34.7%) and an
  AA-Omniscience hallucination rate of 0.30 (gpt-oss-20b 0.94) (§ Cross-model
  synthesis; Model 2 §3, citing
  [AA](https://artificialanalysis.ai/models/qwen3-8-27b)).
- **Vision and structured output.** JSON `bbox_2d` bounding boxes on a 0-1000
  scale were "such a good match" (§2; SW). Classification: "near-perfect score
  on my E-mail spam filtering benchmark, best of any model I tested, ever. But
  it is slow" ([HNREL](https://news.ycombinator.com/item?id=49301283);
  unverified, one private benchmark).
- **Exact with reasoning on.** At medium effort it wrote sums in words
  correctly "167 out of 169 attempts" (§2;
  [SWADD](https://simonwillison.net/2026/Oct/4/qwen38-addition-in-words/)).
- **Open and widely packaged.** Apache 2.0, unlike Flash-Next
  (`qwen-community-1.0`) and the 2.4T flagship (custom licence). Day-zero GGUF
  and NVFP4 builds; Ollama tags it vision, tools and thinking; Qwen's own
  coding benchmarks were run "with the Claude Code harness" (self-reported)
  (§2, §6; [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B),
  [UNS](https://unsloth.ai/docs/models/qwen3.8),
  [OLL](https://ollama.com/library/qwen3.8)).

## Weaknesses and failure modes

- **The default `xhigh` over-thinks.** Simon's pelican SVG "took **21
  minutes** to generate, using 22,276 reasoning tokens to produce 3,223 tokens
  of output... Was that worth waiting 21 minutes for? Absolutely not." An "svg
  owl" took 17m12s on an M4 Pro Mac mini. AA counts 200M output tokens to run
  its index, 25th of 27 for verbosity (§3; SW,
  [HNREL](https://news.ycombinator.com/item?id=49307087), AA).
- **It gold-plates.** For "draw an svg of a circle" it produced "this
  absolutely beautiful animated circle, which was entirely not what I had asked
  for!"; a bounding-box tool came with an unrequested demo scene, "massively
  over-engineered" (§3; SW).
- **Lower effort trades quality.** IFBench (BF16, strict) falls from 81.7% at
  xhigh to 65.3% at medium and 60.5% at low; AA falls from 34 to 28, 26 and 20
  with reasoning off. Qwen warns lower effort in agent loops can mean "more
  failures, and repeated retries" (§3; QUESMA, AA, HFCARD).
- **Looping at medium** ("the very typical Qwen looping. Not seen looping in
  the 'low' reasoning effort mode") (§3;
  [HNSW](https://news.ycombinator.com/item?id=49325856); unverified).
- **Slow, because it is dense.** Every weight is read for every token. 9.5 to
  30 tok/s on most Apple silicon reports, 44.4 tok/s hosted with a 3.95 s time
  to first token against a class median of 79.8 tok/s and 1.12 s; spilling out
  of VRAM collapses it to 2.41 tok/s (§3; SW, AA, HNREL).
- **Arithmetic without reasoning fails.** 23.57% on sums in words with
  reasoning off, 6.44% for 10-13 digit operands (§3; SWADD).
- **Agent context fills fast.** "request (71461 tokens) exceeds the available
  context size (65536 tokens)" (PAUL); an opencode subagent's compacted context
  overflowed and "errored out"; agent preambles take 5K to 25K tokens before
  the user prompt (§3; [HNCB](https://news.ycombinator.com/item?id=49591719)).
- **1-bit is useless and 2-bit costs agentic skill.** UD-IQ1_S scores 10.4% on
  GPQA, around chance, and "longer reasoning makes it worse". UD-Q2_K_XL drops
  Terminal-Bench 2.1 to 64.0% and writes 1.27x more tokens (§3; QUESMA).
- **Tooling traps.** llama.cpp builds before 2026-08-16 do not work ("fluent
  garbage on CUDA" before b10450); Unsloth GGUFs were replaced with Dynamic
  V3.0 builds on 2026-08-19, so re-download older files; one user saw Unsloth's
  Q8_K_XL loop where bartowski's Q8_0 did not (unverified). LM Studio defaults
  to 8,192 context and Ollama to 4K below 24 GiB of VRAM, both too small (§3).
- **Obsessive.** It "will do insane/unusual things to get to the solution",
  "similarly obsessive" to GPT-5.6-Sol-max (§3;
  [HNAA](https://news.ycombinator.com/item?id=49336610); unverified, one forum
  report). Do not skip verification because the index is high for its size.
- **Hosted, it is not a cheap worker.** $1.01 per AA task, about 100x
  gpt-oss-20b and almost 3x Flash-Next, which scores higher (§3; AA).

## How to prompt it

- **Set effort on every call; never leave `xhigh`.** Simon: "My strong
  recommendation: ignore that default. Run Qwen 3.8 27B on low or even no
  reasoning levels at first" (§5; SW). The levels are thinking off, `low`,
  `medium` and `xhigh`; there is no `high`.
  - `none` or `low`: classification, extraction, short summaries, bounding
    boxes.
  - `medium`: agent loops and exact multi-step answers.
  - `xhigh`: only a hard, instruction-heavy one-shot where waiting is fine.
  - Lower effort in agent loops can mean more retries; test it per task.
- **Check that the effort setting actually reaches the model.**
  - llama.cpp trap: `--reasoning-effort none` fails with "Jinja Exception:
    Unexpected reasoning effort none". Use `--reasoning off` for the whole
    server, or `"reasoning_effort": "none"` in a single request body. Unsloth
    lists `none` as a level, which is the trap (§3; PAUL, UNS). For a level,
    use `--chat-template-kwargs '{"reasoning_effort":"low"}'` (or `medium`)
    (§7; UNS).
  - The `ollama` bridge's OpenAI-style body has no effort field
    (`core/bridges/ollama.md`), so a plain curl call runs at Qwen's `xhigh`
    default. How Ollama's CLI `--think low|medium|high` maps onto Qwen's levels
    is not found; Qwen has no `high`.
  - QwenCloud turns thinking on with `extra_body={"enable_thinking": True}`
    (§7; QCLOUD); the hosted field for choosing a level was not found.
    OpenRouter's `reasoning_effort` handling for this model is unverified
    (`core/bridges/openrouter-api.md`).
  - "Reasoning level: low" written in the prompt reportedly works ("it is
    actually really pretty solid") (§5;
    [HNSW](https://news.ycombinator.com/item?id=49332582)); unverified, so do
    not rely on it in place of the runtime setting.
- **Sampling (official, HFCARD):**

  | Mode | temperature | top_p | top_k | min_p | presence_penalty | repetition_penalty |
  |---|---|---|---|---|---|---|
  | Thinking | 1.0 | 0.95 | 20 | 0.0 | 0.0 | 1.0 |
  | Non-thinking | 0.7 | 0.80 | 20 | 0.0 | 1.5 | 1.0 |

  presence_penalty can go up to 2 "to reduce endless repetition", but "a higher
  value may occasionally result in language mixing" (§5).
- **`preserve_thinking`** is on by default and "retains thinking blocks from
  all historical messages". Keep it on for agent loops (better KV cache use,
  possibly better accuracy); set `preserve_thinking: false` for one-shot batch
  jobs on a small context (§5; HFCARD, UNS).
- **Size the context first.** At least 32K for anything, 64K or more for
  agents ("OpenCode requires a context length of 64k or higher"). In Ollama set
  `OLLAMA_CONTEXT_LENGTH=64000 ollama serve` and check with `ollama ps`; in LM
  Studio raise the 8,192 default (§5, §7; OLL, SW). Prefer Pi for its short
  system prompt (§6; SW).
- **Scope tightly.** State the output format and say "no extras". A nudge
  ("Hey, finish up," or "Review the syntax") reportedly ends a long think
  (§5; [HNREL](https://news.ycombinator.com/item?id=49307615); unverified).
- **Hand arithmetic and exact facts to tools.** Without reasoning,
  multi-digit arithmetic fails; one user calls it "perfect for situations
  where it can just tool call a web search" (§5;
  [HNAA](https://news.ycombinator.com/item?id=49335776); unverified).
- **Vision:** ask for JSON `bbox_2d` on a 0-1000 scale (§5; SW).
- **Time out long calls.** Qwen Code's local-model example sets `timeout`
  300000 and `streamIdleTimeoutMs` 600000 (§6;
  [QCODE](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/)).
  Thinking-budget flags in llama.cpp (`--thinking-budget`, `--reasoning-budget`)
  are unverified (§5).
- Prompt in the literal open-weights style the bridges describe: one task, a
  strict output format, an example of the expected output, and "If you find
  nothing, say so explicitly and list what you inspected."

## Routing guidance

**Local-only user (no frontier access, or data that cannot leave the
machine):**
- On a 32 GB+ Mac or a 24 GB GPU, this is the best local generalist and coding
  agent: Q4_K_M, `medium` effort, 64K+ context, through Pi or OpenCode
  (§8). Route `analyze`, `bulk`, `quick-fix` and `investigate` here, with
  every change checked by tests or a script, and review and merge decisions
  kept with a human.
- Expect 10 to 45 tok/s on Apple silicon (third-party). For speed over
  smarts on the same machine, Qwen3.6-35B-A3B (AA 18) runs at 60 to 90 tok/s
  (§8).
- On a 16 GB machine, do not route coding-agent work to it. It fits a 16 GB
  Mac only at 2-bit through llama.cpp, at an estimated 5 to 12 tok/s (the
  digest's estimate, not a measurement) with minutes of prompt processing for
  an agent preamble. Use it there only for overnight or background
  classification, short summaries, JSON extraction and image labelling at
  `none` or `low`, one request at a time. The digest names gpt-oss-20b as the
  offline model that fits a 16 GB Mac (§ Routing shortlist for this setup).
- Never use 1-bit builds. Qwen3-Coder-Next (AA 9, 52 GB in Ollama) is not the
  practical local coder; this model dominates it (§8).

**User with frontier access:**
- At most a cheap private subagent: codebase Q&A, classification, JSON
  extraction, image and long-document reading, and summarising noisy tool
  output ("run cargo test and summarize the result so that the main agent
  doesn't get polluted") (§6;
  [HNCB](https://news.ycombinator.com/item?id=49562575)), on hardware the user
  already has.
- Route there only when the data should stay local or the network is down.
  The digest's verdict: "Neither model earns a row in the routing table
  today"; Haiku 5.5 holds `bulk`, and GPT-6 Luna and DeepSeek V4.1 Flash are
  cheaper hosted tiers (§ Routing shortlist for this setup).
- Do not route here for feature work that must merge, long runs, babysitting,
  orchestration, frontend or copy.

**Hosted alternative:** for open-weights API routing, prefer
**Qwen3.8-Flash-Next** (125B total, 6B active MoE): AA 40 vs 34, $0.37 vs
$1.01 per AA task, $0.15 / $0.47 per MTok, but under the `qwen-community-1.0`
licence rather than Apache 2.0. Use the hosted 27B only when you need Apache
2.0 weights you can later self-host, or a specific cheap provider (§8;
[AA](https://artificialanalysis.ai/models/qwen3-8-flash-next)). It is not
profiled in this kit.

Handoff patterns:
- **Qwen drafts locally, tests decide.** The local model makes the change or
  writes the analysis; a test run or script check accepts it; a frontier model
  or the human reviews before anything merges (§6).
- **Fan out only with concurrency headroom.** Shared-prefix fan-out works on a
  dual-4090 server ("shared prefix prefill is close to free on a cache hit");
  a 16 GB Mac has memory for one slot (§6;
  [HNAA](https://news.ycombinator.com/item?id=49350724)).

## Cost notes

- QwenCloud: $0.50 input, $0.10 implicit cached read ($0.05 explicit read,
  $0.625 explicit write), $3.00 output per MTok; 1M context, 131K max output
  (§4; [QCLOUD](https://www.qwencloud.com/models/qwen3.8-27b)).
- OpenRouter `qwen/qwen3.8-27b`: 20 endpoints, output $0.50 to $3.20 per MTok.
  The Alibaba endpoint is $0.425 / $2.55 with 1M context; the cheapest
  (Tenstorrent, fp4) is $0.02 / $0.50 at 262K; Cerebras (fp16) is $0.99 /
  $1.49 but capped at 65,536 context, too small for agents. A claim of
  "Cerebras at 1500 tokens/s" is unverified (§4;
  [OR](https://openrouter.ai/qwen/qwen3.8-27b)).
- AA cost per task: $1.01 at xhigh, $1.13 medium, $1.05 low, $2.49 with
  reasoning off; lower effort does not cut the hosted bill per task (§2; AA).
- Locally the cost is hardware and wall-clock. Pick `none` or `low` for bulk,
  `medium` for agent loops, and test `xhigh` per task against the clock.

### Local hardware

None of this was measured by this kit. Memory figures are Unsloth's guidance
(total RAM plus VRAM, or unified memory) and the file sizes Quesma tested;
quality is Quesma's independent run; speeds are third-party reports, mostly
anecdotal.

| Quant | Total memory (Unsloth) | File as tested or listed | Terminal-Bench 2.1 / GPQA / IFBench (Quesma, xhigh) |
|---|---|---|---|
| BF16 | 56 GB | 54.7 GB (HF 55.59 GB; Ollama `27b-bf16` 56 GB) | 70.8% / 89.9% / 81.7% |
| 8-bit | 31 GB | Q8_0 29.0 GB (Ollama `27b-q8_0` 30 GB) | not run / 89.8% / 80.3% |
| 6-bit | 23-26 GB | not tested | not tested |
| 4-bit | 16-19 GB | Q4_K_M 17.0 GB (Ollama `qwen3.8:27b` 18 GB; LM Studio 16.10 GB; MLX 16.08 GB) | 70.8% / 90.4% / 81.0% |
| 3-bit | 12-14 GB | UD-Q3_K_XL 13.15 GB; UD-IQ3_XXS 10.93 GB | not measured |
| 2-bit | 9-11 GB | UD-Q2_K_XL 10.7 GB (v2 file; current v3 is 9.83 GB, not benchmarked) | 64.0% / 85.4% / 80.0% |
| 1-bit | 7-8 GB | UD-IQ1_M 6.7 GB; UD-IQ1_S 6.2 GB | not run / 27.3% and 10.4% / not run |

KV cache on top of the weights (the digest's arithmetic from the model card,
only 16 of 64 layers being full attention): about 64 KiB per token at F16, so
2 GiB at 32K, 4 GiB at 64K and 16 GiB at 262K; q8_0 roughly halves that and
q4_0 roughly quarters it. MTP speculative decoding needs 1 to 2 GB more (§4;
UNS, QUESMA).

| Machine | Runtime and quant | Generation | Source |
|---|---|---|---|
| M5 Max 128 GB MacBook Pro; DGX Spark | LM Studio, Q4_K_M 17 GB | 15-30 tok/s | [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/) |
| DGX Spark | `llama serve --spec-type draft-mtp` | about 72% faster than LM Studio's default | SW |
| M4 Pro Mac mini 64 GB | LM Studio | 12.75 tok/s | [HNREL](https://news.ycombinator.com/item?id=49307087) |
| M1 Max | not stated | about 9.5 tok/s; 10-13 with "Reasoning level: low" | [HNREL](https://news.ycombinator.com/item?id=49304287), [HNSW](https://news.ycombinator.com/item?id=49332582) |
| M1 64 GB | oMLX, 4-bit, Pi | 11 tok/s (65 tok/s prompt) | [HNSW](https://news.ycombinator.com/item?id=49344660) |
| M4 MacBook Pro 64 GB | Ollama `qwen3.8:27b-mlx` | about 45 tok/s | [HNREL](https://news.ycombinator.com/item?id=49309753) |
| M5 Pro 48 GB | Ollama | 20 tok/s | [HNREL](https://news.ycombinator.com/item?id=49307615) |
| M4 Max 48 GB | mtplx | 25 tok/s | [HNSW](https://news.ycombinator.com/item?id=49327214) |
| M5 Max | MTPLX | 35-88 tok/s (self-reported by the MTPLX author) | [MTPLX](https://huggingface.co/Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed) |
| RTX 5060 Ti 16 GB | llama.cpp, UD-IQ4_XS, 64K, q4_0 KV | 24.9 tok/s (888 tok/s prompt) | [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html) |
| RTX 5070 Ti 16 GB | UD-Q2_K_XL, 128K, q4 KV | 50-60 tok/s | [HNREL](https://news.ycombinator.com/item?id=49303788) |
| RTX 3060 12 GB (spills to RAM) | Ollama | 2.41 tok/s | [HNREL](https://news.ycombinator.com/item?id=49311381) |
| Hosted (Alibaba API) | AA measurement | 44.4 tok/s, 3.95 s to first token | [AA](https://artificialanalysis.ai/models/qwen3-8-27b) |

What fits: on a **16 GB Mac** only the 2-bit UD-Q2_K_XL fits, through
llama.cpp with the vision projector off and a quantized KV cache, at about
10.9 GiB with 32K to 64K context under macOS's roughly 12 GiB GPU cap; no
Ollama, LM Studio or MLX build fits, and the expected 5 to 12 tok/s is the
digest's estimate, not a measurement (§4). A 16 GB NVIDIA card is different
because the VRAM is all the model's: Paul Brown ran 4-bit UD-IQ4_XS at 64K
context, 24.9 tok/s. On **24 GB**, Unsloth says 4-bit works "on 16-19GB VRAM
like RTX 5080, 4090 or a Mac with 24GB RAM"; a 24 GB GPU holds Q4 with 64K
context, but a 24 GB Mac is tighter, since macOS reserves part of memory from
the GPU (66 to 75% usable on 32 GB machines per a community note; the 24 GB
figure is not found). On **32 GB**, a Mac runs Q4_K_M with 64K or more of
context, the digest's recommended setup for a local coding agent, and MTPLX
starts there. On **64 GB**, Q8_0 (29-31 GB) or Q4 with the full 262K context
fits; Quesma found no quality gain from Q8 over Q4, so the extra memory is
better spent on context or on running the faster Qwen3.6-35B-A3B alongside
(our reading of the digest; not measured).

## Evidence

- `research/open-weights-small.md` (as of 2026-10-19; web research, nothing
  run hands-on): header and "How to read this"; `§ Model 1 §1` (release
  2026-08-14, Apache 2.0, architecture, AA 34 thesis, 16 GB verdict); `§ Model 1
  §2` (self-reported vs Quesma benchmark table, AA table, coding-agent and
  vision evidence); `§ Model 1 §3` (xhigh over-thinking, effort trade-offs,
  speed, quant cliff, context overflow, tooling pitfalls, misconceptions);
  `§ Model 1 §4` (licence, context, memory by quant, KV arithmetic, 16 GB fit
  table, measured speeds, hosted prices); `§ Model 1 §5` (effort, sampling,
  preserve_thinking, context sizing, scoping); `§ Model 1 §6` (subagent roles,
  verification); `§ Model 1 §7` (llama.cpp, Ollama, LM Studio, MLX, vLLM, Pi,
  Qwen Code, Claude Code); `§ Model 1 §8` (routing implications); `§ Model 2
  §3-§4` (AA-LCR 82%, AA-Omniscience hallucination rate 0.303 and Terminal-Bench
  2.1 79.8% for this model, in the gpt-oss comparison); `§ Cross-model
  synthesis` and `§ Routing shortlist for this setup`.
- `research/model-gaps.md § 4e. Qwen3.8-Max (Alibaba)` and its 2026-10-19
  update note (27B shipped; Coder-Next is not the practical local coder;
  prefer Flash-Next hosted; template blanks filled), and `§ Suggested
  routing-table shortlist` (its Local / offline row still lists
  Qwen3-Coder-Next and gpt-oss and predates the update note).
- `core/bridges/ollama.md`, `openrouter-api.md`, `opencode-cli.md`,
  `pi-cli.md` (invocation routes and their effort-flag limits).
- Key URLs: [HF model card](https://huggingface.co/Qwen/Qwen3.8-27B),
  [QwenLM GitHub](https://github.com/QwenLM/Qwen3.8),
  [AA](https://artificialanalysis.ai/models/qwen3-8-27b),
  [Quesma](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/),
  [Simon Willison](https://simonwillison.net/2026/Aug/16/qwen-38-27b/),
  [Simon Willison, addition in words](https://simonwillison.net/2026/Oct/4/qwen38-addition-in-words/),
  [Unsloth](https://unsloth.ai/docs/models/qwen3.8),
  [Ollama](https://ollama.com/library/qwen3.8),
  [QwenCloud](https://www.qwencloud.com/models/qwen3.8-27b),
  [OpenRouter](https://openrouter.ai/qwen/qwen3.8-27b),
  [Paul Brown](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html),
  [Flash-Next on AA](https://artificialanalysis.ai/models/qwen3-8-flash-next).
- **Self-reported:** every vendor benchmark (Terminal-Bench 2.1 73.0, GPQA
  89.2, IFBench 79.5, SWE-bench Pro 61.7, DeepSWE 42.2, OSWorld-Verified 84.3,
  LiveCodeBench v6 90.3, HLE 30.8, OmniDocBench 91.1, CharXiv 83.7) and the
  MTPLX 35-88 tok/s.
- **Unverified (single source or forum):** looping at medium; "Reasoning
  level: low" in the prompt; the "finish up" nudge; "obsessive"; the spam
  benchmark; the Unsloth Q8_K_XL looping report; q4_0 KV cache quality; the
  thinking-budget flag names; Cerebras at 1500 tok/s; every forum speed in the
  table above.
- **Not found:** independent SWE-bench Pro, OSWorld or tool-calling numbers;
  any first-hand run on a 16 GB Apple silicon Mac; Anthropic-API support in
  llama-server; the QwenCloud Anthropic base URL and its effort-level field;
  how Ollama's `--think` levels map to Qwen's; independent quality numbers for
  the v3 Unsloth 2-bit and 3-bit files; the GPU-usable share of a 24 GB Mac;
  any evidence on frontend, copy, 3D, prompt writing or diff review.
- The AA index of 52 reported on 2026-08-17 is from an older index version
  and is not comparable with today's 34
  ([SW52](https://simonwillison.net/2026/Aug/17/qwen-38-27b-scores-52/)).

### Score rationale

| Axis | Score | Why |
|---|---|---|
| intelligence | 3 | AA 34 at xhigh (28 at the kit's medium), below GPT-6 Luna (38, scored 4) and far below Opus 5.5 (54, scored 8); strong for its size (Quesma Terminal-Bench 2.1 70.8%) but scores are frontier-relative. |
| taste | 2 | No design or copy evidence; gold-plates at high effort ("massively over-engineered", an unrequested animated circle). |
| floor | 3 | Over-thinks at the default, looping reported at medium, "obsessive", tooling traps that produce garbage; one 10+ hour unattended success is anecdotal. |
| thoroughness | 4 | Digs long and found real bugs (anecdotal), AA-Omniscience hallucination rate 0.30 and AA-LCR 82%, but no review evidence. |
| cost_efficiency | 3 | Hosted $1.01 per AA task at index 34, "particularly expensive" for its class and 3x Flash-Next, which scores higher; free per token locally, so local users should set a high config cost. |
| speed | 2 | Dense: 9.5-30 tok/s on most Apple silicon reports (45 at best), 44 tok/s hosted with a 3.95 s TTFT, and 17-21 minute answers at xhigh. |
| computer_use | 2 | OSWorld-Verified 84.3 is self-reported only and bounding boxes are good, but no harness evidence and too slow to drive a UI. |
| orchestration | 2 | No evidence of leading agents; subagent context overflowed 64K; not a lead model. |
