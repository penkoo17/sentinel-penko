"""Token desain, CSS, dan JS statis untuk UI Sentinel.

Satu palet dipakai di dua tempat: halaman Streamlit (APP_CSS) dan papan
severity yang di-embed lewat iframe (BOARD_CSS + BOARD_JS).
"""

FONTS_URL = (
    "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600"
    "&family=IBM+Plex+Sans:wght@400;500;600&display=swap"
)

TOKENS = """
--ink:#090c11;--panel:#0e1218;--line:#1a212b;--line-2:#27313e;
--text:#cdd6e0;--muted:#7d8c9f;--dim:#627184;--accent:#8fd3c8;
--critical:#ff6369;--high:#f08a4b;--medium:#e2c044;--low:#5da9f5;
--info:#7d8c9f;--passed:#4cc38a;
--mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
--sans:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
"""

# --------------------------------------------------------------------------
# Halaman Streamlit
# --------------------------------------------------------------------------
_APP_BODY = """
.stApp{background:var(--ink);color:var(--text);font-family:var(--sans)}
::selection{background:rgba(143,211,200,.25)}
[data-testid="stHeader"]{background:transparent}
[data-testid="stDecoration"],footer,#MainMenu{display:none!important}
.block-container,[data-testid="stMainBlockContainer"]{max-width:1180px;padding:2.6rem 1.5rem 4rem}

/* brand */
.sn-top{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin:0 0 1.6rem}
.sn-id{display:flex;align-items:center;gap:10px}
.sn-mark{display:inline-block;width:11px;height:13px;border:1.5px solid var(--accent);border-radius:2px 2px 7px 7px}
.sn-brand{font:600 1.25rem/1 var(--mono);color:var(--text)}
.sn-tag{font:400 .85rem var(--sans);color:var(--muted)}

/* form scan */
[data-testid="stForm"]{border:0;padding:0;background:transparent}
[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stTextInput"] div[data-baseweb="base-input"]{background:var(--panel);border-radius:4px}
[data-testid="stTextInput"] div[data-baseweb="input"]{border:1px solid var(--line-2)}
[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within{border-color:var(--accent);box-shadow:none}
[data-testid="stTextInput"] input{font:400 .9rem var(--mono);color:var(--text);caret-color:var(--accent)}
[data-testid="stTextInput"] input::placeholder{color:var(--dim)}
[data-testid="stCheckbox"] label p{font:400 .82rem var(--mono);color:var(--muted)}
.stButton>button,[data-testid="stFormSubmitButton"]>button{
  min-width:7.5rem;min-height:2.6rem;background:transparent;border:1px solid var(--accent);
  border-radius:4px;transition:background .15s}
.stButton>button,.stButton>button p,[data-testid="stFormSubmitButton"]>button,
[data-testid="stFormSubmitButton"]>button p{color:var(--accent)!important;font:500 .85rem var(--mono)!important}
.stButton>button:hover,[data-testid="stFormSubmitButton"]>button:hover{background:rgba(143,211,200,.09);border-color:var(--accent)}
.stButton>button:focus-visible,[data-testid="stFormSubmitButton"]>button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
[data-testid="stSpinner"] p{font:400 .85rem var(--mono);color:var(--muted)}

/* ringkasan skor */
.sn-sum{display:grid;grid-template-columns:auto 1fr auto;gap:28px;align-items:center;margin:1.6rem 0 1.4rem;
  padding:18px 22px;background:var(--panel);border:1px solid var(--line);border-radius:4px}
.sn-score{display:flex;align-items:baseline;gap:6px;font-family:var(--mono)}
.sn-score .n{font-size:2.9rem;font-weight:600;line-height:1;color:var(--c);font-variant-numeric:tabular-nums}
.sn-score .of{font-size:.85rem;color:var(--dim)}
.sn-verdict{font:500 .85rem var(--mono);color:var(--c);margin-bottom:8px}
.sn-meter{height:3px;background:var(--line);border-radius:2px;overflow:hidden}
.sn-meter i{display:block;height:100%;background:var(--c)}
.sn-target{margin-top:10px;font:400 .82rem var(--mono);color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sn-stats{display:flex;gap:26px;margin:0}
.sn-stats div{text-align:right}
.sn-stats dt{font:400 .75rem var(--sans);color:var(--muted);margin:0}
.sn-stats dd{margin:2px 0 0;font:600 1.3rem var(--mono);color:var(--text)}
@media(max-width:720px){.sn-sum{grid-template-columns:1fr;gap:16px}.sn-stats div{text-align:left}}

/* tab */
[data-baseweb="tab-list"]{gap:1.6rem}
button[data-baseweb="tab"]{background:transparent;padding:.6rem 0;height:auto}
button[data-baseweb="tab"] p{font:500 .85rem var(--mono);color:var(--muted)}
button[data-baseweb="tab"][aria-selected="true"] p{color:var(--text)}
[data-baseweb="tab-highlight"]{background:var(--accent)!important;height:2px!important}
[data-baseweb="tab-border"]{background:var(--line)!important}
[data-baseweb="tab-panel"]{padding-top:1rem}

/* footer */
.sn-footer{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;
  margin-top:3rem;padding-top:1.2rem;border-top:1px solid var(--line);
  font:400 .78rem var(--mono);color:var(--muted)}
.sn-footer-left{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.sn-footer-right{color:var(--dim)}
.sn-footer-name{font-weight:600;color:#ffffff;margin-left:6px}
.sn-badge{display:inline-block;padding:2px 8px;border-radius:10px;font:600 .62rem var(--mono);letter-spacing:.5px}
.sn-badge-creator{background:rgba(76,195,138,.15);color:#4cc38a;border:1px solid rgba(76,195,138,.35)}

/* attack surface */
.surface-wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;margin-top:1rem}
.surface-card{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:16px}
.surface-card h3{margin:0 0 12px;font:600 .95rem var(--mono);color:var(--accent)}
.surface-grid{display:grid;grid-template-columns:120px 1fr;gap:6px 14px;font:400 .82rem var(--mono)}
.surface-k{color:var(--muted)}
.surface-v{color:var(--text);word-break:break-word}
.tech-tag{display:inline-block;padding:2px 8px;margin:2px;background:rgba(143,211,200,.1);
  border:1px solid rgba(143,211,200,.3);border-radius:4px;color:var(--accent);font-size:.72rem}
.port-list{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.port-row{display:flex;gap:8px;padding:4px 10px;background:rgba(76,195,138,.1);
  border:1px solid rgba(76,195,138,.3);border-radius:4px;font:500 .78rem var(--mono);color:var(--accent)}
.port-num{font-weight:700}
.port-svc{color:var(--muted)}

/* notice, hint, endpoint */
.sn-note{margin:1rem 0;padding:.8rem 1rem;border:1px solid var(--line-2);border-left:2px solid var(--c,var(--accent));
  border-radius:4px;background:var(--panel);font-size:.88rem;color:var(--text)}
.sn-note.err{--c:var(--critical)}
.sn-hint{margin-top:1.4rem;padding:1rem 1.1rem;border:1px dashed var(--line-2);border-radius:4px;color:var(--muted);font-size:.85rem}
.sn-cap{margin:.4rem 0 .6rem;font:400 .8rem var(--mono);color:var(--muted)}
.ep{border:1px solid var(--line);border-radius:4px;background:var(--panel);max-height:520px;overflow:auto}
.ep-row{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:14px;align-items:baseline;
  padding:9px 16px;border-top:1px solid var(--line);font:400 .82rem var(--mono)}
.ep-row:first-child{border-top:0}
.ep-row .url{color:var(--text);overflow-wrap:anywhere}
.ep-row .ct{color:var(--dim)}
.code.ok{color:var(--passed)}.code.redir{color:var(--medium)}.code.bad{color:var(--critical)}
"""

APP_CSS = (
    f"@import url('{FONTS_URL}');\n:root{{{TOKENS}}}\n" + _APP_BODY
)

# --------------------------------------------------------------------------
# Papan severity (di dalam iframe)
# --------------------------------------------------------------------------
BOARD_CSS = (
    ":root{" + TOKENS + "}"
    + """
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--ink);color:var(--text);font:13px/1.5 var(--sans);color-scheme:dark}
.wrap{display:flex;flex-direction:column;height:100%}
.bar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:2px 0 12px}
.tabs{display:flex;gap:6px;min-width:0;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{flex:none;appearance:none;background:transparent;display:inline-flex;align-items:center;gap:8px;padding:7px 11px;
  border:1px solid var(--line);border-radius:4px;font:500 12px/1 var(--mono);color:var(--muted);cursor:pointer;
  transition:border-color .15s,color .15s}
.tab .d{width:7px;height:7px;border-radius:50%;background:var(--c)}
.tab b{font-weight:600;color:var(--text)}
.tab:hover{border-color:var(--line-2);color:var(--text)}
.tab[aria-selected=true]{border-color:var(--c);color:var(--text)}
.tab.off{cursor:default;opacity:.45;pointer-events:none}
.tab.off .d{background:transparent;border:1px solid var(--dim)}
.nav{display:flex;gap:6px;flex:none}
.nav[hidden]{display:none}
.nav button{appearance:none;width:30px;height:28px;border:1px solid var(--line);border-radius:4px;
  background:transparent;color:var(--muted);font:500 15px/1 var(--mono);cursor:pointer}
.nav button:hover:not(:disabled){border-color:var(--line-2);color:var(--text)}
.nav button:disabled{opacity:.3;cursor:default}
.tab:focus-visible,.nav button:focus-visible,.track:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.track{position:relative;flex:1;min-height:0;display:flex;gap:14px;align-items:flex-start;
  overflow-x:auto;overflow-y:hidden;padding-bottom:12px;scrollbar-width:thin;scrollbar-color:var(--line-2) transparent}
.track::-webkit-scrollbar{height:6px}
.track::-webkit-scrollbar-thumb{background:var(--line-2);border-radius:3px}
@media (pointer:coarse){.track{scroll-snap-type:x mandatory}.nav{display:none}}
.track.drag{scroll-snap-type:none}

.lane{flex:1 0 min(420px,88%);max-width:560px;max-height:100%;display:flex;flex-direction:column;
  background:var(--panel);border:1px solid var(--line);border-top:2px solid var(--c);border-radius:4px;
  scroll-snap-align:start;transition:box-shadow .2s}
.lane.hl{box-shadow:0 0 0 1px var(--c)}
.lane>header{display:flex;align-items:baseline;justify-content:space-between;padding:12px 16px;
  font:500 13px/1 var(--mono);color:var(--c);cursor:grab;user-select:none}
.track.drag .lane>header{cursor:grabbing}
.lane>header span{color:var(--muted)}
.body{overflow-y:auto;min-height:0;scrollbar-width:thin;scrollbar-color:var(--line-2) transparent}
.item{padding:14px 16px;border-top:1px solid var(--line)}
.top{display:flex;align-items:flex-start;gap:10px;min-width:0}
.st{flex:none;margin-top:1px;font:500 11px/1 var(--mono);padding:3px 6px;border:1px solid var(--line-2);border-radius:3px;color:var(--muted)}
.st.fail{color:var(--text)}
.st.pass{color:var(--passed);border-color:rgba(76,195,138,.35)}
.top h3{margin:0;font:500 14px/1.4 var(--sans);color:var(--text);min-width:0;overflow-wrap:anywhere}
.fid{margin-left:auto;padding-left:8px;flex:none;max-width:36%;font:400 11px/1.9 var(--mono);color:var(--dim);
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.detail{margin:8px 0 0;color:var(--muted);overflow-wrap:anywhere}
.fix{margin:8px 0 0;display:flex;gap:10px;color:#aab8c7;overflow-wrap:anywhere}
.fix i{flex:none;font:500 11px/1.9 var(--mono);color:var(--accent);font-style:normal}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""
)

BOARD_JS = """
(()=>{
const track=document.getElementById('track');
const lanes=[...track.querySelectorAll('.lane')];
const tabs=[...document.querySelectorAll('.tab[data-i]')];
const prev=document.getElementById('prev'),next=document.getElementById('next');
const nav=document.querySelector('.nav');
const beh=matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth';
const GAP=14;
let pin=null;
const unpin=()=>{pin=null};
const step=()=>(lanes[0]?lanes[0].offsetWidth:300)+GAP;
const go=x=>track.scrollTo({left:x,behavior:beh});

function sync(){
  const max=track.scrollWidth-track.clientWidth;
  const scrolls=max>2;
  nav.hidden=!scrolls;
  prev.disabled=track.scrollLeft<=2;
  next.disabled=track.scrollLeft>=max-2;
  let a=-1;
  if(scrolls){
    a=0;
    if(pin!==null)a=pin;
    else if(track.scrollLeft>=max-2)a=lanes.length-1;
    else lanes.forEach((l,i)=>{if(l.offsetLeft-track.scrollLeft<=lanes[0].offsetWidth*.4)a=i});
  }
  tabs.forEach(t=>t.setAttribute('aria-selected',String(+t.dataset.i===a)));
}

tabs.forEach(t=>t.addEventListener('click',()=>{
  const l=lanes[+t.dataset.i];
  pin=+t.dataset.i;
  go(l.offsetLeft);sync();
  l.classList.add('hl');setTimeout(()=>l.classList.remove('hl'),900);
}));
prev.addEventListener('click',()=>{unpin();go(track.scrollLeft-step())});
next.addEventListener('click',()=>{unpin();go(track.scrollLeft+step())});
track.addEventListener('keydown',e=>{
  unpin();
  if(e.key==='ArrowRight'){e.preventDefault();go(track.scrollLeft+step())}
  if(e.key==='ArrowLeft'){e.preventDefault();go(track.scrollLeft-step())}
});

let drag=null;
track.addEventListener('pointerdown',e=>{
  unpin();
  if(e.pointerType!=='mouse'||e.button!==0)return;
  if(!(e.target===track||e.target.closest('.lane>header')))return;
  drag={x:e.clientX,l:track.scrollLeft};
  track.setPointerCapture(e.pointerId);track.classList.add('drag');
});
track.addEventListener('pointermove',e=>{if(drag)track.scrollLeft=drag.l-(e.clientX-drag.x)});
const end=()=>{drag=null;track.classList.remove('drag')};
track.addEventListener('pointerup',end);
track.addEventListener('pointercancel',end);

track.addEventListener('wheel',unpin,{passive:true});
track.addEventListener('touchstart',unpin,{passive:true});
let raf=0;
track.addEventListener('scroll',()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(sync)},{passive:true});
addEventListener('resize',sync);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(sync);
sync();
})();
"""
