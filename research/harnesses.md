# Coding-Agent Harnesses: Conventions, Headless CLIs, and a Bridge Matrix

Research date: **2026-10-02**. Official docs were used first. Secondary sources are labelled. Where docs and the installed binary disagree, the installed binary wins.

**Verification levels used below**

- **[local]**: checked against `--help` or files on this machine (`claude 2.1.288`, `codex-cli 0.160.0`, `grok 1.0.0`, plus `~/.grok/README.md` shipped with Grok Build).
- **[docs]**: official documentation (URL given in the section).
- **[2nd]**: secondary source (blog or third-party guide). Treat as likely, not exact.
- **UNVERIFIED**: could not confirm. Do not hard-code without testing.

Not installed here: `gemini`, `agy`, `opencode`, Cursor's `agent`, `pi`. Their flags come from docs only.

---

## 0. Headline findings (read first)

1. **Gemini CLI is being retired for consumers.** On **2026-06-18** Google moved free, AI Pro and AI Ultra users to the new closed-source **Antigravity CLI (`agy`)**. Legacy `gemini` still works only with paid Gemini API keys, Vertex AI or Gemini Code Assist Standard/Enterprise. Both get adapter rows below (§4 and §4b).
2. **`agent` is ambiguous on PATH.** Cursor's CLI installs as `agent`. Grok Build *also* installs an `agent` symlink (`~/.grok/bin/agent -> grok binary`) [local]. On this machine `which agent` resolves to **Grok**. Adapters must call Cursor by absolute path or check `agent --version` first.
3. **macOS has no `timeout` command.** On this machine both `timeout` and `gtimeout` are missing [local]. Of the eight CLIs, only Antigravity has a wall-clock timeout flag (`--print-timeout`, **default 5m**). The bridge needs its own wrapper (see §C.2).
4. **Codex computer use runs only in the desktop app.** In July 2026 the Codex desktop app was merged into the ChatGPT desktop app. Docs say computer use is "available exclusively in the ChatGPT desktop application". **No documented way to trigger it from `codex` / `codex exec`.**
5. **Agent Skills (`SKILL.md`) is the de facto cross-harness format.** Codex, Cursor, Gemini CLI, Antigravity, OpenCode, Pi and Grok Build all read it. Claude Code reads it from `.claude/skills/`. The paths differ: `.agents/skills/` is the shared path, but **Claude Code does not document reading `.agents/skills/`**. Several harnesses read `.claude/skills/` for compatibility (Cursor, OpenCode, Grok).
6. **T3 Code ships its own cross-provider delegation MCP server** (`t3-code`, tool `delegate_task`). When the orchestrator runs inside T3 Code, it can delegate to another provider without shelling out (§8).

---

# PART A: Per-harness reference

## 1. Claude Code (Anthropic)

Sources: https://code.claude.com/docs/en/cli-reference , https://code.claude.com/docs/en/headless , https://code.claude.com/docs/en/memory , https://code.claude.com/docs/en/skills , https://code.claude.com/docs/en/sub-agents

**(1) Instructions.** Files: `CLAUDE.md` / `.claude/CLAUDE.md` / `CLAUDE.local.md`, plus managed and user `~/.claude/CLAUDE.md`, plus `.claude/rules/`. Since **v2.1.277** Claude Code reads `AGENTS.md` natively, but by default **only when no `CLAUDE.md`/`.claude/CLAUDE.md`/`CLAUDE.local.md` exists in cwd or above**. `~/.claude/CLAUDE.md` and managed files don't count toward that check. The setting `pluginConfigs["agents-md@builtin"].options.instructionFiles` takes one of these values:
- `claude-md-or-agents-md` (default)
- `claude-md-and-agents-md`
- `claude-md`
- `managed-only`

It is honored only in user, `--settings` or managed settings. Claude Code does **not** read `AGENTS.override.md`, `AGENTS.local.md`, or anything under `.agents/` [docs].

**(2) Skills.** Locations: `~/.claude/skills/<name>/SKILL.md`, `.claude/skills/` (repo root and parents), nested `<subdir>/.claude/skills/`, plugin `skills/`, managed, and `--add-dir` dirs. Custom commands (`.claude/commands/*.md`) are merged into skills. Extra frontmatter beyond the spec:
- `when_to_use`, `argument-hint`, `arguments`
- `disable-model-invocation`, `user-invocable`, `disallowed-tools`
- `model`, `effort`
- `context: fork`, `agent`, `background`
- `hooks`, `paths`, `shell`

Docs don't mention `.agents/skills` [docs].

**(3) Subagents.** Locations: `.claude/agents/`, `~/.claude/agents/`, plugin `agents/`, or `--agents '<json>'` (with `-p`, this can be a file path, v2.1.281+). Frontmatter:
- Required: `name`, `description`
- Common: `tools`, `disallowedTools`, `model` (`sonnet|opus|haiku|fable|<full id>|inherit`), `effort`, `permissionMode`, `maxTurns`
- Also: `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation: worktree`, `omitClaudeMd`

Model resolution order: per-call → frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → parent [docs].

**(4) Commands.** These are skills: `/skill-name`. In `-p`, put `/skill-name` in the prompt and it is expanded [docs].

**(5) Hooks.** In `settings.json` (`hooks`). Events include SessionStart, Setup, PreToolUse, PostToolUse, PermissionRequest, Stop, SessionEnd, PreCompact, Elicitation and more [docs; detail covered elsewhere].

**(6) MCP.** Files: `.mcp.json` (project), `~/.claude.json`, `--mcp-config <file|json>`, `--strict-mcp-config` [docs].

**(7) Non-interactive: `claude -p`** [local + docs]

| Need | Flag (exact) |
|---|---|
| One-shot | `claude -p "<prompt>"` (stdin is prepended/piped; 10 MB stdin cap) |
| Model | `--model <alias\|full-id>`. Aliases include `fable`, `opus`, `sonnet`, `haiku`. Optional `--fallback-model a,b` |
| Effort | `--effort low\|medium\|high\|xhigh\|max` (docs also list `ultracode`). Availability depends on the model |
| Output | `--output-format text\|json\|stream-json`. JSON has `.result`, `.session_id`, `.total_cost_usd`, and `.structured_output` when `--json-schema '<schema>'` is used. `stream-json` needs `--verbose` |
| Tools available | `--tools "Read,Grep,Glob"` (hard allowlist of built-ins; does not affect MCP) |
| Auto-approve | `--allowedTools "Bash(git diff *)" "Read"` (permission-rule syntax); deny with `--disallowedTools` |
| Permission mode | `--permission-mode default\|manual\|acceptEdits\|plan\|auto\|dontAsk\|bypassPermissions` |
| Read-only (recommended) | `--permission-mode dontAsk` denies anything that would prompt. Reads in the working dirs and the read-only Bash command set still run. Add `--tools "Read,Grep,Glob"` for a hard guarantee. (`plan` mode exists, but in `-p` its exit-plan approval is denied; UNVERIFIED how the result looks) |
| Unattended prompts | `--permission-prompts none` (v2.1.259+). Prompts are auto-denied and Claude is told not to retry |
| Turn cap | `--max-turns N` (print-only; exits with an error at the limit; **not shown in `--help`, but documented**) |
| Spend cap | `--max-budget-usd 5.00` (print-only) |
| Working dir | **No `--cwd` flag.** `cd` first. `--add-dir <dirs...>` grants extra access |
| Reproducible | `--bare` skips CLAUDE.md, hooks, skills, plugins and MCP auto-discovery. **Bare uses `ANTHROPIC_API_KEY` / apiKeyHelper only, never subscription OAuth** |
| No persistence | `--no-session-persistence` |
| System prompt | `--append-system-prompt[-file]`, `--system-prompt[-file]` |

**Timeouts.**
- There is no wall-clock flag.
- `-p` waits for background subagents/workflows, with a cap of **10 min idle** (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`, `0` = no cap).
- Background Bash shells are killed about 5 s after the result.
- SIGTERM exits **143** and records no result. Send SIGINT to end the turn cleanly.
- `MCP_TIMEOUT` (30 s default) applies to MCP startup with `--mcp-config`.

**Auth.**
- Without `--bare`, `-p` uses the normal login (`claude auth login`, subscription or Console).
- `claude setup-token` makes a long-lived OAuth token for CI (subscription required).
- `claude auth status` prints JSON with `authMethod`.

**(8) Install.** Native installer / `claude install [stable|latest|<ver>]`, `claude update` [docs]. Also note `claude ultrareview [target] --json --timeout <min>` for non-interactive cloud review (45 min default) [docs].

---

## 2. Codex CLI and the Codex desktop app (OpenAI)

Sources:
- https://learn.chatgpt.com/docs/non-interactive-mode (redirected from developers.openai.com/codex/noninteractive)
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/hooks
- https://learn.chatgpt.com/docs/config-file/config-reference
- https://learn.chatgpt.com/docs/computer-use
- https://learn.chatgpt.com/docs/developer-commands
- https://github.com/openai/codex

> Codex docs moved from `developers.openai.com/codex/*` to `learn.chatgpt.com/docs/*` (308 redirects).

**(1) Instructions.** Files: `AGENTS.md`. Discovery:
- Global: `~/.codex/AGENTS.override.md`, else `~/.codex/AGENTS.md` (first non-empty file only).
- Project: walk from the git root down to cwd. In each directory, take the first of `AGENTS.override.md` → `AGENTS.md` → names in `project_doc_fallback_filenames`, at most one file per directory.
- Files are concatenated root-first, so closer files win.
- Loading stops at `project_doc_max_bytes` (default **32 KiB**).
- Codex does not read `CLAUDE.md` unless you add it to `project_doc_fallback_filenames` [docs].

**(2) Skills.** Agent Skills standard [docs]. Locations:
- `.agents/skills` in cwd or parent folders
- `$HOME/.agents/skills`
- `/etc/codex/skills`
- bundled system skills

Invocation: `$skill-name` or `/skills`, or implicitly. Optional `agents/openai.yaml` sets UI metadata and `allow_implicit_invocation: false`. On name conflicts both copies stay (no merge). The legacy `~/.codex/skills/` exists on this machine [local], but docs no longer list it.

**(3) Subagents.** TOML files, one agent per file, in `~/.codex/agents/` or `.codex/agents/`. Required: `name`, `description`, `developer_instructions`. Optional (any `config.toml` key works): `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`. The `[agents]` table in config holds `enabled`, `max_concurrent_threads_per_session`, `default_subagent_model`, `default_subagent_reasoning_effort`. Built-ins `default`, `worker`, `explorer` can be overridden by name [docs].

**(4) Slash commands.** Built-ins include `/init`, `/review`, `/plan`, `/goal`, `/mcp`, `/status`, `/feedback`. **Custom prompts (`~/.codex/prompts/*.md`) were deprecated 2026-01-22 and removed in 0.117.0. Use skills instead** [2nd: GitHub issues #15972, #14459, plus the custom-prompts page].

**(5) Hooks.** Locations: `~/.codex/hooks.json`, `~/.codex/config.toml [hooks]`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml`, plugin `hooks/hooks.json`. Events:
- `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `PermissionRequest`
- `SessionStart`, `SessionEnd`
- `PreCompact`, `PostCompact`
- `SubagentStart`, `SubagentStop`
- `Stop`, `Interrupt`

Handlers are `command` or `mcp_tool`. Hooks are on by default (`[features] hooks = false` to disable). Non-managed hooks need hash-based trust (`/hooks`). `--dangerously-bypass-hook-trust` exists for automation [docs + local].

**(6) MCP.** `[mcp_servers.<id>]` in `~/.codex/config.toml`. Keys: `command`, `args`, `url`, `startup_timeout_sec`, `tool_timeout_sec`, `bearer_token_env_var`, `required`. Also `codex mcp` [docs]. Per-run override example: `-c mcp_servers.x.url=...`.

**(7) Non-interactive: `codex exec`** (alias `codex e`) [local + docs]

| Need | Flag (exact) |
|---|---|
| One-shot | `codex exec "<prompt>"`. Prompt from arg, or stdin if omitted / `-`. Piped stdin plus an arg gets appended as a `<stdin>` block |
| Model | `-m, --model <MODEL>` (also `-c model="..."`). IDs in the local models cache: `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5` [local] |
| Effort | **No dedicated flag.** Use `-c model_reasoning_effort="high"`. Values: `low\|medium\|high\|xhigh\|max\|ultra`, depending on the model. Locally, `ultra` is supported on gpt-6.1-sol, gpt-6-astra, gpt-6-sol, gpt-5.6-sol and gpt-5.6-terra; gpt-5.5 tops out at `xhigh` [local] |
| Read-only | **Default for `exec` is a read-only sandbox** [docs]. Explicit: `-s read-only` / `--sandbox read-only` |
| Allow edits | `--sandbox workspace-write`. **`--full-auto` is deprecated (prints a warning) and absent from 0.160.0 `--help`** [docs + local]. `--dangerously-bypass-approvals-and-sandbox` for full access |
| Output | Default: progress on **stderr**, final message on **stdout**. `--json` gives JSONL events (`thread.started`, `turn.started`, `turn.completed`, `turn.failed`, `item.started`, `item.completed`, `error`). `-o, --output-last-message <FILE>`. `--output-schema <FILE>` for structured output |
| Working dir | `-C, --cd <DIR>`. `--add-dir <DIR>` for extra writable dirs. `--skip-git-repo-check` is required outside a git repo |
| No persistence | `--ephemeral`. `--ignore-user-config`, `--ignore-rules` for reproducibility |
| Profiles | `-p, --profile <name>` (layers `$CODEX_HOME/<name>.config.toml`). **Note: `-p` here means profile, not prompt** |
| Local / open models | `--oss [--local-provider lmstudio\|ollama]` |
| Resume | `codex exec resume [SESSION_ID] \| --last` |

**`codex review` exists** [local]: `codex review [--uncommitted | --base <BRANCH> | --commit <SHA>] [--title T] [PROMPT|-]`. There is also a `codex exec review` subcommand. `codex review --help` shows **no `-m`, `--sandbox` or `--json`**. Use `-c model="..."` / `-c model_reasoning_effort="..."`. Its output format and sandbox defaults are UNVERIFIED.

**Timeouts.** No wall-clock flag. `stream_idle_timeout_ms` defaults to 300000 and `request_max_retries` to 4 [docs]. MCP servers marked `required = true` abort `exec` if they fail to start.

**Auth.**
- "Sign in with ChatGPT" (`codex login`, uses Plus/Pro/Business/Edu/Enterprise plan limits; `--device-auth` for headless).
- Or an API key: `CODEX_API_KEY=<key> codex exec ...` [docs].
- Multiple accounts are possible via `CODEX_HOME`.

**Desktop app and computer use.**
- On **2026-07-09** the standalone Codex desktop app was merged into the **ChatGPT desktop app**, which has Chat, Work and Codex modes. It reached macOS first, then Windows [2nd: Neowin, Addigy, danielvaughan.com].
- `codex app` "Launch[es] the Desktop app". A secondary source reports it looked for `Codex.app` after the merge and reinstalled a duplicate (issue #32631). The workaround was `open -a ChatGPT .` [2nd].
- **Computer use** is a plugin ("Computer Use": an MCP server plus a skill) in the ChatGPT desktop app, on macOS (Screen Recording and Accessibility permissions) and Windows. Docs say it is available "exclusively in the ChatGPT desktop application". It "can't automate terminal apps or ChatGPT itself".
- **No documented CLI/`exec` trigger.** `codex features list` shows `computer_use stable true` and `browser_use stable true` [local], but whether the CLI exposes that tool is **UNVERIFIED**.
- `codex app-server` / `codex remote-control` (experimental) are the likely bridges, also **UNVERIFIED**.

**(8) Install.**
- `curl -fsSL https://chatgpt.com/codex/install.sh | sh`
- `npm install -g @openai/codex`
- `brew install --cask codex`
- Update with `codex update` [docs: GitHub README]

---

## 3. Cursor (CLI agent)

Sources:
- https://cursor.com/docs/cli/headless
- https://cursor.com/docs/cli/reference/parameters
- https://cursor.com/docs/cli/reference/output-format
- https://cursor.com/docs/cli/using
- https://cursor.com/docs/cli/installation
- https://cursor.com/docs/context/rules
- https://cursor.com/docs/context/skills
- https://cursor.com/docs/context/subagents
- https://cursor.com/docs/agent/hooks
- https://cursor.com/docs/context/mcp

**Binary name: `agent`** (the old name `cursor-agent` isn't in current docs; whether an alias still exists is UNVERIFIED). **It collides with Grok's `agent` symlink.**

**(1) Instructions.** Sources:
- `.cursor/rules/` holding `.mdc` files. Frontmatter is `description`, `globs`, `alwaysApply`. Four rule types: Always, Apply Intelligently, Specific Files, Manual (@-mention). Plain `.md` files there are ignored unless they have frontmatter.
- User Rules (settings) and Team Rules (dashboard; these take precedence).
- `AGENTS.md` at the root and nested (more specific wins).
- The CLI reads `.cursor/rules` plus **`AGENTS.md` and `CLAUDE.md` at project root** [docs].
- Legacy `.cursorrules`: not covered in current docs (UNVERIFIED).

**(2) Skills.** Locations: `.cursor/skills/`, `.agents/skills/`, `~/.cursor/skills/`, `~/.agents/skills/`. For compatibility it also reads `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, `~/.codex/skills/`. Frontmatter: `name` (must match the folder), `description`, `paths`, `disable-model-invocation`, `icon`, `color`, `metadata`. Invoke with `/skill-name` or `@skill-name`. The Cursor 2.4 changelog says skills work in "the editor and CLI" [docs].

**(3) Subagents.** Markdown with YAML in `.cursor/agents/`, `.claude/agents/`, `.codex/agents/` (and the `~/` equivalents). `.cursor/` wins on name conflicts. Fields: `name`, `description`, `model` (`inherit` default, or a model ID with bracket params such as `claude-opus-5[effort=high,context=300k]`), `readonly`, `is_background`. Note that Codex agents are TOML, so how Cursor parses `.codex/agents/` is UNVERIFIED.

**(4) Commands.** `docs/context/commands` now serves the Skills page. Custom commands appear to be folded into skills (UNVERIFIED whether `.cursor/commands/` still loads).

**(5) Hooks.** Files: `~/.cursor/hooks.json`, `<project>/.cursor/hooks.json`, team and enterprise levels. Events:
- `sessionStart`, `sessionEnd`
- `preToolUse`, `postToolUse`, `postToolUseFailure`
- `subagentStart`, `subagentStop`
- `beforeReadFile`, `afterFileEdit`, `beforeShellExecution`, `afterShellExecution`
- `beforeSubmitPrompt`, `preCompact`, `stop`, `afterAgentResponse`, `afterAgentThought`
- `beforeMCPExecution`, `afterMCPExecution`
- Tab hooks, plus `workspaceOpen`

Exit code 2 blocks. Hooks are supported in the CLI [docs].

**(6) MCP.** `.cursor/mcp.json` and `~/.cursor/mcp.json` with an `mcpServers` object (`command`, `args`, `env`, `url`, `headers`; `${env:NAME}` interpolation). CLI: `agent mcp list|enable|disable|login`, and `--approve-mcps` for headless [docs].

**(7) Non-interactive** [docs]

| Need | Flag |
|---|---|
| One-shot | `agent -p "<prompt>"` (`--print`) |
| Model | `--model <model>`. List with `agent models` / `--list-models` |
| Effort | **No CLI flag documented.** Bracket params in the model ID (`<model>[effort=high]`) are documented for subagent `model:`. CLI acceptance is UNVERIFIED |
| Read-only | `--mode ask` (or `--mode plan` / `--plan`). Also: in print mode **without `--force`, changes are "only proposed, not applied"** (headless page). The "using" page says "Cursor has full write access in non-interactive mode", which is ambiguous, so pass `--mode ask` explicitly |
| Allow edits / commands | `-f, --force` (alias `--yolo`) |
| Output | `--output-format text\|json\|stream-json`. JSON gives `{type:"result", subtype, is_error, duration_ms, duration_api_ms, result, session_id, request_id?}`. `--stream-partial-output` |
| Working dir | `--workspace <path>` |
| Trust | `--trust` (trust workspace headless without prompt). `--approve-mcps` |
| Sandbox | `--sandbox enabled\|disabled` |
| Auth | `agent login` (Cursor account) or `CURSOR_API_KEY` / `--api-key` |

**Timeouts.** None documented. A non-zero exit means failure.

**Computer use.** `agent worker start --computer-use` lets cloud agents drive *this machine's* desktop through a private worker [docs]. That is not a one-shot path.

**(8) Install.** `curl https://cursor.com/install -fsS | bash` (Windows: `irm 'https://cursor.com/install?win32=true' | iex`). Update with `agent update` (auto-updates by default) [docs].

---

## 4. Gemini CLI (Google), legacy as of 2026-06-18

Sources:
- https://geminicli.com/docs/cli/headless
- https://geminicli.com/docs/cli/cli-reference
- https://geminicli.com/docs/cli/gemini-md
- https://geminicli.com/docs/cli/skills
- https://geminicli.com/docs/core/subagents
- https://geminicli.com/docs/hooks
- https://geminicli.com/docs/cli/custom-commands
- https://geminicli.com/docs/extensions
- https://geminicli.com/docs/tools/mcp-server
- https://geminicli.com/docs/get-started/installation
- https://geminicli.com/docs/get-started/authentication
- Transition: https://github.com/google-gemini/gemini-cli/discussions/27274

**Status.** Gemini CLI is still open source (Apache 2.0) and gets model and security updates for enterprise users. **It stopped serving Google AI Pro, Ultra and free-tier sign-ins on 2026-06-18.** Consumers were moved to Antigravity CLI (§4b). Treat `gemini` as "API-key / Vertex only".

**(1) Instructions.** `GEMINI.md`, read hierarchically:
- global `~/.gemini/GEMINI.md`
- workspace dirs and their parents
- "just-in-time" files when tools touch a directory

`@file.md` imports work. `/memory show|reload`. To read AGENTS.md, set `settings.json` → `"context": {"fileName": ["AGENTS.md","GEMINI.md"]}` [docs].

**(2) Skills.** Tiers: built-in, then extension, then user (`~/.gemini/skills/` or `~/.agents/skills/`), then workspace (`.gemini/skills/` or `.agents/skills/`). Within a tier, `.agents/` beats `.gemini/`. Commands: `/skills list|link|enable|disable|reload`, `gemini skills install <url> --consent` [docs].

**(3) Subagents.** `.gemini/agents/*.md` and `~/.gemini/agents/*.md`, Markdown plus YAML. Fields:
- Required: `name`, `description`
- Optional: `kind` (`local|remote`), `tools` (wildcards such as `mcp_*`), `model`, `temperature`, `max_turns` (default 30), `timeout_mins` (default 10)

Disable all with `experimental.enableAgents: false` [docs].

**(4) Custom commands.** TOML in `~/.gemini/commands/` or `<project>/.gemini/commands/`. `git/commit.toml` becomes `/git:commit`. Fields: `prompt` (required) and `description`. Templates support `{{args}}`, `!{shell}` and `@{file}` [docs].

**(5) Hooks.** `hooks` key in `.gemini/settings.json`, `~/.gemini/settings.json`, `/etc/gemini-cli/settings.json`, or in extensions. Events: `SessionStart`, `SessionEnd`, `BeforeAgent`, `AfterAgent`, `BeforeModel`, `AfterModel`, `BeforeToolSelection`, `BeforeTool`, `AfterTool`, `PreCompress`, `Notification`. Only `type: "command"` is supported. Default timeout is 60000 ms [docs].

**(6) MCP.** `mcpServers` in `settings.json`. Fields: `command`/`url`/`httpUrl`, `args`, `env`, `cwd`, `headers`, `timeout` (default 600000 ms), `trust`, `includeTools`, `excludeTools`. Also `gemini mcp add <name> <cmd|url> [args]` [docs].

**Extensions.** Live in `~/.gemini/extensions`. Defined by `gemini-extension.json` (`name`, `version`, `mcpServers`, `contextFileName`, `excludeTools`). An extension can bundle commands, hooks, sub-agents, skills, MCP and themes. Install with `gemini extensions install <github-url>` [docs].

**(7) Non-interactive** [docs]

| Need | Flag |
|---|---|
| One-shot | `gemini -p "<prompt>"` (headless is also triggered when there is no TTY). The prompt is appended to stdin |
| Model | `-m, --model <model>` (default `auto`) |
| Effort | **No flag.** Thinking is set in `settings.json` via `modelConfigs` / custom aliases (`thinkingConfig.thinkingLevel`), then you select that alias with `-m`. Exact JSON is UNVERIFIED |
| Approval | `--approval-mode default\|auto_edit\|yolo\|plan`. `-y/--yolo` is deprecated |
| Read-only | `--approval-mode plan` |
| Output | `-o, --output-format text\|json\|stream-json`. JSON gives `{response, stats, error?}` |
| Working dir | **No cwd flag**, so `cd` first. `--include-directories <dirs>` |
| Trust | `--skip-trust` |
| Sandbox | `-s, --sandbox` |
| Exit codes | `0` ok, `1` error, `42` input error, `53` turn limit exceeded |

**Timeouts.** No wall-clock flag. Subagents default to 10 min (`timeout_mins`).

**Auth (headless).** Cached credentials if present; otherwise `GEMINI_API_KEY`, or Vertex (`GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, plus ADC, `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_API_KEY`). **Consumer Google sign-in no longer serves requests after 2026-06-18.**

**(8) Install.** `npm install -g @google/gemini-cli` (`@preview`, `@nightly`), `brew install gemini-cli`, `sudo port install gemini-cli`, or `npx @google/gemini-cli` [docs].

---

## 4b. Antigravity CLI (`agy`), Google's successor to Gemini CLI

Sources:
- https://antigravity.google/docs/cli/headless/
- https://antigravity.google/docs/cli/reference
- https://antigravity.google/docs/cli/gcli-migration
- https://antigravity.google/docs/permissions?tab=cli
- [2nd] https://computingforgeeks.com/antigravity-cli-cheat-sheet/
- [2nd] https://virtualizationreview.com/articles/2026/05/19/google-moves-gemini-cli-into-antigravity-cli-as-agent-platform-expands.aspx

Released 2026-05-19. Closed source, written in Go. It shares its harness with the Antigravity 2.0 desktop app.

- **Instructions:** `GEMINI.md` and `AGENTS.md` with "identical workspace context rules" to Gemini CLI. Global `~/.gemini/GEMINI.md` [docs].
- **Paths.** Global config: `~/.gemini/antigravity-cli/` (`settings.json`). Workspace config: `.agents/`.
- **Skills:** global `~/.gemini/antigravity-cli/skills/`; workspace **`.agents/skills/`** (moved from `.gemini/skills/`) [docs].
- **Subagents / hooks:** an `agents/` dir and a `hooks/` dir (or `hooks.json` / `settings.json`). Exact schema is UNVERIFIED [docs: reference page lists dirs only].
- **Extensions become plugins:** `agy plugin import gemini`, `agy plugin install|uninstall|enable|disable|list` [docs].
- **MCP:** separate `mcp_config.json`, global `~/.gemini/config/mcp_config.json`, workspace `.agents/mcp_config.json`. URL key renamed to `serverUrl` [docs].
- **Permissions:** in `~/.gemini/antigravity-cli/settings.json`, allow/ask/deny lists over the actions `read_file`, `write_file`, `read_url`, `execute_url`, `command`, `unsandboxed`, `mcp`. Precedence is Deny > Ask > Allow [docs].

**Non-interactive** [docs]

| Need | Flag |
|---|---|
| One-shot | `agy -p "<prompt>"` (`--print` / `--prompt`). `--input-format text\|stream-json` |
| Model | `--model <slug>` (e.g. `gemini-3.8-flash-high`). **Docs say the model choice persists across sessions**, so pass it on every call |
| Effort | `--effort low\|medium\|high` |
| Output | `--output-format text\|json\|stream-json`. JSON gives `{conversation_id, status, response, duration_seconds, num_turns, usage{...}}`. `--json-schema <schema\|file\|type>` [2nd] |
| Mode | `--mode accept-edits\|plan` [2nd]. Read-only is presumably `plan` (UNVERIFIED semantics) |
| Full auto | `--dangerously-skip-permissions` |
| Working dir | `--cwd` / `--workspace`, plus `--add-dir <path>` |
| **Timeout** | **`--print-timeout` (default `5m`)**. This is the only harness with a built-in wall clock, and the default is short. Always raise it for real tasks |
| Resume | `-c/--continue`, `--conversation <id>` |
| Exit | `0` success, non-zero on error (reason in stderr plus `status`) |

Known issue: `agy models` may hang when stdin is a held-open non-TTY pipe (GitHub issue #882 in google-antigravity/antigravity-cli) [2nd]. Redirect stdin from `/dev/null`.

**Auth.** Google sign-in (OS keyring, or browser over SSH; free/AI Pro/Ultra). For headless, use `GEMINI_API_KEY` with `"modelProvider": "gemini"` in settings [2nd].
**Install.** `curl -fsSL https://antigravity.google/cli/install.sh | bash`. It self-updates [docs: discussion #27274].

---

## 5. OpenCode

Sources:
- https://opencode.ai/docs/cli/
- https://opencode.ai/docs/rules/
- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/skills/
- https://opencode.ai/docs/commands/
- https://opencode.ai/docs/plugins/
- https://opencode.ai/docs/mcp-servers/
- https://opencode.ai/docs/config/
- https://opencode.ai/docs/providers/
- https://opencode.ai/docs/permissions/
- https://opencode.ai/docs/

**(1) Instructions.** Lookup order:
1. Project: walk up from cwd. `AGENTS.md` is preferred, with `CLAUDE.md` as fallback; the first match wins, so if both exist only `AGENTS.md` loads.
2. Global: `~/.config/opencode/AGENTS.md`, falling back to `~/.claude/CLAUDE.md`.
3. `opencode.json` → `"instructions": [...]` (globs and URLs allowed; 5 s fetch timeout).

Turn Claude compatibility off with `OPENCODE_DISABLE_CLAUDE_CODE`, `..._PROMPT` or `..._SKILLS` [docs].

**Config files** (merged, later wins):
1. remote `.well-known/opencode`
2. `~/.config/opencode/opencode.json`
3. `OPENCODE_CONFIG`
4. project `opencode.json`
5. `.opencode/` dirs
6. `OPENCODE_CONFIG_CONTENT`
7. managed

Schema: `https://opencode.ai/config.json`. Substitutions: `{env:VAR}`, `{file:path}` [docs].

**(2) Skills.** Locations: `.opencode/skills/<name>/SKILL.md`, `~/.config/opencode/skills/`, `.claude/skills/`, `.agents/skills/` (walks up to the git worktree). Docs list `.claude`/`.agents` project paths; global `~/.claude/skills` and `~/.agents/skills` are implied but UNVERIFIED. Frontmatter: `name` (`^[a-z0-9]+(-[a-z0-9]+)*$`, must match the directory), `description` (1–1024 chars), optional `license`, `compatibility`, `metadata`. Gate with `permission.skill` [docs].

**(3) Agents.** Primary agents (`build`, `plan`) and subagents (`general`, `explore`, `scout`). Define them in `opencode.json` → `"agent": {...}`, or as Markdown in `.opencode/agents/` or `~/.config/opencode/agents/`. Fields:
- `description` (required)
- `mode` (`primary|subagent|all`), `model` (`provider/model-id`)
- `prompt`, `temperature`, `top_p`, `steps`
- `permission`, `hidden`

Provider options such as `reasoningEffort` pass through. Create with `opencode agent create` [docs].

**(4) Commands.** `.opencode/commands/*.md`, `~/.config/opencode/commands/`, or `opencode.json` → `"command"`. Frontmatter: `description`, `agent`, `model`, `subtask`. Templates support `$ARGUMENTS`, `$1`…, `` !`cmd` ``, `@file` [docs].

**(5) Hooks.** No shell-hook JSON. JS/TS **plugins** live in `.opencode/plugins/` or `~/.config/opencode/plugins/` and subscribe to events: `tool.execute.before/after`, `session.created/idle/compacted`, `file.edited`, `message.updated`, `shell.env`, and others [docs].

**(6) MCP.** `opencode.json` → `"mcp": { "<name>": { "type": "local", "command": ["npx","-y","x"], "environment": {...}, "enabled": true } }`, or `{"type":"remote","url":...,"headers":...,"oauth":...}`. `timeout` defaults to 5 s for the tool fetch [docs].

**Models / providers.** 75+ providers via AI SDK and models.dev. Open-weights hosts: OpenRouter, Together, Groq, Fireworks, Cerebras, DeepInfra, Ollama, LM Studio, llama.cpp, Moonshot/Kimi, Z.AI/GLM, MiniMax, DeepSeek. Curated hosted options: OpenCode Zen and OpenCode Go. Subscription logins: **ChatGPT Plus/Pro, GitHub Copilot, GitLab Duo**. **Claude Pro/Max subscription login is not supported**: docs say "Anthropic explicitly prohibits" it, and the bundled plugins were removed in 1.3.0 [docs].

**(7) Non-interactive: `opencode run`** [docs]

| Need | Flag |
|---|---|
| One-shot | `opencode run "<prompt>"` (or `--command <cmd>` with message args) |
| Model | `-m, --model provider/model` (e.g. `openrouter/<id>`, `ollama/<id>`) |
| Effort | `--variant <name>` ("provider-specific reasoning effort"). Values depend on the model |
| Agent | `--agent <name>` |
| Read-only | `--agent plan` (built-in analysis-only primary). Exactly how `plan` enforces no-edit is UNVERIFIED. Default permissions are mostly `allow`; `doom_loop` and `external_directory` are `ask`; `.env` reads are denied |
| Allow everything | `--auto` (auto-approve permissions that are not explicitly denied). What happens to `ask` without `--auto` in `run` is UNVERIFIED |
| Output | `--format default\|json` (json = **raw JSON event stream**, not a single result object) |
| Working dir | `--dir <path>` |
| Server reuse | `--attach http://localhost:4096`, `--port` |
| Other | `--file/-f`, `--session/-s`, `--continue/-c`, `--fork`, `--title`, `--thinking`, `--share`. Global: `--pure` (no external plugins), `--print-logs`, `--log-level` |
| Inline perms | env `OPENCODE_PERMISSION='<json>'` |

**Timeouts.** None documented.

**Auth.** `opencode auth login`, or `/connect` in the TUI. API keys go to the provider's env vars.

**(8) Install.**
- `curl -fsSL https://opencode.ai/install | bash`
- `npm install -g opencode-ai`
- `brew install anomalyco/tap/opencode`
- Windows: choco, scoop, mise or Docker [docs]

---

## 6. Pi (the "pi" coding agent)

**Identification.** "Pi" means **Pi, the minimal terminal coding agent** by Mario Zechner (libGDX author), first released in August 2025, MIT-licensed. It is now maintained by **Earendil Inc.** at `github.com/earendil-works/pi` (formerly `badlogic/pi-mono`); site https://pi.dev. There is no competing coding-agent "Pi" of similar prominence. Inflection's "Pi" chatbot is unrelated. T3 Code ships a first-class Pi provider, which confirms this is the intended one.

Sources:
- https://pi.dev
- https://github.com/earendil-works/pi
- Docs folder `packages/coding-agent/docs/`: `cli.md`, `configuration.md`, `skills.md`, `security.md`, `prompt-templates.md`, `extensions.md`, `mcp.md`, `json.md`, `providers.md`

**(1) Instructions.**
- Agent dir (`~/.pi/agent`, override with `PI_CODING_AGENT_DIR`): `AGENTS.override.md`, `AGENTS.md`, `CLAUDE.md` (case variants), `SYSTEM.md` (replaces the system prompt), `APPEND_SYSTEM.md`.
- Project context files (`AGENTS.override.md` / `AGENTS.md` / `CLAUDE.md`) load from cwd and all parents, **regardless of project trust**.
- `AGENTS.override.md` replaces `AGENTS.md`/`CLAUDE.md` in the same directory.
- Project `.pi/SYSTEM.md` and `.pi/APPEND_SYSTEM.md` need trust.
- `-nc` disables context files [docs].

**(2) Skills.** Implements the agentskills.io spec. Locations: `~/.pi/agent/skills/`, `.pi/skills/`, `~/.agents/skills/`, `.agents/skills/` (cwd up to the repo root). Explicit invoke: `/skill:name args`. It honors `disable-model-invocation`. Pi does not enforce that the name matches the directory. Flags: `--skill <path>`, `-ns` [docs].

**(3) Subagents.** **Not built in by design** ("skips features like sub-agents and plan mode"). An example `subagent` extension exists [docs]. There is no per-agent model config in core.

**(4) Commands.** "Prompt templates": `~/.pi/agent/prompts/*.md`, `.pi/prompts/*.md`. Filename = command. Frontmatter `description`, `argument-hint`. Placeholders `$1`, `$@`, `$ARGUMENTS`, `${1:-default}` [docs].

**(5) Hooks.** TypeScript **extensions** in `~/.pi/agent/extensions/`, `.pi/extensions/` or `-e <path>`. They receive events (`session_start`, `session_shutdown`, `input`, `project_trust`, tool-call interception, and so on) and can register tools, commands and providers [docs].

**(6) MCP.** Via the built-in extension `builtin:mcp`. Config in `~/.pi/agent/mcp.json` or `.pi/mcp.json` (project file needs trust), using `mcpServers`-style entries. Manage with `pi mcp add|remove|list|login|logout`. Per-request timeout defaults to 60 s [docs]. (Older guides say "no MCP"; that is outdated.)

**(7) Non-interactive** [docs: cli.md]

| Need | Flag |
|---|---|
| One-shot | `pi -p "<prompt>"` (`--print`; prints final assistant text). Piped stdin is prepended. Use `--` before a prompt starting with `-` |
| JSON | `--mode json "<prompt>"` gives a JSONL event stream (session header, then `agent_start`/`turn_start`/`message_*`...). `--mode rpc` for long-lived control |
| Model | `--model <pattern>`, accepts `provider/id` and the `:thinking` suffix (e.g. `sonnet:high`). `--provider <name>` requires `--model` |
| Effort | `--thinking off\|minimal\|low\|medium\|high\|xhigh\|max` (clamped to the model) |
| Read-only | **No approval system at all**: Pi "does not ask for approval before every tool call". Read-only only via tools: `--tools read,grep,find,ls`. Default tools are `read,bash,edit,write` |
| Working dir | **No flag.** `cd` first (cwd drives config, discovery and sessions) |
| Project trust (headless) | `-a/--approve` or `-na/--no-approve`. Without them, headless follows `defaultProjectTrust` (default `ask`, which **skips** project `.pi/` resources) |
| No persistence | `--no-session` |
| Prompt | `--system-prompt <text\|path>`, `--append-system-prompt <text\|path>` |
| Offline | `--offline` |

**Timeouts.** No wall-clock flag. `httpIdleTimeoutMs` defaults to 300000.

**Auth.** `/login` (OAuth or API key, saved to `~/.pi/agent/auth.json`). Env vars per provider: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `XAI_API_KEY`, `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `CEREBRAS_API_KEY`, `TOGETHER_API_KEY`, `FIREWORKS_API_KEY`, `MOONSHOT_API_KEY`, `ZAI_API_KEY`, `DEEPSEEK_API_KEY`, `OPENCODE_API_KEY`, `COPILOT_GITHUB_TOKEN`, and others. `pi auth check --provider X --json` exits 0/1/2 for ready/not_ready/invalid. Which consumer subscriptions `/login` supports is UNVERIFIED (see OpenCode's note on Anthropic's prohibition).

**(8) Install.**
- `curl -fsSL https://pi.dev/install.sh | sh`
- `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` (older guides use `@mariozechner/pi-coding-agent`)
- Update with `pi update`

---

## 7. Grok Build (xAI / "SpaceXAI")

**Identification.** "GrokBuild" is **Grok Build**, xAI's terminal coding agent and harness. Binary `grok`; source `github.com/xai-org/grok-build`, Apache-2.0, Rust. It has a TUI, a headless mode, and ACP (`grok agent stdio`). Installed here as v1.0.0 [local].

Sources:
- https://docs.x.ai/build/overview
- https://docs.x.ai/build/cli/headless-scripting
- https://github.com/xai-org/grok-build
- The shipped README `~/.grok/README.md` [local], which is the most detailed source

**(1) Instructions.** Global rules live in `~/.grok/`. Then, inside a git repo, every directory from the repo root to cwd is scanned; outside a repo, only cwd. In each directory Grok looks for `Agents.md`, `Claude.md`, `AGENT.md`, `AGENTS.md`. Deeper files come later and win. Gitignored files are skipped. Each file is capped at **10,000 chars**. `--rules "<text>"` appends more. **It also loads `CLAUDE.md` and `.claude/CLAUDE.md`** via Claude compatibility [local README].

**(2) Skills.** Priority order:
1. `./.grok/skills/`
2. `<repo>/.grok/skills/`
3. `~/.grok/skills/`
4. `~/.claude/skills/` (and `.claude/skills/`)

Extra dirs via `[skills] paths/ignore`. Frontmatter requires `name` and `description`. `/skills`, `/skill-name`. `grok inspect` lists discovered skills; here it found 57, including all of `~/.claude/skills` and the Claude plugin skills [local].

**(3) Subagents and agent profiles.**
- Agent profiles: `.md` with YAML in `.grok/agents/` or `~/.grok/agents/`, plus **`.claude/agents/`** and `~/.claude/agents/`. Select with `--agent <NAME|path>` / `--agent-profile`, `[agent]` in config, or `GROK_AGENT`.
- Subagents are on by default. `[subagents.toggle]` enables/disables types. `[subagents.models] explore = "<model>"` gives per-agent model pins (precedence: `[subagents.models]` > the definition's `model` > the parent's model).
- `[subagents.roles.<name>]` holds `default_capability_mode`, `model`, `prompt_file`. Personas also exist.
- Inline definitions: `--agents '<json>'`. Disable with `--no-subagents` or `--disallowed-tools Agent` [local].

**(4) Commands.** Built-in slash commands, plus skills as `/name`. Claude plugin `commands/` are discovered too [local README].

**(5) Hooks.** `.grok/hooks/` (the project must be trusted: `/hooks-trust`), or `[[hooks.PreToolUse]]` tables in `config.toml`, `managed_config.toml` or `requirements.toml`. The schema matches Claude's JSON `hooks` object. Events cover pre/post tool use and session start/end. Claude plugin `hooks/hooks.json` is honored. `--dangerously-...` has no equivalent; trust is required [local README].

**(6) MCP.** `[mcp_servers.<name>]` in `~/.grok/config.toml`, `<repo>/.grok/config.toml` or `<cwd>/.grok/config.toml` (a project entry replaces a global one with the same name). Fields: `command`, `args`, `env`, `headers`, `enabled`, `startup_timeout_sec` (30), `tool_timeout_sec` (60), `tool_timeouts`. **It also loads `~/.claude.json` and `.mcp.json`.** `grok mcp` [local README].

**Claude Code compatibility** [local README §"Claude Code Compatibility"]. Without any setup Grok picks up:
- `.claude/skills`, `.claude/agents`, `.claude/plugins`
- `installed_plugins.json`, `known_marketplaces.json`
- `~/.claude.json` / `.mcp.json` MCP servers
- `CLAUDE.md`
- `.claude/settings*.json` permissions (as a fallback)

**A Claude Code adapter's output is therefore mostly reused by Grok Build for free.**

**(7) Non-interactive** [local `grok --help` + README]

| Need | Flag (exact) |
|---|---|
| One-shot | `grok -p "<prompt>"` (`-p, --single`). Also `--prompt-file <PATH>`, `--prompt-json <JSON>`. Piped stdin works (`git diff \| grok -p ...`) |
| Model | `-m, --model <MODEL>`. `grok models` lists them (here: `grok-4.5` default, CLI v1.0.0). Docs mention `grok-build` and `grok-4.7` as model names; check with `grok models` |
| Effort | `--reasoning-effort <EFFORT>` (alias `--effort`). Values: `none\|minimal\|low\|medium\|high\|xhigh\|max`, plus per-model ids like `deep` |
| Output | `--output-format plain\|json\|streaming-json\|streaming-messages-json`. JSON gives `{text, stopReason, sessionId, requestId}`. `--json-schema '<schema>'` implies json |
| Read-only | `--sandbox read-only` (OS-level Seatbelt/Landlock: writes only to `~/.grok/`, child network blocked). And/or `--tools read_file,grep,list_dir`. `--permission-mode plan` also exists |
| Permission mode | `--permission-mode default\|acceptEdits\|auto\|dontAsk\|bypassPermissions\|plan` |
| Auto-approve | `--always-approve`. Rules: `--allow "Bash(npm*)"` / `--deny "Bash(rm*)"` (aliases `--allowedTools` / `--disallowedTools`; Claude `Bash(cmd:*)` syntax accepted) |
| Turn cap | `--max-turns N` (headless only) |
| Working dir | `--cwd <CWD>` |
| Sessions | `-s/--session-id <id>` (creates or resumes in headless), `-r`, `-c`. `-w` is ignored in headless |
| Updates | `--no-auto-update` per docs.x.ai (**not shown in v1.0.0 `--help`**; config `[cli] auto_update=false` works) |

**Timeouts.** No wall-clock flag. The bash tool defaults to **120 s** (`[toolset.bash] timeout_secs`). What happens to permission prompts in headless when neither `--always-approve` nor `--permission-mode` is set is **UNVERIFIED**, so always set one.

**Auth.**
- Browser login to grok.com (`grok login`, `--device-auth`; tokens in `~/.grok/auth.json`, 7-day expiry).
- Or `XAI_API_KEY`, which takes precedence. It is the recommended path for headless and CI.
- [2nd] Subscription login needs SuperGrok or X Premium+.
- Supports OIDC, external auth helpers, and custom OpenAI-compatible endpoints (`[model.<name>] base_url/env_key`), including Ollama.

**(8) Install.**
- `curl -fsSL https://x.ai/cli/install.sh | bash` (Windows: `irm https://x.ai/cli/install.ps1 | iex`)
- [2nd] `npm install -g @xai-official/grok`
- Update with `grok update`
- **Installs both `grok` and `agent` into `~/.grok/bin`** [local]

---

## 8. T3 Code (Theo / ping.gg)

Sources:
- https://github.com/pingdotgg/t3code (MIT)
- In-repo docs: `docs/user/providers-*.md`, `docs/user/permission-modes.md`, `docs/user/project-settings.md`, `docs/internals/providers.md`, `docs/orchestration-v2/orchestrator-mcp-server.md`

**What it is.** An open-source "agent harness control surface" with web, Electron desktop and iOS/Android apps. A local Node WebSocket server wraps the provider CLIs and SDKs. It adds threads, worktrees, checkpoints, diffs, PR flows, scheduled tasks and remote access (T3 Connect / relay). It is not a model or a harness itself.

**Wrapped providers and their transport** (from the orchestrator doc):

| Provider | How T3 drives it | Prerequisite |
|---|---|---|
| Codex | `codex app-server` (MCP injected via `-c mcp_servers.t3-code.url=...`) | Codex CLI plus `codex login` (or T3-managed ChatGPT sign-in) |
| Claude | **Claude Agent SDK** (`mcpServers` + `allowedTools: ["mcp__t3-code__*"]`) | Claude Code plus `claude auth login`. Multiple accounts via `CLAUDE_CONFIG_DIR` |
| Cursor | **Cursor Agent SDK** | Cursor CLI plus `agent login` |
| Grok Build | **ACP** (`session/new` with `mcpServers`) | `grok login` |
| OpenCode | `opencode` server (one per thread) | `opencode auth login` |
| Pi | `pi --mode rpc --extension <t3 MCP bridge>` | Pi ≥ 0.80.5 (1.0 recommended) |
| Antigravity / any ACP Registry agent | ACP v2/v1 via the official ACP Registry (`antigravity-acp`) | Google sign-in |

**Its own config.**
- `t3.json` at the repo root (`$schema: https://t3.codes/schema/t3.json`): `scripts`/actions (e.g. `runOnWorktreeCreate`), workspace defaults, `worktreeSubmodules`.
- Everything else lives in server-side settings, with override order project > environment > `t3.json` > default.
- Default permission mode for new threads is **Full access**. The modes are Supervised, Auto-accept edits, Auto, Full access, mapped onto each provider's native mode.
- Skills appear in a `$` menu (taken from each provider's native skill dirs).

**What an adapter must account for:**

1. **The `t3-code` MCP server.** Every provider session gets an authenticated HTTP MCP server named `t3-code` at `http://127.0.0.1:<port>/mcp`. In Claude these tools show up as `mcp__t3-code__*`. It has 11 tools, including `orchestrator_capabilities` and **`delegate_task`**. `delegate_task` takes:
   - `task`
   - `target{providerInstanceId|driverKind, model}`
   - `role`: `implementation|research|review|design|test|general`
   - `mode`: `async|wait`
   - `timeoutMs`
   - `runtimeMode`: `inherit|approval-required|auto-accept-edits|full-access`
   - `interactionMode`: `inherit|plan|default`

   It also exposes `task_status`, cancel, `t3_thread_launch`, and thread list/read/send. **Inside T3 Code, cross-provider delegation is native and durable, with a visible child thread.** The kit's bridge skill should detect these tools and prefer them over shelling out. The child gets only the task prompt (no parent history), so the prompt must be self-contained.
2. Providers run with the user's **native** config (CLAUDE.md, skills, Pi extensions and so on), so adapter-rendered files work unchanged.
3. T3 sends prompts through SDK/RPC, not `-p`. So adapter assumptions about `claude -p` / `--bare` don't apply to the main thread.
4. ACP-based providers (Grok, Antigravity) have no native subagents. T3 substitutes orchestrator-owned child threads.

**Install.**
- `curl -fsSL https://t3.codes/install.sh | sh`
- Desktop: GitHub Releases, Homebrew, winget, AUR, .deb
- Trial: `npx t3@latest`

---

# PART B: Cross-harness standards

## B.1 Agent Skills (agentskills.io)

Sources: https://agentskills.io/specification , https://github.com/agentskills/agentskills

**Layout.** A skill is a directory containing `SKILL.md` (required), plus optional `scripts/`, `references/`, `assets/`.

**Frontmatter (spec):**

| Field | Required | Constraint |
|---|---|---|
| `name` | yes | 1–64 chars, `[a-z0-9-]`, no leading/trailing/consecutive `-`, **must match the parent dir** |
| `description` | yes | 1–1024 chars. Say what it does and when to use it |
| `license` | no | name or bundled file |
| `compatibility` | no | ≤500 chars, environment requirements |
| `metadata` | no | string→string map |
| `allowed-tools` | no | space-separated, **experimental** (e.g. `Bash(git:*) Read`) |

**Progressive disclosure.** About 100 tokens of metadata are loaded at startup. The body should stay under 5k tokens and SKILL.md under 500 lines. Resources load on demand, and references should be one level deep. Validate with `skills-ref validate ./my-skill`.

**Implementation matrix** (from the per-harness docs above):

| Harness | Reads `SKILL.md` | Project path(s) | User path(s) | Reads `.claude/skills` | Reads `.agents/skills` | Notable extra frontmatter |
|---|---|---|---|---|---|---|
| Claude Code | yes | `.claude/skills/` | `~/.claude/skills/` | native | **not documented** | `model`, `effort`, `context: fork`, `disable-model-invocation`, `user-invocable`, `paths`, `hooks`… |
| Codex | yes | `.agents/skills` | `~/.agents/skills`, `/etc/codex/skills` | not documented | yes | `agents/openai.yaml` sidecar |
| Cursor | yes | `.cursor/skills/`, `.agents/skills/` | `~/.cursor/skills/`, `~/.agents/skills/` | yes (also `.codex/skills`) | yes | `paths`, `disable-model-invocation`, `icon`, `color` |
| Gemini CLI | yes | `.gemini/skills/`, `.agents/skills/` | `~/.gemini/skills/`, `~/.agents/skills/` | not documented | yes (beats `.gemini`) | — |
| Antigravity | yes | `.agents/skills/` | `~/.gemini/antigravity-cli/skills/` | not documented | yes | — |
| OpenCode | yes | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/` | yes | yes | `permission.skill` gating |
| Pi | yes | `.pi/skills/`, `.agents/skills/` | `~/.pi/agent/skills/`, `~/.agents/skills/` | not documented | yes | `disable-model-invocation` |
| Grok Build | yes | `.grok/skills/` | `~/.grok/skills/`, `~/.claude/skills/` | yes | not documented | — |

**Portable placement rule.** Keep skills in one canonical source. Render them to **`.agents/skills/`** (Codex, Cursor, Gemini, Antigravity, OpenCode, Pi) **and** `.claude/skills/` (Claude Code; also read by Cursor, OpenCode and Grok). A symlink or copy covers all eight. Keep frontmatter to spec fields, plus `disable-model-invocation` (understood by Claude, Cursor and Pi). Put harness-specific fields only in the adapter-rendered copy.

## B.2 AGENTS.md

Source: https://agents.md. AGENTS.md is stewarded by the **Agentic AI Foundation (Linux Foundation)**. The convention is that the nearest file wins and an explicit user prompt overrides everything.

| Harness | Reads AGENTS.md | Notes |
|---|---|---|
| Claude Code | yes (v2.1.277+) | Default: **only if no CLAUDE.md** in cwd/ancestors. Ignores `AGENTS.override.md`. Configurable via `instructionFiles` |
| Codex | yes (primary) | `AGENTS.override.md` > `AGENTS.md` > fallbacks; 32 KiB cap |
| Cursor | yes (root and nested) | CLI also reads root `CLAUDE.md` |
| Gemini CLI | opt-in | `context.fileName` |
| Antigravity | yes | alongside `GEMINI.md` |
| OpenCode | yes (primary) | `CLAUDE.md` fallback |
| Pi | yes | plus `CLAUDE.md`, `AGENTS.override.md` |
| Grok Build | yes | `Agents.md`, `AGENT.md`, `AGENTS.md`, `Claude.md`; 10k-char cap per file |

The agents.md site also lists Jules, Factory, Aider, goose, Zed, Warp, VS Code/Copilot, Devin, Windsurf, Junie, Amp, RooCode, Kilo Code, Augment and others.

**Portable rule.** Write one root `AGENTS.md`. Then either have `CLAUDE.md` contain `@AGENTS.md`, or ship no `CLAUDE.md` at all; both work for Claude Code. Watch out: a user-local `CLAUDE.local.md` turns off Claude's AGENTS.md reading unless `instructionFiles` is changed.

## B.3 Emerging shared conventions (2026)

- **`.agents/` as a neutral directory.** It is the shared skills path. Antigravity also uses `.agents/mcp_config.json`. Claude Code does not read `.agents/`.
- **Claude Code compatibility as a de facto standard.** Grok Build reads `.claude/` (skills, agents, plugins, hooks, settings permissions), `CLAUDE.md` and `.mcp.json` wholesale. Cursor reads `.claude/skills` and `.claude/agents`. OpenCode reads `.claude/skills` and `CLAUDE.md`. Pi reads `CLAUDE.md`. Claude Code now offers `claude import [codex|...]` to pull config the other way.
- **Hook schema convergence.** Grok explicitly reuses Claude's `hooks` JSON schema. Codex and Cursor use similar event names (PreToolUse/PostToolUse vs `preToolUse`), but their files differ.
- **ACP (Agent Client Protocol)** is the shared *runtime* protocol for embedding agents (Grok `agent stdio`, Cursor `acp`, Gemini `--experimental-acp`, Antigravity via the ACP Registry). T3 Code and Zed are clients.
- **Mostly-converged headless surface:** `-p` + `--output-format json` + `--model` (Claude, Cursor, Gemini, Antigravity, Grok, Pi). Codex (`exec`) and OpenCode (`run`) are the outliers.

---

# PART C: Bridge matrix

## C.1 One-shot CLI bridge matrix

`<P>` = prompt, `<M>` = model, `<E>` = effort, `<D>` = absolute working dir. Every command assumes it runs with `cwd=<D>` unless a dir flag is shown. "Read-only" is the flag set that stops file writes.

| Harness → CLI | Command template (read-only, JSON) | Read-only flag(s) | Model flag | Effort flag | JSON output flag → answer field | Auth source | Timeout notes |
|---|---|---|---|---|---|---|---|
| **Claude Code** → `claude` | `cd <D> && claude -p "<P>" --model <M> --effort <E> --permission-mode dontAsk --output-format json` | `--permission-mode dontAsk` (prompts auto-denied; reads OK). Hard: `--tools "Read,Grep,Glob"` | `--model <alias\|id>` | `--effort low\|medium\|high\|xhigh\|max` | `--output-format json` → `.result` (`.structured_output` with `--json-schema`) | Subscription OAuth (`claude auth login`) or `ANTHROPIC_API_KEY`. `--bare` = **API key only** | No wall clock. `--max-turns N`, `--max-budget-usd X`. Background work cap 10 min (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`). SIGTERM → exit 143 |
| **Codex** → `codex exec` | `codex exec -C <D> -m <M> -c model_reasoning_effort="<E>" --sandbox read-only --skip-git-repo-check -o <outfile> "<P>"` | `--sandbox read-only` (also the **default**) | `-m <id>` | `-c model_reasoning_effort="low\|medium\|high\|xhigh\|max\|ultra"` (model-dependent) | `--json` → JSONL events. Simpler: plain stdout = final message, or `-o <file>` | ChatGPT login (`codex login`) or `CODEX_API_KEY` | No wall clock. `stream_idle_timeout_ms` = 300000. Writes: `--sandbox workspace-write` (`--full-auto` deprecated) |
| **Codex review** → `codex review` | `cd <D> && codex review --uncommitted -c model="<M>" -c model_reasoning_effort="<E>"` (or `--base <branch>` / `--commit <sha>`) | UNVERIFIED (assumed non-mutating) | `-c model="<M>"` (**no `-m`**) | `-c model_reasoning_effort=...` | **None** (no `--json` in help) | same as Codex | UNVERIFIED |
| **Cursor** → `agent` | `agent -p "<P>" --model <M> --mode ask --output-format json --workspace <D> --trust` | `--mode ask` (or `plan`). No writes without `--force` | `--model <id>` | **None** (bracket `<M>[effort=high]` UNVERIFIED in CLI) | `--output-format json` → `.result` | `agent login` (Cursor plan) or `CURSOR_API_KEY` | None documented. **Resolve `agent` by path: it collides with Grok's `agent`** |
| **Gemini CLI (legacy)** → `gemini` | `cd <D> && gemini -p "<P>" -m <M> --approval-mode plan -o json` | `--approval-mode plan` | `-m <model>` | **None** (settings.json `modelConfigs` alias) | `-o json` → `.response` | **`GEMINI_API_KEY` or Vertex only** (consumer sign-in ended 2026-06-18) | No wall clock. Exit 53 = turn limit. Subagent default 10 min |
| **Antigravity** → `agy` | `agy -p "<P>" --model <M> --effort <E> --mode plan --output-format json --cwd <D> --print-timeout 30m < /dev/null` | `--mode plan` (semantics UNVERIFIED) | `--model <slug>` (**persists**, so always pass it) | `--effort low\|medium\|high` | `--output-format json` → `.response` (`.status`) | Google sign-in (free/AI Pro/Ultra) or `GEMINI_API_KEY` + `modelProvider: "gemini"` | **`--print-timeout` default 5m. Always raise it.** Redirect stdin (hang bug #882) |
| **OpenCode** → `opencode run` | `opencode run "<P>" -m <provider/model> --variant <E> --agent plan --format json --dir <D>` | `--agent plan` (enforcement UNVERIFIED) | `-m provider/model` | `--variant <name>` (provider-specific) | `--format json` → **raw event stream**. Parse the last assistant text (UNVERIFIED shape) | `opencode auth login`: API keys, ChatGPT Plus/Pro, Copilot, GitLab Duo, Zen/Go. **Not Claude Pro/Max** | None documented. Writes allowed by default in `build`. `--auto` = approve all |
| **Pi** → `pi` | `cd <D> && pi -p "<P>" --model <provider/id> --thinking <E> --tools read,grep,find,ls --no-session --no-approve` | `--tools read,grep,find,ls` (**only** guard; Pi has no approvals) | `--model <pattern>` (`provider/id[:thinking]`) | `--thinking off\|minimal\|low\|medium\|high\|xhigh\|max` | `--mode json` → JSONL events (no single result). `-p` = plain final text | `/login` (OAuth or key) or per-provider env keys | No wall clock. `httpIdleTimeoutMs` 300000 |
| **Grok Build** → `grok` | `grok -p "<P>" -m <M> --reasoning-effort <E> --sandbox read-only --permission-mode plan --output-format json --cwd <D>` | `--sandbox read-only` (OS-enforced) and/or `--tools read_file,grep,list_dir` | `-m <id>` (`grok models`) | `--reasoning-effort none\|minimal\|low\|medium\|high\|xhigh\|max` (alias `--effort`) | `--output-format json` → `.text` (`.sessionId`) | `grok login` (grok.com; SuperGrok/X Premium+ [2nd]) or `XAI_API_KEY` (takes precedence) | No wall clock. `--max-turns N`. Bash tool 120 s. Set `[cli] auto_update=false` for scripts |

**Write-enabled variants** (for implementation tasks):

| Harness | Write flags |
|---|---|
| Claude | `--permission-mode acceptEdits` (plus `--allowedTools` for Bash), or `auto`, or `bypassPermissions` |
| Codex | `--sandbox workspace-write` |
| Cursor | `--force` |
| Gemini | `--approval-mode auto_edit\|yolo` |
| Antigravity | `--mode accept-edits` / `--dangerously-skip-permissions` |
| OpenCode | default `build` agent (+ `--auto`) |
| Pi | default tools |
| Grok | `--always-approve` (optionally with `--sandbox workspace`) |

## C.2 Timeout wrapper (needed on macOS)

Only `agy` has a built-in timeout, and macOS ships no `timeout` binary. Pick one:
- `gtimeout` from `brew install coreutils` (`gtimeout -k 10 1800 <cmd>`)
- the Perl one-liner that is always present: `perl -e 'alarm shift; exec @ARGV' 1800 <cmd>`. SIGALRM kills only the exec'd process, so child processes may survive.
- a background job plus `kill`

Prefer SIGINT before SIGTERM for `claude`. SIGTERM leaves no result (exit 143).

## C.3 Things the bridge skill must not assume

- `-p` does **not** mean prompt for `codex` (it means `--profile`). Codex takes the prompt positionally after `exec`.
- Effort flags are inconsistent:
  - flag `--effort`: Claude, Antigravity, Grok (Grok also accepts `--reasoning-effort`)
  - `-c model_reasoning_effort=...`: Codex
  - `--variant`: OpenCode
  - `--thinking`: Pi
  - none: Cursor, Gemini
- JSON answer fields differ:
  - `.result`: Claude, Cursor
  - `.response`: Gemini, Antigravity
  - `.text`: Grok
  - event streams only: Codex `--json`, OpenCode, Pi. For these, use Codex `-o file` or plain stdout, and Pi `-p` plain text.
- Working-dir handling differs:
  - flags: `-C` (Codex), `--workspace` (Cursor), `--dir` (OpenCode), `--cwd` (Grok, Antigravity)
  - **`cd` required:** Claude, Gemini, Pi
- Codex requires a git repo unless `--skip-git-repo-check`.

---

## Source index

- Claude Code: https://code.claude.com/docs/en/cli-reference · /headless · /memory · /skills · /sub-agents
- Codex: https://learn.chatgpt.com/docs/non-interactive-mode · /agent-configuration/agents-md · /agent-configuration/subagents · /build-skills · /hooks · /config-file/config-reference · /computer-use · /developer-commands · https://github.com/openai/codex
- Codex/ChatGPT merger [2nd]: https://www.neowin.net/news/openai-launches-chatgpt-work-and-unveils-unified-desktop-app-with-codex-built-in/ · https://codex.danielvaughan.com/2026/07/17/codex-chatgpt-unified-desktop-app-cli-migration-codex-app-detection-workarounds/
- Cursor: https://cursor.com/docs/cli/headless · /cli/reference/parameters · /cli/reference/output-format · /cli/using · /cli/installation · /context/rules · /context/skills · /context/subagents · /agent/hooks · /context/mcp · https://cursor.com/changelog/2-4
- Gemini CLI: https://geminicli.com/docs/ (pages cited in §4) · https://github.com/google-gemini/gemini-cli/discussions/27274
- Antigravity CLI: https://antigravity.google/docs/cli/headless/ · /docs/cli/reference · /docs/cli/gcli-migration · /docs/permissions?tab=cli · [2nd] https://computingforgeeks.com/antigravity-cli-cheat-sheet/
- OpenCode: https://opencode.ai/docs/ (pages cited in §5)
- Pi: https://pi.dev · https://github.com/earendil-works/pi (packages/coding-agent/docs/*)
- Grok Build: https://docs.x.ai/build/overview · https://docs.x.ai/build/cli/headless-scripting · https://github.com/xai-org/grok-build · local `~/.grok/README.md`
- T3 Code: https://github.com/pingdotgg/t3code (docs/user/*, docs/internals/providers.md, docs/orchestration-v2/orchestrator-mcp-server.md)
- Standards: https://agentskills.io/specification · https://agents.md
