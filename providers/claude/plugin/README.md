# Papermark for Claude

Papermark is the virtual data room and secure document-sharing platform for your
agents. This plugin makes Claude fluent in Papermark: build and organize data
rooms for deals and due diligence, share documents behind secure links
(password, email-gating, expiry, watermarks, screenshot protection), and read
view analytics down to per-page read time.

## What's included

- **`papermark-overview` skill** — what Papermark is, how its data is
  structured (documents, versions, folders, share links, data rooms, viewers,
  views, analytics), and the rules for sharing safely. Claude reads it before
  creating links or data rooms and before deleting anything.
- **`papermark-cli` skill** — how to drive Papermark from the command line with
  the published [`papermark` CLI](https://www.npmjs.com/package/papermark),
  including scripts and CI. Only used when a shell is available.
- **Papermark MCP server** — the plugin's `.mcp.json` connects Claude to the
  official remote MCP server so Papermark tools are available natively.

The plugin has no hooks, agents, or bundled scripts. It ships only the two
skills and the MCP server declaration.

## What the plugin connects to and runs

- **MCP server:** `https://mcp.papermark.com/mcp`, a streamable HTTP server run
  by Papermark. It authenticates over OAuth in your browser; the plugin stores
  no credentials and sends data only to this endpoint. Tool calls act on the
  Papermark workspace you sign in to.
- **CLI (optional):** the `papermark-cli` skill tells Claude to run the
  `papermark` command if it is installed (Node.js 24 or newer). The CLI talks
  to the Papermark API at `https://api.papermark.com`. You sign in with
  `papermark login`, an OAuth device flow in your browser, and the CLI keeps
  the session in its own configuration. The plugin never reads, stores, or
  forwards credentials itself.

Nothing else is fetched or sent anywhere.

## Install

From the Claude plugin directory, add **Papermark**. Or, in Claude Code:

```bash
/plugin marketplace add papermark/skills
/plugin install papermark@papermark-skills
```

To use the CLI skill as well:

```bash
npm install -g papermark
papermark login
papermark doctor
```

## Example prompts

- "Create a data room for the Acme Series A and add the pitch deck."
- "Share this deck with a password-protected link that expires on Friday."
- "Who viewed my pitch deck, and how long did they spend on page 3?"

## Links

- Website — https://www.papermark.com
- Docs — https://www.papermark.com/docs
- Source — https://github.com/papermark/skills

## License

MIT. See [LICENSE.md](./LICENSE.md).
