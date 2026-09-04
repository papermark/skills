#!/usr/bin/env node
// Fans the canonical skills (and brand assets) out into every provider plugin.
//
// Each agent harness installs a plugin by copying its own directory, so the
// skills have to physically live inside `providers/<provider>/plugin/`. This
// script is the only thing that writes them — edit `skills/` at the repo root
// and re-run it.
//
//   node scripts/sync-skills.mjs           # write
//   node scripts/sync-skills.mjs --check   # exit 1 if anything is out of date

import { readdirSync, readFileSync, rmSync, mkdirSync, cpSync, existsSync } from "node:fs";
import { join, relative, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

// `assets` is only fanned out to providers whose manifest references it.
const TARGETS = [
  { plugin: "providers/claude/plugin", assets: false },
  { plugin: "providers/codex/plugin", assets: true },
];

const check = process.argv.includes("--check");

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out.sort();
}

function snapshot(dir) {
  if (!existsSync(dir)) return new Map();
  return new Map(walk(dir).map((f) => [relative(dir, f), readFileSync(f)]));
}

function diff(from, to) {
  const src = snapshot(from);
  const dst = snapshot(to);
  const stale = [];
  for (const [path, bytes] of src) {
    if (!dst.has(path) || !dst.get(path).equals(bytes)) stale.push(path);
  }
  for (const path of dst.keys()) if (!src.has(path)) stale.push(path);
  return stale;
}

const drift = [];

for (const { plugin, assets } of TARGETS) {
  const dirs = assets ? ["skills", "assets"] : ["skills"];
  for (const dir of dirs) {
    const from = join(ROOT, dir);
    const to = join(ROOT, plugin, dir);
    const stale = diff(from, to);
    if (stale.length === 0) continue;

    if (check) {
      drift.push(...stale.map((f) => `${plugin}/${dir}/${f}`));
      continue;
    }
    rmSync(to, { recursive: true, force: true });
    mkdirSync(to, { recursive: true });
    cpSync(from, to, { recursive: true });
    console.log(`synced ${dir}/ -> ${plugin}/${dir}/ (${stale.length} file(s))`);
  }
}

if (check && drift.length > 0) {
  console.error("Provider plugins are out of sync with the canonical sources:\n");
  for (const f of drift) console.error(`  ${f}`);
  console.error("\nRun `node scripts/sync-skills.mjs` and commit the result.");
  process.exit(1);
}

console.log(check ? "Provider plugins are in sync." : "Done.");
