"""Extract every glyph of Hoefler Text Ornaments as an SVG path (y-down, font units, 2000/em).
Needs fontTools:  python3 -m venv .venv && .venv/bin/pip install fonttools && .venv/bin/python extract.py
Writes glyphs/glyphs.json, consumed by compose.py / candidates.py (which need only the stdlib)."""
import json, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = "/System/Library/Fonts/Supplemental/Hoefler Text Ornaments.ttf"
f = TTFont(FONT); gs = f.getGlyphSet(); cmap = f.getBestCmap(); glyf = f["glyf"]; hmtx = f["hmtx"]
out = {}
for gn in f.getGlyphOrder():
    g = glyf[gn]
    if not g.numberOfContours: continue
    pen = SVGPathPen(gs); gs[gn].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
    cps = [cp for cp, n in cmap.items() if n == gn]; cp = cps[0] if cps else None
    # The font uses the old symbol-font convention: typing 'A' yields U+F041.
    key = chr(cp - 0xF000) if cp and 0xF000 <= cp < 0xF100 else (chr(cp) if cp else None)
    out[gn] = dict(name=gn, cp=cp, key=key, adv=hmtx[gn][0], bbox=[g.xMin, -g.yMax, g.xMax, -g.yMin], d=pen.getCommands())
os.makedirs("glyphs", exist_ok=True)
json.dump(out, open("glyphs/glyphs.json", "w"), indent=0)
print(len(out), "glyphs ->", "glyphs/glyphs.json")
