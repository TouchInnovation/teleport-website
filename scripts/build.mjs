#!/usr/bin/env node
// Build the static site into dist/ for Cloudflare Pages.
// - copies public/ → dist/
// - injects GA_MEASUREMENT_ID (env) into assets/analytics.js, if set
// - rewrites the canonical SITE_URL (env, default https://teleport.touchhk.com) into og:image
import { cpSync, rmSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(root, 'public');
const out = join(root, 'dist');

const SITE_URL = (process.env.SITE_URL || 'https://teleport.touchhk.com').replace(/\/$/, '');
const GA_ID = (process.env.GA_MEASUREMENT_ID || '').trim();

rmSync(out, { recursive: true, force: true });
cpSync(src, out, { recursive: true });

function edit(rel, fn) {
  const p = join(out, rel);
  if (!existsSync(p)) return;
  writeFileSync(p, fn(readFileSync(p, 'utf8')));
}

if (GA_ID) {
  if (!/^G-[A-Z0-9]{6,}$/.test(GA_ID)) {
    console.error(`GA_MEASUREMENT_ID "${GA_ID}" does not look like a GA4 ID (G-XXXXXXXX).`);
    process.exit(1);
  }
  edit('assets/analytics.js', (s) => s.replace("'G-XXXXXXXXXX';", `'${GA_ID}';`));
  console.log(`GA4: ${GA_ID}`);
} else {
  console.log('GA4: GA_MEASUREMENT_ID not set — analytics stays off');
}

for (const page of ['index.html', 'v3.html']) {
  edit(page, (s) => s.replaceAll('__SITE_URL__', SITE_URL));
}

console.log(`Built dist/ for ${SITE_URL}`);
