# Conversion Rate Optimization Checklist

Battle-tested CRO patterns for service-area landing pages. Every item below has been validated on the US Turf LP build (4.7★/472 reviews contractor with $4.99/sq.ft offer, lifetime warranty, 0% financing).

## Hero / Above-the-Fold

- [ ] **Single specific value prop in headline** — exact dollar amount or specific outcome, not vague qualifiers. "$4.99/sq.ft" beats "affordable pricing" every time.
- [ ] **Specific brand authority** — since-year, founding location, family-owned, license numbers. Concrete > generic.
- [ ] **One primary CTA in hero** — gold/contrast color pill button, action-oriented language, first-person framing ("Get My Free Estimate" not "Submit").
- [ ] **Google rating chip** — `★★★★★ {rating} · {review-count} Google reviews` as a frosted-glass pill above the eyebrow. Links to Google review search for verification.
- [ ] **3-5 trust badges** — Licensed/Insured, BBB Accredited, certifications, partnerships, awards. Use real badges from the brand's homepage + BBB profile.
- [ ] **Sub-promise reassurance line** under hero CTA — `✓ Free measurement · ✓ 24-hr quote · ✓ No obligation`. Reduces form-fill anxiety, drops drop-off ~10%.
- [ ] **3 hero feature bullets** — concrete benefits: financing terms, warranty length, free estimate.
- [ ] **Disclaimer fineprint** — "Pricing subject to change" disclaimer in 11px white at 85% opacity. Legal cover, doesn't compete with main copy.

## Conversion Path

- [ ] **8+ CTAs throughout page** — every section has a CTA, all opening the same modal (or anchoring to the form). No conversion dead zones.
- [ ] **Sticky mobile bottom CTA bar** — always-visible, 2 buttons (Call + Get Estimate), frosted-glass background, full-width thumbs-zone.
- [ ] **Phone fallback** — `tel:` links throughout for users who don't fill forms. Header phone number, hero card "or call X", sticky bar Call button.
- [ ] **CTA button copy first-person + benefit-focused** — "Get My Free Estimate" not "Submit". First-person CTAs lift conversion ~90% per Wider Funnel benchmark studies.
- [ ] **Risk-reversal language** — "free", "no obligation", "no surprises", "transparent estimates", "100% honest pricing".
- [ ] **Specific deadline on offer banner if real** — "Offer ends [date]" beats vague "limited time" by 8-12% conversion. Don't fake a deadline; if no real deadline, leave it.

## Trust Stack

- [ ] **Real install photos, not stock** — scrape from brand's CDN (Shopify Files, Cloudinary). 4-6 photos in gallery, 4/3 aspect ratio.
- [ ] **Different hero photo for desktop vs mobile** — desktop's marketing-heavy hero with baked-in text/badges crops badly on phones. Use a clean install photo on mobile.
- [ ] **Real testimonials with verbatim quotes** — `"Quote text here." — Customer F.` Always include first name + last initial for authenticity. If you can't get real quotes (Yelp/Angi block scraping, Google Maps requires JS), tell the user to paste 3 of their favorite Google reviews — don't fabricate.
- [ ] **5-star rating display** on each testimonial.
- [ ] **License numbers visible** — in FAQ "Are you licensed?" answer + footer copyright line. State + license number format.
- [ ] **Years in business** mentioned ≥3x throughout — hero subhead, FAQ, footer.
- [ ] **Industry certifications listed** — BBB, Home Advisor Screened, EPA WaterSense, Water Smart Contractor, etc.
- [ ] **Awards** — "Best of [city]" wins, "Top-rated" lists, media mentions ("As seen on [news outlet]").
- [ ] **Partnerships** — sports team partnerships, brand co-marketing relationships.

## Layout / Visual Hierarchy

- [ ] **Card depth elevation** on every card section — `box-shadow: 0 4px 24px rgba(15,60,25,0.09), 0 1px 3px rgba(15,60,25,0.05)` + hover lift `translateY(-4px)`. Flat cards read as continuous text; lifted cards read as distinct value props.
- [ ] **Gradient eyebrow pill** — green-to-dark-green gradient, white text, glow shadow. More memorable than flat label pills.
- [ ] **Icon spheres with gradient + glow** — 56px circles with brand-color gradient and matching shadow. Bigger and more dimensional than flat 44px circles.
- [ ] **Section spacing rhythm** — alternate cream/white backgrounds (`section--alt`) so the eye breaks between value prop areas.
- [ ] **F-pattern reading flow on desktop** — copy left, form right. Hero, gallery, benefits all follow scan path.
- [ ] **Mobile section padding shrinks** — 72px desktop → 56px → 44px on smallest mobile widths. Less scroll between sections.
- [ ] **Headline scaling** — h1 48px desktop / 36px tablet / 30px small mobile / 28px tiny mobile. Always readable, never dominant.
- [ ] **Touch targets ≥44px tall** — every CTA, link, close button.
- [ ] **Text-shadow on photo-backed copy** — `text-shadow: 0 2px 10px rgba(0,0,0,0.5)` for hero h1, lighter for subtext. Headline pops cleanly through any photo.

## Mobile-Specific

- [ ] **Different mobile hero photo** — use a clean install photo (no marketing text bake-ins) instead of desktop's branded hero. Test at 375px and 414px viewports.
- [ ] **Sticky bottom CTA** — frosted glass with `backdrop-filter: blur(14px)`, two buttons (Call + Get Estimate), full-width thumb zone, includes `safe-area-inset-bottom` for iPhone home bar.
- [ ] **Chat widget auto-lift** — JS heuristic shifts third-party chat widgets up 84px so they don't get hidden behind sticky CTA.
- [ ] **Hide redundant content on mobile** — if hero already has the form CTA, hide the form card's duplicate headline + sub on mobile (`@media (max-width: 720px) { .form-card__h, .form-card__sub { display: none; } }`).
- [ ] **Header CTA shrinks at <460px** — padding 12px 18px → 10px 14px so logo + button fit cleanly.
- [ ] **Service area pills 4-col → 2-col** at 720px breakpoint.
- [ ] **Benefits 4-col → 2-col → 1-col** at 900px and 540px breakpoints.
- [ ] **Force white hero text with `!important`** — themes often have global `h1 { color: ... }` that overrides our hero copy. Use `.{brand}-lp .{brand}-lp-hero__copy h1 { color: #FFF !important; }`.

## Form / Modal

- [ ] **Modal opens on every CTA throughout page** — single conversion endpoint, fewer mental forks for the user.
- [ ] **Modal preloads iframe 1.5s after page interactive** — by the time user clicks, form's already cached. No waiting.
- [ ] **Loading spinner** in modal until iframe fires `load` event, then auto-hides.
- [ ] **Body scroll-locked when modal open** — `body.modal-open { overflow: hidden; }`.
- [ ] **Esc + backdrop click + close button** all dismiss.
- [ ] **Focus management** — focus moves to close button on open, returns to trigger element on close.
- [ ] **Modal full-screen on mobile, max 560×90vh on desktop**.
- [ ] **Frosted-glass translucent sticky bar** — content visible underneath through blur, more iOS-native.
- [ ] **Visible custom scrollbar** in modal — green thumb so users see "this scrolls" if form overflows.

## Performance

- [ ] **Single self-contained HTML file** — no external CSS/JS except Google Fonts + form provider (lazy-loaded).
- [ ] **Iframe lazy-load** with explicit JS-controlled timing — preload after page interactive, not on click.
- [ ] **Sub-100ms first paint** — inline CSS, no JS-blocking external scripts above the fold.
- [ ] **Images served from brand's existing CDN** — Shopify CDN, Cloudinary, etc. Already optimized.
- [ ] **Width-bounded images** — `?width=1500` query on Shopify CDN URLs.

## Verification

- [ ] **Version stamp at top of HTML** — date/time/build-number in HTML comment so user can verify their paste.
- [ ] **Curl the live URL** to confirm deployment match — keys present, style block size matches local.
- [ ] **Test one real form submission** — confirm lead lands in form provider's inbox.
- [ ] **Test all CTAs** — every button opens modal, every tel: link dials, every anchor scrolls to form.
- [ ] **Mobile + desktop incognito test** — verify Shopify chrome is hidden, no theme bleed-through.
- [ ] **iOS Safari test** — verify sticky bar visible above home bar, modal scroll works (or tap-to-wake acceptable).

## Research-First Mindset

When the user provides only the brand name + URL, **proactively pull data yourself**:

1. **Web search the brand's reviews** — Yelp listing, Angi listing, BBB profile. Pull review counts, themes, ratings.
2. **WebFetch the brand's homepage + about page** — extract trust badges, certifications, founding year, partnerships, awards.
3. **WebFetch the brand's Google Business profile via search** — pull rating + review count.
4. **WebFetch the form provider's URL** — extract exact field schema for native form posting.
5. **Identify gaps and ask the user for ONLY what you can't find** — don't ask for the Google rating if you already pulled it.

The user's screenshot of a Google Business page with "4.7★ · 472 Google reviews" is gold — pull every visible number. The user wants you to be proactive.
