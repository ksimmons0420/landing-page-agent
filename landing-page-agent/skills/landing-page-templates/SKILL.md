---
name: Landing Page Templates
description: Templates and operator references for the standalone Landing Page Agent. Includes the universal analytics block (Shopify Liquid + vanilla HTML), per-project experiment backlog, never-go-dark sweep script, LP review checklist, CRO data sources playbook, and listicle LP skeleton. Loaded automatically by the landing-page-dev agent when working on any LP task.
---

# Landing Page Templates Skill

Source-of-truth templates and operator references for the standalone Landing Page Agent.

## Templates (drop-in code)

| File | Purpose |
|---|---|
| `templates/vanilla-script-tag.html` | **Universal `<script>` block.** Works anywhere a `<script>` tag in `<head>` works — WordPress, Webflow, Squarespace, Wix, Framer, HubSpot CMS, plain HTML. Default template for any builder other than Shopify. Configurable conversion event name. Fires the **6 canonical funnel events** (see below). |
| `templates/theme-liquid-universal-block.liquid` | Shopify-specific variant — same logic, wrapped in a Liquid path conditional so the analytics block only fires on `/pages/*` routes by default. Use only when the project is on Shopify. Includes the JotForm hidden-input injection pattern when the form host is JotForm. |
| `templates/experiment-backlog-template.md` | Per-project experiment backlog with machine-readable YAML frontmatter (consumed by the sweep). |
| `templates/lp-experiment-sweep.py` | Never-go-dark sweep — scans `~/landing-page-agent/projects/*/backlog.md`, flags DARK / OVERDUE / BACKLOG-LOW. |

## Operator references (decision-making playbooks)

| File | When to pull it |
|---|---|
| `templates/lp-review-checklist.md` | **Critiquing an existing LP.** When the user says "review this LP", "audit this page", or shares a URL and asks for feedback. 10-check pass + severity ranking (Critical / Important / Polish). |
| `templates/cro-data-sources-playbook.md` | **Diagnosing a leaky funnel or designing the next test.** Five sources ranked by per-query leverage: Clarity → PostHog → form-host API → search-term reports → platform-reported leads (reporting only, never ground truth). |
| `templates/listicle-lp-skeleton.md` | **Building a "Best X for Y" / listicle LP.** Hero formula, item count by intent (5-10 paid / 10-20+ SEO), per-item CTA strategy ("Check price" beats "Check on Amazon" 2x), 2026 AI-search requirements. |

## The 6 canonical funnel events (built into both deploy templates)

Every LP the agent ships instruments these:

1. **`lp_pageview`** — fires on load, includes UTM + variant
2. **`lp_cta_clicked`** — any element with `[data-lp-cta]`, `.lp-cta`, `a[role=button]`, or `button[type=submit]`
3. **`lp_modal_opened`** — explicit fire from form-trigger modals (call `posthog.capture('lp_modal_opened', { trigger: 'hero-cta' })` when a popup form opens)
4. **`lp_form_engaged`** — first `focusin` on any `<form>` element
5. **`lp_form_submit_attempted`** — on `submit` event (fires even if validation blocks)
6. **`{{CONVERSION_EVENT_NAME}}`** — primary conversion, deduped once per session, stamped with `origin_path` + `variant` + UTMs

The gap between `lp_form_submit_attempted` and `{{CONVERSION_EVENT_NAME}}` is the **phantom-lead signal** — leads that started submitting but never completed.

## Conversion attribution bridge (built into both deploy templates)

Shared thank-you pages can't attribute conversions to source page or variant (the feature flag rarely re-resolves there). The deploy templates fix this by:

1. Persisting `origin_path` + `variant` onto the LP via sessionStorage
2. Stamping them onto the conversion event when it fires
3. De-duplicating once per session

Closes the ~50% attribution gap that most LPs leave open. See `learning_lp-conversion-attribution-bridge.md` in the workspace memory.

## Usage

The plugin's `setup` command copies these into the user's workspace at install time:

- `~/landing-page-agent/scripts/lp-experiment-sweep.py`
- `~/landing-page-agent/templates/experiment-backlog-template.md`
- `~/landing-page-agent/templates/vanilla-script-tag.html`
- `~/landing-page-agent/templates/theme-liquid-universal-block.liquid`
- `~/landing-page-agent/templates/lp-review-checklist.md`
- `~/landing-page-agent/templates/cro-data-sources-playbook.md`
- `~/landing-page-agent/templates/listicle-lp-skeleton.md`

The landing-page-dev agent reads from the workspace copies during normal operation, falling back to the plugin copies if the workspace is missing.

## Stack + goal support

**Builder-agnostic** — the vanilla `<script>` block is the universal fallback. Works on any platform that lets you inject a `<script>` tag into `<head>`. The Shopify Liquid variant only exists because Shopify's theme.liquid path conditional makes it convenient to scope the block to LP routes only.

**Goal-agnostic** — the conversion event name is a placeholder (`{{CONVERSION_EVENT_NAME}}`) substituted at project creation. Whether the goal is `lead_form_submitted`, `order_completed`, `booking_completed`, `signup_completed`, `waitlist_joined`, or anything else, the same template works.

**Form-agnostic** — the form-engagement events fire on any `<form>` element via standard DOM events (`focusin` + `submit`). No JotForm / Typeform / Tally / etc. dependency in the analytics block itself. For form hosts with API introspection (JotForm `analyze_submissions`, etc.) the agent uses the relevant MCP / API only at analysis time, not at deploy time.

## Deploy gotchas — pulled from production experience

- **Shopify Pages strip `<script>` tags from page-body content.** Always put LP analytics in `theme.liquid`, NEVER in a page's content editor. Verify with DevTools console (`posthog` returns an object), NOT with `curl` (Shopify edge cache lies).
- **Cloudflare + Shopify page_cache ignore query-string busting.** After saving theme.liquid, verify deploy via fresh incognito browser console, not with `curl ?cb=`.
- **Shopify staff-account theme edits via API can fail when MCP isn't authorized.** Fall back to Playwright + CodeMirror 6 dispatch (`content.cmView.view`, not `.editorView`).
- **CSS-only mobile-flip variants** are cheap A/B test infrastructure: variant assignment via `body` class + `@media (max-width: 900px)` selectors. No JS rebuilds.
- **PostHog A/B framework:** flag + `posthog.onFeatureFlags()` + `experiment_assigned` event + `variant_iteration` property. Reuse the same flag key across iterations (don't rotate flags).
