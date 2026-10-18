"""Build tech-tree.html and tree/<id>.html (plus index-demo.html with --home-demo) from index.html's shared shell.
Run from the repo root: python3 tools/tech-tree/build.py. Content lives in nodes.py next to this file.
Leaves index.html untouched."""
import base64
import html
import json
import mimetypes
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "nodes.py"), encoding="utf-8").read())  # defines NODES
BRANCHES = {"eng": ("Engineering", "var(--violet)"), "sci": ("Science", "var(--periwinkle)"),
            "sport": ("Sport", "var(--red)"), "vol": ("Volunteer", "var(--teal)"), "arts": ("Arts", "var(--orange)")}

src = open("index.html", encoding="utf-8").read()
style_end = src.index("</style>")
head = src[:style_end]
nav = src[src.index("<nav"):src.index("</nav>") + len("</nav>")]
foot = src[src.index("<footer>"):]
avatar = re.search(r'<div class="avatar"><img src="([^"]+)"', src).group(1)

HOME = "index-demo.html" if "--home-demo" in sys.argv else "index.html"
TABS = ('<a href="' + HOME + '" class="{h}">Home</a><a href="projects.html" class="">Projects</a>'
        '<a href="tech-tree.html" class="{t}">Tech Tree</a><a href="writing.html" class="">Writing</a>'
        '<a href="gallery.html" class="">Gallery</a><a href="https://shop.tombannerman.com" class="">Store</a>')
old_tabs = re.search(r'<div class="tabs" id="tabs">.*?</div>', nav).group(0)


def page(title, desc, css, body, js, active, prefix=""):
    h = head.replace(re.search(r"<title>.*?</title>", head).group(0), f"<title>{title}</title>")
    h = h.replace(re.search(r'<meta name="description" content="[^"]*">', h).group(0),
                  f'<meta name="description" content="{desc}">')
    n = nav.replace(old_tabs, '<div class="tabs" id="tabs">' + TABS.format(
        h="active" if active == "home" else "", t="active" if active == "tree" else "") + "</div>")
    n = n.replace('href="index.html" class="mark"', f'href="{HOME}" class="mark"')
    f = foot.replace("</body>", f"<script>{js}</script>\n</body>") if js else foot
    if prefix:  # pages in a subfolder: point the shared nav and footer links back up
        rel = lambda m: f'href="{prefix}{m.group(1)}"'
        n = re.sub(r'href="(?!https?:|mailto:|#)([^"]+)"', rel, n)
        f = re.sub(r'href="(?!https?:|mailto:|#)([^"]+)"', rel, f)
    return f"{h}\n{css}\n</style></head><body>\n{n}\n{body}\n{f}"


# ---------------------------------------------------------------- tech tree
TREE_CSS = r"""
/* DEMO: tech tree */
.tt-wrap{max-width:var(--w-wide);margin:0 auto;padding:0 24px}
.tt-intro{padding:46px 0 10px;max-width:var(--w)}
.tt-intro .lead{color:var(--ink-soft);max-width:58ch;margin:0 0 18px}
.tt-legend{display:flex;flex-wrap:wrap;gap:16px;font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.5px;color:var(--ink-soft);text-transform:uppercase}
.tt-legend span{display:inline-flex;align-items:center;gap:7px}
.tt-legend i{display:inline-block;width:18px;height:12px;border-radius:4px;border:1.5px solid var(--ink)}
.tt-legend i.h{border:2px solid transparent;background:linear-gradient(var(--paper),var(--paper)) padding-box,conic-gradient(from 210deg,var(--violet),var(--red),var(--orange),var(--periwinkle),var(--violet)) border-box}
.tt-legend i.l{border-style:dashed;border-color:var(--ink-soft)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 8px}
.chip{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;cursor:pointer;
  border:1.5px solid var(--ink);background:none;color:var(--ink);padding:7px 14px;border-radius:30px;transition:.2s}
.chip .ct{opacity:.6;margin-left:6px}
.chip:hover{transform:translateY(-2px)}
.chip.on{background:var(--c,var(--ink));border-color:var(--c,var(--ink));color:#fff}
.tt-stage{display:grid;grid-template-columns:1fr 290px;gap:28px;align-items:start;padding:10px 0 40px}
.tree{position:relative;display:grid;grid-template-columns:repeat(var(--cols),minmax(0,1fr));column-gap:12px}
.tree svg{position:absolute;inset:0;pointer-events:none;overflow:visible}
.tree path{fill:none;stroke-width:2;opacity:.55;transition:opacity .3s}
.tree path.dim{opacity:.1}
.cell{grid-column:var(--col);grid-row:var(--r);display:flex;flex-direction:column;align-items:center;gap:10px;padding:14px 0;position:relative;z-index:1;transition:opacity .3s}
.cell.dim{opacity:.28}
.root{grid-column:1/-1;padding:22px 0 0}
.root .me{width:78px;height:78px;border-radius:50%;padding:4px;
  background:conic-gradient(from 210deg,var(--violet),var(--red),var(--orange),var(--periwinkle),var(--violet));box-shadow:4px 6px 0 rgba(42,23,51,.12)}
.root .me img{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid var(--paper);display:block}
.bh .bname{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#fff;
  background:var(--c);padding:5px 12px;border-radius:30px;white-space:nowrap}
.node{font:inherit;text-align:left;cursor:pointer;width:100%;max-width:178px;background:var(--paper);color:var(--ink);
  border:1.5px solid var(--ink);border-radius:12px;padding:9px 11px 10px;box-shadow:3px 4px 0 rgba(42,23,51,.1);
  transition:transform .2s,box-shadow .2s,background .2s;position:relative}
.node:hover,.node:focus-visible{transform:translateY(-3px);box-shadow:4px 7px 0 rgba(42,23,51,.14);outline:none}
.node::before{content:"";position:absolute;left:-1.5px;top:12px;bottom:12px;width:4px;border-radius:0 4px 4px 0;background:var(--c)}
.node.hard{border:2.5px solid transparent;
  background:linear-gradient(var(--paper),var(--paper)) padding-box,conic-gradient(from 210deg,var(--violet),var(--red),var(--orange),var(--periwinkle),var(--violet)) border-box}
.node.todo{border-style:dashed;border-color:var(--ink-soft);box-shadow:none;background:var(--paper);color:var(--ink-soft)}
.node.todo::before{display:none}
.node.sel{background:var(--c);color:#fff;border-color:var(--c)}
.node.sel .n-when{color:rgba(255,255,255,.8)}
.n-when{display:block;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:.5px;text-transform:uppercase;color:var(--ink-soft)}
.n-title{display:block;font-family:"Fraunces",serif;font-weight:600;font-variation-settings:"opsz" 30,"SOFT" 30;font-size:15px;line-height:1.15;margin-top:2px}
.detail{position:sticky;top:80px;border:1.5px solid var(--ink);border-radius:16px;background:var(--paper-deep);padding:22px 22px 24px}
.detail .eyebrow{color:var(--c,var(--violet))}
.detail h3{font-family:"Fraunces",serif;font-weight:600;font-variation-settings:"opsz" 60,"SOFT" 30;font-size:24px;line-height:1.1;margin:0 0 4px}
.detail .d-when{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.5px;text-transform:uppercase;color:var(--ink-soft);margin:0 0 12px}
.detail p{font-size:15px;margin:0 0 12px}
.detail .tag{display:inline-block;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;
  color:#fff;background:var(--ink);padding:3px 9px;border-radius:20px;margin:0 6px 10px 0}
.detail .tag.h{background:linear-gradient(90deg,var(--violet),var(--red),var(--orange))}
.detail .needs{font-size:13px;color:var(--ink-soft)}
.detail .close{display:none}
.mini{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 14px}
.mini div{border-top:1.5px solid var(--c,var(--ink));padding-top:6px}
.mini dt{font-family:"Space Mono",monospace;font-size:9.5px;letter-spacing:.5px;text-transform:uppercase;color:var(--ink-soft)}
.mini dd{margin:2px 0 0;font-family:"Fraunces",serif;font-weight:600;font-size:15px;line-height:1.15}
.story-link{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase}
@media (max-width:820px){
  .tt-stage{grid-template-columns:1fr}
  .tree{grid-template-columns:1fr}
  .cell{grid-column:1;grid-row:var(--mr)}
  .cell.blank,.cell.off,.root{display:none}
  .cell.dim{opacity:1}
  .node{max-width:340px}
  .detail{position:fixed;left:12px;right:12px;bottom:12px;top:auto;z-index:30;max-height:70vh;overflow:auto;
    transform:translateY(120%);transition:transform .3s ease;box-shadow:0 -6px 30px rgba(42,23,51,.2)}
  .detail.open{transform:none}
  .detail .close{display:block;position:absolute;top:10px;right:12px;background:none;border:0;font-size:22px;cursor:pointer;color:var(--ink)}
}
@media (prefers-reduced-motion:reduce){.node,.chip,.detail,.cell,.tree path{transition:none}}
"""

TREE_BODY = f"""
<!-- DEMO for review: the tree data lives in the N array in the script at the bottom. -->
<div class="tt-wrap">
  <section class="tt-intro reveal" style="padding-bottom:0">
    <p class="eyebrow">Tech tree</p>
    <h2>Things I've unlocked</h2>
    <p class="lead">Like the tech tree in a strategy game: each thing I've learned or survived opened up the next one. The newest are at the top; pick one to see the story behind it.</p>
    <div class="tt-legend"><span><i></i>Unlocked</span><span><i class="h"></i>Hard mode</span><span><i class="l"></i>Still to fill in</span><span id="tt-count"></span></div>
  </section>
  <div class="chips" id="chips" role="toolbar" aria-label="Filter branches"></div>
  <div class="tt-stage">
    <div class="tree" id="tree"><svg id="wires" aria-hidden="true"></svg></div>
    <aside class="detail" id="detail" aria-live="polite">
      <button class="close" id="close" aria-label="Close">&times;</button>
      <p class="eyebrow">How it works</p>
      <h3>Pick a node</h3>
      <p>The most recent things sit at the top of each branch. Follow the lines down to see what they grew out of, all the way to the roots, including where one branch fed another.</p>
      <p class="needs">Gradient rings mark the hard-mode unlocks.</p>
    </aside>
  </div>
</div>
""".replace("{AVATAR}", avatar)

TREE_JS = r"""
const BR=[
  {id:'eng',name:'Engineering',c:'var(--violet)'},
  {id:'sci',name:'Science',c:'var(--periwinkle)'},
  {id:'sport',name:'Sport',c:'var(--red)'},
  {id:'vol',name:'Volunteer',c:'var(--teal)'},
  {id:'arts',name:'Arts',c:'var(--orange)'}
];
// node data comes from nodes.py (also used for the tree/<id>.html articles)
const N=__NODES__;

const tree=document.getElementById('tree'),wires=document.getElementById('wires'),detail=document.getElementById('detail');
const byId=Object.fromEntries(N.map(n=>[n.id,n])),brOf=Object.fromEntries(BR.map(b=>[b.id,b]));
const maxT=Math.max(...N.map(n=>n.t));
const mq=matchMedia('(max-width:820px)');
let sel='all',picked=null;
tree.style.setProperty('--cols',BR.length);

// newest first: end year from `when` ("2018–23" → 2023); ongoing work sorts to the top, unknown dates keep source order
const yr=n=>{
  if(/now|ongoing|daily|open/i.test(n.when))return 9999;
  const m=n.when.match(/(\d{4})(?:\s*[–-]\s*(\d{2,4}))?/);if(!m)return 0;
  return +(m[2]?(m[2].length===2?m[1].slice(0,2)+m[2]:m[2]):m[1]);
};

// branch headers on top, each branch's highest tier directly under its header, roots (me) at the bottom
const root=document.createElement('div');root.className='cell root';root.dataset.k='root';
root.style.setProperty('--r',maxT+2);
root.innerHTML='<div class="me"><img src="{AVATAR}" alt="Tom"></div>';tree.appendChild(root);
const cells={};
let off=0;  // mobile: branches stack one after another
BR.forEach((b,bi)=>{
  const bmax=Math.max(...N.filter(n=>n.b===b.id).map(n=>n.t));
  const h=document.createElement('div');h.className='cell bh';h.dataset.b=b.id;
  h.style.cssText=`--col:${bi+1};--r:1;--mr:${off+1};--c:${b.c}`;
  h.innerHTML=`<span class="bname">${b.name}</span>`;tree.appendChild(h);cells[b.id+'h']=h;
  for(let t=bmax;t>=1;t--){
    const c=document.createElement('div');c.className='cell';c.dataset.b=b.id;
    c.style.cssText=`--col:${bi+1};--r:${bmax-t+2};--mr:${off+bmax-t+2}`;
    const ns=N.filter(n=>n.b===b.id&&n.t===t).sort((p,q)=>yr(q)-yr(p));
    if(!ns.length)c.classList.add('blank');
    ns.forEach(n=>{
      const el=document.createElement('button');
      el.className='node'+(n.hard?' hard':'')+(n.todo?' todo':'');el.dataset.id=n.id;el.style.setProperty('--c',b.c);
      el.innerHTML=`<span class="n-when">${n.when}</span><span class="n-title">${n.title}</span>`;
      el.addEventListener('click',()=>pick(n.id));
      c.appendChild(el);
    });
    tree.appendChild(c);
  }
  off+=bmax+1;
});

// edges run from the older thing (below) up to what it unlocked: root → nodes without in-branch parents; then every req
const edges=[];
N.forEach(n=>{
  const c=brOf[n.b].c,req=n.req||[];
  if(!req.some(r=>byId[r].b===n.b))edges.push(['root',n.id,c]);
  req.forEach(r=>edges.push([r,n.id,brOf[byId[r].b].c]));
});
const elOf=k=>k==='root'?root.firstElementChild:tree.querySelector(`[data-id="${k}"]`);
const branchOf=k=>k==='root'?null:byId[k].b;

function draw(){
  const box=tree.getBoundingClientRect();
  wires.setAttribute('viewBox',`0 0 ${box.width} ${box.height}`);
  wires.innerHTML=edges.map(([a,b,c])=>{
    const ea=elOf(a),eb=elOf(b),ba=branchOf(a),bb=branchOf(b);
    if(!ea.offsetParent||!eb.offsetParent)return '';
    if(mq.matches&&ba!==bb)return '';  // stacked on phones: cross-branch lines would cut through other branches
    const ra=ea.getBoundingClientRect(),rb=eb.getBoundingClientRect();
    const dim=sel!=='all'&&ba!==sel&&bb!==sel;
    let d;
    if(a==='root'){  // roots: curve out along the bottom, then straight up the branch's own column
      const x1=ra.left-box.left+ra.width/2,y1=ra.top-box.top,x2=rb.left-box.left+rb.width/2,y2=rb.bottom-box.top,yb=Math.max(y2,y1-70);
      d=`M${x1},${y1} C${x1},${y1-35} ${x2},${y1-30} ${x2},${yb} L${x2},${y2}`;
    }else if(rb.bottom<ra.top-4){  // child sits above: vertical S-curve
      const x1=ra.left-box.left+ra.width/2,y1=ra.top-box.top,x2=rb.left-box.left+rb.width/2,y2=rb.bottom-box.top,my=(y1+y2)/2;
      d=`M${x1},${y1} C${x1},${my} ${x2},${my} ${x2},${y2}`;
    }else{  // side by side (cross-branch at a similar height): horizontal S-curve between facing edges
      const right=rb.left>ra.left;
      const x1=(right?ra.right:ra.left)-box.left,y1=ra.top-box.top+ra.height/2,x2=(right?rb.left:rb.right)-box.left,y2=rb.top-box.top+rb.height/2,mx=(x1+x2)/2;
      d=`M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`;
    }
    return `<path class="${dim?'dim':''}" stroke="${c}" d="${d}"/>`;
  }).join('');
}

function filter(id){
  sel=id;
  document.querySelectorAll('.chip').forEach(ch=>ch.classList.toggle('on',ch.dataset.b===id));
  tree.querySelectorAll('.cell[data-b]').forEach(c=>{
    const other=id!=='all'&&c.dataset.b!==id;
    c.classList.toggle('dim',other);c.classList.toggle('off',other);
  });
  draw();
}

function pick(id){
  const n=byId[id],b=brOf[n.b];picked=id;
  tree.querySelectorAll('.node').forEach(el=>el.classList.toggle('sel',el.dataset.id===id));
  const req=(n.req||[]).map(r=>byId[r].title);
  const unlocks=N.filter(m=>(m.req||[]).includes(id)).map(m=>m.title);
  detail.style.setProperty('--c',b.c);
  detail.innerHTML=`<button class="close" id="close" aria-label="Close">&times;</button>
    <p class="eyebrow">${b.name}</p><h3>${n.title}</h3><p class="d-when">${n.when}</p>
    ${n.hard?'<span class="tag h">Hard mode</span>':''}${n.todo?'<span class="tag">To fill in</span>':''}
    <p>${n.text}</p>
    ${(n.stats||[]).length?`<dl class="mini">${n.stats.slice(0,3).map(([k,v])=>`<div><dt>${k}</dt><dd>${v??'TBC'}</dd></div>`).join('')}</dl>`:''}
    ${req.length?`<p class="needs">Unlocked by: ${req.join(', ')}</p>`:''}
    ${unlocks.length?`<p class="needs">Led to: ${unlocks.join(', ')}</p>`:''}
    <p><a class="story-link" href="tree/${n.id}.html">Read the story &rarr;</a></p>`;
  detail.querySelector('#close').addEventListener('click',()=>detail.classList.remove('open'));
  detail.classList.add('open');
}

const chips=document.getElementById('chips');
[{id:'all',name:'All',c:'var(--ink)'},...BR].forEach(b=>{
  const ch=document.createElement('button');ch.className='chip';ch.dataset.b=b.id;ch.style.setProperty('--c',b.c);
  const k=b.id==='all'?N.length:N.filter(n=>n.b===b.id).length;
  ch.innerHTML=`${b.name}<span class="ct">${k}</span>`;
  ch.addEventListener('click',()=>filter(b.id));chips.appendChild(ch);
});
document.getElementById('close').addEventListener('click',()=>detail.classList.remove('open'));
document.getElementById('tt-count').textContent=`${N.filter(n=>!n.todo).length} unlocked · ${N.filter(n=>n.hard).length} hard mode`;
filter('all');
addEventListener('resize',draw);
const h=decodeURIComponent(location.hash.slice(1));
if(byId[h]){pick(h);elOf(h).scrollIntoView({block:'center'});}
if(document.fonts)document.fonts.ready.then(draw);
""".replace("{AVATAR}", avatar).replace("__NODES__", json.dumps(
    [{k: n[k] for k in ("id", "b", "t", "title", "when", "req", "hard", "todo", "text", "stats") if k in n} for n in NODES],
    ensure_ascii=False))

open("tech-tree.html", "w", encoding="utf-8").write(page(
    "Tech Tree — Tom Bannerman",
    "Tom Bannerman's tech tree: engineering, science, sport, volunteering and the arts, and how each one led to the next.",
    TREE_CSS, TREE_BODY, TREE_JS, "tree"))

# ---------------------------------------------------------------- tree/<id>.html articles
ART_CSS = r"""
/* tech tree article */
.art{max-width:var(--w);margin:0 auto;padding:34px 24px 20px}
.back{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft)}
.back:hover{color:var(--c)}
.art .eyebrow{color:var(--c);margin-top:26px}
.art h1{font-family:"Fraunces",serif;font-weight:600;font-variation-settings:"opsz" 144,"SOFT" 40,"WONK" 1;
  font-size:clamp(34px,6vw,54px);line-height:1;letter-spacing:-.02em;margin:0 0 10px}
.art .when{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.5px;text-transform:uppercase;color:var(--ink-soft);margin:0}
.tag{display:inline-block;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;
  color:#fff;background:var(--ink);padding:3px 9px;border-radius:20px;margin-left:10px;vertical-align:middle}
.tag.h{background:linear-gradient(90deg,var(--violet),var(--red),var(--orange))}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:28px 0}
.stat{border:1.5px solid var(--ink);border-radius:14px;padding:14px 16px 12px;background:var(--paper);box-shadow:3px 4px 0 rgba(42,23,51,.08);border-top:5px solid var(--c)}
.stat .v{font-family:"Fraunces",serif;font-weight:600;font-variation-settings:"opsz" 60,"SOFT" 30;font-size:26px;line-height:1.1}
.stat .k{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.5px;text-transform:uppercase;color:var(--ink-soft);margin-top:6px}
.stat.tbc .v{color:var(--ink-soft);font-weight:400}
.hero{margin:0 0 28px;border-radius:18px;overflow:hidden;border:1.5px solid var(--ink)}
.hero img{width:100%;display:block}
.hero figcaption,.photos figcaption{font-family:"Space Mono",monospace;font-size:11px;color:var(--ink-soft);padding:8px 12px}
.ph{border:1.5px dashed var(--ink-soft);border-radius:18px;padding:46px 20px;text-align:center;margin:0 0 28px;
  font-family:"Space Mono",monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft)}
.story p{font-size:18px;line-height:1.75;margin:0 0 18px}
.todo-box{border:1.5px dashed var(--ink-soft);border-radius:14px;padding:18px 20px;color:var(--ink-soft);font-size:15px;margin:0 0 18px}
.photos{column-count:2;column-gap:12px;margin:10px 0 18px}
.photos figure{break-inside:avoid;margin:0 0 12px;border-radius:14px;overflow:hidden;border:1px solid var(--line)}
.photos img{width:100%;display:block}
.rel{display:flex;flex-direction:column;gap:6px;margin:30px 0 0;padding-top:20px;border-top:1px solid var(--line)}
.rel p{margin:0;font-family:"Space Mono",monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--ink-soft)}
.rel .row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.rel a{font-family:"Fraunces",serif;font-weight:600;font-size:16px;color:var(--ink);border:1.5px solid var(--ink);border-radius:30px;padding:6px 14px 6px 12px;border-left:5px solid var(--rc)}
.rel a:hover{background:var(--ink);color:var(--paper)}
@media (max-width:520px){.photos{column-count:1}.stats{grid-template-columns:1fr 1fr}}
"""


def img_src(src):
    """Photos may be data URIs, URLs, or paths relative to this folder (embedded inline, as the site does)."""
    if src.startswith(("data:", "http")):
        return src
    path = os.path.join(HERE, src)
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


by_id = {n["id"]: n for n in NODES}
os.makedirs("tree", exist_ok=True)
for n in NODES:
    e = html.escape
    name, colour = BRANCHES[n["b"]]
    stats = "".join(
        f'<div class="stat{"" if v is not None else " tbc"}"><div class="v">{e(v) if v is not None else "TBC"}</div><div class="k">{e(k)}</div></div>'
        for k, v in n.get("stats", []))
    photos = n.get("photos", [])
    fig = lambda p: f'<figure><img src="{img_src(p["src"])}" alt="{e(p.get("cap", n["title"]))}" loading="lazy">' + (
        f'<figcaption>{e(p["cap"])}</figcaption>' if p.get("cap") else "") + "</figure>"
    hero = (f'<figure class="hero">{fig(photos[0])[8:]}' if photos else '<div class="ph">Photos coming soon</div>')
    story = "".join(f"<p>{e(para)}</p>" for para in n.get("story", [])) or '<div class="todo-box">The story for this one is still to be written.</div>'
    rest = f'<div class="photos">{"".join(fig(p) for p in photos[1:])}</div>' if len(photos) > 1 else ""
    chip = lambda m: f'<a href="{m["id"]}.html" style="--rc:{BRANCHES[m["b"]][1]}">{e(m["title"])}</a>'
    grew = [by_id[r] for r in n.get("req", [])]
    led = [m for m in NODES if n["id"] in m.get("req", [])]
    rel = ""
    if grew:
        rel += f'<p>Grew out of</p><div class="row">{"".join(chip(m) for m in grew)}</div>'
    if led:
        rel += f'<p>Led to</p><div class="row">{"".join(chip(m) for m in led)}</div>'
    more = ""
    if n.get("link"):
        href = n["link"] if n["link"].startswith("http") else "../" + n["link"]
        more = f'<p><a class="back" href="{href}">More on this &rarr;</a></p>'
    body = f"""
<article class="art reveal" style="--c:{colour}">
  <a class="back" href="../tech-tree.html#{n['id']}">&larr; Tech tree</a>
  <p class="eyebrow">{name}</p>
  <h1>{e(n['title'])}</h1>
  <p class="when">{e(n['when'])}{'<span class="tag h">Hard mode</span>' if n.get('hard') else ''}</p>
  {f'<div class="stats">{stats}</div>' if stats else '<div style="height:26px"></div>'}
  {hero}
  <div class="story">{story}</div>
  {rest}
  {more}
  {f'<nav class="rel" aria-label="Related">{rel}</nav>' if rel else ''}
</article>
"""
    open(f"tree/{n['id']}.html", "w", encoding="utf-8").write(page(
        f"{n['title']} — Tom Bannerman", e(n["text"]), ART_CSS, body, "", "tree", prefix="../"))
print(f"built {len(NODES)} articles in tree/")

# ---------------------------------------------------------------- home demo (review only)
if "--home-demo" not in sys.argv:
    print("built tech-tree.html")
    sys.exit(0)
HOME_CSS = r"""
/* DEMO: warmer home */
.home-hero h1 .wave{display:inline-block;transform-origin:70% 70%;animation:wave 2.4s ease-in-out 1s 2}
@keyframes wave{0%,60%,100%{transform:rotate(0)}10%,30%{transform:rotate(14deg)}20%{transform:rotate(-8deg)}40%{transform:rotate(-4deg)}50%{transform:rotate(10deg)}}
@media (prefers-reduced-motion:reduce){.home-hero h1 .wave{animation:none}}
.links a.primary{background:var(--ink);color:var(--paper)}
.links a.primary:hover{background:var(--violet);border-color:var(--violet)}
.now{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.now-card{border:1.5px solid var(--ink);border-radius:16px;padding:18px 18px 16px;background:var(--paper);box-shadow:4px 5px 0 rgba(42,23,51,.08)}
.now-card .k{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--c);margin:0 0 6px}
.now-card p{margin:0;font-size:15px}
.belief{border-left:4px solid var(--violet);padding:4px 0 4px 20px;margin:0}
.belief p{font-family:"Fraunces",serif;font-weight:400;font-variation-settings:"opsz" 40,"SOFT" 60;font-size:21px;line-height:1.45;margin:0}
@media (max-width:640px){.now{grid-template-columns:1fr}}
"""

HOME_BODY = f"""
<!-- DEMO for review: a warmer take on index.html. The timeline moved to tech-tree.html. -->
<header class="wrap"><div class="home-hero">
  <div class="avatar"><img src="{avatar}" alt="Tom Bannerman"></div>
  <div class="bio">
    <h1>Hi, I'm <span class="b">Tom</span> <span class="wave" aria-hidden="true">👋</span></h1>
    <p>I'm an aerospace engineer on the Gold Coast, helping build rockets at Gilmour Space. When I'm not at work you'll probably find me out on a run, in the ocean, or behind a camera.</p>
    <p class="stars">This site is a bit of everything: things I've built, photos I've taken, and notes on whatever rabbit hole I'm down at the moment. Have a wander, and say hi if something sparks a thought.</p>
    <div class="links">
      <a class="primary" href="mailto:tban4122@gmail.com">Say hello</a>
      <a href="tech-tree.html">What I've been up to</a>
    </div>
  </div>
</div></header>

<section class="wrap reveal" style="padding-top:40px">
  <p class="eyebrow">Right now</p>
  <div class="now">
    <div class="now-card" style="--c:var(--violet)"><p class="k">At work</p><p>Launch-vehicle structures at Gilmour Space: fins, bolted joints and pressure vessels.</p></div>
    <div class="now-card" style="--c:var(--red)"><p class="k">Outside</p><p>Running, triathlons, and time in the surf with the surf club.</p></div>
    <div class="now-card" style="--c:var(--teal)"><p class="k">On my mind</p><p>How fast AI is moving. I keep a <a href="ai-dashboard/">daily tracker</a> of it.</p></div>
  </div>
</section>

<section class="wrap reveal">
  <p class="eyebrow">What I care about</p>
  <blockquote class="belief"><p>I believe our future is in space 🚀, and that intelligent systems can speed up our expansion through the solar system and, one day, to another star.</p></blockquote>
</section>

<section class="wrap reveal">
  <p class="eyebrow">Have a look around</p>
  <ul class="explore">
    <li><a class="e-link" href="tech-tree.html">Tech Tree <span class="arrow">&rarr;</span></a><span class="note">everything I've unlocked so far</span></li>
    <li><a class="e-link" href="projects.html">Projects <span class="arrow">&rarr;</span></a><span class="note">things I've built · 2016&ndash;2024</span></li>
    <li><a class="e-link" href="writing.html">Writing <span class="arrow">&rarr;</span></a><span class="note">engineering, film, AI, rabbit holes</span></li>
    <li><a class="e-link" href="https://shop.tombannerman.com">Store <span class="arrow">&rarr;</span></a><span class="note">prints &amp; merch</span></li>
  </ul>
</section>

<section class="wrap reveal">
  <p class="eyebrow">Things I love</p>
  <ul class="plist">
    <li><span class="dot" style="background:var(--violet)"></span><b>Running</b><span>Chasing the next PB on the road.</span></li>
    <li><span class="dot" style="background:var(--periwinkle)"></span><b>Triathlons</b><span>Swim, bike, run &mdash; one finish line.</span></li>
    <li><span class="dot" style="background:var(--red)"></span><b>Photography</b><span>Skies, oceans, edges of the day.</span></li>
    <li><span class="dot" style="background:var(--teal)"></span><b>Diving</b><span>SCUBA &amp; freediving; the quiet world below.</span></li>
    <li><span class="dot" style="background:var(--orange)"></span><b>Adventures</b><span>Mountains, via ferrata, the long way round.</span></li>
  </ul>
</section>
"""

open("index-demo.html", "w", encoding="utf-8").write(page(
    "Tom Bannerman",
    "Hi, I'm Tom: an aerospace engineer on the Gold Coast. Things I've built, photos I've taken, and notes on whatever I'm curious about.",
    HOME_CSS, HOME_BODY, "", "home"))
print("built tech-tree.html and index-demo.html")
