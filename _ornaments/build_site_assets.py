"""Write the three ornament tiles the site uses into ../assets/.
Fill is solid gold; strength is set in CSS with `opacity`, so recolouring means editing GOLD here
and re-running:  python3 _ornaments/build_site_assets.py  (stdlib only)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from compose import grid_svg, rail, CELL, YTOP

GOLD = "rgb(255,230,150)"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
L = json.load(open(os.path.join(HERE, "glyphs", "lattice_layers.json")))

# Background field: the shared dot net + centre square (orn.border.tile.1). The net repeats
# every cell, but the tile is drawn as a 2x2 block so that it is the same size as the buti
# tile below. That is not cosmetic: two background layers whose background-size differs each
# round their tile to whole device pixels on their own, so at a fractional browser zoom the
# two would round differently and drift apart across the page. Equal tiles round alike.
# grid_svg draws wrapped copies so the corner dots that straddle cell edges tile without gaps.
T1 = "orn.border.tile.1"
net, W, H = grid_svg([[T1, T1], [T1, T1]], fill=GOLD)
open(os.path.join(ASSETS, "lattice.svg"), "w").write(net)

# Hover layer: scattered butis. The same fleurons of orn.border.tile.4, no dots, but on
# only two cells of a 2x2 block, so the motifs sit on a diagonal with a blank cell between.
# Each buti still fills exactly one net cell, so it lands inside the lattice's cells as long
# as this tile is drawn at the same background-size as the lattice. Wrapped copies cover the
# ~32 units the fleurons overshoot their cell, so the tile has no seam.
BLOCK = 2 * CELL
placements = [(0, 0), (CELL, CELL)]
butis = [f'<use href="#buti" transform="translate({x + dx} {y + dy})"/>'
         for x, y in placements
         for dx in (-BLOCK, 0, BLOCK) for dy in (-BLOCK, 0, BLOCK)]
butis_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {YTOP} {BLOCK} {BLOCK}">'
             f'<defs><path id="buti" d="{L["fleurons"]}"/></defs>'
             f'<g fill="{GOLD}">{"".join(butis)}</g></svg>')
open(os.path.join(ASSETS, "butis.svg"), "w").write(butis_svg)

# Banner: a single engraved vine (Hoefler Text Ornaments C D) with a hairline rail
# outside it on each side. One row of cells plus padding, so the tile is 80x60px at
# 40px per cell. Only this one orientation is written: the top banner is the same
# tile mirrored vertically in CSS, so the two frame the page symmetrically.
PAD = 500          # units of clear space above and below the row of cells
RAIL = 50          # rail thickness in units -> 1px at 40px per cell
rows = [list("CD")]
span = len(rows[0]) * CELL
extra = (rail(YTOP - PAD / 2, RAIL, span)
         + rail(YTOP + CELL + PAD / 2, RAIL, span))
banner, W, H = grid_svg(rows, fill=GOLD, pad_top=PAD, pad_bottom=PAD, extra=extra)
open(os.path.join(ASSETS, "banner.svg"), "w").write(banner)

for f in ("lattice.svg", "butis.svg", "banner.svg"):
    print(f, os.path.getsize(os.path.join(ASSETS, f)), "bytes")
print("banner tile units", W, "x", H, "-> at 40px/cell:", W * 40 / CELL, "x", H * 40 / CELL, "px")
