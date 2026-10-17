#!/usr/bin/env python3
"""Rewrite a run log to the canonical record in core/strategies/improvement-loop.md §8.

Reads a runs.jsonl file (default ~/.agent-orchestration/runs.jsonl), maps the
older row shapes onto the ten canonical keys, and canonicalises model ids
against the profile file names in <kit-root>/core/models/*.md. Values it
cannot map without guessing (an unknown model id, a row that is not a task id
in core/tasks.md, a time with no UTC offset) are left as written and listed
with their line numbers.

A compound row such as "babysit+review" keeps its first id in `row` and adds
"also_row: review" to notes, only when every part is a task id. An escalation
such as "claude-fable-5-1->claude-opus-5-5" keeps the left side in `model`
and adds "escalated_to: claude-opus-5-5" to notes, only when both sides
canonicalise to profile ids.

Usage:
  python3 normalize_runs.py [PATH] [--kit-root PATH] [--check | --write]

Default is a dry run: print what would change and write nothing. --check
validates every row against the canonical record. --write copies PATH to
PATH.bak-<timestamp> and then rewrites PATH in place.

Exit codes: 0 ok (for --check: every row valid), 1 (--check only) at least
one row fails, 2 error. Standard library only; Python 3.9+.
"""

import argparse
import collections
import datetime
import json
import math
import os
import re
import shutil
import sys
import tempfile

CANONICAL = ("ts", "repo", "row", "model", "effort", "mechanism",
             "duration_s", "outcome", "follow_ups", "notes")

# Older key -> canonical key. Applied only when the canonical key is not
# already present in the row; otherwise the older key folds into notes.
RENAMES = collections.OrderedDict([
    ("date", "ts"),
    ("project", "repo"),
    ("task", "row"),
    ("task_type", "row"),          # the old §8 name for the same task id
    ("followups", "follow_ups"),
    ("agent", "mechanism"),
])
MINUTES_KEY = "wall_clock_minutes"  # old §8 duration, converted to seconds

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Fractions of 3 or 6 digits only: Python 3.9's fromisoformat accepts nothing else.
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d{3}(\d{3})?)?)?(Z|[+-]\d{2}:\d{2})$")
NAIVE_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?$")


class NormError(Exception):
    pass


def default_log():
    return os.path.join(os.path.expanduser("~"), ".agent-orchestration", "runs.jsonl")


def load_profile_ids(kit_root):
    mdir = os.path.join(kit_root, "core", "models")
    if not os.path.isdir(mdir):
        raise NormError("kit root %s has no core/models directory" % kit_root)
    ids = sorted(f[:-3] for f in os.listdir(mdir) if f.endswith(".md") and not f.startswith("_"))
    if not ids:
        raise NormError("no model profiles in %s" % mdir)
    return ids


def read_text(path, newline=None):
    """Read a UTF-8 file; a decode error names the file that failed."""
    try:
        with open(path, "r", encoding="utf-8", newline=newline) as fh:
            return fh.read()
    except UnicodeDecodeError as exc:
        raise NormError("%s is not valid UTF-8 (%s)" % (path, exc))


def load_task_ids(kit_root):
    path = os.path.join(kit_root, "core", "tasks.md")
    if not os.path.isfile(path):
        raise NormError("missing %s" % path)
    ids = re.findall(r"^\|\s*`([a-z0-9-]+)`\s*\|", read_text(path), re.M)
    if not ids:
        raise NormError("no task ids found in %s" % path)
    return set(ids)


def norm_model(text):
    return re.sub(r"\s+", "-", text.strip().lower()).replace(".", "-")


def build_aliases(profile_ids):
    """Alias -> profile id. Each id answers to itself and, when the rest still
    contains a letter, to itself minus the family prefix (claude-opus-5-5 ->
    opus-5-5). Inputs are compared after norm_model, so opus-5.5 matches.
    An alias claimed by two profiles maps to neither."""
    claims = collections.defaultdict(set)
    for pid in profile_ids:
        claims[pid].add(pid)
        rest = pid.split("-", 1)[1] if "-" in pid else ""
        if re.search(r"[a-z]", rest):
            claims[rest].add(pid)
    return {alias: next(iter(ids)) for alias, ids in claims.items() if len(ids) == 1}


def canonical_model(value, profile_ids, aliases):
    if not isinstance(value, str):
        return None
    if value in profile_ids:
        return value
    return aliases.get(norm_model(value))


def fold_text(key, value):
    shown = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return "%s: %s" % (key, shown)


def ts_problem(value):
    shown = json.dumps(value, ensure_ascii=False)
    if not isinstance(value, str):
        return "ts %s is not a string" % shown
    if DATE_RE.match(value):
        try:
            datetime.date.fromisoformat(value)
            return None
        except ValueError:
            return "ts %s is not a real date" % shown
    if DATETIME_RE.match(value):
        try:
            datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            return None
        except ValueError:
            return "ts %s is not a real date-time" % shown
    if NAIVE_DATETIME_RE.match(value):
        return "ts %s has a time but no UTC offset" % shown
    return "ts %s is not an ISO 8601 date or date-time" % shown


def normalize_row(row, profile_ids, aliases, task_ids, stats):
    """Return (record, problems). Updates stats counters in place."""
    out = {}
    folded = []

    for key in CANONICAL:
        if key in row:
            out[key] = row[key]
    for key, value in row.items():
        if key in CANONICAL:
            continue
        target, new_value = RENAMES.get(key), value
        if key == MINUTES_KEY and isinstance(value, (int, float)) and not isinstance(value, bool):
            # A non-finite value (NaN, Infinity) moves unconverted, so --check lists it.
            target = "duration_s"
            if math.isfinite(value):
                new_value = int(round(value * 60))
        if target is not None and target not in out:
            out[target] = new_value
            stats["renamed"]["%s -> %s" % (key, target)] += 1
        else:
            why = "%s already set" % target if target else "not a canonical key"
            folded.append(fold_text(key, value))
            stats["folded"]["%s (%s)" % (key, why)] += 1

    if out.get("outcome") in (None, ""):
        out["outcome"] = "unknown"
        stats["filled"]["outcome -> unknown"] += 1
    fu = out.get("follow_ups")
    if isinstance(fu, list):
        items = [x if isinstance(x, str) else json.dumps(x, ensure_ascii=False) for x in fu]
        out["follow_ups"] = "; ".join(items) if items else "none"
        stats["filled"]["follow_ups list -> string"] += 1
    elif fu in (None, ""):
        out["follow_ups"] = "none"
        stats["filled"]["follow_ups -> none"] += 1

    for key in CANONICAL:
        if key not in out and key != "notes":
            out[key] = None
            stats["filled"]["%s -> null" % key] += 1

    # Compound row "a+b": split only when every part is a task id.
    row_value = out["row"]
    if isinstance(row_value, str) and "+" in row_value:
        parts = [p.strip() for p in row_value.split("+")]
        if all(p in task_ids for p in parts):
            out["row"] = parts[0]
            folded.extend("also_row: %s" % p for p in parts[1:])
            stats["split"]["row %s -> %s + also_row" % (row_value, parts[0])] += 1

    # Escalation "a->b": split only when both sides canonicalise.
    model = out["model"]
    canon = canonical_model(model, profile_ids, aliases)
    if canon is None and isinstance(model, str) and model.count("->") == 1:
        left, right = (canonical_model(s.strip(), profile_ids, aliases) for s in model.split("->"))
        if left is not None and right is not None:
            out["model"] = left
            folded.append("escalated_to: %s" % right)
            stats["split"]["model %s -> %s + escalated_to" % (model, left)] += 1
    elif canon is not None and canon != model:
        out["model"] = canon
        stats["models"]["%s -> %s" % (model, canon)] += 1

    notes = out.get("notes")
    if folded:
        if isinstance(notes, str):
            parts = [notes] if notes else []
        else:  # null, or a dict / list / number: keep it as text rather than lose it
            parts = [] if notes is None else [fold_text("notes", notes)]
        out["notes"] = "; ".join(parts + folded)
    elif "notes" not in out:
        out["notes"] = None
        stats["filled"]["notes -> null"] += 1
    elif notes == "":
        out["notes"] = None

    record = collections.OrderedDict((k, out[k]) for k in CANONICAL)
    # Whatever still fails validation is a value the script will not guess at.
    problems = [e + "; left as written" for e in check_row(record, profile_ids, task_ids)]
    return record, problems


def check_row(row, profile_ids, task_ids):
    """Return a list of reasons the row is not a canonical record."""
    if not isinstance(row, dict):
        return ["not a JSON object"]
    errs = []
    keys = tuple(row.keys())
    if keys != CANONICAL:
        missing = [k for k in CANONICAL if k not in row]
        extra = [k for k in keys if k not in CANONICAL]
        if missing:
            errs.append("missing keys: %s" % ", ".join(missing))
        if extra:
            errs.append("extra keys: %s" % ", ".join(extra))
        if not missing and not extra:
            errs.append("keys out of order (want %s)" % ", ".join(CANONICAL))

    def is_str(v, nonempty=True):
        return isinstance(v, str) and (bool(v.strip()) or not nonempty)

    if "ts" in row:
        p = ts_problem(row["ts"])
        if p:
            errs.append(p)
    if "repo" in row and not (row["repo"] is None or is_str(row["repo"])):
        errs.append("repo must be a non-empty string or null")
    if "row" in row and not (isinstance(row["row"], str) and row["row"] in task_ids):
        errs.append("row %s is not a task id in core/tasks.md" % json.dumps(row["row"], ensure_ascii=False))
    if "model" in row and not (isinstance(row["model"], str) and row["model"] in profile_ids):
        errs.append("model %s is not a profile id in core/models/" % json.dumps(row["model"], ensure_ascii=False))
    if "effort" in row and not (row["effort"] is None or is_str(row["effort"])):
        errs.append("effort must be a non-empty string or null")
    if "mechanism" in row and not is_str(row["mechanism"]):
        errs.append("mechanism must be a non-empty string")
    if "duration_s" in row:
        d = row["duration_s"]
        if not (d is None or (isinstance(d, int) and not isinstance(d, bool) and d >= 0)):
            errs.append("duration_s must be a non-negative integer or null")
    if "outcome" in row and not is_str(row["outcome"]):
        errs.append("outcome must be a non-empty string (unknown when not recorded)")
    if "follow_ups" in row and not is_str(row["follow_ups"]):
        errs.append("follow_ups must be a non-empty string (none when there are none)")
    if "notes" in row and not (row["notes"] is None or is_str(row["notes"])):
        errs.append("notes must be a non-empty string or null")
    return errs


def read_lines(path):
    if not os.path.isfile(path):
        raise NormError("no such file: %s" % path)
    # Split on "\n" only: splitlines() also breaks on U+2028, U+0085 and other
    # characters that may sit inside a JSON string.
    lines = read_text(path, newline="").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [l[:-1] if l.endswith("\r") else l for l in lines]


def run_check(path, profile_ids, task_ids):
    lines = read_lines(path)
    failures, rows = [], 0
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        rows += 1
        try:
            row = json.loads(line, object_pairs_hook=collections.OrderedDict)
        except ValueError as exc:
            failures.append((n, ["not valid JSON (%s)" % exc]))
            continue
        errs = check_row(row, profile_ids, task_ids)
        if errs:
            failures.append((n, errs))
    for n, errs in failures:
        print("line %d: %s" % (n, "; ".join(errs)))
    print("%s: %d rows, %d valid, %d invalid" % (path, rows, rows - len(failures), len(failures)))
    return 1 if failures else 0


def dump(record):
    return json.dumps(record, ensure_ascii=False, separators=(",", ":"))


def run_normalize(path, profile_ids, task_ids, write):
    aliases = build_aliases(profile_ids)
    lines = read_lines(path)
    stats = {"renamed": collections.Counter(), "folded": collections.Counter(),
             "filled": collections.Counter(), "models": collections.Counter(),
             "split": collections.Counter()}
    out_lines, unmapped = [], []
    rows = changed = blank = verbatim = unchanged_invalid = 0
    for n, line in enumerate(lines, 1):
        if not line.strip():
            blank += 1
            continue
        rows += 1
        try:
            row = json.loads(line, object_pairs_hook=collections.OrderedDict)
        except ValueError as exc:
            row, why = None, "not valid JSON (%s); kept verbatim" % exc
        else:
            why = None if isinstance(row, dict) else "not a JSON object; kept verbatim"
        if why:
            unmapped.append((n, [why]))
            out_lines.append(line)
            verbatim += 1
            continue
        record, problems = normalize_row(row, profile_ids, aliases, task_ids, stats)
        if problems:
            unmapped.append((n, problems))
        if list(record.items()) != list(row.items()):
            changed += 1
        elif problems:
            unchanged_invalid += 1
        out_lines.append(dump(record))

    print("%s: %d rows, %d %s, %d already canonical"
          % (path, rows, changed, "changed" if write else "would change",
             rows - changed - verbatim - unchanged_invalid))
    if unchanged_invalid:
        print("%d row(s) unchanged but still invalid (listed below)" % unchanged_invalid)
    if verbatim:
        print("%d line(s) not parseable as a JSON object, kept verbatim" % verbatim)
    if blank:
        print("%d blank line(s) %s" % (blank, "dropped" if write else "would be dropped"))
    sections = (("Renamed keys", "renamed"), ("Folded into notes", "folded"),
                ("Filled or converted values", "filled"), ("Model ids rewritten", "models"),
                ("Compound values split (extra part into notes)", "split"))
    for title, key in sections:
        if stats[key]:
            print("%s:" % title)
            for label, count in sorted(stats[key].items()):
                print("  %s: %d row%s" % (label, count, "" if count == 1 else "s"))
    if unmapped:
        print("Could not map without guessing (%d row%s):" % (len(unmapped), "" if len(unmapped) == 1 else "s"))
        for n, problems in unmapped:
            for p in problems:
                print("  line %d: %s" % (n, p))

    if not write:
        print("Dry run: nothing written. Re-run with --write to apply.")
        return 0
    if changed == 0 and blank == 0:
        print("Nothing to write.")
        return 0
    # Encode before touching the disk, so a failure (a lone surrogate escape,
    # say) leaves neither a backup nor a half-written file.
    try:
        data = "".join(l + "\n" for l in out_lines).encode("utf-8")
    except UnicodeEncodeError as exc:
        raise NormError("cannot write %s as UTF-8, so nothing was written and no backup made (%s)"
                        % (path, exc))
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    backup = "%s.bak-%s" % (path, stamp)
    shutil.copy2(path, backup)
    fd, tmp = tempfile.mkstemp(prefix=".normalize-", dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        shutil.copymode(path, tmp)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    print("Wrote %s (backup: %s)" % (path, backup))
    return 0


def main(argv=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Normalise a run log to the canonical record "
                                     "in core/strategies/improvement-loop.md section 8.")
    parser.add_argument("path", nargs="?", default=default_log(), help="run log (default: %(default)s)")
    parser.add_argument("--kit-root", default=os.path.dirname(script_dir),
                        help="kit checkout holding core/models and core/tasks.md (default: %(default)s)")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="exit 0 if every row is canonical, 1 if not; writes nothing")
    action.add_argument("--write", action="store_true", help="back up PATH, then rewrite it in place")
    args = parser.parse_args(argv)

    try:
        kit_root = os.path.realpath(os.path.expanduser(args.kit_root))
        profile_ids = load_profile_ids(kit_root)
        task_ids = load_task_ids(kit_root)
        path = os.path.expanduser(args.path)
        if args.check:
            return run_check(path, profile_ids, task_ids)
        return run_normalize(path, profile_ids, task_ids, args.write)
    except UnicodeError as exc:  # e.g. printing a value with a lone surrogate
        sys.stderr.write("normalize_runs.py: error: text is not representable as UTF-8 (%s)\n" % exc)
        return 2
    except (NormError, OSError) as exc:
        sys.stderr.write("normalize_runs.py: error: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
