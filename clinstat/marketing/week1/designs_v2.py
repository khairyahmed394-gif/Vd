"""ClinStat week-1 designs in the 'reference look': cream bg, centered logo, gold block + bold green headline,
light secondary text, soft prop illustrations (stand-ins for photos), green/gold wave footer."""
import sys,os,asyncio
sys.path.insert(0,"/home/user/Vd/clinstat/posts")
from engine import t,logo
import data as D
import designs as O
GREEN,G2,GOLD,CREAM,INK="#003520","#025130","#B19063","#F9F5EF","#0B1F33"
CSS=O.CSS.replace("body{","body{")  # fonts from v1
def wave(w,h):
    return f'<svg style="position:absolute;left:0;bottom:0" width="{w}" height="{h}" viewBox="0 0 1080 90" preserveAspectRatio="none"><path d="M0 46 C260 8 640 78 1080 14 L1080 90 L0 90Z" fill="{GOLD}"/><path d="M0 60 C300 36 700 84 1080 40 L1080 90 L0 90Z" fill="{GREEN}"/></svg>'
# ---- props: soft shaded illustrations (stand-ins for product photos)
def _sh(i,s=14):return f'<filter id="s{i}" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="14" stdDeviation="{s}" flood-color="#6b5a3a" flood-opacity=".28"/></filter>'
PROPS={
"mug":lambda:f'''<ellipse cx="190" cy="268" rx="190" ry="34" fill="#cfc6b2" opacity=".55"/><g filter="url(#sh)"><path d="M70 40 h230 v170 a115 70 0 0 1 -230 0z" fill="url(#mg)"/><ellipse cx="185" cy="40" rx="115" ry="30" fill="#fff"/><ellipse cx="185" cy="42" rx="98" ry="22" fill="#3a2418"/><ellipse cx="170" cy="38" rx="50" ry="8" fill="#5b3a28" opacity=".7"/><path d="M92 70 v120" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".7"/><path d="M298 70 c70 -10 78 90 0 98" fill="none" stroke="url(#mg)" stroke-width="26" stroke-linecap="round"/></g>''',
"notebook":lambda:f'''<g filter="url(#sh)"><path d="M0 120 L320 40 L420 150 L100 250z" fill="#E9E5DC"/><path d="M0 120 L320 40 L322 62 L4 142z" fill="#D8D3C7"/><g stroke="#bdb6a6" stroke-width="3" opacity=".7"><path d="M40 110 L330 38"/><path d="M60 138 L340 66"/></g><path d="M0 142 L100 270 L420 168 L420 150 L100 250 L4 142z" fill="#fff" opacity=".7"/></g>''',
"glasses":lambda:f'''<g filter="url(#sh)" fill="none" stroke="#1a1a1a" stroke-width="12"><ellipse cx="70" cy="80" rx="62" ry="52"/><ellipse cx="228" cy="70" rx="62" ry="52"/><path d="M130 72 q15 -14 38 -4" stroke-width="9"/><path d="M30 60 q20 -24 48 -16" stroke="#fff" stroke-width="6" opacity=".6"/><path d="M190 50 q20 -22 48 -14" stroke="#fff" stroke-width="6" opacity=".6"/><path d="M8 78 L-30 60" stroke-width="9"/></g>''',
"chart":lambda:f'''<g filter="url(#sh)"><rect x="0" y="0" width="300" height="220" rx="14" fill="#fff"/><rect x="26" y="26" width="120" height="14" rx="7" fill="{GREEN}"/><rect x="26" y="58" width="190" height="8" rx="4" fill="#E3DDCF"/><line x1="40" y1="190" x2="270" y2="190" stroke="#C9C3B5" stroke-width="3"/><rect x="60" y="120" width="34" height="70" rx="4" fill="{GREEN}"/><rect x="112" y="92" width="34" height="98" rx="4" fill="{G2}"/><rect x="164" y="136" width="34" height="54" rx="4" fill="{GOLD}"/><rect x="216" y="104" width="34" height="86" rx="4" fill="{GOLD}" opacity=".7"/></g>''',
"clipboard":lambda:f'''<g filter="url(#sh)"><rect x="0" y="20" width="250" height="330" rx="18" fill="#C9AE84"/><rect x="18" y="52" width="214" height="280" rx="8" fill="#fff"/><rect x="80" y="0" width="90" height="44" rx="12" fill="#6b6b66"/><g fill="{GREEN}"><rect x="40" y="90" width="22" height="22" rx="4"/><rect x="40" y="140" width="22" height="22" rx="4"/><rect x="40" y="190" width="22" height="22" rx="4"/><rect x="40" y="240" width="22" height="22" rx="4"/></g><g fill="#D9D3C4"><rect x="80" y="96" width="130" height="10" rx="5"/><rect x="80" y="146" width="110" height="10" rx="5"/><rect x="80" y="196" width="130" height="10" rx="5"/><rect x="80" y="246" width="90" height="10" rx="5"/></g></g>''',
"calc":lambda:f'''<g filter="url(#sh)"><rect x="0" y="0" width="190" height="270" rx="22" fill="#2b2b2b"/><rect x="18" y="20" width="154" height="56" rx="8" fill="#cfe3d6"/>{"".join(f'<rect x="{18+c*52}" y="{98+r*44}" width="42" height="34" rx="8" fill="{GOLD if c==3 else "#555"}"/>' for r in range(4) for c in range(3+1))}</g>''',
"pen":lambda:f'''<g filter="url(#sh)" transform="rotate(-28 120 20)"><rect x="0" y="0" width="240" height="22" rx="11" fill="{GREEN}"/><rect x="200" y="0" width="40" height="22" rx="11" fill="{GOLD}"/></g>''',
}
SIZE={"mug":(420,260),"notebook":(430,280),"glasses":(300,150),"chart":(300,240),"clipboard":(250,350),"calc":(190,270),"pen":(260,120)}
def props(names,x,y,scale=1.0,rot=0):
    """absolutely positioned SVG with the given props laid out left to right at (x,y)."""
    pos={"mug":(120,0),"notebook":(0,150),"glasses":(120,200),"chart":(0,40),"clipboard":(0,0),"calc":(250,70),"pen":(40,260)}
    shs=f'<defs><filter id="sh" x="-30%" y="-30%" width="170%" height="180%"><feDropShadow dx="0" dy="16" stdDeviation="14" flood-color="#6b5a3a" flood-opacity=".28"/></filter><linearGradient id="mg" x1="0" x2="1"><stop offset="0" stop-color="#e9e6df"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#d9d5cc"/></linearGradient></defs>'
    g="".join(f'<g transform="translate({pos[n][0]} {pos[n][1]})">{PROPS[n]()}</g>' for n in names)
    return f'<svg style="position:absolute;left:{x}px;bottom:{y}px;transform:scale({scale}) rotate({rot}deg);transform-origin:left bottom;overflow:visible" width="520" height="440" viewBox="0 0 520 440">{shs}{g}</svg>'
def page(w,h,body,pad=80,wh=None):
    wh=wh or int(h*.07)
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}html,body{{width:{w}px;height:{h}px;background:radial-gradient(120% 90% at 70% 40%,#fff 0%,{CREAM} 55%,#F1EBDD 100%);color:{INK};--p:{pad}px;overflow:hidden}}.c{{padding:{pad}px {pad}px 0}}.h{{font-weight:700;color:{GREEN};line-height:1.3;text-wrap:balance}}.sub{{font-weight:400;color:{G2};line-height:1.6}}.bar{{position:absolute;right:0;width:{int(w*.048)}px;background:{GOLD}}}.hl{{display:inline-block;background:{GREEN};color:{GOLD};font-weight:700;padding:0 .28em;border-radius:6px;line-height:1.25}}.tag{{position:absolute;right:{pad}px;font-weight:400;color:{G2}}}</style></head><body><div class="c" style="position:relative;width:100%;height:100%">{body}<div style="position:absolute;right:{pad}px;bottom:{wh+16}px;font-weight:500;font-size:{max(26,int(w*.024))}px;color:{G2};letter-spacing:.02em;direction:ltr">Research that survives peer review</div>{wave(w,wh)}</div></body></html>'
def head(w,lw,top=0):
    return f'<div style="display:flex;justify-content:center;margin-top:{top}px">{logo(light=False,w=lw)}</div>'
def block(w,y,h,inner,left=None):
    left=int(w*.08) if left is None else left
    return f'<div class="bar" style="top:{y}px;height:{h}px"></div><div style="position:absolute;right:{int(w*.048)+int(w*.04)}px;left:{left}px;top:{y}px;min-height:{h}px;display:flex;flex-direction:column;justify-content:center">{inner}</div>'
def single(w,h,title,sub,vis,pr,tsz,ssz,note=None):
    land=w>h*1.3
    pad=int(w*.06) if not land else int(w*.05)
    lw=int(w*.30) if not land else int(h*.45)
    ty=int(h*.19) if not land else int(h*.20)
    th=int(h*.20) if not land else int(h*.38)
    v=f'<div style="margin-top:28px">{vis}</div>' if vis else ""
    L=int(w*.40) if land else None
    b=head(w,lw)+block(w,ty,th,f'<h1 class="h" style="font-size:{tsz}px">{t(title)}</h1>',L)
    b+=f'<div style="position:absolute;right:{int(w*.048)+int(w*.04)}px;left:{L if L else int(w*.08)}px;top:{ty+th+24}px"><p class="sub" style="font-size:{ssz}px">{t(sub)}</p>{v}</div>'.replace("left:{int(w*.08)}px","left:{L if L else int(w*.08)}px")
    if pr: b+=pr
    if note: b+=f'<div class="tag" style="bottom:{int(h*.07)+22}px;font-size:{int(ssz*.8)}px">{t(note)}</div>'
    return page(w,h,b,pad)
def slide(kind,n,total,title,body,vis=None,pr=None):
    W,H=1080,1350
    cnt=f'<div style="position:absolute;right:80px;bottom:175px;font-weight:600;font-size:28px;color:{G2}">{n}/{total}</div>'
    if kind=="cover":
        b=head(W,420)+block(W,300,360,f'<div style="font-weight:500;font-size:34px;color:{GOLD};margin-bottom:18px">ClinStat Research</div><h1 class="h" style="font-size:92px">{t(title)}</h1>')
        b+=f'<div style="position:absolute;right:{int(W*.048)+43}px;left:86px;top:730px"><p class="sub" style="font-size:44px">{t(body)}</p></div>'
        if pr: b+=pr
        return page(W,H,b+cnt,80)
    if kind=="cta":
        b=head(W,420)+block(W,300,330,f'<h1 class="h" style="font-size:78px">{t(title)}</h1>')
        b+=f'<div style="position:absolute;right:{int(W*.048)+43}px;left:86px;top:680px"><p class="sub" style="font-size:40px;margin-bottom:34px">{t(body)}</p><span class="hl" style="font-size:44px;padding:14px 34px;border-radius:60px">ClinStat Research</span></div>'
        if pr: b+=pr
        return page(W,H,b+cnt,80)
    v=f'<div style="margin-top:34px">{vis}</div>' if vis else ""
    b=head(W,330)+block(W,230,300,f'<div style="margin-bottom:16px"><span class="hl" style="font-size:54px;padding:2px 22px">{n-1}</span></div><h2 class="h" style="font-size:78px">{t(title)}</h2>')
    b+=f'<div style="position:absolute;right:{int(W*.048)+43}px;left:86px;top:570px"><p class="sub" style="font-size:48px">{t(body)}</p>{v}</div>'
    if pr: b+=pr
    return page(W,H,b+cnt,80)
def story(title,sub,note,pr=None,sticker=False):
    W,H=1080,1920
    st=f'<div style="margin-top:46px;width:760px;border-radius:36px;background:#fff;color:{INK};padding:38px;text-align:center;font-size:44px;font-weight:600;box-shadow:0 10px 30px #0002">اكتب سؤالك هنا</div>' if sticker else ""
    b=head(W,440,250)+block(W,520,420,f'<h1 class="h" style="font-size:104px">{t(title)}</h1>')
    b+=f'<div style="position:absolute;right:{int(W*.048)+43}px;left:86px;top:980px"><p class="sub" style="font-size:46px">{t(sub)}</p>{st}<p style="font-size:32px;color:{GOLD};font-weight:500;margin-top:30px">{t(note)}</p></div>'
    if pr: b+=pr
    return page(W,H,b,80,wh=130)
def reelcover(hook,series="Research Red Flags",pr=None):
    W,H=1080,1920
    b=head(W,460,250)+block(W,560,620,f'<div style="font-weight:500;font-size:34px;color:{GOLD};margin-bottom:18px">{t(series)}</div><h1 class="h" style="font-size:118px">{t(hook)}</h1>')
    if pr: b+=pr
    return page(W,H,b,80,wh=130)
def build():
    C={c["id"]:c for c in D.CONTENT};R={}
    P=lambda n,x,y,s=1,r=0:props(n,x,y,s,r)
    R["cs001_linkedin_1200x627"]=single(1200,627,"p-value صغيرة؟ ده مش معناه إن الأثر كبير.","الدلالة الإحصائية وحجم الأثر سؤالان مختلفان",None,P(["chart","pen"],10,45,.85),56,30)
    for i,(a,b_,c_) in enumerate(C["CS-003"]["slides"],1):
        k="cover" if a=="غلاف" else ("cta" if a=="CTA" else "c")
        pr=P(["mug","notebook","glasses"],-30,100,1.0) if k=="cover" else (P(["clipboard","pen"],20,105,.95) if k=="cta" else P(["mug","notebook"],-10,108,.68))
        R[f"cs003_carousel_{i:02d}_1080x1350"]=slide(k,i,7,b_,c_,pr=pr)
    R["cs004_x_1600x900"]=single(1600,900,"دلالة إحصائية ≠ أهمية سريرية","الأولى تقول إن البيانات متوافقة أو لا مع فرضية العدم. الثانية تسأل: هل الأثر يغيّر قرارًا يخص المريض؟",None,P(["chart","pen"],30,70,1.15),82,42)
    R["cs005_facebook_1080x1350"]=single(1080,1350,"قبل ما تجمع أول بيان، راجع تصميم دراستك.","سؤال محدد · تصميم ونتيجة أساسية · حجم عينة · خطة تحليل",'<span class="hl" style="font-size:40px;padding:14px 46px;border-radius:60px">احجز استشارة تصميم دراسة</span>',P(["notebook","mug","glasses"],-30,100,1.0),70,40)
    for i,(a,b_,c_) in enumerate(C["CS-006"]["frames"],1):
        R[f"cs006_story_{i}_1080x1920"]=story(a if i>1 else "اسألنا",b_,c_,pr=P(["mug","notebook"],-20,200,.9),sticker=(i==1))
    R["cs002_reel_cover_1080x1920"]=reelcover("حذف المرضى اللي بياناتهم ناقصة؟ مش قرار محايد.",pr=P(["clipboard","pen"],20,200,1.0))
    for i,(a,b_,c_) in enumerate(C["CS-007"]["slides"],1):
        k="cover" if a=="غلاف" else ("cta" if a=="CTA" else "c")
        pr=P(["mug","notebook","glasses"],-30,100,1.0) if k=="cover" else (P(["clipboard","pen"],20,105,.95) if k=="cta" else P(["mug","notebook"],-10,108,.68))
        R[f"cs007_carousel_{i:02d}_1080x1350"]=slide(k,i,7,b_,c_,O.vis_ci() if i==3 else None,pr=None if i==3 else pr)
    return R
async def render(R,outd="out_v2"):
    from playwright.async_api import async_playwright
    os.makedirs(outd,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--allow-file-access-from-files"])
        for name,h in R.items():
            w,hh=[int(x) for x in name.split("_")[-1].split("x")]
            pg=await b.new_page(viewport={"width":w,"height":hh});open("_t2.html","w").write(h)
            await pg.goto("file://"+os.path.abspath("_t2.html"));await pg.wait_for_timeout(250)
            await pg.screenshot(path=f"{outd}/{name}.png");await pg.close()
        await b.close();os.remove("_t2.html")

SETS=[(["mug","notebook","glasses"],1.0),(["clipboard","pen"],.95),(["chart","pen"],.95),(["calc","notebook"],1.0)]
def auto(title,base):
    n=len(title);return base if n<=38 else int(base*.86) if n<=60 else int(base*.74)
def build_rest():
    import data2
    R={};P=props
    for j,c in enumerate(data2.ALL[7:]):
        n=int(c["id"][3:]);k=f"cs{n:03d}";typ=c["typ"];names,sc=SETS[j%4]
        if typ=="carousel":
            for i,(a,b_,c_) in enumerate(c["slides"],1):
                kk="cover" if a=="غلاف" else ("cta" if a=="CTA" else "c")
                pr=P(names,-30 if kk=="cover" else 20,100,sc*(1.0 if kk=="cover" else .95)) if kk!="c" else P(names,-10,108,.68)
                R[f"{k}_carousel_{i:02d}_1080x1350"]=slide(kk,i,7,b_,c_,pr=pr)
        elif typ=="reel": R[f"{k}_reel_cover_1080x1920"]=reelcover(c["hook"],c["series"],pr=P(names,20,200,sc))
        elif typ=="x": R[f"{k}_x_1600x900"]=single(1600,900,c["hook"],c["core"],None,P(names,30,70,1.15*sc),auto(c["hook"],82),42)
        elif typ=="li": R[f"{k}_linkedin_1200x627"]=single(1200,627,c["hook"],c["core"],None,P(names,10,45,.85*sc),auto(c["hook"],56),30)
        elif typ=="fb": R[f"{k}_facebook_1080x1350"]=single(1080,1350,c["hook"],c["core"],None,P(names,-30,100,sc),auto(c["hook"],70),40)
        elif typ=="story":
            for i,(a,b_,c_) in enumerate(c["frames"],1): R[f"{k}_story_{i}_1080x1920"]=story(a,b_,c_,pr=P(names,-20,200,.9*sc))
    return R
def btn(label,fs):return f'<span class="hl" style="font-size:{fs}px;padding:{int(fs*.3)}px {int(fs*.9)}px;border-radius:60px">{t(label)}</span>'
def build_ads():
    sys.path.insert(0,"/home/user/Vd/clinstat/marketing/round4");import camp
    R={};P=props
    for j,c in enumerate(camp.CAMPS):
        names,sc=SETS[j%3]
        for v in ("A","B"):
            d=c[v];k=f"c{c['id']}_{v}"
            R[f"{k}_feed_1080x1350"]=single(1080,1350,d["h"],d["sub"],btn(c["cta_label"],44),P(names,-30,100,sc),auto(d["h"],70),42)
            W,H=1080,1920
            b=head(W,440,250)+block(W,520,430,f'<h1 class="h" style="font-size:{auto(d["h"],104)}px">{t(d["h"])}</h1>')
            b+=f'<div style="position:absolute;right:{int(W*.048)+43}px;left:86px;top:990px"><p class="sub" style="font-size:46px">{t(d["sub"])}</p><div style="margin-top:44px">{btn(c["cta_label"],46)}</div></div>'+P(names,-20,200,.9*sc)
            R[f"{k}_story_1080x1920"]=page(W,H,b,80,wh=130)
            R[f"{k}_linkedin_1200x627"]=single(1200,627,d["h"],d["sub"],btn(c["cta_label"],28),P(names,10,45,.85*sc),auto(d["h"],56),28)
    return R
if __name__=="__main__":
    asyncio.run(render(build()));asyncio.run(render(build_rest()))
    asyncio.run(render(build_ads(),"../round4/ads_v2"))
