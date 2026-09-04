---
name: papermark-overview
description: >
  Explains what Papermark is and how its data is structured — documents,
  versions, folders, share links, data rooms, viewers, views, and analytics —
  plus the rules for sharing safely. Use this for context about the Papermark
  model whenever you act on it through the Papermark MCP server or the
  `papermark` CLI, and especially before creating links, data rooms, or deleting
  anything.
license: MIT
metadata:
    version: '1.0.0'
    author: papermark
---

# Papermark Overview

Papermark is a virtual data room and secure document-sharing platform. Teams
build data rooms for deals and due diligence, share documents behind secure,
trackable links, and see exactly who viewed what — down to per-page read time.

You can drive Papermark two ways, and both speak the same model below:

- **MCP server** (bundled with this plugin at `https://mcp.papermark.com/mcp`) —
  native tool calls; the default in Claude Code and Codex.
- **`papermark` CLI** (published on npm) — best for shells, scripts, and CI. See
  the `papermark-cli` skill.

## Data model

### Documents

A **document** is an uploaded file (PDF, deck, image, etc.) in the team library.
Documents are private by default — uploading one does not share it. Each document
has one or more **versions**; one version is the *primary* (current) version, and
new uploads can be added and promoted over time.

### Folders

A **folder** organizes documents in the team library. Folders are an
organizational layer only — they do not, by themselves, grant anyone access.

### Links

A **share link** is how a document or data room is exposed to outside viewers.
A link can be protected with any combination of:

- a **password**,
- **email gating** (viewer must enter / verify an email before viewing),
- an **expiry** date,
- **allow / deny lists** (restrict to specific emails or domains),
- **download** permission (off by default),
- **watermarks** (with per-view tokens like email, date, IP),
- **screenshot protection** and **confidential view** (blur).

A single document can have many links, each with different protection — that's
how you give different audiences different access.

### Data rooms

A **data room** is a curated collection of documents and folders shared as a unit
— typical for fundraising, M&A, and due diligence. Documents are *attached* to a
data room (they stay in the library), organized into data-room folders, and
exposed through data-room links. Links can carry **per-file/per-folder view and
download permissions**.

### Viewers, views, and analytics

A **viewer** (visitor) is a person who has accessed a link, tracked persistently
across visits (usually by email). A **view** is a single access event. Papermark
records per-view, per-page detail — which pages were seen, time spent on each,
downloads, and viewer geo/client. **Analytics** aggregate this into total views,
unique viewers, and total read time, for a document, a link, or a whole data
room.

## How the pieces fit together

```
document ──(attach)──> data room ──> data-room folder
   │                       │
   └──> link <─────────────┘         link = the shareable, protected URL
            │
            └──> view (per visitor, per page) ──> analytics
```

The usual flow: **upload a document → create a protected link (or build a data
room and link that) → share the URL → read analytics on who viewed it.**

## Rules for sharing safely

These apply no matter which interface you use. Treat them as hard rules:

1. **Only act on what the user named.** Don't upload files, create links, attach
   documents, or build data rooms the user didn't ask for.
2. **Never invent protection values.** Don't make up passwords, expiry dates,
   watermark text, or allow/deny recipients. Ask the user, or if you generate a
   value (e.g. a password), tell them the exact value you used.
3. **Confirm before sharing more widely or removing access.** Creating a link
   exposes a document to anyone who has the URL; deleting documents, links,
   folders, or data rooms is irreversible. Confirm first.
4. **Surface auth and permission errors** rather than retrying blindly — a token
   that's missing or lacks scope won't fix itself.
5. **Return the link URL** when you create one, and be explicit about what
   protection is (and isn't) on it.
