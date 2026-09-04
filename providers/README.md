# Provider Plugins

This directory contains the Papermark plugin, packaged once per agent harness.

## Layout

Each provider gets its own directory, and each plugin lives in its own
subdirectory under `providers/<provider>/` so its manifest, skills, and assets
stay isolated as more plugins are added.

| Provider | Plugin | Manifest |
| --- | --- | --- |
| [Claude Code](./claude/plugin) | `providers/claude/plugin` | `.claude-plugin/plugin.json` |
| [Codex](./codex/plugin) | `providers/codex/plugin` | `.codex-plugin/plugin.json` |
| [Cursor](./cursor/plugin) | `providers/cursor/plugin` | `.cursor-plugin/plugin.json` |
| [Grok Build](./grok/plugin) | `providers/grok/plugin` | `.grok-plugin/plugin.json` |

The catalog each harness reads lives at the repo root, one file per provider:
`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` (Codex),
`.cursor-plugin/marketplace.json`, and `.grok-plugin/marketplace.json`.

Gemini CLI has no plugin directory here — it installs the repo itself as an
extension, driven by [`gemini-extension.json`](../gemini-extension.json) at the
repo root.

Every provider wires up the same remote MCP server
(`https://mcp.papermark.com/mcp`), just in each harness's own config shape —
`.mcp.json` for Claude and Grok, `mcp.json` for Cursor, and inline under
`mcpServers` in the manifest for Codex.

## Skills

**Do not edit skill files in provider directories manually.**

Skills under `providers/*/plugin/skills/` are copies. The canonical versions
live in [`skills/`](../skills) at the repo root, and are fanned out by
[`scripts/sync-skills.mjs`](../scripts/sync-skills.mjs). Any manual change to a
provider copy gets overwritten on the next sync.

To change a skill: edit it under `skills/`, then run

```bash
node scripts/sync-skills.mjs
```

and commit both the source and the synced copies. CI runs the same script with
`--check` and fails if the copies have drifted.

## Adding a provider

1. Create `providers/<provider>/plugin/` with that harness's manifest.
2. Point the manifest's MCP config at `https://mcp.papermark.com/mcp`.
3. Add the provider to `TARGETS` in `scripts/sync-skills.mjs` and run it.
4. Add the root marketplace catalog the harness reads, pointing at the new
   plugin directory.
5. Document the install command in the top-level [README](../README.md).
