---
name: Landing Page Templates
description: Templates and helpers for the standalone Landing Page Agent. Includes the theme.liquid universal analytics block (for Shopify), the per-project experiment backlog template, and the agency-wide never-go-dark sweep script. Loaded automatically by the landing-page-dev agent when working on any LP task.
---

# Landing Page Templates Skill

Source-of-truth templates for the standalone Landing Page Agent.

## Contents

| File | Purpose |
|---|---|
| `templates/theme-liquid-universal-block.liquid` | Drop-in `<head>` block for Shopify themes. PostHog init + 6-event funnel + conversion attribution bridge. Substitute `{{POSTHOG_PROJECT_TOKEN}}` and `{{EXPERIMENT_FLAG_KEY}}` before deploying. |
| `templates/experiment-backlog-template.md` | Per-project experiment backlog with machine-readable YAML frontmatter (consumed by the sweep). |
| `templates/lp-experiment-sweep.py` | Never-go-dark sweep — scans `~/landing-page-agent/projects/*/backlog.md`, flags DARK / OVERDUE / BACKLOG-LOW. |

## Usage

The plugin's `setup` command copies the sweep script and backlog template into the user's workspace at install time:

- `~/landing-page-agent/scripts/lp-experiment-sweep.py`
- `~/landing-page-agent/templates/experiment-backlog-template.md`
- `~/landing-page-agent/templates/theme-liquid-universal-block.liquid`

The landing-page-dev agent reads from the workspace copies during normal operation, falling back to the plugin copies if the workspace is missing.

## Stack support

Currently the analytics block ships fully wired for **Shopify** only. Webflow / WordPress / vanilla-HTML variants arrive in v0.2.0 — for now the Shopify block can be adapted by hand (strip Liquid tags, swap path conditional).
