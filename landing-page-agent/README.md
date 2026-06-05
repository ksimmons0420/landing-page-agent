# landing-page-agent

Standalone landing-page CRO agent plugin for Claude Code.

See the top-level `README.md` of this repository for install and usage. Full diff per version in `../CHANGELOG.md`.

## Plugin contents (v0.2.0)

```
landing-page-agent/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── landing-page-dev/agent.md             # the agent persona — Karpathy-disciplined,
│                                              #   9 CRO operating principles,
│                                              #   includes LP-review / multi-page-funnel
│                                              #   / brand-palette-audit workflows
├── commands/
│   ├── setup.md                              # /landing-page-agent:setup
│   ├── new-project.md                        # /landing-page-agent:new-project
│   └── sweep.md                              # /landing-page-agent:sweep
└── skills/
    ├── SKILL.md                              # skill index + 6-event canonical funnel + deploy gotchas
    └── templates/
        ├── vanilla-script-tag.html           # universal <script> block (any builder)
        ├── theme-liquid-universal-block.liquid  # Shopify-specific variant
        ├── experiment-backlog-template.md    # per-project ICE-ranked backlog
        ├── lp-experiment-sweep.py            # never-go-dark sweep script
        ├── lp-review-checklist.md            # structured LP critique framework (NEW v0.2.0)
        ├── cro-data-sources-playbook.md      # 5-source diagnostic ladder (NEW v0.2.0)
        └── listicle-lp-skeleton.md           # "Best X for Y" LP template (NEW v0.2.0)
```
