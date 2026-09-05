from compose import *
import html, os
ACC = lambda a: f"rgba(255,230,150,{a})"
T1,T2,T3,T4="orn.border.tile.1","orn.border.tile.2","orn.border.tile.3","orn.border.tile.4"
S = lambda k: (k, f"translate({CX} {CY}) scale(0.82) translate({-CX} {-CY})")   # shrink into cell
SF = lambda k: (k, f"translate({CX} {CY}) scale(-0.82 0.82) translate({-CX} {-CY})")  # shrink + mirror

# ---- Banner candidates: (id, title, rows, px_per_cell, kwargs) ----
BANNERS = [
 ("b1","Vine, double row — engraved wave A B / C D (rails inside, lens shapes between)", [list("AB"),list("CD")], 40, {}),
 ("b2","Cartouche — engraved wave C D / A B (rails outside, closed medallions)",       [list("CD"),list("AB")], 40, {}),
 ("b3","Single vine between hairline rails — engraved wave C D",                       [list("CD")], 40,
       dict(pad_top=420, pad_bottom=420, extra=rail(-1600-260,40,4000)+rail(400+260,40,4000))),
 ("b4","Scroll, double row — engraved scroll I J / K L",                                 [list("IJ"),list("KL")], 40, {}),
 ("b5","Paisley wave, double row — simple wave a b / c d (bold, with boteh drops)",     [list("ab"),list("cd")], 40, {}),
 ("b6","Simple scroll, double row — i j / k l",                                          [list("ij"),list("kl")], 40, {}),
 ("b7","Pallu band — vine rail / dot-lattice row / vine rail (C D · tile.1 · A B)",  [list("CD"),[T1,T1],list("AB")], 32, {}),
 ("b8","Buti row — acorn fleurons alternating mirror, between hairline rails",           [[S("Q"),SF("Q")]], 40,
       dict(pad_top=420, pad_bottom=420, extra=rail(-1600-260,40,4000)+rail(400+260,40,4000))),
 ("b9","Vine single row over sprig tiles — C D / tile.3",                                [list("CD"),[T3,T3]], 36, {}),
]
# ---- Background candidates: (id, title, rows, px_per_cell, alpha) ----
BACKGROUNDS = [
 ("g1","Dot lattice — tile.1 (evolves the current star grid)",            [[T1]], 64, 0.22),
 ("g2","Dot lattice with crosses — tile.2",                                [[T2]], 80, 0.14),
 ("g3","Scattered butis — ornate tile.4 on alternate cells",               [[T4,None],[None,T4]], 96, 0.09),
 ("g4","Jaal — tile.3 and tile.1 checkered",                                [[T3,T1],[T1,T3]], 72, 0.09),
 ("g5","Dense jaal — ornate tile.4 everywhere",                            [[T4]], 96, 0.06),
]
os.makedirs("candidates", exist_ok=True); os.makedirs("mock/orn", exist_ok=True)

def write_svgs(cid, rows, kw, alphas):
    out={}
    for a in alphas:
        svg,PW,PH = grid_svg(rows, fill=ACC(a), **kw)
        p=f"mock/orn/{cid}-{int(a*100):02d}.svg"; open(p,"w").write(svg); out[a]=(svg,PW,PH)
    return out

# ---- Sheets ----
def sheet(title, items, kind):
    cells=[]
    for it in items:
        if kind=="banner":
            cid,label,rows,px,kw = it; a_ctx=0.18
            v = write_svgs(cid, rows, kw, [0.9, a_ctx])
            svg,PW,PH = v[0.9]; scale = px/CELL
            bw, bh = PW*scale, PH*scale
            cells.append(f"""<div class=p><div class=l>{cid} — {html.escape(label)}<span class=m>tile {bw:.0f}×{bh:.0f}px at {px}px/cell</span></div>
<div class=sw style="height:{bh*2}px;background-image:url(orn/{cid}-90.svg);background-size:{bw*2}px {bh*2}px"></div>
<div class=ctx style="height:{bh}px;background-image:url(orn/{cid}-18.svg);background-size:{bw}px {bh}px"></div></div>""")
        else:
            cid,label,rows,px,a = it
            v = write_svgs(cid, rows, {}, [0.9, a])
            svg,PW,PH = v[0.9]; scale=px/CELL; bw,bh=PW*scale,PH*scale
            cells.append(f"""<div class=p><div class=l>{cid} — {html.escape(label)}<span class=m>tile {bw:.0f}×{bh:.0f}px, alpha {a}</span></div>
<div class=row><div class=sw style="width:{bw*2}px;height:{bh*2}px;flex:none;background-image:url(orn/{cid}-90.svg);background-size:{bw*2}px {bh*2}px"></div>
<div class=ctx style="flex:1;height:{max(bh*2,240)}px;background-image:url(orn/{cid}-{int(a*100):02d}.svg);background-size:{bw}px {bh}px"></div></div></div>""")
    return f"""<!doctype html><meta charset=utf-8><style>
body{{margin:0;background:rgb(50,10,20);color:rgb(255,254,238);font:13px/1.35 -apple-system,sans-serif;padding:16px}}
h2{{margin:0 0 12px;font-weight:400}} .p{{margin-bottom:18px}} .l{{margin-bottom:6px;color:rgba(255,230,150,.8)}}
.m{{color:rgba(255,230,150,.45);margin-left:12px}} .row{{display:flex;gap:16px;align-items:flex-start}}
.sw,.ctx{{background-repeat:repeat;background-color:rgb(50,10,20)}} .sw{{margin-bottom:6px;border:1px solid rgba(255,230,150,.15)}}
.ctx{{border-top:1px solid rgba(255,230,150,.12)}}
</style><h2>{html.escape(title)}</h2>{''.join(cells)}"""

open("mock/banners.html","w").write(sheet("Banner candidates — bright swatch at 2×, then in situ at alpha 0.18 and real size", BANNERS, "banner"))
open("mock/backgrounds.html","w").write(sheet("Background candidates — bright swatch at 2×, then at intended alpha and real size", BACKGROUNDS, "bg"))

# ---- In-context mocks (override .banner / body background in the real built page) ----
base = open("mock/index.html").read()
def mock(name, css):
    open(f"mock/{name}.html","w").write(base.replace("</head>", f"<style>{css}</style></head>"))
for cid,label,rows,px,kw in BANNERS:
    svg,PW,PH = grid_svg(rows, **kw); s=px/CELL
    mock(f"mock-{cid}", f".banner{{background-image:url(orn/{cid}-18.svg);background-size:{PW*s}px {PH*s}px;height:{PH*s}px}}")
for cid,label,rows,px,a in BACKGROUNDS:
    svg,PW,PH = grid_svg(rows); s=px/CELL
    b1svg,b1W,b1H = grid_svg(BANNERS[0][2]); bs=40/CELL
    mock(f"mock-{cid}", f"#stars{{display:none}} body{{background-image:url(orn/{cid}-{int(a*100):02d}.svg);background-size:{PW*s}px {PH*s}px;background-attachment:fixed}}"
         f".banner{{background-image:url(orn/b1-18.svg);background-size:{b1W*bs}px {b1H*bs}px;height:{b1H*bs}px}}")
# one combo: g1 background + b3 banner, stars kept
svg,PW,PH = grid_svg(BACKGROUNDS[0][2]); s=64/CELL
b3svg,b3W,b3H = grid_svg(BANNERS[2][2], **BANNERS[2][4]); bs=40/CELL
mock("mock-combo", f"body{{background-image:url(orn/g1-22.svg);background-size:{PW*s}px {PH*s}px;background-attachment:fixed}}"
     f".banner{{background-image:url(orn/b3-18.svg);background-size:{b3W*bs}px {b3H*bs}px;height:{b3H*bs}px}}")
print("sizes:", {f: os.path.getsize('mock/orn/'+f) for f in sorted(os.listdir('mock/orn')) if f.endswith('-90.svg')})
