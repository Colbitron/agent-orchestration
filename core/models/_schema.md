# Model profile schema

One file per model in this directory, named `<vendor>-<model>-<version>.md`
(for example `claude-opus-5-5.md`, `gpt-6-1-sol.md`). Each file is YAML
frontmatter followed by a markdown body. The frontmatter is what the routing
generator reads; the body is what the orchestrator reads when it needs
nuance.

Profiles describe the model as the research found it on the date in
`as_of`. When you learn something new, edit the profile, bump `as_of`, and
re-run the generator. Do not put user-specific opinions here; those belong in
the user's config.

## Frontmatter

```yaml
---
id: claude-opus-5-5              # file name without .md
name: Claude Opus 5.5
vendor: anthropic                # anthropic | openai | google | xai | zhipu | ...
family: claude                   # claude | gpt | gemini | grok | open-weights
status: current                  # current | preview | deprecated | unreleased
released: 2026-08               # YYYY-MM if known, else null
as_of: 2026-10-02               # date the profile was last verified
confidence: high                 # high | medium | low (how good the evidence is)

api_ids: [claude-opus-5-5]       # ids accepted by APIs and CLIs
access:
  subscriptions: [claude-pro, claude-max]   # consumer plans that include it
  api: true
  harnesses: [claude-code, cursor, opencode, t3-code]   # where it can be selected
  invoke_via: [claude-cli]       # bridge ids from core/bridges/ that reach it

pricing_per_mtok:                # USD per million tokens; null if unknown
  input: 4
  output: 20
  cache_read: 0.20
  cache_write: 5
context_window: 1000000
notes_on_cost: >
  Short free text on what actually drives cost for this model (cache reads,
  token hunger, subscription quota rules).

effort:
  levels: [low, medium, high, xhigh, max]
  default: high
  avoid: [low, max]
  notes: one line on why

scores:                          # 1-10, see docs/ARCHITECTURE.md for axis meanings
  intelligence: 8
  taste: 7
  floor: 7
  thoroughness: 5
  cost_efficiency: 6
  speed: 7
  computer_use: 4
  orchestration: 7

tasks:                           # one entry per id in core/tasks.md
  quick-fix:   {fit: good, note: ""}
  feature:     {fit: best, note: ""}
  long-run:    {fit: good, note: ""}
  frontend:    {fit: ok,   note: "needs explicit style direction"}
  review:      {fit: ok,   note: "precise but finds less than OpenAI"}
  investigate: {fit: ok,   note: ""}
  analyze:     {fit: good, note: ""}
  bulk:        {fit: good, note: ""}
  research:    {fit: good, note: ""}
  computer-use:{fit: poor, note: ""}
  copy:        {fit: good, note: ""}
  3d-games:    {fit: good, note: "feel over visuals"}
  prompt-writing: {fit: ok, note: ""}
  babysit:     {fit: good, note: ""}
  orchestrate: {fit: good, note: "must be told it may use subagents"}

role_hints:                      # one-line answers the generator uses
  as_primary: "Default daily driver for most coding work."
  as_subagent: "Implementation and analysis subagent."
  never_for: ["max effort", "unsupervised macOS computer use"]

local:                           # only for open weights the user can run on their own machine; omit for hosted-only models
  runs_locally: true
  licence: apache-2.0
  runtimes: [ollama, llama-cpp, lm-studio, mlx, vllm]
  memory_gb_by_quant:            # total VRAM or unified memory for the weights plus a working context, from third-party measurements
    q8: 31
    q4: 18
    q2: 11
  min_memory_gb: 11              # the smallest build worth running; smaller builds never count as a fit
  preferred_quant: q4            # optional: the build to assume whenever it fits, instead of the largest that fits
  recommended_memory_gb: 24      # usable memory the task fits assume; below it they count one step worse (best -> good -> ok -> poor)
  cpu_offload: false             # optional: true for sparse MoE models that run with some layers on the CPU (gpt-oss); then a unified-memory machine's whole RAM bounds the fit
  runtimes_by_quant:             # optional: which runtimes ship a given build; omitted means all of `runtimes`
    q2: [llama-cpp]
  measured_speed:                # third-party numbers only; never measured by the kit
    - {machine: "M4 Pro Mac mini 64 GB", runtime: "LM Studio Q4_K_M", tok_s: 12.75, source: "HNREL"}
---
```

Quote any id that contains a colon, such as Ollama tags (`"qwen3.8:27b"`,
`"gpt-oss:20b"`), in `api_ids` and in `config.yaml`. Unquoted, YAML reads
the colon as a mapping and the profile fails to parse.

### The `local` block

Present only on profiles whose weights the user can run themselves. The
generator uses it when a model is enabled with `host: local` (or when the
user's `access.open_weights.type` is `local` and the profile has this
block): it takes the user's `hardware.memory_gb`, allows 75% of it on
unified-memory machines (macOS caps what the GPU may use) and all of it on
a dedicated GPU, and picks `preferred_quant` when it fits, else the largest
entry in `memory_gb_by_quant` that fits and is at least `min_memory_gb`. A model with no fitting build is
disabled with a note in routing.md; a fitting one shows its build in the
"Reach it via" column, with the runtimes from `runtimes_by_quant` when that
build is not in every runtime (Ollama's library rarely ships 2-bit files).
When the machine's usable memory is below `recommended_memory_gb`, the
model's task fits count one step worse on that machine (`best` becomes
`good`, `good` becomes `ok`, `ok` becomes `poor`), and routing.md says so:
the fits were written for a machine at or above the recommendation, and a
smaller one runs a smaller build, less context, or part of the model on the
CPU. `cpu_offload: true` marks a model that tolerates the last of these
(a sparse MoE with few active parameters); for it, the whole of a
unified-memory machine counts when deciding whether it fits, since the
layers the GPU cannot hold run from the same RAM, but the GPU's share still
decides the one-step penalty. Dedicated GPUs are bounded by VRAM either way.
The Ollama bridge is named in the reach column only when Ollama ships the
chosen build and `access.open_weights.provider` is Ollama or unset. `runtimes` and
`measured_speed` are for the human reader; `tok_s` may be a number or a
"low-high" string. Every number comes from a cited third-party measurement
in the research digest; the kit runs nothing.

`fit` values: `best` (route here first), `good`, `ok` (works with guardrails),
`poor` (avoid), `unknown` (no evidence). The generator prefers `best`, falls
back to `good`, and only uses `ok` when nothing better is available in the
user's environment.

## Body sections (in this order)

```
## Summary
Two or three sentences: what this model is for and what it is not for.

## Strengths
Bullets with evidence. Cite the research file and, where possible, the
number or quote.

## Weaknesses and failure modes
Bullets. Include the specific behaviours an orchestrator must guard against
(stops early, scope-creeps, says it will fix and doesn't, context anxiety…).

## How to prompt it
What to include, what to leave out, verbatim snippets that are known to
work. Note differences from prompting other models.

## Routing guidance
"Route here for…" and "Do not route here for…" bullets, plus the handoff
patterns it participates in (e.g. "Astra prototypes, Fable polishes").

## Cost notes
What drives cost, subscription quirks, what effort level to use for value.

## Evidence
List of sources: research file sections, URLs, dates. Mark anything
unverified. End with a `### Score rationale` table giving one line per
axis explaining the number in the frontmatter.
```

## Scoring rubric

Scores are relative to the current frontier, not absolute. Re-baseline when a
new generation ships.

- **10** best available anywhere for that axis.
- **8–9** frontier tier, minor gaps.
- **6–7** solid, use with light guardrails.
- **4–5** usable only with heavy guardrails or for narrow cases.
- **1–3** avoid.

When evidence is thin, score conservatively and set `confidence: low`.
