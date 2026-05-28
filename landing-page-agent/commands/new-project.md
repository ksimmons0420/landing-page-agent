---
description: Spin up a new landing-page project. Captures the profile (target URL, KPI, audience, compliance), creates the PostHog flag (if PostHog MCP is connected), generates a stack-specific deploy snippet with tokens pre-filled, and seeds the ICE-ranked experiment backlog. Run once per landing page you're optimizing.
---

# Landing Page Agent — New Project

You are spinning up a new landing-page project. Setup must already be done — `~/.landing-page-agent/.env` should exist. If it doesn't, tell the user to run `/landing-page-agent:setup` first and stop.

## Step 1 — Project intake

Use `AskUserQuestion` for each:

1. **Project slug** — a short kebab-case name (e.g. `acme-trial-lp`). This becomes the directory name and is used in event properties.
2. **Target URL** — the live LP URL (or "not deployed yet" if pre-launch).
3. **Stack** — confirm or override the default from `LP_DEFAULT_STACK`.
4. **Primary KPI** — `lead_form_submitted` / `purchase_completed` / `signup_completed` / other.
5. **Target CPL / CPA** — numeric.
6. **Traffic source** — Meta / Google / TikTok / Organic / Mixed.
7. **Audience one-liner** — who's the page for, in one sentence.

## Step 2 — Compliance pull-forward

Read `~/landing-page-agent/memory/compliance.md` if it exists. Echo the constraints back to the user and ask: "Anything project-specific to add on top of these?"

## Step 3 — Create the PostHog flag

If PostHog MCP is connected:
- Create a multivariate flag with key `{slug}-lp-test`, variants `control` (50%) and `variant_b` (50%), 100% rollout.
- Capture the flag id.

If PostHog MCP is not connected:
- Tell the user to create the flag manually at `https://app.posthog.com/feature_flags/new` and paste the flag id back.

## Step 4 — Generate the deploy snippet

Based on the stack, read the appropriate template from the plugin's `skills/templates/` directory:

- **Shopify** → `theme-liquid-universal-block.liquid`
- **Webflow** → `webflow-embed.html` (coming soon — for now use the Shopify block adapted)
- **WordPress** → `wp-snippet.php` (coming soon — for now use the Shopify block adapted)
- **Custom HTML** → `vanilla-script-tag.html` (coming soon — for now use the Shopify block stripped of Liquid)

Substitute:
- `{{POSTHOG_PROJECT_TOKEN}}` from env
- `{{EXPERIMENT_FLAG_KEY}}` = `{slug}-lp-test`
- `{{LP_PATH_PREFIX}}` — ask the user

Write the result to `~/landing-page-agent/projects/{slug}/deploy.html` (or `.liquid` / `.php`).

## Step 5 — Seed the backlog

Copy the experiment backlog template from `skills/templates/experiment-backlog-template.md` to `~/landing-page-agent/projects/{slug}/backlog.md`. Fill the YAML frontmatter (client, posthog_project_id, flag_key, status: queued, backlog_count: 0).

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

## Note

This command is shipping as MVP in v0.1.0 — for now the deploy templates only ship the Shopify pattern fully wired. Webflow / WordPress / vanilla support arrive in v0.2.0.
