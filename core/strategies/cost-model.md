# Cost model

Load this when choosing between models on cost, when a user worries about
limits or bills, and when you are tempted to downgrade a task to save money.
The unit of cost is **the completed task**: tokens, steps, retries, cache
behaviour, and the human time before and after the run. List price per token
is a weak predictor of that.

Sources:
- FAB51: "My New Favorite Model", Theo (t3.gg), YouTube, https://youtu.be/r_dw-1109Ag
- OPUS55: "My new favorite model.", Theo (t3.gg), YouTube, https://youtu.be/jgGyX7MPPVg
- SON55: "OpenAI should be scared of this one", Theo (t3.gg), YouTube, https://youtu.be/8WbW_n95wc4
- H55: "finally a good small model", Theo (t3.gg), YouTube, https://youtu.be/38_6C0dkKmU
- OPUSG: "Getting the most out of Opus 5.5", Theo (t3.gg), YouTube, https://youtu.be/ejjBbaq9RmY
- FABG: "So I was using Fable wrong...", Theo (t3.gg), YouTube, https://youtu.be/-XWSJM-Ue-o
- INSP: "A proper guide to Fable 5", Theo (t3.gg), YouTube, https://youtu.be/8GRmLR__OGQ
- FVA: "Fable Vs Astra Debate Is Over", Theo (t3.gg), YouTube, https://youtu.be/P7bxbDSnZRM
- MODELS: "Please stop using stupid models", Theo (t3.gg), YouTube, https://youtu.be/iBrAWpjXNxs
- SOL61: "OpenAI fights back", Theo (t3.gg), YouTube, https://youtu.be/vu8X3YroB-w
- ASTRA: "It's Here.", Theo (t3.gg), YouTube, https://youtu.be/XFWpf0wLbh0

`[KEY m:ss]` links open that video at that timestamp; the auto-generated captions often mishear model names (Sol as "Soul", Fable as "Able", GPT-5.6 as "GBD 56").

All prices are as reported in the research on its dates, or on
Anthropic's pricing page where the Source column says so; the dated numbers in
`core/models/*.md` take precedence.

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
   stops" ([MODELS 19:55](https://youtu.be/iBrAWpjXNxs?t=1195), rule 11).

## 2. Cache economics

Agent loops re-read the whole history on every tool call, so most tokens are
cache reads.

- "Agent workloads are 96% cache reads. So 10 cents for cache reads matters
  more than the $2 and $10 headline prices" (Opus 5.5's analysis of Theo's
  sessions, [SOL61 17:52](https://youtu.be/vu8X3YroB-w?t=1072)).
- Theo's Claude Code usage over one period: 42.8B cached input tokens vs 710M
  uncached; without caching it would have cost "135,000 additional dollars"
  ([FAB51 8:16](https://youtu.be/r_dw-1109Ag?t=496)).
- **Cache writes can dominate the bill on expensive models.** His Fable 5.1
  spend of ~$2,000: cache writes ~$1,200 ("nearly 60%"), output ~$500, cache
  reads $264, uncached input $4 ([FAB51 8:35](https://youtu.be/r_dw-1109Ag?t=515)). "I am
  paying Anthropic more money to manage RAM for me than I am paying them to
  run compute for me" ([FVA 58:30](https://youtu.be/P7bxbDSnZRM?t=3510)).
- **The cache-read share of cost depends on the model's price ratio:** "under
  5% with Fable... closer to 20% with Opus and... like 50 plus with Sonnet"
  ([SON55 10:04](https://youtu.be/8WbW_n95wc4?t=604)). The Sonnet figure was said when its
  cache reads cost $0.20/M; after the October 2026 cut to $0.10/M its share
  is lower (§5).
- **Cache TTL is 5 minutes by default;** longer is "way more expensive"
  ([FAB51 9:58](https://youtu.be/r_dw-1109Ag?t=598)). Single-shot calls with one or two
  tool calls barely benefit from caching.

How to apply:

- 96% is a **token** share, not a dollar share. On cheap-per-token models
  (Sonnet, Sol) cache-read price is the main cost lever. On Fable the lever is
  cache writes. Compare models on their whole cache profile, not input/output
  price.
- **Do not lower compaction thresholds to save money.** More compaction means
  more cache rewriting ([FABG 37:27](https://youtu.be/-XWSJM-Ue-o?t=2247)).
- **Exception:** if a long thread's cache has expired (idle past the TTL),
  compacting before resuming can be cheaper than re-reading hundreds of
  thousands of uncached tokens ([FABG 37:44](https://youtu.be/-XWSJM-Ue-o?t=2264)).
- Bloated system prompts barely matter under cheap cache reads; "it's just
  noise" (Opus's takeaway, [SOL61 18:28](https://youtu.be/vu8X3YroB-w?t=1108)). Keep configs
  minimal for behaviour reasons, not cost (`improvement-loop.md`).
- Keep histories append-only on Claude; editing earlier turns breaks the
  thread's reasoning state ([FAB51 18:20](https://youtu.be/r_dw-1109Ag?t=1100)).

**Source disagreement.** One video says cache reads were ~3% of Theo's Fable
cost, now ~1% ([FVA 58:03](https://youtu.be/P7bxbDSnZRM?t=3483)); his itemised Fable 5.1
spend puts them at $264 of ~$2,000 (~13%) ([FAB51 8:41](https://youtu.be/r_dw-1109Ag?t=521)).
Both agree cache writes are ~60%. The kit treats cache writes as Fable's
dominant cost and does not rely on the exact read share.

## 3. Prices as reported (USD per million tokens)

| Model | Input | Output | Cache read | Cache write | Source |
|---|---|---|---|---|---|
| Claude Fable 5.1 | 10 | 50 | 0.25 | not stated | [FAB51 6:54](https://youtu.be/r_dw-1109Ag?t=414) |
| Claude Opus 5.5 | 4 | 20 | 0.20 | 5 | [OPUS55 4:45](https://youtu.be/jgGyX7MPPVg?t=285); [SON55 8:35](https://youtu.be/8WbW_n95wc4?t=515); Anthropic pricing page, fetched 2026-10-08 |
| Claude Sonnet 5.5 | 2 | 10 | 0.10 (0.20 until October 2026) | 2.50 | [SON55 7:32](https://youtu.be/8WbW_n95wc4?t=452); cut per Anthropic pricing page, fetched 2026-10-08; [H55 4:36](https://youtu.be/38_6C0dkKmU?t=276) |
| Claude Haiku 5.5, prompt ≤ 100K tokens | 0.10 | 0.50 | 0.01 | 0.125 | Anthropic pricing page, fetched 2026-10-08 |
| Claude Haiku 5.5, prompt > 100K tokens | 0.50 | 2.50 | 0.05 | 0.625 | Anthropic pricing page, fetched 2026-10-08 |
| Claude Haiku 4.5 (superseded by Haiku 5.5) | 1 | 5 | 0.10 | 1.25 | Anthropic pricing page; `core/models/claude-haiku-4-5.md` |
| GPT-6 Astra | 10 | 50 | 1.00 | 12.50 | [ASTRA 3:33](https://youtu.be/XFWpf0wLbh0?t=213); [FVA 59:14](https://youtu.be/P7bxbDSnZRM?t=3554) |
| GPT-6.1 Sol | 2 | 10 | 0.10 | not stated | [SOL61 17:40](https://youtu.be/vu8X3YroB-w?t=1060) |

Cache write is the 5-minute price. One-hour writes cost more (Opus $8,
Sonnet $4, Haiku 5.5 $0.20 or $1.00 by tier), and Claude Code wrote only
one-hour entries on Theo's Haiku run ([H55 30:20](https://youtu.be/38_6C0dkKmU?t=1820)).

Modifiers:

- Haiku 5.5 above 100K prompt tokens: 5x every price for that request. The
  prompt length counts all input tokens, including cache reads and cache
  writes, and each request is priced on its own (Anthropic pricing page). It
  is the only current Claude model without flat 1M-context pricing (§10, §11).
- Astra via API above 272K input: 2x input, 1.5x output. Codex is exempt
  ([ASTRA 5:06](https://youtu.be/XFWpf0wLbh0?t=306)).
- OpenAI `fast` mode: ~2x speed at ~2x price ([ASTRA 3:39](https://youtu.be/XFWpf0wLbh0?t=219)).
- OpenAI Flex: half price, no throughput guarantee, not available in Codex
  ([FVA 1:02:17](https://youtu.be/P7bxbDSnZRM?t=3737)). Good for batch jobs that can wait.

## 4. Token efficiency and cost per task

Token use per task varies about 4–10x between models, which swamps list-price
differences.

| Model | Tokens per task | Cost per task | Measure and source |
|---|---|---|---|
| GPT-6 Astra | ~27K | $3.26 | Artificial Analysis (AA), max; [FVA 1:00:47](https://youtu.be/P7bxbDSnZRM?t=3647); [OPUS55 14:11](https://youtu.be/jgGyX7MPPVg?t=851) |
| Claude Fable 5.1 | ~78–80K | $7.60–7.63 | AA; same sources |
| Claude Opus 5.5 | ~120K (max) | ~$6 at max, ~$1.34 at medium | AA; [OPUS55 14:11](https://youtu.be/jgGyX7MPPVg?t=851); [OPUS55 15:17](https://youtu.be/jgGyX7MPPVg?t=917) |
| Claude Sonnet 5.5 | ~272K | — | **Cursor Bench, not AA** (Opus 218K on the same bench); [SON55 17:41](https://youtu.be/8WbW_n95wc4?t=1061) |
| GPT-6.1 Sol | ~110K read per request (vs ~360K for Sonnet) | DeepSWE low $0.21/task | Theo's own runs; [SOL61 19:16](https://youtu.be/vu8X3YroB-w?t=1156) |

The Sonnet and Sol figures come from different measures from the AA rows;
compare within a row's source, not across rows.

What follows from this:

- **Fable is not worth API prices** for most users: "Paying the full API price
  just kind of sounds insane to me" ([FABG 4:21](https://youtu.be/-XWSJM-Ue-o?t=261)).
  Its savings come from agentic, cache-heavy work; do not use it for long
  one-shot generation another model could do ([FAB51 22:13](https://youtu.be/r_dw-1109Ag?t=1333)).
- **Astra is cheap per median task but can burn money at the extremes:** "it
  can often get stuck in a loop and end up spending way more than it should";
  Fable "is at least a bit more likely to stop when it should"
  ([FABG 4:27](https://youtu.be/-XWSJM-Ue-o?t=267)). "I just spent a thousand dollars
  for it to run in a loop and not ship anything"
  ([FVA 1:12:01](https://youtu.be/P7bxbDSnZRM?t=4321)).
- **Sol at low is the price/performance outlier on scoped work:** equal score to
  Opus 5.5 max on DeepSWE at about 1/70 the cost and 1/10 the time
  ([SOL61 21:24](https://youtu.be/vu8X3YroB-w?t=1284)). Its weakness is long unattended loops,
  "but not because of money" ([SOL61 18:34](https://youtu.be/vu8X3YroB-w?t=1114)).

## 5. Why Sonnet's discount is smaller than it looks in long loops

Sonnet 5.5 halves Opus's input, output and cache-write prices. Until October
2026 it did **not** halve the cache-read price: both were $0.20/M
([SON55 8:41](https://youtu.be/8WbW_n95wc4?t=521)). With the Haiku 5.5 launch, Anthropic
cut Sonnet's cache reads to $0.10/M; Opus stays at $0.20/M (Anthropic pricing
page, fetched 2026-10-08; [H55 4:36](https://youtu.be/38_6C0dkKmU?t=276)). Sonnet is now half Opus's price on
every line item. The discount is still smaller than it looks:

- Sonnet uses more tokens (Cursor Bench 272K vs Opus 218K) and more input per
  run (3.5x Opus's input tokens on one game build).
- Faster tokens per second, slower wall-clock: 43 min vs 36 min on the same
  build.
- Before the cut: "I've looked at the numbers for doing like-for-like work
  with opus versus sonnet for real code tasks and sonnet consistently comes
  out as if not more expensive than opus does"
  ([SON55 10:45](https://youtu.be/8WbW_n95wc4?t=645)). That used the old $0.20 price.

Arithmetic for a loop dominated by cache reads. Opus reads 10M cached tokens
at $0.20/M, so it pays $2.00.

| Sonnet's read volume vs Opus | Sonnet reads | Sonnet at $0.20 (before) | Sonnet at $0.10 (now) |
|---|---|---|---|
| 1x | 10M | $2.00 | $1.00 |
| 1.25x (Cursor Bench token ratio) | 12.5M | $2.50 | $1.25 |
| 2x | 20M | $4.00 | $2.00 |
| 3.5x (one game build, input tokens) | 35M | $7.00 | $3.50 |

Break-even moved from 1x to 2x Opus's volume. Below 2x Sonnet is now cheaper;
above it Opus is. On the evidence (1.25x to 3.5x), like-for-like loops land at
roughly Opus's cost rather than above it, and Opus finishes sooner with a
stronger result. This is inference from list prices and pre-cut token data;
the research has no like-for-like run since the cut. Theo's chart after
Artificial Analysis repriced Sonnet: it "shifted quite a bit to the left...
Sonnet feels less bad now by quite a bit" ([H55 19:14-19:30](https://youtu.be/38_6C0dkKmU?t=1154)), yet on the
Anthropic Pareto line "it offers nothing now. Maybe just barely on high"
([H55 37:37](https://youtu.be/38_6C0dkKmU?t=2257)).

Rule: use Sonnet for **short, bounded investigations** (about 5 minutes on
Theo's decomposition bench, at about half Opus's cost) and as a cheap wrapper
(`parallelism.md` §8). Do not route long implementation loops to it to save
money: the saving is small and uncertain, and the wall clock is worse. The
same logic warned Theo's older roster: "Sonnet 5 is so token hungry that Opus
48 is often cheaper" ([INSP 17:40](https://youtu.be/8GRmLR__OGQ?t=1060)).

## 6. The naive-router failure

Do not route by a context-free "cheapest model that can probably do it"
classifier. OpenRouter's cost router ([SOL61 19:42](https://youtu.be/vu8X3YroB-w?t=1182)):

- Sent ~60% of requests to a cheap flash model.
- Ended **more expensive** than GPT-6 Astra on `low`.
- Took 20 minutes vs 4.6 minutes per task, and **104 steps vs 19**.
- GPT-6.1 Sol on `low` got the same score for 1/8 the price.

"A model that cannot reason, that is given a prompt and no context, cannot
make a good decision around how hard the problem is." Route by task type and
context, using the routing table, and count steps-to-completion. "Sometimes
the cheaper model ends up more expensive" ([MODELS 19:19](https://youtu.be/iBrAWpjXNxs?t=1159),
rule 10).

## 7. Scores are defaults, not limits

Theo's CLAUDE.md scored each model 1–10 on **cost**, **intelligence**, and
**taste**, with his own definitions in a glossary ([INSP 16:51](https://youtu.be/8GRmLR__OGQ?t=1011)):

- **intelligence:** how hard a problem the model can handle unsupervised.
- **taste:** UI/UX, code quality, API design, and copy.
- **cost:** how cheap it is *to him*, including subscription headroom. He gave
  GPT-5.5 a cost of 9 because his Codex usage felt "basically infinite".

His roster, in words (older models, [INSP 17:26](https://youtu.be/8GRmLR__OGQ?t=1046)): GPT-5.5 "intelligent, no taste";
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
| Read logs, giant PDFs/specs, codebase deep dives | Token-efficient or subscription-cheap model via shell-out or Sonnet subagent; Haiku 5.5 subagents for bounded, verifiable gathering (§11) | Token-heavy, output is information ([INSP 10:38](https://youtu.be/8GRmLR__OGQ?t=638); [SON55 24:16](https://youtu.be/8WbW_n95wc4?t=1456)) |
| Computer use over many screenshots | Strongest computer-use model on the most generous subscription | Hundreds of screenshots per hour ([INSP 10:50](https://youtu.be/8GRmLR__OGQ?t=650)) |
| Review and investigation | Second-family, token-efficient model (e.g. Sol) | Finds more per dollar; noise is filtered (`verification-and-review.md`) |
| Implementation that must merge | Highest-floor, highest-taste model available | Fewer follow-ups: Fable 2 vs Astra 6 per PR ([FVA 33:40](https://youtu.be/P7bxbDSnZRM?t=2020)) |
| Rescue a looping cheap run | Highest-floor model, "make this actually land" | Stop the burn ([FVA 39:43](https://youtu.be/P7bxbDSnZRM?t=2383)) |

Theo's result with this split: a 5.5-hour Fable loop plus all the models it
called came to "around 150 bucks" of usage, inside two subscriptions, neither
above 40% weekly; the Codex one around 15% ([INSP 7:22](https://youtu.be/8GRmLR__OGQ?t=442); [INSP 11:15](https://youtu.be/8GRmLR__OGQ?t=675)).

Time-cost framing for the user: "my time is more valuable than Fable's"
([MODELS 19:47](https://youtu.be/iBrAWpjXNxs?t=1187)); "If Julius can be three times more
productive by spending his salary in tokens, that's a no-brainer"
([MODELS 10:38](https://youtu.be/iBrAWpjXNxs?t=638)).

## 9. Subscriptions vs API

API-equivalent value of the $200/month plans, as Theo estimated them:

| | Claude $200 | Codex $200 |
|---|---|---|
| Monthly value | ~$8K ([FAB51 6:41](https://youtu.be/r_dw-1109Ag?t=401)); ~$2,300/week, "almost 10 grand a month" ([SON55 29:32](https://youtu.be/8WbW_n95wc4?t=1772)); $8–9K ([SOL61 6:40](https://youtu.be/vu8X3YroB-w?t=400)) | ~$12K ([FVA 1:03:52](https://youtu.be/P7bxbDSnZRM?t=3832)); "over $12K" ([SOL61 6:46](https://youtu.be/vu8X3YroB-w?t=406)); "like 14 grand" ([INSP 15:10](https://youtu.be/8GRmLR__OGQ?t=910)) |
| Frontier-model cap | Fable limited to **50% of the weekly limit** ([FABG 4:09](https://youtu.be/-XWSJM-Ue-o?t=249)) | None stated |
| 5-hour limit | Yes; each window ≈ 40% of the Fable allowance ([FVA 1:06:58](https://youtu.be/P7bxbDSnZRM?t=4018)). Raised in the Opus 5.5 era ([OPUS55 38:44](https://youtu.be/jgGyX7MPPVg?t=2324)) | None on $100/$200 tiers |
| Resets | Rare | Frequent: "eight free resets in the last 30 days", plus banked resets ([FVA 1:09:02](https://youtu.be/P7bxbDSnZRM?t=4142)) |

Caveats to state when advising a user:

- These numbers move. The Sol 6.1 video reports a new Codex accounting that
  "will net out at half the dollar in API spend compared to the old pro $200
  plan" ([SOL61 6:09](https://youtu.be/vu8X3YroB-w?t=369)), and Theo calls it possibly "the
  start of the end of the subsidization era". Treat the Codex figure as an
  upper bound and let the user's own usage data override it.
- Theo admits a bias: OpenAI early access did not count against his usage
  ([FVA 26:49](https://youtu.be/P7bxbDSnZRM?t=1609)).
- Light users: "a few hours a day, two to three days a week... not using a lot
  of sub agents, you can probably get by on a single $200 plan" (Claude); most
  devs can get by on Codex $200 "when used responsibly".

Routing implications (the generator reads these from the user's config):

- **Protect the scarce pool.** On Claude subscriptions, spend the non-Fable
  half on work that does not need Fable. "The things I'd use low for I'm just
  going to deal with Opus for if I'm really trying to maximize my usage of the
  subs" ([FABG 8:04](https://youtu.be/-XWSJM-Ue-o?t=484)). With Opus 5.5 that pool is
  now a capable default, not a wasted "Opus pot"
  ([FVA 1:04:26](https://youtu.be/P7bxbDSnZRM?t=3866); [SON55 0:00](https://youtu.be/8WbW_n95wc4?t=0)).
- **Lean on the generous pool** for token-heavy reading, review, and computer
  use.
- **On API billing**, weight token efficiency heavily and avoid Fable for work
  another model can do.

## 10. Hidden multipliers to guard against

| Multiplier | Effect | Guard |
|---|---|---|
| `max` effort | ~13x cost, ~15x tokens for +1 point ([OPUSG 13:40](https://youtu.be/ejjBbaq9RmY?t=820)) | Never use it. |
| `fast` mode | ~2x price | Off for orchestrated work. |
| Unbounded fan-out (`ultra`, `ultracode`) | Many parallel agents | Use deliberately (`parallelism.md`). |
| Unintended expensive subagent | Opus spawned a Fable subagent ([SON55 26:32](https://youtu.be/8WbW_n95wc4?t=1592)) | Pin subagent models. |
| Looping runs | Astra death loops; review-bot fix loops | Cap babysit rounds; hand off to a higher-floor model. |
| Long context via API (Astra) | 2x input / 1.5x output above 272K | Prefer Codex for long Astra sessions. |
| Retry after `low` fails | Pays twice | Use `high` for work that must land. |
| Haiku 5.5 prompt over 100K tokens | 5x every price for that request; the threshold counts cache reads and writes. 47 of 51 requests on Theo's Haiku game build crossed it ([H55 30:26](https://youtu.be/38_6C0dkKmU?t=1826)) | Cap the autocompact window near 100K or split the input (§11). |

## 11. Haiku 5.5 and small models

**History.** Theo's older roster ([INSP 19:00](https://youtu.be/8GRmLR__OGQ?t=1140), recorded in the Fable 5 / GPT-5.5 /
Opus 4.8 era, before Haiku 5.5 shipped in October 2026) said: "Never use
haiku. Just don't at this point. It's not useful for anything real,
especially with [GPT-5.5] being effectively free". That was about Haiku 4.5,
which the research never evaluated and which Haiku 5.5 now supersedes
(`core/models/claude-haiku-4-5.md`). In the Haiku 5.5 video he still calls
Haiku 4.5 "useless" ([H55 0:31](https://youtu.be/38_6C0dkKmU?t=31)).

**Haiku 5.5** shipped about 2026-10-07 at $0.10 / $0.50 per M in/out for
prompts up to 100K tokens, and 5x that above (§3). Theo: "Anthropic now has
one small model that is sometimes worth using" ([H55 40:16](https://youtu.be/38_6C0dkKmU?t=2416)). Its best use is
"letting your agents use it and letting your applications use it", not
picking it by hand ([H55 22:00](https://youtu.be/38_6C0dkKmU?t=1320)). "Coding is not what makes LLMs expensive...
Your costs come from everything else" ([H55 31:29-31:46](https://youtu.be/38_6C0dkKmU?t=1889)): gathering context, vetting
a theory, reading docs. That is the work Haiku can take. Executing the plan
stays with the smart model. Full profile: `core/models/claude-haiku-5-5.md`.

**Kit rule:** route Haiku 5.5 only as a subagent for bounded, verifiable
work: file search, data gathering, categorisation, reading docs, and tasks
where many attempts with cheap programmatic verification beat one careful
attempt. Never as a primary model, never for work that must land, never as
the merge-gate reviewer.

Required guardrails in every Haiku prompt:

1. **Reasoning on, never off.** Anthropic has "trained their models to be bad
   at that... you always have to let it reason at least a little bit"
   ([H55 10:23-11:25](https://youtu.be/38_6C0dkKmU?t=623)). ThePrimeagen swapped GPT-6 Luna for Haiku 5.5 with
   reasoning off and got a worse pass rate, more failures and slower runs.
   For reasoning-off categorisation, use OpenAI's cheap model instead unless
   vision is needed.
2. **Keep each request's prompt under about 100K tokens.** Above that every
   price is 5x, and the threshold counts cache reads. Cap the autocompact
   window (Claude Code's `/autocompact` accepts 100K to 1M; an Anthropic
   employee said it is saved per model, unverified, [H55 8:31-8:55](https://youtu.be/38_6C0dkKmU?t=511)) or split the
   input across more subagents. On Theo's game build 47 of 51 requests
   crossed it ([H55 30:26](https://youtu.be/38_6C0dkKmU?t=1826)).
3. **Make "cannot", "rate-limited" and "nothing found" valid returns, and
   forbid self-waiting loops.** On camera it hit GitHub's rate limit, saved
   the error bodies as data, then said it would wait for the reset and never
   resumed. The thread was dead until Theo stepped in, and his GitHub
   integration was locked out for about 50 minutes ([H55 33:46-34:56](https://youtu.be/38_6C0dkKmU?t=2026)).
4. **Verify outputs programmatically or with a stronger model. Never accept
   CI status as an audit.** The same run called PRs "merge ready" because the
   GitHub checks were green; "it didn't seem to audit them thoroughly itself"
   ([H55 30:47-30:55](https://youtu.be/38_6C0dkKmU?t=1847)).

**Cost inversion.** "If Opus can solve a problem in 100k tokens and Haiku
burns a million before it figures out it can't, Haiku ends up more
expensive" ([H55 36:23-36:48](https://youtu.be/38_6C0dkKmU?t=2183)). A cheap per-token price does not make a failing run
cheap. If Haiku is not converging on a bounded task, stop it and give the
task to a stronger model (§1, rule 1).

**Many attempts.** Haiku pays off "for the subset of tasks where more
attempts is more valuable than smart attempts, where you'd rather try 10
times and verify each result" ([H55 23:34-24:06](https://youtu.be/38_6C0dkKmU?t=1414)). Theo calls this "a small
subset of work". Anthropic's egg-drop demo (one run, vendor numbers): Opus
5.5 alone took 3 min 37 s, made 25 attempts and cost $0.47. Opus 5.5 leading
10 Haiku 5.5 subagents took 58 s, made 86 attempts and cost $0.14
([H55 22:17-23:20](https://youtu.be/38_6C0dkKmU?t=1337)). The rule only holds when each attempt can be checked
cheaply.

**Subscription credit (reported, unverified).** Max plans reportedly include
a monthly programmatic-use credit: $100 on Max 5x and $200 on Max 20x
([H55 20:12-20:36](https://youtu.be/38_6C0dkKmU?t=1212); a secondary report says it covers the Agent SDK, `claude -p`,
Claude Code GitHub Actions and third-party apps, billed at API rates). If so,
`claude -p` bridge calls (`core/bridges/claude-cli.md`) may draw from that
credit rather than plan quota. Verify this in the account before relying
on it.

Before routing real work to Haiku 5.5 or any other new small model, run it
through the re-baseline procedure (`improvement-loop.md` §6) on bounded tasks
first. Effort for Haiku subagents: `effort-levels.md` §3.

## 12. Spreading load across accounts

Some heavy users split traffic across several subscriptions with a local proxy
(Theo's "Vibe Proxy" auto-splits across accounts and uses the API-key mode of
Claude Code, losing some built-in features; [INSP 42:20](https://youtu.be/8GRmLR__OGQ?t=2540); [FVA 1:07:12](https://youtu.be/P7bxbDSnZRM?t=4032)). This kit mentions it only so you can
recognise the setup in a user's config. It does not endorse it. Check the
provider's terms before suggesting it, and never set it up unasked.
