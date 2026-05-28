# Landing Page Agent — Scale House Media

A standalone landing-page CRO agent for Claude Code. No Agency OS dependency — runs as a self-contained plugin.

**What it does:** runs a continuous CRO program on every landing page you point it at. Six-event funnel instrumentation, conversion attribution bridge (closes the ~50% unattributable gap), ICE-ranked experiment backlog, weekly never-go-dark sweep, and an A/B engine on PostHog.

**Status:** v0.1.0 — MVP. The `setup` command is the focus of this release; `new-project` and `sweep` ship as functional but lightly-finished. Stack support: Shopify is fully wired today; Webflow / WordPress / vanilla HTML arrive in v0.2.0.

## Install

From inside Claude Code:

```
claude plugin marketplace add ksimmons0420/landing-page-agent
claude plugin install landing-page-agent@scalehouse --scope project
```

Then restart Claude Code. Plugins load at session start.

To verify it loaded, type `/landing-page-agent:` — autocomplete should suggest `setup`, `new-project`, and `sweep`.

## First-time setup

```
/landing-page-agent:setup
```

The agent walks you through a six-question stack questionnaire, collects platform tokens (PostHog, Microsoft Clarity, Google APIs, etc. — with hyperlinks to the right settings pages), writes `~/.landing-page-agent/.env`, and scaffolds the workspace at `~/landing-page-agent/`.

## Spin up your first project

```
/landing-page-agent:new-project
```

Captures the project profile, creates the PostHog feature flag, generates a stack-specific deploy snippet with your tokens pre-filled, and seeds an ICE-ranked experiment backlog.

## Weekly cadence

```
/landing-page-agent:sweep
```

Scans every project in the workspace and flags any that have gone DARK (no live test), are OVERDUE (live test past its decision date), or have a thin BACKLOG (<3 queued tests).

## Workspace layout

After setup:

```
~/.landing-page-agent/.env                      tokens (chmod 600)
~/landing-page-agent/projects/{slug}/
  profile.md                                   project profile + compliance
  backlog.md                                   ICE-ranked tests, status, archive
  deploy.html                                  stack-specific deploy snippet
~/landing-page-agent/memory/compliance.md      cross-project compliance rules
~/landing-page-agent/scripts/                  the sweep script
~/landing-page-agent/templates/                experiment-backlog + analytics block
```

## What it's based on

This is the standalone repackaging of patterns developed inside the Scale House Agency OS, validated against ~6 weeks of live A/B testing for a local home-services client (+37% mobile conversion lift shipped to 100%, −78% loss caught and reverted in a controlled test). See the case study at https://github.com/ksimmons0420/scalehouse-lp-cro-casestudy.

## License

Internal — not licensed for public redistribution.
