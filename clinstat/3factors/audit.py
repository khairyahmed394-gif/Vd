import os, re, json
from playwright.sync_api import sync_playwright
JS = """() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.6||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.replace(/\\s+/g,' ').trim(),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom});});return out;}"""
SETTLED = {"S1": 2.7, "S2": 7.5, "S3": 11.5, "S4": 16.3, "S5": 19.97}
REQUIRED = {"S1": ["CLINSTAT RESEARCH INSTITUTE", "3 FACTORS", "That Make a Research Institution Reliable"],
 "S2": ["01 — A RESEARCH-ACTIVE MEDICAL TEAM", "50+ publications per team member", "H-index of 5 or higher", "Not just clinicians. Researchers."],
 "S3": ["02 — A PROVEN TRACK RECORD", "1,000+ Researchers Supported", "5,000+ Research Projects", "Across specialties and study designs."],
 "S4": ["03 — STRUCTURED QUALITY CONTROL", "Data checks", "Appropriate methodology", "Independent review", "Reproducible practices"],
 "S5": ["Reliability isn't a claim.", "It's a process you can ask to see.", "EVIDENCE. INSIGHT. IMPACT."]}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"]); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto("file://"+os.getcwd()+"/index.html"); pg.wait_for_function("window.READY===true"); bad = 0
    for sc, t in SETTLED.items():
        pg.evaluate(f"render({t})"); items = pg.evaluate(JS); joined = " | ".join(i["s"] for i in items)
        for req in REQUIRED[sc]:
            if req not in joined: bad += 1; print(f"[{sc} t={t}] MISSING EXACT TEXT: {req!r}")
        for it in items:
            if it["x0"] < 64 or it["x1"] > 1016 or it["y0"] < 240 or it["y1"] > 1590: bad += 1; print(f"[{sc}] SAFE-ZONE: '{it['s'][:40]}' x {it['x0']:.0f}-{it['x1']:.0f} y {it['y0']:.0f}-{it['y1']:.0f}")
        # overlap only between elements that are not intentional stacked lines of one block (>14px both ways)
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                a, c = items[i], items[j]; ox = min(a["x1"], c["x1"])-max(a["x0"], c["x0"]); oy = min(a["y1"], c["y1"])-max(a["y0"], c["y0"])
                if ox > 14 and oy > 14: bad += 1; print(f"[{sc}] OVERLAP: '{a['s'][:30]}' x '{c['s'][:30]}' ({ox:.0f}x{oy:.0f})")
        print(f"[{sc} t={t}] {len(items)} text items checked")
    n = 0
    for k in range(0, 601, 3): pg.evaluate(f"render({k/30})"); n += 1
    print(f"swept {n} frames; page errors: {errs[:3]}; problems: {bad}")
    b.close()
