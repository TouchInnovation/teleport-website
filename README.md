# Teleport website

Marketing site for Teleport (Hire More), aimed at Hong Kong recruitment-agency owners. Static HTML/CSS/JS with a tiny Node build step, deployed on **Cloudflare Pages**. Package manager: **pnpm**.

## Structure

```
public/                 # everything that ships
  index.html            # v2 design
  v3.html               # v3 design with HD character photos (also served at /v3)
  _headers              # Cloudflare Pages headers (caching, security)
  assets/
    analytics.js        # GA4 (inactive until GA_MEASUREMENT_ID is set)
    teleport-hero.jpg   # low-res cover crop used by index.html
    people/*-1200.jpg, *-2400.jpg   # HD character photos (Figma V4.2): hero-tablet, consultant-orange, meeting, cafe-laptop, handshake
scripts/build.mjs       # public/ → dist/, injects GA_MEASUREMENT_ID and SITE_URL
tools/add_i18n.py       # EN / 繁 / 简 translation table + tagger
wrangler.toml           # Cloudflare Pages config (output: dist)
```

## Local development

```bash
pnpm install
pnpm dev          # build + wrangler pages dev on http://localhost:8788
pnpm build        # just build dist/
```

Requires Node ≥ 20 (`.node-version` pins 22) and pnpm 10 (`corepack enable` or `npm i -g pnpm`).

## Deploy — Cloudflare Pages

### Option A: Git integration (recommended)

Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git** → `TouchInnovation/teleport-website`.

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | None |
| Build command | `pnpm build` |
| Build output directory | `dist` |
| Root directory | *(blank)* |

Environment variables (Production, and Preview if you want analytics there):

| Variable | Value |
|---|---|
| `GA_MEASUREMENT_ID` | `G-…` from GA4 (optional — analytics stays off without it) |
| `SITE_URL` | `https://teleport.touchhk.com` (default) — used for the share image URL |

Cloudflare detects pnpm from `pnpm-lock.yaml` and Node from `.node-version`. Every branch / PR gets a preview URL (`<branch>.teleport-website.pages.dev`); `main` is production.

### Option B: Direct upload from a machine

```bash
pnpm wrangler login
pnpm deploy            # production (main)
pnpm deploy:preview    # preview deployment for the current branch
```

### Custom domain

Pages project → **Custom domains → Set up a domain** → `teleport.touchhk.com`. If `touchhk.com` is on Cloudflare DNS this is one click; otherwise add a `CNAME teleport → teleport-website.pages.dev` at the current DNS host.

The domain currently points at GitHub Pages (`CNAME` file in the repo root). Cut over by changing that DNS record to Cloudflare, then switch GitHub Pages off (Settings → Pages) and delete `CNAME`.

## Languages

Both pages have an **EN / 繁 / 简** switch in the nav.

- Link straight to a language with `?lang=zh-HK`, `?lang=zh-CN` or `?lang=en`
- The choice is remembered in the browser; first visit follows the browser language (zh-HK/TW → 繁, zh-CN/SG → 简)
- Translations live in `tools/add_i18n.py` (key, English, 繁, 简). To change copy, edit the table, restore the English HTML, and run `pnpm i18n`. The script tags elements with `data-i18n` and is a no-op on already-tagged pages.

## Analytics (GA4)

Set `GA_MEASUREMENT_ID` in Cloudflare Pages (see above). The build writes it into `assets/analytics.js`. Without it nothing loads; it never runs on `file://` previews.

Events (each carries `page_variant` v2/v3 and `site_language`):

- `generate_lead` — mailto / Book clicks. Mark as a **Key event** in GA4.
- `cta_click` — every button, with `cta_text` and `cta_location`
- `language_switch` — `from_language` → `to_language`
- `section_view` — each main section seen (50%)

Register event-scoped custom dimensions `page_variant`, `site_language`, `cta_location`, `section_id`, `to_language` in GA4 to break reports down.

## Before going live

- [ ] Replace every `CONTACT_EMAIL` in `public/*.html` with the real booking address
- [ ] Swap the CSS-rebuilt wordmark for the official logo file (SVG) from Figma
- [ ] Confirm the brand orange — `--orange: #FF8200` is sampled from the cover, not an approved hex
- [ ] Confirm rights to use the cover / character photos publicly (check licence)
- [ ] Native-speaker review of the 繁 / 简 copy
- [ ] Set `GA_MEASUREMENT_ID` in Cloudflare Pages
- [ ] Point `teleport.touchhk.com` at Cloudflare Pages

## Copy rule

Only claim what is live today. Anything still being built is labelled *In development* / *Building*. No borrowed client logos, invented metrics, or testimonials.
