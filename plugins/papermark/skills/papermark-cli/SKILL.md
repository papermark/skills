---
name: papermark-cli
description: >
  Drive Papermark from the command line with the published `papermark` CLI:
  upload documents, create secure share links (password, email-gating, expiry,
  watermarks, screenshot protection), build and organize data rooms for deals and
  due diligence, and read view analytics — including in scripts and CI. Reach for
  this when the user says things like "share this deck", "create a data room for
  Acme", "who viewed my pitch", "send a password-protected link", or "how much time
  did they spend on page 3", and a shell is available. For concepts and guardrails,
  see the papermark-overview skill.
license: MIT
allowed-tools: Bash(papermark:*)
metadata:
    version: '1.0.0'
    author: papermark
---

# Papermark CLI Skill

Drive [Papermark](https://www.papermark.com) — document sharing, secure links, and
virtual data rooms — through the `papermark` command-line tool.

| Property | Value |
|----------|-------|
| **name** | papermark |
| **description** | Share documents, create secure links and data rooms, and read analytics from the CLI |
| **allowed-tools** | `Bash(papermark:*)` |
| **npm** | https://www.npmjs.com/package/papermark |
| **repo** | https://github.com/papermark/papermark |
| **website** | https://www.papermark.com |
| **docs** | https://www.papermark.com/docs |

## Install the CLI if it doesn't exist

```bash
npm install -g papermark
# requires Node.js >= 24
```

Verify it's available:

```bash
papermark --version
```

## ⚠️ Two Hard Rules (Read First)

**Rule 1 — Authenticate before anything.** Every command that touches the API
fails without a valid token. Run `papermark doctor` first and only proceed once
auth is confirmed (see *Setup* below).

**Rule 2 — Never act on documents, links, or data rooms the user didn't name.**
Don't upload arbitrary files, create share links for documents the user didn't
point at, or delete anything without explicit confirmation. Don't invent
passwords, expiry dates, watermark text, or recipient emails — ask the user or
generate a value and tell them the exact value you used.

## Setup

Before running any other command, confirm auth and connectivity:

```bash
papermark doctor --json
```

This checks `auth.present`, `config.api_url`, `api.reachable`, and `api.auth`. If
any check reports `"ok": false`, the token is missing or invalid. To fix:

- **Interactive (recommended):** `papermark login` runs the OAuth device flow —
  it prints a verification URL + user code and opens the browser. Use
  `papermark login --no-browser` to only print the URL.
- **Direct token:** `papermark login --token pm_live_…` to paste an existing
  API token.
- **Non-interactive / CI:** set `PAPERMARK_TOKEN`, or pipe a token via
  `papermark auth set --stdin`, or point `PAPERMARK_CREDENTIALS_FILE` at a JSON
  file `{ "token": "pm_live_…", "apiUrl": "…" }`.

Token resolution order: `PAPERMARK_TOKEN` → `PAPERMARK_CREDENTIALS_FILE` → stored
config. Check the active identity any time with `papermark whoami`.

**Do NOT proceed with any other command until `papermark doctor` passes.**

Useful environment variables:

| Variable | Purpose |
|----------|---------|
| `PAPERMARK_TOKEN` | API token (`pm_live_…` / `pm_test_…` or OAuth bearer); overrides config |
| `PAPERMARK_API_URL` | API endpoint (default `https://api.papermark.com`) |
| `PAPERMARK_CREDENTIALS_FILE` | Path to a JSON credentials file |
| `PAPERMARK_DEBUG=1` | Verbose request tracing to stderr |
| `NO_COLOR=1` | Disable ANSI color |

## Output contract

Pass `--json` (auto-enabled whenever stdout is piped or redirected) for
machine-readable output. Every success is wrapped in an envelope:

```json
{ "ok": true, "data": { … }, "meta": { "next_cursor": "cmo7…" } }
```

- Read payloads through `.data`. For **list** commands, `data` is the array and
  the pagination cursor is lifted to `meta.next_cursor` — pass it back with
  `--cursor <id>` to fetch the next page.
- Errors print to **stderr** as `{ "ok": false, "error": { "code", "message",
  "status", "retryable", "hint", … } }`.

**Retry policy:** retry only when `error.retryable === true` (e.g.
`RATE_LIMITED`, `UPSTREAM_5XX`, `NETWORK_ERROR`, `TIMEOUT`). Never retry
`NO_TOKEN`, `AUTH_INVALID`, `FORBIDDEN`, or `VALIDATION` — surface the error and,
for auth failures, suggest `papermark login`.

Exit codes: `0` success · `1` API error · `2` auth · `3` validation · `4`
network · `5` internal. Use `--dry-run` to print the HTTP request (token
redacted) without sending it.

## Core workflows

### 1. Share a document as a secure link

```bash
# Find it (or upload if it doesn't exist yet)
papermark documents search "q3 deck" --json
papermark documents upload ./deck.pdf --json          # add --link for a default link

# Create a protected link — confirm options with the user first
papermark links create --document <doc-id> \
  --password "<chosen-or-generated>" \
  --expires 2026-09-01T00:00:00Z \
  --email-protected --watermark \
  --json
```

Return the `url` from the response. Link options include `--password`,
`--expires <iso>`, `--email-protected`, `--allow-download`, `--confidential-view`,
`--screenshot-protection`, and a full `--watermark` / `--watermark-text` set
(tokens `{{email}}`, `{{date}}`, `{{time}}`, `{{link}}`, `{{ipAddress}}` are
interpolated per view).

### 2. Answer "who viewed X?"

```bash
# Resolve the link if the user gave a name/document
papermark links list --document <doc-id> --json

# Per-view list for a link (viewer email, view type, timestamps)
papermark views list --link <link-id> --json

# Aggregate analytics (views, unique viewers, total read time, per-page time)
papermark analytics document <doc-id> --json
papermark analytics link <link-id> --json
papermark analytics view <view-id> --json     # page-by-page breakdown for one view
```

`visitors list` / `visitors views <id>` track persistent viewers across links.

### 3. Build a data room for a deal

```bash
papermark datarooms create --name "Acme — Series A" --description "Diligence" --json
papermark datarooms folders create <dr-id> --name "Financials" --json
papermark datarooms attach <dr-id> --document <doc-id> --folder-id <folder-id> --json
papermark datarooms links <dr-id> --json                 # links scoped to the room
papermark datarooms stats <dr-id> --json                 # room-level analytics
```

Create a share link for the whole room with `papermark links create --dataroom
<dr-id>`. Set per-file/folder view & download permissions with `papermark links
permissions set <link-id> --items '[…]'`.

## Command reference

Run `papermark <group> --help` for full flags. Groups:

- **auth** — `login`, `logout`, `whoami`, `auth export`, `auth set`
- **config** — `config get|set|unset` (e.g. `api-url`)
- **doctor** — health/preflight check
- **documents** — `list`, `get`, `search`, `upload`, `update`, `delete`,
  `versions list|get|add|promote`
- **folders** — `list`, `create`, `get`, `update`, `delete`, `move` (team library)
- **links** — `list`, `get`, `create`, `update`, `delete`, `permissions get|set`
- **datarooms** (alias `dr`) — `list`, `get`, `create`, `update`, `delete`,
  `links`, `viewers`, `documents`, `stats`, `attach`, `folders list|create|get|update|delete|move`
- **views** — `list` (per-link view events)
- **visitors** — `list`, `get`, `views`
- **analytics** — `document`, `link`, `dataroom`, `view`

## Do not

- Upload any file the user didn't explicitly point at.
- Create or modify links for documents/data rooms the user didn't name.
- Invent passwords, expiry dates, watermark text, or recipient emails — ask.
- Delete documents, links, folders, or data rooms without explicit confirmation;
  these are irreversible.
- Retry after `AUTH_INVALID` / `FORBIDDEN` — surface the error and suggest
  `papermark login`.
