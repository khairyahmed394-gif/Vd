import json,asyncio,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
LOGO=open(f"{HERE}/logo_vec.json").read()
C=[ # name, theme, kicker, lines[(text,color-key)], sub, visual, rtl
dict(n="clinstat_motion",dark=1,kick="CLINICAL  ·  BIOSTATISTICS  ·  GULF",lines=[("DATA","pale"),("INTEGRITY","pale"),("ACCELERATED","gold"),("TRIALS","gold")],sub="Editors screen your manuscript in minutes.",vis=("chips",["BEFORE PEER REVIEW","SURVIVAL ANALYSIS"])),
dict(n="clinstat_3factors",dark=0,kick="CLINSTAT RESEARCH INSTITUTE",lines=[("3 FACTORS","ink")],sub="That Make a Research Institution Reliable",vis=("dots3",None),foot="EVIDENCE. INSIGHT. IMPACT."),
dict(n="clinstat_reliable",dark=0,kick="RELIABLE RESEARCH",lines=[("WHAT ACTUALLY MAKES","ink"),("A RESEARCH FINDING","ink"),("‘RELIABLE’?","gold")],sub="Use meta-analysis when appropriate to evaluate the consistency of evidence across studies.",vis=("badge",("10",None))),
dict(n="clinstat_reliable15",dark=0,kick="RELIABLE RESEARCH",lines=[("WHAT ACTUALLY MAKES","ink"),("A RESEARCH FINDING","ink"),("‘RELIABLE’?","gold")],sub="STARTS WITH RIGOR.",vis=("chips",["VALIDATION","REPRODUCIBILITY","ROBUSTNESS","MULTIPLE TESTING"])),
dict(n="clinstat_gulf",dark=0,kick="CLINICAL BIOSTATISTICS",lines=[("Medical Insights","ink"),("ACROSS THE GULF","gold")],sub="Technical Research",vis=("map",None),foot="EVIDENCE. INSIGHT. IMPACT."),
dict(n="deskreview_en",dark=0,kick="BEFORE PEER REVIEW",lines=[("Editors decide","ink"),("in minutes.","forest")],sub="before anyone reads your results.",vis=("note",None)),
dict(n="deskreview_ar",dark=0,rtl=1,kick="قبل المراجعة العلمية",lines=[("المحررون يقررون","ink"),("خلال دقائق.","forest")],sub="قبل أن يقرأ أحد نتائجك.",vis=("note",None)),
]
PAGE='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:LX;src:url(Lexend.ttf);font-weight:100 900}@font-face{font-family:CA;src:url(Cairo.ttf);font-weight:200 900}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden} svg{display:block}
</style></head><body><svg id="s" width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"></svg><script>
const LG=__LOGO__,CFG=__CFG__,NS="http://www.w3.org/2000/svg",AR=!!CFG.rtl,F=AR?"CA":"LX";
const C={ivory:"#F9F5EF",ink:"#003520",forest:"#025130",gold:"#B19063",pale:"#E8F0EA",dark:"#00251A",sand:"#D4BD9E"};
const svg=document.getElementById("s");function el(t,a,p){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;}
function text(p,s,x,y,sz,w,f,ex={}){const at=Object.assign({x,y,"font-size":sz,"font-weight":w,fill:f,"font-family":F},ex);if(AR){at.direction="rtl";delete at["letter-spacing"];}const t=el("text",at,p);t.textContent=s;return t;}
function fit(t,m){const w=t.getBBox().width;if(w>m)t.setAttribute("font-size",parseFloat(t.getAttribute("font-size"))*m/w);return t;}
Promise.all(["700 100px LX","350 100px LX","700 100px CA","400 100px CA"].map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>{
 const defs=el("defs",{},svg);const f=el("filter",{id:"sh",x:"-30%",y:"-30%",width:"160%",height:"170%"},defs);el("feDropShadow",{dx:0,dy:8,stdDeviation:9,"flood-color":"#00200f","flood-opacity":.18},f);
 const D=!!CFG.dark,bg=D?C.dark:C.ivory,txt=D?C.pale:C.ink;
 el("rect",{width:1080,height:1920,fill:bg},svg);
 if(D){const g=el("g",{stroke:"#CFE3D6","stroke-width":1,opacity:.06},svg);for(let x=0;x<=1080;x+=72)el("line",{x1:x,y1:0,x2:x,y2:1920},g);for(let y=0;y<=1920;y+=72)el("line",{x1:0,y1:y,x2:1080,y2:y},g);}
 // logo
 const LCX=(LG.mark.x0+LG.word.x1)/2,LCY=(LG.mark.y0+LG.mark.y1)/2,lg=el("g",{transform:`translate(540,330) scale(.96) translate(${-LCX},${-LCY})`},svg);
 LG.dots.forEach(d=>el("circle",{cx:d.cx,cy:d.cy,r:d.r,fill:d.color},lg));LG.chev.forEach(c=>el("path",{d:c.d,fill:c.color,"fill-rule":"evenodd"},lg));el("path",{d:LG.divider.d,fill:D?C.gold:LG.divider.color},lg);["clin","stat","res"].forEach(k=>LG[k].forEach(l=>el("path",{d:l.d,fill:D&&k!=="res"?C.pale:l.color,"fill-rule":"evenodd"},lg)));
 // kicker
 fit(text(svg,CFG.kick,540,640,AR?40:30,600,C.gold,{"text-anchor":"middle","letter-spacing":AR?0:9}),900);
 // headline
 const n=CFG.lines.length,sz=n>=4?92:n===3?84:(CFG.lines[0][0].length>10?104:150);let y=740+(n<3?40:0);
 CFG.lines.forEach(([s,k],i)=>{const col=k==="ink"?txt:k==="pale"?C.pale:C[k];const t=text(svg,s,540,y,sz,700,col,{"text-anchor":"middle","letter-spacing":AR?0:-1});fit(t,920);y+=sz*(AR?1.25:1.2);});
 const hy=y;
 el("line",{x1:440,x2:640,y1:hy-sz*.45,y2:hy-sz*.45,stroke:C.gold,"stroke-width":6,"stroke-linecap":"round"},svg);
 // visual
 const V=CFG.vis[0],A=CFG.vis[1];let vy=Math.max(hy+70,1010);
 if(V==="badge"){el("circle",{cx:540,cy:vy+130,r:130,fill:C.gold,filter:"url(#sh)"},svg);text(svg,A[0],540,vy+130+52,150,700,C.ink,{"text-anchor":"middle"});vy+=300;}
 if(V==="dots3"){el("line",{x1:240,x2:840,y1:vy+90,y2:vy+90,stroke:C.gold,"stroke-width":3,opacity:.7},svg);for(let i=0;i<3;i++){const g=el("g",{transform:`translate(${240+i*300},${vy+90})`},svg);el("circle",{r:76,fill:C.gold,filter:"url(#sh)"},g);text(g,"0"+(i+1),0,24,70,700,C.ink,{"text-anchor":"middle"});}vy+=240;}
 if(V==="map"){const cp=el("clipPath",{id:"mp"},defs);el("rect",{x:90,y:vy,width:900,height:560,rx:36},cp);el("image",{href:"map_gulf.png",x:90,y:vy-250,width:900,height:1600,"clip-path":"url(#mp)",preserveAspectRatio:"xMidYMid slice"},svg);el("rect",{x:90,y:vy,width:900,height:560,rx:36,fill:"none",stroke:C.gold,"stroke-width":4},svg);vy+=600;}
 if(V==="chips"){let cx=0,rowY=vy+30,rows=[[]];const items=A.map(s=>({s,w:s.length*21+70}));let cur=0;const lines=[[]];items.forEach(it=>{const w=lines[lines.length-1].reduce((a,b)=>a+b.w+20,0);if(w+it.w>900)lines.push([]);lines[lines.length-1].push(it);});
  lines.forEach((ln,li)=>{const tot=ln.reduce((a,b)=>a+b.w+20,-20);let x=540-tot/2;ln.forEach(it=>{const g=el("g",{transform:`translate(${x},${rowY+li*96})`},svg);el("rect",{width:it.w,height:68,rx:34,fill:"none",stroke:C.gold,"stroke-width":3},g);text(g,it.s,it.w/2,45,26,600,D?C.sand:C.forest,{"text-anchor":"middle","letter-spacing":3});x+=it.w+20;});});vy+=lines.length*96+40;}
 if(V==="note"){const g=el("g",{transform:`translate(540,${vy+170}) rotate(-4)`},svg);el("rect",{x:-190,y:-150,width:380,height:300,rx:14,fill:"#FFFFFF",stroke:C.sand,"stroke-width":3,filter:"url(#sh)"},g);for(let i=0;i<5;i++)el("line",{x1:-140,x2:i===4?20:140,y1:-90+i*46,y2:-90+i*46,stroke:C.sand,"stroke-width":8,"stroke-linecap":"round"},g);el("circle",{cx:120,cy:100,r:34,fill:"none",stroke:C.gold,"stroke-width":8},g);el("path",{d:"M104,100 L117,113 L138,86",fill:"none",stroke:C.forest,"stroke-width":9,"stroke-linecap":"round","stroke-linejoin":"round"},g);vy+=400;}
 // sub
 const sy=Math.min(Math.max(vy+40,1480),1560);const words=CFG.sub.split(" ");const lines2=[];let ln="";const lim=AR?30:34;words.forEach(w=>{if((ln+" "+w).trim().length>lim){lines2.push(ln);ln=w;}else ln=(ln+" "+w).trim();});lines2.push(ln);
 lines2.slice(0,3).forEach((s,i)=>fit(text(svg,s,540,sy+i*58,AR?46:42,350,txt,{"text-anchor":"middle"}),900));
 // footer curve
 el("path",{d:"M360,1920 C730,1919 950,1872 1080,1778 L1080,1920 Z",fill:C.gold},svg);el("path",{d:"M360,1920 C730,1919 950,1872 1080,1778 L1080,1750 C960,1840 760,1896 470,1920 Z",fill:D?"#0B4A32":C.forest},svg);
 if(CFG.foot)fit(text(svg,CFG.foot,40,1870,28,500,D?C.sand:C.forest,{"letter-spacing":6}),600);
 window.READY=true;});
</script></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"])
        for cfg in C:
            for scale,suf in((1,"1080x1920"),(2,"2160x3840")):
                pg=await b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=scale)
                errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
                open(f"{HERE}/_c.html","w").write(PAGE.replace("__LOGO__",LOGO).replace("__CFG__",json.dumps(cfg,ensure_ascii=False)))
                await pg.goto(f"file://{HERE}/_c.html");await pg.wait_for_function("window.READY===true",timeout=20000);await pg.wait_for_timeout(200)
                await pg.screenshot(path=f"{HERE}/cover_{cfg['n']}_{suf}.png");await pg.close()
                if errs:print(cfg["n"],errs)
        await b.close();os.remove(f"{HERE}/_c.html")
asyncio.run(main())
