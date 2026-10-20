# Small open-weights models: Qwen3.8-27B and gpt-oss-20b

**As of 2026-10-19.** Web research done on that date; nothing here was run hands-on. Research note on two open-weights models small enough to run on one machine, written for the same purpose as `research/claude-releases.md`: the conclusions, numbers and decision rules this kit uses, not a general review. Unlike the other digests, the sources are written posts, model cards and benchmark pages rather than videos, so citations are `[KEY](url)` with no timestamps. Saved copies of every source live in the private companion repo under `agent-orchestration-sources/articles/qwen/` and `articles/gpt-oss/`, with a header giving title, author, URL, publication date and fetch date, following the same rule as the video transcripts: cite the public page here, keep the copy private.

The reference machine for the "does it fit" questions is a common entry-level setup: a MacBook Pro with an Apple M2 Pro and 16 GB of unified memory, running Ollama. Other machines scale from it by memory and bandwidth (the generator does this from `hardware` in config.yaml). Figures that depend on that machine are marked as such.

## How to read this

- **Vendor benchmark numbers are self-reported.** An independent number (Artificial Analysis, "AA", or a practitioner's measured run) is given next to each one where it exists.
- **"unverified"** means a single non-primary source, or sources that disagree. **"not found"** means no source answered the question. Neither should be hard-coded into routing logic.
- **"our arithmetic" and "our estimate"** mark numbers derived in this digest (memory budgets, token throughput ceilings). They are reasoning from published specs, not measurements.
- **Forum reports** (Hacker News, r/LocalLLaMA) are first-hand but anecdotal; they are cited for hardware speeds and failure modes, never for capability rankings.
- **Simon Willison** is the main practitioner voice here, the role Theo plays in the video digests. He runs models locally on Apple silicon and a DGX Spark and drives them through the Pi coding agent and his `llm` CLI, so his notes transfer directly to this kit's setup.
- **Baseline for routing advice:** the same as `research/model-gaps.md`: Claude Opus 5.5 at AA 54 and about $1.82 per AA task, Claude Haiku 5.5 as the cheap Anthropic subagent (`research/claude-releases.md` Video 4), GPT-6 Luna at AA 38 and about $0.07 per task as the cheapest hosted tier worth routing to.
- **What changed in `research/model-gaps.md`:** this digest resolves two open items there. §4e said the Qwen3.8-27B release status "conflicts between sources" and called Qwen3-Coder-Next the practical local coding model; §4f said there was no new gpt-oss generation. Dated update notes point from those sections to this file.

---

# Model 1: Qwen3.8-27B (dense, Alibaba Qwen team)

Saved copies of every source are under `agent-orchestration-sources/articles/qwen/`. The reading notes at the top of this file apply.

**Name check.** There is one model: `Qwen/Qwen3.8-27B`, a single hybrid-thinking checkpoint (thinking on by default, can be switched off per request). There are no separate -Instruct or -Thinking repos, and no Qwen4 27B weights on Hugging Face as of the fetch date (our search of the `Qwen` org via the HF API, 2026-10-19) [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). Its predecessor `Qwen/Qwen3.6-27B` (April 2026) is a different model [QWGH](https://github.com/QwenLM/Qwen3.8). The name is not ambiguous.

## 1. Subject and overall thesis

- **Release status (resolves model-gaps.md §4e): it shipped on 2026-08-14.**
  - QwenLM GitHub news: "2026-08-14: Qwen3.8-27B is now available on Hugging Face Hub and ModelScope" [QWGH](https://github.com/QwenLM/Qwen3.8).
  - The Hugging Face repo went public at 15:00 UTC on 2026-08-14. The HF API gives `lastModified` 2026-08-14T15:00:01Z, and the HN release thread (linking `Qwen/Qwen3.8-27B-FP8`) was posted at 15:00 UTC [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B) [HNREL](https://news.ycombinator.com/item?id=49299605). Artificial Analysis also gives "August 14, 2026" [AA](https://artificialanalysis.ai/models/qwen3-8-27b). Simon Willison called it "Friday's big release"; 2026-08-14 was a Friday [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - The earlier conflict came from timing. The 2.4T-A95B flagship weights landed on 2026-08-12 [QWGH](https://github.com/QwenLM/Qwen3.8), and the 27B followed two days later. Sources written in between reported it as delayed.
  - **Official HF repo IDs:** `Qwen/Qwen3.8-27B` (BF16 safetensors, 55.59 GB, 27,781,427,952 parameters, not gated) and `Qwen/Qwen3.8-27B-FP8` [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B) [HNREL](https://news.ycombinator.com/item?id=49299605).
  - **Licence: Apache 2.0.** The card front matter says `license: apache-2.0` and the repo ships an Apache 2.0 `LICENSE` file [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). This differs from Qwen3.8-Flash-Next (`qwen-community-1.0`) [FNCARD](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) and from the 2.4T flagship's custom licence (model-gaps §4e).
- **What it is:** a dense 27B "Causal Language Model with Vision Encoder". It has 64 layers in a hybrid layout, `16 × (3 × (Gated DeltaNet → FFN) → 1 × (Gated Attention → FFN))`, MTP heads, and a context of "262,144 natively and extensible up to 1,000,000 tokens" [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). It takes text, image and video input and outputs text [AA](https://artificialanalysis.ai/models/qwen3-8-27b).
- **Thesis from practitioners:** a very capable local generalist, held back by speed and verbosity.
  - Simon Willison: "The fact that a 17GB file can do all of this stuff on my home machines is a **miracle**." The catch: "The only thing holding this back from being a daily driver is performance... dense (non-Mixture-of-Experts) models... require a whole lot of memory bandwidth" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - His headline warning about the default: "This is a **hilarious** default. It's absolutely not a good way to run the model, especially on consumer hardware" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - Independent ranking: AA Intelligence Index **34** at the default xhigh, #1 of 141 open-weights models in AA's 4B-40B "Small" class. AA also says it is "particularly expensive when comparing to other open weight models of similar size" [AA](https://artificialanalysis.ai/models/qwen3-8-27b).
- **Verdict for this user (MacBook Pro M2 Pro, 16 GB):** it fits only at 2-3 bit, with 16K to 64K context, and only through llama.cpp. No official Ollama, LM Studio or MLX build fits (section 4). Locally it suits slow background jobs, not an interactive coding agent. For real work, call it hosted, or use the hosted MoE sibling Qwen3.8-Flash-Next, which scores higher on AA for about a third of the cost per task (section 8).

## 2. Strengths (with evidence)

- **Benchmarks: Qwen's self-reported numbers, with independent runs next to them where they exist.**

  | Benchmark | Qwen3.8-27B (self-reported) | Independent result | Qwen3.6-27B (self-reported) |
  |---|---|---|---|
  | Terminal-Bench 2.1 (Terminus) | 73.0 | Quesma: BF16 63/89 = **70.8%** (95% CI 61-79); Q4_K_M 70.8%; UD-Q2_K_XL 64.0% (xhigh, 3 h timeout) [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/) | 63.4 |
  | GPQA Diamond | 89.2 | Quesma: BF16 **89.9%** at xhigh; Q4_K_M 90.4%; UD-Q2_K_XL 85.4% [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/) | 87.8 |
  | IFBench | 79.5 | Quesma: BF16 **81.7%** strict at xhigh; UD-Q2_K_XL 80.0% [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/) | 69.1 |
  | SWE-bench Pro (Claude Code harness) | 61.7 | not found | 53.5 |
  | DeepSWE 1.1 | 42.2 | not found | 13.3 |
  | OSWorld-Verified | 84.3 | not found | 63.9 |
  | LiveCodeBench v6 | 90.3 | not found | 83.9 |
  | HLE | 30.8 | not found | 24.0 |

  Self-reported figures are from [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). Piotr Migdał: "First and foremost, I was happy I replicated the official results" (GPQA), and on Terminal-Bench "my measurement of BF16 replicate[s] the stated result" [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/).
- **Artificial Analysis (independent, Intelligence Index v4.3.2):**

  | Model | AA Index | Output tokens to run index | Cost per AA task (hosted) | Hosted output speed |
  |---|---|---|---|---|
  | Qwen3.8-27B xhigh (default) | 34 | 200M | $1.01 | 44.4 tok/s |
  | Qwen3.8-27B medium | 28 | 110M | $1.13 | 43.5 tok/s |
  | Qwen3.8-27B low | 26 | 82M | $1.05 | 43.9 tok/s |
  | Qwen3.8-27B non-reasoning | 20 | 43M | $2.49 | 43.6 tok/s |
  | Qwen3.8-Flash-Next (125B, 6B active, MoE) | 40 | 240M | $0.37 | 52.4 tok/s |
  | Qwen3.6-27B (predecessor) | 21 | 160M | $0.62 | 56.4 tok/s |
  | Qwen3.6-35B-A3B (MoE) | 18 | 160M | $0.48 | 134.4 tok/s |
  | Qwen3-Coder-Next (80B, 3B active, MoE) | 9 | 34M | $0.47 | 93.7 tok/s |
  | gpt-oss-20b (high) | 9 | 70M | $0.01 | 258.0 tok/s |

  All rows are from [AA](https://artificialanalysis.ai/models/qwen3-8-27b) and its sibling pages (copies in the same saved file). Hosted speed is measured on Alibaba's API, not on local hardware. On 2026-08-17 the then-current index showed **52**, "the same score as GPT-5.6 Luna (max)" [SW52](https://simonwillison.net/2026/Aug/17/qwen-38-27b-scores-52/). That figure is from an older index version and cannot be compared with today's 34.
- **Drives a coding agent.** Simon: "Yes, it can drive coding agents... My initial experiments with Pi have been very promising." On `how does auth work?` in the Datasette repo, "After a sequence of reasoning and tool calls that accessed a bunch of different files it produced this reply, which is very solid." It then "built and tested" a JSONL-to-Markdown converter "which did exactly what I needed" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - Long unattended debugging (anecdotal): on an M4 MacBook Pro (48 GB) with llama.cpp and Pi, "After about 10+ hours of digging, it has apparently found a bug in the Next.js framework, with an example app that replicates the bug" [HNSW](https://news.ycombinator.com/item?id=49328527).
  - One-shot app work (anecdotal): "It one-shotted the Web app, had no bug. The Rust rewrite only had one bug"; "Perfectly usable for local coding through OpenCode" on an M5 Max at 15-30 tok/s [HNREL](https://news.ycombinator.com/item?id=49308246).
  - With GitHub MCP tools wired in, "it found a real bug in one of my repos" [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html).
- **Vision and structured output.** Bounding boxes: asked to "Return JSON bounding boxes for the pelicans in this photo, 0-1000 scale", it returned `bbox_2d` JSON that is "**such a good match**" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). Qwen self-reports OmniDocBench 1.5 at 91.1 and CharXiv (RQ) at 83.7 without a code interpreter; no independent numbers were found [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B).
- **Classification.** "near-perfect score on my E-mail spam filtering benchmark, best of any model I tested, ever. But it is slow" [HNREL](https://news.ycombinator.com/item?id=49301283) (unverified, single private benchmark). Other practitioners list "categorization, information retrieval, semantic search, image description" as small-model uses [HNREL](https://news.ycombinator.com/item?id=49304989).
- **Quantization-robust down to 4-bit.** "if you go with a 4-bit quantization Q4_K_M (17GB), you won't notice a difference on these benchmarks". IFBench shows "no change between models, down to a decent 2-bit one, weighing less than 11 GB" [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/).
- **Exactness with reasoning on.** Writing sums in words, at medium reasoning it "got the right answer in 167 out of 169 attempts", against 23.57% with reasoning disabled [SWADD](https://simonwillison.net/2026/Oct/4/qwen38-addition-in-words/).
- **Licence and harness support:** Apache 2.0 [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). There are day-zero GGUF and NVFP4 builds; Unsloth says its quants add "Developer Role Support for agentic tools like Codex" and better tool-call parsing of nested objects [UNS](https://unsloth.ai/docs/models/qwen3.8). Ollama's library entry is tagged vision, tools and thinking [OLL](https://ollama.com/library/qwen3.8).

## 3. Weaknesses, pitfalls and misconceptions

- **The default `xhigh` effort over-thinks badly.**
  - Simon's pelican "took **21 minutes** to generate, using 22,276 reasoning tokens to produce 3,223 tokens of output... Was that worth waiting 21 minutes for? Absolutely not." For `draw an svg of a circle` it produced "this **absolutely beautiful** animated circle, which was entirely not what I had asked for!" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - On an M4 Pro Mac mini, "svg owl" took 17m12s at 12.75 tok/s and 21,769 tokens. Qwen3.6-35B-A3B on the same prompt "thought for 1.59 seconds... and hit 80.83 tok/s" [HNREL](https://news.ycombinator.com/item?id=49307087).
  - At xhigh "it will burn through 2K tokens before it has even finished its bullet point overview" [HNSW](https://news.ycombinator.com/item?id=49325856).
  - AA counts 200M output tokens to run its index, ranking verbosity 25th of 27 [AA](https://artificialanalysis.ai/models/qwen3-8-27b).
  - It also gold-plates: it built an unrequested "demo scene" and drew its own pelicans in a bounding-box tool, "**massively over-engineered**" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
- **Lower effort trades quality, and not always in your favour.**
  - Qwen's own warning: "In multi-turn agentic tasks, lower reasoning effort does not always reduce overall task completion time... it can also lead to insufficient analysis, more failures, and repeated retries" [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B).
  - IFBench (BF16, strict) falls from 81.7% at xhigh to 65.3% at medium and 60.5% at low. GPQA falls from 89.9% to 83.3% and 86.4% [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/). AA: 34 at xhigh, 28 medium, 26 low, 20 non-reasoning [AA](https://artificialanalysis.ai/models/qwen3-8-27b-low).
  - With no reasoning, numeric accuracy is 23.57%, dropping to 6.44% for 10-13 digit operands [SWADD](https://simonwillison.net/2026/Oct/4/qwen38-addition-in-words/). Simon's no-reasoning bounding-box tool "nearly works but shows the boxes in the wrong place" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - Looping: at medium "it gets caught up in the very typical Qwen looping. Not seen looping in the 'low' reasoning effort mode" [HNSW](https://news.ycombinator.com/item?id=49325856) (unverified).
- **Slow, because it is dense.** Simon got "around 15-30 tokens a second from LM Studio" on an M5 Max and a DGX Spark [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). On an M1 Max, "well up into the 60s t/s with the A3B, stuck at 9.5 or so with this new 27B" [HNREL](https://news.ycombinator.com/item?id=49304287). Hosted on Alibaba's API it runs at 44.4 tok/s with a 3.95 s TTFT, against a class median of 79.8 tok/s and 1.12 s [AA](https://artificialanalysis.ai/models/qwen3-8-27b).
- **Spilling out of GPU memory collapses throughput.** "A dense model has to fit entirely in VRAM, since every weight is read for every token" [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html). Example: an RTX 3060 12 GB under Ollama ran at 2.41 tok/s, 8m18s for one answer [HNREL](https://news.ycombinator.com/item?id=49311381).
- **The quantization cliff is at 1-bit, and 2-bit costs some agentic skill.** UD-IQ1_S (6.2 GB) scores 10.4-16.9% on GPQA, around chance, with up to 64% empty answers; "longer reasoning makes it worse". UD-Q2_K_XL drops Terminal-Bench from 70.8% to 64.0% and writes 1.27x more tokens on the same solved tasks [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/).
- **Agent context fills fast.** With 64K served, "64K runs out in agent sessions": "request (71461 tokens) exceeds the available context size (65536 tokens)" [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html). In opencode, a subagent's "compacted context plus prompts and such was over the window and it errored out" [HNCB](https://news.ycombinator.com/item?id=49591719). Agent tools, MCP, skills and system prompt "take between 5k and 25k tokens" before the user prompt [HNCB](https://news.ycombinator.com/item?id=49562188).
- **Tooling pitfalls (all llama.cpp or GGUF):**
  - llama.cpp builds before 2026-08-16 do not work for this model [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/). Paul Brown needs b10450 or later: "Older builds load the model and then produce fluent garbage on CUDA" [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html).
  - `--reasoning-effort none` fails with "Jinja Exception: Unexpected reasoning effort none". Use `--reasoning off` for the whole server, or `"reasoning_effort": "none"` in a single request body [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html). Unsloth lists `none` as a level [UNS](https://unsloth.ai/docs/models/qwen3.8), which is the trap.
  - One user found Unsloth's Q8_K_XL "looping and going crazy on the think part" while bartowski's Q8_0 did not [HNREL](https://news.ycombinator.com/item?id=49304627) (unverified). Unsloth replaced its GGUFs with "Dynamic V3.0" builds on 2026-08-19 [UNS](https://unsloth.ai/docs/models/qwen3.8), so re-download older files.
  - LM Studio's default context of 8,192 tokens is too small: "Qwen was using them all up thinking about even the most mundane of problems" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). Ollama defaults to 4K context below 24 GiB of VRAM [OLL](https://docs.ollama.com/context-length).
- **Misconceptions:**
  - *"LM Studio says 16 GB is enough."* Its page says "To run the smallest Qwen3.8, you need at least 16 GB of RAM", and its smallest build is 16.10 GB [LMS](https://lmstudio.ai/models/qwen3.8). That is the file size, not a working setup on a 16 GB Mac (section 4).
  - *"There is a Qwen3.8 30B-A3B or 35B-A3B MoE."* None was found. Users at launch were still asking for one ("I hope really badly that we'll get a new 35B A3B") [HNREL](https://news.ycombinator.com/item?id=49299815). The only Qwen3.8 MoE besides the 2.4T flagship is Qwen3.8-Flash-Next, 125B with 6B active (180B counting its 51B n-gram embedding and 4B MTP head, which is the figure Artificial Analysis shows) [FNCARD](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) [SWFN](https://simonwillison.net/2026/Aug/26/qwen38-flash-next/).
  - *"Hosted, it is a cheap worker."* At $1.01 per AA task it costs about 100x gpt-oss-20b ($0.01) and almost 3x Qwen3.8-Flash-Next ($0.37, which scores higher) [AA](https://artificialanalysis.ai/models/qwen3-8-27b).
  - *"A smart model needs no verification."* It "will do insane/unusual things to get to the solution", "similarly obsessive" to GPT-5.6-Sol-max [HNAA](https://news.ycombinator.com/item?id=49336610) (unverified, single forum report).

## 4. Pricing, speed, context and limits

- **Licence:** Apache 2.0 [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B).
- **Context:** 262,144 native, extensible to 1,000,000 with YaRN. Qwen notes that static YaRN is "potentially impacting performance on shorter texts", so enable it only when needed [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). The hosted API offers 1M context and a 131K max output [QCLOUD](https://www.qwencloud.com/models/qwen3.8-27b). Recommended output budgets are 262,144 tokens for reasoning and 131,072 for the final answer [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B); neither is realistic locally.
- **Memory (Unsloth guidance, "total memory: RAM + VRAM, or unified memory"):** 1-bit 7-8 GB, 2-bit 9-11 GB, 3-bit 12-14 GB, 4-bit 16-19 GB, 6-bit 23-26 GB, 8-bit 31 GB, BF16 56 GB. "4-bit quants work on 16-19GB VRAM like RTX 5080, 4090 or a Mac with 24GB RAM". MTP needs "1-2GB extra headroom" [UNS](https://unsloth.ai/docs/models/qwen3.8).
- **Quality by quant (Quesma, independent; GGUF sizes as tested):**

  | Quant | File | Same top-1 token as BF16 | Terminal-Bench 2.1 | GPQA (xhigh) | IFBench (xhigh) |
  |---|---|---|---|---|---|
  | BF16 | 54.7 GB | 100% | 70.8% | 89.9% | 81.7% |
  | Q8_0 | 29.0 GB | 98.7% | not run | 89.8% | 80.3% |
  | Q4_K_M | 17.0 GB | 94.8% | 70.8% | 90.4% | 81.0% |
  | UD-Q2_K_XL (v2 file) | 10.7 GB | 87.3% | 64.0% | 85.4% | 80.0% |
  | UD-IQ1_M | 6.7 GB | 77.6% | not run | 27.3% | not run |
  | UD-IQ1_S | 6.2 GB | 74.2% | not run | 10.4% | not run |

  Source: [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/). The 2-bit row used Unsloth's v2 file. The current v3 `UD-Q2_K_XL` is 9.83 GB and has not been benchmarked independently (not found).
- **KV cache (our arithmetic from the model card):** only 16 of 64 layers are full attention, with 4 KV heads × 256 dims [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B).
  - Per token at F16: 16 layers × 4 heads × 256 dims × 2 (K, V) × 2 bytes = **64 KiB**.
  - That gives 0.5 GiB at 8K, 1 GiB at 16K, 2 GiB at 32K, 4 GiB at 64K and 16 GiB at 262K. q8_0 roughly halves these and q4_0 roughly quarters them.
  - The Gated DeltaNet state is fixed size: 48 layers × 48 heads × 128 × 128 × 4 bytes ≈ 0.14 GiB.
  - Quesma's "around 2.3 GB per 32k tokens" at F16 matches [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/). So does Paul Brown's 64K at q4_0 on a 16 GB GPU: "15769 MiB of the card's 16311 MiB" with a 13.27 GB (GiB) UD-IQ4_XS [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html).
- **Does it fit on the reference MacBook Pro (M2 Pro, 16 GB)?**
  - **Budget:** 16 GiB physical. macOS caps GPU-wired memory at a default of about 75% of RAM. The community note's table gives "~21-24 GB" on a 32 GB machine, i.e. 66-75% [DEVNOTE](https://github.com/ivanopcode/devnote-override-macos-metal-vram-cap). On 16 GB that extrapolates to roughly **10.7 to 12 GiB** usable by Metal (our extrapolation; Apple does not document it). A measured figure agrees: an M2 16 GB Mac mini reports a Metal `recommendedMaxWorkingSetSize` of 12,713 MB, about 11.8 GiB [LCPP-20704](https://github.com/ggml-org/llama.cpp/issues/20704) (saved under `articles/gpt-oss/`; see Model 2 §4). The note advises leaving "8-16 GB" for macOS, which a 16 GB Mac cannot do. Overheads used below: DeltaNet state 0.14 GiB plus about 0.5 GiB of compute buffers (our estimate). File sizes are converted from Unsloth's GB to GiB.

  | Build | Weights | + KV + overhead | Total | Fits under ~12 GiB GPU cap? |
  |---|---|---|---|---|
  | BF16 (55.59 GB) | 51.8 GiB | n/a | > 52 GiB | No |
  | Q8_0 (29.05 GB) | 27.1 GiB | n/a | > 27 GiB | No |
  | Ollama `qwen3.8:27b` (18GB listed) [OLL](https://ollama.com/library/qwen3.8) | about 16.8 GiB | n/a | > 16 GiB | No: larger than all of RAM |
  | MLX `mlx-community/Qwen3.8-27B-4bit` (16.08 GB) | 15.0 GiB | 8K q8: +0.9 | about 15.9 GiB | No |
  | UD-Q4_K_M (16.46 GB) | 15.3 GiB | 8K q8: +0.9 | about 16.2 GiB | No |
  | UD-IQ4_XS (14.25 GB) | 13.3 GiB | 8K q8: +0.9 | about 14.2 GiB | No: would need the cap raised to about 14.5 GiB, leaving about 1.5 GiB for macOS |
  | UD-Q3_K_XL (13.15 GB) | 12.25 GiB | 8K q8: +0.9 | about 13.2 GiB | No under the default cap; marginal even if raised |
  | UD-IQ3_XXS (10.93 GB) | 10.2 GiB | 16K q8: +1.2 | about 11.4 GiB | Borderline yes, about 4.6 GiB left for macOS; quality not measured |
  | **UD-Q2_K_XL (9.83 GB)** | **9.15 GiB** | **32K q8: +1.7, or 64K q4_0: +1.8** | **about 10.9 GiB** | **Yes**: the best measured option (Terminal-Bench 64.0% on the v2 file) |
  | UD-IQ1_S (6.19 GB) | 5.8 GiB | 64K: +2-4 | about 8-10 GiB | Yes, but useless (GPQA about 10%) |

  File sizes are from the `unsloth/Qwen3.8-27B-GGUF` file listing and [UNS](https://unsloth.ai/docs/models/qwen3.8); quality is from [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/).
  - **Answer:** yes, but only at 2-bit, or borderline at the smallest 3-bit, with 16K to 64K context. Run it through llama.cpp with the vision projector off, flash attention on, and a quantized KV cache. Close other apps. KV cache at q4_0 is untested on quality; Paul Brown says "Qwen tolerates it well" [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html) (unverified).
  - **Not via Ollama's library:** its smallest tag is 18GB [OLL](https://ollama.com/library/qwen3.8).
  - **Not via LM Studio or MLX official builds:** the smallest are 16.10 GB [LMS](https://lmstudio.ai/models/qwen3.8) and 16.08 GB (mlx-community 4-bit).
  - **MTPLX:** requires "32 GB of unified memory or more". For 16 GB it points to "Prism ML's ternary Qwen 3.8 27B" (Bonsai 2 27B), with an 11.4 GB peak on an M5 Max [MTPLX](https://huggingface.co/Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed). That is a third-party derivative with no independent quality numbers (unverified).
  - **Expected speed on the reference Mac (our estimate, not measured):**
    - The M2 Pro has "200GB/s of unified memory bandwidth" [APPLE](https://www.apple.com/newsroom/2023/01/apple-unveils-m2-pro-and-m2-max-next-generation-chips-for-next-level-workflows/). Each generated token reads all of the weights, so the ceiling at 9.83 GB is 200 ÷ 9.83 ≈ 20 tok/s.
    - Real runs land well below that ceiling. We assume 25-60% of it, which is an assumption, not a measurement. The one nearby data point: a plain M2 Mac mini (16 GB; the M2 has half the M2 Pro's bandwidth, i.e. 100 GB/s [APPLE](https://www.apple.com/newsroom/2023/01/apple-unveils-m2-pro-and-m2-max-next-generation-chips-for-next-level-workflows/)) ran the predecessor Qwen3.6-27B at 1-bit at "like 3-5tok/s" [HNREL](https://news.ycombinator.com/item?id=49304224).
    - Expect about **5-12 tok/s** generation (our estimate). Prompt processing on Apple silicon was about 65 tok/s on an M1 with 64 GB [HNSW](https://news.ycombinator.com/item?id=49344660), so a 20K-token agent preamble could take several minutes before the first output token.
    - No first-hand Qwen3.8-27B report from a 16 GB Apple silicon Mac was found.
- **Measured speeds elsewhere (anecdotal unless marked):**

  | Hardware | Setup | Generation | Source |
  |---|---|---|---|
  | M5 Max 128 GB MBP; DGX Spark | LM Studio Q4_K_M 17GB | 15-30 tok/s | [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/) |
  | DGX Spark | `llama serve` with `--spec-type draft-mtp` | about 72% faster than LM Studio default | [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/) |
  | M4 Pro Mac mini 64 GB | LM Studio | 12.75 tok/s | [HNREL](https://news.ycombinator.com/item?id=49307087) |
  | M1 Max | not stated | about 9.5 tok/s; 10-13 at "Reasoning level: low" | [HNREL](https://news.ycombinator.com/item?id=49304287) [HNSW](https://news.ycombinator.com/item?id=49332582) |
  | M1 64 GB | 4-bit, oMLX, Pi | 11 tok/s (65 tok/s prompt) | [HNSW](https://news.ycombinator.com/item?id=49344660) |
  | M4 MBP 64 GB | Ollama `qwen3.8:27b-mlx` | about 45 tok/s | [HNREL](https://news.ycombinator.com/item?id=49309753) |
  | M5 Pro 48 GB | Ollama | 20 tok/s | [HNREL](https://news.ycombinator.com/item?id=49307615) |
  | M4 Max 48 GB | mtplx | 25 tok/s | [HNSW](https://news.ycombinator.com/item?id=49327214) |
  | M5 Max | MTPLX (vendor) | 35-88 tok/s, self-reported | [MTPLX](https://huggingface.co/Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed) |
  | RTX 5060 Ti 16 GB | UD-IQ4_XS, 64K, q4_0 KV | 24.9 tok/s (888 tok/s prompt) | [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html) |
  | RTX 5070 Ti 16 GB | UD-Q2_K_XL, 128K, q4 KV | 50-60 tok/s | [HNREL](https://news.ycombinator.com/item?id=49303788) |
  | RTX 3060 12 GB (spills to RAM) | Ollama | 2.41 tok/s | [HNREL](https://news.ycombinator.com/item?id=49311381) |

- **Hosted prices (USD per million tokens):**

  | Route | Input | Cached input | Output | Context | Max output |
  |---|---|---|---|---|---|
  | QwenCloud `qwen3.8-27b` (official) | 0.50 | 0.10 implicit; 0.05 explicit read; 0.625 explicit write | 3.00 | 1M | 131K |
  | OpenRouter `qwen/qwen3.8-27b`, Alibaba endpoint | 0.425 | n/a | 2.55 | 1,000,000 | 131,072 |
  | OpenRouter, cheapest listed (Tenstorrent, fp4) | 0.02 | n/a | 0.50 | 262,144 | 65,536 |
  | OpenRouter, Cerebras (fp16) | 0.99 | n/a | 1.49 | 65,536 | 32,768 |

  Sources: [QCLOUD](https://www.qwencloud.com/models/qwen3.8-27b) and [OR](https://openrouter.ai/qwen/qwen3.8-27b). OpenRouter lists 20 endpoints; output prices run from $0.50 to $3.20. Prices change often. The model card still says the hosted version "is coming soon" [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B), but the QwenCloud page shows prices and a "Call API" button [QCLOUD](https://www.qwencloud.com/models/qwen3.8-27b). An HN story claimed "Cerebras at 1500 tokens/s" [HNCB](https://news.ycombinator.com/item?id=49554520) (unverified), but that endpoint is capped at 64K context [OR](https://openrouter.ai/qwen/qwen3.8-27b).

## 5. Recommended prompting style and workflow

- **Set the effort explicitly; never leave it at the default.** Simon: "My strong recommendation: ignore that default. Run Qwen 3.8 27B on low or even no reasoning levels at first" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). Supported levels are `xhigh` (default), `medium` and `low`, plus thinking off [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B).
  - Use **low or off** for classification, extraction, short summaries and bounding boxes.
  - Use **medium** for exact multi-step answers; it got 167/169 sums right against 23.57% with reasoning off [SWADD](https://simonwillison.net/2026/Oct/4/qwen38-addition-in-words/).
  - Use **xhigh** only for instruction-heavy or hard one-shot work where you can wait. IFBench is 81.7% at xhigh against 60-65% at low or medium [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/).
  - In agent loops, heed Qwen's warning that lower effort can mean "more failures, and repeated retries" [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B).
- **In-prompt control works (unverified):** "you can set reasoning level in the prompt... it is actually really pretty solid at 'Reasoning level: low'" [HNSW](https://news.ycombinator.com/item?id=49332582).
- **Sampling (official):**

  | Mode | temperature | top_p | top_k | min_p | presence_penalty | repetition_penalty |
  |---|---|---|---|---|---|---|
  | Thinking | 1.0 | 0.95 | 20 | 0.0 | 0.0 | 1.0 |
  | Non-thinking | 0.7 | 0.80 | 20 | 0.0 | 1.5 | 1.0 |

  Source: [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). The card says presence_penalty can go from 0 to 2 "to reduce endless repetition", but "a higher value may occasionally result in language mixing" [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B).
- **Preserved thinking** is on by default. It "retains thinking blocks from all historical messages" and "improves KV cache utilization"; turn it off with `preserve_thinking: false` [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B). Unsloth: it "increases the number of tokens you use, but could increase accuracy in continued conversations" [UNS](https://unsloth.ai/docs/models/qwen3.8). Keep it on for agent loops, and off for one-shot batch jobs on a small context.
- **Size the context window before anything else.** Load at least 32K. Simon's problem "went away" at 262,144 [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). Ollama and OpenCode want "64k or higher" for agents [OLL](https://docs.ollama.com/integrations/opencode).
- **Scope the request tightly.** At high effort it adds features nobody asked for (section 3). State the output format and say "no extras". Nudge it to finish: "if you even nudge it and say, 'Hey, finish up,' or 'Review the syntax,' boom, it's done" [HNREL](https://news.ycombinator.com/item?id=49307615) (unverified).
- **Vision prompts:** ask for JSON `bbox_2d` on a 0-1000 scale [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
- **Hand arithmetic and exact facts to tools.** Without reasoning, multi-digit arithmetic fails (section 3). One user says it "scores high in AA non-hallucination, so it knows what it doesn't know -- perfect for situations where it can just tool call a web search" [HNAA](https://news.ycombinator.com/item?id=49335776) (unverified).
- **Thinking budgets in llama.cpp:** one user caps runaway thinking with a budget plus a redirect message ("--thinking-budget and --thinking-message") [HNSW](https://news.ycombinator.com/item?id=49325652). The flag names are unverified; another user's config uses `--reasoning-budget -1` [HNREL](https://news.ycombinator.com/item?id=49303788).

## 6. Subagents, orchestration, delegation and verification

- **Good subagent roles (hosted, or local on a 32 GB+ machine):**
  - Codebase Q&A and exploration with tool calls (Simon's "how does auth work?") [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - Classification and triage [HNREL](https://news.ycombinator.com/item?id=49301283).
  - Image and document reading with structured JSON out [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
  - Summarizing noisy output, e.g. "run cargo test and summarize the result so that the main agent doesn't get polluted" [HNCB](https://news.ycombinator.com/item?id=49562575).
  - Long-context reading within 262K.
- **Practitioner view on subagents:** "Small local models can also be used for sub-agent tasks in most agent harnesses. But I'd probably run a larger MoE for that; they're faster and have broader knowledge. The dense models, even very small ones, are not blazing fast" [HNREL](https://news.ycombinator.com/item?id=49304989).
- **Keep subagent prompts lean.** Simon chose Pi "because it has a shorter system prompt than most other options, making it a better fit for trying out smaller models" [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). In opencode, subagent context overflowed a 64K window [HNCB](https://news.ycombinator.com/item?id=49591719).
- **Fan-out works only with concurrency headroom.** On a dual-4090 server: "fan out multiple concurrent branches that share non trivial amount of prefix then reduce their output/summary back into main agent... shared prefix prefill is close to free on a cache hit" [HNAA](https://news.ycombinator.com/item?id=49350724). Quesma ran 8 parallel streams at 17-33 tok/s each on datacenter GPUs [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/). A 16 GB Mac has memory for one slot at modest context, so there is no fan-out there.
- **Verify its output.** It is "obsessive" and "will do insane/unusual things to get to the solution" [HNAA](https://news.ycombinator.com/item?id=49336610) (unverified). It shipped a working tool only with reasoning on [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). Pair it with tests or a script check. Keep review and merge decisions with a frontier model, as the model-gaps routing already does for open models.
- **Watch the clock on long jobs.** At xhigh a single answer can take 17-21 minutes on fast Macs (section 3). Set request timeouts and thinking caps, and do not leave it waiting on rate-limited external APIs. Qwen Code's local-model example sets `timeout` 300000 and `streamIdleTimeoutMs` 600000 for slow servers [QCODE](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/).
- **Delegation from Claude or GPT orchestrators:** no first-hand report of Claude Code or Codex delegating subagents to Qwen3.8-27B was found. Qwen's own coding benchmarks were run "with the Claude Code harness" [HFCARD](https://huggingface.co/Qwen/Qwen3.8-27B), which suggests it handles Claude Code's tool schema (self-reported).

## 7. Harness specifics

Commands below are copied from the cited source. Where we combined flags from several sources, we say so; those combinations are untested.

- **llama.cpp (the only practical route on the 16 GB Mac):**
  - Build: clone `ggml-org/llama.cpp` and build with CMake. "For Apple Mac / Metal devices, set `-DGGML_CUDA=OFF`... Metal support is on by default" [UNS](https://unsloth.ai/docs/models/qwen3.8). You need a build from 2026-08-16 or later [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/).
  - Download: `hf download unsloth/Qwen3.8-27B-GGUF --local-dir unsloth/Qwen3.8-27B-GGUF --include "*UD-Q4_K_XL*"`. For a 16 GB Mac, change the pattern to `"*UD-Q2_K_XL*"` [UNS](https://unsloth.ai/docs/models/qwen3.8).
  - Server for a 16 GB Mac, composed from flags in the cited sources (untested):
    ```
    llama-server -hf unsloth/Qwen3.8-27B-GGUF:UD-Q2_K_XL \
      --ctx-size 32768 -fa on --cache-type-k q8_0 --cache-type-v q8_0 \
      --no-mmproj --jinja --parallel 1 \
      --reasoning off --temp 0.7 --top-p 0.8 --top-k 20 --min-p 0 --presence-penalty 1.5 \
      --port 8080
    ```
    Flag sources: `-hf`, `--no-mmproj`, `--ctx-size` and `--cache-type-*` [HNAA](https://news.ycombinator.com/item?id=49339498); `-fa on` [HNREL](https://news.ycombinator.com/item?id=49304627); `--reasoning off` and the jinja template [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html); `--presence-penalty` [HNREL](https://news.ycombinator.com/item?id=49303788).
    - For reasoning, replace `--reasoning off` with `--chat-template-kwargs '{"reasoning_effort":"low"}'` (or `medium`) and use the thinking-mode sampling [UNS](https://unsloth.ai/docs/models/qwen3.8).
    - For 64K context, use `--ctx-size 65536 --cache-type-k q4_0 --cache-type-v q4_0` [PAUL](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html).
  - MTP speed-up (Simon, on a DGX Spark): `llama serve -hf ggml-org/Qwen3.8-27B-GGUF:Q4_K_M -hfd ggml-org/Qwen3.8-27B-GGUF:Q4_0 --spec-default --spec-type draft-mtp --reasoning-preserve` [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). It needs 1-2 GB more memory [UNS](https://unsloth.ai/docs/models/qwen3.8), so it does not fit on the 16 GB Mac. One tuner found `--spec-draft-n-max 2` best: "Longer sequences actually decrease overall performance" [HNREL](https://news.ycombinator.com/item?id=49301283).
  - Raising the macOS GPU cap: `sudo sysctl iogpu.wired_limit_mb=<MB>`, "No reboot required". This is unsupported by Apple; "If Memory Pressure turns yellow/red or system starts swapping, lower the cap" [DEVNOTE](https://github.com/ivanopcode/devnote-override-macos-metal-vram-cap). It is not recommended on a 16 GB machine.
- **Ollama:**
  - Library: `ollama run qwen3.8`. Tags include `qwen3.8:27b` (18GB, Q4_K_M), `27b-mlx`, `27b-mtp-q4_K_M`, `27b-q8_0` (30GB) and `27b-bf16` (56GB) [OLL](https://ollama.com/library/qwen3.8). None fits 16 GB.
  - Context: "< 24 GiB VRAM: 4k context". Agents need at least 64000, set with `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`; check with `ollama ps` [OLL](https://docs.ollama.com/context-length). Quantize the KV cache with `OLLAMA_KV_CACHE_TYPE` (needs flash attention) [OLL](https://docs.ollama.com/faq).
  - Claude Code: `ollama launch claude --model qwen3.8`. Non-interactive: `ollama launch claude --model <m> --yes -- -p "..."`. Manual setup: `ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen3.8` [OLL](https://docs.ollama.com/integrations/claude-code).
  - OpenCode: `ollama launch opencode --model qwen3.8`, or an `opencode.json` provider using `"npm": "@ai-sdk/openai-compatible"` and `"baseURL": "http://localhost:11434/v1"`. "OpenCode requires a context length of 64k or higher" [OLL](https://docs.ollama.com/integrations/opencode).
  - Running a smaller Unsloth GGUF through Ollama via `hf.co/...`: not verified for this architecture (not found).
- **LM Studio:** model `qwen/qwen3.8-27b`, 16.10 GB [LMS](https://lmstudio.ai/models/qwen3.8). Raise the context from the 8,192 default [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). Simon's `llm` CLI call: `llm -a <image-url> -m lmstudio/qwen/qwen3.8-27b '<prompt>'` [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). It does not fit on the 16 GB Mac.
- **MLX:** `mlx-lm` (text-only) and `mlx-vlm` (vision + text) support the Qwen3.5-architecture series [QWGH](https://github.com/QwenLM/Qwen3.8). The official mlx-community 4-bit is 16.08 GB, too big for a 16 GB Mac. MTPLX: `pip install mtplx`, then `mtplx serve --model Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed`, serving OpenAI- and Anthropic-compatible APIs at `http://127.0.0.1:8000`; it needs 32 GB or more [MTPLX](https://huggingface.co/Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed).
- **vLLM / SGLang (NVIDIA servers, not Macs):** `vllm serve Qwen/Qwen3.8-27B --port 8000 --tensor-parallel-size 4 --max-model-len 262144 --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder` [QWGH](https://github.com/QwenLM/Qwen3.8). NVFP4 with MTP: `vllm serve unsloth/Qwen3.8-27B-NVFP4 --speculative-config '{"method": "mtp", "num_speculative_tokens": 2}'` (Blackwell only) [UNS](https://unsloth.ai/docs/models/qwen3.8).
- **Pi:** Simon's `~/.pi/agent/models.json` defines a provider with `"baseUrl": ".../v1"`, `"api": "openai-responses"`, `"apiKey": "dummy"`, and model `{"id": "qwen3.8-27b", "reasoning": true}`. Run with `pi --provider spark --model qwen3.8-27b` [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). This confirms the `--provider/--model` flags that model-gaps §4 marked unverified. For a local llama-server, point `baseUrl` at `http://localhost:8080/v1`; whether llama-server serves the `openai-responses` API is not verified.
- **Qwen Code:** add a `modelProviders.openai` entry in `settings.json` with `"id"`, `"envKey"`, `"baseUrl": "http://localhost:11434/v1"` (Ollama) or `"http://localhost:1234/v1"` (LM Studio), and `generationConfig` keys such as `timeout`, `streamIdleTimeoutMs` and `contextWindowSize`. Any placeholder API key works for local servers [QCODE](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/). Headless use: `qwen -p "..." --output-format json` (model-gaps §4). Hosted QwenCloud is "compatible with various API specifications, including OpenAI and Anthropic" [QWGH](https://github.com/QwenLM/Qwen3.8).
- **Claude Code via an Anthropic-compatible proxy:** use Ollama's built-in Anthropic API (above) or MTPLX's Anthropic-compatible server (32 GB+) [MTPLX](https://huggingface.co/Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed). Unsloth Desktop also lists Claude Code under "Connect tools" [UNS](https://unsloth.ai/docs/models/qwen3.8). Whether llama-server speaks the Anthropic Messages API, and the exact QwenCloud Anthropic base URL, were not found.
- **Hosted IDs:** QwenCloud `qwen3.8-27b` with an OpenAI-compatible base `https://ap-southeast-1.maas.qwencloudapi.com/compatible-mode/v1` and `extra_body={"enable_thinking": True}` [QCLOUD](https://www.qwencloud.com/models/qwen3.8-27b); OpenRouter `qwen/qwen3.8-27b` [OR](https://openrouter.ai/qwen/qwen3.8-27b).

## 8. Routing-table implications (Qwen3.8-27B)

- **On this 16 GB M2 Pro: do not route coding-agent work to a local Qwen3.8-27B.** It runs only at 2-bit (about 10.9 GiB with 32K to 64K context), at an estimated 5-12 tok/s, and agent preambles may take minutes to process (section 4).
  - Acceptable local uses: overnight or background **classification, short summaries, extraction to JSON, and image labelling**, with reasoning low or off, one request at a time, through llama.cpp.
  - Avoid 1-bit builds entirely [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/).
- **On a 32 GB+ Mac or a 24 GB GPU:** a credible **local coding agent and subagent** (Pi or OpenCode) at Q4_K_M, with no measured loss against BF16 on Terminal-Bench [QUESMA](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/). Use effort medium, or xhigh only for hard one-shots; give it 64K+ context; expect 10-45 tok/s on Apple silicon.
- **Hosted:** prefer **Qwen3.8-Flash-Next** over the 27B for open-weights API routing. It scores AA 40 vs 34, costs $0.37 vs $1.01 per AA task, and lists at $0.15 / $0.47 [AA](https://artificialanalysis.ai/models/qwen3-8-flash-next). Use the hosted 27B only when you need Apache 2.0 weights you can later self-host, or a specific cheap provider.
- **vs gpt-oss-20b:** gpt-oss-20b is far cheaper and faster (AA 9, 258 tok/s, $0.01 per task) but much less capable [AA](https://artificialanalysis.ai/models/gpt-oss-20b). Ollama lists it at 14GB, which is also above a 16 GB Mac's estimated GPU cap; its fit here was not verified. For reasoning-light bulk classification it is the cheaper hosted choice. For anything needing judgement, vision or tool-driven coding, the 27B is in a different class.
- **vs MoE siblings:**
  - No Qwen3.8 30B/35B-A3B exists (section 3).
  - Qwen3.6-35B-A3B (AA 18) is the speed pick on 32 GB+ Macs, at 60-90 tok/s vs about 10 for the 27B [HNREL](https://news.ycombinator.com/item?id=49304287) [HNREL](https://news.ycombinator.com/item?id=49307087).
  - Qwen3-Coder-Next (AA 9, 52GB in Ollama) is dominated by the 27B on AA and does not fit 16 GB. This **corrects model-gaps §4e**, which called Coder-Next "the practical local coding model".
- **Stale items in model-gaps §4e to update:**
  - 27B status: shipped 2026-08-14, Apache 2.0, `Qwen/Qwen3.8-27B` and `-FP8`.
  - Add Qwen3.8-Flash-Next (125B total, 6B active, `qwen-community-1.0` licence, AA 40) [FNCARD](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) [SWFN](https://simonwillison.net/2026/Aug/26/qwen38-flash-next/).
  - Fill the template for the 27B: API ID `qwen3.8-27b` (QwenCloud) or `qwen/qwen3.8-27b` (OpenRouter); price $0.50 input / $0.10 cached / $3.00 output; hosted context 1M (262,144 for open weights); max output 131K [QCLOUD](https://www.qwencloud.com/models/qwen3.8-27b).
  - Pi `--provider/--model` flags are now confirmed [SW](https://simonwillison.net/2026/Aug/16/qwen-38-27b/).
- **Effort rule for any route:** never leave `xhigh` as an unexamined default. Pick low or off for bulk work and medium for agent loops, and test xhigh per task against wall-clock time.

## Sources (Qwen3.8-27B)

| Key | Source | Type | Saved copy (`articles/qwen/`) |
|---|---|---|---|
| HFCARD | [Qwen/Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B), Qwen Team, 2026-08-14 | model card | `hf-model-card-qwen3.8-27b.md` |
| QWGH | [QwenLM/Qwen3.8 GitHub README](https://github.com/QwenLM/Qwen3.8), Qwen Team | vendor blog | `qwenlm-github-qwen3.8-readme.md` |
| FNCARD | [Qwen/Qwen3.8-Flash-Next model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next), Qwen Team, 2026-08-26/27 | model card | `hf-model-card-qwen3.8-flash-next.md` |
| QCLOUD | [QwenCloud qwen3.8-27b page](https://www.qwencloud.com/models/qwen3.8-27b), Alibaba Cloud | vendor blog | `qwencloud-qwen3.8-27b.md` |
| SW | [Qwen 3.8 27B is excellent, but it defaults to wildly overthinking things](https://simonwillison.net/2026/Aug/16/qwen-38-27b/), Simon Willison, 2026-08-16 | practitioner post | `sw-qwen38-27b-overthinking.md` |
| SW52 | [Qwen 3.8 27B scores 52 on the AA Intelligence Index](https://simonwillison.net/2026/Aug/17/qwen-38-27b-scores-52/), Simon Willison, 2026-08-17 | practitioner post | `sw-qwen38-27b-aa-52.md` |
| SWADD | [Qwen3.8 27B addition in words](https://simonwillison.net/2026/Oct/4/qwen38-addition-in-words/), Simon Willison, 2026-10-04 | practitioner post | `sw-qwen38-addition-in-words.md` |
| SWFN | [Qwen3.8-Flash-Next](https://simonwillison.net/2026/Aug/26/qwen38-flash-next/), Simon Willison, 2026-08-26 | practitioner post | `sw-qwen38-flash-next.md` |
| AA | [Artificial Analysis: Qwen3.8 27B](https://artificialanalysis.ai/models/qwen3-8-27b), plus variant and comparison pages | benchmark | `artificial-analysis-qwen3.8-27b.md` |
| QUESMA | [Benchmarking Qwen3.8 27B quantizations](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/), Piotr Migdał, 2026-08-26 | benchmark | `quesma-qwen38-27b-quantizations.md` |
| UNS | [Unsloth: Qwen3.8 - How to Run Locally](https://unsloth.ai/docs/models/qwen3.8), 2026-08-14 (updated 08-19) | vendor blog | `unsloth-qwen3.8-run-locally.md` |
| OLL | [Ollama qwen3.8 library](https://ollama.com/library/qwen3.8) and docs ([Claude Code](https://docs.ollama.com/integrations/claude-code), [OpenCode](https://docs.ollama.com/integrations/opencode), [context length](https://docs.ollama.com/context-length), [FAQ](https://docs.ollama.com/faq)) | vendor blog | `ollama-qwen3.8-library-and-docs.md` |
| LMS | [LM Studio: Qwen3.8](https://lmstudio.ai/models/qwen3.8) | vendor blog | `lmstudio-qwen3.8.md` |
| MTPLX | [Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed](https://huggingface.co/Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed), third-party | model card | `mtplx-qwen3.8-27b-optimized-speed.md` |
| QCODE | [Qwen Code docs: Model Providers](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/) | vendor blog | `qwen-code-model-providers.md` |
| OR | [OpenRouter: qwen/qwen3.8-27b](https://openrouter.ai/qwen/qwen3.8-27b), live API listing | benchmark (price listing) | `openrouter-qwen3.8-27b-pricing.md` |
| PAUL | [Running Qwen 3.8 27B on a 16 GB GPU](https://www.paulsprogrammingnotes.com/2026/08/running-qwen-3-8-27b-16gb.html), Paul Brown, 2026-08-23 | practitioner post | `paul-brown-qwen38-27b-16gb-gpu.md` |
| DEVNOTE | [Override macOS Metal VRAM cap](https://github.com/ivanopcode/devnote-override-macos-metal-vram-cap), ivanopcode | practitioner post | `devnote-macos-metal-vram-cap.md` |
| APPLE | [Apple unveils M2 Pro and M2 Max](https://www.apple.com/newsroom/2023/01/apple-unveils-m2-pro-and-m2-max-next-generation-chips-for-next-level-workflows/), 2023-01-17 | vendor blog | `apple-m2-pro-press-release.md` |
| HNREL | [HN: Qwen 3.8 27B release thread](https://news.ycombinator.com/item?id=49299605), 2026-08-14 | forum | `hn-release-thread.md` |
| HNSW | [HN: discussion of Simon's post](https://news.ycombinator.com/item?id=49324985), 2026-08-16 | forum | `hn-overthinking-thread.md` |
| HNAA | [HN: Qwen3.8 27B scores 52 on AA](https://news.ycombinator.com/item?id=49334544), 2026-08-17 | forum | `hn-aa-52-thread.md` |
| HNCB | [HN: Qwen 3.8 27B on Cerebras](https://news.ycombinator.com/item?id=49554520), 2026-09-03 | forum | `hn-cerebras-thread.md` |

Not found: independent SWE-bench Pro, OSWorld or tool-calling (tau-style) numbers for this model; any first-hand run on a 16 GB Apple silicon Mac; Anthropic-API support in llama-server; the QwenCloud Anthropic base URL; independent quality numbers for the current v3 Unsloth 2-bit and 3-bit files and the Bonsai ternary derivative.

---
# Model 2: gpt-oss-20b (OpenAI open weights)

Saved copies of every source are under `agent-orchestration-sources/articles/gpt-oss/`. The reading notes at the top of this file apply; AA figures are Intelligence Index v4.3.2 at fetch.

**Which "latest"?** There is one general-purpose gpt-oss-20b checkpoint, from 2025-08-05, and no newer one. The only later OpenAI release built on it is **gpt-oss-safeguard-20b** (2025-10-29), a safety-classification fine-tune, covered briefly below. A claimed June 2026 "gpt-oss-20b-a3b" refresh is false (section 1).

## 1. Subject and overall thesis

- **Subject:** `gpt-oss-20b`, OpenAI's smaller open-weight reasoning model: Apache 2.0, 20.91B total and 3.6B active parameters, MoE weights in MXFP4, text only, 131,072-token context, released 2025-08-05 [OAI](https://openai.com/index/introducing-gpt-oss/) [CARD](https://arxiv.org/abs/2508.10925) [OAIDEV](https://developers.openai.com/api/docs/models/gpt-oss-20b).
- **Is there a newer release? No.** Evidence, all checked 2026-10-19:
  - OpenAI's API model page lists a single snapshot, `gpt-oss-20b` [OAIDEV](https://developers.openai.com/api/docs/models/gpt-oss-20b).
  - OpenAI's "Open models" page (Wayback snapshot 2026-10-12) lists only gpt-oss (120B and 20B) and gpt-oss-safeguard [OPENMODELS](https://openai.com/open-models/).
  - On Hugging Face, the `openai/gpt-oss-20b` repo's last commit is 2025-08-26 ("Update README.md"); weight files have not changed since August 2025. The OpenAI org's only newer repos are `gpt-oss-safeguard-*` (created 2025-09-18, released 2025-10-29), `circuit-sparsity` (2025-12) and `privacy-filter` (2026-04) [HFCARD](https://huggingface.co/openai/gpt-oss-20b).
  - AA's data gives gpt-oss-20b a single release date, 2025-08-05 [AA](https://artificialanalysis.ai/models/gpt-oss-20b).
  - The `openai/gpt-oss` GitHub repo's last release is v0.0.9 (2026-01-13). Its 2026 commits only touch tooling (browser-backend and search changes) [GHREPO](https://github.com/openai/gpt-oss).
- **The June 2026 refresh claim is false.** It comes from freeainews.com (Jarrod Gravison, 2026-08-22, low trust). The article says OpenAI "shipped the gpt-oss open-weight model family on June 9, 2026", in sizes "gpt-oss-8b, gpt-oss-20b-a3b, and gpt-oss-120b-a12b" with a 256K context, under an "OpenAI Open Weight License 1.0" [FAN](https://freeainews.com/open-source/openai-gpt-oss-open-weight-2026/). None of these model names exists on OpenAI's Hugging Face org, API docs or open-models page. The only gpt-oss repo commit on 2026-06-09 is "default browser backend to You.com" [GHREPO](https://github.com/openai/gpt-oss).
- **Corrections to `research/model-gaps.md` (2026-10-02):**
  - Its "AA Intelligence Index 12, 160 tok/s" is the **120b** figure. gpt-oss-20b (High) scores **9** and runs at 258 tok/s (hosted median). gpt-oss-120b (High) scores **12** at 265 tok/s [AA](https://artificialanalysis.ai/models/gpt-oss-20b) [AA120](https://artificialanalysis.ai/models/gpt-oss-120b).
  - The "256K" context is the freeainews claim. The real limit is 131,072 tokens [CARD](https://arxiv.org/abs/2508.10925).
  - Its source for "no new generation" is frankx.ai, which is on this brief's excluded list. The primary sources above now support that statement.
  - The Ollama library shows gpt-oss "Updated 1 week ago". That is a repackaging for Ollama's llama.cpp runner (manifest `"runner": "llamacpp"`; Ollama v0.40.2 upgrades older downloads "for better performance and compatibility when running on llama.cpp"), not new weights [OLLIB](https://ollama.com/library/gpt-oss) [OLREL](https://github.com/ollama/ollama/releases/tag/v0.40.2).
- **Thesis:** a fast, cheap, tool-trained small reasoner that is now far behind 2026 models: AA 9 vs 34 for Qwen3.8 27B [AA](https://artificialanalysis.ai/models/gpt-oss-20b) [AAQ27](https://artificialanalysis.ai/models/qwen3-8-27b). Practitioners call it "a tool calling god" for a ripgrep loop [HN-postalcoder](https://news.ycombinator.com/item?id=46628688), but also "definitely not competitive now" [HN-anon373839](https://news.ycombinator.com/item?id=49406023). Its niche is an **offline or private worker** for short, checkable tasks: classification, extraction, search-and-summarise with tools.
- **gpt-oss-safeguard-20b** (the other candidate): "fine-tuned versions of our gpt-oss open models", for classifying content against "a developer-provided policy at inference time", Apache 2.0 [SAFEGUARD](https://openai.com/index/introducing-gpt-oss-safeguard/). Its model card says it fits GPUs with 16GB of VRAM and says: "For other applications, we recommend using gpt-oss models" [SAFEGUARD](https://huggingface.co/openai/gpt-oss-safeguard-20b). Use it only for moderation or policy-labelling pipelines.

## 2. Strengths (with evidence)

- **Small memory footprint for its class.** The checkpoint is 12.8 GiB [CARD](https://arxiv.org/abs/2508.10925). It used "just 11.72GB of my system RAM" in LM Studio and about 13.26 GB in Ollama on Simon Willison's 64 GB Mac [SW](https://simonwillison.net/2025/Aug/5/gpt-oss/). His favourite local model "because it only uses 11GB of RAM and it's designed to run at that quantization size" [HN-simonw](https://news.ycombinator.com/item?id=45002111).
- **Native MXFP4, so extra quantization buys little.** "Always use the original MXFP4 model files" [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396). Unsloth's 2-bit file is 11.5 GB vs 14 GB at F16 and "performs nearly the same" [UNSLOTH](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune).
- **Fast and cheap when hosted.** AA measures 258 tok/s, $0.06 / $0.21 per M tokens and about $0.01 per Index task. It produced 70M output tokens on the Index against an 82M median, "fairly concise" [AA](https://artificialanalysis.ai/models/gpt-oss-20b).
- **Math and STEM reasoning at high effort.**

  | Benchmark (high effort) | OpenAI (self-reported) | AA (independent) |
  |---|---|---|
  | AIME 2025, no tools | 91.7 | 89.3 |
  | GPQA Diamond, no tools | 71.5 | 68.8 |
  | LiveCodeBench | not reported | 77.7 |

  Sources: [CARD](https://arxiv.org/abs/2508.10925) Table 3; [AA](https://artificialanalysis.ai/models/gpt-oss-20b).
- **Trained for tools and structured output.** It was post-trained on a browsing tool, a Python tool and "arbitrary developer functions" [CARD](https://arxiv.org/abs/2508.10925), and supports Structured Outputs [OAI](https://openai.com/index/introducing-gpt-oss/).
  - Tau-Bench Retail is 54.8 at high (self-reported) [CARD](https://arxiv.org/abs/2508.10925). AA's independent tau2 score is 60.2 at high and 50.3 at low [AA](https://artificialanalysis.ai/models/gpt-oss-20b).
  - Practitioner reports:
    - It "had no trouble in Pi" [HN-accrual](https://news.ycombinator.com/item?id=48928098).
    - One user tried Codex, OpenCode, Claude Code and Pi with several small models and settled "on gpt for its impressive pass rates" [HN-abhikul0](https://news.ycombinator.com/item?id=47134991).
    - "Capable of operating tools like bash in a reasonably useful way" on a 32 GB laptop [HN-simonw2](https://news.ycombinator.com/item?id=45844631).
- **Classification.** In one user's spam-filter benchmark (August 2025) it was the best local model at 95.6%, ahead of gemma3:27b at 94.3% and qwen3:32b at 89.2% [HN-jwr](https://news.ycombinator.com/item?id=44815446). Single benchmark, unverified.
- **Configurable effort and a full chain of thought.** Low, medium and high levels are set "with one sentence in the system message" [OAI](https://openai.com/index/introducing-gpt-oss/). Licence: "Apache 2.0 license and our gpt-oss usage policy" [CARD](https://arxiv.org/abs/2508.10925). The usage-policy file asks users to "comply with all applicable law" [HFCARD](https://huggingface.co/openai/gpt-oss-20b).

## 3. Weaknesses, pitfalls and misconceptions

- **It hallucinates facts heavily.**

  | Measure | gpt-oss-20b | gpt-oss-120b | Qwen3.8 27B | Source |
  |---|---|---|---|---|
  | SimpleQA accuracy / hallucination rate (self-reported) | 0.067 / 0.914 | 0.168 / 0.782 | not reported | [CARD](https://arxiv.org/abs/2508.10925) Table 9 |
  | AA-Omniscience index (higher is better) | -63.05 | -49.25 | -9.98 | [AA](https://artificialanalysis.ai/models/gpt-oss-20b), [AA120](https://artificialanalysis.ai/models/gpt-oss-120b), [AAQ27](https://artificialanalysis.ai/models/qwen3-8-27b) |
  | AA-Omniscience hallucination rate | 0.941 | 0.908 | 0.303 | same |

  - OpenAI: smaller models "tend to hallucinate more", and "browsing or gathering external information tends to reduce instances of hallucination" [CARD](https://arxiv.org/abs/2508.10925).
  - A practitioner: "as soon as a solution isn't clear it will hallucinate" [HN-strangescript](https://news.ycombinator.com/item?id=46680313).
  - Never use it as a knowledge source without retrieval.
- **Weak at agentic coding by 2026 standards.**
  - AA Terminal-Bench 4.0: **0%**. Terminal-Bench 2.1: 13.9%, vs 26.2% for gpt-oss-120b and 79.8% for Qwen3.8 27B [AA](https://artificialanalysis.ai/models/gpt-oss-20b) [AA120](https://artificialanalysis.ai/models/gpt-oss-120b) [AAQ27](https://artificialanalysis.ai/models/qwen3-8-27b).
  - Aider Polyglot is 34.2 at high (self-reported) [CARD](https://arxiv.org/abs/2508.10925).
  - In a 24 GB M4 lint-fixing test it "frequently made mistakes like adding or duplicating statements unnecessarily, listing things as fixed without editing the code". Qwen 3.5 9B in OpenCode "fixed every warning" [HN-quacker](https://news.ycombinator.com/item?id=48089940).
  - At launch, in Cline, "Tools calling doesn't work ( they say it does)" and "the structured output doesn't work" [HN-NicoJuicy](https://news.ycombinator.com/item?id=44803073). This was day-one software and may be fixed.
- **Weak long-context reading despite the 128K window.**
  - AA-LCR (long-context reasoning): 34.7%, vs 52% for 120b and 82% for Qwen3.8 27B [AA](https://artificialanalysis.ai/models/gpt-oss-20b) [AAQ27](https://artificialanalysis.ai/models/qwen3-8-27b).
  - In a hash-recall test, "Past 32k characters the response contained hallucinations" [HN-mhitza](https://news.ycombinator.com/item?id=49097572). Unverified.
- **Effort levels behave unevenly.**
  - Low is much weaker: AA AIME25 62.3 at low vs 89.3 at high, GPQA 61.1 vs 68.8 [AA-LOW](https://artificialanalysis.ai/models/gpt-oss-20b-low) [AA](https://artificialanalysis.ai/models/gpt-oss-20b).
  - AA shows Low's Index as "10*" (estimated), above High's 9. That is an estimation artefact; every measured low score is lower.
  - Low produced invalid SVG in Simon's test. High "thought for 5 minutes and 50 seconds" and overflowed LM Studio's default 4096-token context [SW](https://simonwillison.net/2025/Aug/5/gpt-oss/).
  - At high it "randomly results in reasoning loops where the model keeps repeating itself" with about 8 tools bound (open issue) [OLISS-12606](https://github.com/ollama/ollama/issues/12606).
- **Harmony format quirks.**
  - The model "should only be used with the harmony format as it will not work correctly otherwise" [HFCARD](https://huggingface.co/openai/gpt-oss-20b).
  - Drop the previous chain of thought after a `final` message, but pass it back between tool calls in the same turn [HARMONY](https://cookbook.openai.com/articles/openai-harmony).
  - For Chat Completions APIs there is "no generally agreed upon specification" for returning the reasoning [VERIFY](https://cookbook.openai.com/articles/gpt-oss/verifying-implementations).
  - Unsloth found four jinja-template bugs (backslashed strings in tool calls, extra newlines, wrong `final` and `analysis` tags) [UNSLOTH](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune). The HF repo itself changed its chat template twice and added `<|call|>` as an EOS token in August 2025 [HFCARD](https://huggingface.co/openai/gpt-oss-20b).
- **Tool calling depends on the runtime.**
  - Hosted providers differed: Azure scored 80% on AIME25x32 because old vLLM "didn't respect reasoning_effort, so all requests defaulted to medium". "Tool calling is particularly vulnerable to these differences" [SW-PROV](https://simonwillison.net/2025/Aug/15/inconsistent-performance/).
  - Open Ollama bugs:
    - HTTP 500 "error parsing tool call" on its own output, "roughly 2 in 5" calls with an `apply_patch`-style tool [OLISS-17638](https://github.com/ollama/ollama/issues/17638).
    - The template drops `enum` values from tool schemas [OLISS-12763](https://github.com/ollama/ollama/issues/12763).
    - Tool calls not completing in Open WebUI on macOS [OLISS-12187](https://github.com/ollama/ollama/issues/12187).
- **Weaker instruction hierarchy.** "gpt-oss-120b and gpt-oss-20b generally underperform OpenAI o4-mini on our instruction hierarchy evaluations" [CARD](https://arxiv.org/abs/2508.10925). That raises the prompt-injection risk when it reads untrusted web pages or files.
- **Structured output needs enforcement.** A schema in the prompt "doesn't guarantee the full adherence to the schema. For this you still need to construct your own grammar" [HARMONY](https://cookbook.openai.com/articles/openai-harmony). Use the runtime's schema-constrained `format` (section 7).
- **Misconception: "runs in 16 GB" means a 16 GB Mac runs it well.** The card says "systems with as little as 16GB memory" [CARD](https://arxiv.org/abs/2508.10925). The llama.cpp guide says "Macs don't allow to utilize the full 16GB memory by the GPU" [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396). See section 4.
- **Misconception: there is a 2026 "gpt-oss-20b-a3b" with 256K context.** It does not exist (section 1).
- **Misconception: chat output should show the reasoning.** "Developers should not directly show CoTs to users"; they "may contain hallucinated or harmful content" [OAI](https://openai.com/index/introducing-gpt-oss/).
- **Stale knowledge.** Knowledge cutoff is June 2024 per OpenAI [OAIDEV](https://developers.openai.com/api/docs/models/gpt-oss-20b), May 31 2024 per AA [AA](https://artificialanalysis.ai/models/gpt-oss-20b). Text only.

## 4. Pricing, speed, context and limits

- **Specs:**

  | Item | Value | Source |
  |---|---|---|
  | Parameters | 20.91B total, 3.6B active; 32 experts, top-4; 24 layers | [CARD](https://arxiv.org/abs/2508.10925), [HFCARD](https://huggingface.co/openai/gpt-oss-20b) |
  | Context / max output | 131,072 / 131,072 | [OAIDEV](https://developers.openai.com/api/docs/models/gpt-oss-20b) |
  | Attention | alternating 128-token banded and dense layers; GQA with 8 KV heads | [CARD](https://arxiv.org/abs/2508.10925) |
  | Licence | Apache 2.0 plus a short usage policy | [HFCARD](https://huggingface.co/openai/gpt-oss-20b) |
  | Weight files | HF checkpoint 12.8 GiB; Ollama `gpt-oss:20b` 14 GB; ggml-org GGUF 11.27 GiB; MLX 4-bit 11.2 GB | [CARD](https://arxiv.org/abs/2508.10925), [OLLIB](https://ollama.com/library/gpt-oss), [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396), [MLX](https://huggingface.co/mlx-community/gpt-oss-20b-MXFP4-Q4) |

- **Memory arithmetic, from the llama.cpp guide (decimal GB, f16 KV cache, `-ub 2048`)** [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396):

  | Context | Model data | Compute buffers | KV cache | Total |
  |---|---|---|---|---|
  | 8,192 | 12.0 | 2.7 | 0.2 | **14.9** |
  | 32,768 | 12.0 | 2.7 | 0.8 | **15.5** |
  | 131,072 | 12.0 | 2.7 | 3.2 | **17.9** |

  - Cross-check from `config.json` [HFCARD](https://huggingface.co/openai/gpt-oss-20b): the 12 dense layers × 8 KV heads × 64 dims × 2 (K and V) × 2 bytes = 24,576 bytes per token. That gives 0.20 GB per 8K tokens, matching the guide. The 12 sliding layers keep only 128 tokens each.
  - The guide notes that larger `-ub`/`-b` values grow the compute buffers [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396). The 2.7 GB figure is for `-ub 2048`.
- **The reference MacBook Pro M2 Pro, 16 GB: it runs, but not well, and only at short context.**
  - **GPU budget:** an M2 16 GB Mac mini logs Metal `recommendedMaxWorkingSetSize = 12713.12 MB`, about 12.7 GB [LCPP-20704](https://github.com/ggml-org/llama.cpp/issues/20704). The llama.cpp guide advises staying under 70% of total memory, about 12.0 GB on a 16 GiB machine [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396).
  - **Arithmetic:** model data alone (12.0 GB) uses about 94% of the 12.7 GB GPU budget. The full 8K setup (14.9 GB) exceeds it by about 2.2 GB, and 128K (17.9 GB) exceeds total RAM. Part of the model must therefore run on the CPU, and macOS plus your apps share what is left.
  - **llama.cpp's command for 16 GB Macs:** it keeps 12 of the 24 MoE layers on the CPU and caps context at 32K (`--n-cpu-moe 12 -c 32768`) [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396).
  - **Practitioner measurements on 16 GB Macs:**

    | Machine | Runtime | Setting | Result | Source |
    |---|---|---|---|---|
    | MBP M1, 16 GB | LM Studio | ctx 7,990; GPU offload 8/24 layers; low effort | "runs slow and still fine"; with MCP tools, "the tool calls instruction follow is quite good" | [HN-vinhnx](https://news.ycombinator.com/item?id=44811891) |
    | MacBook Air M4, 16 GB | Ollama (Aug 2025) | defaults | "hello" took "a little more than five minutes"; one question about 43 minutes | [9TO5](https://9to5mac.com/2025/08/06/how-to-run-gpt-oss-20b-on-mac/) |
    | "16GB Mac" (model not stated) | Ollama vs llama.cpp (Mar 2026) | not stated | runs with Ollama; "out of memory" with latest llama.cpp | [HN-0xbadcafebee](https://news.ycombinator.com/item?id=47370473) |

  - **No M2 Pro 16 GB tok/s figure found.** The nearest bound: an M1 Pro, 32 GB (same 200 GB/s bandwidth as the M2 Pro [APPLE](https://www.apple.com/newsroom/2023/01/apple-unveils-m2-pro-and-m2-max-next-generation-chips-for-next-level-workflows/) [APPLE-M1](https://www.apple.com/newsroom/2021/10/introducing-m1-pro-and-m1-max-the-most-powerful-chips-apple-has-ever-built/)) with everything on the GPU. Expect less on 16 GB, where experts run on the CPU (not measured).

    | Measure (llama.cpp, M1 Pro 32 GB) | Value |
    |---|---|
    | Generation, empty context | 45.7 tok/s |
    | Generation at 16K context | 33.9 tok/s |
    | Prompt processing at 2K | 505 tok/s |
    | Prompt processing at 16K | 367 tok/s (44.7 s to read 16K tokens) |

    Source: [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396).
  - **Practical context on a 16 GB Mac:** 8K to 16K tokens. 32K is the guide's ceiling with CPU offload. The 64K that Ollama says OpenCode, Codex and Claude Code need does not fit (section 7).
- **Larger Macs for comparison:**

  | Machine | Runtime | Generation | Source |
  |---|---|---|---|
  | M2 MBP 64 GB | llama.cpp | about 82 tok/s | [SW-LCPP](https://simonwillison.net/2025/Aug/19/gpt-oss-with-llama-cpp/) |
  | M2 MBP 64 GB (machine per [HN-simonw](https://news.ycombinator.com/item?id=45002111)) | LM Studio | 39 tok/s (low), 55 tok/s (medium) | [SW](https://simonwillison.net/2025/Aug/5/gpt-oss/) |
  | M4 Max 36 GB | llama.cpp | 92.4 tok/s; 64.8 tok/s at 32K | [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396) |
  | M2 Pro 32 GB | not stated | "quite good"; "around 30k" context practical | [HN-mixermachine](https://news.ycombinator.com/item?id=46932292) |

- **Hosted prices** (USD per M tokens) [OR](https://openrouter.ai/openai/gpt-oss-20b):

  | Provider | Input | Output | Max output |
  |---|---|---|---|
  | Darkbloom (fp8), cheapest | 0.018 | 0.09 | 32,768 |
  | DeepInfra (bf16) | 0.03 | 0.14 | 117,964 |
  | Amazon Bedrock | 0.07 | 0.15 | 117,964 |
  | Groq | 0.075 | 0.30 | 65,536 |

  - All OpenRouter endpoints list 131,072 context. Cerebras does not list gpt-oss-20b there (not found).
  - AA prices the 20b at $0.058 / $0.215 and about $0.01 per Index task [AA](https://artificialanalysis.ai/models/gpt-oss-20b).
- **Comparison with gpt-oss-120b and Qwen's 27B dense model:**

  | | gpt-oss-20b (High) | gpt-oss-120b (High) | Qwen3.8 27B (Xhigh) |
  |---|---|---|---|
  | Released | 2025-08-05 | 2025-08-05 | 2026-08-14 (AA) |
  | Params total / active | 21B / 3.6B | 117B / 5.1B | 27B dense (27.78B in HF metadata) |
  | Licence | Apache 2.0 | Apache 2.0 | Apache 2.0 |
  | Local size (Ollama) | 14 GB | 65 GB | 18 GB (Q4_K_M), 30 GB (Q8) [OLQ38](https://ollama.com/library/qwen3.8/tags) |
  | Fits a 16 GB Mac? | partly (CPU offload) | no | no |
  | Context | 131K | 131K | 256K |
  | AA Intelligence Index | 9 | 12 | 34 |
  | AA hosted tok/s | 258 | 265 | 44 |
  | AA $ per Index task | 0.01 | 0.09 | 1.01 |
  | AA output tokens on Index | 70M | 84M | 200M |
  | AA Terminal-Bench 2.1 | 13.9% | 26.2% | 79.8% |
  | AA-LCR | 34.7% | 52% | 82% |
  | Input modalities | text | text | text, image, video |

  Sources: [AA](https://artificialanalysis.ai/models/gpt-oss-20b), [AA120](https://artificialanalysis.ai/models/gpt-oss-120b), [AAQ27](https://artificialanalysis.ai/models/qwen3-8-27b), [OLLIB](https://ollama.com/library/gpt-oss).

  - Qwen3.8 27B Ollama tags: `qwen3.8:27b` (Q4_K_M) 18 GB, `q8_0` 30 GB [OLQ38](https://ollama.com/library/qwen3.8/tags).
  - One practitioner benchmark on an RTX 5090: gpt-oss 20B generates at 327 tok/s vs 53 tok/s for a Qwen3.5 27B Q6_K [HN-magicalhippo](https://news.ycombinator.com/item?id=47942148). That is roughly the dense-27B speed penalty.

## 5. Recommended prompting style and workflow

- **Set effort in the system message.** The recommended form is `Reasoning: high` (or `medium`, `low`); the default is medium [HARMONY](https://cookbook.openai.com/articles/openai-harmony). In runtimes:
  - Ollama: `think: "low"|"medium"|"high"` (default `medium`) [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
  - llama.cpp: `--chat-template-kwargs '{"reasoning_effort": "high"}'` [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396).
- **Effort cost:**
  - OpenAI reports "log-linear returns on most tasks, where longer CoTs provide higher accuracy at a relatively large increase in final response latency and cost". gpt-oss-20b uses "over 20k CoT tokens per problem on average for AIME" [CARD](https://arxiv.org/abs/2508.10925).
  - Thinking time in one test: 0.07 s at low, 4.44 s at medium, 5 min 50 s at high (pelican SVG prompt, 64 GB M2) [SW](https://simonwillison.net/2025/Aug/5/gpt-oss/).
  - AA counts 70M output tokens across its Index at high. No per-level token counts were found for low or medium.
- **Effort by task (vendor numbers self-reported; AA independent):**

  | Task family | Low | Medium | High | Source |
  |---|---|---|---|---|
  | AIME 2025, no tools (OpenAI) | 37.1 | 72.1 | 91.7 | [CARD](https://arxiv.org/abs/2508.10925) |
  | SWE-bench Verified (OpenAI) | 37.4 | 53.2 | 60.7 | [CARD](https://arxiv.org/abs/2508.10925) |
  | Tau-Bench Retail (OpenAI) | 35.0 | 47.3 | 54.8 | [CARD](https://arxiv.org/abs/2508.10925) |
  | AA tau2 | 50.3 | not measured | 60.2 | [AA-LOW](https://artificialanalysis.ai/models/gpt-oss-20b-low), [AA](https://artificialanalysis.ai/models/gpt-oss-20b) |
  | AA IFBench | 57.8 | not measured | 65.1 | same |

  - **Low:** yes/no classification, extraction and short summaries where speed matters.
  - **Medium:** the default for tool loops.
  - **High:** only for math or logic, with at least 16K context and a loop guard (section 3).
- **Sampling:** `temperature=1.0`, `top_p=1.0`. "**Do not use repetition penalties!**" [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396). Unsloth adds `top_k=0` and a "recommended minimum context: 16,384" [UNSLOTH](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune).
- **Harmony roles:** the system message carries effort, dates and built-in tools. The developer message is "what is commonly considered the 'system prompt'": instructions, function definitions and response formats [HARMONY](https://cookbook.openai.com/articles/openai-harmony).
  - Hierarchy: system over developer over user [CARD](https://arxiv.org/abs/2508.10925).
  - Put task rules in the developer message. Do not rely on them against injected text.
- **Channels:** `analysis` holds the chain of thought, which does "not adhere to the same safety standards as final messages". `commentary` carries function calls and occasional user-visible preambles. `final` is the answer [HARMONY](https://cookbook.openai.com/articles/openai-harmony). Parse only `final` as the deliverable.
- **Structured output:** declare the schema under `# Response Formats` in the developer message [HARMONY](https://cookbook.openai.com/articles/openai-harmony), and also enforce it with the runtime's schema option. Ollama says "It is ideal to also pass the JSON schema as a string in the prompt" [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
- **Ground factual answers** with browsing or supplied documents, given the hallucination rates in section 3 [CARD](https://arxiv.org/abs/2508.10925).
- **Keep prompts short on small machines.** Pi's initial prompt is about 1.5K tokens vs 7-10K for other CLIs [HN-abhikul0](https://news.ycombinator.com/item?id=47134991). Claude Code's system prompt is 15-40K tokens [HN-d4rkp4ttern](https://news.ycombinator.com/item?id=47620689).

## 6. Subagents, orchestration, delegation and verification

- **Role:** a worker, never the orchestrator. It fits:
  - "running gpt-oss 20B in a while loop with access to ripgrep" for local RAG-style search [HN-postalcoder](https://news.ycombinator.com/item?id=46628688)
  - classification and triage with an enforced schema [HN-jwr](https://news.ycombinator.com/item?id=44815446)
  - first-pass security review against a fixed checklist [HN-mhitza2](https://news.ycombinator.com/item?id=45451864)
- **Verify every claimed edit.** It has listed "things as fixed without editing the code" [HN-quacker](https://news.ycombinator.com/item?id=48089940). The orchestrator should diff, run tests and re-check; the subagent's "done" counts for nothing.
- **Check facts against sources.** With an AA-Omniscience hallucination rate of 0.94 [AA](https://artificialanalysis.ai/models/gpt-oss-20b), any fact it states without a quoted source should be treated as unverified.
- **Untrusted content risk.** Its instruction hierarchy is weaker than o4-mini's [CARD](https://arxiv.org/abs/2508.10925). Do not give it write tools while it reads untrusted web pages.
- **Parallelism costs memory.** llama.cpp's multi-slot example (`-np 4`, 524,288 context) "requires extra memory" [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396). Ollama: "Required RAM will scale by `OLLAMA_NUM_PARALLEL` * `OLLAMA_CONTEXT_LENGTH`" [OLDOCS](https://github.com/ollama/ollama/tree/main/docs). On the 16 GB Mac, run one slot.
- **Check the provider before trusting results.** Run OpenAI's compatibility test; a correct implementation shows "0 invalid requests and over 90% on both pass@k and pass^k" [VERIFY](https://cookbook.openai.com/articles/gpt-oss/verifying-implementations). Simon ran OpenAI's AIME25 eval against LM Studio on his Mac in about 3.5 hours [SW-EVAL](https://simonwillison.net/2025/Aug/17/gpt-oss-eval-suite/).
- **Hosted vs local:** for a non-private task, a hosted 20b at $0.03-0.075 input is far faster than a 16 GB Mac [OR](https://openrouter.ai/openai/gpt-oss-20b). Local only makes sense for offline or private data.

## 7. Harness specifics

- **Ollama:**
  - Pull: `ollama pull gpt-oss:20b` (14 GB) [OLLIB](https://ollama.com/library/gpt-oss).
  - Run: `ollama run gpt-oss:20b --think=low --hidethinking --verbose` (`--verbose` shows "timings for response") [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
  - Default context is "< 24 GiB VRAM: 4k context". Agents and coding tools "should be set to at least 64000 tokens" [OLDOCS](https://github.com/ollama/ollama/tree/main/docs). On 16 GB, set 16K instead: `launchctl setenv OLLAMA_CONTEXT_LENGTH 16384`, then restart the app. Check the CPU/GPU split with `ollama ps`.
  - K/V cache: `OLLAMA_KV_CACHE_TYPE=q8_0` "uses approximately 1/2 the memory of `f16`" [OLDOCS](https://github.com/ollama/ollama/tree/main/docs). One llama.cpp user found KV quantization on gpt-oss "bad, performance was halved" on an AMD GPU [LCPP-SteelPh0enix](https://github.com/ggml-org/llama.cpp/discussions/15396#discussioncomment-14143427). Test before relying on it.
  - Schema-constrained output: `POST /api/chat` with `"format": {<JSON schema>}`. Effort: `"think": "low"` [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
  - Since v0.40 Ollama runs supported models on MLX by default on Apple silicon [OLREL](https://github.com/ollama/ollama/releases/tag/v0.40.0). The gpt-oss manifest targets the llama.cpp runner [OLLIB](https://ollama.com/library/gpt-oss).
- **llama.cpp:**
  - Install: `brew install llama.cpp`.
  - 16 GB Mac: `llama-server -hf ggml-org/gpt-oss-20b-GGUF --n-cpu-moe 12 -c 32768 --jinja --no-mmap` [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396). Lower `-c` to 16384 if it swaps.
  - Add `--temp 1.0 --top-p 1.0 --chat-template-kwargs '{"reasoning_effort": "low"}'` [LCPP](https://github.com/ggml-org/llama.cpp/discussions/15396).
  - Serves an OpenAI-compatible API and web UI on port 8080 [SW-LCPP](https://simonwillison.net/2025/Aug/19/gpt-oss-with-llama-cpp/).
  - `sudo sysctl iogpu.wired_limit_mb=...` raises the GPU memory cap. The guide shows it only for a 192 GB machine; on 16 GB it starves macOS (untested).
- **LM Studio:** `lms get openai/gpt-oss-20b` [HFCARD](https://huggingface.co/openai/gpt-oss-20b). Raise the context above its default (4096 in August 2025) and set partial GPU offload (one 16 GB user used 8/24 layers) [SW](https://simonwillison.net/2025/Aug/5/gpt-oss/) [HN-vinhnx](https://news.ycombinator.com/item?id=44811891).
- **MLX:** `pip install mlx-lm`, then `load("mlx-community/gpt-oss-20b-MXFP4-Q4")` and `generate(...)` in Python (11.2 GB) [MLX](https://huggingface.co/mlx-community/gpt-oss-20b-MXFP4-Q4). No measured M2 Pro MLX speed found.
- **vLLM:** `vllm serve openai/gpt-oss-20b`. The install command uses a CUDA wheel (`cu128`) [HFCARD](https://huggingface.co/openai/gpt-oss-20b), so it is for NVIDIA servers, not Macs.
- **Codex CLI:**
  - Run: `codex --oss -m gpt-oss:20b`, or `--local-provider ollama|lmstudio`. The default OSS model is `gpt-oss:20b`, and Codex **pulls the model automatically if it is missing** (14 GB) [CODEX](https://github.com/openai/codex/blob/main/codex-rs/ollama/src/lib.rs).
  - Ollama route: `ollama launch codex`. Ollama: "Use a context window of at least 64k tokens for Codex" [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
  - One user ran an agentic Codex refactor against llama-server at 125K context on a 16 GB NVIDIA card at about 96 tok/s [LCPP-bartlettroscoe](https://github.com/ggml-org/llama.cpp/discussions/15396#discussioncomment-14388222).
- **OpenCode:**
  - Run: `ollama launch opencode --model gpt-oss` [OLLIB](https://ollama.com/library/gpt-oss).
  - Manual setup: in `opencode.json`, add an `ollama` provider with `"npm": "@ai-sdk/openai-compatible"`, `baseURL` `http://localhost:11434/v1`, and model `gpt-oss:20b` [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
  - "OpenCode requires a context length of 64k or higher" [OLDOCS](https://github.com/ollama/ollama/tree/main/docs), which does not fit in 16 GB.
- **Pi:**
  - Run: `ollama launch pi --model gpt-oss:20b`.
  - Manual setup: in `~/.pi/agent/models.json`, add provider `ollama` with `"api": "openai-completions"`, `baseUrl` `http://localhost:11434/v1`, and model id `gpt-oss:20b` [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
  - Its small prompt makes it the best fit for 16 GB [HN-abhikul0](https://news.ycombinator.com/item?id=47134991).
- **Claude Code via Ollama's Anthropic-compatible API:**
  - Run: `ollama launch claude --model gpt-oss` [OLLIB](https://ollama.com/library/gpt-oss), or set `ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434` and run `claude --model gpt-oss:20b` [OLDOCS](https://github.com/ollama/ollama/tree/main/docs).
  - Not on a 16 GB Mac. Since v0.40.2, "`ollama launch claude` uses the model's full context length" [OLREL](https://github.com/ollama/ollama/releases/tag/v0.40.2), which for this model is 131K, about 17.9 GB by the table in section 4. Claude Code's prompt alone is 15-40K tokens [HN-d4rkp4ttern](https://news.ycombinator.com/item?id=47620689).

## 8. Routing-table implications (gpt-oss-20b)

- **Add only as an offline or private tier.** Hosted cheap models dominate it on capability, and on a 16 GB Mac it is slow and memory-bound (sections 2 and 4).
- **Route to gpt-oss-20b (low or medium effort, Pi or a direct Ollama/llama.cpp API call, 8-16K context):**
  - classification and triage with a schema enforced by Ollama `format`
  - extraction to JSON
  - short summaries of supplied text
  - grep or ripgrep tool loops that return file paths and quotes for the orchestrator to check
- **Do not route:**
  - code edits, refactors or PR work (Terminal-Bench 4.0 = 0%, false "fixed" claims)
  - factual Q&A without sources (hallucination rate 0.94)
  - long-document reading over about 16K tokens (AA-LCR 34.7%, and slow prefill on a 16 GB Mac)
  - anything through Claude Code, OpenCode or Codex on the 16 GB Mac, since all three need 64K or more context
  - reading untrusted web content with write tools enabled
- **Effort:** default `low` for classification and extraction, `medium` for tool loops. Avoid `high` on 16 GB: thinking runs long, it loops with tools, and it overflows small contexts.
- **Prefer instead:**
  - Hosted bulk work: a hosted 20b or 120b at a few cents per M tokens, or the profiled 2026 cheap models in `model-gaps.md`.
  - A stronger local option needs a bigger machine. Qwen3.8 27B scores AA 34 but needs 18 GB at Q4.
  - On 16 GB, practitioners prefer Qwen 3.5 9B for coding ("For 16GB laptops, Qwen 3.5 9B is the undisputed champ") [HN-0xbadcafebee2](https://news.ycombinator.com/item?id=48390110) [HN-quacker](https://news.ycombinator.com/item?id=48089940). Unverified; worth its own profile.
- **Safety and moderation labelling:** gpt-oss-safeguard-20b, not the base model [SAFEGUARD](https://openai.com/index/introducing-gpt-oss-safeguard/).
- **Update `model-gaps.md`:**
  - gpt-oss-20b AA Index is 9 (120b is 12).
  - Context is 131,072, not 256K.
  - There is no 2026 refresh: the freeainews June 2026 claim is false. Cite OpenAI's API model page and Hugging Face instead of frankx.ai.

## Sources (gpt-oss-20b)

| Key | Source | Type | Saved copy (`articles/gpt-oss/`) |
|---|---|---|---|
| OAI | [OpenAI: Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/), 2025-08-05 | vendor blog | openai-introducing-gpt-oss.md |
| CARD | [gpt-oss-120b & gpt-oss-20b Model Card](https://arxiv.org/abs/2508.10925), arXiv v1 2025-08-08 | model card | openai-gpt-oss-model-card.md |
| HFCARD | [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | model card | hf-gpt-oss-20b-model-card.md |
| OAIDEV, OPENMODELS | [OpenAI API: gpt-oss-20b](https://developers.openai.com/api/docs/models/gpt-oss-20b); [Open models by OpenAI](https://openai.com/open-models/) (Wayback 2026-10-12) | vendor docs | openai-platform-gpt-oss-20b-and-open-models.md |
| SAFEGUARD | [Introducing gpt-oss-safeguard](https://openai.com/index/introducing-gpt-oss-safeguard/), 2025-10-29, plus [HF card](https://huggingface.co/openai/gpt-oss-safeguard-20b) | vendor blog + card | openai-gpt-oss-safeguard.md |
| HARMONY | [OpenAI Harmony Response Format](https://cookbook.openai.com/articles/openai-harmony) | vendor docs | openai-cookbook-harmony-format.md |
| VERIFY | [Verifying gpt-oss implementations](https://cookbook.openai.com/articles/gpt-oss/verifying-implementations) | vendor docs | openai-cookbook-verifying-implementations.md |
| GHREPO | [openai/gpt-oss on GitHub](https://github.com/openai/gpt-oss) | vendor docs | github-openai-gpt-oss-readme.md |
| SW | [Simon Willison: OpenAI's new open weight (Apache 2) models are really good](https://simonwillison.net/2025/Aug/5/gpt-oss/), 2025-08-05 | practitioner | simonwillison-gpt-oss-launch.md |
| SW-PROV | [Simon Willison: inconsistent performance across providers](https://simonwillison.net/2025/Aug/15/inconsistent-performance/), 2025-08-15 | practitioner | simonwillison-inconsistent-providers.md |
| SW-LCPP | [Simon Willison: llama.cpp guide link](https://simonwillison.net/2025/Aug/19/gpt-oss-with-llama-cpp/), 2025-08-19 | practitioner | simonwillison-llama-cpp-guide-link.md |
| SW-EVAL | [Simon Willison: gpt-oss eval suite on LM Studio](https://simonwillison.net/2025/Aug/17/gpt-oss-eval-suite/), 2025-08-17 | practitioner | simonwillison-gpt-oss-eval-suite.md |
| LCPP (+ comment keys) | [llama.cpp guide: running gpt-oss](https://github.com/ggml-org/llama.cpp/discussions/15396), ggerganov, 2025-08-18, live | practitioner / forum | llama-cpp-guide-running-gpt-oss.md |
| LCPP-20704 | [llama.cpp issue #20704](https://github.com/ggml-org/llama.cpp/issues/20704), M2 16GB Metal limit, 2026-03-18 | forum | llama-cpp-issue-20704-m2-16gb-metal-limit.md |
| AA, AA-LOW | [AA: gpt-oss-20b](https://artificialanalysis.ai/models/gpt-oss-20b), [AA: gpt-oss-20b (Low)](https://artificialanalysis.ai/models/gpt-oss-20b-low) | benchmark | artificial-analysis-gpt-oss-20b.md |
| AA120 | [AA: gpt-oss-120b](https://artificialanalysis.ai/models/gpt-oss-120b) | benchmark | artificial-analysis-gpt-oss-120b.md |
| AAQ27 | [AA: Qwen3.8 27B](https://artificialanalysis.ai/models/qwen3-8-27b) | benchmark | artificial-analysis-qwen3-8-27b.md |
| OLLIB | [Ollama library: gpt-oss](https://ollama.com/library/gpt-oss) plus registry manifest | vendor docs | ollama-library-gpt-oss.md |
| OLQ38 | [Ollama library: qwen3.8 tags](https://ollama.com/library/qwen3.8/tags) | vendor docs | ollama-library-qwen3-8-tags.md |
| OLDOCS, OLREL | [Ollama docs](https://github.com/ollama/ollama/tree/main/docs) (context length, FAQ, thinking, structured outputs, integrations, CLI flags); releases [v0.40.0](https://github.com/ollama/ollama/releases/tag/v0.40.0) and [v0.40.2](https://github.com/ollama/ollama/releases/tag/v0.40.2) | vendor docs | ollama-docs-context-and-integrations.md |
| OLISS-* | Ollama issues [#12606](https://github.com/ollama/ollama/issues/12606), [#17638](https://github.com/ollama/ollama/issues/17638), [#12187](https://github.com/ollama/ollama/issues/12187), [#12763](https://github.com/ollama/ollama/issues/12763) | forum | ollama-github-issues-gpt-oss.md |
| HN-* | Hacker News comments by named users (permalinks inline) | forum | hackernews-gpt-oss-20b-comments.md |
| UNSLOTH | [Unsloth: gpt-oss How to Run](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune) | practitioner docs | unsloth-gpt-oss-how-to-run.md |
| 9TO5 | [9to5Mac (Zac Hall): How to run gpt-oss-20b on Mac](https://9to5mac.com/2025/08/06/how-to-run-gpt-oss-20b-on-mac/), 2025-08-06 | release coverage | 9to5mac-how-to-run-gpt-oss-20b-on-mac.md |
| CODEX | [openai/codex: Ollama OSS defaults](https://github.com/openai/codex/blob/main/codex-rs/ollama/src/lib.rs) | vendor source | codex-cli-oss-provider-source.md |
| MLX | [mlx-community/gpt-oss-20b-MXFP4-Q4](https://huggingface.co/mlx-community/gpt-oss-20b-MXFP4-Q4) | model card | mlx-community-gpt-oss-20b-mxfp4-q4.md |
| OR | [OpenRouter: openai/gpt-oss-20b](https://openrouter.ai/openai/gpt-oss-20b) | pricing data | openrouter-gpt-oss-20b-endpoints.md |
| APPLE, APPLE-M1 | [Apple: M2 Pro](https://www.apple.com/newsroom/2023/01/apple-unveils-m2-pro-and-m2-max-next-generation-chips-for-next-level-workflows/); [Apple: M1 Pro](https://www.apple.com/newsroom/2021/10/introducing-m1-pro-and-m1-max-the-most-powerful-chips-apple-has-ever-built/) | vendor press release | apple-m2-pro-m1-pro-press-releases.md |
| FAN | [freeainews.com: gpt-oss Full Guide 2026](https://freeainews.com/open-source/openai-gpt-oss-open-weight-2026/), 2026-08-22 (**low trust; origin of the false June 2026 claim**) | content site | freeainews-claimed-june-2026-gpt-oss-release.md |

---
# Cross-model synthesis (for the routing table)

Both models are Apache 2.0 open weights that a single machine can run. They sit at opposite corners of the small-model space: the Qwen is the smartest open model in its size class and the slow, expensive one; gpt-oss-20b is a fast, cheap, tool-trained reasoner that 2026 models have left behind. Figures are from the Model 1 and Model 2 sections above, with their sources.

| Dimension | Qwen3.8-27B | gpt-oss-20b |
|---|---|---|
| Released / licence | 2026-08-14 / Apache 2.0 | 2025-08-05 / Apache 2.0 plus usage policy; no newer checkpoint exists |
| Architecture | 27.8B dense, hybrid Gated DeltaNet and attention, vision and video input | 20.9B total, 3.6B active MoE, MXFP4 native, text only |
| Context | 262K native (1M hosted or with YaRN) | 131K |
| AA Intelligence Index | 34 at default `xhigh`; 28 medium; 26 low; 20 no reasoning | 9 at high; low shown as an estimated 10 but every measured low score is lower |
| AA cost per task, hosted | $1.01 ($0.50 in / $3.00 out on QwenCloud) | about $0.01 ($0.06 in / $0.21 out) |
| AA hosted speed | 44 tok/s | 258 tok/s |
| AA Terminal-Bench 2.1 / 4.0 | 79.8% / not listed; Quesma independent 70.8% at BF16 and Q4_K_M | 13.9% / 0% |
| AA long-context (AA-LCR) | 82% | 34.7% |
| AA-Omniscience hallucination rate | 0.30 | 0.94 |
| Practical local file | Q4_K_M, 17 GB (no measured loss); 2-bit UD-Q2_K_XL, 9.8 GB (Terminal-Bench 64%) | MXFP4 as shipped, 12.8 GiB (Ollama 14 GB); further quantization buys little |
| Fits a 16 GB M2 Pro? | Only at 2-bit through llama.cpp, 32K to 64K context, about 10.9 GiB total | Yes with 12 of 24 MoE layers on the CPU, 8K to 16K practical context, 32K ceiling |
| Expected speed there | 5 to 12 tok/s (our estimate); minutes of prompt processing for an agent preamble | No measurement; below the 34 to 46 tok/s an M1 Pro 32 GB gets fully on GPU |
| Needs a bigger machine for | Coding agent at Q4 on a 32 GB Mac or 24 GB GPU, 10 to 45 tok/s | Any 64K-context harness (Claude Code, OpenCode, Codex), which needs about 18 GB |
| Role in this kit | Local or hosted generalist subagent: codebase Q&A, classification, JSON extraction, vision, long reading | Offline or private worker: classification with an enforced schema, extraction, short summaries, grep loops |
| Do not route | Interactive coding on 16 GB; hosted bulk work (Flash-Next is smarter and 3x cheaper); anything at 1-bit | Code edits, factual Q&A without sources, reading past about 16K, untrusted web content with write tools |
| Effort guidance | Never leave the `xhigh` default; low or off for bulk, medium for agent loops | `low` for classification, `medium` for tool loops; avoid `high` on 16 GB (loops, overflows) |
| Harness on the 16 GB Mac | llama.cpp server plus Pi or direct API; no Ollama, LM Studio or MLX build fits | Ollama or llama.cpp plus Pi or direct API; `ollama launch claude` now uses 131K context and will not fit |
| Verification | Smart but "obsessive"; pair with tests; keep review and merge with a frontier model | Reports edits it did not make; the orchestrator diffs and re-runs tests |

## Routing shortlist for this setup

- **Neither model earns a row in the routing table today.** The table's `bulk` row is Haiku 5.5 at $0.10 / $0.50 per MTok with reasoning on, and `research/model-gaps.md` already lists GPT-6 Luna and DeepSeek V4.1 Flash as cheaper hosted tiers. A local model only wins when the data cannot leave the machine or the network is down.
- **If an offline tier is wanted on the 16 GB M2 Pro, gpt-oss-20b is the one that fits.** Run it through Ollama or llama.cpp at 8K to 16K context, `low` or `medium` effort, with a JSON schema enforced by the runtime, one request at a time, and have the orchestrator verify every output. Expect classification, extraction and short summaries, not code.
- **Qwen3.8-27B is the local model to want on 32 GB or more.** At 32 GB or more it becomes a credible coding subagent through Pi or OpenCode. On 16 GB, its 2-bit build is an overnight batch tool at best, and the hosted sibling Qwen3.8-Flash-Next (AA 40, $0.37 per task) is the better API call.
- **Both digests disagree with `research/model-gaps.md` as of 2026-10-02** on four points, now carried there as dated update notes: the 27B shipped; Qwen3-Coder-Next is not the practical local coder; the gpt-oss AA score of 12 was the 120b (the 20b is 9); and the "256K" context and "June 2026 refresh" trace to one low-trust content site and are false.
- **Candidate for a follow-up profile:** Qwen 3.5 9B, which two practitioners call the best coding model for 16 GB laptops (Model 2 §8; unverified).
