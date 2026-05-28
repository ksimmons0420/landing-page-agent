---
description: First-time setup for the Landing Page Agent. Runs the onboarding questionnaire, collects platform tokens (PostHog, Microsoft Clarity, Google APIs, etc.), writes ~/.landing-page-agent/.env, and scaffolds the workspace. Run this once per workstation.
---

# Landing Page Agent — Setup

You are running first-time setup for the standalone Landing Page Agent. The user has just installed the plugin. Your job: walk them through a short questionnaire, collect their platform tokens, write the env file, scaffold the workspace, and run a verification pass.

**Always use `AskUserQuestion`** for every decision point. Never make the user type when they could click.

---

## Step 0 — Detect existing setup

Run via Bash:

```bash
ls ~/.landing-page-agent/.env 2>/dev/null
ls ~/landing-page-agent/projects 2>/dev/null
```

- **If `.env` exists** → tell the user setup is already done, summarize the env (variable names only, not values), and ask if they want to re-run (overwrites) or just verify (no changes). Default to verify.
- **If neither exists** → proceed to Step 1.

## Step 1 — Welcome

Say:

> Welcome to the Landing Page Agent. I'll walk you through setup in about 5 minutes — six quick questions, then I'll collect tokens for the platforms you said yes to, write everything to `~/.landing-page-agent/.env`, and scaffold your workspace. Then we verify.

## Step 2 — Stack questionnaire

Ask each with `AskUserQuestion`. Record the answers. **Q1 (goal) drives downstream questions** — some questions only apply for certain goals.

**Q1 — What's the primary conversion goal? (drives everything downstream)**
```
Header: "Goal"
Options:
  - Lead form fill           — Service businesses, B2B demos, local lead gen
  - Ecommerce purchase       — Online store, checkout completion
  - Account signup           — SaaS, app, membership
  - Calendar booking         — Consultations, demos, sales calls
MultiSelect: false
```

Then a follow-up if none of those fit:

```
Question: "If your goal wasn't in that list, which of these?"
Header: "Other goal"
Options:
  - Content unlock / download   — Whitepaper, demo, gated asset
  - Newsletter / waitlist signup
  - App install                 — Mobile store CTA
  - Other (you'll name it)      — I'll ask for your event name
MultiSelect: false
```

Capture the **conversion event name** the user wants the agent to fire on success. Default suggestions (the user can override):
- Lead form → `lead_form_submitted`
- Ecommerce → `order_completed`
- Signup → `signup_completed`
- Booking → `booking_completed`
- Content → `content_unlocked`
- Newsletter → `newsletter_signed_up`
- App install → `app_install_clicked`
- Other → ask the user

**Q2 — Where do your landing pages live? (the builder)**
```
Header: "Builder"
Options:
  - Shopify
  - WordPress
  - Webflow
  - Squarespace
MultiSelect: false
```

If none of those:

```
Question: "Which builder are you using?"
Header: "Other builder"
Options:
  - Wix
  - Framer
  - HubSpot CMS
  - Custom / static HTML (or other)
MultiSelect: false
```

The agent supports any builder where a `<script>` tag can be injected into `<head>`. If the user picks "Custom / static HTML (or other)" and their stack isn't listed, ask: "Which platform? I'll adapt the vanilla template to it." Free-text the answer and save to env as `LP_DEFAULT_STACK`.

**Q3 — Which analytics platform?**
```
Header: "Analytics"
Options:
  - PostHog (Recommended)  — Unlocks A/B engine, funnel events, replays
  - GA4 only               — Forward events via GTM, no PostHog
  - Both                   — PostHog for experiments, GA4 for reporting
  - Other / decide later   — Skip for now
MultiSelect: false
```

**Q4 — Heatmaps / session replay?**
```
Header: "Heatmaps"
Options:
  - Microsoft Clarity (Recommended) — Free, fast scroll-depth + replay
  - PostHog Replay                  — Use PostHog's built-in replay
  - Hotjar                          — Existing Hotjar account
  - None                            — Skip
MultiSelect: false
```

**Q5 — Form tool? (only ask if Q1 goal involves a form)**

Skip this question entirely if the goal is ecommerce-purchase, app-install, or any other non-form goal.

If the goal is lead form / signup / booking / content unlock / newsletter / waitlist:

```
Header: "Form tool"
Options:
  - JotForm
  - Typeform / Tally / Fillout (hosted)
  - Native HTML form
  - CRM-native (HubSpot / ActiveCampaign / Mailchimp / etc.)
MultiSelect: false
```

If none of the above fit, ask follow-up:

```
Question: "Which form tool?"
Header: "Other form"
Options:
  - WordPress plugin (Gravity Forms, WPForms, etc.)
  - Shopify / Webflow / Squarespace native form block
  - Something else (you'll name it)
  - Not using a form yet — varies per project
MultiSelect: false
```

Record the answer as `LP_FORM_TOOL` (lowercased keyword). Drives which engagement-event wiring the agent loads per project.

**Q6 — Communication channel?**
```
Header: "Comms"
Options:
  - CLI only (Recommended) — Run sweeps and reports inside Claude Code
  - Slack                  — Weekly sweep posts to Slack
  - Email                  — Weekly digest by email
  - Multiple               — Configure more than one
MultiSelect: false
```

**Q7 — Compliance constraints?**
```
Header: "Compliance"
Options:
  - Heavily regulated  — Industry rules (healthcare, finance, legal, energy rebates, etc.)
  - Some constraints   — Brand voice / banned phrases / claims rules
  - None / standard    — No special constraints beyond best practices
MultiSelect: false
```

If they pick "Heavily regulated" or "Some constraints", follow up with a free-text ask: "Briefly — what are the constraints? (Industry, banned phrases, required disclosures.) I'll save these to memory so all copy I write respects them."

## Step 3 — Platform credentials

Based on Q2 / Q3 / Q5 answers, collect tokens. Use `AskUserQuestion` with an "Other (paste it)" affordance for each, then write to env.

### If PostHog was selected (Q2)

Walk through both keys:

> I need two things from PostHog: your **project token** (public, ships in the LP) and a **personal API key** (secret, stays local).
>
> 1. **Project token** — open https://app.posthog.com/settings/project, scroll to "Project ID & API Key", copy the value that starts with `phc_`. Paste it here.
> 2. **Personal API key** — open https://app.posthog.com/settings/user-api-keys, click "Create personal API key", give it a name like "landing-page-agent", grant scope `project:read` and `feature_flag:write`. Paste it here.
> 3. **Project ID** — open https://app.posthog.com/settings/project and copy the numeric project ID at the top.

Ask each with `AskUserQuestion` (single option "Paste it" + the natural "Other" affordance for the value). Record as:
- `POSTHOG_PROJECT_TOKEN=`
- `POSTHOG_PERSONAL_API_KEY=`
- `POSTHOG_PROJECT_ID=`

### If Microsoft Clarity was selected (Q3)

> For Clarity I need your **project ID** and optionally an **API token** (for scroll-depth pulls).
>
> 1. **Project ID** — open https://clarity.microsoft.com/, click your project, the ID is in the URL.
> 2. **API token (optional)** — Settings → Data Export Settings → API Token. Skip if you don't want automated scroll-depth pulls.

Record as `CLARITY_PROJECT_ID=` and (if provided) `CLARITY_API_TOKEN=`.

### Form-tool-specific keys (only if Q5 was asked and answered)

The questionnaire selected a form tool. Some tools need an API key for `analyze_submissions`-style introspection; many don't. Collect only what's needed:

- **JotForm** — API key at https://www.jotform.com/myaccount/api (read+write). Record as `JOTFORM_API_KEY=`.
- **Typeform** — Personal token at https://admin.typeform.com/account#/section/tokens (read scope). Record as `TYPEFORM_PERSONAL_TOKEN=`.
- **Tally** — API key at https://tally.so/settings/api (read scope). Record as `TALLY_API_KEY=`.
- **Fillout** — API key at https://www.fillout.com/dashboard (Settings → Developers). Record as `FILLOUT_API_KEY=`.
- **HubSpot** — Private app token at https://app.hubspot.com/private-apps. Record as `HUBSPOT_PRIVATE_APP_TOKEN=`.
- **Native HTML / WordPress plugin / platform-native form block / "something else"** — no API key needed; skip.

Only ask for the key matching the tool the user picked. Don't prompt for all of them.

### If Slack was selected (Q5)

> Slack webhook URL for the channel where the weekly sweep should post:
> Get one at https://api.slack.com/messaging/webhooks. Paste here.

Record as `SLACK_WEBHOOK_URL=`.

### LP host (Q1) — note in env

No token collection at this stage (handled per-project), but record the default stack for new projects:

- `LP_DEFAULT_STACK=shopify` (or `webflow`, `wordpress`, `custom`)

## Step 4 — Write the env file

Build the env content from the answers above. Write it via Bash:

```bash
mkdir -p ~/.landing-page-agent
cat > ~/.landing-page-agent/.env <<'ENV'
# Landing Page Agent — generated by /landing-page-agent:setup on {today}
LP_DEFAULT_GOAL={goal}                # lead-form | purchase | signup | booking | content | newsletter | app-install | other
LP_DEFAULT_CONVERSION_EVENT={event}   # e.g. lead_form_submitted, order_completed, booking_completed
LP_DEFAULT_STACK={stack}              # shopify | wordpress | webflow | squarespace | wix | framer | hubspot-cms | custom | <other free-text>
LP_FORM_TOOL={form_tool_or_blank}     # only set if the goal involves a form
LP_COMMS={comms}

# PostHog
POSTHOG_PROJECT_TOKEN={token}
POSTHOG_PERSONAL_API_KEY={key}
POSTHOG_PROJECT_ID={id}

# Microsoft Clarity (optional)
CLARITY_PROJECT_ID={id}
CLARITY_API_TOKEN={token}

# Form-tool API (optional — only one of these, matching LP_FORM_TOOL)
JOTFORM_API_KEY={key}
TYPEFORM_PERSONAL_TOKEN={token}
TALLY_API_KEY={key}
FILLOUT_API_KEY={key}
HUBSPOT_PRIVATE_APP_TOKEN={token}

# Slack (optional)
SLACK_WEBHOOK_URL={url}
ENV
chmod 600 ~/.landing-page-agent/.env
```

**Only include lines for platforms / fields the user actually provided.** Don't write blank env vars — keep the file tight. For example, if the goal is ecommerce-purchase, omit `LP_FORM_TOOL` and all form-tool API keys entirely.

## Step 5 — Scaffold the workspace

```bash
mkdir -p ~/landing-page-agent/projects ~/landing-page-agent/memory ~/landing-page-agent/scripts
```

Copy the sweep script and templates from the plugin's `skills/templates/` directory into `~/landing-page-agent/scripts/` and `~/landing-page-agent/templates/`. Use `cp` from the plugin path (the user's Claude Code config exposes it via the `CLAUDE_PLUGIN_ROOT` env var or you can use `~/.claude/plugins/cache/scalehouse/landing-page-agent/`).

## Step 6 — Compliance memory (if they had constraints in Q6)

Write the constraints to `~/landing-page-agent/memory/compliance.md`:

```markdown
# Compliance constraints

Loaded before any LP copy is written.

{user's free-text answer}
```

## Step 7 — Offer MCP install

Ask:

```
Question: "Want me to walk through installing the recommended MCPs now?"
Header: "MCPs"
Options:
  - Yes, all of them                  — PostHog + Firecrawl + Playwright
  - Yes, but only PostHog              — Skip the others for now
  - No, I'll set them up later        — Skip — links are in the docs
MultiSelect: false
```

For each MCP they pick, give them the install command + a link to the official setup docs:

- **PostHog MCP** — https://posthog.com/docs/model-context-protocol
- **Firecrawl MCP** — https://docs.firecrawl.dev/mcp
- **Playwright MCP** — https://github.com/microsoft/playwright-mcp

Don't try to edit `~/.config/claude-code/mcp.json` directly — point them at the docs and let Claude Code's own MCP install flow handle it. Tell them to restart Claude Code after.

## Step 8 — Verify

Run a simple verification:

1. `ls -la ~/.landing-page-agent/.env` — confirm exists, chmod 600.
2. `ls -la ~/landing-page-agent/` — confirm workspace dirs exist.
3. If PostHog was provided: a quick `curl` to `https://us.i.posthog.com/decide/?v=3&token={POSTHOG_PROJECT_TOKEN}` to confirm the token is valid (200 vs 401).
4. Echo a summary back to the user.

## Step 9 — What's next

Tell the user:

> Setup is done. Next move: `/landing-page-agent:new-project` to spin up your first project. That'll create `~/landing-page-agent/projects/{slug}/` with a profile, ICE-ranked backlog, and a stack-specific deploy snippet.
>
> Weekly: `/landing-page-agent:sweep` checks every project for DARK / OVERDUE / BACKLOG-LOW status.
>
> The setup state file lives at `~/.landing-page-agent/setup-state.json` if you want to inspect it.

Write the state file at the end:

```bash
cat > ~/.landing-page-agent/setup-state.json <<JSON
{
  "version": "0.1.0",
  "created_at": "{ISO timestamp}",
  "lp_default_stack": "{stack}",
  "platforms_connected": [{list}],
  "mcps_installed": [{list}],
  "comms": "{comms}",
  "has_compliance_memory": {true/false}
}
JSON
```

## Failure modes

- **User cancels mid-setup** — Save partial state to `setup-state.json` with `"status": "incomplete"` so they can resume.
- **PostHog token invalid** — Tell them, point at the settings URL, ask them to re-paste.
- **No write permission to `~/`** — Should never happen, but if it does, fall back to `$XDG_DATA_HOME` if set, else error out cleanly.

## Constraints

- Never write tokens to stdout or to a file outside `~/.landing-page-agent/`.
- Never commit the env file to git.
- Never proceed past Step 2 without an explicit answer to each question (no defaults for the stack/analytics questions).
