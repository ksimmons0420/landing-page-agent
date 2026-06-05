# CRO Data Sources — Playbook

Five sources of LP performance signal, ranked by per-query leverage. Pull from them in this order when diagnosing a leaky funnel or designing the next experiment.

## Source ranking

| # | Source | Best for | Speed | Per-query value |
|---|---|---|---|---|
| 1 | **Microsoft Clarity** | First-look "is anyone scrolling?" + dead-click + rage-click signals | 3-day API window, ~1 query/min | 🟢 Very high |
| 2 | **PostHog funnel insight** | Step-by-step drop-off + variant-level comparison | Live data, no rate limit | 🟢 Very high |
| 3 | **Form-host API** (JotForm `analyze_submissions`, Typeform, Tally) | Real customer language for hero rewrites + new ad angles | Read-only, generous limits | 🟡 High |
| 4 | **Search-term reports** (Google Ads / GSC) | Net-new keyword + intent discovery for ad groups + LP copy | Daily refresh | 🟡 High |
| 5 | **Platform-reported leads** (Meta Ads Manager / Google Ads "Conversions" column) | Spend reporting + bid optimization only — **never ground truth** | Live | 🔴 Reporting only |

## When to pull which

### "Page traffic looks normal but conversions tanked"
1. **Clarity first** — has scroll depth changed? Dead-click rate up?
2. **PostHog second** — at which step is the drop? `pageview` → `cta_clicked` → `form_engaged` → `submit_attempted` → conversion.
3. **Form-host third** — are submitted forms valid? Spam-filter false-positives?

### "Same traffic, conversions stayed the same, but ad spend doubled"
1. **Platform reporting** — are ad-platform conversions inflated (in-platform attribution lying)?
2. **PostHog conversion event** — what's the truth?
3. The gap between (1) and (2) is the **attribution gap** — close it via the conversion attribution bridge in `theme-liquid-universal-block.liquid`.

### "Designing the next A/B test, low on ideas"
1. **Form-host** `analyze_submissions` — what words are real customers using?
2. **Search-term report** — what queries are landing here?
3. **Clarity** — where do users hesitate / abandon?
4. Cross-reference: a high-intent search term that doesn't appear in the LP copy = a test idea.

### "Concluded test — was the win real?"
1. **PostHog funnel insight** — variant-level, filter bot traffic, check `experiment_assigned` event count.
2. **Clarity** — did the winning variant change behavior or just the headline number?
3. **Form-host** — are submissions valid in both variants?

## Bot filter — required for any conclusion

Meta paid traffic has high prefetch noise. Apply a bot filter BEFORE declaring a test winner:

```sql
-- PostHog HogQL — example
SELECT variant, count() as exposures, sum(converted) as conversions
FROM (
  SELECT
    properties.$feature_flag_response as variant,
    if(event = '{{CONVERSION_EVENT}}', 1, 0) as converted
  FROM events
  WHERE
    event IN ('experiment_assigned', '{{CONVERSION_EVENT}}')
    AND properties.utm_source = 'facebook'
    AND timestamp > now() - interval 14 day
    -- bot filter
    AND properties.$browser != 'Bot'
    AND properties.$ua_user_agent NOT LIKE '%headless%'
    AND properties.$ua_user_agent NOT LIKE '%bot%'
)
GROUP BY variant;
```

## Anti-patterns

❌ **Reading Meta's "Cost per Lead" as ground truth** — Meta over-attributes by 20-40% on iOS. Use it for spend reporting only.

❌ **Declaring a winner without a bot filter** — paid Meta traffic has 5-15% bot noise in the first 24h after ad approval.

❌ **Comparing this week's conversion rate to last week's without controlling for traffic source mix** — a campaign mix shift can shift LP CR by 30%+ with no actual LP change.

❌ **Pulling Clarity only after a problem is reported** — Clarity is the FIRST source you should check on any weekly review. Catch problems before the client does.

## Source-specific gotchas

### Clarity
- 3-day max window per query. Plan accordingly.
- `numOfDays=3` is the max value.
- 10 calls/day rate limit per token.
- `totalBotSessionCount` field is mislabeled (don't trust it).

### PostHog
- Person-on-events mode means `person.properties.*` reflects the value at event time, not the current value.
- Feature flag exposure only fires if `posthog.onFeatureFlags()` resolves — verify in DevTools console.
- Bot filter via `$browser != 'Bot'` catches most but not all.

### Form-host APIs
- JotForm: `analyze_submissions` is the gold standard for real customer language.
- Spam filter false-positives inflate "submitted" count — cross-check vs CRM.
- Internal test submissions also contaminate — always filter by `landing_referrer` or test-email patterns.

### Search terms
- Google Ads `keyword_view` includes negatives by default — add `AND ad_group_criterion.negative = false`.
- GSC has 3-day lag; Google Ads has 7-day lag for data-driven attribution restate (see `learning_conversion-lag-two-types.md`).

## Workflow for the weekly LP review

Per project, every Monday:

1. **Clarity** — scroll depth + quickback for last 3 days.
2. **PostHog funnel** — full funnel last 7 days, broken out by variant if a test is live.
3. **Form-host** — submitted count, spam %, real customer language sample.
4. **Search terms** — new queries that converted (Google) / new clicks (GSC).
5. **Platform reported** — only to flag attribution gap, not as truth.

Output: 5-line summary, one anomaly flagged, next-test recommendation.
