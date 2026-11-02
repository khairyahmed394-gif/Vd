import sys,asyncio,os
sys.path.insert(0,"../week1");sys.path.insert(0,"/home/user/Vd/clinstat/posts")
import designs as G
from designs import page,svg_logo,single,NAVY,GREEN,GOLD,SAND,t
import camp
def btn(label,fs): return f'<div class="btn" style="font-size:{fs}px;padding:{fs*.5}px {fs*1.2}px">{t(label)}</div>'
def story_ad(h,sub,label):
    W,H=1080,1920
    b=f'<div class="top" style="margin-top:250px">{svg_logo(True,280)}<span class="kick" style="font-size:34px">ClinStat Research</span></div><div style="margin:auto 0"><h1 style="font-size:108px;color:{SAND}">{t(h)}</h1><p style="font-size:50px;margin-top:44px;color:#D7D1BF">{t(sub)}</p><div style="margin-top:70px">{btn(label,48)}</div></div><div style="height:230px"></div>'
    return page(W,H,b,GREEN,SAND,100)
R={}
for c in camp.CAMPS:
    for v in ("A","B"):
        d=c[v];k=f"c{c['id']}_{v}"
        R[f"{k}_feed_1080x1350"]=single(1080,1350,d["h"],d["sub"],btn(c["cta_label"],44),90,92,44)
        R[f"{k}_story_1080x1920"]=story_ad(d["h"],d["sub"],c["cta_label"])
        R[f"{k}_linkedin_1200x627"]=single(1200,627,d["h"],d["sub"],btn(c["cta_label"],30),44,54,28)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--allow-file-access-from-files"])
        for n,h in R.items():
            w,hh=[int(x) for x in n.split("_")[-1].split("x")]
            pg=await b.new_page(viewport={"width":w,"height":hh});open("_t.html","w").write(h)
            await pg.goto("file://"+os.path.abspath("_t.html"));await pg.wait_for_timeout(250);await pg.screenshot(path=f"ads/{n}.png");await pg.close()
        await b.close();os.remove("_t.html")
asyncio.run(go())
