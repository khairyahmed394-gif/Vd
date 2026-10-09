import os, json
from playwright.sync_api import sync_playwright
JS = """() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.5||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.trim().slice(0,28),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom,o:+o.toFixed(2)});});return out;}"""
TIMES = {"A": 3.2, "B": 8.6, "C": 13.2, "D": 17.2, "E": 21.5}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"]); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto("file://"+os.getcwd()+"/index3.html"); pg.wait_for_function("window.READY===true"); pg.evaluate("window.NOBLUR=true")
    bad = 0
    for sc, t in TIMES.items():
        pg.evaluate(f"render({t})"); items = pg.evaluate(JS)
        for it in items:
            if it["x0"] < 36 or it["x1"] > 1044 or it["y0"] < 225 or it["y1"] > 1600:
                bad += 1; print(f"[{sc} t={t}] SAFE-ZONE: '{it['s']}' x {it['x0']:.0f}-{it['x1']:.0f} y {it['y0']:.0f}-{it['y1']:.0f}")
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                a, c = items[i], items[j]; ox = min(a["x1"], c["x1"])-max(a["x0"], c["x0"]); oy = min(a["y1"], c["y1"])-max(a["y0"], c["y0"])
                if ox > 6 and oy > 6: bad += 1; print(f"[{sc} t={t}] OVERLAP: '{a['s']}' x '{c['s']}' ({ox:.0f}x{oy:.0f}px)")
        print(f"[{sc} t={t}] {len(items)} visible text items")
    # frame-by-frame sweep for JS exceptions at 0.1 s steps
    for k in range(0, 221):
        pg.evaluate(f"render({k*0.1})")
    print("sweep done; page errors:", errs[:5], "| problems:", bad)
    b.close()
