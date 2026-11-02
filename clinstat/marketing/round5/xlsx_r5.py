import openpyxl
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
G="003522";hf=Font(bold=True,color="FFFFFF");hfill=PatternFill("solid",fgColor=G)
thin=Side(style="thin",color="D9D9D2");bd=Border(left=thin,right=thin,top=thin,bottom=thin)
IN=PatternFill("solid",fgColor="FBEBCC")
def head(ws,r,v):
    for i,x in enumerate(v,1):
        c=ws.cell(r,i,x);c.font=hf;c.fill=hfill;c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True);c.border=bd
def row(ws,r,v,inp=()):
    for i,x in enumerate(v,1):
        c=ws.cell(r,i,x);c.alignment=Alignment(vertical="top",wrap_text=True,horizontal="right");c.border=bd
        if i in inp:c.fill=IN
def prep(ws,w):
    ws.sheet_view.rightToLeft=True
    for i,x in enumerate(w,1): ws.column_dimensions[L(i)].width=x
def title(ws,t,s):
    ws["A1"]=t;ws["A1"].font=Font(bold=True,size=14,color=G);ws["A2"]=s
def lst(ws,vals,rng):
    dv=DataValidation(type="list",formula1='"'+",".join(vals)+'"',allow_blank=True);ws.add_data_validation(dv);dv.add(rng)
wb=openpyxl.Workbook()
# 1 approval log
a=wb.active;a.title="سجل الاعتماد";title(a,"سجل اعتماد المحتوى","كل عنصر يمر بالبنود بالترتيب. الخلايا الصفراء إدخال. العنصر لا يُنشر قبل أن تكون الحالة «جاهز للنشر».")
H=["المعرف","العنوان","دقة علمية","مراجعة لغوية","الشعار والألوان","المقاسات","المراجع بالاسم","لا ضمانات / لا أرقام مخترعة","موافقة المالك (إن لزمت)","عدد البنود غير المكتملة","الحالة"]
head(a,4,H)
for r in range(5,65):
    row(a,r,[None]*9,inp=range(1,10))
    a.cell(r,10,f'=IF(A{r}="","",COUNTIF(C{r}:I{r},"لا")+COUNTBLANK(C{r}:I{r}))')
    a.cell(r,11,f'=IF(A{r}="","",IF(J{r}=0,"جاهز للنشر",IF(COUNTIF(C{r}:I{r},"لا")>0,"يحتاج تعديل","قيد المراجعة")))')
    for c in (10,11):a.cell(r,c).border=bd
lst(a,["نعم","لا","لا ينطبق"],"C5:I64")
prep(a,[11,32,12,12,14,12,14,22,18,14,16])
# 2 publishing tracker
p=wb.create_sheet("جدول النشر");title(p,"جدول النشر والمتابعة","سجّل كل منشور بعد نشره. يربط بالمعرف في التقويم.")
head(p,4,["المعرف","المنصة","التاريخ المخطط","التاريخ الفعلي","رابط المنشور [مطلوب]","المسؤول","الحالة","ملاحظات","تأخير بالأيام"])
for r in range(5,65):
    row(p,r,[None]*8,inp=range(1,9));p.cell(r,9,f'=IF(OR(C{r}="",D{r}=""),"",D{r}-C{r})').border=bd
    p.cell(r,3).number_format=p.cell(r,4).number_format="yyyy-mm-dd"
lst(p,["Instagram","Facebook","LinkedIn","X"],"B5:B64");lst(p,["مجدول","منشور","مؤجل","ملغى"],"G5:G64")
prep(p,[11,14,15,15,34,16,12,30,12])
# 3 community log
c=wb.create_sheet("سجل المجتمع");title(c,"سجل التعليقات والرسائل","اكتب كل تفاعل يحتاج متابعة. لا تسجل بيانات مرضى أو معلومات تعريفية.")
head(c,4,["التاريخ","المنصة","النوع","الموضوع","الأولوية","زمن الرد المستهدف (ساعات)","وقت الرد الفعلي (ساعات)","النتيجة","تصعيد؟","ملاحظات"])
for r in range(5,105):
    row(c,r,[None]*10,inp=range(1,11));c.cell(r,1).number_format="yyyy-mm-dd"
    c.cell(r,6,f'=IF(E{r}="","",IF(E{r}="عاجل",2,IF(E{r}="عادي",24,48)))').border=bd
lst(c,["Instagram","Facebook","LinkedIn","X","واتساب","بريد"],"B5:B104")
lst(c,["سؤال علمي","طلب استشارة","شكوى","انتقاد علمي","سبام","سؤال طبي شخصي","أخرى"],"C5:C104")
lst(c,["عاجل","عادي","منخفض"],"E5:E104");lst(c,["تم الرد","حُوّل للمبيعات","حُوّل للمراجع العلمي","تم الإخفاء/الحذف","مفتوح"],"H5:H104");lst(c,["نعم","لا"],"I5:I104")
prep(c,[13,12,18,28,11,16,16,20,10,30])
# 4 weekly report
w=wb.create_sheet("تقرير أسبوعي");title(w,"التقرير الأسبوعي","أدخل الأرقام الفعلية من المنصات والـCRM. لا تُدخل تقديرات. الأهداف تُحدَّد بعد 4 أسابيع من البيانات الفعلية (خلية الهدف فارغة عمدًا).")
w["A3"]="بداية الأسبوع";w["B3"]=None;w["B3"].fill=IN;w["B3"].number_format="yyyy-mm-dd"
head(w,5,["المؤشر","الأسبوع الحالي","الأسبوع السابق","التغير","التغير %","الهدف [يُحدَّد لاحقًا]","المصدر"])
M=[("المنشورات المنشورة","جدول النشر"),("مرات الظهور (Impressions)","المنصات"),("الوصول (Reach)","المنصات"),("التفاعلات (إعجاب/تعليق/مشاركة)","المنصات"),("الحفظ","Instagram"),("المشاركات","المنصات"),("نقرات الرابط","المنصات / UTM"),("زيارات الموقع","Analytics"),("تحميلات قائمة الفحص","صفحة الهبوط"),("اشتراكات البريد","منصة البريد"),("استفسارات واردة","CRM"),("عملاء مؤهلون","CRM"),("استشارات محجوزة","CRM"),("متابعون جدد","المنصات")]
for i,(m,s) in enumerate(M,6):
    row(w,i,[m,None,None,None,None,None,s],inp=(2,3,6))
    w.cell(i,4,f'=IF(OR(B{i}="",C{i}=""),"",B{i}-C{i})').border=bd
    w.cell(i,5,f'=IF(OR(B{i}="",C{i}="",C{i}=0),"",(B{i}-C{i})/C{i})').border=bd;w.cell(i,5).number_format="0.0%"
n=6+len(M)
w.cell(n+1,1,"معدل التفاعل = التفاعلات ÷ الوصول");w.cell(n+1,2,f'=IF(OR(B9="",B8="",B8=0),"",B9/B8)');w.cell(n+1,2).number_format="0.0%"
w.cell(n+2,1,"معدل النقر = نقرات الرابط ÷ الوصول");w.cell(n+2,2,f'=IF(OR(B12="",B8="",B8=0),"",B12/B8)');w.cell(n+2,2).number_format="0.0%"
w.cell(n+3,1,"تحويل الزيارات إلى تحميلات = تحميلات ÷ زيارات");w.cell(n+3,2,f'=IF(OR(B14="",B13="",B13=0),"",B14/B13)');w.cell(n+3,2).number_format="0.0%"
w.cell(n+4,1,"تأهيل الاستفسارات = مؤهلون ÷ استفسارات");w.cell(n+4,2,f'=IF(OR(B17="",B16="",B16=0),"",B17/B16)');w.cell(n+4,2).number_format="0.0%"
for k in range(n+1,n+5):w.cell(k,1).font=Font(bold=True)
q=n+6
for j,t in enumerate(["أفضل 3 منشورات (المعرف + السبب)","أضعف 3 منشورات (المعرف + السبب)","ما تعلمناه هذا الأسبوع","القرار للأسبوع القادم (محتوى/توقيت/دعوة)","مشكلات تحتاج مالكًا"]):
    w.cell(q+j,1,t).font=Font(bold=True);w.merge_cells(start_row=q+j,start_column=2,end_row=q+j,end_column=7);w.cell(q+j,2).fill=IN;w.row_dimensions[q+j].height=45
prep(w,[44,16,16,12,12,22,18])
# 5 monthly
m=wb.create_sheet("تقرير شهري");title(m,"التقرير الشهري","يجمع 4 أسابيع. أدخل إجمالي كل أسبوع. الخلية الفارغة تُترك فارغة ولا تُملأ بصفر.")
head(m,4,["المؤشر","أسبوع 1","أسبوع 2","أسبوع 3","أسبوع 4","إجمالي الشهر","الشهر السابق","التغير %"])
for i,(x,s) in enumerate(M,5):
    row(m,i,[x,None,None,None,None,None,None,None],inp=(2,3,4,5,7))
    m.cell(i,6,f'=IF(COUNT(B{i}:E{i})=0,"",SUM(B{i}:E{i}))').border=bd
    m.cell(i,8,f'=IF(OR(F{i}="",G{i}="",G{i}=0),"",(F{i}-G{i})/G{i})').border=bd;m.cell(i,8).number_format="0.0%"
k=5+len(M)+1
head(m,k,["قمع التحويل","العدد","نسبة من المرحلة السابقة"])
steps=[("وصول","F7"),("نقرات الرابط","F11"),("زيارات الموقع","F12"),("تحميلات القائمة","F13"),("استفسارات","F15"),("مؤهلون","F16"),("استشارات محجوزة","F17")]
for j,(t,ref) in enumerate(steps):
    r=k+1+j;row(m,r,[t,f'=IF({ref}="","",{ref})',None])
    if j: m.cell(r,3,f'=IF(OR(B{r}="",B{r-1}="",B{r-1}=0),"",B{r}/B{r-1})').number_format="0.0%"
r=k+len(steps)+2
for j,t in enumerate(["حالة المحاور السبعة (ما زاد وما قل)","أداء الحملات 01/02/03 (مؤشر لكل حملة)","أفضل المحتوى ولماذا","ما سنوقفه","ما سنكرره ونوسّعه","اختبارات الشهر القادم (فرضية + مقياس)","مخاطر وملاحظات علمية/قانونية"]):
    m.cell(r+j,1,t).font=Font(bold=True);m.merge_cells(start_row=r+j,start_column=2,end_row=r+j,end_column=8);m.cell(r+j,2).fill=IN;m.row_dimensions[r+j].height=45
prep(m,[40,12,12,12,12,14,14,12])
# 6 experiments
e=wb.create_sheet("سجل الاختبارات");title(e,"سجل اختبارات التحسين","فرضية واحدة لكل اختبار. لا نغيّر أكثر من متغير واحد. القرار بعد حجم بيانات كافٍ وليس بعد منشور واحد.")
head(e,4,["#","الفرضية","المتغير المختبَر","المقياس الأساسي","بداية","نهاية","النسخة أ","النسخة ب","القرار","ما تعلمناه"])
for r in range(5,25):
    row(e,r,[r-4]+[None]*9,inp=range(2,11));e.cell(r,5).number_format=e.cell(r,6).number_format="yyyy-mm-dd"
lst(e,["الهوك","الشكل (كاروسيل/ريل)","وقت النشر","الدعوة CTA","العنوان","الصورة","الجمهور"],"C5:C24");lst(e,["نعتمد أ","نعتمد ب","غير حاسم، نعيد","نوقف"],"I5:I24")
prep(e,[5,34,20,22,13,13,22,22,18,34])
wb.save("ClinStat_Reporting_Templates.xlsx")
