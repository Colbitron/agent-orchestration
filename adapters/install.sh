#!/bin/sh
# agent-orchestration adapter installer (POSIX sh).
#
#   sh adapters/install.sh <harness> [--update] [--force] [--kit-root PATH] [--dry-run]
#
# Harnesses: codex cursor opencode pi grok agy (alias: antigravity) gemini openclaw hermes claude
#
# For each harness it:
#   1. resolves KIT_ROOT (default: the repo this script lives in)
#   2. copies adapters/_shared/skills/* into the harness's global skills dir,
#      with the KIT_ROOT placeholder substituted, and records the hash of each
#      installed file in <skills dir>/.agent-orchestration-manifest
#   3. appends adapters/_shared/AGENTS.fragment.md (KIT_ROOT substituted) to
#      the harness's global instructions file, unless the marker line
#      "<!-- agent-orchestration -->" is already there
#   4. prints what it did and what to do next
#
# A plain install never overwrites a file: skills that already exist are
# skipped (and reported as up to date or different), instruction files are
# only appended to or created.
#
# --update brings an earlier install up to date with this kit. A skill file
# whose hash still matches the manifest (never edited) is overwritten; one
# that was edited locally, or that the manifest does not cover, is skipped.
# The block between "<!-- agent-orchestration -->" and
# "<!-- /agent-orchestration -->" in the instructions file is replaced.
# --force implies --update and also overwrites locally edited skill files.
#
# The manifest's first line names the hash tool (shasum -a 256, sha256sum or
# cksum); every other line is "<hash> <path relative to the skills dir>".
#
# Every path below cites research/harnesses.md (Part A section numbers).
# Paths the research leaves unconfirmed are marked UNVERIFIED and produce a
# runtime warning.

set -eu

MARKER='<!-- agent-orchestration -->'
END_MARKER='<!-- /agent-orchestration -->'
MANIFEST_NAME='.agent-orchestration-manifest'
MANIFEST_HEAD='# agent-orchestration manifest; hash:'

usage() {
  cat <<'USAGE'
usage: sh adapters/install.sh <harness> [--update] [--force] [--kit-root PATH] [--dry-run]

harness: codex | cursor | opencode | pi | grok | agy | antigravity | gemini |
         openclaw | hermes | claude

  --update          update an earlier install: overwrite skill files you
                    have not edited (checked against the manifest), skip
                    edited ones, and replace the agent-orchestration block
                    in the instructions file
  --force           like --update, but also overwrite edited skill files
  --kit-root PATH   kit location written into the installed files
                    (default: the repo containing this script)
  --dry-run         print what would happen; change nothing
USAGE
}

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
say() { printf '%s\n' "$*"; }
warn() { printf 'WARNING: %s\n' "$*"; WARNINGS=$((WARNINGS + 1)); }

# ---------------------------------------------------------------- arguments

HARNESS=''
KIT_ROOT=''
DRY=0
UPDATE=0
FORCE=0
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
    --update|-u)
      UPDATE=1; shift ;;
    --force|-f)
      FORCE=1; UPDATE=1; shift ;;
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

render_out() { # render_out <src>: print src with KIT_ROOT substituted
  sed -e "s|KIT_ROOT|$KIT_ROOT_SED|g" "$1"
}

# ---------------------------------------------------------------- hashing

have() { command -v "$1" >/dev/null 2>&1; }

if have shasum; then SHA256_TOOL='shasum -a 256'
elif have sha256sum; then SHA256_TOOL='sha256sum'
else SHA256_TOOL=''
fi
HASH_TOOL=${SHA256_TOOL:-cksum}

hash_stdin() { # hash of stdin with $HASH_TOOL, as one word
  case "$HASH_TOOL" in
    cksum) cksum | awk '{ print $1 "-" $2 }' ;;
    *) $HASH_TOOL | awk '{ print $1 }' ;;
  esac
}

# ---------------------------------------------------------------- AGENTS.md block

block_ok() { # block_ok <file>: exactly one start marker line, then an end marker line
  M1=$MARKER M2=$END_MARKER awk '
    { l = $0; sub(/\r$/, "", l) }
    l == ENVIRON["M1"] { n++; if (s == 0) s = 1; next }
    s == 1 && l == ENVIRON["M2"] { s = 2 }
    END { exit (s == 2 && n == 1) ? 0 : 1 }' "$1"
}

render_block() { # render_block <file>: print file with its marked block replaced by the fragment
  render_out "$SHARED/AGENTS.fragment.md" |
    M1=$MARKER M2=$END_MARKER awk '
      NR == FNR { frag = frag $0 "\n"; next }
      { l = $0; sub(/\r$/, "", l) }
      s == 0 && l == ENVIRON["M1"] { printf "%s", frag; s = 1; next }
      s == 1 { if (l == ENVIRON["M2"]) s = 2; next }
      { print }' - "$1"
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
    say '  claude plugin marketplace add Colbitron/agent-orchestration'
    say '  claude plugin install agent-orchestration@agent-orchestration'
    say ''
    say 'Then, in any session:  /agent-orchestration:setup'
    say ''
    say 'To update later:  claude plugin update agent-orchestration'
    say 'then restart and run /agent-orchestration:refresh if profiles changed.'
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

  openclaw)
    # §9(2): managed skills dir ~/.openclaw/skills, shared by every agent
    # (workspace skills/ and .agents/skills rank higher).
    SKILLS_DIR="$HOME/.openclaw/skills"
    # §9(1): the default workspace's AGENTS.md is injected into every
    # Gateway session; OPENCLAW_WORKSPACE_DIR overrides the default
    # location. Its precedence against an explicit agents.defaults.workspace
    # is undocumented ('openclaw agents list' is the authority).
    # OPENCLAW_PROFILE and OPENCLAW_STATE_DIR are ignored here.
    # Other agents' workspaces have their own AGENTS.md.
    INSTR_FILE="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace}/AGENTS.md"
    # §9(2): /skill <name> always works; native command names are
    # sanitized to a-z0-9_, so ao-setup becomes /ao_setup.
    INVOKE='/skill <name>  (or the native command /ao_setup)' ;;

  hermes)
    # §10(2): ~/.hermes/skills/<category>/<name>/SKILL.md; HERMES_HOME
    # relocates ~/.hermes. The category is optional (the loader walks
    # skills/ recursively); the kit keeps agent-orchestration for grouping.
    SKILLS_DIR="${HERMES_HOME:-$HOME/.hermes}/skills/agent-orchestration"
    # §10(1): SOUL.md is the only global instructions file (system prompt
    # slot 1, verbatim, user-owned).
    INSTR_FILE="${HERMES_HOME:-$HOME/.hermes}/SOUL.md"
    # §10(2): every installed skill is a slash command.
    INVOKE='/<name>  (or hermes chat -s <name>)' ;;

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
  openclaw)
    # §9(1): OpenClaw seeds its default AGENTS.md template when it first
    # prepares the workspace and never overwrites an existing AGENTS.md.
    # A kit-created file would hold only the kit block, and OpenClaw's
    # default operating instructions would never be written. So refuse
    # until the seeded AGENTS.md exists.
    if [ ! -f "$INSTR_FILE" ]; then
      die "$INSTR_FILE does not exist. Run 'openclaw onboard' first so OpenClaw seeds it, then re-run."
    fi
    # Only the default workspace-<id> layout is detected here; custom
    # workspace: pins and <agents.defaults.workspace>/<id> are not.
    if [ -d "$HOME/.openclaw" ] && ls -d "$HOME"/.openclaw/workspace-* >/dev/null 2>&1; then
      warn "per-agent workspaces exist ($(ls -d "$HOME"/.openclaw/workspace-* | tr '\n' ' ' | sed 's/ $//')); each has its own AGENTS.md. This lists only the default layout; run 'openclaw agents list' to see every workspace. Copy the agent-orchestration block into the ones that should load the routing table."
    fi ;;
  hermes)
    # §10(1): Hermes seeds SOUL.md with its starter identity on first run and
    # never overwrites it. A SOUL.md holding only the kit block would become
    # the whole identity, so refuse until the seeded file exists.
    if [ ! -f "$INSTR_FILE" ]; then
      die "$INSTR_FILE does not exist. Run 'hermes' once (or 'hermes setup'; 'hermes -p <name>' when HERMES_HOME is a profile) so Hermes seeds it, then re-run."
    fi
    # §10(1): an untouched legacy scaffold is a '# Hermes Agent Persona'
    # heading plus an HTML comment (src: hermes_cli/default_soul.py); Hermes
    # stops auto-upgrading it once the kit block is appended. The awk exits 0
    # when any text remains outside <!-- --> comments, headings and blank lines.
    if [ "$(wc -c < "$INSTR_FILE" | tr -d ' ')" -lt 200 ] || ! awk '
        { l = $0
          while (l != "") {
            if (c) { i = index(l, "-->"); if (!i) { l = ""; break }; l = substr(l, i + 3); c = 0 }
            else { i = index(l, "<!--"); if (!i) break; if (substr(l, 1, i - 1) ~ /[^[:space:]]/) { t = 1 }; l = substr(l, i + 4); c = 1 }
          }
          if (l ~ /[^[:space:]]/ && l !~ /^[[:space:]]*#/) t = 1 }
        END { exit t ? 0 : 1 }' "$INSTR_FILE"; then
      warn "SOUL.md looks like the untouched scaffold; run 'hermes' once so it holds real content before appending the kit block."
    fi
    # §10(1): each profile has its own SOUL.md and skills/; only the given
    # home is installed into.
    if [ -z "${HERMES_HOME:-}" ] && [ -d "$HOME/.hermes/profiles" ] && ls -d "$HOME"/.hermes/profiles/*/ >/dev/null 2>&1; then
      warn "Hermes profiles found ($(cd "$HOME/.hermes/profiles" && ls -d */ | tr -d / | tr '\n' ' ' | sed 's/ $//')); this install targets the default home only. Set HERMES_HOME=~/.hermes/profiles/<name> to install into a profile."
    fi ;;
esac

# ---------------------------------------------------------------- manifest

MANIFEST="$SKILLS_DIR/$MANIFEST_NAME"
MAN_OK=0   # 1 when an existing manifest can be compared against

if [ -f "$MANIFEST" ]; then
  man_tool=$(sed -n "1s/^$MANIFEST_HEAD //p" "$MANIFEST")
  case "$man_tool" in
    cksum)
      HASH_TOOL=cksum; MAN_OK=1 ;;
    'shasum -a 256'|sha256sum)
      if [ -n "$SHA256_TOOL" ]; then MAN_OK=1
      else warn "$MANIFEST uses $man_tool, which is not available here; treating it as missing."
      fi ;;
    *)
      warn "$MANIFEST has no recognised header line; treating it as missing." ;;
  esac
elif [ "$UPDATE" -eq 1 ] && [ "$FORCE" -eq 0 ] && [ -d "$SKILLS_DIR" ]; then
  warn "no manifest at $MANIFEST (installed before manifests existed?), so every existing skill file that differs from this kit counts as possibly edited and is skipped. Re-run with --force to overwrite them."
fi

manifest_hash() { # manifest_hash <relpath>: recorded hash, or nothing
  [ "$MAN_OK" -eq 1 ] || return 0
  P=$1 awk 'NR > 1 {
      i = index($0, " ")
      if (i > 0 && substr($0, i + 1) == ENVIRON["P"]) { print substr($0, 1, i - 1); exit }
    }' "$MANIFEST"
}

NEWMAN=''
cleanup() { [ -z "$NEWMAN" ] || rm -f "$NEWMAN" "$NEWMAN.all"; }
trap cleanup EXIT
trap 'exit 130' INT TERM

if [ "$DRY" -eq 0 ]; then
  mkdir -p "$SKILLS_DIR"
  NEWMAN="$MANIFEST.ao-tmp.$$"
  : > "$NEWMAN"
fi

record() { # record <hash> <relpath>: manifest entry for the content now installed
  [ "$DRY" -eq 1 ] || printf '%s %s\n' "$1" "$2" >> "$NEWMAN"
}

# ---------------------------------------------------------------- 1. skills

SK_NEW=0; SK_SAME=0; SK_UPD=0; SK_DIFF=0

did() { # did <past> <dry-run> <path>: report an action, worded for --dry-run
  if [ "$DRY" -eq 1 ]; then printf '  %-17s %s\n' "$2" "$3"
  else printf '  %-11s %s\n' "$1" "$3"; fi
}

say 'Skills:'
for skill_dir in "$SHARED"/skills/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  name=$(basename "$skill_dir")
  # Every file in the skill dir (SKILL.md plus any references/ or scripts/).
  for src in $(cd "$skill_dir" && find . -type f | sed 's|^\./||' | sort); do
    rel="$name/$src"
    dst="$SKILLS_DIR/$rel"
    new_hash=$(render_out "$skill_dir/$src" | hash_stdin)
    if [ ! -e "$dst" ]; then
      if [ "$DRY" -eq 0 ]; then
        mkdir -p "$(dirname "$dst")"
        render "$skill_dir/$src" "$dst"
      fi
      did created 'would create' "$dst"
      record "$new_hash" "$rel"; SK_NEW=$((SK_NEW + 1))
    elif render_out "$skill_dir/$src" | cmp -s - "$dst"; then
      did 'up to date' 'up to date' "$dst"
      record "$new_hash" "$rel"; SK_SAME=$((SK_SAME + 1))
    elif [ "$UPDATE" -eq 0 ]; then
      did SKIPPED 'would skip' "$dst (exists and differs; run with --update to update it)"
      SK_DIFF=$((SK_DIFF + 1))
    else
      old_hash=$(manifest_hash "$rel")
      cur_hash=$(hash_stdin < "$dst")
      if [ "$FORCE" -eq 0 ] && [ -z "$old_hash" ]; then
        did SKIPPED 'would skip' "$dst (not in the manifest, so it may be edited locally; use --force to overwrite)"
        SK_DIFF=$((SK_DIFF + 1))
      elif [ "$FORCE" -eq 0 ] && [ "$cur_hash" != "$old_hash" ]; then
        did SKIPPED 'would skip' "$dst (edited locally; use --force to overwrite)"
        SK_DIFF=$((SK_DIFF + 1))
      else
        [ "$DRY" -eq 1 ] || render "$skill_dir/$src" "$dst"
        if [ "$cur_hash" = "$old_hash" ]; then did updated 'would update' "$dst"
        else did overwritten 'would overwrite' "$dst"; fi
        record "$new_hash" "$rel"; SK_UPD=$((SK_UPD + 1))
      fi
    fi
  done
done

# The new manifest: entries for what is installed now, plus earlier entries
# for files this run did not write (skipped files keep their old hash, so a
# later --update still sees the local edit).
if [ "$DRY" -eq 1 ]; then
  did '' 'would write' "$MANIFEST"
else
  {
    printf '%s %s\n' "$MANIFEST_HEAD" "$HASH_TOOL"
    cat "$NEWMAN"
    if [ "$MAN_OK" -eq 1 ]; then
      awk 'NR == FNR { i = index($0, " "); seen[substr($0, i + 1)] = 1; next }
           FNR > 1 { i = index($0, " "); if (i > 0 && !(substr($0, i + 1) in seen)) print }' \
        "$NEWMAN" "$MANIFEST"
    fi
  } > "$NEWMAN.all"
  mv "$NEWMAN.all" "$MANIFEST"
  did manifest '' "$MANIFEST ($HASH_TOOL)"
fi

if [ "$SK_DIFF" -gt 0 ]; then
  if [ "$UPDATE" -eq 0 ]; then
    warn "$SK_DIFF skill file(s) differ from this kit and were left alone. Run with --update to update the ones you have not edited."
  else
    warn "$SK_DIFF skill file(s) may have local edits and were left alone. Compare them with $SHARED/skills, then re-run with --force to overwrite."
  fi
fi
say ''

# ---------------------------------------------------------------- 2. instructions

say 'Instructions:'
if [ -n "$INSTR_FILE" ]; then
  if [ -f "$INSTR_FILE" ] && grep -qF "$MARKER" "$INSTR_FILE"; then
    if [ "$UPDATE" -eq 0 ]; then
      say "  already present in $INSTR_FILE (marker found); unchanged (--update replaces it)"
    elif ! block_ok "$INSTR_FILE"; then
      warn "$INSTR_FILE does not hold exactly one block from a $MARKER line to a $END_MARKER line; left unchanged. Fix the block by hand, then re-run."
    elif render_block "$INSTR_FILE" | cmp -s - "$INSTR_FILE"; then
      say "  up to date in $INSTR_FILE"
    elif [ "$DRY" -eq 1 ]; then
      say "  would replace the agent-orchestration block in $INSTR_FILE"
    else
      blk="$INSTR_FILE.ao-blk.$$"
      render_block "$INSTR_FILE" > "$blk"
      # cat, not mv: keeps the file's permissions and any symlink.
      cat "$blk" > "$INSTR_FILE"
      rm -f "$blk"
      say "  replaced the agent-orchestration block in $INSTR_FILE"
    fi
  else
    if [ -f "$INSTR_FILE" ]; then action='append to'; else action='create'; fi
    if [ "$DRY" -eq 1 ]; then
      say "  would $action $INSTR_FILE ($(wc -l < "$SHARED/AGENTS.fragment.md" | tr -d ' ') lines, marker $MARKER)"
    else
      mkdir -p "$(dirname "$INSTR_FILE")"
      frag="$INSTR_FILE.ao-frag.$$"
      render_out "$SHARED/AGENTS.fragment.md" > "$frag"
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
  if [ ! -e "$rule" ]; then
    if [ "$DRY" -eq 1 ]; then
      say "  would create $rule (paste it into Cursor Settings > Rules > User Rules)"
    else
      mkdir -p "$(dirname "$rule")"
      render "$SHARED/AGENTS.fragment.md" "$rule"
      say "  created $rule"
    fi
  elif render_out "$SHARED/AGENTS.fragment.md" | cmp -s - "$rule"; then
    say "  $rule is up to date"
  elif [ "$UPDATE" -eq 0 ]; then
    say "  $rule exists and differs; unchanged (--update rewrites it)"
  elif [ "$DRY" -eq 1 ]; then
    say "  would rewrite $rule (then paste it into Cursor again)"
  else
    render "$SHARED/AGENTS.fragment.md" "$rule"
    say "  rewrote $rule; paste it into Cursor again"
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
  say "Dry run: $SK_NEW skill file(s) would be created, $SK_UPD updated, $SK_SAME already up to date, $SK_DIFF skipped."
else
  say "Done: $SK_NEW skill file(s) created, $SK_UPD updated, $SK_SAME up to date, $SK_DIFF skipped."
fi
[ "$WARNINGS" -gt 0 ] && say "$WARNINGS warning(s) above."
say ''
say 'Next:'
if [ "$UPDATE" -eq 1 ]; then
  say "  1. Start a new $HARNESS session so it loads the updated skills."
  [ "$HARNESS" = openclaw ] && say '     In OpenClaw, send /new if the updated skills do not show up (the docs disagree on whether a running session sees them).'
  [ "$HARNESS" = hermes ] && say '     SOUL.md changes apply to new sessions; new skills are announced on your next message.'
  say '  2. If model profiles changed, run the ao-refresh skill to regenerate'
  say '     ~/.agent-orchestration/routing.md from your config.yaml.'
else
  say "  1. Start a new $HARNESS session (skills and instructions load at start)."
  [ "$HARNESS" = openclaw ] && say '     In OpenClaw, send /new if the skills do not show up (the docs disagree on whether a running session sees them).'
  [ "$HARNESS" = hermes ] && say '     SOUL.md changes apply to new sessions; new skills are announced on your next message.'
  say "  2. Run the ao-setup skill: $skill_cmd"
  say '     It interviews you and writes ~/.agent-orchestration/routing.md.'
  say '  3. From then on every session reads routing.md, glossary.md and lessons.md.'
fi
say "  Details and optional upgrades: $KIT_ROOT/adapters/$README_DIR/README.md"
