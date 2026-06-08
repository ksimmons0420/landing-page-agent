# LP Review Checklist

Structured framework for critiquing an existing landing page. Use when the user says "review this LP", "audit this page", or shares a URL and asks for feedback.

## Operating principles for the review

1. **State assumptions at the top** — goal (lead vs purchase vs signup), audience, traffic source. Don't review a paid-Meta lead-gen LP the same way as an organic-SEO content LP.
2. **Severity-rank, don't list flat.** 3 tiers: Critical (block launch) · Important (high leverage) · Polish (post-launch tests). The buyer skims by severity.
3. **Every finding has a fix.** Don't surface a problem without a concrete rewrite, test idea, or specific action.
4. **Cite the rule, not the opinion.** "Per content virality memory (Tuan Le #2) — never lead with the product." > "I think the hero should be more compelling."
5. **End with a ship order.** A numbered sequence from fastest fix to biggest bet, with time tags (5 min · this week · before launch · post-launch wk 1).

## The review pass — 10 checks in order

### 1. Hero
- **Curiosity gap in first 2s?** (Tuan Le #2). Does the headline open a question or describe the product?
- **Problem-orientated framing?** Hero should describe the prospect's problem, not the agency's capabilities.
- **Above-fold CTA visible?** Not a scroll prompt — a real conversion action.
- **Credential in second 1, not section 3?** (Tuan Le #4).

### 2. Math / numbers
- Every percentage between 0–100. No "−156%" or "+200% lift" without context.
- Every claim has a source or is hedged ("can", "up to", "as much as").
- Every $ figure has a unit (per/month, per/year, total, etc.).

### 3. Social proof
- **Named testimonials only.** Anonymous quotes ("Founder, e-com brand") undercut whichever section they're in.
- **Logo wall = verified clients only.** Co-claimed (agency-of-agency, white-label) brands need explicit permission to attribute publicly.
- **Stats density:** numbers > narrative. "$2M → $18M in 12 months" beats "we grew their revenue significantly".

### 4. Brand palette compliance
- Extract the actual hex codes used on the LP (CSS sweep or browser DevTools).
- Compare to the brand guide locked palette.
- Flag any colors used that aren't in the guide. Flag any guide colors that are absent if the guide reserves them for required roles (e.g. CTA yellow).
- See `templates/brand-palette-audit.md` for the audit pattern (when present).

### 5. Analytics + measurement
- **PostHog (or equivalent) loaded?** Quick `grep "posthog\|gtm\|gtag\|clarity\|pixel"` on HTML.
- **Funnel events firing?** Check `lp_pageview`, `lp_cta_clicked`, `lp_form_engaged`, conversion event.
- **Conversion attribution bridge?** `origin_path` + `variant` stamped onto the conversion event?
- If anything missing, **block launch**.

### 6. CTA discipline
- **How many CTA variations?** >4 = fragmented. Recommend ≤2 canonical phrasings.
- **Same CTA repeated 5-7x?** Or scattered across 12 different strings?
- **Primary CTA visible above the fold?**
- **Mobile sticky CTA on long-scroll pages?**

### 7. Pricing transparency
- If pricing is shown, is it complete (all tiers visible)?
- "Tier-based" / "Contact us for pricing" creates uncertainty. Either fully transparent or fully gated — not half.
- $ figures need units + what's included.

### 8. Name / brand consistency
- One display name used everywhere (no "ScaleHouse" vs "Scale House" vs "Scale House Media" mixing).
- Domain matches the display name.
- Legal name reserved for footer.

### 9. Visual metaphor follow-through
- If the LP uses a metaphor (rooms, journey, system), is it visually consistent throughout?
- Or is the metaphor only in the headline and then abandoned?
- Strong metaphor + weak follow-through reads as a gimmick.

### 10. Compliance + legal
- Pull the client's `feedback_{client}-compliance-rules.md` from memory if it exists.
- Check banned phrases, required disclaimers, claim hedging.
- See `learning_lp-compliance-copy-rule-loader.md` for the loader pattern.

## Deliverable format

When the user asks for the review as a deliverable (PDF, doc, slack post), use this structure:

```
PAGE 1  — Cover + verdict + severity counts (X critical / Y important / Z polish)
PAGE 2  — Critical findings 1-N (with rewrites)
PAGE 3+ — Important findings (with test ideas + rewrites)
PAGE N  — Polish + ship order + next-action options (A/B/C/D)
```

PDF rendering: HTML → headless Chrome → PDF (landscape 11×8.5, brand-compliant). Reuse the universal HTML report template.

## When NOT to use this checklist
- Initial LP build briefs (use the listicle skeleton or build pattern instead).
- A/B test design (use the experiment backlog template).
- Pre-launch QA (use the build verification checklist).

This checklist is for **critiquing an existing LP** — not designing a new one.
