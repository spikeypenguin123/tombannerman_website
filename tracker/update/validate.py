#!/usr/bin/env python3
"""validate.py — sanity-check the dashboard data file before it is published.

Usage:  python3 update/validate.py [path/to/latest.json] [--previous path/to/previous.json]

Exit code 0 = safe to publish, 1 = errors (do not publish). Warnings never block.
Standard library only, so it runs anywhere the daily job runs.
"""
import json
import re
import sys
from datetime import date, datetime, timedelta

DEFAULT = "ai-dashboard/data/latest.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def is_date(s):
    if not isinstance(s, str) or not DATE_RE.match(s):
        return False
    try:
        date.fromisoformat(s)
        return True
    except ValueError:
        return False


def num_or_none(v, lo=None, hi=None):
    if v is None:
        return True
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return False
    if lo is not None and v < lo:
        return False
    if hi is not None and v > hi:
        return False
    return True


def check(d, prev=None):
    for key in ["schema_version", "updated_at", "index", "fx", "models", "benchmarks", "history",
                "forecast", "agent_hour_tokens", "plans", "hardware", "releases", "sources", "changelog"]:
        if key not in d:
            err(f"missing top-level key: {key}")
    if errors:
        return

    if d["schema_version"] != 1:
        err("schema_version must be 1 (bump the validator together with the schema)")

    try:
        upd = datetime.fromisoformat(d["updated_at"])
        if upd.tzinfo is None:
            err("updated_at needs a timezone offset, e.g. +10:00")
        now = datetime.now(upd.tzinfo) if upd.tzinfo else datetime.now()
        if upd > now + timedelta(hours=1):
            err("updated_at is in the future")
    except (ValueError, TypeError):
        err("updated_at is not ISO 8601")

    if not num_or_none(d["fx"].get("aud_per_usd"), 0.8, 2.5) or d["fx"].get("aud_per_usd") is None:
        err("fx.aud_per_usd missing or outside 0.8–2.5")

    # models
    ids = set()
    for i, m in enumerate(d["models"]):
        tag = m.get("id", f"models[{i}]")
        for k in ["id", "name", "lab", "released", "weights"]:
            if not m.get(k):
                err(f"{tag}: missing {k}")
        if m.get("id") in ids:
            err(f"duplicate model id {m.get('id')}")
        ids.add(m.get("id"))
        if m.get("weights") not in ("open", "closed"):
            err(f"{tag}: weights must be 'open' or 'closed'")
        if not is_date(m.get("released")):
            err(f"{tag}: released is not YYYY-MM-DD")
        if not num_or_none(m.get("aa_index"), 0, 100):
            err(f"{tag}: aa_index outside 0–100")
        if not num_or_none(m.get("eci"), 50, 300):
            err(f"{tag}: eci outside 50–300")
        for k in ["cost_per_task_usd", "price_in", "price_out", "price_cache_read"]:
            if not num_or_none(m.get(k), 0, 500):
                err(f"{tag}: {k} must be null or a number 0–500")
        if m.get("price_in") and m.get("price_out") and m["price_out"] < m["price_in"]:
            warn(f"{tag}: output price below input price — check")
        if m.get("weights") == "open" and not m.get("license"):
            err(f"{tag}: open model without a licence")

    # benchmarks
    names = {m["name"] for m in d["models"]}
    for b in d["benchmarks"]:
        for k in ["name", "unit", "higher_is_better", "entries"]:
            if k not in b:
                err(f"benchmark {b.get('name')}: missing {k}")
        for e in b.get("entries", []):
            if not isinstance(e.get("value"), (int, float)):
                err(f"benchmark {b.get('name')}: non-numeric value for {e.get('model')}")
            if "vendor_reported" not in e:
                err(f"benchmark {b.get('name')}: {e.get('model')} lacks vendor_reported flag")
            if e.get("model") not in names:
                warn(f"benchmark {b.get('name')}: '{e.get('model')}' is not in models[] (fine for retired models)")

    # history: dated, sorted, monotone envelope
    for series in ["closed_frontier", "open_frontier"]:
        pts = d["history"].get(series, [])
        if len(pts) < 2:
            err(f"history.{series} needs at least 2 points")
        last_d, last_v = None, None
        for p in pts:
            if not is_date(p.get("date")):
                err(f"history.{series}: bad date {p.get('date')}")
                continue
            if last_d and p["date"] < last_d:
                err(f"history.{series}: dates not ascending at {p['date']}")
            if last_v is not None and p.get("value", 0) < last_v:
                err(f"history.{series}: frontier value fell at {p['date']} (the envelope must not decrease)")
            last_d, last_v = p["date"], p.get("value")

    # history must agree with the models table
    best = {"closed": 0, "open": 0}
    for m in d["models"]:
        if m.get("aa_index") is not None:
            best[m["weights"]] = max(best[m["weights"]], m["aa_index"])
    for w, series in [("closed", "closed_frontier"), ("open", "open_frontier")]:
        pts = d["history"].get(series) or []
        top = pts[-1]["value"] if pts else 0
        if best[w] > top:
            err(f"history.{series} ends at {top} but a {w} model scores {best[w]} — append a history point")

    # forecast parameters
    f = d["forecast"]
    for k in ["closed_growth_pts_per_month", "open_lag_months", "local_extra_lag_months"]:
        r = f.get(k, {})
        if not (isinstance(r, dict) and r.get("low") is not None and r["low"] <= r.get("central", -1) <= r.get("high", -1)):
            err(f"forecast.{k} must have low <= central <= high")
    hz = f.get("horizon", {})
    if not hz.get("measured"):
        err("forecast.horizon.measured is empty")
    for p in hz.get("measured", []):
        if p.get("minutes_80") is not None and p["minutes_80"] > p.get("minutes", 0):
            err(f"forecast.horizon.measured {p.get('model')}: 80% horizon exceeds 50% horizon")
    for o in hz.get("other_readings", []):
        if not str(o.get("url", "")).startswith("https://") or not is_date(o.get("date")):
            err(f"forecast.horizon.other_readings {o.get('subject')}: needs an https url and a YYYY-MM-DD date")
    dm = hz.get("doubling_months", {})
    if not (0 < dm.get("low", 0) <= dm.get("high", 0) <= 24):
        err("forecast.horizon.doubling_months must satisfy 0 < low <= high <= 24")
    fo = f.get("founder", {})
    mix = fo.get("task_mix", [])
    tot = sum(t.get("share", 0) for t in mix)
    if abs(tot - 1.0) > 0.011:
        err(f"forecast.founder.task_mix shares sum to {tot:.3f}, must be 1.0")
    for t in mix:
        if t.get("kind") not in ("digital", "physical"):
            err(f"task '{t.get('task')}': kind must be digital or physical")
        if not num_or_none(t.get("multiplier"), 0.5, 20):
            err(f"task '{t.get('task')}': multiplier outside 0.5–20")
    g = fo.get("multiplier_growth_monthly", {})
    if not (0 <= g.get("low", -1) <= g.get("central", -1) <= g.get("high", -1) <= 0.25):
        err("forecast.founder.multiplier_growth_monthly must be 0 <= low <= central <= high <= 0.25")
    if not is_date(fo.get("as_of")):
        err("forecast.founder.as_of must be YYYY-MM-DD")

    # plans
    for p in d["plans"]:
        tag = p.get("id")
        for k in ["id", "name", "vendor", "price_usd_month", "est_api_value_usd_month", "est_agent_hours_week", "confidence"]:
            if p.get(k) is None:
                err(f"plan {tag}: missing {k}")
        for k in ["est_api_value_usd_month", "est_agent_hours_week"]:
            r = p.get(k)
            if not (isinstance(r, list) and len(r) == 2 and 0 <= r[0] <= r[1]):
                err(f"plan {tag}: {k} must be [low, high] with low <= high")
        if p.get("default_model") and p["default_model"] not in ids:
            err(f"plan {tag}: default_model '{p['default_model']}' not in models[]")

    # releases
    for r in d["releases"]:
        if not is_date(r.get("date")):
            err(f"release '{r.get('title')}': bad date")
        if not str(r.get("url", "")).startswith("https://"):
            err(f"release '{r.get('title')}': url must be https")
        if r.get("kind") not in ("model", "hardware", "pricing", "benchmark", "policy"):
            err(f"release '{r.get('title')}': unknown kind {r.get('kind')}")
    if [r["date"] for r in d["releases"]] != sorted([r["date"] for r in d["releases"]], reverse=True):
        err("releases must be sorted newest first")

    for s in d["sources"]:
        if not str(s.get("url", "")).startswith("https://"):
            err(f"source '{s.get('title')}': url must be https")

    # day-over-day guard rails
    if prev:
        pm = {m["id"]: m for m in prev.get("models", [])}
        for m in d["models"]:
            o = pm.get(m["id"])
            if o and o.get("aa_index") is not None and m.get("aa_index") is not None:
                if abs(m["aa_index"] - o["aa_index"]) > 5:
                    warn(f"{m['id']}: aa_index moved {o['aa_index']} → {m['aa_index']} in one day — confirm (index version change?)")
        removed = set(pm) - ids
        if removed:
            warn(f"models removed since previous file: {sorted(removed)} — keep retired models with status 'superseded' instead")
        if len(d["changelog"]) < len(prev.get("changelog", [])):
            err("changelog shrank — entries must only be appended")


def main(argv):
    path, prev_path = DEFAULT, None
    args = list(argv)
    if "--previous" in args:
        i = args.index("--previous")
        prev_path = args[i + 1]
        del args[i:i + 2]
    if args:
        path = args[0]
    try:
        d = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read {path}: {e}")
        return 1
    prev = None
    if prev_path:
        try:
            prev = json.load(open(prev_path, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read previous file {prev_path}: {e}")
    check(d, prev)
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{path}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
