# Teleport website

One-page marketing site for Teleport (Hire More), aimed at Hong Kong recruitment-agency owners. Plain static HTML/CSS/JS, no build step.

## Structure

- `index.html` — v2 design (styles and script inline)
- `v3.html` — v3 design with HD character photos, for side-by-side comparison
- `assets/teleport-hero.jpg` — low-res cover crop used by `index.html`
- `assets/people/*-1200.jpg` / `*-2400.jpg` — HD character photos from the current deck (Figma V4.2, upscaled), used by `v3.html`: `hero-tablet` (73:2), `consultant-orange` (131:17), `meeting` (138:26), `cafe-laptop` (52:14), `handshake` (53:6)

## Preview locally

Open `index.html` in a browser, or run `npx serve .`

## Deploy

Import this repo into Vercel as a static site (Framework preset: Other, no build command, output directory `.`). Every PR gets a preview URL; `main` is production.

## Before going live

- [ ] Replace every `CONTACT_EMAIL` in `index.html` with the real booking address
- [ ] Swap the CSS-rebuilt wordmark for the official logo file (SVG) from Figma
- [ ] Confirm the brand orange — `--orange: #FF8200` is sampled from the cover, not an approved hex
- [ ] Confirm rights to use the cover / character photos publicly (check licence)
- [ ] Connect a domain

## Copy rule

Only claim what is live today. Anything still being built is labelled *In development* / *Building*. No borrowed client logos, invented metrics, or testimonials.
