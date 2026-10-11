"""Render the PNG icons, logo PNGs and social-share images from the SVGs.
Run after tools/brand.py:  python3 tools/render_images.py   (needs playwright + chromium)"""
import asyncio, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "assets"
FONTS = (A / "fonts.css").as_uri()
def logo(name): return (A / "brand" / name).as_uri()

OG = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{fonts}"><style>
body{{margin:0;width:1200px;height:630px;background:#10181A;color:#E8ECEA;font-family:"IBM Plex Sans";position:relative;overflow:hidden}}
.lg{{position:absolute;left:80px;top:72px;height:56px}}
h1{{position:absolute;left:80px;right:110px;top:205px;margin:0;font-family:"Fraunces";font-weight:500;font-size:{size}px;line-height:1.08;letter-spacing:-.012em;color:#fff;font-variation-settings:"opsz" 72}}
h1 em{{color:#D4AE52;font-weight:400}}
.ft{{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono";font-size:22px;color:#9AA8A6}}
.rule{{position:absolute;left:80px;width:64px;height:3px;background:#D4AE52;bottom:120px}}
</style></head><body><img class="lg" src="{logo}"><h1>{h1}</h1><div class="rule"></div><div class="ft"><span>{left}</span><span>{right}</span></div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        async def shot(html, w, h, out, transparent=False):
            pg = await b.new_page(viewport={"width": w, "height": h})
            # Load from a file: pages set from a string may not read local files.
            tmp = ROOT / "tools" / "_render.html"
            tmp.write_text(html, encoding="utf-8")
            await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(400)
            tmp.unlink()
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(out), omit_background=transparent)
            await pg.close()
        page = lambda inner, bg="transparent": f'<!doctype html><html><body style="margin:0;background:{bg}">{inner}</body></html>'
        # favicon PNG for old browsers (transparent, light-tab colours)
        await shot(page(f'<img src="{(A/"favicon.svg").as_uri()}" width="32" height="32" style="display:block">'), 32, 32, A / "favicon-32.png", True)
        # Apple touch icon: opaque ink square, iOS rounds the corners itself
        await shot(page(f'<div style="width:180px;height:180px;display:grid;place-items:center"><img src="{logo("goldendane-mark-on-dark.svg")}" width="128" height="128"></div>', "#10181A"), 180, 180, A / "apple-touch-icon.png")
        # Logo PNGs for email signatures, documents and slides
        for name, bg in [("goldendane-logo", "transparent"), ("goldendane-logo-on-dark", "transparent"), ("goldendane-mark", "transparent"), ("goldendane-mark-on-dark", "transparent")]:
            w = 64 if "mark" in name else None
            await shot(page(f'<img src="{logo(name + ".svg")}" style="display:block;height:512px">'), (512 if "mark" in name else 1640), 512, A / "brand" / (name + ".png"), True)
        # Social share images
        await shot(OG.format(fonts=FONTS, logo=logo("goldendane-logo-on-dark.svg"), size=74,
                             h1='We automate the admin your team still does <em>by hand.</em>',
                             left="Orders · Customer emails · Documents", right="goldenda.com · Copenhagen"), 1200, 630, ROOT / "og-image.png")
        await shot(OG.format(fonts=FONTS, logo=logo("goldendane-logo-on-dark.svg"), size=70,
                             h1='Vi automatiserer det papirarbejde, jeres team stadig laver <em>i hånden.</em>',
                             left="Ordrer · Kundemails · Dokumenter", right="goldenda.com/da · København"), 1200, 630, ROOT / "og-image-da.png")
        await b.close()
asyncio.run(main())
print("Rendered icons, logo PNGs and share images")
