# Teleport website

One-page marketing site for Teleport (Hire More), aimed at Hong Kong recruitment-agency owners. Plain static HTML/CSS/JS, no build step.

## Structure

- `index.html` — the page (styles and script inline)
- `assets/teleport-hero.jpg` — photo cropped from the Figma brand cover (`Teleport HR Operating System`, frame 202:351)

## Preview locally

Open `index.html` in a browser, or run `npx serve .`

## Deploy

Import this repo into Vercel as a static site (Framework preset: Other, no build command, output directory `.`). Every PR gets a preview URL; `main` is production.

## Before going live

- [ ] Replace every `CONTACT_EMAIL` in `index.html` with the real booking address
- [ ] Swap the CSS-rebuilt wordmark for the official logo file (SVG) from Figma
- [ ] Confirm the brand orange — `--orange: #FF8200` is sampled from the cover, not an approved hex
- [ ] Confirm rights to use the cover photo publicly (stock licence if applicable)
- [ ] Connect a domain

## Copy rule

Only claim what is live today. Anything still being built is labelled *In development* / *Building*. No borrowed client logos, invented metrics, or testimonials.
