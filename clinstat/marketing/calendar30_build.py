import openpyxl,datetime
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
import cal30_data as C
G="003522";hf=Font(bold=True,color="FFFFFF");hfill=PatternFill("solid",fgColor=G)
thin=Side(style="thin",color="D9D9D2");bd=Border(left=thin,right=thin,top=thin,bottom=thin)
def head(ws,r,v):
    for i,x in enumerate(v,1):
        c=ws.cell(r,i,x);c.font=hf;c.fill=hfill;c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True);c.border=bd
def row(ws,r,v):
    for i,x in enumerate(v,1):
        c=ws.cell(r,i,x);c.alignment=Alignment(vertical="top",wrap_text=True,horizontal="right");c.border=bd
def prep(ws,w):
    ws.sheet_view.rightToLeft=True
    for i,x in enumerate(w,1): ws.column_dimensions[L(i)].width=x
def fmt(f):
    return f if f=="منشور مهني" else ("منشور" if f.startswith("منشور") else f)
wb=openpyxl.Workbook();ws=wb.active;ws.title="التقويم"
ws["A1"]="ClinStat Research: تقويم المحتوى (30 يومًا)";ws["A1"].font=Font(bold=True,size=16,color=G)
ws["A2"]="تاريخ أول نشر";ws["B2"]=datetime.date(2026,11,8);ws["B2"].number_format="yyyy-mm-dd";ws["B2"].fill=PatternFill("solid",fgColor="FBEBCC")
ws["C2"]="غيّر B2 لتتحرك كل التواريخ. الحالات والمراجعون تُحدَّث بعد المراجعة العلمية والإبداعية."
ws["C2"].font=Font(italic=True,color="5A6564")
H=["رقم المحتوى","التاريخ","اليوم","المنصة الأساسية","منصات التكييف","المحور","السلسلة","الجمهور","هدف التسويق","الشكل","الحملة","الموضوع","الـHook","الرسالة الأساسية","الدعوة","المرجع العلمي (للتحقق)","الحالة","المراجع العلمي"]
head(ws,4,H)
for i,d in enumerate(C.D):
    r=5+i
    plat,ad,pil,ser,aud,obj,f,cam,topic,hook,core,cta,ref=d
    row(ws,r,[f"CS-{i+1:03d}",f"=$B$2+{i}",f'=CHOOSE(WEEKDAY(B{r},1),"الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت")',plat,ad,pil,ser,aud,obj,fmt(f),{"01":"01 قبل ما تقدّم","02":"02 افهم بياناتك","03":"03 ابنِ بحثًا أفضل"}[cam],topic,hook,core,cta,ref,"مسودة","[مطلوب]"])
    ws.cell(r,2).number_format="yyyy-mm-dd"
prep(ws,[12,13,12,14,16,22,22,22,16,14,18,32,40,44,24,34,16,16]);ws.freeze_panes="C5";ws.auto_filter.ref=f"A4:R{4+30}"
dv=DataValidation(type="list",formula1='"مسودة,مراجعة علمية,مراجعة إبداعية,معتمد,منشور"');ws.add_data_validation(dv);dv.add("Q5:Q34")
# pillars
p=wb.create_sheet("توزيع المحاور");prep(p,[28,14,14,14,14])
head(p,1,["المحور","النسبة المطلوبة","الهدف (من 30)","الفعلي","الفرق"])
T=[("التثقيف البحثي",.20,6),("الإحصاء الحيوي ببساطة",.20,6),("علامات خطر بحثية",.15,5),("قبل ما تقدّم",.15,4),("داخل ClinStat",.10,3),("أثر البحث",.10,3),("الخدمات والتحويل",.10,3)]
for i,(n,pc,t) in enumerate(T,2):
    row(p,i,[n,pc,t,f"=COUNTIF('التقويم'!F5:F34,A{i})",f"=D{i}-C{i}"]);p.cell(i,2).number_format="0%"
row(p,9,["المجموع","=SUM(B2:B8)","=SUM(C2:C8)","=SUM(D2:D8)","=D9-C9"]);p["B9"].number_format="0%"
p["A11"]="ملاحظة: 15% من 30 = 4.5، لذلك وُزّعت إلى 5 و4 ليبقى المجموع 30."
# platforms/formats
q=wb.create_sheet("المنصات والأشكال");prep(q,[24,12,6,24,12])
head(q,1,["المنصة الأساسية","العدد","","الشكل","العدد"])
for i,n in enumerate(["Instagram","LinkedIn","X","فيسبوك"],2): row(q,i,[n,f"=COUNTIF('التقويم'!D5:D34,A{i})"])
for i,n in enumerate(["ريل","كاروسيل","ستوري","منشور مهني","سلسلة تغريدات","منشور"],2):
    q.cell(i,4,n);q.cell(i,5,f"=COUNTIF('التقويم'!J5:J34,D{i})")
q["A8"]="المجموع";q["B8"]="=SUM(B2:B5)";q["D9"]="المجموع";q["E9"]="=SUM(E2:E7)"
# adaptation
a=wb.create_sheet("قواعد التكييف");prep(a,[16,30,40,44])
head(a,1,["المنصة","الشكل","نبرة المحتوى","قاعدة"])
for i,x in enumerate([("إنستجرام","ريل، كاروسيل، إنفوجرافيك، ستوري","بصرية ومختصرة","فكرة واحدة. العنوان فوق 3 ثوانٍ الأولى. نص على الشاشة"),("فيسبوك","منشور نقاش، مقتطف، نموذج","حوارية","سؤال يفتح النقاش ورابط واضح لصفحة الهبوط"),("LinkedIn","منشور مهني، مقال قصير","مهنية متعمقة","مثال واحد معمّق، مرجع علمي، دعوة للتواصل المؤسسي"),("X","سلسلة، نقطة إحصائية","علمية مباشرة","نقطة واحدة لكل تغريدة، 280 حرفًا، مصدر عند الحاجة")],2): row(a,i,list(x))
a["A7"]="لا يُنشر نفس النص على كل المنصات. المحتوى نفسه يُعاد تشكيله لكل منصة."
# series
s=wb.create_sheet("السلاسل");prep(s,[28,24,36,40])
head(s,1,["السلسلة","التكرار","الشكل","أرقام المحتوى"])
SER=["Research Red Flags","Behind the Statistics","Before You Submit","Research Mythbusters","Inside ClinStat","Research Case Files","Ask ClinStat","Services"]
for i,n in enumerate(SER,2):
    ids=", ".join(f"CS-{k+1:03d}" for k,d in enumerate(C.D) if d[3]==n)
    row(s,i,[n,{"Research Red Flags":"أسبوعي","Behind the Statistics":"أسبوعي","Before You Submit":"أسبوعي","Research Mythbusters":"كل أسبوعين","Inside ClinStat":"كل أسبوعين","Research Case Files":"شهري (أمثلة تعليمية فقط)","Ask ClinStat":"أسبوعي","Services":"حسب الحملة"}[n],"حسب السلسلة",ids])
# rules
r=wb.create_sheet("قواعد المراجعة");prep(r,[26,60])
head(r,1,["البند","القاعدة"])
for i,x in enumerate([("رقم المحتوى","CS-001 إلى CS-030 لهذا الشهر. الشهر التالي يبدأ بـCS-031"),("تدفق الحالة","مسودة ← مراجعة علمية ← مراجعة إبداعية ← معتمد ← منشور"),("المراجعة العلمية","التحقق من كل ادعاء، والتمييز بين الدلالة الإحصائية والأهمية السريرية، ومنع الربط بين الارتباط والسببية"),("المراجع","تُذكر أسماء الإرشادات فقط. لا DOI ولا روابط قبل التحقق من المصدر الأصلي"),("فحوص إبداعية","الإملاء، موضع الشعار، ألوان الهوية، جودة الصورة، مقاسات المنصة"),("الحالات الحساسة","لا حالات عملاء وهمية ولا شهادات بدون إذن مكتوب"),("المحتوى الداخلي","عناصر داخل ClinStat وأثر البحث بين [ ] حتى تؤكدها الإدارة"),("عدم الضمان","لا وعد بقبول مجلة")],2): row(r,i,list(x))
wb.save("ClinStat_Content_Calendar_30D.xlsx");print("saved")
