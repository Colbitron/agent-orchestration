#!/bin/sh
# Injects the user's generated routing table into context at session start.
# Output on stdout becomes context for the agent.

cfg="${AGENT_ORCHESTRATION_HOME:-$HOME/.agent-orchestration}"
root="${CLAUDE_PLUGIN_ROOT:-unknown}"

# Append an id (with optional detail) to a comma-separated list, keeping at
# most 6 entries; the caller tracks the total count for the "+N more" tail.
# Usage: list=$(list_add "$list" "$count" "item")   ($count is the count before adding)
list_add() {
  if [ "$2" -ge 6 ]; then
    printf '%s' "$1"
  elif [ -z "$1" ]; then
    printf '%s' "$3"
  else
    printf '%s, %s' "$1" "$3"
  fi
}

# Finish a list: add "+N more" when more than 6 ids were counted.
list_end() {
  if [ "$2" -gt 6 ]; then
    printf '%s, +%s more' "$1" "$(($2 - 6))"
  else
    printf '%s' "$1"
  fi
}

# Read one field from the stamp: stamp_get <key> -> rest of the line after the key.
stamp_get() {
  awk -v k="$1" '{ sub(/\r$/, "") } $1 == k { sub(/^[^ \t]+[ \t]+/, ""); print; exit }' "$stamp" 2>/dev/null
}

# Print the installed kit's commit, or nothing when it cannot be told.
# 1. The root is the top of a git checkout (a path install): its short HEAD.
#    A root inside some other repository (a git-managed ~/.claude) does not count.
# 2. Otherwise a marketplace cache copy, which Claude Code names after the
#    commit it installed (cache/<marketplace>/<plugin>/<12-hex sha>/): the
#    root's basename, when it is 7 to 40 lowercase hex characters.
# core/interview/generate.py (kit_info) applies the same two rules.
kit_commit() {
  if command -v git >/dev/null 2>&1 &&
    prefix=$(git -C "$root" rev-parse --show-prefix 2>/dev/null) && [ -z "$prefix" ]; then
    git -C "$root" rev-parse --short HEAD 2>/dev/null
    return 0
  fi
  base=${root%/}
  base=${base##*/}
  case "$base" in
    "" | *[!0-9a-f]*) return 0 ;;
  esac
  if [ "${#base}" -ge 7 ] && [ "${#base}" -le 40 ]; then
    printf '%s\n' "$base"
  fi
  return 0
}

# Compare the routing stamp against the kit's current profiles, tasks.md and commit.
routing_status() {
  stamp="$cfg/routing.stamp"
  echo
  echo "## Routing table status"
  if [ ! -f "$stamp" ]; then
    echo "The routing table is unstamped (generated before stamps existed); run /agent-orchestration:refresh to regenerate and stamp it."
    return 0
  fi

  generated=$(stamp_get generated)
  nprof=$(awk '{ sub(/\r$/, "") } $1 == "profile" && NF >= 3 { n++ } END { print n + 0 }' "$stamp" 2>/dev/null)
  if [ -z "$generated" ] || [ -z "$nprof" ] || [ "$nprof" -eq 0 ]; then
    echo "The routing stamp at $stamp could not be read; run /agent-orchestration:refresh to regenerate it."
    return 0
  fi

  models="$root/core/models"
  if [ "$root" = "unknown" ] || [ ! -d "$models" ]; then
    echo "Generated $generated; staleness not checked (kit files not found)."
    return 0
  fi

  changed="" nchanged=0 new="" nnew=0
  for f in "$models"/*.md; do
    [ -f "$f" ] || continue
    id=${f##*/}
    id=${id%.md}
    [ "$id" = "_schema" ] && continue
    asof=$(sed -n 's/^as_of:[[:space:]]*//p' "$f" 2>/dev/null | head -n 1 |
      sed 's/[[:space:]]*#.*$//; s/[[:space:]]*$//; s/^["'\'']//; s/["'\'']$//')
    [ -n "$asof" ] || asof="unknown"
    # Prints "=<as_of>" when the id has a profile line, nothing otherwise.
    stamped=$(awk -v id="$id" '{ sub(/\r$/, "") } $1 == "profile" && $2 == id { print "=" $3; exit }' "$stamp" 2>/dev/null)
    if [ -z "$stamped" ]; then
      new=$(list_add "$new" "$nnew" "$id")
      nnew=$((nnew + 1))
    elif [ "$stamped" != "=$asof" ]; then
      changed=$(list_add "$changed" "$nchanged" "$id ($asof)")
      nchanged=$((nchanged + 1))
    fi
  done

  tasks_changed=0
  stamp_tasks=$(stamp_get tasks)
  if [ -n "$stamp_tasks" ] && [ -f "$root/core/tasks.md" ]; then
    if command -v shasum >/dev/null 2>&1; then
      cur_tasks=$(shasum -a 256 "$root/core/tasks.md" 2>/dev/null | cut -c1-12)
    elif command -v sha256sum >/dev/null 2>&1; then
      cur_tasks=$(sha256sum "$root/core/tasks.md" 2>/dev/null | cut -c1-12)
    else
      cur_tasks=""
    fi
    if [ -n "$cur_tasks" ] && [ "$cur_tasks" != "$stamp_tasks" ]; then
      tasks_changed=1
    fi
  fi

  # The kit has no version number; a push to main is a release. Compare the
  # commit the table was generated from with the installed one. Short SHAs can
  # differ in length, so one being a prefix of the other counts as a match.
  # Older stamps may carry kit_version and no kit_commit; that is not a change.
  stamp_commit=$(stamp_get kit_commit)
  [ "$stamp_commit" = "unknown" ] && stamp_commit=""
  cur_commit=$(kit_commit)
  commit_changed=0 commit_note=""
  if [ -z "$cur_commit" ]; then
    commit_note="not checked: the install is neither a git checkout nor a commit-named cache copy"
  elif [ -z "$stamp_commit" ]; then
    commit_note="not checked: the stamp records no commit"
  else
    case "$cur_commit" in
      "$stamp_commit"*) ;;
      *) case "$stamp_commit" in "$cur_commit"*) ;; *) commit_changed=1 ;; esac ;;
    esac
  fi

  if [ "$nchanged" -eq 0 ] && [ "$nnew" -eq 0 ] && [ "$tasks_changed" -eq 0 ] && [ "$commit_changed" -eq 0 ]; then
    if [ -n "$commit_note" ]; then
      echo "Up to date (generated $generated; kit commit $commit_note)."
    else
      echo "Up to date (generated $generated)."
    fi
    return 0
  fi
  if [ "$nchanged" -gt 0 ]; then
    echo "$nchanged profile(s) changed since the table was generated: $(list_end "$changed" "$nchanged")"
  fi
  if [ "$nnew" -gt 0 ]; then
    echo "$nnew new profile(s) not in the table: $(list_end "$new" "$nnew")"
  fi
  [ "$tasks_changed" -eq 1 ] && echo "tasks.md changed since the table was generated."
  [ "$commit_changed" -eq 1 ] && echo "kit commit $stamp_commit -> $cur_commit"
  [ -n "$commit_note" ] && echo "Kit commit $commit_note."
  echo "Run /agent-orchestration:refresh to regenerate."
  return 0
}

echo "<agent-orchestration kit root=\"$root\" config=\"$cfg\">"

if [ -f "$cfg/routing.md" ]; then
  cat "$cfg/routing.md"
  if [ -f "$cfg/glossary.md" ]; then
    echo
    cat "$cfg/glossary.md"
  fi
  if [ -f "$cfg/lessons.md" ]; then
    echo
    echo "## Lessons learned (appended by the improvement loop)"
    cat "$cfg/lessons.md"
  fi
  echo
  echo "Strategy docs live under $root/core/strategies/. Read delegation-prompting.md before delegating anything."
  routing_status
else
  echo "No routing table found at $cfg/routing.md."
  echo "Run /agent-orchestration:setup to interview the user and build one."
  echo "Until then, do not assume which models or subscriptions are available."
fi

echo "</agent-orchestration>"
