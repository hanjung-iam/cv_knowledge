"""graph.py — 產生互動式 Wiki 關聯圖（規格見 CLAUDE.md 第 11 節）。

用法：
    python tools/graph.py                # 產出 tools/out/graph.html
    python tools/graph.py --root <dir>   # 測試用

產出的是單一、自足的 HTML 檔（不載入任何外部資源），可離線開啟。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wikilib as wl  # noqa: E402


def build(root: Path) -> dict:
    wiki_dir, pages, _ = wl.load_wiki(root)
    ids = {p.rel for p in pages}
    keys = wl.cite_key_map(pages)
    nodes, edges = [], []
    for p in pages:
        fm = p.fm or {}
        nodes.append({
            "id": p.rel,
            "title": p.title,
            "type": p.type or "unknown",
            "tags": wl.as_list(fm.get("tags")),
            "sources": wl.as_list(fm.get("sources")),
            "updated": fm.get("updated", "") if isinstance(fm.get("updated"), str) else "",
        })
        links = wl.internal_page_links(p, wiki_dir)
        for dest in links:
            if dest in ids and dest != p.rel:
                edges.append({"source": p.rel, "target": dest, "kind": "link"})
        for dest in wl.cited_sources(p, keys):
            if dest in ids and dest not in links:
                edges.append({"source": p.rel, "target": dest, "kind": "cite"})
    return {"nodes": nodes, "edges": edges}


HTML = r"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CV Wiki Graph</title>
<style>
:root{
  --bg:#f7f7f5; --panel:#ffffff; --fg:#1f2328; --muted:#6a737d; --line:#d0d7de;
  --edge:rgba(80,90,100,.28); --edge-hi:rgba(30,40,50,.85);
  --model:#2f6fdd; --task:#d9822b; --concept:#2a9d6f; --source:#8a63d2;
  --comparison:#c94f7c; --overview:#444; --unknown:#999; --dataset:#a0892c;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#16181b; --panel:#1f2226; --fg:#e6e6e6; --muted:#9aa4ae; --line:#33383e;
    --edge:rgba(200,205,210,.22); --edge-hi:rgba(235,240,245,.9);
    --model:#6aa1ff; --task:#f0a55a; --concept:#4cc79a; --source:#b192f0;
    --comparison:#ef7ea6; --overview:#ddd; --unknown:#777; --dataset:#d8c060;
  }
}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--bg);color:var(--fg);
  font-family:system-ui,-apple-system,"Segoe UI","Noto Sans TC","Microsoft JhengHei",sans-serif}
#app{display:flex;height:100%}
#stage{flex:1;position:relative;min-width:0}
canvas{display:block;width:100%;height:100%;cursor:grab}
canvas.dragging{cursor:grabbing}
#side{width:320px;max-width:42vw;border-left:1px solid var(--line);background:var(--panel);
  padding:16px;overflow:auto;font-size:14px}
h1{font-size:16px;margin:0 0 4px}
.muted{color:var(--muted);font-size:12px}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.filters label{display:flex;align-items:center;gap:4px;padding:3px 8px;border:1px solid var(--line);
  border-radius:999px;cursor:pointer;user-select:none;font-size:12px}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
input[type=search]{width:100%;padding:6px 8px;border:1px solid var(--line);border-radius:6px;
  background:var(--bg);color:var(--fg)}
#detail{margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
#detail h2{font-size:15px;margin:0 0 6px}
#detail ul{padding-left:18px;margin:4px 0 10px}
#detail li a{color:inherit;cursor:pointer;text-decoration:underline dotted}
#detail a.file{color:var(--model)}
.hint{position:absolute;left:12px;bottom:10px;font-size:12px;color:var(--muted);pointer-events:none}
@media (max-width:700px){#app{flex-direction:column}#side{width:auto;max-width:none;height:40%;border-left:0;border-top:1px solid var(--line)}}
</style>
</head>
<body>
<div id="app">
  <div id="stage"><canvas id="c"></canvas>
    <div class="hint">實線＝連結、虛線＝引用・拖曳節點移動・拖曳背景平移・滾輪縮放・點節點看詳細</div></div>
  <aside id="side">
    <h1>CV Wiki 關聯圖</h1>
    <div class="muted" id="stats"></div>
    <div class="filters" id="filters"></div>
    <input type="search" id="q" placeholder="搜尋頁面標題…">
    <div id="detail"><span class="muted">點選一個節點查看它的連結。</span></div>
  </aside>
</div>
<script>
const DATA = __DATA__;
const TYPE_LABEL = {overview:"Overview",model:"Model",task:"Task",concept:"Concept",
  dataset:"Dataset",comparison:"Comparison",source:"Source",unknown:"Unknown"};
// 顏色從 CSS 變數讀取後快取；切換深淺色主題時重新讀取
let CSS_CACHE = {};
const css = n => CSS_CACHE[n] ??= getComputedStyle(document.documentElement).getPropertyValue(n).trim();
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { CSS_CACHE = {}; });
const color = t => css("--" + (TYPE_LABEL[t] ? t : "unknown"));

const nodes = DATA.nodes.map((n,i)=>({...n, x:Math.cos(i)*200*Math.random(), y:Math.sin(i)*200*Math.random(), vx:0, vy:0}));
const byId = Object.fromEntries(nodes.map(n=>[n.id,n]));
const edges = DATA.edges.filter(e=>byId[e.source]&&byId[e.target]).map(e=>({s:byId[e.source],t:byId[e.target],cite:e.kind==="cite"}));
nodes.forEach(n=>{n.out=[];n.in=[];});
edges.forEach(e=>{e.s.out.push(e.t);e.t.in.push(e.s);});
nodes.forEach(n=>n.r=6+Math.sqrt(n.in.length+n.out.length)*3);

const types = [...new Set(nodes.map(n=>n.type))].sort((a,b)=>Object.keys(TYPE_LABEL).indexOf(a)-Object.keys(TYPE_LABEL).indexOf(b));
const visibleType = Object.fromEntries(types.map(t=>[t,true]));
document.getElementById("stats").textContent = `${nodes.length} 頁・${edges.length} 條連結`;
const fBox = document.getElementById("filters");
types.forEach(t=>{
  const l=document.createElement("label");
  const cnt=nodes.filter(n=>n.type===t).length;
  l.innerHTML=`<input type="checkbox" checked><span class="dot" style="background:${color(t)}"></span>${TYPE_LABEL[t]||t} (${cnt})`;
  l.querySelector("input").onchange=e=>{visibleType[t]=e.target.checked;heat=1;};
  fBox.appendChild(l);
});

const cv=document.getElementById("c"), ctx=cv.getContext("2d");
let W=0,H=0,dpr=1, view={x:0,y:0,k:1}, selected=null, hover=null, query="", heat=1;
let drag=null,pan=null,moved=false;
function resize(){dpr=window.devicePixelRatio||1;W=cv.clientWidth;H=cv.clientHeight;cv.width=W*dpr;cv.height=H*dpr;}
window.addEventListener("resize",resize);resize();
const vis = n => visibleType[n.type];

function step(){
  if(heat<0.02) return;
  const vn=nodes.filter(vis);
  for(let i=0;i<vn.length;i++)for(let j=i+1;j<vn.length;j++){
    const a=vn[i],b=vn[j];let dx=b.x-a.x,dy=b.y-a.y,d2=dx*dx+dy*dy+0.01;
    if(d2>250000)continue;const f=1800/d2,d=Math.sqrt(d2);dx/=d;dy/=d;
    a.vx-=dx*f;a.vy-=dy*f;b.vx+=dx*f;b.vy+=dy*f;}
  edges.forEach(e=>{if(!vis(e.s)||!vis(e.t))return;let dx=e.t.x-e.s.x,dy=e.t.y-e.s.y;
    const d=Math.sqrt(dx*dx+dy*dy)||1,f=(d-110)*0.02;dx/=d;dy/=d;
    e.s.vx+=dx*f;e.s.vy+=dy*f;e.t.vx-=dx*f;e.t.vy-=dy*f;});
  vn.forEach(n=>{n.vx-=n.x*0.004;n.vy-=n.y*0.004;
    if(n===drag)return;n.x+=n.vx*heat;n.y+=n.vy*heat;n.vx*=0.6;n.vy*=0.6;});
  heat*=0.992;
}

function neighbors(n){return new Set([n,...n.in,...n.out]);}
function draw(){
  ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
  ctx.translate(W/2+view.x,H/2+view.y);ctx.scale(view.k,view.k);
  const focus=selected||hover, nb=focus?neighbors(focus):null;
  const q=query.toLowerCase();
  edges.forEach(e=>{if(!vis(e.s)||!vis(e.t))return;
    const hi=focus&&(e.s===focus||e.t===focus);
    ctx.strokeStyle=hi?css("--edge-hi"):css("--edge");ctx.lineWidth=(hi?1.8:1)/view.k;
    ctx.globalAlpha=focus&&!hi?0.25:1;
    ctx.setLineDash(e.cite?[4/view.k,4/view.k]:[]);   // 引用關係畫虛線
    ctx.beginPath();ctx.moveTo(e.s.x,e.s.y);ctx.lineTo(e.t.x,e.t.y);ctx.stroke();
    ctx.setLineDash([]);
    if(hi){const a=Math.atan2(e.t.y-e.s.y,e.t.x-e.s.x),r=e.t.r+2,x=e.t.x-Math.cos(a)*r,y=e.t.y-Math.sin(a)*r,s=7/view.k;
      ctx.fillStyle=css("--edge-hi");ctx.beginPath();ctx.moveTo(x,y);
      ctx.lineTo(x-Math.cos(a-0.4)*s,y-Math.sin(a-0.4)*s);ctx.lineTo(x-Math.cos(a+0.4)*s,y-Math.sin(a+0.4)*s);ctx.fill();}
  });
  ctx.globalAlpha=1;
  nodes.forEach(n=>{if(!vis(n))return;
    const dim=(nb&&!nb.has(n))||(q&&!n.title.toLowerCase().includes(q)&&!n.id.toLowerCase().includes(q));
    ctx.globalAlpha=dim?0.18:1;ctx.fillStyle=color(n.type);
    ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,Math.PI*2);ctx.fill();
    if(n===selected){ctx.lineWidth=3/view.k;ctx.strokeStyle=css("--fg");ctx.stroke();}
    ctx.fillStyle=css("--fg");ctx.font=`${12/Math.max(view.k,0.6)}px system-ui,sans-serif`;
    ctx.textAlign="center";ctx.fillText(n.title,n.x,n.y+n.r+12/Math.max(view.k,0.6));
  });
  ctx.globalAlpha=1;
}
function loop(){step();draw();requestAnimationFrame(loop);}loop();

function toWorld(px,py){return{x:(px-W/2-view.x)/view.k,y:(py-H/2-view.y)/view.k};}
function pick(px,py){const p=toWorld(px,py);let best=null,bd=1e9;
  nodes.forEach(n=>{if(!vis(n))return;const d=Math.hypot(n.x-p.x,n.y-p.y);if(d<n.r+4&&d<bd){bd=d;best=n;}});return best;}
cv.addEventListener("pointerdown",e=>{const r=cv.getBoundingClientRect(),px=e.clientX-r.left,py=e.clientY-r.top;
  drag=pick(px,py);moved=false;if(!drag)pan={x:e.clientX-view.x,y:e.clientY-view.y};
  cv.setPointerCapture(e.pointerId);cv.classList.add("dragging");});
cv.addEventListener("pointermove",e=>{const r=cv.getBoundingClientRect(),px=e.clientX-r.left,py=e.clientY-r.top;
  if(drag){const p=toWorld(px,py);drag.x=p.x;drag.y=p.y;drag.vx=drag.vy=0;moved=true;heat=Math.max(heat,0.3);}
  else if(pan){view.x=e.clientX-pan.x;view.y=e.clientY-pan.y;moved=true;}
  else hover=pick(px,py);});
cv.addEventListener("pointerup",e=>{if(!moved){const r=cv.getBoundingClientRect();select(pick(e.clientX-r.left,e.clientY-r.top));}
  drag=null;pan=null;cv.classList.remove("dragging");});
cv.addEventListener("wheel",e=>{e.preventDefault();const r=cv.getBoundingClientRect(),px=e.clientX-r.left-W/2,py=e.clientY-r.top-H/2;
  const k=Math.min(4,Math.max(0.2,view.k*Math.exp(-e.deltaY*0.0015)));
  view.x=px-(px-view.x)*k/view.k;view.y=py-(py-view.y)*k/view.k;view.k=k;},{passive:false});
document.getElementById("q").addEventListener("input",e=>query=e.target.value);

const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function list(arr){return arr.length?"<ul>"+arr.map(n=>`<li><a data-id="${esc(n.id)}">${esc(n.title)}</a> <span class="muted">${esc(TYPE_LABEL[n.type]||n.type)}</span></li>`).join("")+"</ul>":'<div class="muted">（無）</div>';}
function select(n){selected=n;const d=document.getElementById("detail");
  if(!n){d.innerHTML='<span class="muted">點選一個節點查看它的連結。</span>';return;}
  d.innerHTML=`<h2>${esc(n.title)}</h2>
   <div class="muted"><span class="dot" style="background:${color(n.type)}"></span> ${esc(TYPE_LABEL[n.type]||n.type)}・<a class="file" href="../../wiki/${encodeURI(n.id)}" target="_blank">${esc(n.id)}</a></div>
   ${n.tags.length?`<div class="muted">tags：${n.tags.map(esc).join(", ")}</div>`:""}
   ${n.sources.length?`<div class="muted">sources：${n.sources.map(esc).join(", ")}</div>`:""}
   ${n.updated?`<div class="muted">updated：${esc(n.updated)}</div>`:""}
   <p><b>連出（${n.out.length}）</b></p>${list(n.out)}
   <p><b>連入（${n.in.length}）</b></p>${list(n.in)}`;
  d.querySelectorAll("a[data-id]").forEach(a=>a.onclick=()=>{const t=byId[a.dataset.id];select(t);
    view.x=-t.x*view.k;view.y=-t.y*view.k;});
}
</script>
</body>
</html>
"""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="CV Wiki graph")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    root = Path(args.root).resolve()
    data = build(root)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = root / "tools" / "out"
    out.mkdir(parents=True, exist_ok=True)
    (out / "graph.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    print(f"graph.html 已產生：{len(data['nodes'])} 個節點、{len(data['edges'])} 條連結 → {out / 'graph.html'}")


if __name__ == "__main__":
    main()
