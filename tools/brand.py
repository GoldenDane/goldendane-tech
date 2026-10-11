"""Generate GoldenDane logo files.

The mark is a hallmark: the stamp a goldsmith strikes into real gold to prove
it is genuine. An octagonal cartouche with the initials GD, echoing our promise
that every system is tested before anyone relies on it.

Run `python3 tools/brand.py` to rebuild every SVG in assets/brand/ and the
favicon, then `python3 tools/render_images.py` for the PNGs.
Needs: pip install fonttools brotli uharfbuzz
"""
import io
import pathlib

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "brand"
OUT.mkdir(parents=True, exist_ok=True)

INK, NIGHT, GOLD, GOLD_INK, WHITE = "#10181A", "#1E2C31", "#D4AE52", "#9C7419", "#FFFFFF"
FONT_FILE = ROOT / "assets" / "fonts" / "fraunces-latin-opsz-normal.woff2"


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Face:
    """One instance of Fraunces, drawn as outlines so no font is needed to show the logo."""

    def __init__(self, opsz, wght):
        font = instantiateVariableFont(TTFont(FONT_FILE), {"opsz": opsz, "wght": wght})
        font.flavor = None  # HarfBuzz can't read WOFF2: shape from plain TrueType
        buf = io.BytesIO()
        font.save(buf)
        self.hb = hb.Font(hb.Face(hb.Blob(buf.getvalue())))
        self.glyphs = font.getGlyphSet()
        self.order = font.getGlyphOrder()
        self.upem = font["head"].unitsPerEm
        self.cap = font["OS/2"].sCapHeight

    def run(self, text, size, tracking=0.0):
        """Glyph placements scaled to `size`, plus the total advance."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        s = size / self.upem
        x, out = 0.0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], x + pos.x_offset * s, pos.y_offset * s))
            x += pos.x_advance * s + tracking * size
        return out, s, x - tracking * size

    def path(self, text, size, x0, baseline, tracking=0.0):
        placed, s, _ = self.run(text, size, tracking)
        pen = SVGPathPen(self.glyphs, ntos=num)
        for name, x, y in placed:
            self.glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, x0 + x, baseline - y)))
        return pen.getCommands()

    def ink_bounds(self, text, size, tracking=0.0):
        placed, s, _ = self.run(text, size, tracking)
        pen = BoundsPen(self.glyphs)
        for name, x, y in placed:
            self.glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, x, -y)))
        return pen.bounds  # xmin, ymin, xmax, ymax; y points down, baseline at 0


MONO = Face(opsz=72, wght=600)   # the initials in the hallmark
WORD = Face(opsz=36, wght=500)   # the wordmark


def octagon(inset, chamfer, size=64):
    a, b, c = inset, size - inset, chamfer
    return (f"M{num(a + c)} {num(a)}H{num(b - c)}L{num(b)} {num(a + c)}V{num(b - c)}"
            f"L{num(b - c)} {num(b)}H{num(a + c)}L{num(a)} {num(b - c)}V{num(a + c)}Z")


def initials(height):
    """'GD' centred in the 64 grid, cap height = `height`."""
    size = height / (MONO.cap / MONO.upem)
    track = -0.02
    x0, y0, x1, y1 = MONO.ink_bounds("GD", size, track)
    return MONO.path("GD", size, 32 - (x0 + x1) / 2, 32 - (y0 + y1) / 2, track)


def mark(body, frame, letters, small=False):
    """64-unit hallmark. `small` drops the inner frame and enlarges the letters for icon sizes."""
    parts = [f'<path d="{octagon(1.5, 11)}" fill="{body}"/>']
    if small:
        parts.append(f'<path d="{initials(25.5)}" fill="{letters}"/>')
    else:
        parts.append(f'<path d="{octagon(6.5, 8.6)}" fill="none" stroke="{frame}" stroke-width="1.7"/>')
        parts.append(f'<path d="{initials(20.5)}" fill="{letters}"/>')
    return "".join(parts)


def svg(w, h, body, title="GoldenDane"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {num(w)} {num(h)}" width="{num(w)}" height="{num(h)}" role="img">'
            f"<title>{title}</title>{body}</svg>\n")


def lockup(body, frame, letters, word_a, word_b):
    H = 64.0
    size = H * 0.46 / (WORD.cap / WORD.upem)   # wordmark cap height = 46% of the mark
    baseline = H / 2 + (WORD.cap / WORD.upem * size) / 2
    _, _, wa = WORD.run("Golden", size)
    _, _, wb = WORD.run("Dane", size)
    x = H + H * 0.3
    a = WORD.path("Golden", size, x, baseline)
    b = WORD.path("Dane", size, x + wa, baseline)
    return svg(x + wa + wb + 2, H, mark(body, frame, letters) + f'<path d="{a}" fill="{word_a}"/><path d="{b}" fill="{word_b}"/>')


files = {
    "goldendane-mark.svg": svg(64, 64, mark(INK, GOLD, GOLD)),
    "goldendane-mark-on-dark.svg": svg(64, 64, mark(NIGHT, GOLD, GOLD)),
    "goldendane-mark-small.svg": svg(64, 64, mark(INK, GOLD, GOLD, small=True)),
    "goldendane-logo.svg": lockup(INK, GOLD, GOLD, INK, GOLD_INK),
    "goldendane-logo-on-dark.svg": lockup(NIGHT, GOLD, GOLD, WHITE, GOLD),
}
for name, data in files.items():
    (OUT / name).write_text(data, encoding="utf-8")

# Favicon: the small hallmark; on dark browser chrome the body lifts a little so its edge stays visible.
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
       '<style>.b{fill:#10181A}@media (prefers-color-scheme:dark){.b{fill:#1E2C31}}</style>'
       + mark("X", GOLD, GOLD, small=True).replace('fill="X"', 'class="b"', 1) + "</svg>\n")
(ROOT / "assets" / "favicon.svg").write_text(fav, encoding="utf-8")
print("Wrote", ", ".join(files), "and favicon.svg")
