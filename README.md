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
| `assets/favicon.svg`, `*.png` | Icons. |

## Quick upgrades

- **Booking link**: in `assets/site.js`, set `BOOKING_URL` (first line) to a Cal.com or Calendly link. Every "Book" button then opens the calendar.
- **Founder photos**: in `index.html`, replace the initials inside `<div class="portrait">SG</div>` and `<span class="av">SG</span>` with `<img src="assets/team/soheil.jpg" alt="">` (square, at least 400×400). Same for Vadim. Then run `python3 tools/build_da.py`.
- **LinkedIn**: add a link under each founder's role, and add the URLs to `"sameAs"` in the JSON-LD at the top of `index.html`.
