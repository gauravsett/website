import json
from urllib.parse import quote
L = json.load(open("glyphs/lattice_layers.json"))
def uri(svg): return "data:image/svg+xml," + quote(svg, safe="=:/,;-._~!*")
def tile(paths):  # one 2000-unit cell, viewBox exactly one period, opaque black for use as a CSS mask
    return uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1600 2000 2000">' + "".join(f'<path d="{p}"/>' for p in paths) + '</svg>')
dots_svg = "".join(f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}"/>' for x,y,s in L["dots"])
NET   = uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1600 2000 2000">' + dots_svg + f'<path d="{L["center"]}"/></svg>')
SPIKES = tile([L["spikes"]]); SPRIGS = tile([L["spikes"], L["sprigs"]]); FLEUR = tile([L["fleurons"]])

HTML = r'''<title>Lattice Motion Studies</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,300;0,400;0,500;1,300&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:rgb(50,10,20);--ink:rgb(255,254,238);--ink-2:rgba(255,254,238,.68);--gold:rgb(255,230,150);--gold-dim:rgba(255,230,150,.25);--rule:rgba(255,230,150,.16);
 --a:1;--spd:1;--serif:"IBM Plex Serif",Georgia,"Times New Roman",serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
html{color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--ink);font:300 17px/1.5 var(--serif);-webkit-font-smoothing:antialiased}
a{color:var(--ink);text-decoration-color:rgba(255,230,150,.5);text-underline-offset:3px} a:hover{color:var(--gold)}
.wrap{max-width:1080px;margin:0 auto;padding:56px 24px 96px}
.prose{max-width:66ch}
h1{font:300 44px/1.1 var(--serif);color:var(--gold);margin:0 0 12px;text-wrap:balance;letter-spacing:-.01em}
h2{font:400 26px/1.2 var(--serif);color:var(--gold);margin:0;text-wrap:balance}
h3{font:500 17px/1.3 var(--serif);margin:28px 0 6px}
p{margin:12px 0} .lede{font-size:19px}
.eyebrow{font:500 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--gold-dim);margin:0 0 18px}
.rulehead{display:flex;align-items:baseline;gap:16px;border-bottom:1px solid var(--rule);padding-bottom:10px;margin-top:72px}
.rulehead .eyebrow{margin:0;margin-left:auto}
code{font:400 .88em var(--mono);color:var(--gold);background:rgba(255,230,150,.07);padding:1px 5px;border-radius:2px}
dl.map{display:grid;grid-template-columns:max-content 1fr;gap:6px 22px;margin:18px 0;max-width:66ch}
dl.map dt{font:500 15px var(--serif);color:var(--gold)} dl.map dd{margin:0;color:var(--ink-2)}
ul{padding-left:22px;margin:10px 0} li{margin:6px 0}
/* controls */
.ctl{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;align-items:center;gap:10px 22px;padding:12px 0;margin:28px 0 8px;background:linear-gradient(var(--bg) 78%,transparent);font:400 13px var(--mono);color:var(--ink-2)}
.ctl label{color:var(--gold)} .ctl input[type=range],.tools input[type=range]{accent-color:var(--gold);width:min(220px,40vw);vertical-align:middle} .tools input[type=range]{width:140px} .tools output{font:400 13px var(--mono);color:var(--ink);min-width:3ch;text-align:right} .ctl output{display:inline-block;min-width:4ch;font-variant-numeric:tabular-nums;color:var(--ink)}
.ctl small{color:var(--gold-dim)}
button{font:500 12px var(--mono);letter-spacing:.06em;color:var(--gold);background:none;border:1px solid var(--gold-dim);padding:7px 11px;cursor:pointer}
button:hover,button:focus-visible{border-color:var(--gold);outline:none}
button[aria-pressed="true"]{background:var(--gold);color:var(--bg);border-color:var(--gold)}
select{font:400 13px var(--mono);color:var(--gold);background:var(--bg);border:1px solid var(--gold-dim);padding:5px 8px}
/* studies */
.study{margin:40px 0 0}
.study header{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;margin:0 0 10px;font-size:15px}
.id{font:500 12px/1 var(--mono);color:var(--gold);border:1px solid var(--gold-dim);padding:5px 7px 4px;letter-spacing:.06em}
.name{font-weight:400} .meta{color:var(--ink-2);font-size:14px} .study header .tools{margin-left:auto;display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;font-size:13px}
.stage{position:relative;height:320px;overflow:hidden;outline:1px solid var(--rule);background:var(--bg)}
.stage canvas{display:block;width:100%;height:100%}
.study .note{max-width:66ch;color:var(--ink-2);font-size:15px;margin:10px 0 0}
.study .note strong{color:var(--ink);font-weight:500}
/* masked CSS layers */
.layer{position:absolute;inset:0;background-color:var(--gold);-webkit-mask-repeat:repeat;mask-repeat:repeat;-webkit-mask-size:64px 64px;mask-size:64px 64px}
.net{-webkit-mask-image:url("__NET__");mask-image:url("__NET__")}
.spikes{-webkit-mask-image:url("__SPIKES__");mask-image:url("__SPIKES__")}
.sprigs{-webkit-mask-image:url("__SPRIGS__");mask-image:url("__SPRIGS__")}
.fleur{-webkit-mask-image:url("__FLEUR__");mask-image:url("__FLEUR__")}
/* m1 sheen: the net as a mask over a slowly travelling highlight */
.sheen{opacity:calc(.26*var(--a));background-color:transparent;
 background-image:linear-gradient(135deg,var(--gold) 0 34%,rgb(255,246,214) 47%,#fff 50%,rgb(255,246,214) 53%,var(--gold) 66% 100%);
 background-size:300% 300%;animation:sheen calc(16s/var(--spd)) linear infinite}
@keyframes sheen{from{background-position:100% 100%}to{background-position:0% 0%}}
/* m4 lamp: plain net everywhere, ornate layer through a soft radial window that follows the pointer */
.lamp .net{opacity:calc(.2*var(--a))}
.window{position:absolute;inset:0;-webkit-mask-image:radial-gradient(circle 230px at var(--mx,50%) var(--my,50%),#000 0,rgba(0,0,0,.6) 45%,transparent 100%);mask-image:radial-gradient(circle 230px at var(--mx,50%) var(--my,50%),#000 0,rgba(0,0,0,.6) 45%,transparent 100%)}
.window .layer{opacity:calc(.42*var(--a))}
/* m5 zoning: three layers, each faded by a horizontal gradient mask that drifts */
.zone .net{opacity:calc(.2*var(--a))}
.zone .fade{position:absolute;inset:0;-webkit-mask-size:200% 100%;mask-size:200% 100%;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;animation:drift calc(18s/var(--spd)) ease-in-out infinite alternate}
.zone .fade.a{-webkit-mask-image:linear-gradient(90deg,#000 0 18%,transparent 34%);mask-image:linear-gradient(90deg,#000 0 18%,transparent 34%)}
.zone .fade.b{-webkit-mask-image:linear-gradient(90deg,#000 0 8%,transparent 26%);mask-image:linear-gradient(90deg,#000 0 8%,transparent 26%);animation-delay:-6s}
.zone .fade.a .layer{opacity:calc(.32*var(--a))} .zone .fade.b .layer{opacity:calc(.34*var(--a))}
@keyframes drift{from{-webkit-mask-position:-4% 0;mask-position:-4% 0}to{-webkit-mask-position:-16% 0;mask-position:-16% 0}}
@media (prefers-reduced-motion:reduce){.sheen,.zone .fade{animation:none}}
.spec{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin-top:16px}
.spec figure{margin:0;text-align:center} .spec svg{width:96px;height:96px;fill:var(--gold);display:block} .spec figcaption{font:400 11px var(--mono);color:var(--gold-dim);margin-top:4px}
.spec .plus{font:300 26px var(--serif);color:var(--gold-dim)}
@media (max-width:760px){h1{font-size:34px}.stage{height:260px}}
</style>
<div class="wrap">
<p class="eyebrow">gauravsett.com &middot; background motion studies</p>
<h1>Lattice Motion Studies</h1>
<div class="prose">
<p class="lede">Seven ways to make the jaal move. Six are ambient and one is a page-load moment. All of them rest on a fact about the font: the four diaper tiles share one net and differ only in what blooms at the cell centre.</p>
<p>Pulling the tiles apart gives a net of 24 dots plus a centre square that never changes, and three ornament layers that can be laid on any cell: spikes, sprigs, fleurons. Blending from one lattice to another is therefore never a morph of geometry. The net holds still and the blooms fade and scale, cell by cell, which is also what keeps it cheap.</p>
</div>
<div class="spec">
<figure><svg viewBox="0 -1600 2000 2000">__DOTS_SVG__<path d="__CENTER__"/></svg><figcaption>net</figcaption></figure><span class="plus">+</span>
<figure><svg viewBox="0 -1600 2000 2000"><path d="__SPIKES_D__"/></svg><figcaption>spikes</figcaption></figure><span class="plus">+</span>
<figure><svg viewBox="0 -1600 2000 2000"><path d="__SPRIGS_D__"/></svg><figcaption>sprigs</figcaption></figure><span class="plus">+</span>
<figure><svg viewBox="0 -1600 2000 2000"><path d="__FLEUR_D__"/></svg><figcaption>fleurons</figcaption></figure>
</div>
<div class="prose">
<p>The sari gives the motion its vocabulary. Zari thread catches light as the wearer moves, cloth breathes and drapes, the weave is laid down thread by thread on a loom, and the border and pallu are denser than the field. Each study below takes one of those.</p>
</div>

<div class="ctl">
 <span><label for="ink">Ink</label> <input id="ink" type="range" min="0.4" max="2.5" step="0.05" value="1"> <output id="inko">1.00</output>&times;</span>
 <span><label for="spd">Speed</label> <input id="spd" type="range" min="0.25" max="4" step="0.05" value="1"> <output id="spdo">1.00</output>&times;</span>
 <small>speed 1&times; is the pace proposed for the site &middot; canvases pause off screen</small>
</div>

<section class="study" id="m1"><header><span class="id">m1</span><span class="name">Zari sheen</span><span class="meta">CSS only &middot; the net as a mask over a travelling highlight</span></header>
<div class="stage"><div class="layer net sheen"></div></div>
<p class="note">One lattice, alive by lighting alone. A soft highlight crosses the net along the thread direction every sixteen seconds, the way metallic thread flashes when a sari moves. <strong>Cost:</strong> zero JavaScript, one masked div, one keyframe. The quietest option and the easiest to ship.</p></section>

<section class="study" id="m2"><header><span class="id">m2</span><span class="name">Breeze</span><span class="meta">canvas &middot; the net displaced by slow noise &middot; move the pointer</span>
<span class="tools"><label for="m2r" class="meta">radius</label><input id="m2r" type="range" min="100" max="600" step="10" value="340"><output id="m2ro">340</output><span class="meta">px</span>
<label for="m2s" class="meta">strength</label><input id="m2s" type="range" min="0" max="2" step="0.05" value="0.7"><output id="m2so">0.70</output>
<select id="m2p"><option value="ring">ring (soft centre)</option><option value="dome">dome (strong centre)</option></select>
<button type="button" id="m2i" aria-pressed="false">Invert</button></span></header>
<div class="stage"><canvas data-field='{"breeze":true,"cursor":true,"radius":340,"profile":"ring","strength":0.7}'></canvas></div>
<p class="note">Cloth hung in moving air. Every dot drifts a couple of pixels on a noise field and its brightness shimmers, so the grid reads as a surface rather than a pattern. The pointer presses the fabric: dots near it are pushed outward and brighten. The press radius is set broad here, about a third of the stage. The <strong>ring</strong> profile leaves the dots directly under the pointer almost still and moves them most about a third of the way out, which is how cloth behaves under a fingertip; <strong>dome</strong> is the usual falloff, strongest at the centre. Strength scales both the push and the brightening. <strong>Invert</strong> mirrors the chosen profile across the radius, so nothing moves under the pointer and the disturbance sits at the far edge of the circle, tapering off just inside the radius so there is no hard rim. <strong>Cost:</strong> about the same as the current star canvas, which already does the brightness half of this on a square grid.</p></section>

<section class="study" id="m3"><header><span class="id">m3</span><span class="name">Bloom field</span><span class="meta">canvas &middot; one lattice becomes another, cell by cell</span>
<span class="tools"><label for="m3mode" class="meta">motion</label><select id="m3mode"><option value="drift">drift (regions wander)</option><option value="breathe">breathe (whole field cycles)</option><option value="tide">tide (a wave passes)</option></select></span></header>
<div class="stage"><canvas data-field='{"blooms":true,"mode":"drift","cursor":false}'></canvas></div>
<p class="note">The net stays fixed and a slow value field decides how much each cell blooms: nothing, spikes, sprigs, or the full fleuron. <strong>Drift</strong> is the answer to "part of the screen has one lattice and part has another": islands of ornament form, wander, and dissolve over about a minute. <strong>Breathe</strong> cycles the whole field from plain to ornate and back, one lattice becoming the next. <strong>Tide</strong> sends a single wave of ornament across the field. Drift is the one I would ship; the other two read as effects once you have seen them twice.</p></section>

<section class="study" id="m4"><header><span class="id">m4</span><span class="name">Lamp</span><span class="meta">CSS masks + six lines of JS &middot; move the pointer</span></header>
<div class="stage lamp"><div class="layer net"></div><div class="window"><div class="layer fleur"></div></div></div>
<p class="note">The plain field everywhere, and the ornate jaal only inside a soft circle of light around the pointer, as if holding a lamp to brocade. Without a pointer the lamp wanders slowly on its own, so touch devices still see it live. This is the direct descendant of the glow the star canvas already draws around the cursor. <strong>Cost:</strong> two masked divs and a pointermove handler that sets two CSS variables.</p></section>

<section class="study" id="m5"><header><span class="id">m5</span><span class="name">Pallu zoning</span><span class="meta">CSS only &middot; density by position</span></header>
<div class="stage zone"><div class="layer net"></div><div class="fade a"><div class="layer sprigs"></div></div><div class="fade b"><div class="layer fleur"></div></div></div>
<p class="note">Different lattices in different parts of the screen, arranged the way a sari is: ornate at the edge, plain across the body. On the site the dense band would sit under the 360 px sidebar with the headshot and name, and the reading column would get the plain net. The boundary drifts a few percent over eighteen seconds so it never looks like a hard cut. <strong>Cost:</strong> three masked layers, no JavaScript.</p></section>

<section class="study" id="m6"><header><span class="id">m6</span><span class="name">Loom</span><span class="meta">canvas &middot; a page-load sequence, then rest</span><span class="tools"><button type="button" id="replay">Replay</button></span></header>
<div class="stage"><canvas data-loom="1"></canvas></div>
<p class="note">The only orchestrated moment. On load, the warp threads lay down along one diagonal with a bright leading edge, then the weft crosses them on the other, then the sprigs open at the intersections. Five seconds, once, then the field is still. With reduced motion on it simply appears finished. Pairs well with m1 or m3 for what happens afterwards.</p></section>

<section class="study" id="m7"><header><span class="id">m7</span><span class="name">Composite</span><span class="meta">canvas &middot; drift + breeze + lamp + sheen in one loop &middot; move the pointer</span></header>
<div class="stage"><canvas data-field='{"blooms":true,"mode":"drift","breeze":true,"cursor":true,"sheen":true,"amp":1.2,"radius":260,"profile":"ring","strength":0.8}'></canvas></div>
<p class="note">What I would actually propose for the site: the bloom field drifting slowly, a faint breeze so the net is a surface, the pointer raising the bloom level around it so the lamp effect comes free, and a very slow sheen. One canvas, one animation frame loop, and it replaces the star canvas rather than adding to it, so the reduced-motion and visibility handling already in the layout carries over unchanged.</p></section>

<div class="rulehead"><h2>Reading the studies</h2><p class="eyebrow">what to choose</p></div>
<div class="prose">
<dl class="map">
<dt>Living fabric</dt><dd>m1 sheen and m2 breeze keep a single lattice and animate light or position. m1 is the safe pick, m2 the more tactile one.</dd>
<dt>Lattice to lattice</dt><dd>m3 breathe cycles everything through the four tiles. m3 tide does it as a passing wave.</dd>
<dt>Different lattices by region</dt><dd>m3 drift moves the regions; m5 zoning fixes them by layout; m4 lamp lets the pointer decide.</dd>
<dt>A moment</dt><dd>m6 loom, once per visit.</dd>
</dl>
<p>The ideas compose because they share one engine and one net. The composite (m7) shows drift, breeze, lamp and sheen together, and it is the one I would carry into the layout, with the loom as an optional opening. If the site should stay closer to what it has today, m1 over the b3 border is a two-rule change with no script at all.</p>
<h3>Things to keep in mind</h3>
<ul>
<li>Every canvas study honours <code>prefers-reduced-motion</code> by drawing one still frame, pauses when the tab is hidden, and pauses when scrolled out of view. The site's current canvas does the first two; the third is new.</li>
<li>Canvas cost at 1280&times;900 and 64 px cells is roughly 1,500 dots and 300 cells per frame. The blooms are pre-rendered sprites, so the fleuron outlines are never re-rasterised in the loop.</li>
<li>The CSS studies use <code>mask-image</code>, supported in every current browser. The prefixed form is included for older Safari.</li>
<li>The lattice data (dots and the three layers) is in <code>_ornaments/glyphs/lattice_layers.json</code> in the repo, next to the tile generator from the first round.</li>
</ul>
</div>
</div>
<script>
(function(){
const T=__TILEDATA__, U=2000, YOFF=1600, GOLD='255,230,150';
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
const S={ink:1,speed:1};
function hash(x,y){const n=Math.sin(x*127.1+y*311.7)*43758.5453;return n-Math.floor(n)}
function noise(x,y){const ix=Math.floor(x),iy=Math.floor(y);let fx=x-ix,fy=y-iy;fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy);const a=hash(ix,iy),b=hash(ix+1,iy),c=hash(ix,iy+1),d=hash(ix+1,iy+1);return a+(b-a)*fx+(c-a)*fy+(a-b-c+d)*fx*fy}
const ss=(a,b,x)=>{const t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)};
const paths={center:new Path2D(T.center),spikes:new Path2D(T.spikes),sprigs:new Path2D(T.sprigs),fleurons:new Path2D(T.fleurons)};

class Field{
  constructor(canvas,opts){
    this.c=canvas;this.o=Object.assign({cell:64,blooms:false,breeze:false,cursor:false,sheen:false,mode:'drift',amp:2.2,radius:150,strength:1,profile:'dome',invert:false},opts);
    this.ctx=canvas.getContext('2d');this.mx=-1e4;this.my=-1e4;this.t=0;this.last=null;this.raf=null;this.visible=false;
    if(this.o.cursor){canvas.addEventListener('pointermove',e=>{const r=canvas.getBoundingClientRect();this.mx=e.clientX-r.left;this.my=e.clientY-r.top});canvas.addEventListener('pointerleave',()=>{this.mx=-1e4;this.my=-1e4})}
    new ResizeObserver(()=>this.resize()).observe(canvas);
    new IntersectionObserver(es=>{this.visible=es[0].isIntersecting;this.visible?this.start():this.stop()}).observe(canvas);
    document.addEventListener('visibilitychange',()=>document.hidden?this.stop():this.start());
    reduce.addEventListener('change',()=>{this.stop();this.start()});
    this.resize();
  }
  resize(){
    const dpr=Math.min(2,devicePixelRatio||1),w=this.c.clientWidth,h=this.c.clientHeight;if(!w||!h)return;
    this.w=w;this.h=h;this.dpr=dpr;this.c.width=Math.round(w*dpr);this.c.height=Math.round(h*dpr);this.ctx.setTransform(dpr,0,0,dpr,0,0);
    const cell=this.o.cell,k=cell/U;this.k=k;this.cols=Math.ceil(w/cell)+1;this.rows=Math.ceil(h/cell)+1;
    const m=new Map();
    for(let r=0;r<this.rows;r++)for(let c=0;c<this.cols;c++)for(const [x,y,s] of T.dots){
      const gx=c*cell+x*k,gy=r*cell+(y+YOFF)*k,key=gx.toFixed(1)+','+gy.toFixed(1);
      if(!m.has(key))m.set(key,{x:gx,y:gy,s:Math.max(1.4,s*k),warp:Math.abs(x-(y+YOFF))<20,weft:Math.abs(x+(y+YOFF)-U)<20});
    }
    this.dots=[...m.values()];
    this.cells=[];for(let r=0;r<this.rows;r++)for(let c=0;c<this.cols;c++)this.cells.push({c,r,x:c*cell+cell/2,y:r*cell+cell/2,seed:hash(c*7.3+1,r*3.1+2)});
    this.sprites={};
    for(const name in paths){const s=document.createElement('canvas');s.width=s.height=Math.ceil(cell*dpr);const g=s.getContext('2d');g.setTransform(dpr*k,0,0,dpr*k,0,YOFF*dpr*k);g.fillStyle='rgb('+GOLD+')';g.fill(paths[name]);this.sprites[name]=s}
    this.draw(this.t);
  }
  start(){if(this.raf!==null||!this.visible||document.hidden)return;if(reduce.matches){this.draw(this.t);return}
    this.last=null;const loop=now=>{if(this.last!==null)this.t+=Math.min(.1,(now-this.last)/1000)*S.speed;this.last=now;this.draw(this.t);this.raf=requestAnimationFrame(loop)};this.raf=requestAnimationFrame(loop)}
  stop(){if(this.raf!==null){cancelAnimationFrame(this.raf);this.raf=null}}
  press(x,y){const R=this.o.radius,dx=x-this.mx,dy=y-this.my,dist=Math.sqrt(dx*dx+dy*dy);if(dist>=R||dist<=0)return null;const g0=dist/R,k=this.o.strength,inv=this.o.invert,g=inv?1-g0:g0;let s,b;
    if(this.o.profile==='ring'){s=Math.pow(g,.6)*Math.pow(1-g,1.4)/.294;b=.16*s+.05*(1-g)}else{s=(1-g)*(1-g);b=.35*(1-g)}
    if(inv){const taper=1-ss(.72,1,g0);s*=taper;b*=taper}
    const push=Math.min(14,R*.035)*k*s;return [dx/dist*push,dy/dist*push,b*k]}
  blit(name,x,y,scale,alpha){if(alpha<=0.004)return;const cell=this.o.cell*scale;this.ctx.globalAlpha=Math.min(1,alpha);this.ctx.drawImage(this.sprites[name],x-cell/2,y-cell/2,cell,cell);this.ctx.globalAlpha=1}
  level(ce,t){const o=this.o,c=ce.c,r=ce.r;let n;
    if(o.mode==='breathe'){n=.5+.48*Math.sin(t*.22)+.12*(noise(c*.4,r*.4)-.5)}
    else if(o.mode==='tide'){const q=(((ce.x+ce.y)*.0016-t*.05)%1+1)%1;n=Math.pow(Math.max(0,1-Math.abs(q-.5)*2.8),1.3)*.95+.16*noise(c*.5,r*.5)}
    else{n=noise(c*.23+t*.04,r*.23+t*.03)*.7+noise(c*.55-t*.02,r*.55+t*.015)*.3;n=(n-.28)/.5}
    if(o.cursor){const R=this.o.radius*1.6,dx=ce.x-this.mx,dy=ce.y-this.my,d=Math.sqrt(dx*dx+dy*dy),f=Math.max(0,1-d/R);n+=.6*f*f}
    return n}
  draw(t){const ctx=this.ctx,o=this.o,w=this.w,h=this.h,ink=S.ink,amp=o.breeze?o.amp:0;ctx.clearRect(0,0,w,h);
    for(const d of this.dots){let x=d.x,y=d.y,b=.22;
      if(o.breeze){x+=(noise(d.x*.006,d.y*.006+t*.12)-.5)*2*amp;y+=(noise(d.x*.006+40,d.y*.006-t*.1)-.5)*2*amp;b=.12+.22*noise(d.x*.005,d.y*.005+t*.3)}
      if(o.cursor){const p=this.press(x,y);if(p){x+=p[0];y+=p[1];b+=p[2]}}
      ctx.fillStyle='rgba('+GOLD+','+Math.min(1,b*ink)+')';ctx.fillRect(x-d.s/2,y-d.s/2,d.s,d.s)}
    for(const ce of this.cells){let x=ce.x,y=ce.y;
      if(o.breeze){x+=(noise(x*.006,y*.006+t*.12)-.5)*2*amp;y+=(noise(x*.006+40,y*.006-t*.1)-.5)*2*amp}
      if(o.cursor&&o.breeze){const p=this.press(x,y);if(p){x+=p[0];y+=p[1]}}
      const n=o.blooms?this.level(ce,t):0,fl=ss(.72,.9,n),sp=ss(.38,.52,n)*(1-fl),sg=ss(.55,.7,n)*(1-fl);
      this.blit('center',x,y,1,(.22+.2*Math.max(sp,sg,fl))*ink);
      if(sp>.01)this.blit('spikes',x,y,.75+.25*sp,sp*.5*ink);
      if(sg>.01)this.blit('sprigs',x,y,.7+.3*sg,sg*.45*ink);
      if(fl>.01)this.blit('fleurons',x,y,.7+.3*fl,fl*.42*ink)}
    if(o.sheen){const p=(t*.03)%1,s=p*(w+h)*1.4-(w+h)*.2,b=w*.22;const g=ctx.createLinearGradient(s/2-b,s/2-b,s/2+b,s/2+b);
      g.addColorStop(0,'rgba(255,246,214,0)');g.addColorStop(.5,'rgba(255,250,230,.45)');g.addColorStop(1,'rgba(255,246,214,0)');
      ctx.globalCompositeOperation='source-atop';ctx.fillStyle=g;ctx.fillRect(0,0,w,h);ctx.globalCompositeOperation='source-over'}
  }
}
class Loom extends Field{
  constructor(canvas){super(canvas,{cell:64});this.total=6}
  start(){if(this.raf!==null||!this.visible||document.hidden)return;if(reduce.matches){this.t=this.total;this.draw(this.t);return}super.start()}
  replay(){this.t=0;this.last=null;if(reduce.matches){this.draw(this.total);return}this.stop();this.start()}
  draw(t){const ctx=this.ctx,w=this.w,h=this.h,ink=S.ink,d1=2.3,d2=2.3;ctx.clearRect(0,0,w,h);
    if(t>this.total+1){this.stop()}
    const f1=Math.min(1,t/d1)*(w+h)+40,f2=-h+Math.min(1,Math.max(0,(t-d1)/d2))*(w+h)+40;
    const edge=(dd)=>dd<0?0:dd<48?.22+.7*(1-dd/48):.22;
    for(const d of this.dots){let a=0;if(d.warp)a=Math.max(a,edge(f1-(d.x+d.y)));if(d.weft&&t>d1)a=Math.max(a,edge(f2-(d.x-d.y)));if(a<=0)continue;
      ctx.fillStyle='rgba('+GOLD+','+Math.min(1,a*ink)+')';ctx.fillRect(d.x-d.s/2,d.y-d.s/2,d.s,d.s)}
    for(const ce of this.cells){const p=ss(0,1,(t-d1-d2-ce.seed*.7)/.9);if(p<=0)continue;
      this.blit('center',ce.x,ce.y,1,.3*p*ink);this.blit('sprigs',ce.x,ce.y,.5+.5*p,.4*p*ink)}
  }
}
const fields=[];
document.querySelectorAll('canvas[data-field]').forEach(c=>fields.push(new Field(c,JSON.parse(c.dataset.field))));
const m2=fields.find(f=>f.c.closest('#m2')),m2r=document.getElementById('m2r'),m2ro=document.getElementById('m2ro');m2r.addEventListener('input',()=>{m2.o.radius=+m2r.value;m2ro.textContent=m2r.value});
const m2s=document.getElementById('m2s'),m2so=document.getElementById('m2so');m2s.addEventListener('input',()=>{m2.o.strength=+m2s.value;m2so.textContent=(+m2s.value).toFixed(2)});
document.getElementById('m2p').addEventListener('change',e=>{m2.o.profile=e.target.value});
const m2i=document.getElementById('m2i');m2i.addEventListener('click',()=>{m2.o.invert=!m2.o.invert;m2i.setAttribute('aria-pressed',String(m2.o.invert))});
const m3=fields.find(f=>f.c.closest('#m3'));document.getElementById('m3mode').addEventListener('change',e=>{m3.o.mode=e.target.value});
const loom=new Loom(document.querySelector('canvas[data-loom]'));document.getElementById('replay').addEventListener('click',()=>loom.replay());
// lamp: pointer sets the window centre; otherwise it wanders on its own
(function(){const st=document.querySelector('.lamp');let idle=true,t=0,raf=null;
  st.addEventListener('pointermove',e=>{const r=st.getBoundingClientRect();st.style.setProperty('--mx',(e.clientX-r.left)+'px');st.style.setProperty('--my',(e.clientY-r.top)+'px');idle=false});
  st.addEventListener('pointerleave',()=>{idle=true});
  function wander(now){if(idle&&!reduce.matches){t=now/1000*S.speed;const w=st.clientWidth,h=st.clientHeight;st.style.setProperty('--mx',(w*.5+w*.36*Math.sin(t*.21))+'px');st.style.setProperty('--my',(h*.5+h*.3*Math.sin(t*.33+1))+'px')}raf=requestAnimationFrame(wander)}
  new IntersectionObserver(es=>{if(es[0].isIntersecting){if(raf===null)raf=requestAnimationFrame(wander)}else if(raf!==null){cancelAnimationFrame(raf);raf=null}}).observe(st);
})();
// controls
const ink=document.getElementById('ink'),inko=document.getElementById('inko'),spd=document.getElementById('spd'),spdo=document.getElementById('spdo');
function sync(){S.ink=+ink.value;S.speed=+spd.value;document.documentElement.style.setProperty('--a',ink.value);document.documentElement.style.setProperty('--spd',spd.value);inko.textContent=S.ink.toFixed(2);spdo.textContent=S.speed.toFixed(2);if(reduce.matches)fields.forEach(f=>f.draw(f.t))}
ink.addEventListener('input',sync);spd.addEventListener('input',sync);sync();
})();
</script>
'''
page = (HTML.replace("__TILEDATA__", json.dumps(L)).replace("__NET__", NET).replace("__SPIKES__", SPIKES).replace("__SPRIGS__", SPRIGS).replace("__FLEUR__", FLEUR)
        .replace("__DOTS_SVG__", dots_svg).replace("__CENTER__", L["center"]).replace("__SPIKES_D__", L["spikes"]).replace("__SPRIGS_D__", L["spikes"]+L["sprigs"]).replace("__FLEUR_D__", L["fleurons"]))
open("lattice-motion-studies.html","w").write(page)
import os; print("bytes", os.path.getsize("lattice-motion-studies.html"))
