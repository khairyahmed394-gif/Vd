import asyncio
from playwright.async_api import async_playwright
N,T,G,C,I="#0F1F3D","#12B5A6","#E8A33D","#F7F4EE","#5B6B82"
FONT="""@font-face{font-family:P;src:url(PlexAr-Regular.ttf);font-weight:400}@font-face{font-family:P;src:url(PlexAr-Medium.ttf);font-weight:500}
@font-face{font-family:P;src:url(PlexAr-SemiBold.ttf);font-weight:600}@font-face{font-family:P;src:url(PlexAr-Bold.ttf);font-weight:700}
*{box-sizing:border-box;margin:0}body{font-family:P,Inter,sans-serif;direction:rtl;color:%s}"""%N
PIX=["XXXX.","....X","....X","...X.","XXX.."]
def pixel(sz=300,fg=N,ac=T,bg=None):
    u=sz/8;ox=(sz-5*u)/2;oy=(sz-5*u)/2;s=f'<svg width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}">'
    if bg: s+=f'<rect width="{sz}" height="{sz}" rx="{sz*.22}" fill="{bg}"/>'
    for r,row in enumerate(PIX):
        for c,ch in enumerate(row):
            if ch=="X":
                col=ac if (r==4 and c==0) else fg
                s+=f'<rect x="{ox+c*u}" y="{oy+r*u}" width="{u*.88}" height="{u*.88}" rx="{u*.16}" fill="{col}"/>'
    return s+'</svg>'
def glyph(sz=300,fg=N,ac=T,bg=None):
    s=f'<svg width="{sz}" height="{sz}" viewBox="0 0 300 300">'
    if bg: s+=f'<rect width="300" height="300" rx="66" fill="{bg}"/>'
    s+=f'<text x="150" y="235" font-family="P" font-weight="700" font-size="260" text-anchor="middle" fill="{fg}">د</text>'
    s+=f'<path d="M205 70 l34 22 l-34 22" fill="none" stroke="{ac}" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return s
def star(sz=300,fg=N,ac=T,bg=None):
    s=f'<svg width="{sz}" height="{sz}" viewBox="0 0 300 300">'
    if bg: s+=f'<rect width="300" height="300" rx="66" fill="{bg}"/>'
    import math
    pts=lambda r,rot:" ".join(f"{150+r*math.cos(math.radians(rot+a)):.1f},{150+r*math.sin(math.radians(rot+a)):.1f}" for a in range(0,360,90))
    s+=f'<polygon points="{pts(122,45)}" fill="none" stroke="{ac}" stroke-width="7"/><polygon points="{pts(122,0)}" fill="none" stroke="{ac}" stroke-width="7"/>'
    for a in range(0,360,45):
        x=150+122*math.cos(math.radians(a));y=150+122*math.sin(math.radians(a))
        s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{G}"/>'
    s+=f'<text x="150" y="205" font-family="P" font-weight="700" font-size="150" text-anchor="middle" fill="{fg}">د</text></svg>'
    return s
def lock(mark,fg=N,sub=I,sz=120):
    return f'<div style="display:flex;align-items:center;gap:22px;direction:ltr">{mark}<div style="direction:rtl;text-align:right"><div style="font-size:{sz*.62}px;font-weight:700;color:{fg};line-height:1">دراية</div><div style="font-family:Inter;font-size:{sz*.2}px;letter-spacing:.38em;color:{sub};margin-top:8px;font-weight:600">DARAYA</div></div></div>'
def board():
    sw=lambda c,n,r:f'<div style="flex:1"><div style="height:130px;border-radius:16px;background:{c};border:1px solid #0001"></div><div style="font-weight:700;margin-top:10px">{n}</div><div style="font-family:Inter;font-size:15px;color:{I};direction:ltr;text-align:right">{c}</div><div style="font-size:14px;color:{I}">{r}</div></div>'
    card=lambda t,inner,bg="#fff":f'<div style="background:{bg};border-radius:26px;padding:30px;display:flex;flex-direction:column;gap:18px;border:1px solid #0F1F3D12"><div style="font-size:18px;font-weight:600;color:{I}">{t}</div>{inner}</div>'
    return f"""<html><style>{FONT}body{{background:{C};width:1920px;padding:70px}}h1{{font-size:56px}}</style><body>
<div style="display:flex;justify-content:space-between;align-items:end;margin-bottom:40px"><div><div style="font-family:Inter;letter-spacing:.3em;color:{T};font-weight:700">BRAND BOARD · V1</div><h1>درايه — الهوية البصرية المقترحة</h1></div><div style="font-size:22px;color:{I}">معرفة تُبنى</div></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:26px">
{card("A · الحرف + المؤشر",f'<div style="display:flex;justify-content:center;padding:10px">{glyph(260,bg=N,fg="#fff",ac=T)}</div>'+lock(glyph(80,bg=N,fg="#fff"),sz=80)+f'<p style="color:{I};font-size:17px;line-height:1.7">حرف «د» مع سهم برمجي. الأوضح والأسهل في الاستخدام الصغير.</p>')}
{card("B · البكسل",f'<div style="display:flex;justify-content:center;padding:10px">{pixel(260,bg=N,fg="#fff",ac=G)}</div>'+lock(pixel(80,bg=N,fg="#fff",ac=G),sz=80)+f'<p style="color:{I};font-size:17px;line-height:1.7">«د» مبنية من وحدات صغيرة = التعلّم خطوة خطوة. الأكثر تقنية.</p>')}
{card("C · الزخرفة الدائرية",f'<div style="display:flex;justify-content:center;padding:10px">{star(260,bg=N,fg="#fff",ac=T)}</div>'+lock(star(80,bg=N,fg="#fff"),sz=80)+f'<p style="color:{I};font-size:17px;line-height:1.7">نجمة هندسية خليجية تتحول لدائرة منطقية. الأكثر هوية محلية.</p>')}
</div>
<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:26px;margin-top:26px">
{card("الألوان",f'<div style="display:flex;gap:16px">{sw(N,"Midnight","الأساسي")}{sw(T,"Teal","المميّز")}{sw(G,"Amber","الإنجاز / CTA")}{sw(C,"Cream","الخلفية")}{sw(I,"Slate","نص ثانوي")}</div>')}
{card("الخطوط",f'<div style="font-size:54px;font-weight:700;line-height:1.2">تعلّم لتبني</div><div style="font-size:22px;color:{I}">IBM Plex Sans Arabic — عربي</div><div style="font-family:Inter;font-size:34px;font-weight:700;direction:ltr;text-align:left">Learn to build. <span style="color:{T}">Inter</span></div><div style="font-family:monospace;direction:ltr;text-align:left;background:{N};color:{T};padding:12px 16px;border-radius:12px;font-size:20px">const daraya = know(&quot;how&quot;);</div>')}
</div></body></html>"""
def post(mark,bg=C):
    dark=bg==N;fg="#fff" if dark else N
    return f"""<html><style>{FONT}body{{width:1080px;height:1350px;background:{bg};position:relative;overflow:hidden}}
.dots{{position:absolute;inset:0;background-image:radial-gradient({'#ffffff22' if dark else '#0F1F3D14'} 2px,transparent 2px);background-size:36px 36px}}</style><body><div class="dots"></div>
<div style="position:absolute;top:70px;right:80px">{lock(mark,fg=fg,sub=T if dark else I,sz=90)}</div>
<div style="position:absolute;top:360px;right:80px;left:80px"><div style="color:{G};font-weight:700;font-size:34px;margin-bottom:26px">نصيحة برمجة — ١</div>
<div style="font-size:104px;font-weight:700;line-height:1.25;color:{fg}">الكود الأنظف<br>مش الأقصر<br><span style="color:{T}">هو الأوضح.</span></div>
<div style="margin-top:50px;background:{'#0b1730' if dark else N};color:{T};direction:ltr;text-align:left;padding:28px 34px;border-radius:22px;font-family:monospace;font-size:34px;line-height:1.6">// bad<br>x=a&gt;b?a:b<br>// clear<br>maxValue = max(a, b)</div></div>
<div style="position:absolute;bottom:70px;right:80px;left:80px;display:flex;justify-content:space-between;align-items:center"><div style="background:{G};color:{N};font-weight:700;font-size:34px;padding:18px 38px;border-radius:60px">احفظ البوست</div><div style="color:{I};font-size:28px">معرفة تُبنى</div></div></body></html>"""
def endcard(mark):
    return f"""<html><style>{FONT}body{{width:1080px;height:1920px;background:{N};position:relative}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(#ffffff1c 2px,transparent 2px);background-size:40px 40px}}</style><body><div class="dots"></div>
<div style="position:absolute;top:560px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:50px">{lock(mark,fg="#fff",sub=T,sz=170)}<div style="width:200px;height:6px;background:{G};border-radius:3px"></div>
<div style="color:#fff;font-size:60px;font-weight:600">تعلّم لتبني</div><div style="background:{G};color:{N};font-weight:700;font-size:52px;padding:26px 70px;border-radius:80px;margin-top:20px">تابعنا</div></div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome");pg=await b.new_page()
        async def shot(html,name,w,h):
            open("t.html","w").write(html);await pg.set_viewport_size({"width":w,"height":h});await pg.goto("file:///home/user/Vd/daraya/t.html");await pg.wait_for_timeout(400);await pg.screenshot(path=f"out/{name}.png",full_page=(h==0))
        await pg.set_viewport_size({"width":1920,"height":1400});open("t.html","w").write(board());await pg.goto("file:///home/user/Vd/daraya/t.html");await pg.wait_for_timeout(500);await pg.screenshot(path="out/00_brand_board.png",full_page=True)
        for k,(mk,tag) in enumerate([(glyph(110,bg=T,fg=N,ac=N),"A"),(pixel(110,bg=N,fg="#fff",ac=G),"B"),(star(110,bg=N,fg="#fff"),"C")]):
            await shot(post(mk if False else (glyph(110,bg=T,fg=N,ac=N) if tag=="A" else pixel(110,bg=T,fg=N,ac=N) if tag=="B" else star(110,bg=T,fg=N,ac=N)) if False else mk,N if tag=="A" else C),f"post_{tag}",1080,1350)
            big={"A":glyph(190,bg=T,fg=N,ac=N),"B":pixel(190,bg=N,fg="#fff",ac=G),"C":star(190,bg=N,fg="#fff")}[tag]
            await shot(endcard(big),f"endcard_{tag}",1080,1920)
        await b.close()
asyncio.run(main())
