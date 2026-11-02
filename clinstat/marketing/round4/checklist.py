import sys,os,asyncio
sys.path.insert(0,"/home/user/Vd/clinstat/posts");sys.path.insert(0,"../week1")
import engine as E
from engine import t,logo
NAVY,GREEN,GOLD,SAND="#0B1F33","#103D2E","#A8854E","#F7F4ED"
FD="/home/user/Vd/clinstat/posts/fonts"
P=[
("السؤال والأهداف","هل السؤال البحثي والهدف مصاغان بوضوح، ومتسقان بين العنوان والملخص والمنهج والنتائج؟","نتائج تجيب عن سؤال غير الذي في المقدمة.","STROBE / CONSORT (بند الأهداف)"),
("الإرشاد المناسب للإبلاغ","هل حددت إرشاد الإبلاغ المناسب لتصميمك: CONSORT للتجارب العشوائية، STROBE للدراسات الرصدية، PRISMA 2020 للمراجعات المنهجية؟ وهل أرفقت قائمة التحقق إن طلبتها المجلة؟","مخطوطة لا تذكر أي إرشاد مناسب لتصميمها.","EQUATOR Network (مكتبة الإرشادات)"),
("النتيجة الأساسية والتسجيل","هل حُدّدت النتيجة الأساسية مسبقًا؟ وهل سُجّل البروتوكول أو التجربة حيث ينطبق؟","تغيير النتيجة الأساسية بعد رؤية البيانات دون ذكر السبب.","CONSORT 2010 (بند 6a و6b)"),
("حجم العينة","هل حُسب حجم العينة على النتيجة الأساسية؟ وهل ذُكرت الافتراضات (الأثر المتوقع، التباين، مستوى الدلالة، القدرة الإحصائية، الانسحاب)؟","حجم عينة بلا حساب أو بلا افتراضات.","CONSORT 2010 (بند 7a)"),
("التصميم والاختيار وتدفق المشاركين","هل وُصف التصميم والمكان والفترة ومعايير الاختيار؟ وهل يظهر تدفق المشاركين (من فُحص ومن دخل ومن خرج ولماذا)؟","أعداد المشاركين لا تتطابق بين المخطط والنص والجداول.","CONSORT (مخطط التدفق) / PRISMA 2020 (مخطط التدفق)"),
("المتغيرات والقياس","هل عُرّف كل متغير، وكيف ومتى قُيس، ووحدته؟","متغير بلا تعريف أو بطرق قياس متعددة غير موضحة.","STROBE (المتغيرات ومصادر البيانات)"),
("البيانات الناقصة","هل ذُكر حجم البيانات الناقصة وسببها وطريقة التعامل معها؟","حذف الحالات الناقصة دون تبرير.","STROBE (بند البيانات الناقصة)"),
("الطرق الإحصائية","هل ذُكرت الاختبارات والبرنامج وإصداره ومستوى الدلالة، والتعامل مع الاختبارات المتعددة والافتراضات؟","اختبار غير مناسب للتصميم، أو تعدد اختبارات بلا تصحيح أو توضيح.","STROBE / CONSORT (الطرق الإحصائية)"),
("حجم الأثر وفترة الثقة","هل عرضت حجم الأثر مع فترة الثقة، وليس p-value وحدها؟ وهل ميّزت بين الدلالة الإحصائية والأهمية السريرية؟","الاكتفاء بعبارة «دالة» أو «غير دالة».","ASA Statement on p-Values (2016) / CONSORT 2010 (بند 17a)"),
("الجداول والأشكال والأعداد","هل الأعداد والنسب في الجداول والأشكال تطابق النص؟ هل الوحدات والعناوين واضحة؟","أرقام متناقضة بين الملخص والجداول.","إرشاد المجلة + الإرشاد المناسب لتصميمك"),
("التحليلات الاستكشافية والتعديلات","هل أُعلنت التحليلات الاستكشافية أو ما بعد الحدوث وأي تعديل عن خطة التحليل وسببه؟","تحليلات كثيرة يُعرض الدال منها فقط.","STROBE / CONSORT (التحليلات الفرعية)"),
("الأخلاقيات والتمويل وحدود الدراسة","هل ذُكرت موافقة لجنة الأخلاقيات والموافقة المستنيرة أو الإعفاء، والتمويل وتضارب المصالح، وبيان إتاحة البيانات حسب المجلة؟ وهل عرضت حدود الدراسة واستنتاجاتك بما لا يتجاوز نتائجها (دون استنتاج سببية من ارتباط)؟","بيانات أخلاقيات ناقصة، أو استنتاجات أقوى من التصميم.","متطلبات المجلة المستهدفة / توصيات ICMJE [للتحقق]"),
]
def build():
    cards="".join(f'''<div class="pt"><div class="hd"><span class="n">{i}</span><h3>{t(a)}</h3><span class="chk"></span></div>
<p><b>اسأل نفسك:</b> {t(q)}</p><p class="rf"><b>علامة خطر:</b> {t(r)}</p><p class="ref">المرجع: <span dir="ltr">{t(x)}</span></p></div>''' for i,(a,q,r,x) in enumerate(P,1))
    css=f'''@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Regular.ttf);font-weight:400}}@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Medium.ttf);font-weight:500}}@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-SemiBold.ttf);font-weight:600}}@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Bold.ttf);font-weight:700}}
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:PX,sans-serif;direction:rtl;color:{NAVY};font-size:11.5pt;line-height:1.7}}
.pg{{width:210mm;height:297mm;padding:12mm 15mm;page-break-after:always;position:relative;overflow:hidden}}
.cov{{background:{GREEN};color:{SAND};display:flex;flex-direction:column;justify-content:space-between}}
.cov h1{{font-size:38pt;line-height:1.25;font-weight:700}}.cov .k{{color:{GOLD};font-weight:700;font-size:14pt;letter-spacing:.04em}}
.tag{{font-size:12pt;color:#D7D1BF;margin-top:10mm}}
.top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:4mm}}.top small{{color:{GOLD};font-weight:600}}
h2{{font-size:16pt;color:{GREEN};margin-bottom:3mm}}
.pt{{border:1px solid #D9D2BF;border-radius:10px;padding:3mm 5mm;margin-bottom:2.6mm;background:#fff;page-break-inside:avoid}}
.hd{{display:flex;align-items:center;gap:4mm;margin-bottom:2mm}}.hd h3{{font-size:12pt;color:{GREEN};flex:1}}
.n{{width:9mm;height:9mm;border-radius:50%;background:{GOLD};color:{NAVY};display:grid;place-items:center;font-weight:700}}
.chk{{width:6mm;height:6mm;border:2px solid {GOLD};border-radius:2px}}
.pt p{{font-size:9.6pt;line-height:1.55}}.rf{{color:#7a2f1f}}.ref{{color:#6b6b66;font-size:9pt}}
.foot{{position:absolute;bottom:6mm;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#6b6b66;direction:ltr}}
.box{{background:{GREEN};color:{SAND};border-radius:12px;padding:8mm;margin-top:6mm}}.box h2{{color:{SAND}}}
.dis{{font-size:9pt;color:#6b6b66;margin-top:6mm}}
.btn{{display:inline-block;background:{GOLD};color:{NAVY};font-weight:700;border-radius:30px;padding:3mm 8mm;margin-top:4mm}}
'''
    foot='<div class="foot"><span>Research that survives peer review</span><span>ClinStat Research</span></div>'
    html=f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="pg cov"><div>{logo(light=True,w=240)}</div><div><div class="k">Before You Submit</div><h1>قائمة الفحص العلمي قبل التقديم</h1><div class="tag">12 نقطة منهجية تراجعها قبل أن تقدّم مخطوطتك</div></div><div class="dis" style="color:#D7D1BF">أداة مساعدة للمراجعة الذاتية، وليست بديلًا عن مراجعة مختص ولا تضمن قبول أي مجلة. أسماء الإرشادات المذكورة تُراجَع من مصادرها الأصلية.</div></div>
<div class="pg"><div class="top">{logo(light=False,w=160)}<small>1 إلى 6 من 12</small></div><h2>النقاط من 1 إلى 6</h2>{"".join(cards.split('<div class="pt">')[1:7] and ['<div class="pt">'+x for x in cards.split('<div class="pt">')[1:7]])}{foot}</div>
<div class="pg"><div class="top">{logo(light=False,w=160)}<small>7 إلى 12 من 12</small></div><h2>النقاط من 7 إلى 12</h2>{"".join(['<div class="pt">'+x for x in cards.split('<div class="pt">')[7:13]])}{foot}</div>
<div class="pg"><div class="top">{logo(light=False,w=160)}<small>الخطوة التالية</small></div><h2>كيف تستخدم القائمة</h2>
<p>1) اقرأ مخطوطتك مقابل كل نقطة وعلّم ما تحقق.<br>2) ما لم يتحقق، دوّنه كملاحظة قبل التقديم.<br>3) راجع الإرشاد المناسب لتصميمك (CONSORT أو STROBE أو PRISMA) من مصدره الأصلي.<br>4) راجع متطلبات المجلة المستهدفة.</p>
<div class="box"><h2>هل تريد مراجعة منهجية لمخطوطتك؟</h2><p>يراجع فريق ClinStat الجوانب المنهجية والإحصائية ويقدّم ملاحظات قابلة للتنفيذ. لا نضمن قبول المجلة.</p><div class="btn">تواصل معنا [الرابط مطلوب]</div></div>
<p class="dis">المراجع: ASA Statement on p-Values (2016)، CONSORT 2010، STROBE، PRISMA 2020، EQUATOR Network، توصيات ICMJE. كلها للتحقق من النصوص الأصلية قبل الاستناد إليها. هذه الوثيقة مسودة بانتظار المراجعة العلمية.</p>{foot}</div></body></html>'''
    open("checklist.html","w").write(html)
async def pdf():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--allow-file-access-from-files"])
        pg=await b.new_page();await pg.goto("file://"+os.path.abspath("checklist.html"));await pg.wait_for_timeout(500)
        await pg.pdf(path="ClinStat_PreSubmission_Checklist_AR.pdf",format="A4",print_background=True,prefer_css_page_size=True)
        await b.close()
build();asyncio.run(pdf())
