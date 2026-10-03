# Task taxonomy

Every model profile rates itself against these task types, and the generated
routing table has one row per type. Keep the list short; a routing row that
nobody can tell apart from another is noise.

| id | Task type | What it covers | Width | Must land? |
|---|---|---|---|---|
| `quick-fix` | Narrow, specified change | Files or behaviour named, "Jira ticket to code". Minutes of work. | narrow | yes |
| `feature` | Feature or bug fix that must merge | Find the files, change them, test, PR, address review. Hours. | wide | yes |
| `long-run` | Multi-hour or multi-day autonomous build | Migrations, ports, large refactors, multi-phase plans with no human in the loop. | very wide | yes |
| `frontend` | UI, design, animation, landing pages | Anything a user sees. Taste-sensitive. | any | yes |
| `review` | Independent code review | Second-family review of a diff, PR, or branch. Find what the author missed. | narrow | n/a |
| `investigate` | Root-cause and deep bug hunting | Bugs not visible from reading the code; exhaustive testing and repro. | medium | n/a |
| `analyze` | Codebase comprehension and planning | Audits, decomposition ("how do we split this?"), architecture critique, scoping research. | medium | n/a |
| `bulk` | Mechanical, high-volume work | Clear-spec implementations, data munging, log digging, large-document reading, migrations with no judgment calls. | any | sometimes |
| `research` | External information gathering | Docs, APIs, web, summarisation. Output is a report, not code. | narrow | n/a |
| `computer-use` | Drive a browser or desktop | Verify a running app, click through flows, screenshots, simulators, app setup. | medium | n/a |
| `copy` | User-facing prose | UI text, docs for users, marketing copy. | narrow | yes |
| `3d-games` | 3D, Blender, CAD, game mechanics | Split in profiles: visuals vs feel/controls. | wide | sometimes |
| `prompt-writing` | Writing prompts, skills, agent definitions | Self-prompting and config authoring. Always human-audited. | narrow | n/a |
| `babysit` | Watch a PR to green | Poll CI and review bots, fix real findings, rebase, report or merge per config. | long, narrow | yes |
| `orchestrate` | Lead a multi-agent effort | Plan, spawn, steer, and judge subagents; own the end state. | very wide | yes |

## Width

"Width" is Theo's term: not how hard the task is, but how far it is from
start to end and how many things it touches. Wider tasks need models with a
higher `floor`, because any single dumb step can sink the run and the odds
compound with time.

## Must land?

Tasks whose output ships (merges, is shown to users) weight `taste` and
`floor`. Tasks whose output is information (`review`, `investigate`,
`analyze`, `research`) weight `thoroughness` and `cost_efficiency`, and can
tolerate a noisier model because a human or the orchestrator filters the
result.

## Glossary defaults

These definitions are copied into every user's generated glossary and can be
edited there. They exist because the model needs to know what the user means
by the word, not because the word is obscure.

- **intelligence**: how hard a problem the model can handle unsupervised.
- **taste**: UI/UX quality, code quality, API design, and copy.
- **floor**: how rarely the model does something dumb; consistency over a
  long run. The opposite of "spiky".
- **wide / narrow**: distance from start to finish and number of things
  touched, independent of difficulty.
- **shell out**: call another model or agent from a bash command, one-shot,
  with a self-contained prompt, and read its output back.
- **bridge**: a skill that wraps one specific shell-out (which CLI, which
  flags, how to prompt that model, how to report back).
- **done state**: the checkable condition that ends a delegated task (tests
  pass, PR filed, link or screenshot exists).
- **the out**: the clause in a prompt that tells the model when it may stop
  and ask instead of pushing through.
- **babysit**: watch a PR until every check and reviewer is green, fixing
  real findings and replying to the rest.
- **goal mode**: an autonomous loop that keeps going until a stated condition
  holds. Off by default; enabled per user.
