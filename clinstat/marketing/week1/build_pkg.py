import base64,io,glob,html
from PIL import Image
import data as D
src=open("../build_strategy.py").read()
exec(src.split("N='<span")[0])
def esc(s): return html.escape(str(s),quote=False)
def th(path,w=420):
    im=Image.open(path).convert("RGB");im.thumbnail((w,w*2));b=io.BytesIO();im.save(b,"JPEG",quality=72)
    return "data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()
def imgs(prefix):
    fs=sorted(glob.glob(f"out/{prefix}_*.png"))
    return '<div class="gal">'+"".join(f'<figure><img src="{th(f)}" alt="{f.split("/")[-1]}"><figcaption>{f.split("_")[-1].replace(".png","")}</figcaption></figure>' for f in fs)+'</div>'
def lst(items,ol=False):
    tag="ol" if ol else "ul";return f"<{tag}>"+"".join(f"<li>{esc(i)}</li>" for i in items if i)+f"</{tag}>"
def box(lines):
    return '<div class="copy">'+"<br>".join(esc(l) if l else "&nbsp;" for l in lines)+'</div>'
S=[]
for i,c in enumerate(D.CONTENT,1):
    f=[["رقم المحتوى",c["id"]],["تاريخ النشر",c["date"]],["المنصة الأساسية",c["platform"]],["منصات التكييف",c["adapt"]],["المحور",c["pillar"]],["السلسلة",c["series"]],["الجمهور",c["aud"]],["هدف التسويق",c["obj"]],["الحملة",c["campaign"]],["الشكل",c["fmt"]],["الـHook",c["hook"]],["الرسالة الأساسية",c["core"]],["الكابشن",c["caption"]],["الدعوة (CTA)",c["cta"]],["الهاشتاجات",c.get("hashtags") or "-"],["التوجيه البصري",c["visual"]],["تعليمات التصميم",c["design"]],["المراجع العلمية (للتحقق)",c["ref"]],["حالة المراجعة",c["status"]]]
    body=tbl(["الحقل","القيمة"],f)
    body+="<h3>النص الكامل</h3>"+box(c["copy"])
    if "vo" in c:
        body+=f"<h3>الريل: {c['duration']}</h3><h4>التعليق الصوتي</h4>"+lst(c["vo"],True)
        body+="<h4>Storyboard</h4>"+tbl(["الوقت","المشهد","الوصف البصري","الحركة"],[list(x) for x in c["story"]])
        body+="<h4>النص على الشاشة</h4>"+lst(c["onscreen"])+f"<h4>الترجمة</h4><p>{esc(c['subs'])}</p><h4>تعليمات الموشن</h4><p>{esc(c['motion'])}</p><h4>الـCTA الأخير</h4><p>{esc(c['cta'])}</p>"
    if "slides" in c:
        body+="<h3>شرائح الكاروسيل</h3>"+tbl(["الشريحة","العنوان","النص"],[list(x) for x in c["slides"]])+f"<p><b>منطق الانتقال:</b> {esc(c['transition'])}</p>"
    if "frames" in c:
        body+="<h3>إطارات الستوري</h3>"+tbl(["الإطار","العنوان","ملاحظة"],[[j,x[1],x[2]] for j,x in enumerate(c["frames"],1)])
    if "x" in c:
        body+="<h3>نص السلسلة على X</h3>"+lst(c["x"],True)+f"<p class='small'>أطول تغريدة: {max(len(t) for t in c['x'])} حرفًا (الحد 280).</p>"
    if "li" in c:
        body+="<h3>نسخة LinkedIn المكيّفة</h3>"+box(c["li"])
    if "fb" in c:
        body+="<h3>نسخة فيسبوك المكيّفة</h3>"+box(c["fb"])
    key={"CS-001":"cs001","CS-002":"cs002","CS-003":"cs003","CS-004":"cs004","CS-005":"cs005","CS-006":"cs006","CS-007":"cs007"}[c["id"]]
    body+="<h3>التصاميم (معاينة مصغّرة، الملفات كاملة في الـzip)</h3>"+imgs(key)
    S.append(sec(i,f"{c['id']} · {c['hook']}",body,f"{c['platform']} · {c['date']}"))
CSS2=CSS+"\n.copy{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 20px;font-size:16px;line-height:1.9;margin:8px 0}.gal{display:flex;gap:14px;flex-wrap:wrap}.gal figure{margin:0;width:150px}.gal img{width:150px;border:1px solid var(--line);border-radius:8px;display:block}.gal figcaption{font-size:11px;color:var(--mut);direction:ltr;text-align:center}\n"
toc="".join(f'<a href="#d{i}"><b>{i}</b>{c["id"]}</a>' for i,c in enumerate(D.CONTENT,1))
html_=f'''<title>حزمة محتوى ClinStat الأسبوع 1</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS2.replace("Amiri,serif","'IBM Plex Sans Arabic',sans-serif").replace("Cairo,","'IBM Plex Sans Arabic',")}</style>
<div dir="rtl" lang="ar" class="layout"><nav class="rail" aria-label="المحتويات"><small>المحتوى</small>{toc}</nav>
<main><div class="hero"><h1>حزمة محتوى ClinStat: الأسبوع 1</h1><p>دفعة تجريبية من 7 مواد (8 إلى 14 نوفمبر 2026). نصوص كاملة وسكريبت وستوري بورد وتصاميم بصيغها. كل مادة مسودة بانتظار المراجعة العلمية والإبداعية، وكل رابط أو عرض بين [ ] لا ينشر قبل تأكيده.</p><span class="tag">الجولة 3 · دفعة تجريبية · مسودة</span></div>
{"".join(S)}</main></div>'''
open("week1_package_ar.html","w").write(html_);print(len(html_))
