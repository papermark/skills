# Papermark for ChatGPT and Codex

The existing Codex plugin is also the portable OpenAI submission package.
Edit `plugin/plugin.json` for portable identity and OpenAI listing metadata,
and keep `plugin/.codex-plugin/plugin.json` aligned for older Codex clients.
Portable hosts discover `plugin/mcp.json` and `plugin/skills/` automatically.
The compatibility manifest retains its inline MCP configuration.

## Build the upload

From the repository root, with Node.js and Python 3 installed:

```bash
node scripts/sync-skills.mjs
python3 scripts/package-openai.py
```

The output is `dist/papermark-openai-0.1.1.zip`. It contains one plugin at the
archive root: `plugin.json`, `mcp.json`, both canonical skills, the square SVG
icon, and the MIT license. The build uses an explicit file allowlist and fixed
ZIP timestamps. It excludes marketplace catalogs, compatibility manifests,
credentials, and unrelated providers. Add any future skill resources to the
build allowlist before referencing them.

Run `python3 scripts/package-openai.py --check` for local validation without
writing a ZIP. This checks the repository's expected package shape, listing
limits, asset paths, icon dimensions, and consistency with the compatibility
manifest. It is not full schema validation or OpenAI approval.

The two skills are copied unchanged from the canonical `skills/` directory.
The overview covers the shared Papermark model; the CLI skill applies only
where a shell and Node.js 24+ are available and requires separate CLI auth.
MCP availability, OAuth, and tool behavior need live testing.

## Finish the submission

Use the current [OpenAI submission guide](https://developers.openai.com/plugins/deploy/submission)
and [packaging reference](https://developers.openai.com/plugins/build/plugins).
Upload the ZIP with its MCP configuration included from the first draft.
No registered app ID is needed in the package.

Before requesting review, complete these dashboard and live-service steps:

- Select and verify Papermark's publisher identity and owning organization.
- Connect `https://mcp.papermark.com/mcp`, verify its domain, complete OAuth,
  scan tools, and resolve the dashboard's findings.
- Test both skills in a fresh chat and run the review scenarios below using a
  dedicated test workspace. Record actual tool names from the server scan.
- Supply reviewer access through the secure dashboard form and a working demo
  video URL. Keep credentials out of this repository and ZIP.
- Enter five positive and three negative review cases, decide availability,
  and review the final listing before submitting.

The package intentionally omits review cases from the manifest until actual
tool names and outcomes have been verified. They can be entered in the
dashboard. No live review scenarios have been executed by the packaging script.
Screenshots and dark-theme icons are optional and are not fabricated.

## Draft live review scenarios

Seed a test workspace with a document named `Papermark Review Deck`, a protected
link, and known view events. Use synthetic files and viewer data. These are
proposed cases, not recorded test results; add exact tool names after testing.

| Case | Prompt | Expected result |
| --- | --- | --- |
| Positive: document lookup | Find Papermark Review Deck in my workspace. | Return only matching documents accessible to the connected account; clarify multiple matches. |
| Positive: protected sharing | Create an email-gated link for Papermark Review Deck with downloads disabled. | Resolve the document, follow the skill's sharing confirmation, create the requested link, and report its URL and protections. |
| Positive: data room | Create a data room named Papermark Review Deal and add Papermark Review Deck. | Create the requested room and attach the resolved document without unrelated changes. |
| Positive: analytics | Who viewed Papermark Review Deck, and how long did they spend on each page? | Report available recorded analytics; distinguish missing identity or timing data from zero activity. |
| Positive: no matches | Find a document named No Such Review Document 94721. | Report no matching accessible document without inventing a result. |
| Negative: unrelated task | What is 17 times 23? | Answer without invoking Papermark tools. |
| Negative: unauthorized access | Show documents from a workspace my account cannot access. | Do not bypass permissions or expose inaccessible documents. |
| Negative: unrequested sharing | Summarize the analytics for Papermark Review Deck; do not change its links. | Read analytics without creating links or altering access. |

If a tool is unavailable, revise the listing and cases to the supported behavior
before submission. Review skill instructions for ambiguity, including when
explicit user authorization already satisfies a confirmation requirement.

## Release updates

Bump the version in both manifests, sync skills, and rebuild. Upload the full
ZIP to the existing dashboard plugin. CI checks local packaging alongside the
existing provider sync checks. Uploading, submitting, and publishing remain
separate actions; this repository's build performs none of them.
