#!/bin/sh
# Injects the user's generated routing table into context at session start.
# Output on stdout becomes context for the agent.

cfg="${AGENT_ORCHESTRATION_HOME:-$HOME/.agent-orchestration}"
root="${CLAUDE_PLUGIN_ROOT:-unknown}"

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
else
  echo "No routing table found at $cfg/routing.md."
  echo "Run /agent-orchestration:setup to interview the user and build one."
  echo "Until then, do not assume which models or subscriptions are available."
fi

echo "</agent-orchestration>"
