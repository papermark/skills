# Papermark

Papermark is the virtual data room and secure document-sharing platform for your
agents. Build and organize data rooms for deals and due diligence, share documents
behind secure links (password, email-gating, expiry, watermarks, screenshot
protection), and read view analytics down to per-page read time. It's the
open-source alternative to DocSend.

This repo is the canonical, official home for the plugins, skills, and other
artifacts we ship to make Papermark as fluent to agents as it already is to the
teams who use it. Today that ships as an installable plugin for
[Claude Code](https://code.claude.com) and [Codex](https://developers.openai.com/codex),
and as a standalone collection of skills installable via the
[`skills` CLI](https://github.com/vercel-labs/skills) for any agent that consumes
[agentskills.io](https://agentskills.io)–format skills.

## What's inside

The bundled skills live under [`plugins/papermark/skills/`](./plugins/papermark/skills/):

- **`papermark-overview`** — what Papermark is, the data model (data rooms,
  documents, links, viewers, analytics), and the rules for sharing safely.
- **`papermark-cli`** — driving Papermark from the command line with the
  published [`papermark` CLI](https://www.npmjs.com/package/papermark), including
  scripts and CI.

The official Papermark MCP server (`mcp.papermark.com/mcp`) is auto-wired via
`.mcp.json`, so the plugin gives the agent native Papermark tools out of the box.

## Install

### Claude Code

```bash
/plugin marketplace add papermark/skills
/plugin install papermark@papermark-skills
```

For local testing from a clone:

```bash
/plugin marketplace add /path/to/this/repo
/plugin install papermark@papermark-skills
```

### Codex

```bash
codex plugin marketplace add papermark/skills
```

Then enable the plugin via the Codex TUI's plugins menu, or by adding to
`~/.codex/config.toml`:

```toml
[plugins."papermark@papermark-skills"]
enabled = true
```

If you'd rather wire the MCP server manually instead of via the plugin, add the
following to `~/.codex/config.toml` (the plugin handles this automatically when
enabled — this is just an escape hatch):

```toml
[[mcp_servers]]
name = "papermark"
type = "http"
url = "https://mcp.papermark.com/mcp"
```

### Standalone skills (any agent)

For Cursor, OpenCode, Gemini CLI, or any other agent that consumes
[Agent Skills](https://agentskills.io):

```bash
# All skills
npx skills add papermark/skills

# A specific skill
npx skills add papermark/skills --skill papermark-cli
```

### Using the CLI directly

The `papermark-cli` skill shells out to the published CLI (Node.js ≥ 24):

```bash
npm install -g papermark
papermark login        # OAuth device flow
papermark doctor       # confirm auth + connectivity
```

## Layout

```
.
├── .claude-plugin/marketplace.json     # Claude marketplace catalog
├── .agents/plugins/marketplace.json    # Codex marketplace catalog
├── .mcp.json                           # top-level MCP wiring
└── plugins/papermark/                  # the v1 plugin
    ├── .claude-plugin/plugin.json
    ├── .codex-plugin/plugin.json
    ├── .mcp.json
    ├── assets/
    └── skills/
        ├── papermark-overview/
        └── papermark-cli/
```

## Links

- Website — https://www.papermark.com
- Docs — https://www.papermark.com/docs
- CLI on npm — https://www.npmjs.com/package/papermark
- MCP server — `https://mcp.papermark.com/mcp`

## License

[MIT](./LICENSE.md).
