# Landing Page Agent — Scale House Media

A standalone landing-page CRO agent for Claude Code. No Agency OS dependency — runs as a self-contained plugin.

## Install (2 minutes)

**Prerequisites:** [Claude Code](https://docs.anthropic.com/claude-code) installed and signed in. PostHog account is recommended (free tier is fine) but optional — you can skip it during setup and add it later.

From inside Claude Code, run these two commands:

```
claude plugin marketplace add ksimmons0420/landing-page-agent
claude plugin install landing-page-agent@scalehouse --scope project
```

Then **restart Claude Code** — plugins load at session start.

To verify it loaded, type `/landing-page-agent:` in any Claude Code session — autocomplete should suggest `setup`, `new-project`, and `sweep`. If nothing autocompletes, fully quit Claude Code (not just close the window) and reopen.

**First time? Run setup next:**

```
/landing-page-agent:setup
```

The agent walks you through a 6-question questionnaire (~5 min), collects platform tokens (PostHog, Microsoft Clarity, etc.), and scaffolds your workspace at `~/landing-page-agent/`. Then `/landing-page-agent:new-project` spins up your first project.

---

## What it does

**Builder-agnostic. Goal-agnostic. Form-agnostic.**

- **Builders:** Shopify, WordPress, Webflow, Squarespace, Wix, Framer, HubSpot CMS, plain HTML, anything else where you can paste a `<script>` tag.
- **Goals:** lead form fills, ecommerce purchases, account signups, calendar bookings, content unlocks, newsletter signups, app installs, or anything custom you name.
- **Form tools:** JotForm, Typeform, Tally, Fillout, HubSpot, Gravity Forms, WPForms, ConvertKit, Mailchimp embed, native HTML — or no form at all.

Runs a continuous CRO program on every landing page you point it at. Funnel instrumentation (`lp_pageview` → `lp_cta_clicked` → `lp_form_engaged` → `<your conversion event>`), conversion attribution bridge (closes the ~50% unattributable gap), ICE-ranked experiment backlog, weekly never-go-dark sweep, and an A/B engine on PostHog.

**Status:** v0.2.0 — feature release. The agent now ships a structured LP review framework, content-virality discipline (Tuan Le 6 principles), brand-palette audit workflow, and three new operator-reference templates (`lp-review-checklist`, `cro-data-sources-playbook`, `listicle-lp-skeleton`). The vanilla deploy template now fires all 6 canonical funnel events (`lp_pageview` · `lp_cta_clicked` · `lp_modal_opened` · `lp_form_engaged` · `lp_form_submit_attempted` · your conversion event) with the conversion attribution bridge built in. See `CHANGELOG.md` for the full v0.2.0 diff.

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
