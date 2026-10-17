"""Builds NEXORA_Company_Profile_AR.pdf (18 pages, RTL, same design system as the English profile). python3 build.py"""
import os, html
from playwright.sync_api import sync_playwright
from content import PILLARS
HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, TEAL, BG, MUTED, LINE = "#101C2C", "#19C6B4", "#F5F7FA", "#536273", "#DDE2E8"
TAG = "ابنِ أفضل. انمُ بذكاء."
CSS = f"""
@font-face{{font-family:P;src:url(fonts/PlexAr-Regular.ttf);font-weight:400}}@font-face{{font-family:P;src:url(fonts/PlexAr-Medium.ttf);font-weight:500}}
@font-face{{font-family:P;src:url(fonts/PlexAr-SemiBold.ttf);font-weight:600}}@font-face{{font-family:P;src:url(fonts/PlexAr-Bold.ttf);font-weight:700}}
@page{{size:827px 1169px;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:P,sans-serif;direction:rtl;color:{NAVY};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:827px;height:1169px;position:relative;overflow:hidden;background:{BG};page-break-after:always;break-after:page}}
.dark{{background:{NAVY};color:#fff}}.ab{{position:absolute}}
.hd{{position:absolute;top:40px;right:60px;left:60px;display:flex;justify-content:space-between;align-items:center;height:26px}}
.hd .lg{{display:flex;align-items:center;gap:10px;font-weight:600;letter-spacing:3px;font-size:13px;direction:ltr}}.hd img{{height:22px}}.hd .pr{{font-size:12px;color:{MUTED}}}
.hl{{position:absolute;top:80px;right:60px;left:60px;border-top:1px solid {LINE}}}.dark .hl,.dark .fl{{border-color:rgba(255,255,255,.14)}}
.fl{{position:absolute;top:1106px;right:60px;left:60px;border-top:1px solid {LINE}}}
.ft{{position:absolute;top:1117px;right:60px;left:60px;display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}.dark .ft,.dark .hd .pr{{color:#9FB0C3}}
.k{{position:absolute;right:60px;top:106px;color:{TEAL};font-weight:700;font-size:13px}}
h1{{position:absolute;right:60px;left:60px;top:132px;font-size:36px;line-height:1.35;font-weight:700}}
.t{{color:{MUTED};font-size:14.5px;line-height:1.85}}.dark .t{{color:#B9C6D6}}
.card{{position:absolute;background:#fff;border:1px solid {LINE};border-right:5px solid {TEAL};padding:16px 22px 14px 18px}}
.card .n{{position:absolute;right:20px;top:20px;color:{TEAL};font-weight:700;font-size:15px}}
.card h3{{font-size:16.5px;font-weight:700;margin-right:46px;line-height:1.5}}.card p{{font-size:13px;color:{MUTED};line-height:1.7;margin-right:46px;margin-top:6px}}
.box{{position:absolute;background:{NAVY};color:#fff}}.lab{{font-size:12px;font-weight:700;color:{TEAL};margin-bottom:10px}}
ul.b{{list-style:none}}ul.b li{{position:relative;padding-right:18px;font-size:13.5px;line-height:1.7;margin-bottom:5px}}ul.b li:before{{content:"";position:absolute;right:0;top:9px;width:6px;height:6px;background:{NAVY}}}
ul.d li:before{{border-radius:50%;background:{TEAL}}}.dark ul.b li:before{{background:#fff}}
.dot{{display:inline-block;width:14px;height:14px;border-radius:50%;background:{TEAL}}}
.note{{position:absolute;right:60px;left:60px;border:1.5px solid {TEAL};background:#E4F7F4;border-radius:8px;padding:9px 16px;font-size:11.5px;color:{MUTED};font-style:normal}}
.fmt{{position:absolute;right:60px;left:60px;top:955px;height:62px;background:#E4F7F4;border-right:5px solid {TEAL};padding:12px 20px;font-size:13px;line-height:1.7}}.fmt b{{font-size:12px;color:{NAVY};margin-left:12px}}
.fn{{position:absolute;right:60px;left:60px;top:1038px;font-size:10.5px;color:{MUTED};line-height:1.6}}
"""
def hdr(n, dark=False):
    return (f'<div class="hd"><div class="lg"><img src="img/mark.png"><span>NEXORA</span></div><div class="pr">ملف الشركة</div></div><div class="hl"></div>'
            f'<div class="fl"></div><div class="ft"><span>{TAG}</span><span style="direction:ltr">{n:02d} / 18</span></div>')
def page(n, body, dark=False, head=True): return f'<section class="page{" dark" if dark else ""}">{hdr(n, dark) if head else ""}{body}</section>'
def kt(k, title, top=None): return f'<div class="k">{k}</div><h1{f" style=top:{top}px" if top else ""}>{title}</h1>'
def li(items, cls="b"): return f'<ul class="{cls}">' + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"
def constellation(pts, lines, w=827, h=1169, mirror=False):
    P = [(w - x if mirror else x, y) for x, y in pts]
    s = "".join(f'<line x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" stroke="{TEAL}" stroke-opacity=".35" stroke-width="1.5"/>' for a, b in lines)
    s += "".join(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{TEAL}"/>' for x, y in P)
    return f'<svg class="ab" style="left:0;top:0" width="{w}" height="{h}">{s}</svg>'
pages = []
# ---- 1 cover
cover_pts = [(520, 760), (640, 700), (730, 790), (600, 860), (700, 930), (540, 960), (770, 1020)]
pages.append(page(1, constellation(cover_pts, [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6)], mirror=True) +
 '<img class="ab" src="img/logo_full.png" style="right:60px;top:120px;width:480px">' +
 f'<div class="ab" style="right:60px;top:436px;width:90px;height:4px;background:{TEAL}"></div>'
 f'<div class="ab" style="right:60px;top:466px;font-size:28px;font-weight:700;color:{TEAL}">{TAG}</div>'
 '<div class="ab" style="right:60px;top:520px;font-size:19px;color:#CBD5E1">شريك نمو الأعمال والأداء</div>'
 '<div class="ab" style="right:60px;top:1020px;font-size:13px;font-weight:700;color:#fff">ملف الشركة</div>'
 '<div class="ab" style="right:60px;top:1050px;font-size:13px;color:#9FB0C3;line-height:1.8">الاستراتيجية · التسويق · العمليات · التدريب<br>مصر · [الإصدار / السنة قيد التأكيد]</div>', dark=True, head=False))
# ---- 2 who we are
toc = [("03", "التحدي في الأعمال"), ("04", "نهجنا"), ("05", "إطار الخدمات"), ("06–09", "محفظة الخدمات"), ("10", "نموذج الأعمال المتكامل"), ("11", "نماذج التعاقد"),
       ("12", "المنهجية والحوكمة"), ("13", "القياس ومؤشرات الأداء"), ("14", "القطاعات التي ندعمها"), ("15", "لماذا NEXORA"), ("16", "سيناريوهات التعاون"), ("17", "عملية الشراكة")]
def tocrow(a, b): return f'<div style="display:flex;gap:18px;font-size:13.5px;height:32px;align-items:center"><b style="color:{TEAL};width:44px">{a}</b><span>{b}</span></div>'
tocR = "".join(tocrow(a, b) for a, b in toc[:6]); tocL = "".join(tocrow(a, b) for a, b in toc[6:])
pages.append(page(2, kt("من نحن", "شريك نمو يربط الاستراتيجية بالتنفيذ") +
 f'<div class="ab" style="right:60px;top:262px;width:430px"><div style="font-size:17.5px;font-weight:700;line-height:1.85">NEXORA شركة لتطوير الأعمال مقرها مصر. نساعد أصحاب الأعمال وفرق الإدارة على تحويل طموحات النمو إلى خطط منظمة، وأنظمة عمل فعّالة، وفرق قادرة، وتقدّم قابل للقياس.</div>'
 '<p class="t" style="margin-top:20px">معظم الشركات النامية لا ينقصها الجهد، بل ينقصها التوافق. التسويق يعمل دون اتجاه تجاري واضح، والمتابعة في المبيعات تعتمد على الأفراد، والعمليات تسير بالعادة لا بالإجراء، والقرارات تُتخذ دون مؤشرات موثوقة.</p>'
 '<p class="t" style="margin-top:14px">تعمل NEXORA عبر أربعة مجالات مترابطة: الاستراتيجية وتطوير الأعمال، والتسويق ونمو العلامة التجارية، والعمليات وإدارة الأداء، والتدريب المؤسسي. نقيّم أين يضيع الأداء، ونتفق مع القيادة على الأولويات، وندعم تنفيذ الخطط والعمليات والمهارات اللازمة للتحسين.</p>'
 '<p class="t" style="margin-top:14px">نخدم المنشآت الصغيرة والمتوسطة، والشركات الناشئة، والشركات القائمة، والأعمال الخدمية في مصر، بنيّة دعم العملاء في الشرق الأوسط ودول الخليج.</p></div>'
 f'<div class="box" style="left:60px;top:262px;width:212px;height:490px;padding:30px 26px"><div class="lab" style="line-height:1.6">لماذا يهم التكامل</div>' +
 "".join(f'<div style="display:flex;align-items:center;gap:14px;height:56px;font-size:15px;font-weight:600"><span class="dot"></span>{x}</div>' for x in ["الاستراتيجية", "التسويق", "المبيعات", "العمليات", "الأفراد", "القياس"]) +
 f'<div style="margin-top:22px;font-size:12.5px;color:#9FB0C3;line-height:1.7">يستمر النمو حين تدعم كل وظيفة الوظيفة التي تليها.</div></div>'
 f'<div class="ab" style="right:60px;left:60px;top:792px;border-top:1px solid {LINE}"></div><div class="ab lab" style="right:60px;top:812px">في هذا الملف</div>'
 f'<div class="ab" style="right:60px;top:844px;width:340px">{tocR}</div>'
 f'<div class="ab" style="right:420px;top:844px;width:340px">{tocL}</div>'))
# ---- 3 challenge
CH = [("تسويق بلا استراتيجية", "نشاط كثيف ومرئي، لكنه غير مرتبط بهدف تجاري أو بعميل محدد."), ("مبيعات بلا متابعة", "العملاء المحتملون يصلون ثم يضيعون. المتابعة تعتمد على من هو متاح، لا على إجراء."),
      ("أعمال تعيش في عقول الأفراد", "المهام الأساسية تعتمد على ذاكرة الأفراد. وحين يغادر شخص، يغادر الأداء معه."), ("فرق بلا تدريب منظم", "يتعلم الموظفون بالتجربة والخطأ، وتختلف المعايير من شخص لآخر."),
      ("مسؤوليات غير واضحة", "الأدوار متداخلة، والتوقعات غير مكتوبة، والمساءلة صعبة."), ("قرارات بلا مؤشرات", "يقرر الملاك بالحدس لأن بيانات الأداء الموثوقة لا تُجمع ولا تُراجع."), ("نمو يستنزف الهامش", "مزيد من العملاء والموظفين يعني تكلفة وتعقيدًا أكبر دون ربحية أفضل.")]
cs = ""
for i, (a, b) in enumerate(CH):
    if i < 6: x = 60 if i % 2 else 427; y = 305 + (i // 2) * 138; w, h = 340, 120
    else: x, y, w, h = 60, 305 + 3 * 138, 707, 120
    cs += f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span class="n">0{i+1}</span><h3>{a}</h3><p>{b}</p></div>'
pages.append(page(3, kt("التحدي في الأعمال", "النمو يضيف التعقيد قبل أن يضيف الربح") + '<p class="t ab" style="right:60px;left:60px;top:238px;font-size:13.5px">هذه أنماط شائعة في الشركات النامية بالسوق المصري، تُعرض كتحديات سوقية لا كنتائج عن أي منشأة بعينها.</p>' + cs +
 f'<div class="box" style="right:60px;left:60px;top:875px;height:176px;padding:28px 34px"><div class="lab">الفكرة المحورية</div><div style="font-size:18px;font-weight:600;line-height:1.85">يتحسن أداء الأعمال حين تعمل المنشأة كنظام واحد متكامل: استراتيجية واضحة، ومحرك تسويق يغذيها، وعملية مبيعات تحوّل الاهتمام إلى عملاء، وعمليات تنفذ باتساق، وأفراد مدرَّبون على تشغيلها.</div></div>'))
# ---- 4 approach (diagram mirrored for RTL)
STG = [("01", "افهم", "تقييم النشاط والسوق والأهداف والتحديات الحالية.", 413, 400), ("02", "خطّط", "تحديد الأولويات والفرص والأهداف القابلة للقياس.", 253, 492), ("03", "نظّم", "تصميم العمليات وسير العمل والمسؤوليات والأنظمة.", 253, 677),
       ("04", "فعّل", "دعم تنفيذ المبادرات المتفق عليها.", 413, 770), ("05", "قِس", "تقييم الأداء مقابل مؤشرات الأداء المتفق عليها.", 573, 677), ("06", "حسّن", "سدّ الفجوات والتحسين بناءً على النتائج.", 573, 492)]
dg = f'<svg class="ab" style="left:0;top:0" width="827" height="1169"><circle cx="413" cy="585" r="185" fill="none" stroke="{TEAL}" stroke-width="1.6" stroke-dasharray="6 6"/>'
for n, a, b, x, y in STG: dg += f'<circle cx="{x}" cy="{y}" r="32" fill="{NAVY}" stroke="{TEAL}" stroke-width="2"/><text x="{x}" y="{y+6}" text-anchor="middle" fill="{TEAL}" font-size="17" font-weight="700" font-family="P">{n}</text>'
dg += "</svg>"
for n, a, b, x, y in STG:
    if x == 413: pos = f"left:{x-110}px;width:220px;text-align:center;top:{y-92 if y<500 else y+42}px"
    elif x < 413: pos = f"left:{x-32-10-185}px;width:185px;text-align:right;top:{y-24}px"
    else: pos = f"left:{x+32+10}px;width:185px;text-align:left;top:{y-24}px"
    if x > 413: pos = pos.replace("text-align:left", "text-align:right").replace(f"left:{x+42}px", f"left:{x+42}px")
    dg += f'<div class="ab" style="{pos}"><div style="font-size:16.5px;font-weight:700">{a}</div><div style="font-size:11.5px;color:#B9C6D6;line-height:1.6;margin-top:3px">{b}</div></div>'
pages.append(page(4, kt("نهجنا", "ست مراحل في دورة واحدة مستمرة", 130) + '<p class="t ab" style="right:60px;left:60px;top:205px;font-size:13.5px">يتبع كل تعاون مع NEXORA منطق الأداء نفسه. ويعتمد عمق كل مرحلة، ومدى دعمنا للتنفيذ مباشرة، على النطاق المتفق عليه مع العميل.</p>' + dg +
 '<div class="ab" style="left:344px;width:140px;top:565px;text-align:center;font-size:12px;font-weight:700;color:#fff;line-height:1.7">أداء<br>الأعمال</div>' +
 f'<div class="ab" style="right:60px;left:60px;top:900px;height:156px;background:#17273A;padding:22px 30px"><div class="lab">ماذا يعني ذلك للعملاء</div>{li(["التوصيات مرتبطة بأهداف يمكن قياسها.", "التنفيذ مخطط له بمسؤولين محددين، لا يُترك كنصيحة.", "النتائج تغذي الدورة التالية، فيستمر التحسن بعد المشروع الأول."])}</div>', dark=True))
# ---- 5 framework
PIL = [("01", "الاستراتيجية وتطوير الأعمال", "أين ننمو، وكيف ستنافس المنشأة.", "الاتجاه", True), ("02", "التسويق ونمو العلامة التجارية", "من نصل إليه، وماذا نقول، وكيف نولّد طلبًا مؤهلًا.", "الطلب", False),
       ("03", "العمليات وإدارة الأداء", "كيف يُنجز العمل باتساق وكفاءة ومساءلة.", "التنفيذ", False), ("04", "التدريب المؤسسي وتنمية القدرات", "المهارات التي يحتاجها الأفراد لتشغيل النظام جيدًا.", "القدرات", True)]
pc = ""
for i, (n, a, b, tg, dk) in enumerate(PIL):
    x = 427 if i % 2 == 0 else 60; y = 310 + (i // 2) * 285
    st = f"background:{NAVY};color:#fff" if dk else "background:#fff;border:1px solid " + LINE
    pc += f'<div class="ab" style="left:{x}px;top:{y}px;width:340px;height:255px;{st};padding:30px"><div class="lab">الركيزة {n}</div><div style="font-size:21px;font-weight:700;line-height:1.5;margin-top:4px">{a}</div><div style="margin-top:26px;font-size:13.5px;line-height:1.8;color:{"#C7D2E0" if dk else MUTED}">{b}</div><div style="position:absolute;bottom:26px;right:30px;font-size:12px;font-weight:700;color:{"#9FB0C3" if dk else MUTED}">{tg}</div></div>'
pages.append(page(5, kt("إطار خدماتنا", "أربع ركائز لنظام نمو واحد") + '<p class="t ab" style="right:60px;left:60px;top:240px;font-size:13.5px">يمكن التعاقد على كل ركيزة بمفردها. وتزداد قيمتها حين تترابط، لأن كل واحدة تزيل قيدًا عن الأخريات.</p>' + pc +
 f'<div class="ab" style="left:356px;top:524px;width:114px;height:114px;border-radius:50%;background:{TEAL};color:{NAVY};display:flex;align-items:center;justify-content:center;text-align:center;font-weight:700;font-size:13px;line-height:1.6">نظام<br>النمو</div>'
 f'<div class="ab" style="right:60px;left:60px;top:900px;text-align:center;font-style:italic;color:{MUTED};font-size:13.5px">يربط القياس الركائز الأربع: تُدار كل ركيزة عبر مؤشرات أداء متفق عليها ومراجعات دورية.</div>'
 '<div class="note" style="top:975px">قوائم الخدمات في الصفحات 06–09 مقترحة. أكّد أي الخدمات تقدمها NEXORA بنفسها أو عبر شركاء أو لم تُقدَّم بعد، قبل النشر.</div>'))
# ---- 6-9 pillars
def pillar(i, p):
    n = 6 + i
    left = (f'<div class="ab" style="right:60px;top:362px;width:420px"><div class="lab" style="letter-spacing:0">التحديات التي نعالجها</div><div style="border-top:1px solid {LINE};padding-top:12px">{li(p["ch"])}</div></div>'
            f'<div class="ab" style="right:60px;top:{540 if len(p["ch"])<=4 else 540}px;width:420px"><div class="lab">الخدمات</div><div style="border-top:1px solid {LINE};padding-top:12px">{li(p["sv"], "b d")}</div></div>')
    boxh = 66 + len(p["dl"]) * 34
    right = (f'<div class="box" style="left:60px;top:362px;width:257px;height:{boxh}px;padding:22px 24px"><div class="lab">المخرجات المعتادة</div>' +
             "".join(f'<div style="font-size:13px;padding:7px 0;border-top:1px solid rgba(255,255,255,.14)">{d}</div>' for d in p["dl"]) + "</div>"
             f'<div class="ab" style="left:60px;top:{362+boxh+26}px;width:257px"><div class="lab">القيمة للأعمال</div><div class="t" style="font-size:13px;line-height:1.8">{p["val"]}</div>'
             f'<div class="lab" style="margin-top:22px">مؤشرات قد نستخدمها</div>{li(p["ind"])}</div>')
    return page(n, f'<div class="k">الركيزة {p["n"]} · محفظة الخدمات</div><h1 style="font-size:34px">{p["name"]}</h1>'
        f'<div class="ab" style="right:60px;left:60px;top:{228 if len(p["name"])<32 else 232}px;color:{TEAL};font-weight:700;font-size:16.5px">{p["tag"]}</div><p class="t ab" style="right:60px;left:60px;top:272px;font-size:13.5px">{p["intro"]}</p>' + left + right +
        f'<div class="fmt"><b>صيغة التعاقد</b>{p["fmt"]}</div><div class="fn">قائمة خدمات مقترحة وتحتاج تأكيدًا. تعتمد المخرجات على النطاق المتفق عليه ومتطلبات العميل؛ وتتوقف النتائج على عوامل خارج سيطرة NEXORA ولا نضمنها.</div>')
for i, p in enumerate(PILLARS): pages.append(pillar(i, p))
# ---- 10 integrated model
ST = [("الاستراتيجية", "تحدد فرصة النمو", "تُحدد الشريحة والعرض الأكثر ربحية."), ("التسويق", "يولّد اهتمامًا مناسبًا", "الحملات تستهدف تلك الشريحة برسالة واحدة واضحة."), ("المبيعات وتطوير الأعمال", "تحوّل الفرص", "عملية متابعة وقناة مبيعات تحلان محل البيع العشوائي."),
      ("العمليات", "تصنع الاتساق", "إجراءات التشغيل والأدوار تُبقي التسليم على المستوى نفسه."), ("التدريب", "ينمّي الفريق", "يتعلم الموظفون معايير البيع والخدمة الجديدة."), ("مؤشرات الأداء", "تقيس التقدم", "تُراجَع شهريًا: العملاء المحتملون والتحويل والجودة والهامش."), ("التحسين", "يقوّي النظام", "النتائج تحدد أولويات الربع التالي.")]
rows = f'<div class="ab" style="right:93px;top:420px;width:2px;height:530px;background:#2A4A5A"></div>'
for i, (a, b, c) in enumerate(ST):
    y = 392 + i * 88; last = i == 6
    rows += (f'<div class="ab" style="right:60px;top:{y}px;width:56px;height:56px;border-radius:50%;border:2px solid {TEAL};background:{TEAL if last else NAVY};color:{NAVY if last else TEAL};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:17px">{i+1}</div>'
             f'<div class="ab" style="right:140px;top:{y+8}px;width:330px;font-size:17px;font-weight:700;line-height:1.5"><span>{a}</span> <span style="color:{TEAL};font-weight:500">{b}</span></div>'
             f'<div class="ab" style="left:60px;top:{y+6}px;width:210px;font-size:12px;color:#B9C6D6;line-height:1.65">{c}</div>')
pages.append(page(10, kt("نموذج أعمالنا المتكامل", "كيف تعمل الركائز معًا") +
 f'<div class="ab" style="right:60px;top:236px;border:1.5px solid {TEAL};border-radius:20px;padding:6px 28px;color:{TEAL};font-weight:700;font-size:12px">مثال افتراضي</div>'
 '<p class="t ab" style="right:60px;left:60px;top:292px;font-size:13.5px">شركة خدمات نامية وصلت إلى مرحلة ثبات. الاستفسارات غير منتظمة، ومتابعة المبيعات غير متسقة، وجودة التسليم تختلف من موظف لآخر، والإدارة لا ترى أي الأنشطة يقود الإيرادات. هذا توضيح للنموذج، وليس قصة عميل.</p>' + rows +
 '<div class="ab" style="right:60px;top:1020px;font-style:italic;font-size:12.5px;color:#B9C6D6">↻ تتكرر الدورة، وتبدأ كل جولة من نتائج مُقاسة.</div>', dark=True))
# ---- 11 engagement models
EM = [("01", "مشروع استراتيجي", "تعاقد محدد يركز على تحدٍّ تجاري واحد أو هدف استراتيجي.", "بداية ونهاية واضحتان؛ مخرجات ثابتة"), ("02", "استشارات وتنفيذ", "تقييم وتوصيات، يعقبهما دعم تنفيذ متفق عليه.", "للتغيير الذي يجب تطبيقه عمليًا"),
      ("03", "شراكة نمو مستمرة", "تعاقد متكرر يدعم أولويات متفقًا عليها في التسويق أو تطوير الأعمال أو العمليات أو الأداء.", "دورات شهرية أو ربع سنوية مع تقارير"), ("04", "تدريب مؤسسي", "برنامج مخصص للمديرين أو الموظفين أو وظائف محددة.", "من تقييم الاحتياجات إلى التقييم"),
      ("05", "تقييم أداء الأعمال", "تشخيص مركّز يحدد الفجوات والفرص والخطوات التالية الموصى بها.", "نقطة بداية عملية")]
ec = ""
for i, (n, a, b, c) in enumerate(EM):
    dk = i == 4; y = 300 + i * 130
    ec += (f'<div class="ab" style="right:60px;left:60px;top:{y}px;height:112px;{"background:" + NAVY + ";color:#fff" if dk else "background:#fff;border:1px solid " + LINE}">'
           f'<div class="ab" style="right:26px;top:30px;font-size:28px;font-weight:700;color:{TEAL}">{n}</div><div class="ab" style="right:100px;top:20px;width:320px"><div style="font-size:18px;font-weight:700">{a}</div><div style="font-size:12.5px;line-height:1.7;margin-top:5px;color:{"#B9C6D6" if dk else MUTED}">{b}</div></div>'
           f'<div class="ab" style="left:24px;top:20px;width:200px;border-right:1px solid {"rgba(255,255,255,.2)" if dk else LINE};padding-right:18px;height:72px"><div class="lab" style="font-size:11.5px">الأنسب عند</div><div style="font-size:13px;font-weight:{600}">{c}</div></div></div>')
pages.append(page(11, kt("نماذج التعاقد", "خمس طرق للعمل مع NEXORA") + '<p class="t ab" style="right:60px;left:60px;top:240px;font-size:13.5px">يتعاقد العملاء بالصيغة التي تناسب وضعهم. ليس كل تعاقد يشمل الركائز الأربع.</p>' + ec +
 f'<div class="ab" style="right:60px;left:60px;top:960px;font-size:12px;font-style:italic;color:{MUTED};line-height:1.7">يُحدد النطاق والمدة والمخرجات والرسوم لكل عميل في عرض مكتوب. لا تنشر NEXORA أسعار باقات ثابتة.</div>'))
# ---- 12 methodology
MS = ["الاستكشاف الأولي", "تقييم النشاط", "تحديد الأهداف", "تحديد النطاق", "تخطيط المشروع", "توزيع المسؤوليات", "التنفيذ", "تقارير التقدم", "مراجعة الأداء", "التحسين المستمر"]
mh = "".join(f'<div style="display:flex;gap:20px;height:48px;align-items:center;border-bottom:1px solid {LINE};font-size:14px;width:330px;{"position:absolute;right:" + ("60" if i < 5 else "424") + "px;top:" + str(300 + (i % 5) * 48) + "px"}"><b style="color:{TEAL};width:26px">{i+1:02d}</b><span>{m}</span></div>' for i, m in enumerate(MS))
TB = [("الأهداف", "تقترح أهدافًا قابلة للقياس", "يعتمد الأهداف والأولويات"), ("المعلومات", "تطلب البيانات وتجري التقييم", "يوفر الوصول والبيانات والأشخاص الرئيسيين"), ("المخرجات", "تعدّ الخطط والعمليات والمواد", "يراجع ويعتمد خلال الوقت المتفق عليه"),
      ("التنفيذ", "تدعم وتوجّه حسب النطاق", "يعيّن المسؤولين ويطبق التغييرات"), ("التقارير", "تقدم تقارير التقدم مقابل المؤشرات", "يحضر المراجعات ويؤكد القرارات"), ("ضبط التغيير", "تنبّه كتابيًا إلى تغييرات النطاق", "يعتمد التغييرات قبل بدء العمل")]
tb = f'<table class="ab" style="right:60px;left:60px;top:607px;border-collapse:collapse;font-size:12.5px;width:707px"><tr style="background:{NAVY};color:#fff;height:40px"><th style="width:130px;text-align:right;padding:0 12px">المجال</th><th style="text-align:right;padding:0 12px;border-right:1px solid rgba(255,255,255,.3)">NEXORA</th><th style="text-align:right;padding:0 12px;border-right:1px solid rgba(255,255,255,.3)">العميل</th></tr>'
for i, (a, b, c) in enumerate(TB): tb += f'<tr style="height:42px;background:{"#fff" if i%2==0 else "#F8F9FB"}"><td style="padding:0 12px;font-weight:700;border:1px solid {LINE}">{a}</td><td style="padding:0 12px;border:1px solid {LINE}">{b}</td><td style="padding:0 12px;border:1px solid {LINE}">{c}</td></tr>'
tb += "</table>"
pages.append(page(12, kt("المنهجية والحوكمة", "نطاق واضح، ومسؤولون محددون، وتقدم موثّق") + f'<div class="ab lab" style="right:60px;top:270px">كيف تُدار المشاريع</div>' + mh + f'<div class="ab lab" style="right:60px;top:572px">نموذج مسؤوليات (للتوضيح)</div>' + tb +
 f'<div class="box" style="right:60px;left:60px;top:915px;height:150px;padding:22px 30px"><div class="lab">التزامات الحوكمة</div>{li(["جهة اتصال واحدة مسماة لدى كل طرف", "خطوات اعتماد وأزمنة استجابة متفق عليها", "دورة تقارير ثابتة ومخرجات موثقة"])}</div>'))
# ---- 13 KPIs
KP = [("التسويق", ["العملاء المحتملون المؤهلون", "تكلفة العميل المحتمل", "تكلفة اكتساب العميل", "معدل التحويل", "العائد على الإنفاق الإعلاني، حيثما ينطبق"]), ("المبيعات وتطوير الأعمال", ["الفرص المؤهلة", "التحويل من فرصة إلى عميل", "مدة دورة البيع", "معدل تحويل العروض", "الإيرادات، حيث يمكن نسبتها"]),
      ("العمليات", ["زمن إتمام العملية", "معدلات الأخطاء وإعادة العمل", "الالتزام بمستوى الخدمة", "الالتزام بالعملية", "التكلفة لكل معاملة، حيثما ينطبق"]), ("التدريب", ["إتمام التدريب", "نتائج تقييم المعرفة", "تحسن المهارات المُثبت", "الأداء بعد التدريب", "التطبيق في العمل"])]
kc = ""
for i, (a, items) in enumerate(KP):
    x = 427 if i % 2 == 0 else 60; y = 305 + (i // 2) * 246
    kc += f'<div class="ab" style="left:{x}px;top:{y}px;width:340px;height:228px;background:#fff;border:1px solid {LINE};padding:22px 26px"><div style="font-size:16.5px;font-weight:700">{a}</div><div style="width:40px;height:3px;background:{TEAL};margin:10px 0 12px"></div>{li(items)}</div>'
ov = "".join(f'<div style="font-size:14px;font-weight:700;width:120px;line-height:1.6">{x}</div>' for x in ["نمو الإيرادات", "هامش الربح الإجمالي", "الاحتفاظ بالعملاء", "رضا العملاء", "الإنتاجية"])
pages.append(page(13, kt("القياس ومؤشرات الأداء", "ما يُقاس يُدار") + '<p class="t ab" style="right:60px;left:60px;top:238px;font-size:13.5px">تُختار مؤشرات الأداء لكل تعاقد بناءً على الأهداف التجارية وتوافر البيانات والنطاق. تعرض القائمة أدناه المدى الذي قد تستند إليه NEXORA، وهي ليست ادعاءً بنتائج سابقة.</p>' + kc +
 f'<div class="box" style="right:60px;left:60px;top:812px;height:175px;padding:24px 30px"><div style="font-size:16.5px;font-weight:700">الأداء العام للأعمال</div><div style="width:40px;height:3px;background:{TEAL};margin:10px 0 24px"></div><div style="display:flex;justify-content:space-between;color:#fff">{ov}</div></div>'))
# ---- 14 industries
def ic(i):
    s = {0: f'<circle cx="19" cy="19" r="17" fill="none" stroke="{TEAL}" stroke-width="2"/>', 1: f'<rect x="3" y="3" width="32" height="32" fill="none" stroke="{TEAL}" stroke-width="2"/>', 2: f'<path d="M19 3 L36 35 H2 Z" fill="none" stroke="{TEAL}" stroke-width="2"/>',
         3: f'<path d="M19 2 L36 19 L19 36 L2 19 Z" fill="none" stroke="{TEAL}" stroke-width="2"/>', 4: f'<circle cx="31" cy="6" r="4" fill="{TEAL}"/><circle cx="7" cy="32" r="4" fill="{TEAL}"/><path d="M9 29 L29 9" stroke="{TEAL}" stroke-width="2"/>',
         5: f'<rect x="3" y="22" width="8" height="14" fill="{TEAL}"/><rect x="15" y="12" width="8" height="24" fill="{TEAL}"/><rect x="27" y="2" width="8" height="34" fill="{TEAL}"/>', 6: "".join(f'<rect x="{3+a*18}" y="{3+b*18}" width="14" height="14" fill="none" stroke="{TEAL}" stroke-width="2"/>' for a in range(2) for b in range(2))}[i]
    return f'<svg width="40" height="40" viewBox="0 0 38 38">{s}</svg>'
IN = [("اللياقة والعافية", "اكتساب الأعضاء والاحتفاظ بهم، وجدولة الحصص والمدربين، ومبيعات مكتب الاستقبال.", "تسويق العضويات، ونصوص المبيعات، وإجراءات الخدمة، وتدريب المدربين."),
      ("الضيافة وخدمات الطعام", "الاتساق عبر الورديات، وتجربة الضيف، والطلب المحلي، وتكرار الزيارات.", "التسويق المحلي، ومعايير الخدمة، وإجراءات الفتح والإغلاق، وتدريب العاملين."),
      ("التجزئة والخدمات الاستهلاكية", "حركة الزوار والتحويل، واتساق المخزون والفروع، ومهارات البيع لدى العاملين.", "تخطيط الحملات، وإجراءات المتجر، ولوحات مؤشرات الأداء، وتدريب المبيعات."),
      ("الخدمات المهنية", "رؤية خط المبيعات، وتحويل العروض، وجودة التسليم والاستخدام.", "عملية تطوير الأعمال، ونماذج العروض، وتصميم سير العمل."),
      ("الشركات الناشئة والأعمال الناشئة", "التموضع، والعملاء الأوائل، وأساسات قابلة للتوسع.", "خطة دخول السوق، وتموضع العلامة، وعمليات المراحل المبكرة."),
      ("المنشآت الصغيرة والمتوسطة", "اعتماد على المالك، وعمليات غير رسمية، ونمو غير متسق.", "تقييم الأداء، وتعريف الأدوار، والتدريب الإداري."),
      ("الأعمال B2B والمنظمات الخدمية", "دورات بيع طويلة، وإدارة الحسابات، واتساق الخدمة.", "عملية المبيعات، وانضباط CRM، وأطر مستوى الخدمة.")]
ir = ""
for i, (a, c, s) in enumerate(IN):
    y = 308 + i * 98
    ir += (f'<div class="ab" style="right:60px;top:{y}px;width:707px;height:98px;border-top:1px solid {LINE}"><div class="ab" style="right:0;top:22px">{ic(i)}</div><div class="ab" style="right:64px;top:22px;width:190px;font-size:15.5px;font-weight:700;line-height:1.5">{a}</div>'
           f'<div class="ab" style="left:0;top:14px;width:430px;font-size:12px;line-height:1.7"><div><b style="color:{NAVY}">التحديات</b> <span style="color:{MUTED}">{c}</span></div><div style="margin-top:6px"><b style="color:{TEAL}">الدعم</b> <span style="color:{MUTED}">{s}</span></div></div></div>')
pages.append(page(14, kt("القطاعات التي ندعمها", "قطاعات يهم فيها النمو المتكامل أكثر") + '<p class="t ab" style="right:60px;left:60px;top:240px;font-size:13.5px;top:248px">تعمل NEXORA عبر قطاعات ولا تدّعي تخصصًا حصريًا. هذه قطاعات يكون فيها الجمع بين التسويق والمبيعات والعمليات والتدريب وثيق الصلة بوجه خاص.</p>' + ir))
# ---- 15 why
WH = [("تفكير متكامل", "ننظر عبر الاستراتيجية والتسويق والمبيعات والعمليات والأفراد، لأن المشكلات في مجال تبدأ عادةً من مجال آخر."), ("استراتيجية مرتبطة بالتنفيذ", "التوصيات تأتي بمسؤولين وجداول زمنية والعمليات اللازمة لتطبيقها."), ("عمل منظم وموثق", "كل تعاقد ينتج مخرجات واضحة يحتفظ بها العميل ويستفيد منها."),
      ("قياس ومساءلة", "تُتفق الأهداف مقدمًا وتُراجع مقابل مؤشرات الأداء."), ("تعاقد مرن", "من تقييم مركّز إلى شراكة مستمرة، بحسب احتياج العميل."), ("مخصص لا قوالب جاهزة", "الحلول تُبنى حول سوق العميل وفريقه ومرحلة نموه."), ("قدرات تبقى", "نبني أنظمة ومهارات داخلية لتستمر التحسينات بعد انسحابنا.")]
wr = "".join(f'<div class="ab" style="right:60px;left:60px;top:{250+i*108}px;height:108px;border-bottom:1px solid rgba(255,255,255,.12)"><div class="ab" style="right:0;top:6px;font-size:28px;font-weight:700;color:{TEAL}">{i+1:02d}</div><div class="ab" style="right:86px;top:8px;left:0"><div style="font-size:17.5px;font-weight:700">{a}</div><div style="font-size:13px;color:#B9C6D6;margin-top:6px;line-height:1.75">{b}</div></div></div>' for i, (a, b) in enumerate(WH))
pages.append(page(15, kt("لماذا NEXORA", "ما الذي يمكن للعملاء توقعه") + wr + '<div class="ab" style="right:60px;left:60px;top:1030px;font-style:italic;font-size:12px;color:#B9C6D6;line-height:1.7">لا تدّعي NEXORA الريادة في السوق ولا نتائج مضمونة. نلتزم بنطاق واضح وتقارير صادقة وعمل عملي.</div>', dark=True))
# ---- 16 scenarios
SC = [("سيناريو أ · افتراضي", "سلسلة صالات رياضية بأداء متفاوت بين الفروع", "التحدي: تنمو العضويات في فرع وتتراجع في فرعين.", "النطاق المحتمل: تقييم الأداء، وعملية مبيعات مكتب الاستقبال، وإجراءات التشغيل للفروع، وتدريب العاملين على البيع، ومراجعة شهرية لمؤشرات الأداء.", "يُقاس بـ: التحويل من تجربة إلى عضو، والاحتفاظ، والمبيعات لكل فرع."),
      ("سيناريو ب · افتراضي", "شركة خدمات B2B تعتمد على مؤسسها", "التحدي: تكاد كل صفقة وقرار رئيسي تمر عبر المالك.", "النطاق المحتمل: الاستراتيجية التجارية، وخط المبيعات وعملية العروض، وتعريف الأدوار، والتدريب الإداري.", "يُقاس بـ: الفرص المؤهلة، وتحويل العروض، ومدة دورة البيع.")]
sc = "".join(f'<div class="ab" style="{"right:60px" if i==0 else "left:60px"};top:300px;width:340px;height:355px;background:#fff;border:1px solid {LINE};padding:26px"><div class="lab" style="font-size:11.5px">{a}</div><div style="font-size:17.5px;font-weight:700;line-height:1.55;margin-bottom:18px">{b}</div><div class="t" style="font-size:12.5px;line-height:1.8">{c}</div><div class="t" style="font-size:12.5px;line-height:1.8;margin-top:8px">{d}</div><div class="t" style="font-size:12.5px;line-height:1.8;margin-top:8px">{e}</div></div>' for i, (a, b, c, d, e) in enumerate(SC))
CF = ["قطاع العميل", "التحدي في الأعمال", "الوضع الأولي", "نطاق العمل", "الحل المقترح أو المنفّذ", "المخرجات", "منهج القياس", "النتائج الموثّقة", "شهادة العميل، إن سُمح"]
cf = "".join(f'<div class="ab" style="right:{60+(i%3)*241}px;top:{762+(i//3)*72}px;width:225px;height:60px;{"background:" + NAVY + ";color:#fff" if i==7 else "background:#fff;border:1px solid " + LINE};display:flex;align-items:center;gap:12px;padding:0 16px;font-size:12.5px"><b style="color:{TEAL}">{i+1:02d}</b><span>{x}</span></div>' for i, x in enumerate(CF))
pages.append(page(16, kt("إثبات القدرات", "سيناريوهات تعاقد توضيحية") + '<div class="note" style="top:236px;text-align:center;font-size:12px">لم تُقدَّم دراسات حالة موثّقة. السيناريوهات أدناه افتراضية ويجب ألا تُعرض كنتائج عملاء.</div>' + sc +
 f'<div class="ab lab" style="right:60px;top:690px">إطار دراسة الحالة</div><div class="t ab" style="right:60px;top:716px;font-size:12.5px">ستتبع كل دراسة حالة منشورة هذا الهيكل، بمعلومات موثّقة وموافقة العميل.</div>' + cf + f'<div class="ab" style="right:60px;top:985px;color:{TEAL};font-weight:700;font-size:13px">[أدرج دراسات الحالة الموثّقة هنا عند توفرها]</div>'))
# ---- 17 partnership
PR = [("الحديث الأول", "فهم نشاطك وأهدافك والمشكلة التي تريد حلها."), ("تقييم الاحتياجات", "مراجعة الوضع الحالي وتحديد القيود الحقيقية."), ("النطاق والأهداف", "الاتفاق على شكل النجاح وكيف سيُقاس."), ("العرض والمخرجات", "عرض مكتوب بالنطاق والجدول الزمني والمخرجات والرسوم."),
      ("الاتفاق والتخطيط", "التوقيع وتسمية المسؤولين لدى الطرفين ووضع الخطة."), ("التنفيذ والتقارير", "تنفيذ العمل المتفق عليه مع تقارير تقدم منتظمة."), ("مراجعة الأداء", "مراجعة النتائج مقابل مؤشرات الأداء والاتفاق على الخطوات التالية.")]
pr = f'<div class="ab" style="right:85px;top:300px;width:3px;height:430px;background:{TEAL}"></div>'
for i, (a, b) in enumerate(PR):
    y = 270 + i * 86; last = i == 6
    pr += (f'<div class="ab" style="right:60px;top:{y}px;width:50px;height:50px;border-radius:50%;background:{TEAL if last else NAVY};color:{NAVY if last else "#fff"};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px">{i+1}</div>'
           f'<div class="ab" style="right:130px;top:{y+13}px;width:240px;font-size:17px;font-weight:700">{a}</div><div class="ab" style="left:60px;top:{y+8}px;width:330px;font-size:13px;color:{MUTED};line-height:1.7">{b}</div>')
pages.append(page(17, kt("عملية الشراكة", "من أول حديث إلى تقدم قابل للقياس") + pr +
 f'<div class="box" style="right:60px;left:60px;top:880px;height:170px;padding:34px 40px"><div style="width:60px;height:4px;background:{TEAL};margin-bottom:18px"></div><div style="font-size:20px;font-weight:700;line-height:1.75">«دعونا نحدد ما يعيق أعمالك، ونبني خطة عملية للمضي بها قدمًا.»</div><div style="margin-top:14px;color:{TEAL};font-size:13.5px">ابدأ بحديث أولي: [بيانات التواصل على الغلاف الخلفي]</div></div>'))
# ---- 18 back cover
bp = [(220, 90), (100, 140), (310, 170), (180, 240), (290, 290)]
cd = [("الموقع الإلكتروني", "[www.قيد-التأكيد]"), ("البريد الإلكتروني", "[البريد الإلكتروني للأعمال]"), ("الهاتف", "[رقم الهاتف]"), ("واتساب", "[رقم واتساب]"), ("لينكدإن", "[صفحة لينكدإن]"), ("المكتب", "[العنوان، إن وُجد]")]
ch = "".join(f'<div class="ab" style="{"right:60px" if i%2==0 else "left:60px;width:300px"};top:{730+(i//2)*75}px"><div class="lab" style="font-size:11.5px;margin-bottom:4px">{a}</div><div style="font-size:14px">{b}</div></div>' for i, (a, b) in enumerate(cd))
pages.append(page(18, constellation(bp, [(0, 1), (0, 2), (1, 3), (3, 4), (2, 4)], mirror=True).replace('style="left:0;top:0"', 'style="left:0;top:0"') + '<img class="ab" src="img/logo_full.png" style="right:60px;top:330px;width:330px">' +
 f'<div class="ab" style="right:60px;top:560px;font-size:23px;font-weight:700;color:{TEAL}">{TAG}</div><div class="ab" style="right:60px;top:606px;font-size:15px;color:#CBD5E1">استراتيجية أفضل. أنظمة أقوى. تقدم قابل للقياس.</div>'
 f'<div class="ab" style="right:60px;left:60px;top:700px;border-top:1px solid rgba(255,255,255,.14)"></div>' + ch + '<div class="ab" style="right:60px;top:1090px;font-size:10.5px;font-style:italic;color:#7F90A5">بيانات التواصل مؤقتة. استبدلها قبل التوزيع.</div>', dark=True, head=False))
open(f"{HERE}/profile_ar.html", "w", encoding="utf-8").write(f'<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><style>{CSS}</style><body>' + "".join(pages) + "</body></html>")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 827, "height": 1169}); pg.goto(f"file://{HERE}/profile_ar.html"); pg.wait_for_timeout(800)
    pg.pdf(path=f"{HERE}/NEXORA_Company_Profile_AR.pdf", width="827px", height="1169px", print_background=True, prefer_css_page_size=True); b.close()
print("pages", len(pages))
