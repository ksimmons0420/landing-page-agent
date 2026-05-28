---
name: Landing Page Templates
description: Templates and helpers for the standalone Landing Page Agent. Includes the theme.liquid universal analytics block (for Shopify), the per-project experiment backlog template, and the agency-wide never-go-dark sweep script. Loaded automatically by the landing-page-dev agent when working on any LP task.
---

# Landing Page Templates Skill

Source-of-truth templates for the standalone Landing Page Agent.

## Contents

| File | Purpose |
|---|---|
| `templates/vanilla-script-tag.html` | **Universal `<script>` block.** Works anywhere a `<script>` tag in `<head>` works — WordPress, Webflow, Squarespace, Wix, Framer, HubSpot CMS, plain HTML. Default template for any builder other than Shopify. Configurable conversion event name (lead form / purchase / signup / booking / anything). |
| `templates/theme-liquid-universal-block.liquid` | Shopify-specific variant — same logic, wrapped in a Liquid path conditional so the analytics block only fires on `/pages/*` routes by default. Use only when the project is on Shopify. |
| `templates/experiment-backlog-template.md` | Per-project experiment backlog with machine-readable YAML frontmatter (consumed by the sweep). |
| `templates/lp-experiment-sweep.py` | Never-go-dark sweep — scans `~/landing-page-agent/projects/*/backlog.md`, flags DARK / OVERDUE / BACKLOG-LOW. |

## Usage

The plugin's `setup` command copies these into the user's workspace at install time:

- `~/landing-page-agent/scripts/lp-experiment-sweep.py`
- `~/landing-page-agent/templates/experiment-backlog-template.md`
- `~/landing-page-agent/templates/vanilla-script-tag.html`
- `~/landing-page-agent/templates/theme-liquid-universal-block.liquid`

The landing-page-dev agent reads from the workspace copies during normal operation, falling back to the plugin copies if the workspace is missing.

## Stack + goal support

**Builder-agnostic** — the vanilla `<script>` block is the universal fallback. Works on any platform that lets you inject a `<script>` tag into `<head>`. The Shopify Liquid variant only exists because Shopify's theme.liquid path conditional makes it convenient to scope the block to LP routes only.

**Goal-agnostic** — the conversion event name is a placeholder (`{{CONVERSION_EVENT_NAME}}`) substituted at project creation. Whether the goal is `lead_form_submitted`, `order_completed`, `booking_completed`, `signup_completed`, `waitlist_joined`, or anything else, the same template works.

**Form-agnostic** — the form-engagement events fire on any `<form>` element via standard DOM events (`focusin` + `submit`). No JotForm / Typeform / Tally / etc. dependency in the analytics block itself. For form hosts with API introspection (JotForm `analyze_submissions`, etc.) the agent uses the relevant MCP / API only at analysis time, not at deploy time.
