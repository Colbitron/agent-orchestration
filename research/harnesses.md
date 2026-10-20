# Coding-Agent Harnesses: Conventions, Headless CLIs, and a Bridge Matrix

Research date: **2026-10-02**; §9 (OpenClaw) and §10 (Hermes Agent) added **2026-10-19**. Official docs were used first. Secondary sources are labelled. Where docs and the installed binary disagree, the installed binary wins.

**Verification levels used below**

- **[local]**: checked against `--help` or files on this machine (`claude 2.1.288`, `codex-cli 0.160.0`, `grok 1.0.0`, plus `~/.grok/README.md` shipped with Grok Build).
- **[docs]**: official documentation (URL given in the section).
- **[2nd]**: secondary source (blog or third-party guide). Treat as likely, not exact.
- **UNVERIFIED**: could not confirm. Do not hard-code without testing.

Not installed here: `gemini`, `agy`, `opencode`, Cursor's `agent`, `pi`, `hermes`. Their flags come from docs only. `openclaw` is not on PATH either, but a `~/.openclaw` state dir from version 2026.3.9 (March 2026) is, so §9 has a few `[local]` reconciliations against that older build.

---

## 0. Headline findings (read first)

1. **Gemini CLI is being retired for consumers.** On **2026-06-18** Google moved free, AI Pro and AI Ultra users to the new closed-source **Antigravity CLI (`agy`)**. Legacy `gemini` still works only with paid Gemini API keys, Vertex AI or Gemini Code Assist Standard/Enterprise. Both get adapter rows below (§4 and §4b).
2. **`agent` is ambiguous on PATH.** Cursor's CLI installs as `agent`. Grok Build *also* installs an `agent` symlink (`~/.grok/bin/agent -> grok binary`) [local]. On this machine `which agent` resolves to **Grok**. Adapters must call Cursor by absolute path or check `agent --version` first.
3. **macOS has no `timeout` command.** On this machine both `timeout` and `gtimeout` are missing [local]. Of the eight CLIs, only Antigravity has a wall-clock timeout flag (`--print-timeout`, **default 5m**). The bridge needs its own wrapper (see §C.2).
4. **Codex computer use runs only in the desktop app.** In July 2026 the Codex desktop app was merged into the ChatGPT desktop app. Docs say computer use is "available exclusively in the ChatGPT desktop application". **No documented way to trigger it from `codex` / `codex exec`.**
5. **Agent Skills (`SKILL.md`) is the de facto cross-harness format.** Codex, Cursor, Gemini CLI, Antigravity, OpenCode, Pi and Grok Build all read it. Claude Code reads it from `.claude/skills/`. The paths differ: `.agents/skills/` is the shared path, but **Claude Code does not document reading `.agents/skills/`**. Several harnesses read `.claude/skills/` for compatibility (Cursor, OpenCode, Grok).
6. **T3 Code ships its own cross-provider delegation MCP server** (`t3-code`, tool `delegate_task`). When the orchestrator runs inside T3 Code, it can delegate to another provider without shelling out (§8).
7. **OpenClaw and Hermes Agent are assistant runtimes, not terminal coding agents** (added 2026-10-19). Both run a chat-channel gateway, cron and subagents around an embedded agent, read Agent Skills from their own dirs (`~/.openclaw/skills`, `~/.hermes/skills/<category>/`), and have a headless one-shot with a per-call working dir (`openclaw agent exec --cwd`, `hermes chat --in`). Neither has a read-only mode: OpenClaw needs a tool deny list, Hermes has no read-only file toolset at all. OpenClaw dispatches to Claude Code, Codex, OpenCode, Gemini CLI and Cursor over ACP; Hermes imports their config once (`hermes import-agent`). Neither reads `CLAUDE.md` live, both read `AGENTS.md` (§9, §10).

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

## 9. OpenClaw (Peter Steinberger / openclaw.ai)

**Identification.** OpenClaw is a self-hosted personal AI assistant: a local **Gateway** process (WebSocket control plane, default port `18789`) that connects chat channels (Discord, Slack, Telegram, WhatsApp, iMessage, Signal, Matrix, and ~30 more) to an embedded agent runtime with tools, skills, sub-agents and plugins, plus a CLI/TUI, Control UI and companion apps for macOS/iOS/Android/Windows/Linux `[docs]` https://github.com/openclaw/openclaw. It can also dispatch work to external coding harnesses over ACP (Agent Client Protocol). Rename history `[2nd]` https://en.wikipedia.org/wiki/OpenClaw: first published 2025-11-24 as *Warelay*; renamed *Clawdbot* 2026-01-02; renamed *Moltbot* 2026-01-27 after Anthropic trademark complaints; renamed *OpenClaw* 2026-01-30. Steinberger announced a move to OpenAI on 2026-02-14 and an "OpenClaw Foundation" to steward the project `[2nd]` same URL. Language: TypeScript (plus Swift/Kotlin for apps) `[local]` via `gh api repos/openclaw/openclaw/languages`; license MIT `[docs]` README; repo github.com/openclaw/openclaw, docs https://docs.openclaw.ai (append `.md` to any page for raw Markdown `[docs]` https://docs.openclaw.ai/llms.txt). Install footprint: global npm package `openclaw`, state dir `~/.openclaw/` (config, SQLite state, per-agent dirs), workspace `~/.openclaw/workspace` `[docs]` https://docs.openclaw.ai/concepts/agent-workspace. Version scheme is `year.month.patch` where patch is a release counter, not a day (`2026.9.6`, `2026.9.6-beta.1`, extended-stable lines start at patch 33) `[docs]` https://docs.openclaw.ai/reference/RELEASING; channels stable/beta/extended-stable/dev. Cadence is several releases per week: tags `v2026.10.4` (2026-10-16) and `v2026.10.5` (2026-10-18) `[local]` via `gh api .../releases`. Docs relied on below are the live docs as of 2026-10-19 (≈ v2026.10.5); the machine's `2026.3.9` is seven months behind. Note: no `v2026.3.9` git tag exists (neighbours are `v2026.3.8`, committed 2026-03-09, and `v2026.3.11`) `[local]` via `gh api .../git/matching-refs/tags/v2026.3.`; so the local version string is UNVERIFIED as a published release (possibly an npm-only or beta build).

Sources:
- https://github.com/openclaw/openclaw (README)
- https://docs.openclaw.ai/llms.txt, https://docs.openclaw.ai/sitemap.xml
- https://docs.openclaw.ai/cli/agent, /cli/models, /cli/skills, /cli/gateway, /cli/gateway/running, /cli/acp, /cli/mcp, /cli/mcp/registry
- https://docs.openclaw.ai/concepts/agent-workspace, /concepts/system-prompt, /concepts/agent, /concepts/multi-agent, /concepts/agent-runtimes, /concepts/models, /concepts/oauth
- https://docs.openclaw.ai/tools/skills, /tools/skills-config, /tools/creating-skills, /tools/subagents, /tools/slash-commands, /tools/exec, /tools/exec-approvals, /tools/acp-agents, /tools/acp-agents-setup, /tools/acp-agents/sessions, /tools/acp-agents/controls
- https://docs.openclaw.ai/automation/hooks, /automation/hooks/configuration, /automation/hooks/writing-hooks, /automation/hooks/event-types
- https://docs.openclaw.ai/plugins/hooks/prompt-and-session, /plugins/hooks/reference, /plugins/agent-guidance, /plugins/webhooks
- https://docs.openclaw.ai/gateway/config-hooks, /gateway/config-tools/tool-policy, /gateway/config-tools/sessions-and-subagents, /gateway/config-agents/models, /gateway/config-gateway, /gateway/config-secrets-env, /gateway/sandboxing, /gateway/sandbox-vs-tool-policy-vs-elevated
- https://docs.openclaw.ai/providers/anthropic, /providers/openai/authentication
- https://docs.openclaw.ai/install, /install/updating, /install/docker, /platforms/macos, /install/migrating-claude, /start/bootstrapping, /reference/RELEASING, /reference/templates/HEARTBEAT, /reference/templates/TOOLS, /releases
- https://en.wikipedia.org/wiki/OpenClaw `[2nd]`

**(1) Instructions.** Standing instructions are the *workspace bootstrap files*, injected into the system prompt's "Workspace Files" section on a session's first turn, in this order: `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `BOOTSTRAP.md` (brand-new workspaces only), `MEMORY.md` (only if present at the workspace root, and only in the main private session) `[docs]` https://docs.openclaw.ai/concepts/system-prompt, https://docs.openclaw.ai/concepts/agent-workspace. Purposes: `AGENTS.md` operating instructions and memory usage (its `## Tools` section holds local tool notes and is guidance only); `SOUL.md` persona/tone/boundaries; `USER.md` user preferences (separate 4,000-char cap); `IDENTITY.md` name/vibe/emoji set during the bootstrap ritual; `BOOTSTRAP.md` one-time first-run ritual, deleted when the workspace counts as configured; `BOOT.md` optional startup checklist run on Gateway start when the `boot-md` hook is enabled; `memory/YYYY-MM-DD.md` daily logs `[docs]` agent-workspace page. Caps: `agents.defaults.bootstrapMaxChars` default 20000 per file, `agents.defaults.bootstrapTotalMaxChars` default 60000 total; truncated files get a notice `[docs]` system-prompt page. `TOOLS.md` and `HEARTBEAT.md` are **retired**: TOOLS.md content moves to the `## Tools` section of AGENTS.md; HEARTBEAT.md is no longer created or read, heartbeat instructions live in "monitor scratch" managed with `openclaw automations scratch <jobId>`; `openclaw doctor --fix` migrates both `[docs]` https://docs.openclaw.ai/reference/templates/TOOLS, https://docs.openclaw.ai/reference/templates/HEARTBEAT (retirement version not stated on either page). Reconciliation: the `[local]` 2026.3.9 workspace still has `TOOLS.md` and `HEARTBEAT.md`, consistent with the older build. Workspace location: default `~/.openclaw/workspace`; `OPENCLAW_WORKSPACE_DIR` overrides; `agents.defaults.workspace` sets the default; per-agent `agents.entries.<id>.workspace` overrides, defaulting to `<state-dir>/workspace-<agentId>` `[docs]` agent-workspace, multi-agent pages. This matches the `[local]` `workspace-claude/` dir (an agent id `claude`). `agents.list[]` is the **legacy** array form; `agents.entries` (keyed map) is current and `openclaw doctor --fix` migrates `[docs]` https://docs.openclaw.ai/concepts/multi-agent; the `[local]` config uses `agents.defaults` only. Sub-agents get prompt mode `minimal` where only `AGENTS.md` is injected `[docs]` system-prompt page. `CLAUDE.md` is **not read at runtime** by any docs page; `openclaw migrate claude` copies project `CLAUDE.md`/`.claude/CLAUDE.md` into workspace `AGENTS.md` and `~/.claude/CLAUDE.md` into `USER.md` `[docs]` https://docs.openclaw.ai/install/migrating-claude. Project-directory AGENTS.md: when a session runs from another folder or worktree (e.g. `openclaw agent exec --cwd <repo>`), that folder's `AGENTS.md` is appended as project context; `SOUL.md`/`IDENTITY.md`/`USER.md`/`MEMORY.md`/`BOOTSTRAP.md` are not loaded from there `[docs]` system-prompt page. The optional plugin **Agent Guidance** can inject operator files via `prependSystemContext`/`appendSystemContext` without touching workspace files `[docs]` https://docs.openclaw.ai/plugins/agent-guidance. `openclaw agent exec` pins every agent workspace to `--cwd` and skips workspace bootstrap, so the default workspace `AGENTS.md` is not injected in exec runs (source `src/commands/agent-exec-input.ts`, `[2nd]` static read, not run).

**(2) Skills.** OpenClaw reads Agent Skills (`SKILL.md` directories, nested up to 6 levels). Precedence, highest first `[docs]` https://docs.openclaw.ai/tools/skills: (1) workspace `<workspace>/skills`, (2) project `<workspace>/.agents/skills`, (3) personal `~/.agents/skills` (default state dir only), (4) managed `<state-dir>/skills` = `~/.openclaw/skills`, (5) per-agent "workshop" skills learned by the agent, (6) bundled (plus Custodian skills), (7) `skills.load.extraDirs` and plugin skills. `.claude/skills` is not a skill root (only imported by `openclaw migrate claude`) `[docs]` migrating-claude page; `$CODEX_HOME/skills` is likewise import-only `[docs]` skills page. Frontmatter beyond name/description `[docs]` https://docs.openclaw.ai/tools/creating-skills, skills page: `homepage`, `user-invocable` (default `true`, exposes a slash command), `disable-model-invocation` (default `false`; hides from the model's prompt but `/skill <name>` still works), `command-dispatch: tool`, `command-tool`, `command-arg-mode` (default `raw`), and `metadata.openclaw` with `requires.bins|anyBins|env|config`, `primaryEnv`, `always` (skip bins/env/config gating), `os`, `emoji`, `skillKey`, `install` (brew/node/go/uv/download). The pre-July-2026 `metadata.clawdbot` block is no longer read. Config `[docs]` https://docs.openclaw.ai/tools/skills-config: `skills.entries.<name>` {`enabled`, `apiKey`, `env`, `config`}, `skills.allowBundled[]`, `skills.load.extraDirs[]`, `skills.load.watch` (default true), `skills.install.{preferBrew,nodeManager,allowUploadedArchives}`, `agents.defaults.skills[]` and per-agent `agents.entries.<id>.skills[]` (replaces, not merges). The prompt injects an `<available_skills>` list; the model loads the SKILL.md with `read` `[docs]` system-prompt page. Invocation: `/skill <name> [input]`, or user-invocable skills register as their own slash command; in the Control UI type `$` to pick a skill `[docs]` https://docs.openclaw.ai/tools/slash-commands, skills page. `commands.nativeSkills` default `"auto"` registers skill commands natively on Discord/Telegram `[docs]` slash-commands page. Command names are sanitized to `a-z0-9_` (max 32 chars), so `ao-setup` becomes `/ao_setup`; `/skill <name>` accepts either spelling `[docs]` https://docs.openclaw.ai/tools/slash-commands. New skills: the watcher picks them up, but a session snapshots its skills at start, so start a new one with `/new` `[docs]` https://docs.openclaw.ai/tools/creating-skills. CLI `[docs]` https://docs.openclaw.ai/cli/skills: `openclaw skills list [--eligible] [--verbose] [--json] [--agent <id>]`, `info <name>`, `check`, `search [query] [--limit n]`, `install @owner/<slug>|skills-sh:<o>/<r>/<slug>|git:owner/repo[@ref]|./path [--global] [--agent <id>] [--as <slug>] [--version]`, `update @owner/<slug>|--all`, `verify @owner/<slug>`. Installs land in the active workspace `skills/` by default, or the managed state-dir skills dir with `--global`. ClawHub (https://clawhub.ai) is the registry; `clawhub sync --all` publishes `[docs]` skills page.

**(3) Subagents and multi-agent.** Tool `sessions_spawn` (params `task`, `label`, `agentId`, `cwd`, `runtime` (`subagent` default | `acp`), `model`, `thinking`, `runTimeoutSeconds`, `mode`, `context: "fork"`, `visible`, `worktree`, `worktreeName`, `worktreeBaseRef`, `streamTo`, `resumeSessionId`, …) spawns a background run with session key `agent:<id>:subagent:<uuid>` that announces its result back `[docs]` https://docs.openclaw.ai/tools/subagents. Also `sessions_yield` and a `subagents` management tool. Config `[docs]` https://docs.openclaw.ai/gateway/config-tools/sessions-and-subagents: `agents.defaults.subagents.maxConcurrent` (default 8, per spawning session), `.maxChildrenPerAgent` (5), `.runTimeoutSeconds` (0 = none), `.model` (unset = inherit caller), `.allowAgents` (same agent only; `["*"]` any), `.announceTimeoutMs` (120000); `agents.defaults.subagents.thinking` (and per-agent `agents.entries.*.subagents.thinking`) sets the child's default thinking level; it is not on the config page but is on https://docs.openclaw.ai/tools/subagents/tool-reference `[docs]`; `thinking` is also a per-call `sessions_spawn` param. Local `[local]` `agents.defaults.subagents.maxConcurrent` matches. Multi-agent `[docs]` https://docs.openclaw.ai/concepts/multi-agent: `agents.entries.<id>` {`name`, `workspace`, `agentDir` (default `~/.openclaw/agents/<id>/agent`, holds per-agent SQLite), `model` pinned as `provider/model` e.g. `anthropic/claude-sonnet-4-6`, `identity`, `skills`, `subagents.allowAgents`, `sandbox`, `tools.allow/deny`}; `bindings[]` with `agentId` + `match {channel, accountId, peer{kind,id}}` route inbound traffic; `openclaw agents add <name> --workspace --model --agent-dir --bind <channel[:accountId]>`, `openclaw agents list --bindings`. ACP dispatch `[docs]` https://docs.openclaw.ai/tools/acp-agents-setup: `acp.enabled: true`, `acp.backend: "acpx"`, `acp.defaultAgent`, `acp.allowedAgents[]`, `acp.dispatch.enabled` (default true); plugin `openclaw plugins install @openclaw/acpx` + `openclaw config set plugins.entries.acpx.enabled true`; per-harness overrides `plugins.entries.acpx.config.agents.<id>.{command,args}`; `permissionMode: approve-all|approve-reads|deny-all` (default `approve-reads`), `nonInteractivePermissions: fail|deny` (default `fail`), `timeoutSeconds` default 120 for startup/control. Harnesses named `[docs]` https://docs.openclaw.ai/tools/acp-agents: Claude Code, Cursor, Copilot, Droid, OpenCode, Gemini CLI, Codex (ACP path; native Codex app-server is the preferred separate route), "other acpx harnesses". `pi` is in the `[local]` `allowedAgents` list but not named on current docs: UNVERIFIED. Spawn: `sessions_spawn` with `runtime: "acp"` (`agentId`, `cwd`, `mode: run|session`, `thread`, `model`, `thinking`, `resumeSessionId`; per-call timeout overrides are rejected) or chat `/acp spawn <agent> [--mode persistent|oneshot] [--bind here|off] [--thread auto|here|off] [--cwd <abs>] [--label]` `[docs]` https://docs.openclaw.ai/tools/acp-agents/sessions. No `acp_spawn` tool is documented. Reverse direction: `openclaw acp` is a stdio ACP bridge so editors (Zed) talk to the Gateway `[docs]` https://docs.openclaw.ai/cli/acp. Per-model runtime pin: `agents.defaults.models["provider/model"].agentRuntime.id` (`openclaw` | `codex` | `copilot` | `muse` | `claude-cli`) `[docs]` https://docs.openclaw.ai/concepts/agent-runtimes.

**(4) Commands.** `[docs]` https://docs.openclaw.ai/tools/slash-commands: `/new [model]`, `/reset [soft]`, `/compact [instructions]`, `/stop`, `/model [name|default|list|status] [-s|-a|-g]` (session/agent/global scope), `/models`, `/think <level|default>` (aliases `/thinking`, `/t`), `/verbose on|off|full`, `/fast`, `/reasoning`, `/elevated on|off|ask|full`, `/exec host=… security=… ask=…`, `/queue <mode>`, `/steer <msg>`, `/status`, `/context`, `/tools`, `/usage`, `/skill <name> [input]`, `/learn`, `/approve <id> <decision>`, `/subagents list|log|info`, `/acp spawn|cancel|steer|close|status|set-mode|set|cwd|permissions|timeout|model|sessions|doctor|install`, `/agents`, `/config show|get|set|unset` (needs `commands.config: true`), `/mcp …` (needs `commands.mcp: true`), `/plugins`, `/debug`, `/restart`, `/update`, `/bash <cmd>` or `! <cmd>` (needs `commands.bash: true`), `/export-session`, `/codex <action>`. Config: `commands.text` (true), `commands.native` ("auto"), `commands.nativeSkills` ("auto"), `commands.bash` (false), `commands.config|mcp|plugins|debug` (false), `commands.restart` (true), `commands.allowFrom.<provider>[]` (sole authorisation source when set), `commands.ownerAllowFrom[]`. Matches `[local]` `commands.{native,nativeSkills,allowFrom.discord}`.

**(5) Hooks.** *Internal hooks* are trusted JS/TS handlers in the Gateway process: one dir per hook with `HOOK.md` + `handler.ts|handler.js|index.ts|index.js` `[docs]` https://docs.openclaw.ai/automation/hooks/writing-hooks. Discovery, lowest→highest `[docs]` https://docs.openclaw.ai/automation/hooks/configuration: bundled → plugin → managed `~/.openclaw/hooks/` → `hooks.internal.load.extraDirs` → workspace `<workspace>/hooks/` (can only add names; needs `hooks.internal.entries.<key>.enabled: true`). Master switch `hooks.internal.enabled`; entries `hooks.internal.entries.<hookKey>.{enabled, env}`; `hooks.internal.handlers` is retired. HOOK.md frontmatter: `name`, `description`, `metadata.openclaw.{events[] (required), export, hookKey, emoji, homepage, os, requires.bins|anyBins|env|config, always, install}`. Events `[docs]` https://docs.openclaw.ai/automation/hooks/event-types: `command:new`, `command:reset`, `command:stop`, `session:auto-reset`, `session:compact:before|after`, `session:patch`, `agent:bootstrap`, `gateway:startup|shutdown|pre-restart`, `message:received|transcribed|preprocessed|sent`. **Context injection:** `agent:bootstrap` exposes a mutable `context.bootstrapFiles[]` (records `{name, path, missing, content}`) which a handler may replace or extend, so a hook can add instruction text at session bootstrap (subject to dedup and the bootstrap char budget); bundled hook `bootstrap-extra-files` exists for this `[docs]` event-types and hooks pages. Its config is `hooks.internal.entries.bootstrap-extra-files.{enabled, paths}`; paths must stay inside the event's workspace, and only the six bootstrap basenames (`AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `BOOTSTRAP.md`, `MEMORY.md`) load `[docs]` https://docs.openclaw.ai/automation/hooks/bundled-hooks. So it cannot load files outside the workspace. The `agent-guidance` plugin can: it reads an absolute operator directory, 1-8 files, 16 KiB each and 64 KiB total, read once at registration, so changes need `openclaw plugins reload agent-guidance` `[docs]` https://docs.openclaw.ai/plugins/agent-guidance. No session-start or turn-start internal event exists. *Plugin hooks* (`api.on(...)`) `[docs]` https://docs.openclaw.ai/plugins/hooks/prompt-and-session, https://docs.openclaw.ai/plugins/hooks/reference: `before_prompt_build` returns `prependContext`, `appendContext`, `systemPrompt`, `prependSystemContext`, `appendSystemContext`, `toolsAllow` (per-plugin system context capped at 25% of the model window); `agent_turn_prepare` returns `prependContext`/`appendContext`; `before_model_resolve` overrides provider/model; `before_tool_call` (modify/gate), `after_tool_call`, `agent_end`, `session_start`, `session_end`, `before_compaction`, `gateway_start|stop` are observe-only. There is no `before_agent_start` hook (the kit's assumption); the closest are `before_agent_run` (gate only) and `before_prompt_build`. Bundled hooks: `command-logger`, `session-memory`, `boot-md`, `compaction-notifier`, `bootstrap-extra-files` `[docs]` https://docs.openclaw.ai/automation/hooks. CLI: `openclaw hooks list|info|check|enable|disable [--agent <id>]`. *Webhooks* `[docs]` https://docs.openclaw.ai/gateway/config-hooks: `hooks.enabled` (false), `hooks.token` (required), `hooks.path` (`/hooks`), `POST /hooks/agent` {`message` required, `agentId`, `sessionKey`, `sessionMode: isolated|persistent`, `deliver`, `channel`+`to`, `model`, `thinking`, `timeoutSeconds`, `waitForCompletion`}, `POST /hooks/wake` {`text`, `mode: now|next-heartbeat`}, `hooks.mappings[]`. Reconciliation: `[local]` has no `~/.openclaw/hooks/` dir, which is fine (optional); plugin management is `openclaw plugins install|list|enable|disable|reload`.

**(6) MCP.** Yes, natively, in two directions `[docs]` https://docs.openclaw.ai/cli/mcp, https://docs.openclaw.ai/cli/mcp/registry. *Client:* `mcp.servers.<name>` {`command`, `args`, `cwd`, `env` | `url`, `transport` (`streamable-http`, SSE, stdio), `headers`, `enabled`, `requestTimeoutMs`, `connectionTimeoutMs`, `toolFilter.include|exclude`, OAuth/TLS, optional `codex` block}; managed with `openclaw mcp add <name> --command … --arg … | --url … --transport …`, `set`, `list`, `show`, `tools`, `configure`, `login`, `probe`, `doctor`, and chat `/mcp` (needs `commands.mcp: true`). Configured MCP tools appear in the embedded agent's `coding` and `messaging` tool profiles (hidden in `minimal`; `tools.deny: ["bundle-mcp"]` disables), and are projected to Codex/Claude Code/Gemini runtimes in their native shapes. *Server:* `openclaw mcp serve` exposes Gateway channel conversations over stdio to Codex/Claude Code; the opt-in `mcp-relay` plugin serves remote MCP clients `[docs]` https://docs.openclaw.ai/plugins/mcp-relay. Config keys do not appear in the `[local]` 2026.3.9 config; whether that build had `mcp.servers` is UNVERIFIED.

**(7) Non-interactive.** Two CLI paths `[docs]` https://docs.openclaw.ai/cli/agent: `openclaw agent` (one turn through the running Gateway, or `--local` embedded) and `openclaw agent exec` (isolated embedded turn, no Gateway, recommended headless/CI entry point). All flags below are from that page.

| Need | Flag |
|---|---|
| One-shot | `openclaw agent exec "<P>"` or `openclaw agent exec --message-file <path|-> [--cwd <D>]` `[docs]`; Gateway path `openclaw agent --message "<P>"` (`-m`) or `--message-file`, plus exactly one selector `--agent <id>` / `--to <target>` / `--session-key <k>` / `--session-id <id>`; `--local` runs embedded without the Gateway; `--deliver` sends the reply to the channel `[docs]` |
| Model | `--model <provider/model>` on both paths; `exec` also `--fallback <provider/model>` (repeatable, requires `--model`); defaults from `agents.defaults.model.primary` `[docs]` |
| Effort/thinking | `--thinking <level>`: `off`, `minimal`, `low`, `medium`, `high`, plus provider-supported levels "such as `xhigh`, `adaptive`, `max`, `ultra`" (not a fixed list; clamped with a notice if unsupported) `[docs]`; in chat `/think <level>` |
| Read-only | No single flag. `exec` defaults: sandbox off, `coding` profile, fs tools limited to `--cwd`, full exec policy `[docs]`. Restrict with `--config-override '{"tools":{"deny":["group:runtime","write","edit","apply_patch"]}}'` (repeatable, merged, not saved) `[docs]` cli/agent + tool-policy pages; `tools.profile: minimal|coding|messaging|full`; `tools.exec.mode: deny|allowlist|ask|auto|full` (legacy `tools.exec.security`/`.ask`) `[docs]` https://docs.openclaw.ai/tools/exec-approvals; `agents.defaults.sandbox.mode` (`off`, `non-main`, `all`; only `non-main`/`all` shown on docs) `[docs]` sandboxing page |
| Allow everything | exec defaults already grant full exec and `coding` tools; `--config-override '{"tools":{"profile":"full"}}'` and `openclaw exec-policy preset yolo` `[docs]` exec-approvals page |
| Output | `--json`: stdout is one envelope `{ok, status: ok|error|timeout, final, payloads[], usage, costUsd, model, provider, sessionId, error{message,kind}}` on `exec` `[docs]`; the answer text is `final` (and `payloads[].text`). Gateway path: `payloads[].text`, `meta`, optional `deliveryStatus`; failures `ok:false, error.type:"cli_error"` `[docs]`. `--verbose on|off` on the Gateway path |
| Working dir | `openclaw agent exec --cwd <D>` sets both the agent workspace and tool cwd, and `<D>/AGENTS.md` is appended as project context `[docs]` cli/agent + system-prompt. The Gateway path has **no** working-dir flag; it uses the agent's configured workspace |
| Timeout | `--timeout <seconds>` on both paths, default 600 per model attempt, `0` disables; `agents.defaults.timeoutSeconds` for Gateway turns (default 48 h) `[docs]` |
| Gateway requirement | `openclaw agent` needs a running Gateway unless `--local`; `--local` needs exclusive ownership of the state dir and refuses to start while a Gateway owns it. `exec` creates a temporary state dir by default, still reaches stored credentials, and does not touch the Gateway; only `exec --state-dir <dir>` needs exclusive ownership (`openclaw gateway stop` first) `[docs]` cli/agent |
| Resume | Gateway path: `--session-id <id>` (created if missing) or `--session-key agent:<id>:<key>`; `exec`: no resume flag documented (state goes to a temp dir unless `--state-dir`) `[docs]` |

**File-tool scope and questions.** `tools.fs.workspaceOnly` is optional and off unless set; with no permission mode or sandboxing either, file tools have full access ("Without those settings or sandboxing, the default is full access") `[docs]` https://docs.openclaw.ai/gateway/permission-modes. The `exec` defaults set it on, which is why fs tools are limited to `--cwd` there. For questions, the `ask_user` tool asks structured questions, but only in the main session on Discord, Slack, Telegram or WebChat `[docs]` https://docs.openclaw.ai/tools/ask-user; elsewhere and in sub-agents the agent asks in plain text.

**Timeouts.** `--timeout <seconds>` on `openclaw agent` and `openclaw agent exec`, default 600 s per model attempt, `0` disables, each fallback gets a fresh budget `[docs]` https://docs.openclaw.ai/cli/agent. Ordinary Gateway turns use `agents.defaults.timeoutSeconds` (unset = 48 h per attempt, `0` unlimited) `[docs]` https://docs.openclaw.ai/gateway/config-agents/models. Exec tool: `tools.exec.timeoutSeconds` default 1800 s; per call `timeoutSeconds: 0` disables `[docs]` https://docs.openclaw.ai/tools/exec. Sub-agents: `agents.defaults.subagents.runTimeoutSeconds` default 0 `[docs]`. ACP: `timeoutSeconds` default 120 for startup/control; `/acp timeout <s>` per session `[docs]`. Exit code 2 on `exec` marks a timeout `[docs]`.

**Auth.** Providers are plugins (Anthropic, OpenAI, Google, Copilot, Ollama, OpenRouter, Bedrock, …) `[docs]` https://docs.openclaw.ai/providers. Credentials: env vars (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) via process env, `openclaw.json` `env.vars`, `./.env` or `~/.openclaw/.env`, SecretRefs `{source: env|file|exec|store, provider, id}`; `auth.profiles.<id>` {`provider`, `mode: api_key|oauth`} and `auth.order.<provider>[]` in `openclaw.json` `[docs]` https://docs.openclaw.ai/gateway/config-secrets-env. Stored credentials now live in SQLite (`~/.openclaw/state/openclaw.sqlite`, per-agent `~/.openclaw/agents/<id>/agent/openclaw-agent.sqlite`); older `auth-profiles.json`/`credentials/oauth.json` are migrated by `openclaw doctor --fix` `[docs]` https://docs.openclaw.ai/concepts/oauth. Profile ids are `provider:name` (`anthropic:default`); `openai-codex:*` is a **legacy** prefix, use `--provider openai` `[docs]` oauth + openai/authentication pages. Commands: `openclaw onboard [--anthropic-api-key …]`, `openclaw models auth login --provider <id> [--method oauth|device-code|siwc|api-key|setup-token] [--agent <id>] [--profile-id <id>]`, `paste-api-key`, `paste-token`, `setup-token`; `openclaw models status [--json] [--check] [--probe]` (exit 0 ok / 1 missing-expired / 2 expiring), `openclaw models list --provider anthropic`, `openclaw models set <provider/model>` `[docs]` https://docs.openclaw.ai/cli/models. Anthropic `[docs]` https://docs.openclaw.ai/providers/anthropic: API key, or **Claude CLI** reuse (set `agentRuntime: { id: "claude-cli" }` on the model; OpenClaw shells out to `claude` and never reads its tokens), or `claude setup-token` → `openclaw models auth login --provider anthropic --method setup-token`. Vendor note on that page: Anthropic treats third-party/`claude -p` usage as programmatic, subscription usage draws from the subscription's limits, the Agent SDK credit plan was paused 2026-06-15, and the docs recommend an API key for shared/production automation. The `[local]` `auth.profiles` key and workspace `.secrets` file: the former matches docs; `.secrets` is undocumented (UNVERIFIED).

**(8) Install.** `[docs]` https://docs.openclaw.ai/install: `curl -fsSL https://openclaw.ai/install.sh | bash` (add `--no-onboard`; `--install-method git --version main` for main), `curl -fsSL https://openclaw.ai/install-cli.sh | bash` (prefix install under `~/.openclaw`), `npm install -g openclaw@latest --allow-scripts=openclaw` (drop the flag on npm ≤ 11.15), `pnpm add -g --allow-build=openclaw openclaw@latest`, `bun add -g --trust openclaw@latest`. Node 24.16+ or 26.1+ (26 recommended). Then `openclaw onboard --install-daemon`, `openclaw doctor`, `openclaw gateway status`. Service: `openclaw gateway install [--force]` (LaunchAgent on macOS, systemd user unit on Linux, Scheduled Task on Windows); `openclaw daemon …` is a legacy alias `[docs]` https://docs.openclaw.ai/cli/gateway. Update: `openclaw update [--channel beta|extended-stable|dev] [--dry-run] [--json]`, then `openclaw doctor --fix` and `openclaw gateway restart`; installs older than July 2026 must step through `2026.9.5` first `[docs]` https://docs.openclaw.ai/install/updating (relevant to the `[local]` 2026.3.9 machine). Docker: `ghcr.io/openclaw/openclaw:latest` (mirror `openclaw/openclaw`; tags `main`, `extended-stable`, `<version>`, `-slim`, `-browser`), state volume `/home/node/.openclaw`, `./scripts/docker/setup.sh` + `docker compose up -d openclaw-gateway` `[docs]` https://docs.openclaw.ai/install/docker. macOS menu-bar app: DMGs on GitHub releases (`OpenClaw-2026.10.3-arm64.dmg`), needs macOS 26.2+, bundles a Gateway runtime; no Homebrew cask documented `[docs]` https://docs.openclaw.ai/platforms/macos.

**Exit codes.** `openclaw agent`: 0 completed; 1 error, timeout or cancellation; 130/143 on SIGINT/SIGTERM `[docs]`. `openclaw agent exec`: 0 success; 1 model/result error (also cleanup failure after success); 2 timeout; 130 SIGINT; 143 SIGTERM `[docs]` https://docs.openclaw.ai/cli/agent. `openclaw models status --check`: 0/1/2 as above `[docs]` cli/models.

**Open questions** (not confirmed on 2026-10-19; do not hard-code):
- Whether `openclaw agent exec` existed in v2026.3.9: the live cli/agent page is undated; the `[local]` binary is not on PATH so `openclaw agent exec --help` could not be run. Treat the bridge row as valid for ≥ 2026.10 only until tested.
- `agents.defaults.sandbox.mode` full value list: docs show `non-main` (gateway/sandboxing) and `off`/`all` (multi-agent page) but no page lists all values with a default; `[local]` has `sandbox.mode` set so the key exists.
- RESOLVED: `agents.defaults.subagents.thinking` exists. Sub-agents inherit the caller's thinking level "unless you set `agents.defaults.subagents.thinking` (or per-agent `agents.entries.*.subagents.thinking`)" `[docs]` https://docs.openclaw.ai/tools/subagents/tool-reference. `agents.defaults.maxConcurrent` default is `max(8, CPU parallelism*4)` `[docs]` config-agents/models.
- `pi` as an ACP harness id: present in `[local]` `acp.allowedAgents` but not on current ACP docs (Claude Code, Cursor, Copilot, Droid, OpenCode, Gemini CLI, Codex). The embedded runtime id is `openclaw`; agent-runtimes page mentions "PI" only in comparison.
- `subagents/runs.json`, `memory/main.sqlite`, `exec-approvals.json`, workspace `.secrets`: present `[local]` but current docs describe SQLite replacements (`state/openclaw.sqlite`, per-agent `openclaw-agent.sqlite`; `exec-approvals.json` is imported as legacy by `doctor --fix`). `.secrets` not found in any fetched page.
- `--message`/`-m` on `agent exec`: the page lists a positional `[message]` and `--message-file`; whether `-m` is accepted there is unconfirmed.
- Thinking level set: docs say "provider/runtime-supported levels such as xhigh, adaptive, max, ultra"; no authoritative closed list found (searched cli/agent, concepts/models, config-agents/models).
- Read-only via `--config-override` tool deny: syntax of `--config-override` is documented, and tool deny semantics are documented, but no doc shows them combined; still not run.
- Whether `--config-override '{"tools":{"fs":{"workspaceOnly":false}}}'` lifts the `exec` file restriction to `--cwd`: docs say config wins over exec defaults; not run.
- The retirement version for `TOOLS.md` and `HEARTBEAT.md`: neither template page states it; hooks/skills pages reference "pre-July 2026" format changes, so sometime between 2026.3 and 2026.9.
- Exact release date of the local `2026.3.9`: no `v2026.3.9` tag on GitHub (`v2026.3.8` 2026-03-09, `v2026.3.11` 2026-03-12); releases page lists no such version.
- OpenAI "Sign in with ChatGPT" / Codex-subscription policy for third-party use: the openai/authentication page gives no policy statement, only that consent is app-specific.

---

## 10. Hermes Agent (Nous Research)

**Identification.** Hermes Agent is Nous Research's open-source "self-improving" agent: a terminal agent (classic REPL or Ink TUI) plus a long-running messaging gateway (Telegram, Discord, Slack, WhatsApp, Signal, email, ~30 more), a built-in cron scheduler, isolated subagents, and a learning loop that writes and refines `SKILL.md` skills and a persistent memory file [docs: https://github.com/NousResearch/hermes-agent]. Identity check: "Hermes" here is the Nous Research *agent* (`NousResearch/hermes-agent`), distinct from the Nous "Hermes" model series (Hermes 4 70B/405B are offered as models inside it [docs: https://hermes-agent.nousresearch.com/docs/integrations/nous-portal]); the many `github.com/<user>/hermes-agent` hits are forks, and no competing coding-agent named "Hermes" of comparable prominence turned up in searches (one `wellux/hermes` result 404s). Language: Python (`language: "Python"` on the GitHub API; `requires-python = ">=3.11,<3.15"`, first-party installs run 3.14) [docs: https://api.github.com/repos/NousResearch/hermes-agent, https://raw.githubusercontent.com/NousResearch/hermes-agent/main/pyproject.toml, https://hermes-agent.nousresearch.com/docs/getting-started/installation]. License MIT [docs: README]. Repo https://github.com/NousResearch/hermes-agent; docs https://hermes-agent.nousresearch.com/docs (llms.txt index at /docs/llms.txt). Repo created 2025-07-22 (GitHub API); public launch reported as 2026-02-25 [2nd: https://horadecodar.com.br/?p=40598, https://getcoai.com/article/hermes-ai/]. Releases: oldest GitHub release tag is date-based `v2026.3.12` (2026-03-12); current tags are SemVer `vX.Y.Z`, latest `v0.22.2` (2026-10-15), with several patch releases per week; channels `stable` (tagged releases, default for source installs) and `main` (every commit) [docs: https://github.com/NousResearch/hermes-agent/releases, https://hermes-agent.nousresearch.com/docs/getting-started/updating]. `pyproject.toml` `version = "0.0.0"`; `hermes --version` / `-V` prints the installed version [docs: cli-commands]. Console scripts: `hermes` (`hermes_cli.main:main`), `hermes-agent` (legacy one-query runner), `hermes-acp` [docs: pyproject.toml]. On POSIX the installer places a wrapper at `~/.local/bin/hermes` with the checkout at `~/.hermes/hermes-agent/`; state dir `~/.hermes` (Windows `%LOCALAPPDATA%\hermes`, Docker `/opt/data`) [docs: installation, environment-variables].

Sources:
- https://github.com/NousResearch/hermes-agent (README) and https://api.github.com/repos/NousResearch/hermes-agent
- https://raw.githubusercontent.com/NousResearch/hermes-agent/main/pyproject.toml
- https://github.com/NousResearch/hermes-agent/releases
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands
- https://hermes-agent.nousresearch.com/docs/user-guide/cli
- https://hermes-agent.nousresearch.com/docs/reference/slash-commands
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
- https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
- https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
- https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents
- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
- https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
- https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://hermes-agent.nousresearch.com/docs/user-guide/sessions
- https://hermes-agent.nousresearch.com/docs/user-guide/security
- https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference
- https://hermes-agent.nousresearch.com/docs/reference/environment-variables
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://hermes-agent.nousresearch.com/docs/integrations/nous-portal
- https://hermes-agent.nousresearch.com/docs/getting-started/installation, /platform-support, /updating
- https://hermes-agent.nousresearch.com/docs/user-guide/docker
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging
- https://hermes-agent.nousresearch.com/docs/user-guide/features/acp
- https://github.com/NousResearch/hermes-agent/issues/25267 and https://cybersecuritynews.com/claude-ends-openclaw-subscriptions/ (policy, [2nd])

**(1) Instructions.** Standing instructions come from three layers, all assembled into the system prompt [docs: https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly]:
- Identity: `~/.hermes/SOUL.md` (i.e. `$HERMES_HOME/SOUL.md`). Loaded *only* from `HERMES_HOME`, never from the working directory; seeded with a starter file if absent, never overwritten; inserted verbatim as slot #1 of the system prompt; empty/unreadable file falls back to a built-in identity; same size cap as context files (`context_file_max_chars`, dynamic 20,000-char floor / 500,000 ceiling) [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/personality, context-files]. Above the cap Hermes keeps the first 70 % and the last 20 % of the file, so text appended at the end survives only inside that tail [src: agent/prompt_builder.py]. Seeding runs in `initialize_home` on every `load_config()`, so `hermes`, `hermes setup` and `hermes doctor --fix` all seed it [src: hermes_cli/config_home.py, hermes_cli/config.py]. "Never overwritten" has four exceptions: an untouched legacy comment-only scaffold is auto-upgraded [src: hermes_cli/config.py]; `hermes profile update` rewrites a distribution-owned profile's `SOUL.md`; `hermes claw migrate --overwrite` replaces it; config migration v41 strips a "Messaging other agents" section. Each profile has its own: `~/.hermes/profiles/<name>/SOUL.md` ("Each profile gets its own directory containing its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills") [docs: user-guide/profiles]. Edits apply to new sessions; existing sessions keep the old prompt [docs: user-guide/profiles]. Related config: `agent.system_prompt` (manual system prompt, applies only when no personality is selected), `agent.personalities`, `display.personality`; `/personality <name>` [docs: personality]. `HERMES_EPHEMERAL_SYSTEM_PROMPT` / `ephemeral_system_prompt` take inline text, not a path; it is added at API-call time and never persisted [docs: reference/environment-variables; src: gateway/run_config_loaders.py].
- Memory: `~/.hermes/memories/MEMORY.md` (agent notes, `memory.memory_char_limit` 2200 chars) and `~/.hermes/memories/USER.md` (user profile, `memory.user_char_limit` 1375); named profiles use `~/.hermes/profiles/<name>/memories/`. Loaded at session start as a frozen snapshot into the system prompt; written by the `memory` tool (`add`/`patch`/`remove`); `memory.write_approval` gates writes [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory].
- Project context files, read from the working directory: one project file per directory, first match wins in the order `.hermes.md` / `HERMES.md` > `AGENTS.override.md` > `AGENTS.md` > `CLAUDE.md` > `.cursorrules` (plus `.cursor/rules/*.mdc`). Inside a git repo Hermes loads the merged chain of `AGENTS.md` from git root down to cwd (deeper = later = higher precedence, duplicates deduped); outside a repo only cwd is checked, never parents or `$HOME`; as tools touch subdirectories during a session each is checked once (up to 5 parents, 32,000-char hint cap). Per-file cap `context_file_max_chars` (null = dynamic 20K–500K; 70% head / 20% tail truncation), `context_file_read_timeout` 5.0 s. Files are scanned for prompt-injection patterns and blocked on a match. There is no `.hermes/` *instructions* directory; `.hermes/` in a project holds `skills/` and `plugins/` only [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files, configuration].
- Skip switches: `--ignore-rules` / `HERMES_IGNORE_RULES=1` skips `AGENTS.md`, `SOUL.md`, `.cursorrules`, memory and preloaded skills; `--ignore-user-config` ignores `config.yaml` (`.env` still loads) [docs: cli-commands, environment-variables].
- Relocation: `HERMES_HOME` sets the config + data dir (default `~/.hermes`; `~` and `$VAR` in the value are expanded); `--profile <name>` / `-p` selects `~/.hermes/profiles/<name>/` for one run, `hermes profile use <name>` makes it sticky [docs: environment-variables, cli-commands, user-guide/profiles]. Precedence: CLI args > `config.yaml` > `~/.hermes/.env` > defaults; `hermes config set KEY VALUE` writes dotted keys to `config.yaml` and `UPPER_SNAKE` names to `.env` [docs: configuration].

**(2) Skills.** Hermes implements the agentskills.io `SKILL.md` standard [docs: README, skills].
- Locations and precedence (highest first): project `<project-root>/.hermes/skills/` and `<project-root>/.agents/skills/` (loaded only after `hermes skills trust`; keys `skills.project_discovery`, `skills.trusted_project_dirs`) > `~/.hermes/skills/` (bundled skills are copied here on install; hub installs and agent-created skills also land here) > `skills.create_dir` (redirect for agent-created skills) > `skills.external_dirs` (e.g. `~/.agents/skills`) [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills]. Layout is `~/.hermes/skills/<category>/<name>/SKILL.md` (bundled: `skills/research/arxiv/SKILL.md`; the guide creates `~/.hermes/skills/my-category/my-skill/`); a category directory is *not* required: the loader walks `~/.hermes/skills` recursively (`os.walk(..., followlinks=True)`), so a flat `~/.hermes/skills/<name>/SKILL.md` is found and listed under `general` [src: agent/skill_utils.py, tools/skills_tool.py] (imports land in category dirs `claude-code-imports/<name>/`, `codex-imports/<name>/`, `openclaw-imports/`) [docs: creating-skills, work-with-skills, import-from-other-agents]. No frontmatter is required for discovery (a missing `name` falls back to the directory name); `skill_manage` validation wants `name` and `description` [src: agent/skill_utils.py]. `.claude/skills` is **not** read by default (`skills.external_dirs` can point at `~/.claude/skills` to read it live; `hermes import-agent --sync` re-imports changes); `hermes import-agent claude-code` copies `~/.claude/skills/<name>/` into `~/.hermes/skills/claude-code-imports/<name>/` and converts `CLAUDE.md` into `MEMORY.md` entries [docs: import-from-other-agents]. Opt out of bundled skills with a `.no-bundled-skills` marker in the profile; `HERMES_BUNDLED_SKILLS` overrides the bundled list [docs: skills, environment-variables].
- Frontmatter beyond `name`/`description`: `version`, `author`, `license`, `platforms` (`macos`|`linux`|`windows`), `required_environment_variables` (`name`, `prompt`, `help`, `required_for`), `required_credential_files`, and `metadata.hermes.{tags, category, related_skills, requires_toolsets, requires_tools, fallback_for_toolsets, fallback_for_tools, config, blueprint}`; `${HERMES_SKILL_DIR}` token for bundled scripts [docs: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills, skills].
- Hub CLI: `hermes skills browse|search|inspect|install|list|check|update|audit|uninstall|reset [--restore]|opt-out|opt-in|publish|snapshot export|tap add|list|remove|trust|untrust|config`; sources `official`, `skills-sh`, `well-known`, `url`, `github`, `clawhub`, `lobehub`, `browse-sh`; identifiers like `official/research/arxiv` or a raw URL (`hermes skills install https://example.com/SKILL.md`); hub landing page https://agentskills.io [docs: skills, work-with-skills, cli-commands]. In chat: `/skills search <term>`, `/skills install <id> [--name x]`, `/skills browse`, `/skills pending|diff|approve|reject|approval on|off`, `/reload-skills`.
- Automatic learning: the agent calls `skill_manage` (`create`, `patch`, `delete`, `write_file`, `remove_file`) and writes new skills under `~/.hermes/skills/` (or `skills.create_dir`); a background review may propose edits after a session; with `skills.write_approval: true` writes are staged under `~/.hermes/pending/skills/`; `skills.guard_agent_created` (default false); `/learn <source>` builds a skill from a directory, URL, workflow or doc [docs: skills, configuration].
- Invocation: every installed skill is a slash command `/<skill-name> [instructions]` (chain up to five: `/a /b do X`); `/<bundle-name>` loads a bundle; `-s`/`--skills <name>` preloads skills into the session prompt (`hermes chat -s my-skill -q "..."`); `skills.auto_load` loads a list every session; in one-shot mode `hermes chat -q "/my-skill help me"` works; otherwise the model picks skills itself via `skills_list` → `skill_view` (progressive disclosure) [docs: skills, work-with-skills, cli-commands]. The `<available_skills>` index in the system prompt shows each name plus its description cut to 60 characters (`SKILL_PROMPT_DESC_LIMIT = 60`); the full description is only in `SKILL.md` and `skills_list`/`skill_view` results [src: agent/skill_utils.py]. New skills are picked up by a running gateway without a restart ("your next message to the agent carries a short note naming the new skills"; the prompt index refreshes at the next compaction; `/reload-skills` refreshes slash commands) [docs: features/skills]; the slash-command map rescans when the skills tree's stat signature changes [src: agent/skill_commands.py].

**(3) Subagents.** Tool `delegate_task` (toolset `delegation`): params `goal`, `context` (child starts with a fresh conversation), `tasks[]` for a parallel batch (each with optional `output_schema`, `images`, `group`), `role: leaf|orchestrator`; top-level calls run in the background and return a handle [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation]. No per-call `model` or `toolsets` parameter: children inherit the parent's toolsets, and the model override is global via `delegation.model`, `delegation.provider`, `delegation.base_url` (wins over provider), `delegation.api_key`, `delegation.api_mode`, and, in source only, `delegation.reasoning_effort` (undocumented) [src: tools/delegate_tool_config.py] — so subagents may run a *different* model, but all children share it [docs: delegation, configuring-models]. Limits: `delegation.max_iterations` 250, `delegation.max_concurrent_children` (docs disagree: delegation page says 10, configuration/env pages say 3; env override `DELEGATION_MAX_CONCURRENT_CHILDREN`), `delegation.max_spawn_depth` 1 (range 1–3), `delegation.orchestrator_enabled`, `delegation.child_timeout_seconds` 0, `delegation.oneshot_max_children` 2 (cap in `-q` runs), `delegation.worktree_isolation` false, `tool_loop_guardrails.loop_caps.max_subagents` 50 [docs: delegation, configuration]. Children get the project context files but not `SOUL.md`, not the parent history, and cannot write `memory` [docs: delegation]. Other background surfaces: `/bg <prompt>`, `/agents`, `hermes kanban`, Mixture-of-Agents `/moa` [docs: slash-commands]. Questions: the `clarify` tool asks the user up to 5 questions per call, each with up to 4 choices plus an automatic "Other" row ("Ask the user a question when the agent needs clarification"); it is not in the subagent, api-server or ACP toolsets [src: tools/clarify_tool.py; docs: reference/toolsets-reference].

**(4) Commands.** Global: `hermes [--profile|-p NAME] [--resume|-r ID|TITLE|latest] [--continue|-c [TITLE]] [--in DIR] [--worktree|-w] [--yolo] [--ignore-rules] [--ignore-user-config] [--tui|--cli] [--version|-V] <command>`; `hermes -z "<prompt>"` (scripted one-shot) [docs: https://hermes-agent.nousresearch.com/docs/reference/cli-commands]. Subcommands (full list on that page): `chat`, `setup [--portal]`, `model`, `auth add <provider> [--type oauth|--browser]` (`login`/`logout` deprecated), `tools [--summary]`, `skills …`, `bundles …`, `mcp …`, `plugins …`, `hooks list|test <event>|revoke|doctor`, `cron list|create|edit|pause|resume|run|remove|status|runs|doctor|tick`, `config show|edit|get|set|unset|path|env-path|check|migrate`, `sessions list|export|import|delete|rename|prune|archive|stats|…`, `profile …`, `gateway run|start|stop|restart|status|install|uninstall|setup`, `worktree list|prune|restore`, `memory setup|status|off`, `acp`, `serve`, `dashboard`, `desktop` (`gui`), `proxy`, `status`, `usage`, `doctor [--fix]`, `update [--check|--plan|--channel|--set-channel|--branch|--backup|--no-backup|-y]`, `uninstall [--full|--data|--dry-run|--yes]`, `import-agent [claude-code|codex]`, `claw migrate`, `portal info`, `curator`, `journey`, `secrets`, `security audit`, `completion`. In-chat slash commands (case-insensitive) [docs: https://hermes-agent.nousresearch.com/docs/reference/slash-commands]: `/model [name] [--provider P] [--reasoning L] [--global|--session|--once]`, `/tools [list|enable|disable NAME]`, `/toolsets`, `/skills …`, `/new [name]` (`/reset` alias), `/compress [here [N] | <focus>]` (there is no `/compact`), `/reasoning [none…ultra|show|hide|full|clamp] [--global]`, `/yolo`, `/approvals manual|smart|off`, `/personality`, `/learn`, `/memory`, `/title`, `/save`, `/history`, `/status`, `/context`, `/bg`, `/btw`, `/queue`, `/steer`, `/branch`, `/worktree`, `/reload-mcp`, `/reload-skills`, `/plugins`, `/cron`, `/review`, `/plan`, `/init`, `/usage`, `/quit [--delete]`.

**(5) Hooks.** Four mechanisms [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks]:
- Shell hooks: a `hooks:` block in the profile's `config.yaml`, keyed by plugin event name, each entry `command` (required), `matcher` (regex, `pre_tool_call`/`post_tool_call` only), `timeout` (60 s default, 300 max), `fail_closed`. Stdin JSON carries `hook_event_name`, `tool_name`, `tool_input`, `session_id`, `cwd`, `profile`, `extra`; stdout JSON may be `{"decision":"block"}` / `{"action":"modify","args":…}` / `{"context":"…"}` (for `pre_llm_call`) / `{}`; exit 2 from `pre_tool_call` blocks. First use of each `(event, command)` prompts for consent, saved in `~/.hermes/shell-hooks-allowlist.json`; skip with `--accept-hooks`, `HERMES_ACCEPT_HOOKS=1`, or `hooks_auto_accept: true` (gateway/cron/CI never prompt). Event names: `on_session_start`, `on_session_end`, `on_session_reset`, `on_session_finalize`, `pre_llm_call`, `post_llm_call`, `pre_tool_call`, `post_tool_call`, `pre_verify`, `post_compaction`, `pre_command`, `pre_approval_request`, `post_approval_response`, `subagent_start`, `subagent_stop`, `pre_gateway_dispatch` (Claude Code names like `SessionStart`/`PreToolUse` are not used).
- Plugin hooks: Python plugins in `~/.hermes/plugins/<name>/` (`plugin.yaml` + `__init__.py` with `register(ctx)`; project `./.hermes/plugins/` exists but is not loaded by the gateway), enabled via `plugins.enabled` / `plugins.disabled`; `ctx.register_hook("<event>", cb)`; CLI `hermes plugins install|list|enable|disable|update|remove|doctor` [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins].
- Gateway hooks: `~/.hermes/hooks/<name>/HOOK.yaml` + `handler.py`, gateway-only, events `gateway:startup`, `session:start`, `session:end`, `agent:start|step|end`, …, trusted by placement.
- Outbound webhooks: `hooks.outbound:` list (`url`, `events`, `secret_env`), fire-and-forget.
- Context injection at session start: `on_session_start` is observer-only (return value ignored). Text can be injected by (a) `pre_llm_call` (shell `{"context": "..."}` or plugin return) — appended to the current turn's *user* message, not the system prompt — or (b) a plugin calling `ctx.register_system_prompt_section()`, which adds a bounded system-prompt section (evaluated once per new session, placed after memory, capped at 4,000 chars per section, 8,000 chars and 32 sections in total) [docs: hooks]. Config-only routes: `skills.auto_load` loads the listed skills' full text into the system prompt at the start of every new session on every surface (`--ignore-rules` suppresses it; delegate children skip it) [docs: user-guide/configuration]; `HERMES_EPHEMERAL_SYSTEM_PROMPT` / `agent.system_prompt` add inline text, not a path [docs: reference/environment-variables; src: gateway/run_config_loaders.py]. No file-drop mechanism injects into the system prompt and none of these reads an arbitrary file; use `SOUL.md`, `MEMORY.md`, a project `AGENTS.md`, or a pinned skill.

**(6) MCP.** Top-level `mcp_servers:` map in `~/.hermes/config.yaml` [docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp, reference/mcp-config-reference]:
```yaml
mcp_servers:
  local_tools:            # stdio
    command: "npx"
    args: ["-y", "some-mcp-package", "/allowed/dir"]
    env: {API_TOKEN: "***"}
    cwd: "/path"          # optional
    timeout: 120          # tool-call seconds; also connect_timeout, enabled, lazy, idle_timeout_seconds
    tools: {include: [read_file]}   # or exclude: ["delete_*"]; include wins
  remote_api:             # http (or transport: sse)
    url: "https://mcp.example.com/mcp"
    headers: {Authorization: "Bearer ***"}
    auth: oauth           # optional; oauth: {client_id, client_secret, redirect_port, flow, timeout}
```
Tools register as `mcp_<server>_<tool>` and each server becomes a toolset `mcp-<server>`; `mcp.discovery_concurrency` 4; `tool_budget.mcp_result_size_chars` 50000. CLI: `hermes mcp [catalog|install <name>|add <name> --url|--command … [--auth oauth|header]|remove|list|test <name>|configure <name>|login <name> [--flow device]|serve]`; `hermes mcp serve` exposes Hermes itself as a stdio MCP server; `/reload-mcp` in chat. `hermes import-agent claude-code` copies `mcpServers` from `~/.claude.json` [docs: mcp, cli-commands, import-from-other-agents].

**(7) Non-interactive.** Since v0.21 `hermes chat` and `hermes -z` are *gateway clients*: each call discovers or starts the profile's gateway (`hermes gateway ensure`), creates the session there and attaches over a local WebSocket; the working dir, `--model`, `--provider`, `--reasoning`, `--toolsets`, `--max-turns`, `--yolo`, `--ignore-rules` and `--safe-mode` are frozen into the session, and in-process-only options (`--run-budget`, `-w`, `--image`, `-v`, `--compact`, `--no-restore-cwd`) are refused with exit 2 [docs: user-guide/cli; source: `hermes_cli/main.py` routes `-z` through `launch_gateway_chat`]. Closing the terminal detaches and the turn continues at the gateway; Ctrl-C/SIGINT interrupts it (exit 130).
| Need | Flag |
|---|---|
| One-shot | `hermes chat -q "<P>"` (`--query`; on a TTY it seeds an interactive session, on non-TTY stdio it answers and exits; add `--oneshot` to force exit) [docs: cli-commands]. Stdin: `hermes chat --query-file - < prompt.txt` (`--query-file PATH`, mutually exclusive with `-q`; nothing is shell-interpreted) [docs: user-guide/cli]. Minimal: `hermes -z "<P>"` prints the final response text and nothing else on stdout/stderr [docs: cli-commands]; it does not read stdin, despite the docs' `hermes -z "summarize this" < file.txt` example [src: `gateway_chat.py` reads stdin only for `--query-file -`, and `-z` sets the query]. Legacy: `hermes-agent --query "<P>"`. |
| Model | `-m`/`--model <M>` (bare name resolved within the provider, e.g. `claude-sonnet-4` on OpenRouter → `anthropic/claude-sonnet-4.6`; aliases from `model.aliases.<name>`); persist with `hermes model` (writes `model.provider`, `model.default`, `agent.reasoning_effort`) or `hermes config set model.default <M>`; env `HERMES_INFERENCE_MODEL` forces the model for `-z`/`chat` without touching config [docs: cli-commands, configuring-models, environment-variables]. `provider/model` strings are OpenRouter ids; in-chat syntax is `/model provider:model`. |
| Provider | `--provider <name>` (e.g. `nous`, `openrouter`, `anthropic`, `openai-codex`, `copilot`, `custom`); `--base-url <url>` + `--api-key <key>` with `--provider custom` [docs: cli-commands, providers]. |
| Effort | `--reasoning <LEVEL>` on `hermes chat` [docs: user-guide/cli lists it among frozen options; cli-commands page does not list it — treat as `[docs]` for existence, level names UNVERIFIED for the flag]. Config `agent.reasoning_effort` ("" = medium; values `minimal` … `ultra`, `none` disables) and `agent.reasoning_overrides.<model>`; in chat `/reasoning <level> [--global]` with levels `none`…`ultra`; `/model … --reasoning <level>` [docs: configuration, configuring-models, slash-commands]. |
| Read-only | `-t`/`--toolsets <csv>` picks toolsets, e.g. `--toolsets web,search,session_search,vision`; the `safe` toolset is `web_search, web_extract, vision_analyze, image_generate` (no file/terminal). There is **no read-only file toolset**: `file` = `read_file, search_files, write_file, patch` [docs: toolsets-reference]. Mitigations: `HERMES_WRITE_SAFE_ROOT=<dir>` restricts `write_file`/`patch` to prefixes (hard reject), `approvals.deny` glob list, `approvals.mode: manual`, `agent.disabled_toolsets: [...]`, `terminal.backend: docker` (container is the boundary; dangerous-command checks are skipped there) [docs: environment-variables, security, configuration]. In `-q` mode approval prompts are *denied* by default (`approvals.single_query_mode: deny`) [docs: security]. |
| Allow everything | `--yolo` (= `HERMES_YOLO_MODE=1`; hardline blocklist still applies), `approvals.single_query_mode: approve` or `approvals.mode: off`, `--accept-hooks`/`HERMES_ACCEPT_HOOKS=1` for shell hooks [docs: security, cli-commands, hooks]. |
| Output | `--format stream-json` (requires `-q`/`--query-file`; implies quiet; rejected with `--tui`): every stdout line is one JSON object; events `system` (`subtype:"init"`, `model`, `session_id`), `text` (delta in `text`), `tool_use` (`name`, `input`), `tool_result` (`name`, `output` ≤5000 chars, `duration_ms`, `is_error`), terminal `result` (`session_id`, `exit_code`, `text` = final answer, `tokens`, `duration_ms`, `error`); diagnostics and the `session_id:` line go to stderr [docs: cli-commands]. `-Q`/`--quiet` suppresses banner/spinner/tool previews; `-v`/`--verbose` debug. Plain `-q` stdout content (final text only vs traces) is not stated — UNVERIFIED; `-z` is documented as final text only. `-z --usage-file <path>` writes a JSON cost/token report. No `--json` flag on `chat`. |
| Working dir | `--in <D>` changes into `<D>` before starting and scopes `--resume latest`/`-c` to that workspace; otherwise cwd is used and recorded as the session workspace (git root if any) and restored on resume (`--no-restore-cwd` to stay put); `-w`/`--worktree` runs in an isolated git worktree; `terminal.cwd` applies to gateway/cron only [docs: cli-commands, sessions, configuration]. |
| Session persistence | Always saved to `~/.hermes/state.db` (SQLite); one-shot runs are tagged `oneshot` (hidden from pickers; `--source <tag>` overrides, docs suggest `tool` for integrations); `-r`/`--resume <id|title|latest>`, `-c`/`--continue [title]`, `--create-if-missing`. No `--no-save`/ephemeral flag is documented [docs: sessions, cli-commands]. |
| System prompt override | No `--system-prompt` flag. Use `agent.system_prompt` in config (only when no personality is selected), `SOUL.md`, `HERMES_EPHEMERAL_SYSTEM_PROMPT` (inline text, added at API-call time, never persisted) [docs: reference/environment-variables], or `--ignore-rules` to drop files [docs: personality, cli-commands]. |
| Timeout | `--run-budget <SECONDS>` (float; wall-clock budget per run, wrap-up notice at 80 %, config twin `agent.run_budget_seconds`) exists on `hermes chat` [docs: configuration; source: `hermes_cli/_parser.py`] **but the gateway client refuses it** (`Unsupported gateway CLI options`, exit 2) because it only makes sense for an in-process agent [docs: user-guide/cli]. `--max-turns <N>` (default 500 / `agent.max_turns`) is accepted [docs: cli-commands]. |
| Exit codes | see below. |

**Timeouts.** Wall clock: `agent.run_budget_seconds` in config (the `--run-budget N` flag is refused by the gateway client, exit 2); turns: `--max-turns N` (default 500 per the parser and cli-commands; the configuration page says unlimited by default, a docs conflict; `HERMES_MAX_ITERATIONS` 500 is the tool-iteration cap). Per tool: `terminal.timeout` 180 s per command by default [docs: user-guide/configuration]; the foreground maximum is 600 s, and a call with a larger `timeout` is promoted to a tracked background process (or pass `background=true` and poll with `process_manage`) [src: tools/terminal_tool.py; foreground max source-only]; `context_file_read_timeout` 5 s; MCP `timeout` per server; `agent.session_stall_timeout` 300 s; `agent.turn_liveness.timeout_s` 600. API: `HERMES_API_TIMEOUT` 1800 s, `HERMES_API_CALL_STALE_TIMEOUT` 90 s, `providers.<id>.request_timeout_seconds`. Approvals: `approvals.timeout` 300 s (not reached in `-q`, where the default is deny); `agent.clarify_timeout` 3600 s. Delegation: `delegation.child_timeout_seconds` 0 = none [docs: configuration, environment-variables, security, delegation].

**Auth.** Providers (ids as used by `--provider`) [docs: https://hermes-agent.nousresearch.com/docs/integrations/providers, nous-portal]: `nous` (Nous Portal subscription; `hermes setup --portal` or `hermes auth add nous`, browser OAuth with loopback callback, refresh token in `~/.hermes/auth.json`, also enables the Tool Gateway), `openrouter` (`OPENROUTER_API_KEY` or `hermes auth add openrouter --type oauth`), `openai-api` (`OPENAI_API_KEY`), `openai-codex` (ChatGPT/Codex OAuth, device code or `--browser` PKCE; can import `~/.codex/auth.json`), `anthropic` (`ANTHROPIC_API_KEY`, or Claude Code OAuth chosen in `hermes model`, or `ANTHROPIC_TOKEN`), `copilot` (`COPILOT_GITHUB_TOKEN`/`GH_TOKEN`/`GITHUB_TOKEN` or device login), `copilot-acp`, `gemini`, `vertex`, `bedrock`, `azure-foundry`, `xai`/`xai-oauth`, `minimax`/`minimax-oauth`, `qwen-oauth`, `deepseek`, `huggingface`, `nvidia`, `ollama-cloud`, `lmstudio`, plus ~25 others, and `custom` (any OpenAI-compatible base URL; local Ollama `http://localhost:11434/v1`, vLLM :8000, SGLang :30000, llama-server :8080 with `--jinja`, LM Studio :1234). Keys live in `~/.hermes/.env`; OAuth tokens in `~/.hermes/auth.json`; provider/endpoint settings in `~/.hermes/config.yaml` (`model.provider`, `model.default`, `model.base_url`, `providers.*`, `fallback_providers:`); `hermes config set OPENROUTER_API_KEY …` writes `.env`; `hermes status` / `hermes config get model --json` show the active choice [docs: providers, configuration, configuring-models]. `hermes setup` is the full wizard; `hermes model` the provider/model/effort picker. Policy: the providers page states that Claude Max via Anthropic OAuth uses only purchased extra-usage credits, not the base allowance, and "Claude Pro subscribers cannot use this path" (use an API key) [docs: providers]; this follows Anthropic's April 2026 cut-off of Pro/Max subscription limits for third-party harnesses (OpenClaw first, then all) [2nd: https://cybersecuritynews.com/claude-ends-openclaw-subscriptions/], and Hermes issue #25267 (opened 2026-05-13, labelled `needs-decision`/`blocked`) records that the later Agent SDK monthly credit had no Hermes route yet [2nd: https://github.com/NousResearch/hermes-agent/issues/25267]. The docs carry no equivalent warning for ChatGPT/Codex OAuth.

**(8) Install.** Linux/macOS/WSL2: `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` (flags `--channel main`, `--non-interactive`, `--skip-browser`, `--skip-computer-use`, `--include-desktop`, `--dir`, `--verbose`; env `HERMES_INSTALL_CHANNEL`, `HERMES_INSTALL_VERBOSE`); then `source ~/.bashrc` (or `~/.zshrc`) and run `hermes` [docs: https://hermes-agent.nousresearch.com/docs/getting-started/installation, README]. Windows native: `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`. Docker: `docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup`, then `docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent` (tags `latest`, `stable`, `main`, `X.Y.Z`; gateway via `… nousresearch/hermes-agent gateway run -p 8642:8642`) [docs: https://hermes-agent.nousresearch.com/docs/user-guide/docker]. Termux (aarch64): signed APT repo, `pkg install hermes-agent`; Nix flake (Tier 2). PyPI (`pip install`, `uv tool install`) and Homebrew are listed as *unsupported* [docs: platform-support]. Python: installer provisions 3.14; `pyproject` allows `>=3.11,<3.15` but only 3.14 is supported at runtime [docs: installation]. Platforms: Tier 1 macOS Apple Silicon, Windows 10/11 x86_64/aarch64, Linux/WSL2 x86_64/aarch64, Docker; Intel macOS gets CLI only [docs: platform-support]. Update: `hermes update` (`--check`, `--set-channel stable|main`, `--backup`); Docker/Nix/Termux update via their package path [docs: updating]. Gateway service: `hermes gateway install` (Linux systemd user unit `hermes-gateway` under `~/.config/systemd/user`, macOS `~/Library/LaunchAgents/ai.hermes.gateway.plist`), `sudo hermes gateway install --system`, `hermes gateway start|stop|status`, `sudo loginctl enable-linger $USER` for headless hosts [docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging]. Uninstall: `hermes uninstall [--dry-run|--full|--data]`.

**Exit codes.** `hermes chat` one-shot/quiet: `0` completed; `1` failed, partial, run budget hit, or init/`--resume` miss ("No session found"); `3` input required (clarify or approval in a finite run; detached without cancelling) [src: `gateway_chat_view.py`]; `2` unsupported gateway-client option or slash command (`Unsupported gateway CLI options: …`); `3` turn lost its owner while queued (gateway mode); `75` Kanban worker hit provider rate limit/quota; `130` interrupted. `hermes -z`: `0` completed; `1` completed with no text; `2` failed/partial/budget/usage error; `130` interrupted. `stream-json` `result.exit_code` equals the process exit code. `hermes doctor`: `0` clean, `1` problems. `hermes update`: `0`/`1`/`2` (working-tree changes block pull). `hermes serve`: `75` port in use [docs: https://hermes-agent.nousresearch.com/docs/reference/cli-commands, user-guide/cli].

**Open questions** (not confirmed on 2026-10-19; do not hard-code):
- (resolved 2026-10-19 from source `hermes_cli/cli_single_query.py`) `-Q` prints only the final response on stdout and `session_id:` on stderr; without `-Q` or `--format`, tool previews reach stdout. Bare `-q` on non-TTY stdio implies `--oneshot` but not `-Q`.
- (resolved 2026-10-19 from source `hermes_cli/_parser.py`) `--reasoning` on `hermes chat` and top level takes `none|minimal|low|medium|high|xhigh|max|ultra`; an unknown value warns and keeps the configured level.
- (resolved 2026-10-19 from source `hermes_cli/_parser.py`) `--run-budget` is `type=float`, seconds. Moot for bridging: the gateway client refuses it (see (7)). Whether the gateway that `hermes chat`/`hermes -z` auto-starts exits when idle after a one-shot is UNVERIFIED (`hermes gateway stop` stops it).
- (RESOLVED 2026-10-19 from source `agent/skill_utils.py`, `tools/skills_tool.py`) A category subdirectory under `~/.hermes/skills/` is not required: the walk is recursive and a flat `~/.hermes/skills/<name>/SKILL.md` is listed under `general`.
- `delegation.max_concurrent_children` default: delegation page says 10, configuration page and environment-variables page say 3.
- Exact public launch date (2026-02-25 appears only in secondary coverage; the GitHub releases list starts at `v2026.3.12`). Tried: README, releases API, web search.
- (RESOLVED 2026-10-19 from source `gateway/run_config_loaders.py` and reference/environment-variables) `HERMES_EPHEMERAL_SYSTEM_PROMPT` / `ephemeral_system_prompt` is inline text (not a path), added at API-call time and never persisted.
- Whether `delegate_task` children see the `<available_skills>` index. Source suggests yes; not run.
- Whether a resumed session (`-r`/`-c`) re-reads a `SOUL.md` changed since it started.
- Whether skill slash commands run in the gateway-client `hermes chat` (since v0.21). Source paths exist; not run.
- Whether `hermes chat` has any `--no-save`/ephemeral switch; none documented — one-shot sessions are merely tagged `oneshot`.
- Docs page versions/dates: the docs site shows no version or last-updated stamp; facts were read on 2026-10-19 against the site live at that time (latest release v0.22.2, 2026-10-15).

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
| OpenClaw | yes | `<workspace>/skills/`, `<workspace>/.agents/skills/` (a repo passed with `agent exec --cwd` is that run's workspace: inferred, UNVERIFIED) | `~/.agents/skills/`, `~/.openclaw/skills/` | no (import only, `openclaw migrate claude`) | yes | `user-invocable`, `disable-model-invocation`, `command-dispatch`, `command-tool`, `command-arg-mode`, `metadata.openclaw.{requires, primaryEnv, always, os, emoji, skillKey, install}` |
| Hermes Agent | yes | `<root>/.hermes/skills/`, `<root>/.agents/skills/` (after `hermes skills trust`) | `~/.hermes/skills/<category>/<name>/` (+ `skills.external_dirs`) | no (import only, `hermes import-agent claude-code`) | project yes; `~/.agents/skills` only via `skills.external_dirs` | `platforms`, `required_environment_variables`, `metadata.hermes.{tags, category, requires_toolsets, fallback_for_toolsets, config, blueprint}` |

**Portable placement rule.** Keep skills in one canonical source. Render them to **`.agents/skills/`** (Codex, Cursor, Gemini, Antigravity, OpenCode, Pi, OpenClaw) **and** `.claude/skills/` (Claude Code; also read by Cursor, OpenCode and Grok). A symlink or copy covers nine of the ten; Hermes wants its own category dir under `~/.hermes/skills/` unless `skills.external_dirs` lists `~/.agents/skills`. Keep frontmatter to spec fields, plus `disable-model-invocation` (understood by Claude, Cursor and Pi). Put harness-specific fields only in the adapter-rendered copy.

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
| OpenClaw | yes | Workspace `AGENTS.md` is the standing-instructions file (every session, 20k-char cap); with `agent exec --cwd <dir>` that dir's `AGENTS.md` is appended as project context; `CLAUDE.md` never read; `TOOLS.md`/`HEARTBEAT.md` retired |
| Hermes Agent | yes | first match per dir of `.hermes.md`/`HERMES.md` > `AGENTS.override.md` > `AGENTS.md` > `CLAUDE.md` > `.cursorrules`; merged chain git root to cwd; 20K–500K-char dynamic cap; `--ignore-rules` skips; also given to subagents |

The agents.md site also lists Jules, Factory, Aider, goose, Zed, Warp, VS Code/Copilot, Devin, Windsurf, Junie, Amp, RooCode, Kilo Code, Augment and others.

**Portable rule.** Write one root `AGENTS.md`. Then either have `CLAUDE.md` contain `@AGENTS.md`, or ship no `CLAUDE.md` at all; both work for Claude Code. Watch out: a user-local `CLAUDE.local.md` turns off Claude's AGENTS.md reading unless `instructionFiles` is changed.

## B.3 Emerging shared conventions (2026)

- **`.agents/` as a neutral directory.** It is the shared skills path. Antigravity also uses `.agents/mcp_config.json`. Claude Code does not read `.agents/`.
- **Claude Code compatibility as a de facto standard.** Grok Build reads `.claude/` (skills, agents, plugins, hooks, settings permissions), `CLAUDE.md` and `.mcp.json` wholesale. Cursor reads `.claude/skills` and `.claude/agents`. OpenCode reads `.claude/skills` and `CLAUDE.md`. Pi reads `CLAUDE.md`. Claude Code now offers `claude import [codex|...]` to pull config the other way. The assistant runtimes import instead of reading live: `openclaw migrate claude` and `hermes import-agent claude-code|codex` copy skills, `CLAUDE.md` and MCP servers once.
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
| **OpenClaw** → `openclaw agent exec` | `printf '%s\n' "<P>" \| openclaw agent exec --cwd <D> --model <provider/model> --thinking <E> --json --timeout 1200 --config-override '{"tools":{"deny":["group:runtime","write","edit","apply_patch"]}}' --message-file -` | No flag; the `--config-override` tool deny list. Deny wins over profile and allow; `group:runtime` = `exec`, `process`, `code_execution`; `write`/`edit`/`apply_patch` are separate ids; `read` stays `[docs]` tool-policy. Combination not run (UNVERIFIED). `exec` defaults: `coding` profile, file tools limited to `<D>`, full host exec | `--model <provider/model>` | `--thinking off\|minimal\|low\|medium\|high` plus provider levels (`xhigh`, `adaptive`, `max`, `ultra`; clamped) | `--json` → `.final` (also `.payloads[].text`); check `.ok` | Stored auth profiles (`openclaw models auth login`) and ordinary config by default; `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` with `--auth-env-only` (loads no config, so no deny list) | **`--timeout <s>`** default 600 per model attempt; exit 2 = timeout. Temp state dir, no Gateway conflict unless `--state-dir` |
| **Hermes Agent** → `hermes chat` / `hermes -z` | `{ printf '%s\n\n' "<P>"; git diff; } \| hermes chat --in <D> --oneshot -Q --ignore-rules --source tool --toolsets safe -m <M> --provider <id> --reasoning <E> --max-turns 60 --format stream-json --query-file -` (prompt plus diff on stdin); or `hermes -z "<P>" --in <D> -t safe --ignore-rules -m <M> --provider <id>` (final text only; `-z` does not read stdin, so put the content in the argument or use `--query-file -`) | `--toolsets safe` (no file, no terminal; pipe the content in). **No read-only file toolset exists**: `file` includes `write_file`/`patch`; `HERMES_WRITE_SAFE_ROOT` only guards those two and must be in the gateway's environment (the client drops `HERMES_*` names) [src: `session_client_env.py`] | `-m <model>` (`provider/model` or bare) with `--provider <id>`; `-z` needs `-m` when `--provider` is given | `--reasoning none\|minimal\|low\|medium\|high\|xhigh\|max\|ultra` (source) | `--format stream-json` → last line `result`, `.text` (`.exit_code`); or `hermes -z` → bare text | `~/.hermes/.env` keys or OAuth via `hermes model` (Nous Portal, Codex, Copilot; Claude Max extra-usage only, Pro not allowed) | **No wall clock**: `--run-budget` is refused by the gateway client (exit 2); use the outer timeout plus `--max-turns N`. Every run is a gateway client and auto-starts the profile's gateway. `chat -q` denies approvals (`--yolo` to allow); `-z` bypasses them |

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
| OpenClaw | `agent exec` defaults (writes under `--cwd`, host exec); `--config-override '{"tools":{"profile":"full"}}'` for everything |
| Hermes | `--yolo` with `--toolsets file,terminal,web,search` (approvals otherwise denied in `-q`); `-w` for a git worktree |

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
  - `--thinking`: Pi, OpenClaw (`off|minimal|low|medium|high` plus provider levels)
  - `--reasoning`: Hermes (level names UNVERIFIED on the flag)
  - none: Cursor, Gemini
- JSON answer fields differ:
  - `.result`: Claude, Cursor
  - `.response`: Gemini, Antigravity
  - `.text`: Grok
  - `.final`: OpenClaw `agent exec --json` (one object)
  - event streams only: Codex `--json`, OpenCode, Pi, Hermes `--format stream-json` (last line is a `result` object with `.text`). For these, use Codex `-o file` or plain stdout, Pi `-p` plain text, and Hermes `-z` or the last JSONL line.
- Working-dir handling differs:
  - flags: `-C` (Codex), `--workspace` (Cursor), `--dir` (OpenCode), `--cwd` (Grok, Antigravity, OpenClaw `agent exec`), `--in` (Hermes)
  - **`cd` required:** Claude, Gemini, Pi
  - **none at all:** OpenClaw's Gateway path (`openclaw agent --agent <id>`) uses the agent's configured workspace
- Codex requires a git repo unless `--skip-git-repo-check`.
- `-p` is `--profile` in Hermes as well as Codex; Hermes's prompt flag is `-q`, and `-Q` is quiet.
- OpenClaw `agent exec` runs against a temporary state dir and does not conflict with a running Gateway (only `--state-dir` and `agent --local` do); Hermes `chat -q` denies approvals instead of asking, and `hermes -z` bypasses them. Hermes `chat` and `-z` are gateway clients: the first call starts the profile's gateway, and `--run-budget`/`-w` are refused there.

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
- OpenClaw: https://docs.openclaw.ai (pages cited in §9; append `.md` to a page URL for raw Markdown) · https://github.com/openclaw/openclaw · [2nd] https://en.wikipedia.org/wiki/OpenClaw
- Hermes Agent: https://hermes-agent.nousresearch.com/docs (pages cited in §10) · https://github.com/NousResearch/hermes-agent
- Standards: https://agentskills.io/specification · https://agents.md
