import openpyxl
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
G="003522";hf=Font(bold=True,color="FFFFFF");hfill=PatternFill("solid",fgColor=G)
thin=Side(style="thin",color="D9D9D2");bd=Border(left=thin,right=thin,top=thin,bottom=thin)
def head(ws,r,vals):
    for i,v in enumerate(vals,1):
        c=ws.cell(r,i,v);c.font=hf;c.fill=hfill;c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True);c.border=bd
def row(ws,r,vals):
    for i,v in enumerate(vals,1):
        c=ws.cell(r,i,v);c.alignment=Alignment(vertical="top",wrap_text=True,horizontal="right");c.border=bd
def prep(ws,w):
    ws.sheet_view.rightToLeft=True
    for i,x in enumerate(w,1): ws.column_dimensions[L(i)].width=x
# ---- KPI
wb=openpyxl.Workbook();ws=wb.active;ws.title="لوحة KPI"
ws["A1"]="ClinStat Research: لوحة مؤشرات الأداء";ws["A1"].font=Font(bold=True,size=16,color=G)
ws["A2"]="أدخل الأرقام الفعلية من إحصاءات المنصات فقط. الأهداف تُحدَّد بعد 4 أسابيع من خط أساس. لا تُدخل تقديرات كنتائج."
ws["A2"].font=Font(italic=True,color="5A6564")
H=["الفئة","المؤشر","المنصة/المصدر","التعريف","الأسبوع 1","الأسبوع 2","الأسبوع 3","الأسبوع 4","مجموع الشهر","الهدف (بعد خط الأساس)","الحالة"]
head(ws,4,H)
K=[("وعي","الوصول (Reach)","إنستجرام وفيسبوك وLinkedIn وX","عدد الحسابات الفريدة التي رأت المحتوى"),("وعي","مرات الظهور","كل المنصات","إجمالي مرات عرض المحتوى"),("وعي","مشاهدات الفيديو","إنستجرام وفيسبوك","مشاهدات الريلز والفيديو"),("وعي","نمو المتابعين","كل المنصات","صافي المتابعين الجدد"),
("تفاعل","معدل التفاعل","كل المنصات","التفاعلات ÷ الوصول"),("تفاعل","الحفظ","إنستجرام","عدد الحفظ"),("تفاعل","المشاركات","كل المنصات","عدد المشاركات"),("تفاعل","التعليقات","كل المنصات","عدد التعليقات"),("تفاعل","زيارات الملف الشخصي","إنستجرام وLinkedIn","زيارات الصفحة"),
("تحويل","نقرات الموقع","كل المنصات","النقرات على رابط الموقع"),("تحويل","عملاء محتملون مؤهلون","CRM","عملاء وصلوا مرحلة مؤهل"),("تحويل","حجوزات استشارة","CRM","استشارات محجوزة"),("تحويل","تكلفة العميل المحتمل","إعلانات","الإنفاق ÷ عدد العملاء المحتملين"),
("أعمال","نسبة التحويل إلى عميل","CRM","عملاء ناجحون ÷ عملاء محتملون"),("أعمال","تكلفة اكتساب العميل","إعلانات + أتعاب","إجمالي التكلفة ÷ عملاء جدد"),("أعمال","الإيراد حسب القناة","المالية","إيراد كل مصدر"),("أعمال","متوسط قيمة المشروع","المالية","إجمالي الإيراد ÷ عدد المشاريع"),("أعمال","العملاء المتكررون","CRM","عملاء لهم أكثر من مشروع")]
for i,(a,b,c,d) in enumerate(K,5):
    row(ws,i,[a,b,c,d,None,None,None,None,f"=IF(COUNT(E{i}:H{i})=0,\"\",SUM(E{i}:H{i}))","[بعد خط الأساس]",f'=IF(COUNT(E{i}:H{i})=0,"بدون بيانات","مُدخَل")'])
    for c in range(5,9): ws.cell(i,c).fill=PatternFill("solid",fgColor="FBEBCC")
prep(ws,[12,28,26,38,12,12,12,12,14,20,14]);ws.freeze_panes="C5"
n=wb.create_sheet("ملاحظات");prep(n,[60]);
for i,t in enumerate(["القيم في خلايا الأسابيع تُدخل يدويًا من لوحات المنصات.","التحويل إلى نسب (مثل معدل التفاعل) يحسب خارج الجدول أو بصيغة تضيفها بعد اتفاق التعريفات.","لا يُنشر أي رقم قبل مراجعة مصدره."],1): n.cell(i,1,t).alignment=Alignment(wrap_text=True,horizontal="right")
wb.save("ClinStat_KPI_Dashboard.xlsx")
# ---- CRM
wb=openpyxl.Workbook();ws=wb.active;ws.title="العملاء المحتملون"
H=["رقم العميل","تاريخ الوصول","الاسم","الجهة","الشريحة","الدولة","مصدر الوصول","الحملة","المرحلة","الخدمة المطلوبة","الإجراء التالي","تاريخ الإجراء","قيمة المشروع (عند الفوز)","ملاحظات"]
head(ws,1,H);prep(ws,[14,14,22,24,24,14,20,22,22,26,28,14,18,34])
lists=wb.create_sheet("القوائم");prep(lists,[24,24,28,24,18])
LS={"A":("المراحل",["عميل جديد","تم التواصل","مؤهل","استشارة محجوزة","استشارة منتهية","عرض مُرسل","تفاوض","ناجح","خاسر","متابعة لاحقًا"]),
"B":("المصدر",["إنستجرام","فيسبوك","LinkedIn","X","الموقع","إحالة","إعلان مدفوع","فعالية","أخرى"]),
"C":("الشريحة",["استشاري/طبيب باحث","باحث دراسات عليا","أكاديمي","مؤسسة"]),
"D":("الدولة",["السعودية","الإمارات","الكويت","قطر","عُمان","أخرى"]),
"E":("الحملة",["قبل ما تقدّم","افهم بياناتك","ابنِ بحثًا أفضل","عضوي","أخرى"])}
for col,(t,vals) in LS.items():
    lists[f"{col}1"]=t;lists[f"{col}1"].font=Font(bold=True)
    for i,v in enumerate(vals,2): lists[f"{col}{i}"]=v
def dv(col,lc,n):
    d=DataValidation(type="list",formula1=f"=القوائم!${lc}$2:${lc}${n+1}",allow_blank=False);ws.add_data_validation(d);d.add(f"{col}2:{col}500")
dv("I","A",10);dv("G","B",9);dv("E","C",4);dv("F","D",6);dv("H","E",5)
ws.freeze_panes="C2"
# mandatory source note
ws["P1"]="كل عميل محتمل يجب أن يملك مصدرًا (العمود G). حقل فارغ = سجل غير مكتمل."
s=wb.create_sheet("القمع");prep(s,[24,14,16])
head(s,1,["المرحلة","العدد","من الإجمالي"])
for i,v in enumerate(LS["A"][1],2):
    row(s,i,[v,f"=COUNTIF('العملاء المحتملون'!I2:I500,A{i})",f'=IF(SUM($B$2:$B$11)=0,"",B{i}/SUM($B$2:$B$11))']);s.cell(i,3).number_format="0%"
s2=wb.create_sheet("حسب المصدر");prep(s2,[24,14,14,14])
head(s2,1,["المصدر","عملاء محتملون","مؤهلون وما بعد","ناجحون"])
for i,v in enumerate(LS["B"][1],2):
    row(s2,i,[v,f"=COUNTIF('العملاء المحتملون'!G2:G500,A{i})",f"=COUNTIFS('العملاء المحتملون'!G2:G500,A{i},'العملاء المحتملون'!I2:I500,\"<>عميل جديد\",'العملاء المحتملون'!I2:I500,\"<>تم التواصل\",'العملاء المحتملون'!I2:I500,\"<>خاسر\",'العملاء المحتملون'!I2:I500,\"<>متابعة لاحقًا\")",f"=COUNTIFS('العملاء المحتملون'!G2:G500,A{i},'العملاء المحتملون'!I2:I500,\"ناجح\")"])
wb.save("ClinStat_CRM_Pipeline.xlsx");print("ok")
