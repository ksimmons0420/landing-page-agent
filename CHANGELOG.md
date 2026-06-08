# Changelog

All notable changes to the Landing Page Agent plugin.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.3.1] — 2026-06-07

Mobile-correctness patch — caught on a real phone during the Strider review: pages rendered desktop-width on mobile despite correct responsive CSS.

### Added — `landing-page-builder` skill

- **Viewport guard (Phase 2 — Architecture).** Paste-blocks have no `<head>` of their own, so a standalone preview — or any host theme missing the tag — renders at ~980px desktop width on phones and the mobile breakpoints never fire. New standard: a self-healing, idempotent `<meta name="viewport">` injector at the top of every block (a no-op when the host already supplies one).
- **Preview-testing fix (Phase 8).** Corrected the multi-device preview guidance: **never force the viewport** (`setViewportSize` / `browser_resize`) to certify responsiveness — it masks a missing viewport meta and yields a false "looks great on mobile." Emulate a real device or assert the meta resolves in the live DOM, then confirm on real hardware. Forced-viewport screenshots are fine only for CSS-change checks (icon size, rank alignment).

### Added — `landing-page-templates` skill

- **Listicle rank badge treatment** (`templates/listicle-lp-skeleton.md`) — make the rank large and left-aligned; don't let an inline-block rank silently inherit `text-align:center` from a centered media column.

## [0.3.0] — 2026-06-07

Consolidation release. Brings the full LP **build-craft** playbook into the plugin (previously a separate user-level skill) so the agent is a single, self-contained home — and bakes in the visual-polish layer learned on the Strider Bikes 6-LP build.

### Added — bundled `landing-page-builder` skill (`skills/landing-page-builder/`)

The complete build playbook now ships inside the plugin: Phase 1 discovery → 1.5 copy psychology → 2 architecture + section library → 3 form integration → 4 critical gotchas → 5 mobile-first → **5.5 visual & interaction polish (new)** → 6 CRO checklist → 7 SEO/GEO → 8 deploy + verify. Plus `references/` (cro-checklist, seo-geo-formulas, shopify-pages-gotchas).

### Added — Phase 5.5: visual & interaction polish (the premium-feel layer)

- **Iconography — Phosphor duotone.** Never ship hand-coded flat SVGs. Iconify fetch (`api.iconify.design/ph:{name}-duotone.svg`, MIT, zero deps, stays ASCII) + the CSS recolor trick (`.ph-duo path[opacity]{opacity:1;fill:#FFCD03}` for the loud two-color treatment; `.ph-duo-b` for the quiet trust treatment). Two-treatment system, sizing, and four rollout gotchas — anchor-by-path-substring, **document-order fallback for path collisions**, pick-by-meaning (heart, not checkmark), don't-icon number-chip lists.
- **Encoding — ASCII-clean (no mobile mojibake).** `<meta charset="utf-8">` + entity conversion table + emoji→inline-SVG + `\uXXXX` in JS + the `sum(ord(c)>127)==0` gate.
- **Interaction polish — the ui-ux-pro-max pass.** Focus-visible rings, press-scale, tabular-nums, and scroll-reveal **with a no-content-hidden failsafe** (a broken observer / no-JS visitor must still see everything), reduced-motion guard.
- **Multi-device live preview** recipe (`http.server` + `cloudflared` quick tunnel) for remote client review before deploy.
- Pre-deploy checklist gains: 0 raw non-ASCII · duotone icons (no flat SVGs) · focus/press/reduced-motion · scroll-reveal failsafe.

### Changed

- **Skills restructured to the canonical subdir layout.** `skills/SKILL.md` → `skills/landing-page-templates/SKILL.md` (templates ride along), making room for the second bundled skill. Template path references updated across `agents/landing-page-dev/agent.md`, `commands/setup.md`, and `commands/new-project.md`.
- **Agent persona now pulls two skills at the start of every build** — `landing-page-builder` (how you build the page) alongside `karpathy-guidelines` (how you write the code).
- Manifests + description updated to advertise BigCommerce as a first-class paste target and the build-craft/iconography capability.

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
