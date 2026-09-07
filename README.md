# Papermark

Papermark is the virtual data room and secure document-sharing platform for your
agents. Build and organize data rooms for deals and due diligence, share documents
behind secure links (password, email-gating, expiry, watermarks, screenshot
protection), and read view analytics down to per-page read time.

This repo is the canonical, official home for the plugins, skills, and other
artifacts we ship to make Papermark as fluent to agents as it already is to the
teams who use it. It ships as an installable plugin for
[Claude Code](https://code.claude.com), [Codex](https://developers.openai.com/codex),
[Cursor](https://cursor.com), and [Grok Build](https://x.ai), as a
[Gemini CLI](https://geminicli.com) extension, and as a standalone collection of
skills installable via the [`skills` CLI](https://github.com/vercel-labs/skills)
for any agent that consumes [agentskills.io](https://agentskills.io)–format skills.

## What's inside

The bundled skills live under [`skills/`](./skills):

- **`papermark-overview`** — what Papermark is, the data model (data rooms,
  documents, links, viewers, analytics), and the rules for sharing safely.
- **`papermark-cli`** — driving Papermark from the command line with the
  published [`papermark` CLI](https://www.npmjs.com/package/papermark), including
  scripts and CI.

The official Papermark MCP server (`https://mcp.papermark.com/mcp`) is wired up by
every plugin, so the agent gets native Papermark tools out of the box.

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

### Cursor

Add this repo as a marketplace from Cursor's plugin settings
(`https://github.com/papermark/skills`), then install the `papermark` plugin.
Cursor reads [`.cursor-plugin/marketplace.json`](./.cursor-plugin/marketplace.json)
from the repo root.

### Grok Build

```bash
grok plugin install papermark/skills#providers/grok/plugin --trust
```

You can also register the repo as a marketplace source under
`[[marketplace.sources]]` in `~/.grok/config.toml` and install it from
`/marketplace` inside a Grok Build session.

### Gemini CLI

```bash
gemini extensions install https://github.com/papermark/skills
```

The extension wires up the Papermark MCP server over OAuth. Gemini CLI doesn't
consume the bundled skills — add those with the `skills` CLI below.

### Standalone skills (any agent)

For OpenCode, Zed, Continue, Windsurf, or any other agent that consumes
[Agent Skills](https://agentskills.io):

```bash
# All skills
npx skills add papermark/skills

# A specific skill
npx skills add papermark/skills --skill papermark-cli
```

### Manual MCP wiring

If you'd rather wire the MCP server up yourself instead of installing a plugin,
point any MCP client at:

```
https://mcp.papermark.com/mcp
```

It's a streamable HTTP server and authenticates over OAuth, so most clients only
need the URL.

## Using the CLI directly

The `papermark-cli` skill shells out to the published CLI (Node.js ≥ 24):

```bash
npm install -g papermark
papermark login        # OAuth device flow
papermark doctor       # confirm auth + connectivity
```

## Layout

```
.
├── .claude-plugin/marketplace.json      # Claude Code catalog
├── .agents/plugins/marketplace.json     # Codex catalog
├── .cursor-plugin/marketplace.json      # Cursor catalog
├── .grok-plugin/marketplace.json        # Grok Build catalog
├── gemini-extension.json                # Gemini CLI extension
├── .mcp.json                            # MCP wiring for this repo itself
├── skills/                              # canonical skills — edit these
├── assets/                              # canonical brand assets
├── scripts/sync-skills.mjs              # fans skills/ + assets/ into providers
└── providers/                           # one plugin per agent harness
    ├── README.md
    ├── claude/plugin/
    ├── codex/plugin/
    ├── cursor/plugin/
    └── grok/plugin/
```

## Contributing

Skills are authored once in [`skills/`](./skills) and copied into each provider
plugin, because every harness installs a plugin by copying its own directory.
Never edit the copies under `providers/*/plugin/skills/` — edit the source and
re-run the sync:

```bash
node scripts/sync-skills.mjs
```

CI runs `node scripts/sync-skills.mjs --check` and fails on drift. See
[`providers/README.md`](./providers/README.md) for how to add a new harness.

## Links

- Website — https://www.papermark.com
- Docs — https://www.papermark.com/docs
- CLI on npm — https://www.npmjs.com/package/papermark
- MCP server — `https://mcp.papermark.com/mcp`

## License

[MIT](./LICENSE.md).
