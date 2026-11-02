import sys,os,asyncio
sys.path.insert(0,"/home/user/Vd/clinstat/posts")
import engine as E
from engine import t,logo
import data as D
NAVY,GREEN,GOLD,SAND="#0B1F33","#103D2E","#A8854E","#F7F4ED"
FD="/home/user/Vd/clinstat/posts/fonts"
CSS=f'''@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Regular.ttf);font-weight:400}}@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Medium.ttf);font-weight:500}}@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-SemiBold.ttf);font-weight:600}}@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Bold.ttf);font-weight:700}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:PX,sans-serif;direction:rtl;overflow:hidden}}
.c{{position:relative;width:100%;height:100%;display:flex;flex-direction:column;padding:var(--p)}}
.top{{display:flex;justify-content:space-between;align-items:center}}.pg{{font-weight:600;letter-spacing:.05em}}
.kick{{font-weight:700;color:{GOLD};letter-spacing:.02em}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:var(--fs0);opacity:.85;direction:ltr}}
h1,h2{{font-weight:700;line-height:1.28;text-wrap:balance}}p,li{{font-weight:500;line-height:1.7}}ul{{list-style:none}}
.num{{width:var(--nb);height:var(--nb);border-radius:50%;background:{GOLD};color:{NAVY};display:grid;place-items:center;font-weight:700}}
.btn{{display:inline-block;background:{GOLD};color:{NAVY};font-weight:700;border-radius:60px}}
'''
def vis_ci():
    return f'''<svg viewBox="0 0 800 260" width="100%" style="max-width:860px;direction:ltr"><line x1="60" y1="130" x2="740" y2="130" stroke="#C9C3B5" stroke-width="3"/>
<g font-family="PX" font-size="26" fill="{NAVY}"><text x="30" y="70">دقيق</text><text x="30" y="212">أقل دقة</text></g>
<line x1="320" y1="70" x2="480" y2="70" stroke="{GREEN}" stroke-width="10" stroke-linecap="round"/><circle cx="400" cy="70" r="14" fill="{GOLD}"/>
<line x1="140" y1="200" x2="660" y2="200" stroke="{GREEN}" stroke-width="10" stroke-linecap="round"/><circle cx="400" cy="200" r="14" fill="{GOLD}"/>
<line x1="400" y1="20" x2="400" y2="240" stroke="{GOLD}" stroke-width="2" stroke-dasharray="6 8"/></svg>'''
def vis_two():
    return f'''<svg viewBox="0 0 800 280" width="100%" style="max-width:900px;direction:ltr"><g font-family="PX" font-size="30" fill="{NAVY}"><text x="790" y="62" text-anchor="end">دلالة إحصائية</text><text x="790" y="192" text-anchor="end">حجم الأثر / الأهمية</text></g>
<rect x="20" y="80" width="760" height="20" rx="10" fill="#E6E0D2"/><rect x="20" y="80" width="560" height="20" rx="10" fill="{GREEN}"/>
<rect x="20" y="210" width="760" height="20" rx="10" fill="#E6E0D2"/><rect x="20" y="210" width="210" height="20" rx="10" fill="{GOLD}"/>
<text x="20" y="262" font-family="PX" font-size="22" fill="#6b6b66">توضيح مفهومي فقط، وليس بيانات</text></svg>'''
def vis_missing():
    cells=""
    for r in range(4):
        for c in range(4):
            miss=(r,c) in [(1,2),(2,0),(2,3),(3,1)]
            cells+=f'<rect x="{c*92+10}" y="{r*62+10}" width="84" height="54" rx="8" fill="{GOLD if miss else "#FFFFFF"}" stroke="#D6CFBE" stroke-width="2"/>'
    return f'<svg viewBox="0 0 390 270" width="620" style="direction:ltr">{cells}</svg>'
def svg_logo(light,w): return logo(light=light,w=w)
def page(w,h,body,bg,fg,pad=80,fs0=26,nb=90):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}html,body{{width:{w}px;height:{h}px;background:{bg};color:{fg};--p:{pad}px;--fs0:{fs0}px;--nb:{nb}px}}</style></head><body><div class="c">{body}</div></body></html>'
FOOT=lambda light:f'<div class="foot"><span>Research that survives peer review</span><span>ClinStat Research</span></div>'
def slide(kind,n,total,title,body,vis=None):
    W,H=1080,1350
    if kind=="cover":
        b=f'<div class="top">{svg_logo(True,240)}<span class="pg" style="font-size:30px;color:{SAND}">1/{total}</span></div><div style="margin:auto 0"><div class="kick" style="font-size:34px;margin-bottom:28px">ClinStat Research</div><h1 style="font-size:96px;color:{SAND}">{t(title)}</h1><p style="font-size:42px;color:#D7D1BF;margin-top:36px">{t(body)}</p></div>{FOOT(True)}'
        return page(W,H,b,GREEN,SAND,90)
    if kind=="cta":
        b=f'<div class="top">{svg_logo(True,240)}<span class="pg" style="font-size:30px;color:{SAND}">{n}/{total}</span></div><div style="margin:auto 0"><h1 style="font-size:84px;color:{SAND}">{t(title)}</h1><div class="btn" style="font-size:42px;padding:26px 56px;margin-top:56px">{t(body)}</div></div>{FOOT(True)}'
        return page(W,H,b,NAVY,SAND,90)
    v=f'<div style="margin:30px 0;display:flex;justify-content:center">{vis}</div>' if vis else ""
    b=f'<div class="top">{svg_logo(False,240)}<span class="pg" style="font-size:30px;color:{GOLD}">{n}/{total}</span></div><div style="margin:auto 0"><div class="num" style="font-size:60px;width:110px;height:110px">{n-1}</div><h2 style="font-size:80px;color:{GREEN};margin-top:40px">{t(title)}</h2><p style="font-size:52px;color:{NAVY};margin-top:36px">{t(body)}</p>{v}</div>{FOOT(False)}'
    return page(W,H,b,SAND,NAVY,90)
def single(w,h,title,sub,vis,pad,tsz,ssz,dark=False):
    bg,fg=(GREEN,SAND) if dark else (SAND,NAVY)
    b=f'<div class="top">{svg_logo(dark,int(w*.2))}<span class="kick" style="font-size:{ssz*.8}px">ClinStat Research</span></div><div style="margin:auto 0"><h1 style="font-size:{tsz}px;color:{SAND if dark else GREEN}">{t(title)}</h1><p style="font-size:{ssz}px;margin-top:{ssz*.6}px;color:{fg}">{t(sub)}</p><div style="margin-top:{ssz*.5}px">{vis or ""}</div></div>{FOOT(dark)}'
    return page(w,h,b,bg,fg,pad,fs0=int(ssz*.6),nb=70)
def story(title,sub,note,dark=False,sticker=False):
    W,H=1080,1920
    bg,fg=(GREEN,SAND) if dark else (SAND,NAVY)
    st=f'<div style="margin:60px auto 0;width:760px;border-radius:36px;background:#fff;color:{NAVY};padding:40px;text-align:center;font-size:44px;font-weight:600;box-shadow:0 10px 30px #0003">اكتب سؤالك هنا</div>' if sticker else ""
    b=f'<div class="top" style="margin-top:250px">{svg_logo(dark,260)}<span class="kick" style="font-size:34px">Ask ClinStat</span></div><div style="margin:60px 0"><h1 style="font-size:92px;color:{SAND if dark else GREEN}">{t(title)}</h1><p style="font-size:46px;margin-top:40px">{t(sub)}</p><p style="font-size:34px;margin-top:30px;color:{GOLD}">{t(note)}</p>{st}</div>'
    return page(W,H,b,bg,fg,100,fs0=30)
def reelcover():
    W,H=1080,1920
    b=f'<div class="top" style="margin-top:250px">{svg_logo(True,280)}<span class="kick" style="font-size:34px">Research Red Flags</span></div><div style="margin:auto 0"><h1 style="font-size:110px;color:{SAND}">حذف المرضى اللي بياناتهم ناقصة</h1><h1 style="font-size:110px;color:{GOLD};margin-top:10px">مش قرار محايد.</h1><div style="margin-top:70px;display:flex;justify-content:center">{vis_missing()}</div></div>'
    return page(W,H,b,GREEN,SAND,100)
def build():
    C={c["id"]:c for c in D.CONTENT};R={}
    R["cs001_linkedin_1200x627"]=single(1200,627,"p-value صغيرة؟ ده مش معناه إن الأثر كبير.","الدلالة الإحصائية وحجم الأثر سؤالان مختلفان",vis_two(),44,54,28)
    for i,(a,b_,c_) in enumerate(C["CS-003"]["slides"],1):
        k="cover" if a=="غلاف" else ("cta" if a=="CTA" else "c");R[f"cs003_carousel_{i:02d}_1080x1350"]=slide(k,i,7,b_,c_)
    R["cs004_x_1600x900"]=single(1600,900,"دلالة إحصائية ≠ أهمية سريرية","الأولى تقول إن البيانات متوافقة أو لا مع فرضية العدم. الثانية تسأل: هل الأثر يغيّر قرارًا يخص المريض؟",vis_two(),90,92,42)
    R["cs005_facebook_1080x1350"]=single(1080,1350,"قبل ما تجمع أول بيان، راجع تصميم دراستك.","سؤال محدد · تصميم ونتيجة أساسية · حجم عينة · خطة تحليل",f'<div class="btn" style="font-size:40px;padding:22px 50px">احجز استشارة تصميم دراسة</div>',90,92,44)
    for i,(a,b_,c_) in enumerate(C["CS-006"]["frames"],1): R[f"cs006_story_{i}_1080x1920"]=story(a if i>1 else "اسألنا",b_,c_,dark=(i==3),sticker=(i==1))
    R["cs002_reel_cover_1080x1920"]=reelcover()
    for i,(a,b_,c_) in enumerate(C["CS-007"]["slides"],1):
        k="cover" if a=="غلاف" else ("cta" if a=="CTA" else "c");R[f"cs007_carousel_{i:02d}_1080x1350"]=slide(k,i,7,b_,c_,vis_ci() if i==3 else None)
    return R
async def render(R):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--allow-file-access-from-files"])
        for name,h in R.items():
            w,hh=[int(x) for x in name.split("_")[-1].split("x")]
            pg=await b.new_page(viewport={"width":w,"height":hh});open("_t.html","w").write(h)
            await pg.goto("file://"+os.path.abspath("_t.html"));await pg.wait_for_timeout(250)
            await pg.screenshot(path=f"out/{name}.png");await pg.close()
        await b.close();os.remove("_t.html")
if __name__=="__main__": asyncio.run(render(build()))
