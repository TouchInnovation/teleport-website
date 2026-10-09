# Teleport website

One-page marketing site for Teleport (Hire More), aimed at Hong Kong recruitment-agency owners. Plain static HTML/CSS/JS, no build step.

## Structure

- `index.html` — v2 design (styles and script inline)
- `v3.html` — v3 design with HD character photos, for side-by-side comparison
- `assets/teleport-hero.jpg` — low-res cover crop used by `index.html`
- `assets/people/*-1200.jpg` / `*-2400.jpg` — HD character photos from the current deck (Figma V4.2, upscaled), used by `v3.html`: `hero-tablet` (73:2), `consultant-orange` (131:17), `meeting` (138:26), `cafe-laptop` (52:14), `handshake` (53:6)

## Languages

Both pages have an **EN / 繁 / 简** switch in the nav (English, Traditional Chinese for HK, Simplified Chinese).

- Link straight to a language with `?lang=zh-HK`, `?lang=zh-CN` or `?lang=en`
- The choice is remembered in the browser; first visit follows the browser language (zh-HK/TW → 繁, zh-CN/SG → 简)
- Translations live in `tools/add_i18n.py` (one table: key, English, 繁, 简). To change copy, edit the table, restore the English HTML, and re-run `python3 tools/add_i18n.py index.html v3.html`. The script tags elements with `data-i18n` and is a no-op on already-tagged pages.

## Preview locally

Open `index.html` in a browser, or run `npx serve .`

## Deploy

Import this repo into Vercel as a static site (Framework preset: Other, no build command, output directory `.`). Every PR gets a preview URL; `main` is production.

## Before going live

- [ ] Replace every `CONTACT_EMAIL` in `index.html` with the real booking address
- [ ] Swap the CSS-rebuilt wordmark for the official logo file (SVG) from Figma
- [ ] Confirm the brand orange — `--orange: #FF8200` is sampled from the cover, not an approved hex
- [ ] Confirm rights to use the cover / character photos publicly (check licence)
- [ ] Native-speaker review of the 繁 / 简 copy
- [ ] Connect a domain

## Copy rule

Only claim what is live today. Anything still being built is labelled *In development* / *Building*. No borrowed client logos, invented metrics, or testimonials.
