"""Generate GoldenDane logo files.

The mark: three quarters of a circle and a gold square, which together read
as a G. The square is exactly the size of the quarter missing from the
circle: the circle is a team's workload, the gold square is the piece of work
we lift off it and handle, and the open space it leaves is the time they get
back. Plain geometry in the Danish modernist tradition, so it stays
recognisable in one colour and at 16 px.

Files in assets/brand/:
  goldendane-mark          ink + gold, for light backgrounds
  goldendane-mark-on-dark  white + gold, for dark backgrounds
  goldendane-badge         the mark on an ink rounded square: app icons, avatars, email signatures
  goldendane-logo / -on-dark   mark + wordmark

Run `python3 tools/brand.py`, then `python3 tools/render_images.py` for PNGs.
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

INK, WHITE = "#10181A", "#FFFFFF"
GOLD, GOLD_DEEP, GOLD_INK = "#D4AE52", "#C49A35", "#86651A"

# 100-unit grid: three quarters of a disc (centre 50,50, r 38) open at the top right, and a gold square
# the size of that missing quarter (38), set 3 units down and right of the centre.
DISC = "M50 12A38 38 0 1 0 88 50H50Z"
SQUARE = '<rect x="53" y="53" width="38" height="38" rx="3"'
BOX = (12, 12, 79, 79)


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def shapes(disc, gold):
    return f'<path d="{DISC}" fill="{disc}"/>{SQUARE} fill="{gold}"/>'


def svg(viewbox, w, h, body, title="GoldenDane"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" width="{num(w)}" height="{num(h)}" role="img">'
            f"<title>{title}</title>{body}</svg>\n")


def mark(disc, gold):
    x, y, w, h = BOX
    return svg(f"{x} {y} {w} {h}", w, h, shapes(disc, gold))


def badge():
    body = f'<rect width="100" height="100" rx="22" fill="{INK}"/><g transform="translate(50 50) scale(.7) translate(-51.5 -51.5)">{shapes(WHITE, GOLD)}</g>'
    return svg("0 0 100 100", 100, 100, body)


# --- wordmark as outlines (Fraunces, optical size 36, weight 500) ---
FONT_FILE = ROOT / "assets" / "fonts" / "fraunces-latin-opsz-normal.woff2"
_font = instantiateVariableFont(TTFont(FONT_FILE), {"opsz": 36, "wght": 500})
_font.flavor = None  # HarfBuzz can't read WOFF2: shape from plain TrueType
_buf = io.BytesIO()
_font.save(_buf)
HB = hb.Font(hb.Face(hb.Blob(_buf.getvalue())))
GLYPHS, ORDER = _font.getGlyphSet(), _font.getGlyphOrder()
UPEM, CAP = _font["head"].unitsPerEm, _font["OS/2"].sCapHeight


def word(text, size, x0, baseline):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(HB, buf, {"kern": True, "liga": True})
    s = size / UPEM
    pen = SVGPathPen(GLYPHS, ntos=num)
    x = x0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        GLYPHS[ORDER[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, baseline - pos.y_offset * s)))
        x += pos.x_advance * s
    return pen.getCommands(), x


def lockup(disc, gold, word_a, word_b):
    bx, by, bw, bh = BOX
    H = 64.0
    k = H / bh
    cap = H * 0.48
    size = cap / (CAP / UPEM)
    baseline = H / 2 + cap / 2
    x = H + H * 0.28
    a, xa = word("Golden", size, x, baseline)
    b, xb = word("Dane", size, xa, baseline)
    body = (f'<g transform="scale({num(k)}) translate({num(-bx)} {num(-by)})">{shapes(disc, gold)}</g>'
            f'<path d="{a}" fill="{word_a}"/><path d="{b}" fill="{word_b}"/>')
    return svg(f"0 0 {num(xb + 2)} {num(H)}", xb + 2, H, body)


files = {
    "goldendane-mark.svg": mark(INK, GOLD_DEEP),
    "goldendane-mark-on-dark.svg": mark(WHITE, GOLD),
    "goldendane-badge.svg": badge(),
    "goldendane-logo.svg": lockup(INK, GOLD_DEEP, INK, GOLD_INK),
    "goldendane-logo-on-dark.svg": lockup(WHITE, GOLD, WHITE, GOLD),
}
for stale in ("goldendane-mark-small.svg",):
    (OUT / stale).unlink(missing_ok=True)
for name, data in files.items():
    (OUT / name).write_text(data, encoding="utf-8")

# Favicon: the plain mark; the disc turns white on dark browser chrome.
x, y, w, h = BOX
fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x - 2} {y - 2} {w + 4} {h + 4}">'
       '<style>.d{fill:#10181A}@media (prefers-color-scheme:dark){.d{fill:#FFFFFF}}</style>'
       f'<path class="d" d="{DISC}"/>{SQUARE} fill="{GOLD_DEEP}"/></svg>\n')
(ROOT / "assets" / "favicon.svg").write_text(fav, encoding="utf-8")
print("Wrote", ", ".join(files), "and favicon.svg")
