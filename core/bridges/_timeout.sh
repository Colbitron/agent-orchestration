#!/bin/sh
# with_timeout <seconds> <cmd...>
#
# Run <cmd...> with a wall-clock limit. macOS ships no `timeout`, so:
#   1. gtimeout (brew install coreutils) or timeout, if present: TERM at the
#      limit, KILL 10 s later.
#   2. Otherwise perl (always present): run the command in its own process
#      group, send SIGINT to the group at the limit (claude -p ends its turn
#      cleanly on SIGINT; SIGTERM leaves no result), then SIGKILL 10 s later.
#      Killing the group also stops child processes, which the bare
#      `perl -e 'alarm shift; exec @ARGV'` one-liner does not.
#
# Exit status: the command's own status, or 124 on timeout (137 from
# gtimeout means the command ignored TERM and was killed).
#
# Use:   . core/bridges/_timeout.sh; with_timeout 1200 codex exec ...
#   or:  sh core/bridges/_timeout.sh 1200 codex exec ...
#
# Note: in the perl path the command runs in a background process group, so
# it must not read from a terminal. Redirect stdin (< /dev/null) or pipe it.

with_timeout() {
  if [ "$#" -lt 2 ]; then
    echo "usage: with_timeout <seconds> <cmd...>" >&2
    return 2
  fi
  _wt_secs=$1
  shift
  if command -v gtimeout >/dev/null 2>&1; then
    gtimeout -k 10 "$_wt_secs" "$@"
    return $?
  fi
  if command -v timeout >/dev/null 2>&1; then
    timeout -k 10 "$_wt_secs" "$@"
    return $?
  fi
  perl -e '
    use POSIX ":sys_wait_h";
    my $secs = shift @ARGV;
    my $pid = fork;
    die "with_timeout: fork failed: $!\n" unless defined $pid;
    if ($pid == 0) {
      setpgrp(0, 0);
      exec @ARGV or do { print STDERR "with_timeout: exec $ARGV[0]: $!\n"; POSIX::_exit(127) };
    }
    $SIG{ALRM} = sub {
      kill "INT", -$pid;
      for (1 .. 10) { exit 124 if waitpid($pid, WNOHANG) > 0; sleep 1 }
      kill "KILL", -$pid;
      waitpid($pid, 0);
      exit 124;
    };
    alarm $secs;
    waitpid($pid, 0);
    alarm 0;
    exit(($? & 127) ? 128 + ($? & 127) : $? >> 8);
  ' "$_wt_secs" "$@"
}

# Executed directly (not sourced): run the arguments. zsh and bash set $0 or
# BASH_SOURCE to this file when sourcing, so detect that first.
_wt_sourced=0
case "${ZSH_EVAL_CONTEXT:-}" in *:file*) _wt_sourced=1 ;; esac
if [ -n "${BASH_SOURCE:-}" ] && [ "${BASH_SOURCE:-}" != "$0" ]; then _wt_sourced=1; fi
if [ "$_wt_sourced" = 0 ]; then
  case "$0" in
    *_timeout.sh) with_timeout "$@"; exit $? ;;
  esac
fi
unset _wt_sourced
