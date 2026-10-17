# Maintaining the kit

This is the runbook for keeping the kit current. It is built from the Haiku 5.5
update of 2026-10-08. That update added one transcript, changed 13 files in
the repo, and changed the user's config. Paths are relative to the repo root unless they start with `~`.

Background reading: `core/models/_schema.md` (profile format),
`core/strategies/improvement-loop.md` §6 (re-baseline) and §9 (distributing
changes).

## 1. A new model ships

Work through the list in order. Each step names the files the Haiku 5.5 drop
touched.

**Capture evidence**

- [ ] Save the source. Video transcripts are not committed to this repo:
  they are a copy of someone else's work. Keep them in the private
  companion repo (`agent-orchestration-sources`, same layout:
  `transcripts/<vendor>/releases/<model-id>.html` plus the cleaned
  `transcripts/txt/<model-id>.txt`) and cite the public video with a
  timestamp instead. Web research goes straight into the digest under
  `research/`.
- [ ] Verify every price against the vendor's pricing page. Write the fetch
  date next to the number. Speakers misread prices, and captions mishear them.
- [ ] Read timestamps from the transcript. Never estimate one. If a quote has
  no timestamp you can find, cite it without one.
- [ ] Note what is vendor-reported, secondhand or untested. Those notes carry
  into the profile's `confidence`.

**Write the profiles**

- [ ] Create `core/models/<model-id>.md` per `core/models/_schema.md`: all
  frontmatter keys, the body sections in schema order, and a score rationale
  table. Set `as_of` to today and `confidence` honestly. Put pricing tiers or
  quirks in `notes_on_cost` (today: Haiku's 5x price above 100K prompt tokens).
  The session-start check compares `as_of` dates to the routing stamp, so a
  profile edit without an `as_of` bump is invisible to users.
- [ ] Mark the superseded profile (today: `core/models/claude-haiku-4-5.md`):
  `status: deprecated` with a comment naming the successor, bump `as_of`,
  point `role_hints.as_primary` and the summary at the new file. Keep its
  history; do not delete the file.

**Update the research digests**

- [ ] Add a section for the new source in the digest's fixed format.
  `research/claude-releases.md` uses eight parts per video: subject and
  thesis; strengths; weaknesses; pricing, speed, context and limits;
  prompting; subagents and orchestration; Claude Code specifics; routing
  implications. `research/gpt-releases.md` has its own sections; match the
  file you are adding to.
- [ ] Update the digest header (source list) and the transcription notes
  (new mishearings).
- [ ] Add the model as a column or row in the synthesis table at the end of
  the digest.
- [ ] Where the new facts change a historical claim, append a dated note:
  `[Update YYYY-MM-DD: what changed; see [H55 12:34](https://youtu.be/38_6C0dkKmU?t=754).]`. Never rewrite or delete
  the old claim. The record of what was true when matters for later audits.
- [ ] In `research/model-gaps.md`, update the naming corrections table, the
  at-a-glance table, the model's numbered section, and the suggested
  shortlist. Bump the dated line at the top.

**Sweep for claims the new facts change**

- [ ] `core/strategies/cost-model.md`: the price table (§3), every section
  that reasons from an old number (today §2, §5, §8, §11), and the hidden
  multipliers table (§10).
- [ ] `core/strategies/effort-levels.md`: the per-model defaults table (§3)
  and the conflicts section (§6) if the new model's evidence disagrees with
  a kit rule.
- [ ] `core/strategies/parallelism.md`: fan-out guidance if the model changes
  what is cheap to run wide (today: a new subsection in §3).
- [ ] Sibling profiles whose claims changed. Today: `claude-sonnet-5-5.md`
  (pricing block, `notes_on_cost`, task notes, `cost_efficiency`),
  `claude-opus-5-5.md` and `gpt-6-luna.md` (cross-references). Bump `as_of`
  on each one you edit.
- [ ] `core/interview/config-schema.md`: the example `models:` block names
  model ids.
- [ ] `agents/analyst.md` and `agents/bridge-runner.md`: check the pinned
  `model:` still fits.
- [ ] Bridge `reaches:` lists in `core/bridges/*.md`. Today:
  `claude-cli.md`, `cursor-cli.md`, `t3-code-mcp.md`. Also fix alias notes
  (the `haiku` alias in `claude-cli.md` now resolves to Haiku 5.5).
- [ ] The user's `~/.agent-orchestration/config.yaml` `models:` block: add
  the new id, disable the superseded one, add a comment on any guessed `cost`.

Grep for the usual stale spots. Set the two variables first.

```sh
OLD=claude-haiku-4-5        # the superseded model id
OLD_PRICE='0.20'            # a price that changed, as written in the docs
# 1. Every mention of the old id outside transcripts
grep -rn --exclude-dir=.git --exclude-dir=transcripts -e "$OLD" .
# 2. Claims that were true before the release
grep -rn -i -E 'unreleased|not yet (released|shipped|digested)|announced|coming in the next' \
  core skills adapters agents hooks docs README.md
# 3. The old price next to the field it belonged to (adjust "cache.read")
grep -rn -i 'cache.read' core research | grep -F "$OLD_PRICE"
# 4. Bridges that reach a missing profile, or a deprecated one
grep -ho '^reaches: \[[^]]*\]' core/bridges/*.md | sed 's/reaches: //' | tr -d '[] ' \
  | tr ',' '\n' | sort -u | while read -r id; do
    [ -n "$id" ] && [ ! -f "core/models/$id.md" ] && echo "no profile: $id"; done
for f in $(grep -l '^status: deprecated' core/models/*.md); do
  grep -l "^reaches:.*$(basename "$f" .md)" core/bridges/*.md; done
# 5. Oldest as_of dates first
grep -n '^as_of:' core/models/*.md core/bridges/*.md | sort -t: -k4
```

Hits in dated `[Update ...]` notes and in the deprecated profile's history
are expected. Everything else is a candidate edit.

**Re-baseline, then ship**

- [ ] Run the re-baseline procedure in `core/strategies/improvement-loop.md`
  §6 before trusting the new `tasks:` fits: the failed-prompt set, wider
  prompts, effort checks. Until then, keep `confidence` at medium or low.
- [ ] Release (section 3), then refresh the routing table (section 4).

## 2. A price or API fact changes

Example: at the Haiku 5.5 launch Anthropic cut Sonnet 5.5 cache reads from
$0.20 to $0.10 per million tokens.

- [ ] Verify the new value on the vendor's pricing page and note the date.
- [ ] Profile (`core/models/claude-sonnet-5-5.md`): the `pricing_per_mtok`
  block, `notes_on_cost`, any task note or score that reasoned from the old
  number, the cost notes section, and `as_of`.
- [ ] `core/strategies/cost-model.md`: the price table in §3, with the old
  value noted beside the new one and the source column dated. Then every section that
  reasons from the old number (today §5 was retitled and its arithmetic
  redone).
- [ ] Research: the synthesis table in `research/claude-releases.md` (or the
  matching digest), plus a dated `[Update ...]` note on each historical
  claim the change affects.
- [ ] Run grep 3 from section 1 with the old price.
- [ ] Release and refresh (sections 3 and 4).

## 3. Release

A push to `main` is a release. There is no version to bump:
`.claude-plugin/plugin.json` deliberately has no `version`, so Claude Code
versions an install by the commit it came from. Users get a push when they
next run `claude plugin marketplace update agent-orchestration` and then
`claude plugin update agent-orchestration@agent-orchestration`, or in the
background if they turned on auto-update for the marketplace (off by default
for a third-party marketplace; see the README's Updating section).

- [ ] Do not add `version` back to `plugin.json` or to the entry in
  `.claude-plugin/marketplace.json`. A pinned version keeps every user on
  their cached copy until the string changes, however many commits you
  push, and `claude plugin update` reports "already at the latest version".
- [ ] Commit with a message that names the models touched, for example
  "Add Claude Haiku 5.5, deprecate Haiku 4.5, cut Sonnet 5.5 cache reads".
- [ ] Push to `main` on the GitHub remote. The marketplace installs from
  GitHub, not from your working tree. The installed copy lands in
  `~/.claude/plugins/cache/agent-orchestration/agent-orchestration/<sha>/`,
  where `<sha>` is the first 12 characters of the commit it was installed
  from.
- [ ] Claude Code users: `claude plugin marketplace update agent-orchestration`,
  then `claude plugin update agent-orchestration@agent-orchestration`,
  restart Claude Code, then run `/agent-orchestration:refresh`.
- [ ] Never rename the plugin. Its `name` (in `plugin.json` and in the
  `marketplace.json` entry) is the install id users hold in `enabledPlugins`
  and type in `/plugin install`, so changing it breaks every existing
  install. For a cosmetic change to the label shown in `/plugin`, set
  `displayName` in `plugin.json` and keep `name`. If a rename is ever
  unavoidable, add a `renames` map to `marketplace.json` (see the Claude
  Code docs, "Host and maintain a marketplace").
- [ ] Other harnesses: pull the repo, then run
  `sh adapters/install.sh <harness> --update`, then the harness's
  `ao-refresh` skill (section 4).

**The developer loop.** An install from a local path (the maintainer's)
loads in place from the repo, so edits are live at the next session start or
`/reload-plugins`, and after each local commit the session-start status
reports `kit commit X -> Y` until you run `/agent-orchestration:refresh`. A
marketplace install is a cache copy pinned to a commit SHA: it sees nothing
until you push, run `claude plugin update agent-orchestration@agent-orchestration`
and restart. To preview a change before release, run the generator against
the repo: `python3 core/interview/generate.py --kit-root . --diff`.

## 4. Refresh an existing routing table

- [ ] At session start `hooks/session-start.sh` compares
  `~/.agent-orchestration/routing.stamp` to the `as_of` dates in
  `core/models/`, the `core/tasks.md` hash and the kit commit. The kit
  commit is the short HEAD when the kit root is a git checkout (a path
  install), else the cache directory's name when it is a commit SHA (a
  marketplace install); otherwise the status says the kit commit was not
  checked. When it reports changes, run `/agent-orchestration:refresh`
  (Claude Code, `skills/refresh/SKILL.md`) or `ao-refresh` (other harnesses,
  `adapters/_shared/skills/ao-refresh/SKILL.md`).
- [ ] Refresh runs `core/interview/generate.py` with `--check --json` to read
  the state, `--diff` to preview, and `--write` to regenerate `routing.md`,
  `glossary.md` and `routing.stamp`. There is no interview.
- [ ] It asks only about profiles that have no line in the config's
  `models:` block. It proposes `enabled` and `cost` for each, in one
  question, and writes only the lines you accept. Adding a profile with
  `enabled: false` stops it being flagged.
- [ ] The preview shows only the routing rows that change. If the diff would
  remove hand edits, refresh lists them and asks before writing.
- [ ] It never touches `~/.agent-orchestration/lessons.md`. In `config.yaml`
  it changes nothing except the model lines you accepted.
- [ ] If routing still feels wrong, edit `config.yaml` and refresh again.
  Never hand-edit the generated `routing.md`.

## 5. Delegating the update

The split that worked on 2026-10-08:

- [ ] One agent per disjoint file set: for example new profile; sibling
  profiles; research digests; strategy docs; bridges and config. No two
  agents edit the same file.
- [ ] One evidence packet handed to every agent: verified prices with fetch
  dates, timestamps looked up in the transcript, and the list of what is
  unverified. Agents cite the packet; they do not re-derive facts.
- [ ] The orchestrator reviews every diff, using a different model from the
  implementer (`core/strategies/verification-and-review.md`).
- [ ] One line per delegation in `~/.agent-orchestration/runs.jsonl`: the
  canonical record in `core/strategies/improvement-loop.md` §8, with
  `model` as the profile id (`claude-opus-5-5`, not `opus-5.5`).
  `python3 scripts/normalize_runs.py --check` validates the log.
