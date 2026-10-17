"""python3 build.py [ar|en|all] [card ...] -> out/<lang>/<card>.png (1080x1350) and out/<lang>/2x/<card>.png (2160x2700)"""
import os, sys
from playwright.sync_api import sync_playwright
import engine
from cards import CARDS
HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = """() => { const out=[]; const H=1350;
 document.querySelectorAll('h1,h2,h3,p,.tag,.cnt,.cta,.pill,.num,.tname,.tdesc').forEach(e=>{const r=e.getBoundingClientRect(); if(r.width<2)return;
   const foot=document.querySelector('.foot'); const ft=foot?foot.getBoundingClientRect().top:H;
   if(!e.closest('.foot') && r.bottom>ft-10) out.push('OVERLAPS FOOTER: '+e.tagName+' '+e.textContent.slice(0,30)+' bottom '+Math.round(r.bottom)+' > '+Math.round(ft));
   if(r.left<60||r.right>1020) out.push('MARGIN: '+e.tagName+' '+e.textContent.slice(0,24)+' x '+Math.round(r.left)+'-'+Math.round(r.right));});
 const rows=[...document.querySelectorAll('.row,.trow')]; for(let i=0;i<rows.length-1;i++){const a=rows[i].getBoundingClientRect(),b=rows[i+1].getBoundingClientRect(); if(a.bottom>b.top+2) out.push('ROW OVERLAP '+i);}
 return out; }"""
def render(langs, only=None):
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files", "--font-render-hinting=none"])
        for lang in langs:
            engine.LANG["v"] = lang
            os.makedirs(f"{HERE}/out/{lang}/2x", exist_ok=True)
            for name, c in CARDS.items():
                if only and name not in only: continue
                f = f"{HERE}/_{name}_{lang}.html"; open(f, "w").write(engine.TPL[c["t"]](c[lang]))
                for scale, outp in ((1, f"out/{lang}/{name}.png"), (2, f"out/{lang}/2x/{name}.png")):
                    pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=scale); pg.goto("file://" + f); pg.wait_for_timeout(250)
                    if scale == 1:
                        for m in pg.evaluate(AUDIT): bad += 1; print(f"[{lang}/{name}] {m}")
                    pg.screenshot(path=f"{HERE}/{outp}"); pg.close()
                os.remove(f)
            print(lang, "done", len(CARDS))
        b.close()
    print("layout problems:", bad)
if __name__ == "__main__":
    a = sys.argv[1:]; langs = ["ar", "en"] if not a or a[0] == "all" else [a[0]]
    render(langs, a[1:] or None)
