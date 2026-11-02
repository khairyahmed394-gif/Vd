import datetime,re
import cal30_data as C
src=open("build_strategy.py").read()
CSS=src.split('CSS0=')[0]  # unused
exec(src.split("N='<span")[0])  # defines CSS, tbl, sec
AR=["الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت"]
start=datetime.date(2026,11,8)
def fmt(f): return f if f=="منشور مهني" else ("منشور" if f.startswith("منشور") else f)
S=[];weeks=[(0,7),(7,14),(14,21),(21,28),(28,30)]
for wi,(a,b) in enumerate(weeks,1):
    rows=[]
    for i in range(a,b):
        d=C.D[i];dt=start+datetime.timedelta(days=i)
        rows.append([f"CS-{i+1:03d}",dt.strftime("%d/%m"),AR[(dt.weekday()+1)%7],d[0],d[2],d[6] if d[6]=="منشور مهني" else fmt(d[6]),d[8],d[9]])
    S.append(sec(wi,f"الأسبوع {wi}",tbl(["الرقم","التاريخ","اليوم","المنصة","المحور","الشكل","الموضوع","الـHook"],rows),f"{(start+datetime.timedelta(days=a)).strftime('%d/%m')} إلى {(start+datetime.timedelta(days=b-1)).strftime('%d/%m')}"))
mix=tbl(["المحور","الهدف","الفعلي"],[["التثقيف البحثي","6","6"],["الإحصاء الحيوي ببساطة","6","6"],["علامات خطر بحثية","5","5"],["قبل ما تقدّم","4","4"],["داخل ClinStat","3","3"],["أثر البحث","3","3"],["الخدمات والتحويل","3","3"]])
S.append(sec(6,"توزيع المحاور",mix+'<p class="small">15% من 30 يساوي 4.5، فوُزّع إلى 5 و4. الجدول الكامل في ملف Excel مع صيغ العد.</p><div class="warn">ملاحظة: التوزيع الفعلي للمنصات مائل لإنستجرام (17 من 30 مادة أساسية)، مع 5 لـLinkedIn و4 لـX و4 لفيسبوك. أخبرني إن كنت تريد رفع نصيب LinkedIn للمؤسسات.</div>',"التوزيع مقابل الـBrief."))
toc="".join(f'<a href="#d{i}"><b>{i}</b>{t}</a>' for i,t in enumerate(["الأسبوع 1","الأسبوع 2","الأسبوع 3","الأسبوع 4","الأسبوع 5","التوزيع"],1))
html=f'''<title>تقويم محتوى ClinStat 30 يومًا</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS.replace("Amiri,serif","'IBM Plex Sans Arabic',sans-serif").replace("Cairo,","'IBM Plex Sans Arabic',")}</style>
<div dir="rtl" lang="ar" class="layout"><nav class="rail" aria-label="المحتويات"><small>الأسابيع</small>{toc}</nav>
<main><div class="hero"><h1>تقويم محتوى ClinStat: 30 يومًا</h1><p>من الأحد 8 نوفمبر إلى الاثنين 7 ديسمبر 2026. مادة أساسية لكل يوم مع تكييف للمنصات. الكتابة الكاملة والتصميم في الجولة 3.</p><span class="tag">الجولة 2 من 5 · مسودة بانتظار المراجعة العلمية</span></div>
{"".join(S)}</main></div>'''
open("calendar_preview_ar.html","w").write(html);print(len(html))
