# goldenda.com

Static site for GoldenDane ApS, served by GitHub Pages (custom domain in `CNAME`). No build step: edit the HTML and push.

| File | What it is |
|---|---|
| `index.html` | Home page (English). Structure follows a cold-called visitor's questions: what is this → can I trust them → what do they do → proof → how it works → who they are → contact. |
| `da/index.html` | Home page (Danish). **Generated** from `index.html` by `python3 tools/build_da.py`: edit the English page, then run the script. It stops and names any English text it can no longer find, so add or update the Danish line in `tools/build_da.py` when you change copy. |
| `da/privatliv.html` | Danish privacy notice. Keep it in sync with `privacy.html`. |
| `assets/site.css`, `assets/site.js` | Styles and script shared by both home pages. The script picks Danish or English interface text from `<html lang>`. |
| `process-xray.html` | Sample Process X-ray report on public help-desk data. |
| `privacy.html` | Privacy notice. Keep it in sync if you add analytics, forms or third-party scripts. |
| `assets/fonts.css`, `assets/fonts/` | Self-hosted Fraunces and IBM Plex (SIL OFL). No requests to Google. |
| `assets/brand/` | Logo files: the mark alone and the full logo, as SVG (for print and design tools) and PNG (for email signatures, documents, slides). Use the `-on-dark` versions on dark backgrounds. |
| `assets/favicon.svg`, `*.png` | Icons and social-share images (`og-image.png`, `og-image-da.png`). |
| `tools/brand.py`, `tools/render_images.py` | Rebuild the logo SVGs, then the PNGs and share images. |

## The logo

A hallmark: the stamp a goldsmith strikes into real gold to prove it is genuine, like our promise that every system is tested before anyone relies on it. An ink octagon with a gold frame and the initials GD in Fraunces. Use `goldendane-mark-small.svg` below 24 px (no inner frame), the `-on-dark` files on dark backgrounds, and keep clear space of at least a quarter of the mark's width around it.

## Quick upgrades

- **Booking link**: in `assets/site.js`, set `BOOKING_URL` (first line) to a Cal.com or Calendly link. Every "Book" button then opens the calendar.
- **Founder photos**: in `index.html`, replace the initials inside `<div class="portrait">SG</div>` and `<span class="av">SG</span>` with `<img src="assets/team/soheil.jpg" alt="">` (square, at least 400×400). Same for Vadim. Then run `python3 tools/build_da.py`.
- **LinkedIn**: add a link under each founder's role, and add the URLs to `"sameAs"` in the JSON-LD at the top of `index.html`.
