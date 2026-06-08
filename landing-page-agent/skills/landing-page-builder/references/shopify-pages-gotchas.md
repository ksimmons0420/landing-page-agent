# Shopify Pages Drop-In HTML — Gotchas Reference

When pasting a self-contained landing-page HTML into Shopify Admin → Pages → `<>` Show HTML, the rich-text editor sanitizes the saved content. Here are the confirmed behaviors and workarounds.

## CSS sanitization

### Stripped
- CSS rules targeting elements OUTSIDE the page rich-text body — any `.shopify-section-group-*`, `.main-page-title`, `.page-title`, etc.
- `display: none !important` declarations on cross-section selectors
- Possibly `:has()` pseudo-class (couldn't fully isolate root cause; test if a rule using `:has()` disappears in the live HTML)

### Survives intact
- All CSS scoped to user-content classes (`.{brand}-lp-*`)
- Full `<script>` blocks (verified end-to-end on multiple deploys)
- Inline `style="..."` attributes set by JS at runtime
- Modern CSS within scoped class hierarchy: grid, flexbox, custom properties, animations, transforms

## Detection

Compare local file `<style>` block size to live preview:

```bash
# Local
python3 -c "
import re
html = open('local.html').read()
styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.S)
for s in styles:
    if '{brand}-lp' in s:
        print(f'local: {len(s)} chars')
"

# Live
curl -sL https://{domain}/pages/{slug} | python3 -c "
import re, sys
html = sys.stdin.read()
styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.S)
for s in styles:
    if '{brand}-lp' in s:
        print(f'live: {len(s)} chars')
"
```

If live is significantly smaller, Shopify stripped chunks. The diff usually matches a specific section of CSS — hunt for what's missing.

## Theme chrome that needs hiding

Standard Shopify themes wrap drop-in page content with:

| Element | Class / Selector |
|---------|------------------|
| Announcement bar | `.shopify-section-group-header-group` |
| Theme nav header | `.shopify-section-group-header-group` (same parent) |
| Newsletter signup | `.shopify-section-group-footer-group` |
| Theme footer | `.shopify-section-group-footer-group` (same parent) |
| Auto-rendered page title | `.main-page-title` and/or `.page-title` |
| Sibling page sections | `.shopify-section` siblings of the section containing your LP |
| Width-constraining wrappers | `.page-width`, `.page-width--narrow`, `.rte` |

## JS-based chrome hide pattern

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
    // Strip width constraints from ancestors
    var p = lp.parentNode;
    while (p && p !== document.body) {
      if (p.classList && (
        p.classList.contains('page-width') ||
        p.classList.contains('page-width--narrow') ||
        p.classList.contains('rte')
      )) {
        p.style.maxWidth = 'none';
        p.style.padding = '0';
        p.style.margin = '0';
        p.style.width = '100%';
      }
      p = p.parentNode;
    }
  }

  var main = document.querySelector('main');
  if (main) {
    main.style.padding = '0';
    main.style.margin = '0';
    main.style.maxWidth = 'none';
  }

  // Reparent fixed-positioned elements
  ['.{brand}-lp-sticky-cta', '#{brand}-lp-modal'].forEach(function(sel) {
    var el = document.querySelector(sel);
    if (el && el.parentNode !== document.body) {
      document.body.appendChild(el);
    }
  });
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', hideShopifyChrome);
} else { hideShopifyChrome(); }
window.addEventListener('load', hideShopifyChrome);
```

## position:fixed transform stacking trap

Themes wrap content in `<div class="rte scroll-trigger animate--slide-in">` etc. with CSS `transform` for slide-in effects. A `transform` on an ancestor creates a new stacking context; **`position: fixed` children are pinned to that ancestor, not the viewport.**

Symptoms:
- Modal opens "halfway off-screen"
- Sticky bar invisible
- Off-canvas drawer at body coordinates

**Fix:** reparent ALL `position: fixed` elements to `<body>` via JS on `DOMContentLoaded`. Don't miss any — sticky CTA, modal popup, drawer, toast each need their own reparent call.

## CSS variables don't cascade through reparenting

When JS moves an element to `<body>`, it leaves the `.{brand}-lp` scope where CSS custom properties (`var(--green)`) are defined. The element renders with empty values.

**Fix:** for elements that get reparented, use **literal hex values** in CSS rules — not `var()`. Document with comment so future devs don't "clean up" the literals back to vars.

## Cross-origin iframe scroll capture

Cross-origin iframes (form.jotform.com on usturf.com) create a security boundary. Wheel/touch events on the iframe area get captured by the iframe document and may not bubble to the parent for scroll. Even with `scrolling="no"`, iOS Safari often traps the first touch — user has to tap-then-cancel a field to "wake up" iframe scroll bubbling.

**Mitigations:**
- Set iframe height tall enough to contain full form (1500px) so wrapper always has overflow
- Use form provider's embed handler to dynamically resize iframe
- Make wrapper scrollbar visible (custom-styled green thumb)
- For desktop: most browsers DO bubble wheel from iframe with `scrolling="no"` to parent
- For iOS: known unfixable on cross-origin iframes — accept tap-to-wake or switch to native form

## CDN cache verification

When verifying a deploy, `?cb=$(date +%s)` cache-busting often doesn't work — Shopify Cloudflare layer hashes URL paths only. **Don't trust curl results when user says they just saved.** Have them view source directly in their browser to confirm version stamp.

Cache-bust with high-uniqueness query param + bypass headers helps slightly:
```bash
curl -sL "https://{domain}/pages/{slug}?cb=$(date +%s%N)" \
  -H "Cache-Control: no-cache" -H "Pragma: no-cache"
```

But ultimately: have the user search their saved HTML for the version stamp.

## Chat widget interference

Third-party chat widgets (Shopify Inbox, Tidio, Drift, etc.) typically sit at `bottom: 0; right: 0` with high z-index. Sticky bottom CTA covers them.

**Fix:** JS heuristic — find any `position: fixed` element within 100px of bottom-right corner that isn't our sticky bar and isn't oversized (modals/overlays), shift up by ~84px:

```js
function liftChatWidget() {
  if (window.innerWidth > 720) return;
  var stickyHeight = 84;
  document.querySelectorAll(
    'iframe, div, button, [id*="chat"], [class*="chat"], [class*="shopify-app-block"]'
  ).forEach(function(el) {
    if (el.classList.contains('{brand}-lp-sticky-cta')) return;
    if (el.closest && el.closest('.{brand}-lp-sticky-cta')) return;
    if (el.getAttribute('data-{brand}-lp-lifted') === '1') return;
    var s = window.getComputedStyle(el);
    if (s.position !== 'fixed') return;
    var rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;
    if (rect.width > 240 || rect.height > 240) return;
    var distBottom = window.innerHeight - rect.bottom;
    var distRight = window.innerWidth - rect.right;
    if (distBottom > 100 || distRight > 100) return;
    var currentBottom = parseInt(s.bottom, 10) || 0;
    el.style.setProperty('bottom', (currentBottom + stickyHeight) + 'px', 'important');
    el.setAttribute('data-{brand}-lp-lifted', '1');
  });
}
setTimeout(liftChatWidget, 1500);
setTimeout(liftChatWidget, 3500);
setTimeout(liftChatWidget, 7000);
if (window.MutationObserver) {
  var t;
  var mo = new MutationObserver(function() {
    clearTimeout(t);
    t = setTimeout(liftChatWidget, 250);
  });
  mo.observe(document.body, { childList: true, subtree: true });
  setTimeout(function() { mo.disconnect(); }, 30000);
}
```
