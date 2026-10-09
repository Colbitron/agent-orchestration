#!/usr/bin/env python3
"""Reference implementation of core/interview/routing-generator.md.

Reads ~/.agent-orchestration/config.yaml (core/interview/config-schema.md),
every core/models/*.md profile and core/tasks.md, and produces routing.md,
glossary.md and routing.stamp. The markdown spec stays authoritative; this
script follows it step by step so the same inputs always give the same bytes.

Usage:
  python3 generate.py [--kit-root PATH] [--config PATH] [--out DIR]
                      [--check | --diff | --write] [--json]

Exit codes: 0 ok (for --check: up to date), 1 (--check only) stale or
differs, 2 error. Standard library only; Python 3.9+. YAML is parsed with
pyyaml when importable, otherwise through ruby.
"""

import argparse
import datetime
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

GENERATOR = "generate.py"
GENERATOR_VERSION = "1"
MAX_LINES = 150
WRAP = 78

FIT_RANK = {"best": 0, "good": 1, "ok": 2, "poor": 3, "unknown": 4}
EFFORT_WORDS = ("none", "minimal", "low", "medium", "high", "xhigh", "max")

# Task kinds from the weighting table in routing-generator.md, step 1.
KIND_BY_TASK = {
    "feature": "wide", "long-run": "wide", "orchestrate": "wide", "babysit": "wide",
    "quick-fix": "narrow", "copy": "narrow", "frontend": "narrow",
    "review": "info", "investigate": "info", "analyze": "info", "research": "info",
    "bulk": "mechanical",
    "computer-use": "computer-use",
    "3d-games": "3d",
    "prompt-writing": "prompt",
}

# Rows an expensive (user cost <= 4) model may win besides wide / very wide.
EXPENSIVE_EXTRA_ROWS = ("frontend",)
EXPENSIVE_MAX_COST = 4
BULK_MIN_COST = 8
COMPUTER_USE_MIN = 6

AUTONOMY_LABELS = [
    ("create_worktrees", "create worktrees"),
    ("open_prs", "open PRs"),
    ("merge_prs", "merge PRs"),
    ("close_prs", "close PRs"),
    ("rebase", "rebase"),
    ("force_push", "force-push"),
    ("deploy", "deploy"),
]

PREFERENCE_LABELS = [
    ("stack", "Stack"),
    ("style", "Style"),
    ("machines", "Machines"),
    ("review_bots_note", "Review bots"),
]

# Words that keep their capital when a profile note follows a semicolon.
PROPER_WORDS = {
    "Anthropic", "OpenAI", "Google", "Claude", "Codex", "Cursor", "GitHub",
    "Theo", "AA", "PR", "PRs", "CI", "UI", "API", "OS", "I", "TS", "ZDR",
    "Fish", "Blender", "Tailwind", "Terminal-Bench", "OSWorld", "Mia",
}

HARNESS_NAMES = {
    "claude-code": "Claude Code", "codex": "Codex", "cursor": "Cursor",
    "gemini-cli": "Gemini CLI", "opencode": "OpenCode", "pi": "Pi",
    "grokbuild": "Grok Build", "t3-code": "T3 Code", "antigravity": "Antigravity",
}

# Times become ISO 8601 UTC strings and dates ISO dates, matching _normalise.
RUBY_YAML = (
    "def n(o); case o; when Hash then o.each_with_object({}) { |(k, v), h| h[n(k)] = n(v) }; "
    "when Array then o.map { |x| n(x) }; "
    "when Time then o.getutc.strftime('%Y-%m-%dT%H:%M:%SZ'); "
    "when DateTime then o.new_offset(0).strftime('%Y-%m-%dT%H:%M:%SZ'); "
    "when Date then o.strftime('%Y-%m-%d'); else o; end; end; "
    "puts JSON.generate(n(YAML.safe_load(STDIN.read, "
    "permitted_classes: [Date, Time, Symbol], aliases: true)))")


class GenError(Exception):
    """A problem that stops generation (exit 2)."""


# --------------------------------------------------------------------------
# YAML loading


def _normalise(value):
    """Turn YAML-native dates into ISO strings and keys into strings."""
    if isinstance(value, datetime.datetime):
        return _utc(value)
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {_key(k): _normalise(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalise(v) for v in value]
    return value


def _key(k):
    if k is None:
        return "null"
    if isinstance(k, bool):
        return str(k).lower()
    if isinstance(k, datetime.datetime):
        return _utc(k)
    if isinstance(k, datetime.date):
        return k.isoformat()
    return str(k)


def _utc(value):
    """ISO 8601 UTC; YAML timestamps without a zone are UTC by the spec."""
    if value.tzinfo is not None:
        value = value.astimezone(datetime.timezone.utc)
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def make_yaml_loader():
    try:
        import yaml  # type: ignore

        def load(text):
            try:
                return _normalise(yaml.safe_load(text))
            except Exception as exc:  # yaml.YAMLError and anything the loader raises
                lines = str(exc).strip().splitlines()
                raise GenError("YAML parse failed: " + (" ".join(l.strip() for l in lines[:3]) or type(exc).__name__))
        return load
    except ImportError:
        pass
    ruby = shutil.which("ruby")
    if ruby:
        def load(text):
            proc = subprocess.run(
                [ruby, "-rdate", "-ryaml", "-rjson", "-e", RUBY_YAML],
                input=text.encode("utf-8"), stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            if proc.returncode != 0:
                err = proc.stderr.decode("utf-8", "replace").strip().splitlines()
                raise GenError("YAML parse failed: " + (err[0] if err else "ruby exited %d" % proc.returncode))
            out = proc.stdout.decode("utf-8", "replace").strip()
            try:
                return _normalise(json.loads(out)) if out else None
            except ValueError as exc:
                raise GenError("YAML parse failed: ruby returned unreadable JSON (%s)" % exc)
        return load
    raise GenError("install pyyaml (pip install pyyaml) or ruby")


# --------------------------------------------------------------------------
# Small helpers


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]) + "\n"
    return None


def as_dict(value):
    return value if isinstance(value, dict) else {}


def as_list(value):
    return value if isinstance(value, list) else []


def iso(value):
    if value is None:
        return "unknown"
    return str(value).strip() or "unknown"


def wrap_bullet(text, prefix="- "):
    return textwrap.fill(text, width=WRAP, initial_indent=prefix,
                         subsequent_indent=" " * len(prefix),
                         break_long_words=False, break_on_hyphens=False)


def wrap_para(text):
    return textwrap.fill(text, width=WRAP, break_long_words=False,
                         break_on_hyphens=False)


def join_words(items, conj="and"):
    items = list(items)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return "%s %s %s" % (items[0], conj, items[1])
    return "%s, %s %s" % (", ".join(items[:-1]), conj, items[-1])


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def strip_citations(note):
    note = re.sub(r"\s*\([^()]*(?:§|research/|transcripts/|\d+:\d\d)[^()]*\)", "", note)
    note = re.sub(r"\s+", " ", note).strip()
    return note


def first_sentence(note):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9'\"(])", note, maxsplit=1)
    return parts[0].strip()


def lower_first(text, model_words=()):
    m = re.match(r"([A-Za-z][A-Za-z'-]*)(\s+(\S+))?", text)
    if not m:
        return text
    word = m.group(1)
    nxt = m.group(3) or ""
    if word in PROPER_WORDS or not word[1:].islower() and len(word) > 1:
        return text
    if (nxt[:1].isupper() or nxt[:1].isdigit()) and nxt.strip(".,;:'") not in model_words:
        return text  # "Fish Slop", "Fable 5.1": treat as a proper noun
    return word[0].lower() + text[1:]


def sentence(parts):
    text = "; ".join(p.rstrip(" .;") for p in parts if p and p.strip(" .;"))
    return text + "." if text else ""


# --------------------------------------------------------------------------
# Kit inputs


class Model(object):
    def __init__(self, file_id, path, data):
        self.file_id = file_id
        self.path = path
        self.data = data
        self.id = str(data.get("id") or file_id)
        self.name = str(data.get("name") or file_id)
        self.family = str(data.get("family") or "unknown")
        self.vendor = str(data.get("vendor") or "unknown")
        self.status = str(data.get("status") or "unknown")
        self.as_of = iso(data.get("as_of"))
        self.scores = as_dict(data.get("scores"))
        self.tasks = as_dict(data.get("tasks"))
        self.effort = as_dict(data.get("effort"))
        self.access = as_dict(data.get("access"))
        self.role_hints = as_dict(data.get("role_hints"))
        # filled from config
        self.state = "unconfigured"
        self.cost = None

    @property
    def short(self):
        return self.name[7:] if self.name.startswith("Claude ") else self.name

    @property
    def alias(self):
        parts = self.id.split("-")
        return parts[1] if self.family == "claude" and len(parts) > 1 else None

    def score(self, axis):
        v = self.scores.get(axis)
        return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0

    def check(self, used_axes):
        """Coerce numeric-string scores and report gaps: (warnings, errors)."""
        warns, errs = [], []
        where = "core/models/%s.md" % self.file_id
        if not isinstance(self.data.get("scores"), dict):
            warns.append("%s has no scores block; every axis counts as 0" % where)
        for axis in used_axes:
            if axis not in self.scores or self.scores.get(axis) is None:
                if isinstance(self.data.get("scores"), dict):
                    warns.append("%s has no scores.%s; it counts as 0" % (where, axis))
                continue
            v = self.scores[axis]
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                try:
                    num = float(str(v).strip())
                    self.scores[axis] = int(num) if num == int(num) else num
                    warns.append("%s scores.%s is %r, not a number; read as %s" % (where, axis, v, self.scores[axis]))
                except ValueError:
                    errs.append("%s scores.%s is %r, not a number" % (where, axis, v))
        if not isinstance(self.data.get("tasks"), dict):
            warns.append("%s has no tasks block; every task fit counts as unknown" % where)
        if self.effort.get("default") in (None, "") and as_list(self.effort.get("levels")):
            warns.append("%s has no effort.default; its rows show no effort" % where)
        return warns, errs

    def fit(self, task):
        entry = as_dict(self.tasks.get(task))
        f = str(entry.get("fit") or "unknown")
        return f if f in FIT_RANK else "unknown"

    def note(self, task):
        return str(as_dict(self.tasks.get(task)).get("note") or "").strip()

    @property
    def subagent_only(self):
        hint = str(self.role_hints.get("as_primary") or "").strip().lower()
        never = [str(x).lower() for x in as_list(self.role_hints.get("never_for"))]
        return (hint.startswith("never") or hint.startswith("not recommended")
                or any(x.startswith("primary or interactive") for x in never))


def load_tasks(kit_root):
    path = os.path.join(kit_root, "core", "tasks.md")
    if not os.path.isfile(path):
        raise GenError("missing %s" % path)
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")
    tasks = []
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(r"^\|\s*id\s*\|", l)), None)
    if start is None:
        raise GenError("no task table (header row starting \"| id |\") in %s" % path)
    header = [c.strip().lower() for c in lines[start].strip().strip("|").split("|")]
    try:
        width_col = next(i for i, h in enumerate(header) if h.startswith("width"))
        must_col = next(i for i, h in enumerate(header) if h.startswith("must land"))
    except StopIteration:
        raise GenError("task table in %s lacks a Width or Must land? column" % path)
    seen = set()
    for line in lines[start + 1:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or set(cells[0]) <= set("-: "):
            continue
        tid = cells[0].strip("` ")
        if not re.match(r"^[a-z0-9-]+$", tid) or len(cells) <= max(width_col, must_col):
            raise GenError("unreadable task row in %s: %s" % (path, line.strip()))
        if tid in seen:
            raise GenError("duplicate task id %s in %s" % (tid, path))
        seen.add(tid)
        tasks.append({"id": tid, "width": cells[width_col].lower(), "must_land": cells[must_col].lower()})
    if not tasks:
        raise GenError("no task rows found in %s" % path)
    glossary = []
    in_gloss = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_gloss = line.strip().lower() == "## glossary defaults"
            continue
        if not in_gloss:
            continue
        m = re.match(r"^- \*\*(.+?)\*\*:\s*(.*)$", line)
        if m:
            glossary.append([m.group(1).strip(), m.group(2).strip()])
        elif glossary and line.startswith("  ") and line.strip():
            glossary[-1][1] += " " + line.strip()
    digest = hashlib.sha256(raw).hexdigest()[:12]
    return tasks, glossary, digest


def task_kind(task):
    if task["id"] in KIND_BY_TASK:
        return KIND_BY_TASK[task["id"]]
    must = task["must_land"]
    if must.startswith("yes"):
        return "wide" if is_wide(task) else "narrow"
    if must.startswith("n/a"):
        return "info"
    return "mechanical"


def is_wide(task):
    w = task["width"]
    return w in ("wide", "very wide")


def load_models(kit_root, load_yaml, errors, warnings):
    mdir = os.path.join(kit_root, "core", "models")
    if not os.path.isdir(mdir):
        raise GenError("missing %s" % mdir)
    models = {}
    for fname in sorted(os.listdir(mdir)):
        if not fname.endswith(".md") or fname == "_schema.md":
            continue
        file_id = fname[:-3]
        path = os.path.join(mdir, fname)
        fm = frontmatter(read_text(path))
        data = None
        if fm is None:
            warnings.append("profile %s has no frontmatter" % fname)
        else:
            try:
                data = load_yaml(fm)
            except GenError as exc:
                warnings.append("profile %s: %s" % (fname, exc))
        model = Model(file_id, path, as_dict(data))
        if data is not None and model.id != file_id:
            warnings.append("profile %s declares id %s; using the file name" % (fname, model.id))
            model.id = file_id
        models[file_id] = model
    return models


def load_bridges(kit_root, load_yaml):
    bdir = os.path.join(kit_root, "core", "bridges")
    bridges = {}
    if not os.path.isdir(bdir):
        return bridges
    for fname in sorted(os.listdir(bdir)):
        if not fname.endswith(".md") or fname == "README.md":
            continue
        fm = frontmatter(read_text(os.path.join(bdir, fname)))
        if fm is None:
            continue
        try:
            data = as_dict(load_yaml(fm))
        except GenError:
            continue
        bridges[str(data.get("id") or fname[:-3])] = data
    return bridges


def load_agents(kit_root):
    """Claude Code agents shipped with the kit: name -> model alias."""
    adir = os.path.join(kit_root, "agents")
    agents = {}
    if not os.path.isdir(adir):
        return agents
    for fname in sorted(os.listdir(adir)):
        if not fname.endswith(".md"):
            continue
        fm = frontmatter(read_text(os.path.join(adir, fname))) or ""
        name = re.search(r"^name:\s*(\S+)", fm, re.M)
        model = re.search(r"^model:\s*(\S+)", fm, re.M)
        if name and model:
            agents[name.group(1)] = model.group(1)
    return agents


def kit_info(kit_root):
    version = "unknown"
    try:
        with open(os.path.join(kit_root, ".claude-plugin", "plugin.json"), "r", encoding="utf-8") as fh:
            version = str(json.load(fh).get("version") or "unknown")
    except (OSError, ValueError):
        pass
    commit = "unknown"
    try:
        proc = subprocess.run(["git", "-C", kit_root, "rev-parse", "--short", "HEAD"],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if proc.returncode == 0 and proc.stdout.strip():
            commit = proc.stdout.decode("utf-8").strip()
    except OSError:
        pass
    return version, commit


# --------------------------------------------------------------------------
# Scoring (step 1)


class Ctx(object):
    def __init__(self, config, models, tasks):
        self.config = config
        self.models = models
        self.tasks = tasks
        pri = as_dict(config.get("priorities"))
        order = [str(a) for a in as_list(pri.get("order"))]
        self.order = order or ["intelligence", "taste", "cost"]
        self.frustration_low = str(pri.get("frustration_tolerance") or "").lower() == "low"
        self.budget_high = str(pri.get("budget_sensitivity") or "").lower() == "high"
        self.speed_matters = pri.get("speed_matters") is True
        self.effort_overrides = as_dict(config.get("effort"))
        harnesses, seen = [], set()
        for h in as_list(config.get("harnesses")):
            h = as_dict(h)
            if str(h.get("id")) not in seen:
                seen.add(str(h.get("id")))
                harnesses.append(h)
        primary = [h for h in harnesses if h.get("primary") is True]
        self.harnesses = harnesses
        self.primary_harness = str((primary or harnesses or [{}])[0].get("id") or "unknown")
        self.enabled = [m for m in models.values() if m.state == "enabled"]

    def axis(self, model, name):
        if name == "cost":
            return model.cost or 0
        return model.score(name)

    def weights(self, task):
        """Weighted axes for a task, after the priorities adjustments.

        frustration_tolerance: low adds 1 to the weight of floor, and
        budget_sensitivity: high adds 1 to the weight of cost, on every row
        (an axis the row does not weight starts from 0).
        """
        w = self._base_weights(task)
        for flag, axis in ((self.frustration_low, "floor"), (self.budget_high, "cost")):
            if not flag:
                continue
            if any(a == axis for a, _ in w):
                w = [(a, n + 1 if a == axis else n) for a, n in w]
            else:
                w = w + [(axis, 1)]
        return w

    def _base_weights(self, task):
        kind = task_kind(task)
        if kind == "wide":
            return [("floor", 2), ("intelligence", 1), ("taste", 1)]
        if kind == "narrow":
            w = [("taste", 2), ("floor", 1)]
            return w + [("speed", 1)] if self.speed_matters else w
        if kind == "info":
            return [("thoroughness", 2), ("intelligence", 1), ("cost", 1)]
        if kind == "mechanical":
            return [("cost", 2), ("floor", 1), ("speed", 1)]
        if kind == "computer-use":
            return [("computer_use", 3)]
        if kind == "3d":
            return [("intelligence", 1), ("taste", 1)]
        return [("intelligence", 1), ("thoroughness", 1)]

    def score(self, model, task):
        return sum(w * self.axis(model, a) for a, w in self.weights(task))

    def expensive(self, model):
        return model.cost is not None and model.cost <= EXPENSIVE_MAX_COST

    def restricted(self, task):
        return not (is_wide(task) or task["id"] in EXPENSIVE_EXTRA_ROWS)

    def tiebreak_key(self, model, task):
        return tuple(-self.axis(model, a) for a in self.order) + (-self.score(model, task), model.id)

    def rank(self, cands, task, penalise=False):
        """Order candidates: fit tier, then score with the priorities tiebreak.

        Scores within one point of the best remaining score are a tie, broken
        by priorities.order. With penalise, expensive models sort after the
        other models of the same fit tier (they may still be the fallback).
        """
        out = []
        tiers = sorted(set(FIT_RANK[m.fit(task["id"])] for m in cands))
        for tier in tiers:
            group = [m for m in cands if FIT_RANK[m.fit(task["id"])] == tier]
            subgroups = [group]
            if penalise:
                subgroups = [[m for m in group if not self.expensive(m)],
                             [m for m in group if self.expensive(m)]]
            for sub in subgroups:
                remaining = sorted(sub, key=lambda m: m.id)
                while remaining:
                    top = max(self.score(m, task) for m in remaining)
                    close = [m for m in remaining if self.score(m, task) >= top - 1]
                    pick = min(close, key=lambda m: self.tiebreak_key(m, task))
                    out.append(pick)
                    remaining.remove(pick)
        return out

    def candidates(self, task, pool=None):
        pool = self.enabled if pool is None else pool
        ok = [m for m in pool if FIT_RANK[m.fit(task["id"])] <= FIT_RANK["ok"]]
        return ok if ok else list(pool)


# --------------------------------------------------------------------------
# Picking (step 2)


class Row(object):
    def __init__(self, task):
        self.task = task
        self.primary = None
        self.fallback = None
        self.effort = None
        self.decider = ""
        self.note = ""
        self.extra = []
        self.primary_label = None
        self.empty_text = None


def check_effort(value, model, where, errors):
    """Config efforts must be one of the model's effort.levels, and never max."""
    if not isinstance(value, str) or not value.strip():
        errors.append("%s is %r; it must be one effort level as a string" % (where, value))
        return
    level = value.strip()
    if level.lower() == "max":
        errors.append("%s is max; the kit never uses max effort" % where)
        return
    if model is None:
        return
    levels = [str(l) for l in as_list(model.effort.get("levels"))]
    if not levels:
        errors.append("%s is %s but %s has no effort control (effort.levels is empty)" % (where, level, model.id))
    elif level not in levels:
        errors.append("%s is %s, not one of %s's levels: %s" % (where, level, model.id, ", ".join(levels)))


def effort_for(ctx, model):
    if model is None:
        return None
    if model.id in ctx.effort_overrides and ctx.effort_overrides[model.id] not in (None, ""):
        value = str(ctx.effort_overrides[model.id]).strip()
    else:
        value = model.effort.get("default")
        value = str(value).strip() if value not in (None, "") else None
    return value


def pick_fallback(ranked, primary, task, exclude=()):
    """Next model in the ranking, preferring another family within the next fit tier.

    A different family never beats a better fit tier: a best-fit same-family
    model stays ahead of an ok-fit model from another vendor.
    """
    rest = [m for m in ranked if m is not primary and m.id not in exclude]
    if not rest:
        return None
    tier = FIT_RANK[rest[0].fit(task["id"])]
    other = [m for m in rest if FIT_RANK[m.fit(task["id"])] == tier and m.family != primary.family]
    return other[0] if other else rest[0]


def explain(ctx, task, primary, runner):
    tid = task["id"]
    if runner is None:
        return "Only candidate"
    pf, rf = primary.fit(tid), runner.fit(tid)
    if FIT_RANK[pf] < FIT_RANK[rf]:
        return "Rated %s fit, ahead of %s (%s)" % (pf, runner.short, rf)
    ps, rs = ctx.score(primary, task), ctx.score(runner, task)
    if abs(ps - rs) <= 1:
        for axis in ctx.order:
            a, b = ctx.axis(primary, axis), ctx.axis(runner, axis)
            if a != b:
                return "Within a point of %s; %s %s vs %s breaks the tie" % (runner.short, axis, a, b)
        return "Tied with %s on score and priorities" % runner.short
    best = None
    for axis, w in ctx.weights(task):
        diff = w * (ctx.axis(primary, axis) - ctx.axis(runner, axis))
        rank = ctx.order.index(axis) if axis in ctx.order else len(ctx.order)
        key = (diff, -rank)
        if best is None or key > best[0]:
            best = (key, axis)
    axis = best[1]
    label = "computer use" if axis == "computer_use" else axis
    return "%s %s vs %s over %s" % (label.capitalize(), ctx.axis(primary, axis),
                                    ctx.axis(runner, axis), runner.short)


MODEL_WORDS = set()


def model_note(model, task_id, guardrail=False):
    note = first_sentence(strip_citations(model.note(task_id)))
    if not note:
        return ""
    note = lower_first(note, MODEL_WORDS)
    return ("guardrail: " + note) if guardrail else note


def build_rows(ctx, errors, warnings):
    rows = {}
    order = [t["id"] for t in ctx.tasks]
    by_id = {t["id"]: t for t in ctx.tasks}
    overrides = as_dict(ctx.config.get("routing_overrides"))

    def plain_pick(task, pool=None):
        cands = ctx.candidates(task, pool)
        restricted = ctx.restricted(task)
        natural = ctx.rank(cands, task)
        ranked = ctx.rank(cands, task, penalise=restricted)
        return cands, natural, ranked, restricted

    def build_row(tid):
        task = by_id[tid]
        row = Row(task)
        rows[tid] = row
        if not ctx.enabled:
            row.empty_text = "No model enabled"
            return

        if tid == "computer-use" and not any(m.score("computer_use") >= COMPUTER_USE_MIN for m in ctx.enabled):
            row.empty_text = ("No capable computer-use model enabled; verify by running "
                              "tests and reading logs instead")
            return

        feature_primary = rows["feature"].primary if "feature" in rows else None
        cands, natural, ranked, restricted = plain_pick(task)
        primary = ranked[0]
        fallback = None
        decider = None
        displaced = None

        if restricted and natural and ctx.expensive(natural[0]):
            cheaper = [m for m in ranked if not ctx.expensive(m)]
            if cheaper:
                displaced = natural[0]
                primary = cheaper[0]

        if tid == "review" and feature_primary is not None:
            fam = feature_primary.family
            families = set(m.family for m in ctx.enabled)
            if len(families) > 1:
                pool = [m for m in ctx.enabled if m.family != fam]
                p_ranked = plain_pick(task, pool)[2]
                primary = p_ranked[0]
                if restricted and ctx.expensive(primary):
                    cheaper = [m for m in p_ranked if not ctx.expensive(m)]
                    if cheaper:
                        displaced = primary
                        primary = cheaper[0]
                    else:
                        displaced = None
                else:
                    displaced = None
                decider = "Cross-family review: %s wrote the feature code, so a %s model reviews" % (
                    feature_primary.short, primary.family)
                fallback = displaced or pick_fallback(ranked, primary, task, exclude=(feature_primary.id,))
            else:
                pool = [m for m in cands if m is not feature_primary]
                displaced = None
                if pool:
                    primary = sorted(pool, key=lambda m: (restricted and ctx.expensive(m),
                                                          -m.score("thoroughness"), ranked.index(m)))[0]
                    decider = ("Single-family setup: a second vendor's reviewer would catch more. "
                               "Highest thoroughness (%s) apart from the feature primary, %s"
                               % (primary.score("thoroughness"), feature_primary.short))
                    fallback = pick_fallback(ranked, primary, task, exclude=(feature_primary.id,))
                else:
                    primary = feature_primary
                    decider = ("Only one model enabled; the implementer reviews its own work. "
                               "Add a second model for a real gate")
                    fallback = pick_fallback(ranked, primary, task)

        if tid == "bulk" or task_kind(task) == "mechanical":
            cheap = [m for m in ctx.enabled
                     if (m.cost or 0) >= BULK_MIN_COST and FIT_RANK[m.fit(tid)] <= FIT_RANK["ok"]]
            if cheap:
                cheap.sort(key=lambda m: (-(m.cost or 0), ranked.index(m) if m in ranked else 99, m.id))
                winner = cheap[0]
                if winner is not primary:
                    primary = winner
                    displaced = None
                decider = "Cheapest capable quota (cost %s, fit %s) wins bulk" % (winner.cost, winner.fit(tid))

        if displaced is not None and displaced is not primary:
            fallback = displaced
            decider = (decider + "; " if decider else "") + (
                "%s (cost %s) is reserved for wide rows" % (displaced.short, displaced.cost))
        if fallback is None:
            fallback = pick_fallback(ranked, primary, task)

        if decider is None:
            runner = next((m for m in ranked if m is not primary), None)
            decider = explain(ctx, task, primary, runner)

        row.primary = primary
        row.fallback = fallback
        row.decider = decider
        row.note = "" if decider.startswith("Only one model enabled") else \
            model_note(primary, tid, guardrail=primary.fit(tid) == "ok")
        if FIT_RANK[primary.fit(tid)] > FIT_RANK["ok"]:
            row.extra.append("no model rates better than %s here" % primary.fit(tid))

        if tid == "orchestrate":
            in_harness = [m for m in ctx.enabled
                          if ctx.primary_harness in [str(h) for h in as_list(m.access.get("harnesses"))]]
            if len(in_harness) >= 2:
                row.primary_label = "The session model (%s preferred)" % primary.short
                row.decider = "%s can switch models, so lead from %s; %s" % (
                    harness_name(ctx.primary_harness), primary.short, lower_first(row.decider, MODEL_WORDS))
            else:
                # Whether the harness can switch is not known here; just name the model.
                row.primary_label = "The session model (%s)" % primary.short

    def apply_override(tid):
        ov = as_dict(overrides[tid])
        row = rows[tid]
        for key in ("primary", "fallback"):
            if key not in ov:
                continue
            mid = ov.get(key)
            if mid in (None, "", "none"):
                setattr(row, key, None)
                continue
            model = ctx.models.get(str(mid))
            if model is None:
                errors.append("routing_overrides.%s.%s: no profile for %s" % (tid, key, mid))
            elif model.state != "enabled":
                errors.append("routing_overrides.%s.%s: %s is not enabled in config.models" % (tid, key, mid))
            else:
                setattr(row, key, model)
        row.empty_text = None if row.primary is not None else (row.empty_text or "Override leaves no primary")
        row.primary_label = None
        reason = str(ov.get("reason") or "").strip()
        row.decider = "Config override" + (": " + reason if reason else "")
        row.note = ""
        row.extra = []
        if "effort" in ov and ov.get("effort") is not None:
            row.effort = ov.get("effort")
            check_effort(row.effort, row.primary, "routing_overrides.%s.effort" % tid, errors)
            row.effort = str(row.effort).strip()

    for tid in sorted(overrides):
        if tid not in by_id:
            errors.append("routing_overrides.%s: no such task id in core/tasks.md" % tid)

    # Feature first (with its override): review depends on its family.
    sequence = (["feature"] if "feature" in by_id else []) + [t for t in order if t != "feature"]
    for tid in sequence:
        build_row(tid)
        if tid in overrides:
            apply_override(tid)

    for tid in order:
        row = rows[tid]
        if row.effort is None and row.primary is not None:
            row.effort = effort_for(ctx, row.primary)

    review, feature = rows.get("review"), rows.get("feature")
    if review and feature and review.primary is not None and feature.primary is not None:
        if review.primary is feature.primary and len(ctx.enabled) > 1:
            warnings.append("review and feature both route to %s: the implementer reviews its own work"
                            % review.primary.id)
        elif (review.primary.family == feature.primary.family
              and len(set(m.family for m in ctx.enabled)) > 1):
            warnings.append("review (%s) and feature (%s) are both %s models although another family is enabled"
                            % (review.primary.id, feature.primary.id, review.primary.family))
    return [rows[t] for t in order]


# --------------------------------------------------------------------------
# Rendering (steps 3 and 4)


UNREACHABLE = "unreachable: no configured harness or bridge reaches it"


def harness_name(hid):
    return HARNESS_NAMES.get(hid, hid)


def reach_via(ctx, model, bridges, agents):
    parts = []
    harness_ids = [str(h.get("id")) for h in ctx.harnesses]
    if ctx.primary_harness in [str(h) for h in as_list(model.access.get("harnesses"))]:
        if model.subagent_only:
            names = subagents_for(ctx, model, agents)
            parts.append("subagent only" + (" (%s)" % ", ".join("`%s`" % n for n in names) if names else ""))
        else:
            parts.append("this session")
    for bid in [str(b) for b in as_list(model.access.get("invoke_via"))]:
        bridge = as_dict(bridges.get(bid))
        if str(bridge.get("harness")) in harness_ids:
            parts.append("`%s`" % bid)
    if not parts:
        return UNREACHABLE
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + ", or " + parts[-1]


def subagents_for(ctx, model, agents):
    if ctx.primary_harness != "claude-code" or not model.alias:
        return []
    # bridge-* agents relay other models; they are not a way to work on this one.
    return sorted(n for n, alias in agents.items() if alias == model.alias and not n.startswith("bridge-"))


def model_cell(ctx, model, agents, label=None, primary=False):
    if model is None:
        return "none"
    if label:
        return label
    if primary and model.subagent_only:
        names = subagents_for(ctx, model, agents)
        if names:
            return "%s via `%s`" % (model.short, names[0])
        return "%s (subagent)" % model.short
    return model.short


def effort_cell(model, effort, overridden):
    if effort is None:
        return "n/a (no effort control)"
    avoid = [str(a) for a in as_list(model.effort.get("avoid")) if str(a) != effort]
    note = "never " + join_words(avoid, "or") if avoid else ""
    if overridden:
        note = "set in config" + ("; " + note if note else "")
    return "%s (%s)" % (effort, note) if note else effort


def vendor_access(config, model):
    access = as_dict(config.get("access"))
    if model.vendor in access:
        return str(as_dict(access[model.vendor]).get("type") or "none")
    if model.family == "open-weights":
        return str(as_dict(access.get("open_weights")).get("type") or "none")
    return "none"


def render_routing(ctx, rows, bridges, agents, date, version, commit, short_why=False):
    cfg = ctx.config
    user = as_dict(cfg.get("user"))
    name = str(user.get("name") or "you")
    out = []
    out.append("# Routing table for %s" % name)
    out.append("Generated %s by generate.py from config.yaml (kit %s, %s). Edit config.yaml and run "
               "/agent-orchestration:refresh rather than editing this file; lessons go in lessons.md."
               % (date, version, commit))
    out.append("")

    # Models available
    out.append("## Models available to me")
    out.append("| Model | Family | Reach it via | Effort | My cost (10 = free) | Floor | Taste | Thorough |")
    out.append("|---|---|---|---|---|---|---|---|")
    for m in ctx.enabled:
        effort = effort_for(ctx, m)
        overridden = m.id in ctx.effort_overrides and ctx.effort_overrides[m.id] not in (None, "")
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            cell(m.name), cell(m.family), cell(reach_via(ctx, m, bridges, agents)),
            cell(effort_cell(m, effort, overridden)), m.cost, m.score("floor"),
            m.score("taste"), m.score("thoroughness")))
    out.append("")

    notes = []
    config_order = list(as_dict(cfg.get("models")).keys())
    disabled = [ctx.models[i] for i in config_order if i in ctx.models and ctx.models[i].state == "disabled"]
    turned_off = [m for m in disabled if vendor_access(cfg, m) != "none"]
    no_access = [m for m in disabled if vendor_access(cfg, m) == "none"]

    def label(m):
        return m.name + (" (%s)" % m.status if m.status in ("deprecated", "preview", "unreleased") else "")
    if turned_off:
        notes.append("Disabled in config: %s." % join_words([label(m) for m in turned_off]))
    if no_access:
        notes.append("Disabled, no vendor access: %s." % join_words([label(m) for m in no_access]))
    unconf = sorted(m for m in ctx.models if ctx.models[m].state == "unconfigured")
    if unconf:
        notes.append("Not in config.models (treated as disabled; run /agent-orchestration:refresh to add): %s."
                     % join_words([ctx.models[m].name for m in unconf]))
    for m in ctx.enabled:
        if m.status in ("deprecated", "unreleased"):
            hint = str(m.role_hints.get("as_primary") or "").strip()
            notes.append("%s is %s but enabled%s" % (m.name, m.status, (' (profile: "%s")' % hint.rstrip(".") + ".") if hint else "."))
    exp = [m for m in ctx.enabled if ctx.expensive(m)]
    if exp:
        one = len(exp) == 1
        notes.append("%s %s a cost of %s, so %s may lead only wide or very wide rows plus frontend; "
                     "elsewhere %s the fallback." % (
                         join_words([m.short for m in exp]),
                         "has" if one else "have",
                         join_words(sorted(set(str(m.cost) for m in exp)), "or"),
                         "it" if one else "they",
                         "it is" if one else "they are"))
    if notes:
        out.append(wrap_para(" ".join(notes)))
        out.append("")

    # Routing table
    out.append("## Routing table")
    out.append("| Task | Primary | Fallback | Effort | Why |")
    out.append("|---|---|---|---|---|")
    for row in rows:
        tid = row.task["id"]
        if row.primary is None:
            why = sentence([row.decider or row.empty_text or "No primary"]) if row.decider else \
                sentence([row.empty_text or "No primary"])
            out.append("| %s | none | %s | — | %s |" % (
                tid, cell(model_cell(ctx, row.fallback, agents)) if row.fallback else "—", cell(why)))
            continue
        parts = [row.decider]
        if not short_why:
            parts += [row.note] + row.extra
        why = sentence(parts)
        if row.decider.startswith("Single-family setup:") and short_why:
            why = "Single-family setup: a second vendor's reviewer would catch more."
        out.append("| %s | %s | %s | %s | %s |" % (
            tid, cell(model_cell(ctx, row.primary, agents, row.primary_label, primary=True)),
            cell(model_cell(ctx, row.fallback, agents)) if row.fallback else "—",
            cell(row.effort or "—"), cell(why)))
    out.append("")

    # Standing rules
    pri = as_dict(cfg.get("priorities"))
    rules = [
        "These are defaults, not limits. If a cheaper model's output doesn't meet the bar, rerun or "
        "redo with a smarter model without asking. Judge the output, not the price tag. Escalating "
        "costs less than shipping mediocre work.",
        "Use cheaper models to gather information and try things; move the work that has to land to "
        "the model with the highest floor and taste.",
        "Priority order when axes conflict: %s." % ", ".join(ctx.order),
    ]
    if pri.get("speed_requires_review") is True:
        rules.append("Speed rule: on small tasks a faster or cheaper model may do the work only if a "
                     "smarter model with better taste reviews the result before it lands. Speed never "
                     "skips review.")
    effort_rule = "Never use `max` effort on any model."
    avoid_groups = {}
    for m in ctx.enabled:
        for lvl in as_list(m.effort.get("avoid")):
            lvl = str(lvl)
            if lvl != "max":
                avoid_groups.setdefault(lvl, []).append(m.short)
    for lvl in sorted(avoid_groups, key=lambda x: (EFFORT_WORDS.index(x) if x in EFFORT_WORDS else 99, x)):
        effort_rule += " Never `%s` on %s." % (lvl, join_words(avoid_groups[lvl], "or"))
    ov = [(ctx.models[k].short, str(v)) for k, v in sorted(ctx.effort_overrides.items())
          if k in ctx.models and v not in (None, "")]
    if ov:
        effort_rule += " Effort set in config.yaml: %s." % ", ".join("%s %s" % p for p in ov)
    rules.append(effort_rule)
    rules.append("Every delegated prompt states what you want, what \"done\" means, and when to stop "
                 "and ask. See core/strategies/delegation-prompting.md.")
    review = next((r for r in rows if r.task["id"] == "review"), None)
    feature = next((r for r in rows if r.task["id"] == "feature"), None)
    families = sorted(set(m.family for m in ctx.enabled))
    if len(families) <= 1:
        rules.append("Review: single-family. Use a different model from the implementer, and require "
                     "the reviewer to mark claims it could not confirm.")
    elif review and review.primary and feature and feature.primary:
        rules.append("Review: cross-family. Code written by %s (%s) is reviewed by %s (%s); never let "
                     "the implementer review its own work." % (
                         feature.primary.short, feature.primary.family,
                         review.primary.short, review.primary.family))
    else:
        rules.append("Review: use a model from a different family than the implementer.")
    ex_impl = (feature.primary.alias or feature.primary.short.split()[0].lower()) if feature and feature.primary else "opus"
    ex_rev = (review.primary.alias or review.primary.short.split()[0].lower()) if review and review.primary else "sol"
    rules.append("Prefix every subagent or workflow stage name with the model it runs on (e.g. "
                 "`[%s] implement-auth`, `[%s] review-auth`) so the human can see who did what."
                 % (ex_impl, ex_rev))
    rules.append("If a bridged model returns nothing, it must say so and name what it inspected; do "
                 "not re-run on an empty result.")
    logging = as_dict(cfg.get("logging"))
    if logging.get("enabled") is True:
        rules.append("Log each delegated task to %s." % (logging.get("path") or "~/.agent-orchestration/runs.jsonl"))
    for extra in as_list(as_dict(cfg.get("standing_rules")).get("extra")):  # non-list: warned, ignored
        if extra is not None and str(extra).strip():
            rules.append(str(extra).strip())
    out.append("## Standing rules")
    out.extend(wrap_bullet(r) for r in rules)
    out.append("")

    # Standing permissions
    auto = as_dict(cfg.get("autonomy"))
    level = str(auto.get("level") or "propose")
    may = as_dict(auto.get("may"))
    gate = str(auto.get("merge_gate") or "").strip()
    perms = []
    if level == "goal-mode":
        perms.append("Goal mode is on: given a stated end condition, keep working until it holds, "
                     "reporting progress as you go.")
    elif level == "merge-with-gates":
        perms.append("Merge with gates: merge only when every gate below is green.")
    else:
        perms.append("Propose mode: open PRs and propose; a human merges.")
    if gate:
        perms.append("Merge gate: `%s`. Never merge without it." % gate)
    known = [k for k, _ in AUTONOMY_LABELS]
    labels = dict(AUTONOMY_LABELS)
    may_notes = as_dict(auto.get("may_notes"))
    keys = known + sorted(k for k in may if k not in known)
    yes, no = [], []
    propose = level not in ("merge-with-gates", "goal-mode")
    for k in keys:
        if k not in may:
            continue
        text = labels.get(k, k.replace("_", " "))
        if k == "merge_prs" and propose and may[k] is True:
            no.append(text)  # propose never merges; generate() warns about the config
            continue
        qualifier = str(may_notes.get(k) or "").strip()
        if may[k] is True and qualifier:
            text += " (%s)" % qualifier
        elif k == "merge_prs" and gate and may[k] is True:
            text += " (only under the merge gate)"
        if may[k] is True:
            yes.append(text)
        elif k != "deploy":
            no.append(text)
    if may.get("deploy") is not True:
        no.append("deploy to production")
    no.append("act outside the repository without asking")
    perms.append("May: %s." % (", ".join(yes) if yes else "nothing beyond reading and proposing"))
    perms.append("May never: %s." % join_words(no, "or"))
    bots = [str(b) for b in as_list(auto.get("reviewer_bots"))]
    if bots:
        perms.append("Reviewer bots that gate merges: %s." % ", ".join(bots))
    elif may.get("merge_prs") is True and gate and not propose:
        perms.append("Reviewer bots that gate merges: none; the merge gate above stands in for them.")
    else:
        perms.append("Reviewer bots that gate merges: none; merges stay human.")
    perms.append("Staging: %s." % ("safe to exercise" if auto.get("staging_is_safe") is True else "treat as shared"))
    out.append("## Standing permissions (autonomy: %s)" % level)
    out.extend(wrap_bullet(p) for p in perms)
    out.append("")

    # How I work (verbatim)
    prefs = as_dict(cfg.get("preferences"))
    out.append("## How I work")
    pkeys = [k for k, _ in PREFERENCE_LABELS] + sorted(k for k in prefs if k not in dict(PREFERENCE_LABELS))
    plabels = dict(PREFERENCE_LABELS)
    wrote = False
    for k in pkeys:
        v = prefs.get(k)
        if v is None or not str(v).strip():
            continue
        text = str(v).strip()
        if any(l.lstrip().startswith("#") for l in text.splitlines()[1:]):
            text = text.splitlines()[0].strip()
        out.append("- %s: %s" % (plabels.get(k, k.replace("_", " ").capitalize()), text))
        wrote = True
    if not wrote:
        out.append("- Nothing recorded in config.yaml preferences.")
    out.append("")

    # Bridges
    out.append("## Bridges")
    config_bridges = []
    for entry in as_list(cfg.get("bridges")):
        entry = as_dict(entry)
        bid = str(entry.get("id") or "").strip()
        if bid:
            config_bridges.append((bid, str(entry.get("note") or "").strip()))
    config_ids = [b for b, _ in config_bridges]
    used = set()

    def config_line(bid):
        used.add(bid)
        note = dict(config_bridges)[bid]
        return wrap_bullet("`%s`: %s" % (bid, note) if note else "`%s`" % bid)

    others = [h for h in ctx.harnesses if h.get("primary") is not True]
    if not others and not config_bridges:
        out.append(wrap_bullet("None: %s is the only configured harness, so every enabled model runs "
                               "in this session or as a subagent. Add a harness to config.yaml to bring "
                               "in a bridge." % harness_name(ctx.primary_harness)))
    for h in others:
        hid = str(h.get("id"))
        ids = sorted(b for b, d in bridges.items() if str(as_dict(d).get("harness")) == hid)
        smoke = h.get("smoke_tested")
        smoke_text = ("smoke-tested %s" % smoke if smoke not in (None, False, "")
                      else "smoke test not recorded in config.yaml")
        cli = h.get("cli")
        replaced = [b for b in ids if b in config_ids and b not in used]
        if replaced:
            out.extend(config_line(b) for b in replaced)
            continue
        if any(b in used for b in ids):
            continue
        if ids:
            out.append(wrap_bullet("%s (harness %s, cli %s): %s; used through the bridge-review, "
                                   "bridge-investigate, bridge-implement and bridge-verify skills." % (
                                       ", ".join("`%s`" % b for b in ids), hid,
                                       "`%s`" % cli if cli else "not installed", smoke_text)))
        else:
            out.append(wrap_bullet("%s: no bridge in core/bridges reaches this harness." % hid))
    for bid in config_ids:
        if bid not in used:
            out.append(config_line(bid))
    return "\n".join(out) + "\n"


def render_glossary(cfg, defaults, date, version, commit):
    name = str(as_dict(cfg.get("user")).get("name") or "you")
    entries = [list(e) for e in defaults]
    overrides = cfg.get("glossary")
    overrides = overrides if isinstance(overrides, dict) else {}
    keys = [e[0] for e in entries]
    for k, v in overrides.items():
        if k in keys:
            idx = keys.index(k)
            if v is None:
                entries[idx] = None
            else:
                entries[idx][1] = str(v).strip()
        elif v is not None:
            entries.append([k, str(v).strip()])
            keys.append(k)
    out = ["# Glossary for %s" % name,
           "Generated %s by generate.py from the kit defaults plus config.yaml (kit %s, %s). Edit the "
           "glossary block in config.yaml and run /agent-orchestration:refresh rather than editing this file."
           % (date, version, commit),
           ""]
    for e in entries:
        if e is None:
            continue
        out.append(wrap_bullet("**%s**: %s" % (e[0], e[1])))
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# Comparison helpers


def drop_generated(text):
    return "\n".join(l for l in text.splitlines() if not l.startswith("Generated "))


def parse_routing_rows(text, models):
    rows = {}
    in_table = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_table = line.strip() == "## Routing table"
            continue
        if not in_table or not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if len(cells) < 4 or cells[0].lower() == "task":
            continue
        rows[cells[0].strip("` ")] = (match_model(cells[1], models), match_model(cells[2], models),
                                      norm_effort(cells[3]))
    return rows


def match_model(text, models):
    best = None
    for m in models.values():
        for name in (m.name, m.short):
            pos = text.find(name)
            if pos >= 0:
                key = (pos, -len(name))
                if best is None or key < best[0]:
                    best = (key, m.id)
    return best[1] if best else None


def norm_effort(text):
    t = text.strip().lower()
    word = re.match(r"[a-z]+", t)
    if word and word.group(0) in EFFORT_WORDS:
        return word.group(0)
    return None


def read_stamp(path):
    stamp = {"profiles": {}}
    if not os.path.isfile(path):
        return None
    for line in read_text(path).splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "profile" and len(parts) >= 3:
            stamp["profiles"][parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
        elif len(parts) >= 2:
            stamp[parts[0]] = " ".join(parts[1:])
    return stamp


def render_stamp(now, kit_root, version, commit, config_updated, tasks_hash, models):
    lines = ["generated %s" % now,
             "generator %s %s" % (GENERATOR, GENERATOR_VERSION),
             "kit_root %s" % kit_root,
             "kit_version %s" % version,
             "kit_commit %s" % commit,
             "config_updated %s" % config_updated,
             "tasks %s" % tasks_hash]
    for mid in sorted(models):
        lines.append("profile %s %s %s" % (mid, models[mid].as_of, models[mid].state))
    return "\n".join(lines) + "\n"


def write_all(out_dir, files):
    """Write every (path, text) to a temp file first; replace the targets only
    once all temp files exist. Keeps an existing file's mode, else 0644."""
    temps = []
    try:
        os.makedirs(out_dir, exist_ok=True)
        for path, text in files:
            fd, tmp = tempfile.mkstemp(prefix=".gen-", dir=out_dir)
            temps.append((tmp, path))
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            mode = (os.stat(path).st_mode & 0o7777) if os.path.exists(path) else 0o644
            os.chmod(tmp, mode)
        for tmp, path in temps:
            os.replace(tmp, path)
        temps = []
    except OSError as exc:
        raise GenError("cannot write to %s: %s" % (out_dir, exc.strerror or exc))
    finally:
        for tmp, _ in temps:
            try:
                os.unlink(tmp)
            except OSError:
                pass


# --------------------------------------------------------------------------
# Main


def now_utc():
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch and epoch.isdigit():
        return datetime.datetime.fromtimestamp(int(epoch), tz=datetime.timezone.utc)
    return datetime.datetime.now(tz=datetime.timezone.utc)


def default_config():
    home = os.environ.get("AGENT_ORCHESTRATION_HOME")
    base = home if home else os.path.join(os.path.expanduser("~"), ".agent-orchestration")
    return os.path.join(base, "config.yaml")


def generate(args, errors, warnings):
    kit_root = os.path.realpath(args.kit_root)
    if not os.path.isdir(os.path.join(kit_root, "core", "models")):
        raise GenError("kit root %s has no core/models directory" % kit_root)
    config_path = os.path.abspath(os.path.expanduser(args.config))
    if not os.path.isfile(config_path):
        raise GenError("config not found: %s (run /agent-orchestration:setup)" % config_path)
    out_dir = os.path.abspath(os.path.expanduser(args.out)) if args.out else os.path.dirname(config_path)

    load_yaml = make_yaml_loader()
    config = load_yaml(read_text(config_path))
    if not isinstance(config, dict):
        raise GenError("config %s is not a YAML mapping" % config_path)

    tasks, gloss_defaults, tasks_hash = load_tasks(kit_root)
    models = load_models(kit_root, load_yaml, errors, warnings)
    for m in models.values():
        MODEL_WORDS.update(w for w in m.name.split() if w[:1].isupper())
    bridges = load_bridges(kit_root, load_yaml)
    agents = load_agents(kit_root)
    version, commit = kit_info(kit_root)

    cfg_models = config.get("models")
    if not isinstance(cfg_models, dict):
        raise GenError("config.models is missing or not a mapping")
    for mid, entry in cfg_models.items():
        entry = as_dict(entry)
        if mid not in models:
            if entry.get("enabled") is True:
                errors.append("config.models.%s is enabled but core/models/%s.md does not exist" % (mid, mid))
            else:
                warnings.append("config.models.%s has no profile in core/models" % mid)
            continue
        m = models[mid]
        if isinstance(entry.get("enabled"), str):
            warnings.append("config.models.%s.enabled is the string %r; treated as disabled (write true or false without quotes)"
                            % (mid, entry.get("enabled")))
        m.state = "enabled" if entry.get("enabled") is True else "disabled"
        cost = entry.get("cost")
        if isinstance(cost, (int, float)) and not isinstance(cost, bool):
            m.cost = cost
        else:
            m.cost = m.score("cost_efficiency")
            if m.state == "enabled":
                warnings.append("config.models.%s has no numeric cost; using the profile's cost_efficiency (%s)"
                                % (mid, m.cost))
        if m.state == "enabled" and not m.data:
            errors.append("profile %s is enabled but could not be read" % mid)
        if m.state == "enabled" and m.status in ("deprecated", "unreleased"):
            warnings.append("%s is %s but enabled in config.models" % (mid, m.status))
    effort_cfg = config.get("effort")
    if effort_cfg is not None and not isinstance(effort_cfg, dict):
        errors.append("config.effort must be a mapping of model id to level, not %s" % type(effort_cfg).__name__)
    for mid, v in as_dict(effort_cfg).items():
        model = models.get(mid)
        if model is None:
            warnings.append("config.effort.%s names no profile in core/models" % mid)
        found = []
        check_effort(v, model, "config.effort.%s" % mid, found)
        # Malformed values and max are always errors; a level the model lacks
        # only matters once the model is enabled.
        strict = (model is None or model.state == "enabled" or not isinstance(v, str)
                  or v.strip().lower() == "max")
        if strict:
            errors.extend(found)
        else:
            warnings.extend(e + " (model not enabled)" for e in found)

    # Re-order enabled models by config order (models table order).
    ctx = Ctx(config, models, tasks)
    ctx.enabled = [models[i] for i in cfg_models if i in models and models[i].state == "enabled"]
    if not ctx.enabled:
        errors.append("no model is enabled in config.models")

    used_axes = sorted(set(a for t in tasks for a, _ in ctx.weights(t) if a != "cost")
                       | {"floor", "taste", "thoroughness", "computer_use"})
    for m in ctx.enabled:
        w, e = m.check(used_axes)
        warnings.extend(w)
        errors.extend(e)
        if reach_via(ctx, m, bridges, agents) == UNREACHABLE:
            warnings.append("%s is enabled but no configured harness or bridge reaches it" % m.id)
    extra = as_dict(config.get("standing_rules")).get("extra")
    if extra is not None and not isinstance(extra, list):
        warnings.append("standing_rules.extra must be a list of strings; ignored")
    if config.get("bridges") is not None and not isinstance(config.get("bridges"), list):
        warnings.append("bridges must be a list of {id, note}; ignored")
    auto = as_dict(config.get("autonomy"))
    if str(auto.get("level") or "propose") == "propose" and as_dict(auto.get("may")).get("merge_prs") is True:
        warnings.append("autonomy.level is propose but autonomy.may.merge_prs is true; propose never merges, "
                        "so merge PRs is listed under May never (raise the level or set merge_prs: false)")
    for k, v in as_dict(config.get("preferences")).items():
        if isinstance(v, str) and any(l.lstrip().startswith("#") for l in v.splitlines()[1:]):
            warnings.append("preferences.%s has a line starting with #; kept only its first line" % k)

    rows = build_rows(ctx, errors, warnings) if ctx.enabled else []

    # Step 5: validate.
    if ctx.enabled:
        ids = [r.task["id"] for r in rows]
        for t in tasks:
            if t["id"] not in ids:
                errors.append("task %s has no row" % t["id"])
        for r in rows:
            for key in ("primary", "fallback"):
                m = getattr(r, key)
                if m is not None and m.state != "enabled":
                    errors.append("row %s: %s %s is not enabled" % (r.task["id"], key, m.id))
        maxed = [r.task["id"] for r in rows if r.effort and r.effort.lower() == "max"]
        if maxed:
            errors.append("effort is max on rows %s; the kit never uses max" % ", ".join(maxed))

    now = now_utc()
    date = now.strftime("%Y-%m-%d")
    routing = render_routing(ctx, rows, bridges, agents, date, version, commit) if ctx.enabled else ""
    if routing and routing.count("\n") > MAX_LINES:
        routing = render_routing(ctx, rows, bridges, agents, date, version, commit, short_why=True)
        if routing.count("\n") > MAX_LINES:
            warnings.append("routing.md is %d lines, over the %d-line target" % (routing.count("\n"), MAX_LINES))
    glossary = render_glossary(config, gloss_defaults, date, version, commit)
    stamp = render_stamp(now.strftime("%Y-%m-%dT%H:%M:%SZ"), kit_root, version, commit,
                         iso(as_dict(config.get("user")).get("updated")), tasks_hash, models)

    # Compare with what is on disk.
    paths = {n: os.path.join(out_dir, n) for n in ("routing.md", "glossary.md", "routing.stamp")}
    old_routing = read_text(paths["routing.md"]) if os.path.isfile(paths["routing.md"]) else None
    old_gloss = read_text(paths["glossary.md"]) if os.path.isfile(paths["glossary.md"]) else None
    old_stamp = read_stamp(paths["routing.stamp"])

    stamp_profiles = old_stamp["profiles"] if old_stamp else {}
    changed_profiles = sorted(i for i in models if i in stamp_profiles and stamp_profiles[i][0] != models[i].as_of)
    new_profiles = sorted(i for i in models if i not in stamp_profiles)
    unconfigured = sorted(i for i in models if models[i].state == "unconfigured")

    new_rows = parse_routing_rows(routing, models)
    old_rows = parse_routing_rows(old_routing, models) if old_routing else {}
    rows_changed = [t["id"] for t in tasks if old_rows.get(t["id"]) != new_rows.get(t["id"])]

    stamp_ok = bool(old_stamp) and (
        stamp_profiles == {i: (models[i].as_of, models[i].state) for i in models}
        and old_stamp.get("tasks") == tasks_hash
        and old_stamp.get("kit_version") == version
        and old_stamp.get("config_updated") == iso(as_dict(config.get("user")).get("updated"))
        and old_stamp.get("generator") == "%s %s" % (GENERATOR, GENERATOR_VERSION))
    content_ok = (old_routing is not None and old_gloss is not None
                  and drop_generated(old_routing) == drop_generated(routing)
                  and drop_generated(old_gloss) == drop_generated(glossary))
    summary = {
        "up_to_date": bool(stamp_ok and content_ok and not errors),
        "changed_profiles": changed_profiles,
        "new_profiles": new_profiles,
        "unconfigured_profiles": unconfigured,
        "rows_changed": rows_changed,
        "errors": list(errors),
        "warnings": list(warnings),
    }
    return {
        "summary": summary, "paths": paths, "out_dir": out_dir,
        "routing": routing, "glossary": glossary, "stamp": stamp,
        "old_routing": old_routing, "old_glossary": old_gloss,
    }


def unified(old, new, path):
    return "".join(difflib.unified_diff(
        (old or "").splitlines(True), new.splitlines(True),
        fromfile=path if old is not None else "/dev/null", tofile=path + " (generated)"))


def main(argv=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Generate routing.md, glossary.md and routing.stamp "
                                     "from config.yaml and the kit's model profiles.")
    parser.add_argument("--kit-root", default=os.path.dirname(os.path.dirname(script_dir)))
    parser.add_argument("--config", default=default_config())
    parser.add_argument("--out", default=None)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="exit 0 if up to date, 1 if stale; writes nothing")
    action.add_argument("--diff", action="store_true", help="print a unified diff (default); writes nothing")
    action.add_argument("--write", action="store_true", help="write routing.md, glossary.md, routing.stamp")
    parser.add_argument("--json", action="store_true", help="print a JSON summary instead of text")
    args = parser.parse_args(argv)

    errors, warnings = [], []
    try:
        res = generate(args, errors, warnings)
    except GenError as exc:
        errors.append(str(exc))
        res = None
    except Exception as exc:  # never a traceback: 1 means "stale" to --check callers
        errors.append("%s: %s" % (type(exc).__name__, exc))
        res = None

    if res is None:
        if args.json:
            print(json.dumps({"up_to_date": False, "changed_profiles": [], "new_profiles": [],
                              "unconfigured_profiles": [], "rows_changed": [], "errors": errors,
                              "warnings": warnings}, indent=2, sort_keys=False))
        for e in errors:
            sys.stderr.write("generate.py: error: %s\n" % e)
        return 2

    summary = res["summary"]
    for w in warnings:
        sys.stderr.write("generate.py: warning: %s\n" % w)
    if errors:
        for e in errors:
            sys.stderr.write("generate.py: error: %s\n" % e)
        if args.json:
            print(json.dumps(summary, indent=2))
        return 2

    if args.write:
        try:
            write_all(res["out_dir"], [(res["paths"]["routing.md"], res["routing"]),
                                       (res["paths"]["glossary.md"], res["glossary"]),
                                       (res["paths"]["routing.stamp"], res["stamp"])])
        except GenError as exc:
            sys.stderr.write("generate.py: error: %s\n" % exc)
            if args.json:
                summary = dict(summary, errors=summary["errors"] + [str(exc)])
                print(json.dumps(summary, indent=2))
            return 2
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print("wrote %s, %s, %s" % (res["paths"]["routing.md"], res["paths"]["glossary.md"],
                                        res["paths"]["routing.stamp"]))
            if summary["rows_changed"]:
                print("rows changed: %s" % ", ".join(summary["rows_changed"]))
        return 0

    if args.check:
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print("up to date" if summary["up_to_date"] else "stale: run with --diff to see changes")
        return 0 if summary["up_to_date"] else 1

    # --diff (default)
    if args.json:
        print(json.dumps(summary, indent=2))
        return 0
    text = unified(res["old_routing"], res["routing"], res["paths"]["routing.md"])
    text += unified(res["old_glossary"], res["glossary"], res["paths"]["glossary.md"])
    sys.stdout.write(text)
    if not text:
        sys.stderr.write("generate.py: routing.md and glossary.md would not change\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
