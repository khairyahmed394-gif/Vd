import os, sys
from playwright.sync_api import sync_playwright
JS="""() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.7||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.replace(/\\s+/g,' ').trim(),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom});});return out;}"""
TIMES=[1.9,2.9,4.9,6.8,9.3,11.0,13.0,14.9,17.0,19.0]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"]);tot=0
    for reel in sys.argv[1:]:
        pg=b.new_page(viewport={"width":1080,"height":1920}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
        pg.goto("file://"+os.getcwd()+f"/index.html?reel={reel}"); pg.wait_for_function("window.READY===true"); bad=0
        for t in TIMES:
            pg.evaluate(f"render({t})"); items=pg.evaluate(JS)
            for it in items:
                if it["x0"]<56 or it["x1"]>1024 or it["y0"]<240 or it["y1"]>1590: bad+=1; print(f"[{reel} t={t}] SAFE-ZONE: '{it['s'][:34]}' x {it['x0']:.0f}-{it['x1']:.0f} y {it['y0']:.0f}-{it['y1']:.0f}")
            for i in range(len(items)):
                for j in range(i+1,len(items)):
                    a,c=items[i],items[j]; ox=min(a["x1"],c["x1"])-max(a["x0"],c["x0"]); oy=min(a["y1"],c["y1"])-max(a["y0"],c["y0"])
                    if ox>10 and oy>12: bad+=1; print(f"[{reel} t={t}] OVERLAP: '{a['s'][:24]}' x '{c['s'][:24]}' ({ox:.0f}x{oy:.0f})")
        for k in range(0,601,4): pg.evaluate(f"render({k/30})")
        print(reel,"sweep ok | page errors:",errs[:3],"| problems:",bad); tot+=bad; pg.close()
    b.close()
