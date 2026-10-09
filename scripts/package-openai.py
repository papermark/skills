#!/usr/bin/env python3
"""Validate this repository's OpenAI package and build an allowlisted ZIP.

Uses Python 3's standard library and Node.js for the existing sync check.
This is a local preflight, not a replacement for OpenAI's submission checks.
"""

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "providers/codex/plugin"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def build(check=False):
    subprocess.run(["node", str(ROOT / "scripts/sync-skills.mjs"), "--check"], check=True)
    manifest = json.loads((PLUGIN / "plugin.json").read_text())
    legacy = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
    mcp = json.loads((PLUGIN / "mcp.json").read_text())
    require(manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "Unexpected plugin schema")
    require(mcp["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json", "Unexpected MCP schema")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest["name"]) and len(manifest["name"]) <= 64, "Invalid plugin name")
    require(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), "Use a stable semantic version")
    extension = manifest["extensions"]["com.openai"]
    require(not ({"apps", "hooks"} & extension.keys()), "Public submission cannot include app references or hooks")
    listing = extension["interface"]
    require(listing == legacy["interface"], "Portable and compatibility listing metadata differ")
    for key in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords"):
        require(manifest[key] == legacy[key], f"Compatibility metadata differs: {key}")
    for key, limit in {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}.items():
        require(isinstance(listing[key], str) and 0 < len(listing[key].strip()) <= limit, f"Invalid {key} (limit {limit})")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        url = urlsplit(listing[key])
        require(url.scheme == "https" and url.hostname and not url.username and not url.password, f"Invalid {key}")
    prompts = listing["defaultPrompt"]
    require(len(prompts) <= 3 and all(0 < len(p) <= 128 for p in prompts), "Invalid starter prompts")
    require(set(mcp["mcpServers"]) == {"papermark"}, "Expected one Papermark MCP server")
    server = mcp["mcpServers"]["papermark"]
    require(server == {"type": "streamable-http", "url": "https://mcp.papermark.com/mcp"}, "Unexpected MCP transport or endpoint")
    require(server["url"] == legacy["mcpServers"]["papermark"]["url"], "Compatibility MCP URL differs")

    # Explicit inputs keep credentials, other providers, and local files out.
    files = {"plugin.json": PLUGIN / "plugin.json", "mcp.json": PLUGIN / "mcp.json", "LICENSE.md": ROOT / "LICENSE.md"}
    for name in ("papermark-overview", "papermark-cli"):
        path = PLUGIN / "skills" / name / "SKILL.md"
        content = path.read_text()
        require(content.startswith("---\n"), f"Missing frontmatter: {name}")
        header = content.split("---", 2)[1]
        require(f"name: {name}\n" in header and "description:" in header, f"Missing skill metadata: {name}")
        files[path.relative_to(PLUGIN).as_posix()] = path
    for value in [listing["logo"], listing["composerIcon"], *listing.get("screenshots", [])]:
        require(value.startswith("./assets/") and ".." not in Path(value).parts, "Asset must be inside ./assets/")
        path = PLUGIN / value
        require(path.is_file() and path.stat().st_size <= 5 * 1024 * 1024, f"Missing or oversized asset: {value}")
        # The current listing uses the existing square SVG for both icons.
        if value in (listing["logo"], listing["composerIcon"]):
            require(path.suffix == ".svg", "Update icon validation before changing image format")
            dimensions = re.search(r'viewBox="0 0 (\d+) (\d+)"', path.read_text())
            require(dimensions and dimensions[1] == dimensions[2] and int(dimensions[1]) >= 48, "Icon must have a square viewBox of at least 48px")
        files[path.relative_to(PLUGIN).as_posix()] = path
    for name, path in files.items():
        require(path.is_file() and not path.is_symlink(), f"Package input must be a regular file: {name}")
        require(not any(parent.is_symlink() for parent in path.parents), f"Symlinked package input: {name}")
    print(f"Local preflight passed: {len(files)} files, two skills, one remote MCP server.")
    if check:
        return
    output = ROOT / "dist" / f"{manifest['name']}-openai-{manifest['version']}.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, path in sorted(files.items()):
            entry = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    with ZipFile(output) as archive:
        require(archive.testzip() is None and set(archive.namelist()) == set(files), "ZIP integrity check failed")
    print(f"Built {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate without writing a ZIP")
    args = parser.parse_args()
    try:
        build(args.check)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Packaging failed: {error}") from error
