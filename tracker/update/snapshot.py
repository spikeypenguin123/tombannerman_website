#!/usr/bin/env python3
"""snapshot.py — archive today's data file and keep the history index current.

Usage:  python3 update/snapshot.py [path/to/latest.json]

Copies latest.json to data/history/YYYY-MM-DD.json (date taken from updated_at, in
the file's own timezone) and rewrites data/history/index.json, newest first.
Run it only after validate.py passes. Safe to re-run on the same day: it overwrites
that day's snapshot.
"""
import json
import os
import shutil
import sys
from datetime import datetime

DEFAULT = "ai-dashboard/data/latest.json"


def main(argv):
    path = argv[0] if argv else DEFAULT
    d = json.load(open(path, encoding="utf-8"))
    day = datetime.fromisoformat(d["updated_at"]).date().isoformat()
    hist = os.path.join(os.path.dirname(path), "history")
    os.makedirs(hist, exist_ok=True)
    shutil.copyfile(path, os.path.join(hist, f"{day}.json"))

    entries = []
    for name in sorted(os.listdir(hist), reverse=True):
        if not name.endswith(".json") or name == "index.json":
            continue
        try:
            snap = json.load(open(os.path.join(hist, name), encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        closed = [m["aa_index"] for m in snap.get("models", []) if m.get("weights") == "closed" and m.get("aa_index") is not None]
        opn = [m["aa_index"] for m in snap.get("models", []) if m.get("weights") == "open" and m.get("aa_index") is not None]
        entries.append({
            "date": name[:-5],
            "file": name,
            "best_closed": max(closed) if closed else None,
            "best_open": max(opn) if opn else None,
            "models": len(snap.get("models", [])),
        })
    json.dump({"generated_at": d["updated_at"], "snapshots": entries},
              open(os.path.join(hist, "index.json"), "w", encoding="utf-8"), indent=2)
    print(f"archived {day}; {len(entries)} snapshot(s) in index")
    embed_fallback(d, path)
    return 0


def embed_fallback(d, path):
    """Copy the fields the founder calculator needs into its offline fallback block."""
    site = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(path))))
    page = os.path.join(site, "founder", "index.html")
    if not os.path.exists(page):
        return
    subset = {k: d[k] for k in ("updated_at", "fx", "models", "plans", "agent_hour_tokens") if k in d}
    subset["forecast"] = {"founder": d["forecast"]["founder"]}
    blob = json.dumps(subset, separators=(",", ":")).replace("</", "<\\/")
    html = open(page, encoding="utf-8").read()
    start_tag = '<script type="application/json" id="fallback-data">'
    a = html.find(start_tag)
    b = html.find("</script>", a)
    if a < 0 or b < 0:
        print("WARN: fallback block not found in founder/index.html")
        return
    html = html[:a + len(start_tag)] + blob + html[b:]
    open(page, "w", encoding="utf-8").write(html)
    print(f"refreshed founder fallback ({len(blob)} bytes)")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
