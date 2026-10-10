import os, json
from playwright.sync_api import sync_playwright
JS="""() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.6||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.replace(/\\s+/g,' ').trim(),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom});});return out;}"""
Q=["هل يسألون عن سؤالك البحثي قبل أن يسألوا عن بياناتك؟","هل يشرحون الطريقة بلغة واضحة، لا بالمصطلحات فقط؟","هل يراجعون تصميم دراستك، أم يكتفون بتحليل ما جُمع من بيانات؟","هل يوثقون كل خطوة بحيث يستطيع غيرهم إعادة إنتاج النتائج؟","كيف يبدو سجلهم في النشر العلمي؟"]
HD=["5","أسئلة اطرحها قبل أن تستعين","بخبير إحصاء حيوي في مشروعك:"]
ST=["في فريقنا، كل عضو لديه","أكثر من 50 بحثًا ومؤشر h-index لا يقل عن 5."]
CHECKS=[(2.9,HD),(5.9,[Q[0]]),(8.9,[Q[0],Q[1]]),(11.9,Q[:3]),(15.9,Q),(18.1,Q+ST)]
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
                a,c=items[i],items[j]; ox=min(a["x1"],c["x1"])-max(a["x0"],c["x0"]); sh=lambda d:(d["y0"]+(d["y1"]-d["y0"])*.25,d["y1"]-(d["y1"]-d["y0"])*.25); (a0,a1),(c0,c1)=sh(a),sh(c); oy=min(a1,c1)-max(a0,c0)
                if ox>8 and oy>8: bad+=1; print(f"[t={t}] OVERLAP: '{a['s'][:28]}' x '{c['s'][:28]}' ({ox:.0f}x{oy:.0f})")
        print(f"[t={t}] {len(items)} text items checked")
    for k in range(0,601,3): pg.evaluate(f"render({k/30})")
    print("sweep done (201 frames); page errors:",errs[:3],"| problems:",bad); b.close()
