import os, json
from playwright.sync_api import sync_playwright
JS="""() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.6||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.replace(/\\s+/g,' ').trim(),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom});});return out;}"""
Q=["Do they ask about your research question before your data?","Can they explain the method in plain language, not just jargon?","Do they review your study design, or only analyse what's already collected?","Do they document every step so someone else could reproduce it?","What does their own publication record look like?"]
CHECKS=[(2.9,["5","questions to ask before you bring","a biostatistician onto your project:"]),(5.9,[Q[0]]),(8.9,[Q[0],Q[1]]),(11.9,Q[:3]),(15.9,Q),(18.1,Q+["Ours: every team member has","50+ papers and an h-index of 5+."])]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
    pg.goto("file://"+os.getcwd()+"/index.html"); pg.wait_for_function("window.READY===true"); bad=0
    for t,req in CHECKS:
        pg.evaluate(f"render({t})"); items=pg.evaluate(JS); joined=" ".join(i["s"] for i in items)
        for r in req:
            if r not in joined: bad+=1; print(f"[t={t}] MISSING EXACT TEXT: {r!r}")
        for it in items:
            if it["x0"]<60 or it["x1"]>1016 or it["y0"]<240 or it["y1"]>1590: bad+=1; print(f"[t={t}] SAFE-ZONE: '{it['s'][:40]}' x {it['x0']:.0f}-{it['x1']:.0f} y {it['y0']:.0f}-{it['y1']:.0f}")
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                a,c=items[i],items[j]; ox=min(a["x1"],c["x1"])-max(a["x0"],c["x0"]); oy=min(a["y1"],c["y1"])-max(a["y0"],c["y0"])
                if ox>8 and oy>8: bad+=1; print(f"[t={t}] OVERLAP: '{a['s'][:28]}' x '{c['s'][:28]}' ({ox:.0f}x{oy:.0f})")
        print(f"[t={t}] {len(items)} text items checked")
    for k in range(0,601,3): pg.evaluate(f"render({k/30})")
    print("sweep done (201 frames); page errors:",errs[:3],"| problems:",bad); b.close()
