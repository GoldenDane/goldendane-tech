"""Generate GoldenDane logo files.

The mark: four tiles whose gaps form the Nordic (Danish) cross. One tile is
gold: the piece of work that's been taken care of. Run
`python3 tools/brand.py` to rebuild every SVG in assets/brand/ and the favicon.
Needs: pip install fonttools brotli uharfbuzz
"""
import io
import pathlib

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "brand"
OUT.mkdir(parents=True, exist_ok=True)

INK, GOLD_INK, GOLD = "#10181A", "#9C7419", "#D4AE52"
SLATE, WHITE = "#34464C", "#FFFFFF"

# 64-unit grid. Vertical gap at x 21–29 (offset left, like the Nordic cross), horizontal gap at y 27–35.
TILES = [(0, 0, 21, 27), (29, 0, 35, 27), (0, 35, 21, 29)]
GOLD_TILE = (29, 35, 35, 29)
R = 6


def mark_shapes(tile, gold, x0=0.0, y0=0.0, s=1.0):
    rects = []
    for (x, y, w, hgt) in TILES:
        rects.append(f'<rect x="{x0 + x*s:.2f}" y="{y0 + y*s:.2f}" width="{w*s:.2f}" height="{hgt*s:.2f}" rx="{R*s:.2f}" fill="{tile}"/>')
    x, y, w, hgt = GOLD_TILE
    rects.append(f'<rect x="{x0 + x*s:.2f}" y="{y0 + y*s:.2f}" width="{w*s:.2f}" height="{hgt*s:.2f}" rx="{R*s:.2f}" fill="{gold}"/>')
    return "".join(rects)


def svg(w, h, body, title="GoldenDane"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img">'
            f'<title>{title}</title>{body}</svg>\n')


# --- wordmark as outlines (Fraunces, optical size 36, weight 500) ---
font_path = ROOT / "assets" / "fonts" / "fraunces-latin-opsz-normal.woff2"
font = TTFont(font_path)
inst = instantiateVariableFont(font, {"opsz": 36, "wght": 500})
upem = inst["head"].unitsPerEm
cap = inst["OS/2"].sCapHeight
glyphset = inst.getGlyphSet()
# HarfBuzz can't read WOFF2, so shape with the instantiated font saved as plain TrueType.
_buf = io.BytesIO()
inst.flavor = None
inst.save(_buf)
hbfont = hb.Font(hb.Face(hb.Blob(_buf.getvalue())))


def shape(text, x_start, size, baseline):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    scale = size / upem
    pen = SVGPathPen(glyphset, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    x = x_start
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = inst.getGlyphOrder()[info.codepoint]
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, baseline - pos.y_offset * scale))
        glyphset[name].draw(tpen)
        x += pos.x_advance * scale
    return pen.getCommands(), x


def lockup(word_a, word_b, tile, gold):
    H = 64.0                      # mark height
    size = H * 0.52 / (cap / upem)  # cap height = 52% of mark height
    gap = H * 0.32
    baseline = H / 2 + (cap / upem * size) / 2
    d_a, x = shape("Golden", H + gap, size, baseline)
    d_b, x = shape("Dane", x, size, baseline)
    width = x + 2
    body = mark_shapes(tile, gold) + f'<path d="{d_a}" fill="{word_a}"/><path d="{d_b}" fill="{word_b}"/>'
    return svg(width, H, body)


files = {
    "goldendane-mark.svg": svg(64, 64, mark_shapes(INK, GOLD)),
    "goldendane-mark-on-dark.svg": svg(64, 64, mark_shapes(SLATE, GOLD)),
    "goldendane-logo.svg": lockup(INK, GOLD_INK, INK, GOLD),
    "goldendane-logo-on-dark.svg": lockup(WHITE, GOLD, SLATE, GOLD),
}
for name, data in files.items():
    (OUT / name).write_text(data, encoding="utf-8")

# Favicon: ink tiles on light browser chrome, slate tiles on dark chrome.
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 68 68">'
       '<style>.t{fill:#10181A}@media (prefers-color-scheme:dark){.t{fill:#9FB0B4}}</style>'
       + mark_shapes("X", GOLD).replace('fill="X"', 'class="t"') + "</svg>\n")
(ROOT / "assets" / "favicon.svg").write_text(fav, encoding="utf-8")
print("Wrote", ", ".join(files), "and favicon.svg")
