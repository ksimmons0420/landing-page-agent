---
description: Spin up a new landing-page project. Captures the profile (target URL, KPI, audience, compliance), creates the PostHog flag (if PostHog MCP is connected), generates a stack-specific deploy snippet with tokens pre-filled, and seeds the ICE-ranked experiment backlog. Run once per landing page you're optimizing.
---

# Landing Page Agent — New Project

You are spinning up a new landing-page project. Setup must already be done — `~/.landing-page-agent/.env` should exist. If it doesn't, tell the user to run `/landing-page-agent:setup` first and stop.

## Step 1 — Project intake

Use `AskUserQuestion` for each:

1. **Project slug** — a short kebab-case name (e.g. `acme-trial-lp`). This becomes the directory name and is used in event properties.
2. **Target URL** — the live LP URL (or "not deployed yet" if pre-launch).
3. **Stack** — confirm or override the default from `LP_DEFAULT_STACK`. The agent supports any builder where `<script>` can be injected into `<head>`.
4. **Conversion goal** — confirm or override the default from `LP_DEFAULT_GOAL`. Options: lead-form, purchase, signup, booking, content, newsletter, app-install, or custom.
5. **Primary conversion event name** — confirm or override the default from `LP_DEFAULT_CONVERSION_EVENT`. This is the event name the agent fires on success and uses as the goal in PostHog. The user can pick anything (e.g. `lead_form_submitted`, `order_completed`, `booking_completed`, `vip_waitlist_joined`, etc.).
6. **Form tool (only if the goal involves a form)** — confirm or override the default from `LP_FORM_TOOL`. Skip entirely if the goal is purchase, app-install, or anything else without a form.
7. **Success metric target** — numeric target for the conversion rate, CPA/CPL, or volume the project is aiming for. The agent uses this to frame test outcomes (e.g. "this hits target" vs. "still below target").
8. **Traffic source(s)** — Meta / Google / TikTok / Organic / Email / Mixed. Drives bot-filter thresholds (Meta paid has the highest prefetch noise).
9. **Audience one-liner** — who's the page for, in one sentence.

## Step 2 — Compliance pull-forward

Read `~/landing-page-agent/memory/compliance.md` if it exists. Echo the constraints back to the user and ask: "Anything project-specific to add on top of these?"

## Step 3 — Create the PostHog flag

If PostHog MCP is connected:
- Create a multivariate flag with key `{slug}-lp-test`, variants `control` (50%) and `variant_b` (50%), 100% rollout.
- Capture the flag id.

If PostHog MCP is not connected:
- Tell the user to create the flag manually at `https://app.posthog.com/feature_flags/new` and paste the flag id back.

## Step 4 — Generate the deploy snippet

Pick the right template based on the stack:

- **Shopify** → `theme-liquid-universal-block.liquid` (uses Liquid path conditional)
- **All other builders (WordPress, Webflow, Squarespace, Wix, Framer, HubSpot CMS, custom HTML, anything else)** → `vanilla-script-tag.html` (universal — works wherever a `<script>` tag in `<head>` works)

Substitute the placeholders:

- `{{POSTHOG_PROJECT_TOKEN}}` — from env
- `{{EXPERIMENT_FLAG_KEY}}` — `{slug}-lp-test`
- `{{CONVERSION_EVENT_NAME}}` — the project's primary conversion event (e.g. `lead_form_submitted`, `order_completed`)
- `{{LP_PATH_PATTERN}}` — the URL path or pattern that should trigger the block (e.g. `/pages/`, `/lp/`, `*` for everywhere); ask the user

Write the result to `~/landing-page-agent/projects/{slug}/deploy.html` (or `.liquid` for Shopify, or whatever extension fits the builder's expected input).

For builders that don't use a file paste (Wix, Squarespace, Framer all take the snippet via UI text fields), the saved file is still the source of truth — the user copy-pastes its contents into the platform's custom-code panel.

## Step 5 — Seed the backlog

Copy the experiment backlog template from `skills/landing-page-templates/templates/experiment-backlog-template.md` to `~/landing-page-agent/projects/{slug}/backlog.md`. Fill the YAML frontmatter (client, posthog_project_id, flag_key, status: queued, backlog_count: 0).

Suggest 2–3 starter test ideas based on the audience + KPI. Ask the user to ICE-score them. Set the first test live with a hypothesis + decision date (≥7d).

## Step 6 — Verify deploy

If Playwright MCP is connected and the LP is already deployed:
- Load the target URL in Playwright.
- Confirm `window.posthog` resolves.
- Trigger a synthetic CTA click.
- Check `lp_cta_clicked` event lands in PostHog.

If Playwright is not connected: give the user a manual verify checklist.

## Step 7 — Report

Echo:

> Project `{slug}` is live.
> - Profile: `~/landing-page-agent/projects/{slug}/profile.md`
> - Backlog: `~/landing-page-agent/projects/{slug}/backlog.md`
> - Deploy snippet: `~/landing-page-agent/projects/{slug}/deploy.html`
>
> First test goes live on {date}, decision date {date+7d}. Run `/landing-page-agent:sweep` weekly to stay current.

## Note on stack support

v0.1.0 ships two templates: the Shopify Liquid block (when the path conditional matters) and the **vanilla `<script>` block** (universal — works on WordPress, Webflow, Squarespace, Wix, Framer, HubSpot CMS, plain HTML, and anything else where you can paste a `<script>` tag into `<head>`). Per-builder polish (auto-generated install instructions for each platform's specific UI) lands in v0.2.0; for now the agent gives the user copy-paste-ready snippet + a quick text walkthrough of where to paste it on their builder.
