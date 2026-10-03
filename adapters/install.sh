#!/bin/sh
# agent-orchestration adapter installer (POSIX sh).
#
#   sh adapters/install.sh <harness> [--kit-root PATH] [--dry-run]
#
# Harnesses: codex cursor opencode pi grok agy (alias: antigravity) gemini claude
#
# For each harness it:
#   1. resolves KIT_ROOT (default: the repo this script lives in)
#   2. copies adapters/_shared/skills/* into the harness's global skills dir,
#      with the KIT_ROOT placeholder substituted
#   3. appends adapters/_shared/AGENTS.fragment.md (KIT_ROOT substituted) to
#      the harness's global instructions file, unless the marker line
#      "<!-- agent-orchestration -->" is already there
#   4. prints what it did and what to do next
#
# It never overwrites a file: skills that already exist are skipped (and
# reported as up to date or different), instruction files are only appended
# to or created.
#
# Every path below cites research/harnesses.md (Part A section numbers).
# Paths the research leaves unconfirmed are marked UNVERIFIED and produce a
# runtime warning.

set -eu

MARKER='<!-- agent-orchestration -->'

usage() {
  cat <<'EOF'
usage: sh adapters/install.sh <harness> [--kit-root PATH] [--dry-run]

harness: codex | cursor | opencode | pi | grok | agy | antigravity | gemini | claude

  --kit-root PATH   kit location written into the installed files
                    (default: the repo containing this script)
  --dry-run         print what would happen; change nothing
EOF
}

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
say() { printf '%s\n' "$*"; }
warn() { printf 'WARNING: %s\n' "$*"; WARNINGS=$((WARNINGS + 1)); }

# ---------------------------------------------------------------- arguments

HARNESS=''
KIT_ROOT=''
DRY=0
WARNINGS=0

while [ $# -gt 0 ]; do
  case "$1" in
    --kit-root)
      [ $# -ge 2 ] || die '--kit-root needs a path'
      KIT_ROOT=$2; shift 2 ;;
    --kit-root=*)
      KIT_ROOT=${1#--kit-root=}; shift ;;
    --dry-run|-n)
      DRY=1; shift ;;
    -h|--help)
      usage; exit 0 ;;
    -*)
      usage >&2; die "unknown option: $1" ;;
    *)
      [ -z "$HARNESS" ] || die "only one harness per run (got '$HARNESS' and '$1')"
      HARNESS=$1; shift ;;
  esac
done

[ -n "$HARNESS" ] || { usage >&2; exit 2; }
[ -n "${HOME:-}" ] || die 'HOME is not set'

# ---------------------------------------------------------------- kit root

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SHARED="$SCRIPT_DIR/_shared"

if [ -z "$KIT_ROOT" ]; then
  KIT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
else
  [ -d "$KIT_ROOT" ] || die "--kit-root does not exist: $KIT_ROOT"
  KIT_ROOT=$(CDPATH= cd -- "$KIT_ROOT" && pwd)
fi

[ -f "$KIT_ROOT/core/interview/setup-interview.md" ] ||
  die "not a kit root (no core/interview/setup-interview.md): $KIT_ROOT"
[ -f "$SHARED/AGENTS.fragment.md" ] || die "missing $SHARED/AGENTS.fragment.md"
[ -d "$SHARED/skills" ] || die "missing $SHARED/skills"

case "$KIT_ROOT" in
  *'
'*) die 'kit root path contains a newline' ;;
esac

# Escape the path for use as a sed replacement with '|' as delimiter.
KIT_ROOT_SED=$(printf '%s\n' "$KIT_ROOT" | sed -e 's/[\\&|]/\\&/g')

render() { # render <src> <dst>: substitute KIT_ROOT, write dst via temp + mv
  _tmp="$2.ao-tmp.$$"
  sed -e "s|KIT_ROOT|$KIT_ROOT_SED|g" "$1" > "$_tmp"
  mv "$_tmp" "$2"
}

# ---------------------------------------------------------------- harness table
#
# SKILLS_DIR    global skills dir (Agent Skills SKILL.md)
# INSTR_FILE    global instructions file the fragment is appended to
#               ('' = harness has no documented global instructions file)
# INVOKE        how the user invokes a skill named <name> in that harness
# *_UNVERIFIED  non-empty reason when the research could not confirm the path

SKILLS_DIR=''
INSTR_FILE=''
INVOKE=''
SKILLS_UNVERIFIED=''
INSTR_UNVERIFIED=''
INVOKE_UNVERIFIED=''
README_DIR=$HARNESS

case "$HARNESS" in
  claude)
    # §1 and README.md "Install (Claude Code)": the repo root is the plugin.
    say 'Claude Code uses the plugin at the repo root, not this installer. Run:'
    say ''
    say '  claude plugin marketplace add <github-user>/agent-orchestration'
    say '  claude plugin install agent-orchestration@agent-orchestration'
    say ''
    say 'Then, in any session:  /agent-orchestration:setup'
    say 'The plugin SessionStart hook (hooks/hooks.json) loads your routing table.'
    exit 0 ;;

  codex)
    # §2(2): user skills at $HOME/.agents/skills. The legacy ~/.codex/skills/
    # is no longer in the docs, so it is not used.
    SKILLS_DIR="$HOME/.agents/skills"
    # §2(1): global ~/.codex/AGENTS.override.md, else ~/.codex/AGENTS.md.
    INSTR_FILE="$HOME/.codex/AGENTS.md"
    # §2(2): "$skill-name or /skills".
    INVOKE='$<name>  (or pick it from /skills)' ;;

  cursor)
    # §3(2): user skills at ~/.cursor/skills/ or ~/.agents/skills/; the
    # cross-harness path is used.
    SKILLS_DIR="$HOME/.agents/skills"
    # §3(1): global instructions are User Rules in settings, not a file.
    INSTR_FILE=''
    # §3(2): "/skill-name or @skill-name".
    INVOKE='/<name>  (or @<name>)' ;;

  opencode)
    # §5(2): ~/.config/opencode/skills/ is documented; ~/.agents/skills is
    # only implied (UNVERIFIED), so the native path is used.
    SKILLS_DIR="$HOME/.config/opencode/skills"
    # §5(1): global ~/.config/opencode/AGENTS.md (falls back to
    # ~/.claude/CLAUDE.md only when absent).
    INSTR_FILE="$HOME/.config/opencode/AGENTS.md"
    # §5: no explicit skill-invocation syntax in the research.
    INVOKE='ask for it by name, e.g. "use the <name> skill"'
    INVOKE_UNVERIFIED='research §5 gives no explicit skill-invocation syntax for OpenCode' ;;

  pi)
    # §6(2): ~/.pi/agent/skills/ or ~/.agents/skills/; cross-harness path used.
    SKILLS_DIR="$HOME/.agents/skills"
    # §6(1): agent dir ~/.pi/agent (override PI_CODING_AGENT_DIR) holds AGENTS.md.
    INSTR_FILE="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/AGENTS.md"
    # §6(2): "/skill:name args".
    INVOKE='/skill:<name>' ;;

  grok)
    # §7(2): user skills at ~/.grok/skills/.
    SKILLS_DIR="$HOME/.grok/skills"
    # §7(1): "Global rules live in ~/.grok/" and the per-directory filenames
    # are Agents.md, Claude.md, AGENT.md, AGENTS.md. The exact global
    # filename is not stated, so ~/.grok/AGENTS.md is UNVERIFIED.
    INSTR_FILE="$HOME/.grok/AGENTS.md"
    INSTR_UNVERIFIED='research §7(1) says global rules live in ~/.grok/ but does not name the file; check that grok loads ~/.grok/AGENTS.md (grok inspect)'
    # §7(2): "/skills, /skill-name".
    INVOKE='/<name>' ;;

  agy|antigravity)
    HARNESS=agy
    README_DIR=antigravity
    # §4b: global skills ~/.gemini/antigravity-cli/skills/.
    SKILLS_DIR="$HOME/.gemini/antigravity-cli/skills"
    # §4b: global ~/.gemini/GEMINI.md (shared with Gemini CLI).
    INSTR_FILE="$HOME/.gemini/GEMINI.md"
    INVOKE='ask for it by name, e.g. "use the <name> skill"'
    INVOKE_UNVERIFIED='research §4b gives no explicit skill-invocation syntax for Antigravity' ;;

  gemini)
    # §4(2): user tier ~/.gemini/skills/ or ~/.agents/skills/ (.agents wins).
    SKILLS_DIR="$HOME/.agents/skills"
    # §4(1): global ~/.gemini/GEMINI.md.
    INSTR_FILE="$HOME/.gemini/GEMINI.md"
    INVOKE='ask for it by name, e.g. "use the <name> skill"  (/skills list shows them)'
    INVOKE_UNVERIFIED='research §4(2) lists /skills list|enable|reload but no per-skill invocation syntax' ;;

  *)
    usage >&2; die "unknown harness: $HARNESS" ;;
esac

# ---------------------------------------------------------------- header

if [ "$DRY" -eq 1 ]; then
  say "agent-orchestration install: $HARNESS (dry run, nothing will change)"
else
  say "agent-orchestration install: $HARNESS"
fi
say "  kit root:     $KIT_ROOT"
say "  skills dir:   $SKILLS_DIR"
say "  instructions: ${INSTR_FILE:-none (see below)}"
say ''

# ---------------------------------------------------------------- harness warnings

[ -n "$SKILLS_UNVERIFIED" ] && warn "$SKILLS_UNVERIFIED"
[ -n "$INSTR_UNVERIFIED" ] && warn "$INSTR_UNVERIFIED"
[ -n "$INVOKE_UNVERIFIED" ] && warn "$INVOKE_UNVERIFIED (UNVERIFIED)"

case "$HARNESS" in
  codex)
    # §2(1): first non-empty of AGENTS.override.md, AGENTS.md wins.
    if [ -s "$HOME/.codex/AGENTS.override.md" ]; then
      warn "~/.codex/AGENTS.override.md exists and is non-empty, so Codex ignores ~/.codex/AGENTS.md. Copy the agent-orchestration block into the override file by hand."
    fi
    # §2 Auth: CODEX_HOME relocates Codex config; whether AGENTS.md follows is UNVERIFIED.
    if [ -n "${CODEX_HOME:-}" ] && [ "$CODEX_HOME" != "$HOME/.codex" ]; then
      warn "CODEX_HOME=$CODEX_HOME is set; Codex may read AGENTS.md from there instead of ~/.codex (UNVERIFIED)."
    fi ;;
  opencode)
    # §5(1): ~/.claude/CLAUDE.md is only a fallback when the OpenCode file is absent.
    if [ ! -e "$INSTR_FILE" ] && [ -f "$HOME/.claude/CLAUDE.md" ]; then
      warn "creating $INSTR_FILE will stop OpenCode falling back to ~/.claude/CLAUDE.md. If you relied on that, add it to \"instructions\" in ~/.config/opencode/opencode.json."
    fi ;;
  pi)
    # §6(1): AGENTS.override.md replaces AGENTS.md in the same directory.
    if [ -e "${INSTR_FILE%/*}/AGENTS.override.md" ]; then
      warn "${INSTR_FILE%/*}/AGENTS.override.md exists and replaces AGENTS.md there. Copy the agent-orchestration block into it by hand."
    fi ;;
  agy|gemini)
    # §4 / §4b: Gemini CLI and Antigravity share ~/.gemini/GEMINI.md, so the
    # marker check makes a second install a no-op for that file.
    : ;;
esac

# ---------------------------------------------------------------- 1. skills

SK_NEW=0; SK_SAME=0; SK_DIFF=0

say 'Skills:'
for skill_dir in "$SHARED"/skills/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  name=$(basename "$skill_dir")
  # Every file in the skill dir (SKILL.md plus any references/ or scripts/).
  for src in $(cd "$skill_dir" && find . -type f | sed 's|^\./||' | sort); do
    dst="$SKILLS_DIR/$name/$src"
    if [ -e "$dst" ]; then
      if [ "$DRY" -eq 0 ]; then
        _cmp="$dst.ao-cmp.$$"
        sed -e "s|KIT_ROOT|$KIT_ROOT_SED|g" "$skill_dir/$src" > "$_cmp"
        if cmp -s "$_cmp" "$dst"; then
          say "  up to date  $dst"; SK_SAME=$((SK_SAME + 1))
        else
          say "  SKIPPED     $dst (exists and differs; delete it and re-run to update)"
          SK_DIFF=$((SK_DIFF + 1))
        fi
        rm -f "$_cmp"
      else
        say "  would skip  $dst (exists)"; SK_SAME=$((SK_SAME + 1))
      fi
    else
      if [ "$DRY" -eq 1 ]; then
        say "  would create $dst"
      else
        mkdir -p "$(dirname "$dst")"
        render "$skill_dir/$src" "$dst"
        say "  created     $dst"
      fi
      SK_NEW=$((SK_NEW + 1))
    fi
  done
done
[ "$SK_DIFF" -gt 0 ] && warn "$SK_DIFF skill file(s) already exist with different content and were left alone."
say ''

# ---------------------------------------------------------------- 2. instructions

say 'Instructions:'
if [ -n "$INSTR_FILE" ]; then
  if [ -f "$INSTR_FILE" ] && grep -qF "$MARKER" "$INSTR_FILE"; then
    say "  already present in $INSTR_FILE (marker found); unchanged"
  else
    if [ -f "$INSTR_FILE" ]; then action='append to'; else action='create'; fi
    if [ "$DRY" -eq 1 ]; then
      say "  would $action $INSTR_FILE ($(wc -l < "$SHARED/AGENTS.fragment.md" | tr -d ' ') lines, marker $MARKER)"
    else
      mkdir -p "$(dirname "$INSTR_FILE")"
      frag="$INSTR_FILE.ao-frag.$$"
      sed -e "s|KIT_ROOT|$KIT_ROOT_SED|g" "$SHARED/AGENTS.fragment.md" > "$frag"
      if [ -s "$INSTR_FILE" ]; then
        # Ensure the existing file ends with a newline, then a blank line.
        if [ "$(tail -c 1 "$INSTR_FILE" | wc -l | tr -d ' ')" -eq 0 ]; then
          printf '\n' >> "$INSTR_FILE"
        fi
        printf '\n' >> "$INSTR_FILE"
      fi
      cat "$frag" >> "$INSTR_FILE"
      rm -f "$frag"
      if [ "$action" = 'create' ]; then
        say "  created $INSTR_FILE with the agent-orchestration block"
      else
        say "  appended the agent-orchestration block to $INSTR_FILE"
      fi
    fi
  fi
else
  # Cursor (§3(1)): User Rules live in Cursor Settings, not in a file. Write
  # the rendered block into the kit's own config dir for the user to paste.
  rule="$HOME/.agent-orchestration/cursor-user-rule.md"
  if [ -e "$rule" ]; then
    say "  $rule exists; unchanged"
  elif [ "$DRY" -eq 1 ]; then
    say "  would create $rule (paste it into Cursor Settings > Rules > User Rules)"
  else
    mkdir -p "$(dirname "$rule")"
    render "$SHARED/AGENTS.fragment.md" "$rule"
    say "  created $rule"
  fi
  say '  Cursor has no global instructions file. Paste that file into'
  say '  Cursor Settings > Rules > User Rules (e.g. pbcopy < the file).'
  say '  Per project, a .cursor/rules/*.mdc rule with alwaysApply: true also'
  say '  works; see adapters/cursor/README.md.'
fi
say ''

# ---------------------------------------------------------------- 3. summary

skill_cmd=$(printf '%s' "$INVOKE" | sed -e 's/<name>/ao-setup/g')
if [ "$DRY" -eq 1 ]; then
  say "Dry run: $SK_NEW skill file(s) would be created, $SK_SAME already present."
else
  say "Done: $SK_NEW skill file(s) created, $SK_SAME up to date, $SK_DIFF skipped."
fi
[ "$WARNINGS" -gt 0 ] && say "$WARNINGS warning(s) above."
say ''
say 'Next:'
say "  1. Start a new $HARNESS session (skills and instructions load at start)."
say "  2. Run the ao-setup skill: $skill_cmd"
say '     It interviews you and writes ~/.agent-orchestration/routing.md.'
say '  3. From then on every session reads routing.md, glossary.md and lessons.md.'
say "  Details and optional upgrades: $KIT_ROOT/adapters/$README_DIR/README.md"
