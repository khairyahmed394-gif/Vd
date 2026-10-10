import os, sys, json
from playwright.sync_api import sync_playwright
JS="""() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 // text + card rects + circles, in screen space; ink bounds for text come from the glyph box (getBBox) so line-height padding is excluded
 document.querySelectorAll('svg text, svg rect, svg circle').forEach(e=>{const o=vis(e);if(o<0.85)return;const r=e.getBoundingClientRect();if(r.width<4||r.height<4)return;
   if(e.tagName==='rect'&&r.width>1000&&r.height>1800)return;
   const k=e.tagName==='text'?'T':(e.tagName==='circle'?'C':'R');
   if(k==='R'&&r.height<12)return;                       // thin rules are handled as decoration
   out.push({k,s:(e.textContent||'').replace(/\\s+/g,' ').trim().slice(0,28),x0:Math.round(r.left),y0:Math.round(r.top),x1:Math.round(r.right),y1:Math.round(r.bottom)});});return out;}"""
CASES={"r01":[3.0,7.0,11.0,15.0,19.5],"r02":[3.0,6.9,10.8,15.2,19.5],"r03":[3.0,7.0,11.0,15.0,19.5],"r04":[3.0,6.9,11.0,15.2,19.5]}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"])
    for reel,ts in CASES.items():
        pg=b.new_page(viewport={"width":1080,"height":1920}); pg.goto("file://"+os.getcwd()+f"/index.html?reel={reel}"); pg.wait_for_function("window.READY===true")
        for t in ts:
            pg.evaluate(f"render({t})"); it=pg.evaluate(JS)
            # drop elements fully contained in another (text inside its card) when computing vertical rhythm
            tops=[i for i in it if not (i['k']!='T' and False)]
            rows=sorted(it,key=lambda i:(i['y0'],i['x0']))
            print(f"--- {reel} t={t}: {len(rows)} items")
            for i in rows: print(f"   {i['k']} y {i['y0']:>4}-{i['y1']:<4} x {i['x0']:>4}-{i['x1']:<4} {i['s']}")
        pg.close()
    b.close()
