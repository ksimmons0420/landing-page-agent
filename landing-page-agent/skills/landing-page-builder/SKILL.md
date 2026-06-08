---
name: landing-page-builder
description: Build production-ready conversion landing pages for client websites. Specializes in Shopify/BigCommerce drop-in HTML, JotForm popup integration, mobile-first responsive design, premium iconography (Phosphor duotone) + ASCII-clean encoding + tactile interaction polish, CRO best practices, and SEO/GEO copy. Use when the user asks to build, recode, improve, or restyle a landing page for a client (especially competitor LP clones for paste-target CMSs), or to upgrade an LP's icons/visual polish. Also handles SEO/GEO meta copy generation for any page.
---

# Landing Page Builder

A complete playbook for building production-grade conversion landing pages. Encodes the architecture, gotchas, and CRO patterns that took hours to figure out the hard way — so future LPs ship right the first time.

## When to use this skill

The user asks to:
- Build a landing page for a client
- Recode/clone a competitor's LP for a client
- Improve an existing LP's conversion / mobile experience
- Optimize SEO or GEO meta copy
- Add specific LP elements (sticky CTA, popup form, trust signals)

This skill assumes paste-ready HTML deploy targets like Shopify Pages, but the patterns work for WordPress page builders, Webflow embeds, and any "paste HTML here" CMS.

---

## Phase 1 — Discovery

Before writing a line of code, gather:

1. **Brand DNA** — name, primary URL, brand colors (hex), logo URL, typography. If unknown, scrape the brand's homepage.
2. **The offer** — exact pricing, financing terms, warranty, rebates, deadline. Get specifics — "starting at $4.99/sq.ft" beats "affordable pricing" every time for SEO + CRO.
3. **Target audience + city/region** — for service-area businesses, the city is a primary keyword and goes in title + meta + headlines.
4. **Form provider** — JotForm, Typeform, HubSpot, Calendly. Get the form ID. Curl the form to extract field schema before coding.
5. **Hosting target** — Shopify Pages, WordPress, Webflow. Each has different paste rules and chrome to suppress.
6. **Trust assets** — Google rating + review count, BBB rating, awards, certifications, partnerships. **Always research these proactively** via web search + WebFetch — don't ask the user for data you can pull yourself. The user's Google Business profile, BBB page, and homepage are gold mines.
7. **Real customer photos** — install photos, before/afters. Scrape from the brand's CDN if hosted (Shopify CDN, Cloudinary).

If competitor clone: get the competitor URL + a screenshot. Honor the structure but rebuild every section with the client's real data.

---

## Phase 1.5 — Copy psychology (the 6 virality principles)

Architecture converts traffic; **copy** converts attention. Apply these before writing a single headline or section heading. Full detail + sources: `learning_content-virality-psychology.md` in memory. The same 6 principles power the `ad-creative-builder` skill — keep ad hook and LP headline consistent.

| # | Principle | LP application |
|---|---|---|
| 1 | **Format Steal** | Use proven LP patterns (listicle, hero + social-proof wall, comparison table, before/after). Don't innovate structure — familiarity = trust. |
| 2 | **Curiosity gap** | The H1 should **not name the product/service**. Open a question the visitor urgently wants answered; the answer lives further down the page. |
| 3 | **Layer 3 copy** | Every section heading speaks to the *identity outcome* (Means-End chain), not the feature. "Save water" is layer 2; "the smartest yard on the street" is layer 3. |
| 4 | **Credential first** | Rating + review count + years-in-business **above the fold, before the CTA**. If they scroll to find your credibility, you've already lost most of them. |
| 5 | **Shareability** | The H1 must be a one-sentence pitch that sounds good as a text to a friend — no extra context required. |
| 6 | **Story arc** | The scroll path IS the story: **Hero = Hook → Problem section = Problem → Social proof/case study = Story → CTA = Payoff.** No dead sections — if a block doesn't move the visitor forward, cut it. |

**Headline pre-write checklist:** [ ] opens a curiosity gap (doesn't name the product) · [ ] a credential sits above the fold · [ ] section headings hit layer-3 identity · [ ] H1 is one shareable sentence · [ ] scroll path follows Hook→Problem→Story→Payoff · [ ] zero filler sections. Then apply the client's compliance rules.

> The brain's <1s filter: *seen-and-liked-this-before? · something unexpected? · relates to me?* — the hero must answer yes to ≥2 before the visitor commits to reading.

---

## Phase 2 — Architecture

**Single self-contained HTML file. One paste. Zero external dependencies except Google Fonts + form provider.**

```
<!-- VERSION STAMP at top so user can verify their paste -->
<style>
  /* All scoped to .{brand}-lp-* */
</style>
<div class="{brand}-lp">
  [sections in order — see Section Library below]
</div>
<!-- Modal markup outside main wrapper for clean reparenting -->
<script>
  /* Chrome hide + modal logic + scroll fixes */
</script>
```

### CSS scoping rule

**Every class is prefixed with `{brand}-lp-`** (e.g. `usturf-lp-hero`). This prevents collision with the host theme's CSS. The root selector includes `* { box-sizing: border-box; margin: 0; padding: 0; }` scoped to `.{brand}-lp *` only — never global.

### CSS variables vs literal hex

Use CSS custom properties (`var(--green)`) for elements that stay inside `.{brand}-lp`. **Use literal hex (`#4FAE45`) for any element that gets JS-reparented to `<body>`** (sticky bars, modal popups). Custom properties don't cascade once an element leaves its declaring scope.

### Section library (in conversion-optimized order)

| # | Section | Pattern |
|---|---------|---------|
| 1 | Top promo banner | Urgency / limited-time offer in brand color, white bold text |
| 2 | Sticky header | Logo + phone (mobile-hidden) + primary CTA pill |
| 3 | Hero | Photo background + dark gradient + headline + sub + 3 bullets + CTA + reassurance line + disclaimer. **Mobile uses a different/cleaner photo** that doesn't have baked-in marketing text |
| 4 | Trust chip in hero | "★★★★★ 4.7 · 472 Google reviews" frosted-glass pill above eyebrow |
| 5 | Form card (desktop right column) | Eyebrow gradient pill + headline + sub + 3-5 trust badges + big CTA button + tel fallback |
| 6 | Gallery | 4-photo install grid, real photos, 4/3 aspect ratio, 12px border-radius |
| 7 | Benefits 4-col | **Phosphor duotone icon** on a soft tinted chip (see Phase 5.5) + title + 1-line body. Cards have `box-shadow` + hover lift |
| 8 | Testimonials 3-col | 5 stars + verbatim quote + customer name. Headline includes review count ("4.7★ across 472 Google reviews") |
| 9 | Process 3-step | Numbered circle (gradient + glow) + title + 1-line body. Cards with depth |
| 10 | Service area pills | All cities served, 4 cols on desktop, 2 on mobile |
| 11 | FAQ | `<details>` tags for native accessibility, 3-5 questions covering price/process/credentials |
| 12 | Footer | Logo, license numbers, copyright, "subject to change" disclaimer |
| 13 | Modal popup (after wrapper) | JotForm iframe OR native form — see Form Integration |
| 14 | Sticky mobile bottom CTA | Call + Get Estimate, 2 buttons, frosted bg, full-width |

---

## Phase 3 — Form integration

### Decision: iframe vs native HTML form

**Use iframe + JotForm modal when:**
- User wants the JotForm appointment-booking calendar widget
- User wants conditional form logic, file uploads, or other JotForm power features
- Trade-off accepted: iOS scroll quirks (tap-to-wake), slower modal load (~1-2s)

**Use native HTML form posting to JotForm submit endpoint when:**
- Speed/reliability matter more than calendar widget
- iOS scroll smoothness is critical
- No conditional logic needed
- Trade-off accepted: lose JotForm's live availability calendar

### Iframe modal pattern (preferred for full features)

1. **Verify the form is clean first.** `curl https://form.jotform.com/{id}` and inspect — if Panda LP / unrelated branding wraps it, tell user to clean up the form's Page Designer in JotForm before embedding.
2. **Disable reCAPTCHA on the form.** Modern JotForm has reCAPTCHA as a Form Builder canvas element (NOT a Settings toggle). User must delete it from the form canvas or invisible reCAPTCHA will silently block all submissions.
3. **Use JotForm's official `for-form-embed-handler.js`** to auto-resize iframe to content height. Load it async, attach via poll-retry (every 200ms for up to 8s) — don't single-shot the attachment because async script timing is racy.
4. **Set static iframe height to 1500px** as fallback in case the embed handler never loads. Form fits, wrapper has overflow.
5. **Wrap iframe in `.{brand}-lp-modal__scroll`** with `overflow-y: auto; -webkit-overflow-scrolling: touch` and visible custom scrollbar (green thumb) so users see "this scrolls."
6. **Preload iframe 1.5s after page is interactive** — silently fetches form while user reads hero. Modal opens snap-instant.
7. **Include a loading spinner overlay** that hides on iframe `load` event for the case user clicks before preload completes.
8. **Modal markup MUST be reparented to `<body>` via JS** — see Phase 4 gotchas. Otherwise it positions wrong inside Shopify's `.rte` transform wrapper.

### Native form pattern (fast, simple, scroll-safe)

1. **Curl the JotForm to extract exact field names** — they're not predictable. Use `q3_name[first]` / `q3_name[last]` / `q4_email` / `q6_phoneNumber[full]` / `q5_address[addr_line1/city/state/postal]` / `q7_appointment[date]` etc. Common but always verify.
2. **Include all required hidden inputs:** `formID`, `simple_spc` (= formID), `submitSource` (any descriptor), `website` (honeypot, empty).
3. **Action URL:** `https://submit.jotform.com/submit/{formID}` (no trailing slash).
4. **Method:** POST with `enctype="multipart/form-data"`.
5. **Appointment field:** since native pickers can't replicate JotForm's calendar widget, use `<input type="date">` + `<select>` for time slots. JS combines them on submit into JotForm's expected `MM/DD/YYYY HH:MM AM/PM` format and writes to hidden `q7_appointment[date]`. Also pass static `q7_appointment[duration]=30`, `[implementation]=new`, `[timezone]=America/Los_Angeles (GMT-08:00)`.
6. **Test one real submission** to confirm it lands in the JotForm Inbox.

---

## Phase 4 — Critical gotchas (the things that took hours to debug)

### Gotcha 1: Shopify HTML editor strips certain CSS

The Shopify Pages rich-text editor sanitizes pasted content. **Confirmed strips:**
- CSS rules targeting cross-section elements (`.shopify-section-group-*`, `.main-page-title`, `.page-title`, etc.)
- `display: none !important` rules that affect cross-section elements
- Possibly `:has()` pseudo-class (couldn't isolate root cause)

**Confirmed survives:**
- All CSS scoped to user-content classes (`.{brand}-lp-*`)
- Full `<script>` blocks (verified end-to-end)
- Inline `style="..."` attributes set by JS at runtime
- Modern CSS within scoped class hierarchy (grid, flexbox, animations, custom properties, transforms)

**Fix:** hide theme chrome via JavaScript on `DOMContentLoaded`. Inline styles set by JS bypass the sanitizer because they're applied at runtime, not stored in saved HTML.

```js
function hideShopifyChrome() {
  ['.shopify-section-group-header-group',
   '.shopify-section-group-footer-group',
   '.main-page-title', '.page-title']
    .forEach(function(sel) {
      document.querySelectorAll(sel).forEach(function(el) {
        el.style.display = 'none';
      });
    });
  // Hide sibling Shopify sections inside <main> that aren't ours
  var lp = document.querySelector('.{brand}-lp');
  if (lp) {
    var section = lp.closest('.shopify-section');
    if (section && section.parentNode) {
      Array.from(section.parentNode.children).forEach(function(s) {
        if (s !== section && s.classList.contains('shopify-section')) {
          s.style.display = 'none';
        }
      });
    }
    // Strip Shopify's narrow page-width + RTE width constraints
    var p = lp.parentNode;
    while (p && p !== document.body) {
      if (p.classList && (p.classList.contains('page-width') ||
          p.classList.contains('page-width--narrow') ||
          p.classList.contains('rte'))) {
        p.style.maxWidth = 'none';
        p.style.padding = '0';
        p.style.margin = '0';
        p.style.width = '100%';
      }
      p = p.parentNode;
    }
  }
  // Reset <main> padding so banner sits flush at top
  var main = document.querySelector('main');
  if (main) {
    main.style.padding = '0';
    main.style.margin = '0';
    main.style.maxWidth = 'none';
  }
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', hideShopifyChrome);
} else { hideShopifyChrome(); }
window.addEventListener('load', hideShopifyChrome); // catch lazy theme JS
```

### Gotcha 2: position:fixed transform stacking trap

Shopify themes wrap page content in animation-trigger divs like `<div class="rte scroll-trigger animate--slide-in">`. These often have a CSS `transform` for slide/fade animations. **A `transform` on an ancestor creates a new stacking context, which means `position: fixed` children get pinned to that ancestor instead of the viewport.**

Symptoms:
- Modal opens "halfway off-screen" or in the middle of page content
- Sticky bar invisible (rendered relative to a scrolled-far ancestor)
- Off-canvas drawer at body coordinates instead of viewport coordinates

**Fix:** reparent EVERY `position: fixed` element to `<body>` via JS. Don't miss any — sticky CTA, modal popup, drawer, toast, etc. all need it.

```js
// Inside hideShopifyChrome() or another DOMContentLoaded handler:
['.{brand}-lp-sticky-cta', '#{brand}-lp-modal'].forEach(function(sel) {
  var el = document.querySelector(sel);
  if (el && el.parentNode !== document.body) {
    document.body.appendChild(el);
  }
});
```

Also bump z-index high (≥9000) to clear Shopify chat widget + late-mounted theme overlays.

### Gotcha 3: CSS variables don't cascade through reparenting

When you JS-move an element to `<body>`, it leaves the `.{brand}-lp` scope where your CSS custom properties (`var(--green)`, etc.) are defined. The element renders with empty values for those properties.

**Fix:** for elements that get reparented (sticky CTA, modal contents that depend on brand vars), use **literal hex values** in the CSS rules — not `var()`. Document this in a comment so future devs don't "clean up" by replacing literals back to vars.

### Gotcha 4: Cross-origin iframe scroll capture

Cross-origin iframes (form.jotform.com on usturf.com) create a security boundary. Wheel/touch events on the iframe area get captured by the iframe document and may not bubble to the parent wrapper for scroll. Even with `scrolling="no"`, iOS Safari often traps the first touch — user has to tap-then-cancel a field to "wake up" iframe scroll bubbling.

**Mitigations (none perfect):**
- Set iframe height tall enough to contain full form (1500px) so wrapper always has overflow
- Use the JotForm embed handler to dynamically resize iframe to content
- Make wrapper scrollbar visible (custom-styled green thumb) so users see they can scroll
- For desktop: most browsers DO bubble wheel from iframe with `scrolling="no"` to parent
- For iOS: known unfixable quirk on cross-origin iframes — accept tap-to-wake or switch to native form

### Gotcha 5: Shopify CDN cache ignores query strings

When verifying a deploy, `?cb=$(date +%s)` cache-busting often doesn't work — Shopify Cloudflare layer hashes URL paths only. **Don't trust curl results when Kyle says he just saved.** Have user view source directly in their browser to confirm version stamp.

### Gotcha 6: JotForm reCAPTCHA blocks native submissions silently

JotForm forms ship with `recaptcha_invisible` enabled by default. The submit endpoint rejects any submission missing a valid reCAPTCHA token. There's no error to the user — leads just disappear.

**Fix:** have the user disable reCAPTCHA on the form. In modern JotForm (2024+), reCAPTCHA is a **Form Builder canvas element** (NOT a Settings toggle). Steps: Form Builder → find the CAPTCHA element on the form canvas → click → trash. The honeypot field + JotForm's `simple_spc` already filter most spam.

### Gotcha 7: Chat widgets get hidden behind sticky CTA

Third-party chat widgets (Shopify Inbox, Tidio, etc.) typically sit at `bottom: 0; right: 0` with high z-index. Our sticky bottom CTA covers them.

**Fix:** JS heuristic that finds any `position: fixed` element within 100px of bottom-right corner, isn't our own sticky bar, and isn't an oversized overlay — then shifts it up by ~84px so it floats above the bar. Run on multiple intervals (1.5s, 3.5s, 7s) and via MutationObserver for 30s post-load to catch lazy-mounted widgets.

---

## Phase 5 — Mobile-first patterns

### Hero photo strategy
**Mobile gets a different hero photo than desktop.** Desktop's marketing-heavy hero (with baked-in text/badges/mascots) crops badly on phone widths. Use a clean install photo on mobile via media query background-image override. Tag both photos in a CSS comment showing which is which.

### Force white text on photos
Themes often have a global `h1 { color: ... }` rule that overrides our hero copy. Use `!important` with high specificity:
```css
.{brand}-lp .{brand}-lp-hero,
.{brand}-lp .{brand}-lp-hero__copy,
.{brand}-lp .{brand}-lp-hero__copy h1,
.{brand}-lp .{brand}-lp-hero__copy h1 *:not(strong),
.{brand}-lp .{brand}-lp-hero__sub,
.{brand}-lp .{brand}-lp-hero__features li {
  color: #FFFFFF !important;
}
```

### Text shadows for legibility
Hero text on a photo background needs `text-shadow` to read cleanly:
```css
.hero h1 { text-shadow: 0 2px 10px rgba(0,0,0,0.5), 0 1px 3px rgba(0,0,0,0.4); }
.hero h1 strong { text-shadow: 0 3px 14px rgba(0,0,0,0.55); }
.hero p { text-shadow: 0 1px 6px rgba(0,0,0,0.5); }
```

### Sticky bottom CTA bar
Frosted-glass translucent (`background: rgba(255,255,255,0.72); backdrop-filter: blur(14px) saturate(160%)`), 2 buttons (Call + primary action), full-width, hides when modal is open via `body.{brand}-lp-modal-open` class, includes safe-area-inset-bottom for iPhones with home bar.

### Card depth elevation
**Flat cards read as continuous text.** Add `box-shadow: 0 4px 24px rgba(15, 60, 25, 0.09), 0 1px 3px rgba(15, 60, 25, 0.05)` + hover transform `translateY(-4px)` + heavier shadow on hover. Apply to ALL card sections (benefits, testimonials, process, FAQ, area pills) for consistent visual rhythm.

### Touch targets
All interactive elements ≥44px tall. CTAs use `padding: 14px 18px` minimum.

---

## Phase 5.5 — Visual & interaction polish (the premium-feel layer)

> The gap between "clearly AI-built" and "a designer made this" is a handful of small, consistent details: two-tone icons, clean encoding, and tactile micro-interactions. Apply all three on every build. Validated across the Strider Bikes 6-LP set (2026-06).

### Iconography — Phosphor duotone (never ship hand-coded flat SVGs)

Hand-coded single-stroke SVGs are the #1 "a script generated this" tell. Replace them with **Phosphor duotone** (9,000+ icons, MIT-licensed, free) — the two-tone fill reads as *designed*. Full detail + gotchas: `learning_lp-phosphor-duotone-icon-system.md` in memory.

**Fetch (no build step, bakes inline → zero runtime deps, stays ASCII):**
```
https://api.iconify.design/ph:{name}-duotone.svg     # e.g. ph:shield-check-duotone
```
Grab the inner `<g>…</g>` and wrap it in your own `<svg class="ph ph-duo" width="30" height="30" viewBox="0 0 256 256" aria-hidden="true">`. Other free duotone sets on the same API: `solar:`, `tabler:`.

**The recolor trick (the reusable bit).** Phosphor duotone = a primary `<path>` (inherits `currentColor`) + a secondary `<path opacity=".2">` (the fill shape). Recolor both in CSS:
```css
.{brand}-lp .ph { display:inline-block; vertical-align:middle; flex:0 0 auto; }
/* LOUD — two brand colors, for benefit/feature tiles (28–32px) on a soft tinted chip */
.{brand}-lp .ph-duo             { color:#004CFF; }                /* primary detail = brand */
.{brand}-lp .ph-duo path[opacity]{ opacity:1; fill:#FFCD03; }     /* fill shape -> accent  */
/* QUIET — one hue at low opacity, for trust/guarantee rows (~22px), kept subordinate */
.{brand}-lp .ph-duo-b           { color:#004CFF; }
.{brand}-lp .ph-duo-b path[opacity]{ opacity:.16; }
```
Two treatments cover most LPs: **loud** (benefit/feature tiles on a soft-tinted square chip) and **quiet** (guarantee/trust strips). Verify render via DOM: `getComputedStyle(path).fill` + `getBoundingClientRect().width > 0`.

**Rollout gotchas:**
- **Anchor by a unique path substring** when swapping existing hand-SVGs (`<svg…(?!</svg>)…{anchor}…</svg>`, count=1) — surgical, no false hits.
- **Path collisions:** if the same icon path appears twice on a page (e.g. a shield in both the guarantee strip *and* a feature tile), anchor-replace hits only the first — fall back to **document-order / index-based** replacement for that page.
- **Pick by meaning, not literal shape:** "it actually gets used" → `heart` (loved), not a checkmark. Means-end beats literal.
- **Don't force icons onto number-chip lists** (listicle items, "5 reasons" rows) — the number IS the visual anchor. Add icons to badges, methodology criteria, and feature tiles instead.

### Encoding — keep it ASCII-clean (no mobile mojibake)

Raw multibyte characters + a missing charset = garbled glyphs (★, —, ·, →, emoji) on real phones even when it looks fine in your editor. Standard for every LP:
- `<meta charset="utf-8">` in the markup — don't rely on the host setting it.
- **Convert every glyph to an HTML entity:** `★`→`&#9733;`, `·`→`&middot;`, `—`→`&mdash;`, `→`→`&rarr;`, `–`→`&ndash;`, `'`→`&rsquo;`, quotes→`&ldquo;`/`&rdquo;`.
- **Emoji → inline SVG** (the duotone icons above), never raw emoji codepoints.
- In JS strings use `\uXXXX` escapes (em-dash = `—`), not literal glyphs.
- **Gate before ship:** `python3 -c "s=open('file.html',encoding='utf-8').read(); print('non-ascii:', sum(ord(c)>127 for c in s))"` → must be **0**.

### Interaction polish — the ui-ux-pro-max pass

Tactile micro-interactions make a static page feel built. Apply this scoped block (validated on Strider, 2026-06):
- **Focus-visible** rings on every interactive element (`outline:3px solid {brand}; outline-offset:3px`) — keyboard + a11y, kills the "no focus state" tell.
- **Press feedback:** `.btn:active{ transform:scale(.97) }` + `touch-action:manipulation` (removes the 300ms tap delay) + `-webkit-tap-highlight-color:transparent`.
- **Tabular numbers** on prices/stats (`font-variant-numeric:tabular-nums`) — no layout shift between values.
- **Scroll-reveal, but with a failsafe.** Subtle fade/translate via IntersectionObserver, gated by `prefers-reduced-motion`. **CRITICAL:** add a JS timeout failsafe (`setTimeout(revealAll, 1500)`) and never let the pre-reveal CSS hide content without JS — a broken observer or no-JS visitor must still see everything. (Strider regression caught this: 20 elements stuck hidden until the failsafe was added.)
- **Respect `prefers-reduced-motion: reduce`** — disable animations/transitions entirely.

Pull the `ui-ux-pro-max` skill for the full ruleset on any net-new design.

---

## Phase 6 — CRO checklist

### Above-the-fold essentials
- [ ] Single specific value prop in headline ("$4.99/sq.ft" not "affordable")
- [ ] Specific brand authority (since {year}, family-owned, license #s)
- [ ] One primary CTA in hero
- [ ] Google rating chip with star + count + source ("4.7★ · 472 Google reviews")
- [ ] Trust badges (3-5): Licensed/Insured, BBB, certifications, partnerships, awards
- [ ] Sub-promise reassurance ("Free measurement · 24-hr quote · No obligation")

### Conversion path
- [ ] 8+ CTAs throughout page, all opening the same modal
- [ ] Sticky mobile bottom CTA (always visible)
- [ ] Phone fallback (`tel:` link) for users who don't fill forms
- [ ] CTA button text first-person + benefit-focused ("Get My Free Estimate")
- [ ] Risk-reversal language: "free", "no obligation", "no surprises"
- [ ] Specific deadline on offer banner if real (e.g. "Offer ends [date]")

### Trust stack
- [ ] Real install photos, not stock
- [ ] Real testimonials with verbatim quotes + customer first names + initials
- [ ] License numbers visible in FAQ + footer
- [ ] Years in business mentioned ≥3x
- [ ] Industry certifications listed
- [ ] All trust signals research-backed (web search the brand's BBB, Google, Yelp, homepage before writing)

---

## Phase 7 — SEO + GEO meta copy

### Page title formula

`{Primary keyword} — {Specific number/offer} | {Brand}` (target ≤60 chars for display, ≤70 hard cap)

Example: `Las Vegas Artificial Turf — $4.99/sq.ft + Lifetime Warranty | US Turf` (69 chars)

Why it wins:
- Primary keyword "Las Vegas Artificial Turf" front-loaded
- Specific price ($4.99/sq.ft) — numbers boost CTR ~30% in Google's title-display tests
- Differentiator (Lifetime Warranty) AI engines can cite for GEO
- Brand last for branded-search recognition

### Meta description formula

`{Authority/longevity hook}. {Service} from {price}, {differentiator}, {dollar-value benefit}. {Star rating} · {review count} {source}.` (target 130-160 chars, all key info in first 120 for mobile snippets)

Example (160 chars exact): `Family-owned Las Vegas artificial turf installer since 2003. Starting at $4.99/sq.ft, lifetime warranty, $7/sq.ft water rebates. 4.7★ across 472 Google reviews.`

Why it wins:
- "Family-owned … since 2003" = authority + experience signal
- Stacks every cite-able number (4.99, 7, 4.7, 472, 2003)
- All offer specifics in first 120 chars (mobile-safe)
- Three primary keywords woven naturally (city + service + role)

### GEO-specific rules

AI engines (ChatGPT, Perplexity, Google AI Overviews) cite content with:
- Specific numbers (rating, count, price, year, percentage)
- Authority markers (BBB, certifications, awards, longevity)
- Declarative cite-able statements (not vague claims)
- Freshness signals (year mentioned, "current," recent updates)
- E-E-A-T (Experience, Expertise, Authoritativeness, Trust)

Pack the meta description with cite-able facts so when an AI summarizes "best artificial turf company in Las Vegas," your meta has the facts it needs.

---

## Phase 8 — Deploy + verify

### Versioning
Add a visible version stamp at the top of the HTML:
```html
<!--
  {BRAND} LP · VERSION YYYY-MM-DD · HH:MM PT · build v{N} ({short note})
  Search this file for "build v{N}" to confirm you have the latest paste.
-->
```

Bump the build number on every push. Tell the user to search the file for the version after pasting to verify it landed.

### Multi-device live preview (remote review before deploy)

To let the client — or you, on a phone — review a self-contained LP before it's pasted live, serve it over a quick public tunnel:
```bash
python3 -m http.server 8755 --directory {lp-dir} &
cloudflared tunnel --url http://127.0.0.1:8755   # prints a temp https://*.trycloudflare.com URL
```
Ephemeral (dies on restart) and review-only — **not** a real deploy. Ideal for "approve these before I host them." For a programmatic render/QA check, drive it with Playwright at a phone viewport (390×844) and assert icon/encoding state via `getComputedStyle` + `getBoundingClientRect`.

### Verification curl

```bash
curl -sL "https://{client-domain}/pages/{slug}?cb=$(date +%s%N)" -o /tmp/lp_check.html

# Verify:
grep -oE "build v[0-9]+" /tmp/lp_check.html        # → matches what you just pushed
grep -c "{key-feature-class}" /tmp/lp_check.html    # → non-zero
python3 -c "import re; html=open('/tmp/lp_check.html').read(); \
  styles=re.findall(r'<style[^>]*>(.*?)</style>', html, re.S); \
  print([len(s) for s in styles if '{brand}-lp' in s])"  # → matches local
```

Note: Shopify CDN often ignores query-string cache busting. If curl shows old version, ask user to view source in their browser directly.

### Pre-deploy checklist

- [ ] Real client phone number in `tel:` links + header + footer + sticky CTA
- [ ] Real client license numbers in FAQ + footer
- [ ] Real client logo URL (from CDN, not placeholder)
- [ ] Real install photos, all 4-6 gallery slots filled
- [ ] Form action URL points at the right form ID
- [ ] reCAPTCHA disabled on JotForm (if native form posting)
- [ ] Version stamp at top of HTML
- [ ] CTA copy first-person + benefit-focused everywhere
- [ ] All `var(--*)` references inside `.{brand}-lp` scope; reparented elements use literal hex
- [ ] `.{brand}-lp-sticky-cta` and `#{brand}-lp-modal` both reparented to body in JS
- [ ] Sub-promise reassurance line under hero CTA
- [ ] Mobile hero uses cleaner photo (different from desktop)
- [ ] All cards have box-shadow elevation (no flat cards)
- [ ] FAQ has 3-5 questions covering price/process/credentials
- [ ] SEO title (≤70 chars) + meta description (≤160 chars) drafted
- [ ] **0 raw non-ASCII** (entities + inline SVG; `<meta charset="utf-8">` present)
- [ ] Icons use the **Phosphor duotone** system — no flat single-stroke SVGs (Phase 5.5)
- [ ] Focus-visible rings + press-scale + `prefers-reduced-motion` guard present
- [ ] Scroll-reveal (if used) has a no-content-hidden failsafe + works with JS disabled

---

## References

- `references/shopify-pages-gotchas.md` — Deep dive on Shopify Pages CSS sanitization, transform stacking trap, CDN caching, chrome-hide patterns
- `references/cro-checklist.md` — Full conversion-rate checklist
- `references/seo-geo-formulas.md` — SEO + GEO copy formulas with worked examples
- `learning_lp-phosphor-duotone-icon-system.md` (memory) — Phosphor/Iconify duotone icon system: fetch, the CSS recolor trick, rollout gotchas (Phase 5.5 deep dive)
- The first reference implementation: US Turf LP at `https://github.com/ksimmons0420/usturf-renders/blob/main/landing-page/usturf-lp-artificial-turf-sale.html` — every pattern in this skill is implemented there

## When in doubt

- **Curl the form provider's URL** to extract real field schema — never guess names like `q3_fullName`
- **Web-search the client's Google/BBB/Yelp pages** to pull rating + review count proactively — don't ask the user for data you can fetch
- **Ship a version stamp** — saves hours when debugging "why isn't my fix showing"
- **Reparent everything fixed-positioned** — modals, sticky bars, drawers, toasts. The transform trap will hit you eventually
- **Use literal hex for reparented elements** — CSS variables don't follow elements out of their declaring scope
