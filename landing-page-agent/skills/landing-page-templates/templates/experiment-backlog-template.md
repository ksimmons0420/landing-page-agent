---
# MACHINE-READABLE STATE — the agency-wide sweep reads ONLY this block.
# Keep it in sync with the human-readable body below on every update.
client: {slug}
posthog_project: {project-id}        # which PostHog project to query for the data-pull layer
flag_key: {flag-key}
status: active                       # active | paused | none
live_test_id: {client-surface-lever-vN}   # set to "none" when nothing is live
live_started: {YYYY-MM-DD}
decision_date: {YYYY-MM-DD}          # when the live test is due to be read
backlog_count: 0                     # number of queued (not-yet-run) hypotheses
last_concluded: {YYYY-MM-DD}         # date the most recent test concluded ("" if never)
last_reviewed: {YYYY-MM-DD}
---

# {Client} — LP Experiment Backlog

> **The living testing roadmap for this client.** One file per client, lives at
> `~/agency-workspace/outputs/{slug}/experiments/backlog.md`.
> This is the source of truth for "what's live, what's next, what we've learned."
> The **agency-wide never-go-dark sweep** reads the frontmatter above; humans read the body below. Update both together.

**Client:** {slug}
**LP(s) under test:** {url(s)}
**PostHog flag(s):** {flag-key} (id {flag-id})
**Primary metric:** {conversion event — e.g. lead_form_submitted} | **Guardrail metric:** {e.g. lp_cta_clicked CTR}
**Last reviewed:** {YYYY-MM-DD}

---

## 🔴 LIVE NOW

> There should ALWAYS be a row here (or a documented reason there isn't). An empty Live section that lasts >14 days is a never-go-dark violation — promote the top backlog item.

| Field | Value |
|---|---|
| **Test ID** | `{taxonomy: client-surface-lever-vN}` e.g. `usturf-hero-mobileflip-v28` |
| **Hypothesis** | If we {change}, then {metric} will {direction} because {reason}. |
| **Flag / variant** | `{flag-key}` → `variant_b` = {what variant_b does} |
| **State** | `live` |
| **Started** | {YYYY-MM-DD HH:MM UTC} |
| **Decision date** | {start + min duration; see stopping rules} |
| **Min sample (per arm)** | {N exposures} |
| **Progress** | {exposures so far} / {N} per arm — {% to decision} |
| **Reading** | {control conv rate vs variant conv rate, confidence %} |
| **Kill criteria** | {e.g. guardrail metric drops >X% at >90% confidence → kill early} |

---

## 🟢 BACKLOG (ICE-ranked queue)

> When the live test concludes, the **highest-ICE** unblocked item here auto-promotes to Live. Re-score after every conclusion.
> **Before adding any idea, check the winning-pattern bank** (`MEMORY.md` → "LP experiment results") — don't re-test a lever that already lost on a comparable client, and fast-track a lever that already won.

| Rank | Test ID | Hypothesis (If… then… because…) | Lever | I | C | E | **ICE** | Notes / blockers |
|---|---|---|---|---|---|---|---|---|
| 1 | `{id}` | If {change} then {metric}↑ because {reason} | {hero/form/proof/cta/offer/risk} | 8 | 7 | 9 | **8.0** | |
| 2 | `{id}` | … | | | | | | |
| 3 | `{id}` | … | | | | | | |

**ICE scoring (1–10 each, average = ICE):**
- **Impact** — how big is the expected lift if it wins? (anchor on traffic volume × plausible % lift)
- **Confidence** — how sure are we it'll win? (prior wins on this lever, Clarity/recording evidence, audit signal all raise it)
- **Ease** — how cheap to build + ship? (CSS-only flip = 9; new hero + copy + creative = 3)

---

## ✅ ARCHIVE — concluded tests (results log)

> Every concluded test gets a row + a link to its `learning_lp-test-{lever}.md` memory file. This is the compounding asset.

| Concluded | Test ID | Result | Lift | Confidence | Shipped? | Learning memory |
|---|---|---|---|---|---|---|
| {YYYY-MM-DD} | `{id}` | WON / LOST / INCONCLUSIVE | {+X% / -X%} | {%} | yes/no | `learning_lp-test-{lever}.md` |

---

## Lifecycle (state machine)

```
queued ──promote──▶ live ──reach decision date / kill criteria──▶ reading
   ▲                                                                  │
   │                                                          decide  │
   └──── refill backlog ◀── archived ◀── shipped/reverted ◀──────────┘
```

- **queued** — in the backlog, ICE-scored, not yet running
- **live** — flag active, splitting traffic, accruing sample
- **reading** — hit decision date OR kill criteria; analyzing (bot-filtered)
- **shipped** — winner rolled to 100%; or **reverted** — variant killed, control stays
- **archived** — result written to a `learning_lp-test-{lever}.md` memory file; backlog refilled and re-ranked → top item promotes to live

**Rule: a client is never in a state where Live is empty AND backlog is empty.** If backlog runs dry, that's the trigger to do a fresh CRO audit and generate new hypotheses.

## Stopping rules (don't peek your way to a false winner)

- **Minimum sample per arm** before reading: enough for the expected MDE. Rough floor: ~100 conversions per arm for small lifts; fewer arms/bigger expected lift can read sooner.
- **Minimum duration:** ≥1 full business cycle (7 days) to cover weekday/weekend mix — even if sample lands early.
- **Decision date** is set at launch. Don't call a winner before it unless a **kill criterion** fires (guardrail metric collapses at high confidence — like US Turf's CTA-CTR gap).
- **Bot filter first.** Always strip bot traffic before reading (Meta paid LPs ~29% bot/prefetch). See `learning_lp-posthog-ab-test-framework.md`.
- **Inconclusive is a valid result.** If it doesn't clear confidence by the decision date, ship control, archive as inconclusive, move on. Don't let a flat test block the queue.

## Never-go-dark monitor (set up once per client)

A scheduled task that reads this file weekly and flags violations:
- Live section empty for >14 days → **promote top backlog item**
- Live test past its decision date with no decision logged → **read it and decide**
- Backlog has <3 queued items → **run a CRO audit to refill**

See the agent's "Set up the never-go-dark monitor" step for the `CronCreate` / scheduled-task wiring.
