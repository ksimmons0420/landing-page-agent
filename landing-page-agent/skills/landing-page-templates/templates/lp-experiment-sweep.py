#!/usr/bin/env python3
"""
LP experiment never-go-dark sweep (STANDALONE).

Auto-discovers every project's experiment backlog and flags health violations by
reading the machine-readable YAML frontmatter block. Pure file reads — no PostHog
calls, so it scales to any number of projects with zero per-project config. A
project comes under surveillance the moment its backlog.md exists.

Usage:
    python3 lp-experiment-sweep.py [--root ~/landing-page-agent/projects] [--json]

Exit code is the number of projects with a HARD flag (DARK or OVERDUE), so a
scheduled task can branch on whether action is needed.
"""
import argparse, datetime, glob, json, os, re, sys

DARK_DAYS = 14      # Live empty longer than this = never-go-dark violation
MIN_BACKLOG = 3     # fewer queued hypotheses than this = refill trigger
NULLISH = {"", "none", "null", "~", "n/a", "tbd"}


def parse_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        line = line.split("#", 1)[0]  # strip inline comments
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def as_date(s):
    try:
        return datetime.date.fromisoformat((s or "").strip())
    except ValueError:
        return None


def evaluate(fm, today):
    """Return (hard_flags, soft_flags) for one client."""
    hard, soft = [], []
    live = (fm.get("live_test_id", "") or "").strip().lower()
    has_live = live not in NULLISH
    status = (fm.get("status", "active") or "active").strip().lower()

    if status == "paused":
        soft.append("PAUSED (intentional)")
        return hard, soft

    # Rule 1 — never go dark
    if not has_live:
        ref = as_date(fm.get("last_concluded")) or as_date(fm.get("last_reviewed"))
        days = (today - ref).days if ref else 9999
        if days > DARK_DAYS:
            hard.append(f"DARK — {days}d with no live test (promote top backlog item)")
        else:
            soft.append(f"between tests — {days}d (promote soon)")

    # Rule 2 — overdue read
    dd = as_date(fm.get("decision_date"))
    if has_live and dd and dd < today:
        hard.append(f"OVERDUE READ — decision date {dd} passed (read + decide)")

    # Rule 3 — backlog low
    try:
        bc = int((fm.get("backlog_count", "0") or "0").strip())
    except ValueError:
        bc = 0
    if bc < MIN_BACKLOG:
        soft.append(f"BACKLOG LOW — {bc} queued (run CRO audit to refill)")

    return hard, soft


def sweep(root):
    today = datetime.date.today()
    pattern = os.path.join(os.path.expanduser(root), "*", "backlog.md")
    rows = []
    for path in sorted(glob.glob(pattern)):
        slug = os.path.basename(os.path.dirname(path))
        fm = parse_frontmatter(path)
        if fm is None:
            rows.append({"project": slug, "hard": ["NO_FRONTMATTER — cannot monitor"],
                         "soft": [], "path": path})
            continue
        hard, soft = evaluate(fm, today)
        rows.append({"project": fm.get("project", fm.get("client", slug)),
                     "hard": hard, "soft": soft,
                     "live_test_id": fm.get("live_test_id", ""),
                     "decision_date": fm.get("decision_date", ""),
                     "backlog_count": fm.get("backlog_count", ""),
                     "path": path})
    return rows, today


def render(rows, today):
    lines = [f"LP EXPERIMENT SWEEP — {today.isoformat()} — {len(rows)} project(s) monitored", "=" * 60]
    if not rows:
        lines.append("No backlog files found. No projects are under LP testing yet.")
        return "\n".join(lines)
    for r in rows:
        if r["hard"]:
            mark = "🔴"
        elif r["soft"]:
            mark = "🟡"
        else:
            mark = "🟢"
        lines.append(f"{mark} {r['project']}  (live: {r.get('live_test_id','?') or 'none'})")
        for f in r["hard"]:
            lines.append(f"     ⚠️  {f}")
        for f in r["soft"]:
            lines.append(f"     ·  {f}")
    hard_total = sum(1 for r in rows if r["hard"])
    lines.append("-" * 60)
    lines.append(f"{hard_total} project(s) need action now. "
                 f"{sum(1 for r in rows if r['soft'] and not r['hard'])} watch-list.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="~/landing-page-agent/projects")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rows, today = sweep(args.root)
    if args.json:
        print(json.dumps({"date": today.isoformat(), "clients": rows}, indent=2))
    else:
        print(render(rows, today))
    sys.exit(sum(1 for r in rows if r["hard"]))


if __name__ == "__main__":
    main()
