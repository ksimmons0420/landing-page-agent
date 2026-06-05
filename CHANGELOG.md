# Changelog

All notable changes to the Landing Page Agent plugin.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] — 2026-06-05

Substantive feature release. Bakes in lessons from ~6 weeks of live LP work and the Scale House LP v2 review.

### Added — agent persona (`agents/landing-page-dev/agent.md`)

- **CRO operating principle #7 — Pull the pattern bank before designing a test.** Check cross-client test-results memory; don't re-test losing levers; fast-track winning ones.
- **CRO operating principle #8 — Apply content virality (Tuan Le / 3B Views, 6 principles) to every copy decision.** Format steal · curiosity gap in first 2s · Layer 3 identity copy · credential in second 1 · design for the sharer's friends · story arc with zero dead space.
- **CRO operating principle #9 — Brand palette compliance is a launch check, not a polish item.** Extract LP hex codes, compare to brand guide, flag drift before ship. Reserved CTA colors are enforced.
- **New workflow: Review an existing LP.** Pulls `templates/lp-review-checklist.md`, runs the 10-check pass, severity-ranks (Critical / Important / Polish), renders a PDF deliverable when asked.
- **New workflow: Diagnose a leaky multi-page funnel.** Per-step traffic ratio analysis, consolidate-vs-instrument decision tree, references the cross-page UTM bridge in deploy templates.
- **New workflow: Brand palette audit.** CSS sweep → compare-to-guide → comparison table output.

### Added — skill index (`skills/SKILL.md`)

- **The 6 canonical funnel events** now explicitly documented: `lp_pageview` · `lp_cta_clicked` · `lp_modal_opened` · `lp_form_engaged` · `lp_form_submit_attempted` · `{{CONVERSION_EVENT_NAME}}`. The phantom-lead signal (submit_attempted → conversion gap) called out.
- **Conversion attribution bridge** documented in-line: how `origin_path` + `variant` persistence closes the ~50% attribution gap.
- **Deploy gotchas** section — Shopify Pages script-stripping, Cloudflare cache bust, CodeMirror 6 EditorView path (`content.cmView.view`), CSS-only mobile-flip A/B variant pattern, PostHog A/B framework standard.

### Added — three new templates

- `skills/templates/lp-review-checklist.md` — structured framework for critiquing an existing LP. 10-check pass + severity-ranking + ship-order output format.
- `skills/templates/cro-data-sources-playbook.md` — five sources of LP performance signal ranked by per-query leverage (Clarity → PostHog → form-host API → search terms → platform-reported leads). When to pull which. Bot-filter SQL. Source-specific gotchas.
- `skills/templates/listicle-lp-skeleton.md` — quick-start structure for "Best X for Y" listicle LPs. Item count by intent, hero formula, item-card schema, 2026 AI-search requirements, pre-flight checklist, anti-patterns.

### Changed — deploy template (`skills/templates/vanilla-script-tag.html`)

- Added `window.lpFireModalOpened(triggerName, extraProps)` helper — completes the 6 canonical funnel events. Call from popup/modal open handlers.
- Updated header comment to list all 6 canonical events.
- Expanded "How to verify" checklist from 4 to 7 steps (now includes modal-open + form-engagement + submit-attempted).

### Changed — packaging

- Version bumped 0.1.0 → 0.2.0 in `plugin.json` + root `marketplace.json`.
- Setup command will now copy the 3 new operator-reference templates into `~/landing-page-agent/templates/` alongside the deploy snippets.
- Marketplace tags expanded: `lp-review`, `content-virality` added.

### Source memories

Patterns in this release are distilled from:

- US Turf 2026-05 A/B program (+37% mobile CR win, −78% loss caught + reverted)
- Scale House LP v2 review (2026-06-05) — brand palette audit framework, LP review structure
- Matt Steiner Meta Andromeda interview (2026-05) — feeds the diversity-not-volume operating principle
- Tuan Le / 3B Views content virality framework — feeds the 6 copy principles
- Shopify deploy patterns: theme.liquid strip workaround, CodeMirror 6 dispatch, jsdelivr CDN pipeline
- LP listicle research (Seer Interactive 2025-2026 AI-search data)

## [0.1.0] — 2026-05-28

Initial release. MVP scaffold.

### Added
- `landing-page-dev` agent with Karpathy-guidelines wired in as operating discipline
- Three commands: `/landing-page-agent:setup` · `/landing-page-agent:new-project` · `/landing-page-agent:sweep`
- Universal deploy templates: vanilla `<script>` block (any builder) + Shopify Liquid variant
- Per-project experiment backlog template + never-go-dark sweep script
- Decoupled from Shopify/JotForm anchoring — truly stack/goal/form agnostic
