# landing-page-agent

Standalone landing-page CRO agent plugin for Claude Code.

See the top-level `README.md` of this repository for install and usage.

## Plugin contents

```
landing-page-agent/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── landing-page-dev/agent.md         # the agent persona
├── commands/
│   ├── setup.md                          # /landing-page-agent:setup
│   ├── new-project.md                    # /landing-page-agent:new-project
│   └── sweep.md                          # /landing-page-agent:sweep
└── skills/
    ├── SKILL.md                          # skill index
    └── templates/
        ├── lp-experiment-sweep.py        # the sweep script
        ├── experiment-backlog-template.md
        └── theme-liquid-universal-block.liquid
```
