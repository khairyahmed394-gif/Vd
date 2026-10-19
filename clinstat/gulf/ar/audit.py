import os
from playwright.sync_api import sync_playwright
JS="""() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.6||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.replace(/\\s+/g,' ').trim(),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom});});return out;}"""
# settled moment of each scene (away from the wipes at 4.2 / 8.4 / 13.8 / 18.6 +-0.5)
CHECKS=[(3.6,["الإحصاء الحيوي السريري"]),(7.6,["سلامة","البيانات","تسريع","التجارب","الإحصاء الحيوي السريري · الخليج"]),
 (13.2,["رؤى طبية","في الخليج","رؤى البحوث","التقنية","يناير","يوليو","تصور توضيحي · وليست بيانات حقيقية"]),
 (17.9,["رؤى طبية","عبر الخليج","الرياض","مدينة الكويت","المنامة","الدوحة","أبوظبي","مسقط","خريطة توضيحية · عواصم دول الخليج"]),
 (22.5,["سلامة البيانات","تسريع التجارب","الدليل. الرؤية. الأثر."])]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
    pg.goto("file://"+os.getcwd()+"/index.html"); pg.wait_for_function("window.READY===true"); bad=0
    for t,req in CHECKS:
        pg.evaluate(f"render({t})"); items=pg.evaluate(JS); joined=" | ".join(i["s"] for i in items)
        for r in req:
            if r not in joined: bad+=1; print(f"[t={t}] MISSING TEXT: {r!r}")
        for it in items:
            if it["x0"]<40 or it["x1"]>1040 or it["y0"]<60 or it["y1"]>1860: bad+=1; print(f"[t={t}] SAFE-ZONE: '{it['s'][:40]}' x {it['x0']:.0f}-{it['x1']:.0f} y {it['y0']:.0f}-{it['y1']:.0f}")
        print(f"[t={t}] {len(items)} text items checked")
    for k in range(0,691,3): pg.evaluate(f"render({k/30})")
    print("sweep done (231 frames); page errors:",errs[:3],"| problems:",bad); b.close()
