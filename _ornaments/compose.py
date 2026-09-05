import json, html, os, re
from urllib.parse import quote
# Path is relative to this file, so the module works from any working directory.
G = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "glyphs", "glyphs.json")))
CELL = 2000; YTOP = -1600  # y-down: a cell spans y in [-1600, 400) relative to its baseline
CX, CY = CELL/2, YTOP+CELL/2
FLIP_H = f"translate({CELL} 0) scale(-1 1)"
FLIP_V = f"translate(0 {2*CY}) scale(1 -1)"
ROT180 = f"rotate(180 {CX} {CY})"
def key2name(k):
    for n,g in G.items():
        if g["key"]==k: return n
    raise KeyError(k)

def grid_svg(rows, fill="rgba(255,230,150,0.9)", wrap=True, pad_top=0, pad_bottom=0, extra=""):
    """rows: list of rows of items; item = None | key-char | glyph name | (key_or_name, transform).
    Returns (svg, W_units, H_units). viewBox is exactly one repeat period. Glyphs are emitted once
    in <defs> and placed with <use>, including wrapped copies so edge overshoot survives tiling."""
    H = len(rows); W = max(len(r) for r in rows)
    PW, PH = W*CELL, H*CELL+pad_top+pad_bottom
    used = {}; uses=[]
    offs = [(dx,dy) for dx in (-PW,0,PW) for dy in (-PH,0,PH)] if wrap else [(0,0)]
    for r,row in enumerate(rows):
        for c,item in enumerate(row):
            if item is None: continue
            tf=""
            if isinstance(item, tuple): item, tf = item
            name = item if item in G else key2name(item)
            gid = "g%d" % list(G).index(name)
            used[gid] = G[name]["d"]
            for dx,dy in offs:
                t = f"translate({c*CELL+dx} {r*CELL+dy})" + (" "+tf if tf else "")
                uses.append(f'<use href="#{gid}" transform="{t}"/>')
    defs = "".join(f'<path id="{k}" d="{v}"/>' for k,v in used.items())
    vb = f"0 {YTOP-pad_top} {PW} {PH}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><defs>{defs}</defs>'
           f'<g fill="{fill}">{"".join(uses)}{extra}</g></svg>')
    return svg, PW, PH

def rail(y, thickness, W):  # horizontal rule across the tile, in font units (y-down)
    return f'<rect x="0" y="{y-thickness/2}" width="{W}" height="{thickness}"/>'

def data_uri(svg):
    return "data:image/svg+xml," + quote(svg, safe="=:/ ,;()'#-._~!*")
