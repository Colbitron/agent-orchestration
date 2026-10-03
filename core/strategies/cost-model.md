# Cost model

Load this when choosing between models on cost, when a user worries about
limits or bills, and when you are tempted to downgrade a task to save money.
The unit of cost is **the completed task**: tokens, steps, retries, cache
behaviour, and the human time before and after the run. List price per token
is a weak predictor of that.

Citations: `research/<file>.md § V1.3` means Video 1, section 3 of that file;
`§ X` means its cross-video synthesis. `INSP` means
`transcripts/general/agent-orchestration-inspiration.html` (recorded in the
Fable 5 / GPT-5.5 / Opus 4.8 era). All prices are as reported in the research
on its dates; the dated numbers in `core/models/*.md` take precedence.

---

## 1. Rules

1. **Judge the output, not the price tag.** Escalate without asking when a
   cheaper model misses the bar (§7).
2. **Cheap models explore; expensive models ship.** Gather information, try
   approaches, review and verify on cheap or subsidised models; move work that
   must land to the highest-floor model (§8).
3. **Compare cost per completed task**, which is driven by token efficiency,
   step count, and cache pricing (§2–§4).
4. **Subscriptions change everything.** On a generous subscription a model is
   "effectively free" until its quota bites; the user's config says which
   access they have (§5).
5. **Never optimise by turning effort up or down blindly.** `max` multiplies
   cost for nothing; `low` that fails costs a retry (`effort-levels.md`).
6. **Human time is the most expensive input.** "If I downgrade to a cheaper
   model I have to put more time in before it fires and more time in when it
   stops" (`research/model-selection.md § V1.3`, rule 11).

## 2. Cache economics

Agent loops re-read the whole history on every tool call, so most tokens are
cache reads.

- "Agent workloads are 96% cache reads. So 10 cents for cache reads matters
  more than the $2 and $10 headline prices" (Opus 5.5's analysis of Theo's
  sessions, `research/gpt-releases.md § V2.4`).
- Theo's Claude Code usage over one period: 42.8B cached input tokens vs 710M
  uncached; without caching it would have cost "135,000 additional dollars"
  (`research/claude-releases.md § V1.4`).
- **Cache writes can dominate the bill on expensive models.** His Fable 5.1
  spend of ~$2,000: cache writes ~$1,200 ("nearly 60%"), output ~$500, cache
  reads $264, uncached input $4 (`research/claude-releases.md § V1.4`). "I am
  paying Anthropic more money to manage RAM for me than I am paying them to
  run compute for me" (`research/model-selection.md § V2.7`).
- **The cache-read share of cost depends on the model's price ratio:** "under
  5% with Fable... closer to 20% with Opus and... like 50 plus with Sonnet"
  (`research/claude-releases.md § V3.3`).
- **Cache TTL is 5 minutes by default;** longer is "way more expensive"
  (`research/claude-releases.md § V1.4`). Single-shot calls with one or two
  tool calls barely benefit from caching.

How to apply:

- 96% is a **token** share, not a dollar share. On cheap-per-token models
  (Sonnet, Sol) cache-read price is the main cost lever. On Fable the lever is
  cache writes. Compare models on their whole cache profile, not input/output
  price.
- **Do not lower compaction thresholds to save money.** More compaction means
  more cache rewriting (`research/claude-supplemental.md § V2.4`).
- **Exception:** if a long thread's cache has expired (idle past the TTL),
  compacting before resuming can be cheaper than re-reading hundreds of
  thousands of uncached tokens (`research/claude-supplemental.md § V2.4`).
- Bloated system prompts barely matter under cheap cache reads; "it's just
  noise" (Opus's takeaway, `research/gpt-releases.md § V2.4`). Keep configs
  minimal for behaviour reasons, not cost (`improvement-loop.md`).
- Keep histories append-only on Claude; editing earlier turns breaks the
  thread's reasoning state (`research/claude-releases.md § V1.3`).

**Source disagreement.** One video says cache reads were ~3% of Theo's Fable
cost, now ~1% (`research/model-selection.md § V2.7`); his itemised Fable 5.1
spend puts them at $264 of ~$2,000 (~13%) (`research/claude-releases.md § V1.4`).
Both agree cache writes are ~60%. The kit treats cache writes as Fable's
dominant cost and does not rely on the exact read share.

## 3. Prices as reported (USD per million tokens)

| Model | Input | Output | Cache read | Cache write | Source |
|---|---|---|---|---|---|
| Claude Fable 5.1 | 10 | 50 | 0.25 | not stated | `research/claude-releases.md § V1.4` |
| Claude Opus 5.5 | 4 | 20 | 0.20 | 5 | `research/claude-releases.md § V2.4, § V3.4` |
| Claude Sonnet 5.5 | 2 | 10 | 0.20 | 2.50 | `research/claude-releases.md § V3.4` |
| GPT-6 Astra | 10 | 50 | 1.00 | 12.50 | `research/gpt-releases.md § V1.4`; `research/model-selection.md § V2.7` |
| GPT-6.1 Sol | 2 | 10 | 0.10 | not stated | `research/gpt-releases.md § V2.4` |

Modifiers:

- Astra via API above 272K input: 2x input, 1.5x output. Codex is exempt
  (`research/gpt-releases.md § V1.4`).
- OpenAI `fast` mode: ~2x speed at ~2x price (`research/gpt-releases.md § V1.4`).
- OpenAI Flex: half price, no throughput guarantee, not available in Codex
  (`research/model-selection.md § V2.7`). Good for batch jobs that can wait.

## 4. Token efficiency and cost per task

Token use per task varies about 4–10x between models, which swamps list-price
differences.

| Model | Tokens per task | Cost per task | Measure and source |
|---|---|---|---|
| GPT-6 Astra | ~27K | $3.26 | Artificial Analysis (AA), max; `research/model-selection.md § V2.2`; `research/claude-releases.md § V2.3` |
| Claude Fable 5.1 | ~78–80K | $7.60–7.63 | AA; same sources |
| Claude Opus 5.5 | ~120K (max) | ~$6 at max, ~$1.34 at medium | AA; `research/claude-releases.md § V2.3, § V2.4` |
| Claude Sonnet 5.5 | ~272K | — | **Cursor Bench, not AA** (Opus 218K on the same bench); `research/claude-releases.md § V3.3` |
| GPT-6.1 Sol | ~110K read per request (vs ~360K for Sonnet) | DeepSWE low $0.21/task | Theo's own runs; `research/gpt-releases.md § V2.2` |

The Sonnet and Sol figures come from different measures from the AA rows;
compare within a row's source, not across rows.

What follows from this:

- **Fable is not worth API prices** for most users: "Paying the full API price
  just kind of sounds insane to me" (`research/claude-supplemental.md § V2.4`).
  Its savings come from agentic, cache-heavy work; do not use it for long
  one-shot generation another model could do (`research/claude-releases.md § V1.8`).
- **Astra is cheap per median task but can burn money at the extremes:** "it
  can often get stuck in a loop and end up spending way more than it should";
  Fable "is at least a bit more likely to stop when it should"
  (`research/claude-supplemental.md § V2.4`). "I just spent a thousand dollars
  for it to run in a loop and not ship anything"
  (`research/model-selection.md § V2.1`).
- **Sol at low is the price/performance outlier on scoped work:** equal score to
  Opus 5.5 max on DeepSWE at about 1/70 the cost and 1/10 the time
  (`research/gpt-releases.md § V2.2`). Its weakness is long unattended loops,
  "but not because of money" (`research/gpt-releases.md § V2.4`).

## 5. Why Sonnet is not cheaper than Opus in long loops

Sonnet 5.5 halves Opus's input, output and cache-write prices but **not the
cache-read price** ($0.20 for both) (`research/claude-releases.md § V3.3`).

- In agent loops cache reads dominate, so the discount mostly disappears.
- Sonnet uses more tokens (Cursor Bench 272K vs Opus 218K) and more input per
  run (3.5x Opus's input tokens on one game build).
- "I've looked at the numbers for doing like-for-like work with opus versus
  sonnet for real code tasks and sonnet consistently comes out as if not more
  expensive than opus does" (`research/claude-releases.md § V3.3`).
- Faster tokens per second, slower wall-clock: 43 min vs 36 min on the same
  build.

Rule: use Sonnet for **short, bounded investigations** (about 5 minutes on
Theo's decomposition bench, at about half Opus's cost) and as a cheap wrapper
(`parallelism.md` §8). Do not route long implementation loops to it to save
money. The same logic warned Theo's older roster: "Sonnet 5 is so token hungry
that Opus 48 is often cheaper" (INSP).

## 6. The naive-router failure

Do not route by a context-free "cheapest model that can probably do it"
classifier. OpenRouter's cost router (`research/gpt-releases.md § V2.6`):

- Sent ~60% of requests to a cheap flash model.
- Ended **more expensive** than GPT-6 Astra on `low`.
- Took 20 minutes vs 4.6 minutes per task, and **104 steps vs 19**.
- GPT-6.1 Sol on `low` got the same score for 1/8 the price.

"A model that cannot reason, that is given a prompt and no context, cannot
make a good decision around how hard the problem is." Route by task type and
context, using the routing table, and count steps-to-completion. "Sometimes
the cheaper model ends up more expensive" (`research/model-selection.md § V1.3`,
rule 10).

## 7. Scores are defaults, not limits

Theo's CLAUDE.md scored each model 1–10 on **cost**, **intelligence**, and
**taste**, with his own definitions in a glossary (INSP):

- **intelligence:** how hard a problem the model can handle unsupervised.
- **taste:** UI/UX, code quality, API design, and copy.
- **cost:** how cheap it is *to him*, including subscription headroom. He gave
  GPT-5.5 a cost of 9 because his Codex usage felt "basically infinite".

His roster, in words (older models, INSP): GPT-5.5 "intelligent, no taste";
Sonnet 5 "not much cheaper, much less intelligent, slightly more taste"; Opus
4.8 more intelligent, "way higher taste"; Fable "the cost sucks, intelligence
is best in class and taste is also best in class". Rules attached:

- Bulk mechanical work (clear-spec implementations, data analysis, migrations)
  → the subsidised GPT model, "effectively free".
- Anything user-facing (UI, copy, API design) needs taste above 7.

The kit's generated routing table uses more axes (see `docs/ARCHITECTURE.md`)
and treats cost as a per-user input. It keeps Theo's standing rule verbatim:

```
These are defaults, not limits. You have standing permission to override
them. If a cheaper model's outputs don't meet the bar, rerun or redo the work
with a smarter model without asking. Judge the output, not the price tag.
Escalating costs less than shipping mediocre work.
```

And his correction of the model-written cost clause, which replaced "cost is
a tiebreaker only when axes conflict":

```
Don't let cost prevent you from using the right model for the job. Instead,
take advantage of cheaper options to get more information and try things
before moving the work to a more expensive option.
```

## 8. Explore cheap, ship expensive

| Phase | Route to | Why |
|---|---|---|
| Read logs, giant PDFs/specs, codebase deep dives | Token-efficient or subscription-cheap model via shell-out or Sonnet subagent | Token-heavy, output is information (INSP; `research/claude-releases.md § V3.6`) |
| Computer use over many screenshots | Strongest computer-use model on the most generous subscription | Hundreds of screenshots per hour (INSP) |
| Review and investigation | Second-family, token-efficient model (e.g. Sol) | Finds more per dollar; noise is filtered (`verification-and-review.md`) |
| Implementation that must merge | Highest-floor, highest-taste model available | Fewer follow-ups: Fable 2 vs Astra 6 per PR (`research/model-selection.md § V2.4`) |
| Rescue a looping cheap run | Highest-floor model, "make this actually land" | Stop the burn (`research/model-selection.md § V2.3`) |

Theo's result with this split: a 5.5-hour Fable loop plus all the models it
called came to "around 150 bucks" of usage, inside two subscriptions, neither
above 40% weekly; the Codex one around 15% (INSP).

Time-cost framing for the user: "my time is more valuable than Fable's"
(`research/model-selection.md § V1.1`); "If Julius can be three times more
productive by spending his salary in tokens, that's a no-brainer"
(`research/model-selection.md § V1.7`).

## 9. Subscriptions vs API

API-equivalent value of the $200/month plans, as Theo estimated them:

| | Claude $200 | Codex $200 |
|---|---|---|
| Monthly value | ~$8K (`research/claude-releases.md § V1.4`); ~$2,300/week, "almost 10 grand a month" (`§ V3.4`); $8–9K (`research/gpt-releases.md § V2.4`) | ~$12K (`research/model-selection.md § V2.7`); "over $12K" (`research/gpt-releases.md § V2.4`); "like 14 grand" (INSP) |
| Frontier-model cap | Fable limited to **50% of the weekly limit** (`research/claude-supplemental.md § V2.4`) | None stated |
| 5-hour limit | Yes; each window ≈ 40% of the Fable allowance (`research/model-selection.md § V2.7`). Raised in the Opus 5.5 era (`research/claude-releases.md § V2.4`) | None on $100/$200 tiers |
| Resets | Rare | Frequent: "eight free resets in the last 30 days", plus banked resets (`research/model-selection.md § V2.7`) |

Caveats to state when advising a user:

- These numbers move. The Sol 6.1 video reports a new Codex accounting that
  "will net out at half the dollar in API spend compared to the old pro $200
  plan" (`research/gpt-releases.md § V2.4`), and Theo calls it possibly "the
  start of the end of the subsidization era". Treat the Codex figure as an
  upper bound and let the user's own usage data override it.
- Theo admits a bias: OpenAI early access did not count against his usage
  (`research/model-selection.md § V2.7`).
- Light users: "a few hours a day, two to three days a week... not using a lot
  of sub agents, you can probably get by on a single $200 plan" (Claude); most
  devs can get by on Codex $200 "when used responsibly".

Routing implications (the generator reads these from the user's config):

- **Protect the scarce pool.** On Claude subscriptions, spend the non-Fable
  half on work that does not need Fable. "The things I'd use low for I'm just
  going to deal with Opus for if I'm really trying to maximize my usage of the
  subs" (`research/claude-supplemental.md § V2.4`). With Opus 5.5 that pool is
  now a capable default, not a wasted "Opus pot"
  (`research/model-selection.md § V2.2`; `research/claude-releases.md § V3.1`).
- **Lean on the generous pool** for token-heavy reading, review, and computer
  use.
- **On API billing**, weight token efficiency heavily and avoid Fable for work
  another model can do.

## 10. Hidden multipliers to guard against

| Multiplier | Effect | Guard |
|---|---|---|
| `max` effort | ~13x cost, ~15x tokens for +1 point (`research/claude-supplemental.md § V1.4`) | Never use it. |
| `fast` mode | ~2x price | Off for orchestrated work. |
| Unbounded fan-out (`ultra`, `ultracode`) | Many parallel agents | Use deliberately (`parallelism.md`). |
| Unintended expensive subagent | Opus spawned a Fable subagent (`research/claude-releases.md § V3.6`) | Pin subagent models. |
| Looping runs | Astra death loops; review-bot fix loops | Cap babysit rounds; hand off to a higher-floor model. |
| Long context via API (Astra) | 2x input / 1.5x output above 272K | Prefer Codex for long Astra sessions. |
| Retry after `low` fails | Pays twice | Use `high` for work that must land. |

## 11. Haiku and other unevaluated models

Theo's roster said: "Never use haiku. Just don't at this point. It's not
useful for anything real, especially with [GPT-5.5] being effectively free"
(INSP). None of the research evaluates Haiku 4.5, and Haiku 5.5 was only
announced as "coming in the next few weeks" for "high volume and cost-sensitive
applications" (`research/claude-releases.md` transcription notes, § V2.4).

**Kit rule:** do not route real work to Haiku by default. Treat that as a
missing-evidence default, not a measured verdict. If the user wants to try a
new small model, run it through the re-baseline procedure
(`improvement-loop.md` §6) on bounded tasks first.

## 12. Spreading load across accounts

Some heavy users split traffic across several subscriptions with a local proxy
(Theo's "Vibe Proxy" auto-splits across accounts and uses the API-key mode of
Claude Code, losing some built-in features; INSP;
`research/model-selection.md § V2.6`). This kit mentions it only so you can
recognise the setup in a user's config. It does not endorse it. Check the
provider's terms before suggesting it, and never set it up unasked.
