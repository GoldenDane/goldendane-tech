# goldenda.com

Static site for GoldenDane ApS, served by GitHub Pages (custom domain in `CNAME`). No build step: edit the HTML and push.

| File | What it is |
|---|---|
| `index.html` | Home page. Structure follows a cold-called visitor's questions: what is this → can I trust them → what do they do → proof → how it works → who they are → contact. |
| `process-xray.html` | Sample Process X-ray report on public help-desk data. |
| `privacy.html` | Privacy notice. Keep it in sync if you add analytics, forms or third-party scripts. |
| `assets/fonts.css`, `assets/fonts/` | Self-hosted Fraunces and IBM Plex (SIL OFL). No requests to Google. |
| `assets/favicon.svg`, `*.png` | Icons. |

## Quick upgrades

- **Booking link**: in `index.html`, set `BOOKING_URL` (near the top of the `<script>`) to a Cal.com or Calendly link. Every "Book" button then opens the calendar.
- **Founder photos**: replace the initials inside `<div class="portrait">SG</div>` and `<span class="av">SG</span>` with `<img src="assets/team/soheil.jpg" alt="">` (square, at least 400×400). Same for Vadim.
- **LinkedIn**: add a link under each founder's role, and add the URLs to `"sameAs"` in the JSON-LD at the top of `index.html`.
- **Phone number**: add it to the contact section and footer; it is one of the strongest trust signals for Danish B2B buyers.
