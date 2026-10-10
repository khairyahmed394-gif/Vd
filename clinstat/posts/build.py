"""ClinStat static-post template system (1080x1350, 4:5, Arabic RTL) + the cards from the 3-month content calendar.
usage: python3 build.py            -> renders every card in CARDS to out/*.png (1080x1350) and out/2x/*.png (2160x2700)
Brand (from the calendar's formula guide): navy #0B1F33, deep green #103D2E, gold #A8854E, warm sand #F7F4ED. Font: IBM Plex Sans Arabic."""
import json, os, re, sys, html
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, GREEN, GOLD, SAND = "#0B1F33", "#103D2E", "#A8854E", "#F7F4ED"
LG = json.load(open(os.path.join(HERE, "logo_vec.json")))

# ------------------------------------------------------------------ helpers
LAT = re.compile(r"\(?[A-Za-z0-9~][A-Za-z0-9 .,<>=/+()%~\-'’·–]*[A-Za-z0-9)%]|\(?[A-Za-z0-9~]")
def t(s):
    """escape + isolate Latin runs so punctuation does not jump around in RTL text"""
    out, pos = [], 0
    for m in LAT.finditer(s):
        out.append(html.escape(s[pos:m.start()], quote=False)); out.append(f'<bdi dir="ltr">{html.escape(m.group(0), quote=False)}</bdi>'); pos = m.end()
    out.append(html.escape(s[pos:], quote=False)); return "".join(out)

def logo(light=False, w=250):
    x0, x1, y0, y1 = LG["mark"]["x0"], LG["word"]["x1"], LG["mark"]["y0"], LG["mark"]["y1"]
    def col(c):
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        return SAND if light and (0.299 * r + 0.587 * g + 0.114 * b) < 90 else c
    parts = [f'<circle cx="{d["cx"]}" cy="{d["cy"]}" r="{d["r"]}" fill="{col(d["color"])}"/>' for d in LG["dots"]]
    parts += [f'<path d="{c["d"]}" fill="{col(c["color"])}" fill-rule="evenodd"/>' for c in LG["chev"]]
    parts.append(f'<path d="{LG["divider"]["d"]}" fill="{col(LG["divider"]["color"])}"/>')
    for k in ("clin", "stat", "res"):
        parts += [f'<path d="{l["d"]}" fill="{col(l["color"])}" fill-rule="evenodd"/>' for l in LG[k]]
    h = w * (y1 - y0) / (x1 - x0)
    return f'<svg class="logo" dir="ltr" width="{w}" height="{h:.0f}" viewBox="{x0} {y0} {x1-x0} {y1-y0}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'

def chevrons(color, op):   # big watermark built from the logo's three chevrons
    paths = "".join(f'<path d="{c["d"]}" fill="{color}" fill-rule="evenodd"/>' for c in LG["chev"])
    return f'<svg class="wm" dir="ltr" viewBox="{LG["mark"]["x0"]} {LG["mark"]["y0"]+70} {LG["mark"]["x1"]-LG["mark"]["x0"]} {LG["mark"]["y1"]-LG["mark"]["y0"]-70}" style="opacity:{op}" xmlns="http://www.w3.org/2000/svg">{paths}</svg>'

ICON_SAVE = '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-6-4-6 4z"/></svg>'
ICON_SEND = '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 3 10 14"/><path d="M21 3l-7 18-4-7-7-4z"/></svg>'

CSS = f"""
@font-face{{font-family:PX;src:url(fonts/PlexAr-Regular.ttf);font-weight:400}}
@font-face{{font-family:PX;src:url(fonts/PlexAr-Medium.ttf);font-weight:500}}
@font-face{{font-family:PX;src:url(fonts/PlexAr-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:PX;src:url(fonts/PlexAr-Bold.ttf);font-weight:700}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:{SAND}}}
body{{font-family:PX,sans-serif;direction:rtl;color:{NAVY}}}
.card{{position:relative;width:1080px;height:1350px;padding:84px 88px 0;overflow:hidden}}
.card.sand{{background:{SAND};color:{NAVY}}}
.card.navy{{background:{NAVY};color:{SAND}}}
.card.green{{background:{GREEN};color:{SAND}}}
.wm{{position:absolute;left:-150px;top:340px;width:760px;pointer-events:none}}
.head{{display:flex;justify-content:space-between;align-items:center;height:60px}}
.tag{{font-size:27px;font-weight:600;letter-spacing:0;color:{GOLD};border:2px solid {GOLD};border-radius:40px;padding:8px 26px 10px}}
.cnt{{font-size:28px;font-weight:500;opacity:.7}}
.foot{{position:absolute;left:88px;right:88px;bottom:70px;display:flex;justify-content:space-between;align-items:center}}
.foot .cta{{font-size:28px;font-weight:500;opacity:.78}}
.rule{{width:132px;height:7px;background:{GOLD};border-radius:4px}}
h1,h2{{font-weight:700;line-height:1.22}}
bdi{{unicode-bidi:isolate}}
.rows{{position:absolute;right:88px;left:88px}}
.row{{display:flex;gap:34px;align-items:flex-start;padding:40px 0;border-top:2px solid rgba(11,31,51,.12)}}
.row:first-child{{border-top:0}}
.num{{flex:0 0 100px;height:100px;border-radius:50%;background:{NAVY};color:{SAND};font-size:44px;font-weight:700;display:flex;align-items:center;justify-content:center;padding-top:4px}}
.num.gold{{background:{GOLD};color:{NAVY}}}
.row h3{{font-size:45px;font-weight:600;line-height:1.36}}
.row p{{font-size:33px;font-weight:400;line-height:1.45;margin-top:12px;color:#4A5A66}}
.navy .row,.green .row{{border-color:rgba(247,244,237,.16)}}
.navy .row p,.green .row p{{color:rgba(247,244,237,.74)}}
.pill{{display:inline-flex;align-items:center;gap:16px;border-radius:60px;padding:22px 40px 24px;font-size:36px;font-weight:600}}
"""

def shell(cls, body, wm=None):
    return f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="card {cls}">{wm or ""}{body}</div></body></html>'

def head(tag, cnt=None):
    return f'<div class="head"><span class="tag">{t(tag)}</span><span class="cnt" dir="ltr">{cnt or ""}</span></div>'

def foot(cta, light=False):
    return f'<div class="foot"><span class="cta">{t(cta)}</span>{logo(light)}</div>'

# ------------------------------------------------------------------ templates
def tpl_cover(c):
    big = c["big"]
    return shell("navy", f"""{head(c["tag"], c["cnt"])}
<div style="position:absolute;right:88px;left:88px;top:250px">
  <div style="font-size:400px;font-weight:700;line-height:.9;color:{GOLD};letter-spacing:-6px;text-align:right" dir="ltr" class="bignum">{big}</div>
  <h1 style="font-size:84px;margin-top:20px">{t(c["title"])}</h1>
  <div class="rule" style="margin:36px 0 34px"></div>
  <p style="font-size:42px;line-height:1.45;font-weight:400;opacity:.88;max-width:860px">{t(c["hook"])}</p>
</div>
{foot(c["foot"], True)}""", chevrons(SAND, .05))

def tpl_points(c):
    rows = "".join(f'<div class="row"><div class="num{" gold" if c.get("gold") else ""}">{n}</div><div><h3>{t(h)}</h3>{f"<p>{t(p)}</p>" if p else ""}</div></div>' for n, h, p in c["rows"])
    return shell(c.get("bg", "sand"), f"""{head(c["tag"], c["cnt"])}
<div style="margin-top:56px"><h2 style="font-size:78px">{t(c["title"])}</h2><div class="rule" style="margin-top:26px"></div></div>
<div class="rows" style="top:{c.get("top", 372)}px">{rows}</div>
{foot(c["foot"])}""")

def tpl_closing(c):
    return shell("green", f"""{head(c["tag"], c["cnt"])}
<div style="position:absolute;right:88px;left:88px;top:250px">
  <h1 style="font-size:104px">{t(c["title"])}</h1>
  <div class="rule" style="margin:36px 0 40px"></div>
  <p style="font-size:44px;line-height:1.5;opacity:.92;max-width:860px">{t(c["body"])}</p>
  <div style="display:flex;gap:26px;margin-top:70px">
    <span class="pill" style="background:{GOLD};color:{NAVY}">{ICON_SAVE}<span>{t(c["btn1"])}</span></span>
    <span class="pill" style="border:3px solid {SAND}">{ICON_SEND}<span>{t(c["btn2"])}</span></span>
  </div>
</div>
<div style="position:absolute;right:88px;left:88px;bottom:178px;font-size:30px;opacity:.7;line-height:1.5">{t(c["note"])}</div>
{foot(c["foot"], True)}""", chevrons(SAND, .05))

def tpl_list(c):   # one-image list card (5 questions)
    rows = "".join(f'<div class="row" style="padding:19px 0"><div class="num gold" style="flex:0 0 74px;height:74px;font-size:34px">{n}</div><div><h3 style="font-size:36px;line-height:1.34">{t(h)}</h3></div></div>' for n, h in c["rows"])
    return shell("sand", f"""{head(c["tag"], None)}
<div style="margin-top:44px"><h2 style="font-size:70px;line-height:1.25">{t(c["title"])}</h2><div class="rule" style="margin-top:24px"></div></div>
<div class="rows" style="top:{c.get("top", 436)}px">{rows}</div>
<div style="position:absolute;right:88px;left:88px;bottom:176px;background:{GREEN};color:{SAND};border-radius:20px;padding:26px 36px 30px;font-size:33px;line-height:1.45;font-weight:500">{t(c["band"])}</div>
{foot(c["foot"])}""")

def tpl_quote(c):
    rows = "".join(f'<div class="row" style="padding:34px 0"><div class="num gold" style="flex-basis:84px;height:84px;font-size:38px">{n}</div><div><h3 style="font-size:54px;font-weight:700">{t(h)}</h3></div></div>' for n, h in c["rows"])
    return shell("green", f"""{head(c["tag"], None)}
<div style="position:absolute;right:88px;top:200px;font-size:300px;line-height:1;color:{GOLD};opacity:.9;font-weight:700" dir="ltr">”</div>
<div style="position:absolute;right:88px;left:88px;top:430px"><h1 style="font-size:84px;line-height:1.25">{t(c["title"])}</h1><div class="rule" style="margin-top:28px"></div></div>
<div class="rows" style="top:706px">{rows}</div>
{foot(c["foot"], True)}""", chevrons(SAND, .05))

def tpl_case(c):
    return shell("navy", f"""{head(c["tag"], None)}
<div style="position:absolute;right:88px;left:88px;top:230px">
  <div style="display:flex;align-items:flex-end;gap:36px;justify-content:space-between" dir="rtl">
    <div><div class="bignum" dir="ltr" style="font-size:300px;font-weight:700;line-height:.95;color:rgba(247,244,237,.55)">{c["n1"]}</div><div style="font-size:44px;font-weight:600;opacity:.8;margin-top:6px">{t(c["l1"])}</div></div>
    <div style="font-size:120px;color:{GOLD};padding-bottom:70px" dir="ltr">←</div>
    <div><div class="bignum" dir="ltr" style="font-size:300px;font-weight:700;line-height:.95;color:{GOLD}">{c["n2"]}</div><div style="font-size:44px;font-weight:600;margin-top:6px">{t(c["l2"])}</div></div>
  </div>
  <div class="rule" style="margin:70px 0 40px"></div>
  <p style="font-size:56px;line-height:1.38;font-weight:600">{t(c["body"])}</p>
</div>
{foot(c["foot"], True)}""", chevrons(SAND, .05))

def tpl_stats(c):
    blocks = "".join(f'<div style="padding:46px 0;border-top:2px solid rgba(247,244,237,.16)"><div dir="ltr" style="text-align:right;font-size:230px;font-weight:700;line-height:1;color:{GOLD}">{n}</div><div style="font-size:54px;font-weight:600;line-height:1.3;margin-top:8px">{t(l)}</div></div>' for n, l in c["stats"])
    return shell("navy", f"""{head(c["tag"], None)}
<div style="position:absolute;right:88px;left:88px;top:208px"><h2 style="font-size:70px">{t(c["title"])}</h2><div class="rule" style="margin-top:24px;margin-bottom:34px"></div>{blocks}</div>
{foot(c["foot"], True)}""", chevrons(SAND, .04))

TPL = dict(cover=tpl_cover, points=tpl_points, closing=tpl_closing, list=tpl_list, quote=tpl_quote, case=tpl_case, stats=tpl_stats)

# ------------------------------------------------------------------ content (from the calendar; wording follows the file's tone)
F = "احفظه وشاركه مع فريقك"
GROUPS = [
 ("التصميم", "محور 1 من 5", [
   ("1", "الفرضية والـprimary outcome اتحددوا قبل جمع الداتا؟", "لو اتحددوا بعد ما شفت النتيجة، دي مش اختبار."),
   ("2", "حجم العيّنة اتحسب مسبقًا؟", "الدراسة الصغيرة بتفوّت التأثير الحقيقي."),
   ("3", "مجموعة المقارنة مناسبة، والـconfounders متحكَّم فيها؟", "من غير كده الفرق ممكن يكون مش حقيقي.")]),
 ("جودة الداتا", "محور 2 من 5", [
   ("4", "حسبت البيانات الناقصة وعالجتها بطريقة واضحة؟", "الحذف الصامت ممكن يشوّه النتيجة."),
   ("5", "فحصت التكرارات والقيم الشاذة وأخطاء الإدخال؟", "نتيجة قوية ممكن تطلع من خطأ إدخال."),
   ("6", "القياس بنفس الطريقة ودقيق لكل المشاركين؟", "اختلاف طريقة القياس بيعمل فروق وهمية.")]),
 ("التحليل", "محور 3 من 5", [
   ("7", "فحصت افتراضات الاختبار قبل ما تشغّله؟", "الـp-value بتاعك ملهوش قيمة لو تخطيت الخطوة دي."),
   ("8", "اخترت الـtest على أساس التصميم، مش على أساس p < 0.05؟", ""),
   ("9", "حسبت تعدد الاختبارات (multiple testing)؟", "20 نتيجة عند 0.05 غالبًا هتدّيك نتيجة 'اتكتشفت' صدفة.")]),
 ("التفسير", "محور 4 من 5", [
   ("10", "ذكرت حجم التأثير وفترة الثقة 95%، مش الـp-value بس؟", ""),
   ("11", "فرّقت بين الدلالة الإحصائية والأهمية الإكلينيكية؟", "ممكن تطلع معنوية ومفيش لها قيمة للمريض."),
   ("12", "قلت 'ارتباط' ولا 'بيسبب'؟", "الارتباط مش سببية.")]),
 ("التقرير والإتاحة", "محور 5 من 5", [
   ("13", "التزمت بالـreporting guideline المناسب؟ (CONSORT, STROBE, PRISMA, STARD)", ""),
   ("14", "عرضت كل النتائج المخطط لها، حتى غير المعنوية؟", ""),
   ("15", "خطة التحليل موثّقة وممكن حد تاني يعيد النتيجة؟", "")]),
]
N = 7
CARDS = {
 "wk01_mon_s1_cover": dict(t="cover", tag="نقاط الموثوقية", cnt=f"1 / {N}", big="15", title="نقطة لنتيجة بحثية موثوقة", hook="15 فحص بيفرّقوا بين النتيجة الحقيقية والإنذار الكاذب.", foot="اسحب لقراءة الـ15 فحص"),
}
for i, (title, tag, rows) in enumerate(GROUPS):
    CARDS[f"wk01_mon_s{i+2}_{['design','data','analysis','interpretation','reporting'][i]}"] = dict(
        t="points", tag=tag, cnt=f"{i+2} / {N}", title=title, rows=rows, foot=F if i == 4 else "اسحب للمحور التالي")
CARDS["wk01_mon_s7_save"] = dict(t="closing", tag="قبل الـSubmit", cnt=f"{N} / {N}", title="احفظه قبل ما تقدّم.",
    body="اعدّ الفحوصات بتاعتك. أي 'لأ' هي نقطة محتاجة مراجعة قبل ما الدراسة تروح للمحرر.",
    btn1="احفظ البوست", btn2="شاركه مع فريقك", note="ClinStat Research · Data Integrity – Accelerated Trials", foot="")
CARDS["wk03_thu_five_questions"] = dict(t="list", tag="اختيار الـbiostatistician", title="5 أسئلة قبل ما تتعاقد مع biostatistician",
    rows=[("1", "بيسأل عن سؤالك البحثي قبل ما يسأل عن الداتا؟"), ("2", "يقدر يشرح الطريقة بلغة بسيطة، مش مصطلحات بس؟"),
          ("3", "بيراجع تصميم الدراسة، ولا بيحلّل اللي اتجمع بس؟"), ("4", "بيوثّق كل خطوة عشان حد تاني يقدر يعيدها؟"), ("5", "سجل نشره العلمي بيقول إيه؟")],
    band="عندنا: كل عضو في الفريق عنده 50+ ورقة وh-index 5+.", foot="شاركه مع زميل بيختار statistician")
CARDS["wk05_mon_ownership"] = dict(t="quote", tag="طريقة شغلنا", title="الباحث بيحتفظ بـ:", rows=[("1", "الملكية الفكرية"), ("2", "الموافقة النهائية"), ("3", "المسؤولية")], foot="اقرأ طريقة شغلنا (اللينك في الكابشن)")
CARDS["wk06_mon_case_study"] = dict(t="case", tag="دراسة حالة", n1="10+", l1="رفضات", n2="1", l2="قبول", body="اترفضت 10+ مرات. واتقبلت من أول مجلة بعد المراجعة.", foot="اقرأ دراسة الحالة كاملة (اللينك في الكابشن)")
CARDS["wk11_thu_partnership"] = dict(t="stats", tag="الشراكات المؤسسية", title="أرقام الشراكة", stats=[("~100", "ورقة كل ربع سنة"), ("80%", "منشورة في مجلات عالية التأثير")], foot="استفسارات الشراكات المؤسسية (اللينك في الكابشن)")

# ------------------------------------------------------------------ render + audit
AUDIT = """() => { const out=[]; const card=document.querySelector('.card'); const H=1350;
 document.querySelectorAll('h1,h2,h3,p,.tag,.cnt,.cta,.pill,.num,.rule').forEach(e=>{const r=e.getBoundingClientRect(); if(r.width<2)return;
   const foot=document.querySelector('.foot'); const ft=foot?foot.getBoundingClientRect().top:H;
   if(!e.closest('.foot') && r.bottom>ft-12 && !e.closest('[data-foot-ok]')) out.push('OVERLAPS FOOTER: '+e.tagName+' '+e.textContent.slice(0,30)+' bottom '+Math.round(r.bottom)+' > '+Math.round(ft));
   if(r.left<60||r.right>1020) out.push('MARGIN: '+e.tagName+' '+e.textContent.slice(0,24)+' x '+Math.round(r.left)+'-'+Math.round(r.right));});
 const rows=[...document.querySelectorAll('.row')]; for(let i=0;i<rows.length-1;i++){const a=rows[i].getBoundingClientRect(),b=rows[i+1].getBoundingClientRect(); if(a.bottom>b.top+2) out.push('ROW OVERLAP '+i);}
 return out; }"""
def render(only=None):
    os.makedirs(os.path.join(HERE, "out", "2x"), exist_ok=True); bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files", "--font-render-hinting=none"])
        for name, c in CARDS.items():
            if only and name not in only: continue
            f = os.path.join(HERE, f"_{name}.html"); open(f, "w").write(TPL[c["t"]](c))
            for scale, outp in ((1, f"out/{name}.png"), (2, f"out/2x/{name}.png")):
                pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=scale); pg.goto("file://" + f); pg.wait_for_timeout(250)
                pg.evaluate("document.fonts.ready")
                if scale == 1:
                    for m in pg.evaluate(AUDIT): bad += 1; print(f"[{name}] {m}")
                pg.screenshot(path=os.path.join(HERE, outp)); pg.close()
            os.remove(f); print("ok", name)
        b.close()
    print("layout problems:", bad)
if __name__ == "__main__": render(sys.argv[1:] or None)
