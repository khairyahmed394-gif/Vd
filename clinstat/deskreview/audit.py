import os, sys, json
from playwright.sync_api import sync_playwright
JS="""() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.6||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.replace(/\\s+/g,' ').trim(),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom});});return out;}"""
EN={2.9:["Editors decide","in minutes.","before anyone reads your results."],4.8:["Your manuscript, on the editor's desk."],8.0:["GATE 1 OF 3","Statistics","Reporting gaps found"],
    11.4:["GATE 2 OF 3","Ethics","Approval documents incomplete"],14.9:["GATE 3 OF 3","Scope","Not a fit for this journal"],17.6:["DESK REJECTED","All three were avoidable."],
    20.2:["One expert review,","before you submit.","Statistics reported in full"],23.8:["READY TO SUBMIT","Scope matched to the journal"],29.0:["Free 15-minute","pre-submission consultation","Book your free consultation","Data Integrity – Accelerated Trials","Acceptance is always the journal's decision."]}
AR={2.9:["المحررون يقررون","خلال دقائق.","قبل أن يقرأ أحد نتائجك."],4.8:["بحثك على مكتب المحرر."],8.0:["البوابة ١ من ٣","الإحصاء","ثغرات في عرض التحليل"],
    11.4:["البوابة ٢ من ٣","الأخلاقيات","وثائق الموافقة غير مكتملة"],14.9:["البوابة ٣ من ٣","نطاق المجلة","لا يناسب نطاق المجلة"],17.6:["رفض أولي","كلها كان يمكن تجنبها."],
    20.2:["مراجعة خبير واحدة","قبل التقديم.","الإحصاء معروض بالكامل"],23.8:["جاهز للتقديم","النطاق مناسب للمجلة"],29.0:["استشارة مجانية","لمدة ١٥ دقيقة قبل التقديم","احجز استشارتك المجانية","Data Integrity – Accelerated Trials","القبول قرار المجلة دائمًا."]}
lang=sys.argv[1]; CH=EN if lang=="en" else AR
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
    pg.goto("file://"+os.getcwd()+f"/index.html?lang={lang}"); pg.wait_for_function("window.READY===true"); bad=0
    for t,req in CH.items():
        pg.evaluate(f"render({t})"); items=pg.evaluate(JS); joined=" | ".join(i["s"] for i in items)
        for r in req:
            if r not in joined: bad+=1; print(f"[t={t}] MISSING EXACT TEXT: {r!r}")
        for it in items:
            if it["s"]=="!" : continue
            if it["x0"]<60 or it["x1"]>1016 or it["y0"]<240 or it["y1"]>1590: bad+=1; print(f"[t={t}] SAFE-ZONE: '{it['s'][:40]}' x {it['x0']:.0f}-{it['x1']:.0f} y {it['y0']:.0f}-{it['y1']:.0f}")
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                a,c=items[i],items[j]
                if "!" in (a["s"],c["s"]): continue
                ox=min(a["x1"],c["x1"])-max(a["x0"],c["x0"]); oy=min(a["y1"],c["y1"])-max(a["y0"],c["y0"])
                if ox>8 and oy>8: bad+=1; print(f"[t={t}] OVERLAP: '{a['s'][:28]}' x '{c['s'][:28]}' ({ox:.0f}x{oy:.0f})")
        print(f"[t={t}] {len(items)} text items checked")
    for k in range(0,901,3): pg.evaluate(f"render({k/30})")
    print(lang,"sweep done (301 frames); page errors:",errs[:3],"| problems:",bad); b.close()
