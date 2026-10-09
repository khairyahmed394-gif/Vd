import os
from playwright.sync_api import sync_playwright
JS="""() => { const out=[]; const vis=(e)=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentNode){if(n.getAttribute&&n.getAttribute('display')==='none')return 0;const a=n.getAttribute&&n.getAttribute('opacity');if(a!==null&&a!==undefined&&a!=='')o*=parseFloat(a);} return o;};
 document.querySelectorAll('svg text').forEach(t=>{const o=vis(t);if(o<0.6||!t.textContent.trim())return;const r=t.getBoundingClientRect();if(r.width<2)return;out.push({s:t.textContent.replace(/\\s+/g,' ').trim(),x0:r.left,y0:r.top,x1:r.right,y1:r.bottom});});return out;}"""
HEAD="WHAT ACTUALLY MAKES A RESEARCH FINDING “RELIABLE”?"
CAP={1:"Ensure high-quality and accurate data.",2:"Use an appropriate study design and adequate sample size",3:"Use the appropriate statistical analysis.",4:"Test the assumptions of the statistical methods",5:"Control for potential confounding factors",6:"Report effect sizes and confidence intervals, not only p-values",7:"Perform sensitivity and robustness analyses",8:"Address missing data appropriately",9:"Correct for multiple testing when necessary",10:"Use meta-analysis when appropriate to evaluate the consistency of evidence across studies",11:"Assess the risk of bias and methodological quality",12:"Have the analysis independently checked",13:"Ensure reproducibility of the analysis",14:"Compare the findings with previous evidence",15:"Avoid selective reporting and data-driven conclusions"}
EXTRA={7:["SENSITIVITY & ROBUSTNESS ANALYSES"],9:["MULTIPLE TESTING CORRECTION","ADJUSTED P-VALUES","REDUCED FALSE POSITIVES","CONTROL FALSE DISCOVERIES"],10:["STUDY 1","STUDY 2","STUDY n","META- ANALYSIS","OVERALL EFFECT","MORE PRECISE ESTIMATE"],13:["DATASET","ANALYSIS SCRIPTS","VALIDATION","REPRODUCIBILITY"],14:["PREVIOUS EVIDENCE","NEW FINDINGS"],15:["EXPLORATORY DATA MINING","POST-HOC ANALYSIS"]}
CLOSE=["RELIABLE RESEARCH STARTS WITH RIGOR.","CLINSTAT RESEARCH","EVIDENCE. INSIGHT. IMPACT."]
import json,sys
TT=json.load(open("times.json"))
CHECKS=[(2.4,[HEAD]),(29.8,CLOSE)]
for n,t0,d in TT: CHECKS.append((round(t0+d-.3,2),[HEAD,str(n),CAP[n]]+EXTRA.get(n,[])))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
    pg.goto("file://"+os.getcwd()+"/index.html"); pg.wait_for_function("window.READY===true"); bad=0
    for t,req in CHECKS:
        pg.evaluate(f"render({t})"); items=pg.evaluate(JS); joined=" ".join(i["s"] for i in items)
        for r in req:
            if r not in joined: bad+=1; print(f"[t={t}] MISSING EXACT TEXT: {r!r}")
        for it in items:
            if it["x0"]<60 or it["x1"]>1020 or it["y0"]<240 or it["y1"]>1595: bad+=1; print(f"[t={t}] SAFE-ZONE: '{it['s'][:40]}' x {it['x0']:.0f}-{it['x1']:.0f} y {it['y0']:.0f}-{it['y1']:.0f}")
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                a,c=items[i],items[j]; ox=min(a["x1"],c["x1"])-max(a["x0"],c["x0"]); oy=min(a["y1"],c["y1"])-max(a["y0"],c["y0"])
                if ox>8 and oy>8: bad+=1; print(f"[t={t}] OVERLAP: '{a['s'][:28]}' x '{c['s'][:28]}' ({ox:.0f}x{oy:.0f})")
        print(f"[t={t}] {len(items)} text items checked")
    for k in range(0,901,3): pg.evaluate(f"render({k/30})")
    print("sweep done (301 frames); page errors:",errs[:3],"| problems:",bad); b.close()
