---
description: Weekly never-go-dark sweep across all landing-page projects. Flags DARK (no live test), OVERDUE (live test past decision date), and BACKLOG-LOW (<3 queued tests). Reports to CLI by default or to Slack if SLACK_WEBHOOK_URL is set. Run weekly — Monday is the suggested cadence.
---

# Landing Page Agent — Weekly Sweep

Read the sweep script and report results.

## Step 1 — Locate the sweep script

The script lives at `~/landing-page-agent/scripts/lp-experiment-sweep.py` (copied from the plugin during setup). If it's missing, tell the user to re-run `/landing-page-agent:setup` (the workspace scaffold is broken).

## Step 2 — Run it

```bash
python3 ~/landing-page-agent/scripts/lp-experiment-sweep.py
```

The script globs `~/landing-page-agent/projects/*/backlog.md`, reads the YAML frontmatter from each, and emits a report with three sections:
- 🔴 **DARK** — projects with no live test
- 🟡 **OVERDUE** — live test past its decision date
- 🟠 **BACKLOG-LOW** — fewer than 3 items in the queue
- ✅ **HEALTHY** — everything fine

## Step 3 — Report

Pretty-print the result inline to the user.

If `SLACK_WEBHOOK_URL` is set in `~/.landing-page-agent/.env`, also POST the summary to Slack (use `curl -X POST -H 'Content-Type: application/json' --data '{...}'`).

## Step 4 — Suggest next moves

For each flagged project, suggest the next action:
- DARK → promote next ICE-ranked test from the backlog
- OVERDUE → pull the conclusion read from PostHog and decide → archive → refill
- BACKLOG-LOW → brainstorm 2–3 new ICE-ranked test ideas based on recent learnings

Don't auto-execute these — just surface them.
