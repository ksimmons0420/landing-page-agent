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

## Step 2 — Stack questionnaire (six questions)

Ask each with `AskUserQuestion`. Record the answers.

**Q1 — Where do your landing pages live?**
```
Header: "LP host"
Options:
  - Shopify     — Shopify store with theme access
  - Webflow     — Webflow project with custom code permission
  - WordPress   — WordPress site with theme/snippet access
  - Custom HTML — Static site or hand-rolled HTML where you can edit <head>
MultiSelect: false
```

**Q2 — Which analytics platform?**
```
Header: "Analytics"
Options:
  - PostHog (Recommended) — Unlocks A/B engine, funnel events, replays
  - GA4 only              — Forward events via GTM, no PostHog
  - Both                  — Run both; PostHog for experiments, GA4 for reporting
  - Other / decide later  — Skip for now
MultiSelect: false
```

**Q3 — Heatmaps / session replay?**
```
Header: "Heatmaps"
Options:
  - Microsoft Clarity (Recommended) — Free, fast scroll-depth + replay
  - PostHog Replay                  — Use PostHog's built-in replay
  - Hotjar                          — Existing Hotjar account
  - None                            — Skip
MultiSelect: false
```

**Q4 — Form tool?**
```
Header: "Forms"
Options:
  - JotForm        — Embedded JotForm (iframe or JS)
  - Native HTML    — Build the form inline on the LP
  - Typeform       — Embedded Typeform
  - Other          — Will specify per project
MultiSelect: false
```

**Q5 — Communication channel?**
```
Header: "Comms"
Options:
  - CLI only (Recommended)   — Run sweeps and reports inside Claude Code
  - Slack                    — Weekly sweep posts to Slack
  - Email                    — Weekly digest by email
  - Multiple                 — Configure more than one
MultiSelect: false
```

**Q6 — Compliance constraints?**
```
Header: "Compliance"
Options:
  - Heavily regulated     — Specific industry rules (healthcare, finance, legal, energy rebates, etc.)
  - Some constraints      — General brand voice / banned phrases / claims rules
  - None / standard       — No special constraints beyond best practices
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

### If JotForm was selected (Q4)

> JotForm API key (optional — needed for `analyze_submissions`):
> Open https://www.jotform.com/myaccount/api → Create new key → read+write. Paste here.

Record as `JOTFORM_API_KEY=`.

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
LP_DEFAULT_STACK={stack}
LP_COMMS={comms}

# PostHog
POSTHOG_PROJECT_TOKEN={token}
POSTHOG_PERSONAL_API_KEY={key}
POSTHOG_PROJECT_ID={id}

# Microsoft Clarity (optional)
CLARITY_PROJECT_ID={id}
CLARITY_API_TOKEN={token}

# JotForm (optional)
JOTFORM_API_KEY={key}

# Slack (optional)
SLACK_WEBHOOK_URL={url}
ENV
chmod 600 ~/.landing-page-agent/.env
```

Only include lines for platforms the user actually provided. Don't write blank env vars — keep the file tight.

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
