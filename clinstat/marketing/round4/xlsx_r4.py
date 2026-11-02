import openpyxl
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
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
wb=openpyxl.Workbook();u=wb.active;u.title="بناء UTM"
u["A1"]="بناء روابط UTM";u["A1"].font=Font(bold=True,size=14,color=G)
u["A2"]="ضع رابط الصفحة في B3 واختر القيم. الصيغة تنتج الرابط النهائي. لا تستخدم مسافات."
u["A3"]="رابط الصفحة [مطلوب]";u["B3"]="https://example.com/landing"
u["B3"].fill=PatternFill("solid",fgColor="FBEBCC")
head(u,5,["المصدر (source)","الوسيط (medium)","الحملة (campaign)","المحتوى (content)","الرابط النهائي"])
SRC=["instagram","facebook","linkedin","x","email","whatsapp","website"]
MED=["paid_social","organic_social","email","referral","messaging"]
CAM=["byfs_checklist","understand_data","build_better","organic"]
combos=[("instagram","paid_social","byfs_checklist","A_feed"),("instagram","paid_social","byfs_checklist","B_story"),("facebook","paid_social","understand_data","A_feed"),("linkedin","paid_social","build_better","A_linkedin"),("instagram","organic_social","organic","bio_link"),("email","email","byfs_checklist","seq_d5")]
for i,(a,b,c,d) in enumerate(combos,6):
    row(u,i,[a,b,c,d,f'=$B$3&"?utm_source="&A{i}&"&utm_medium="&B{i}&"&utm_campaign="&C{i}&"&utm_content="&D{i}'])
for r in range(12,26): row(u,r,[None,None,None,None,f'=IF(A{r}="","",$B$3&"?utm_source="&A{r}&"&utm_medium="&B{r}&"&utm_campaign="&C{r}&"&utm_content="&D{r})'])
for col,vals in(("A",SRC),("B",MED),("C",CAM)):
    dv=DataValidation(type="list",formula1='"'+",".join(vals)+'"',allow_blank=True);u.add_data_validation(dv);dv.add(f"{col}6:{col}25")
prep(u,[18,18,22,20,70])
q=wb.create_sheet("تأهيل العملاء");q["A1"]="درجة التأهيل (اقتراح قابل للتعديل)";q["A1"].font=Font(bold=True,size=14,color=G)
head(q,3,["رقم العميل","الخدمة مطابقة (0-2)","المرحلة (0-2)","الموعد (0-2)","القرار والتمويل (0-2)","الدولة والجهة (0-2)","الدرجة","التصنيف"])
for r in range(4,54):
    row(q,r,[None]*5+[None])
    q.cell(r,7,f'=IF(COUNT(B{r}:F{r})=0,"",SUM(B{r}:F{r}))')
    q.cell(r,8,f'=IF(G{r}="","",IF(G{r}>=6,"مؤهل",IF(G{r}>=3,"متابعة لاحقًا","غير مناسب حاليًا")))')
dv=DataValidation(type="whole",operator="between",formula1="0",formula2="2");q.add_data_validation(dv);dv.add("B4:F53")
q["J3"]="الحدود (للضبط)";q["J4"]="مؤهل: 6 فما فوق";q["J5"]="متابعة لاحقًا: 3 إلى 5"
prep(q,[14,16,14,14,18,18,12,18,4,24])
r=wb.create_sheet("قواعد");prep(r,[26,70])
head(r,1,["البند","القاعدة"])
for i,x in enumerate([("المصدر","إلزامي لكل عميل في الـCRM"),("الموافقة","لا رسائل تسويقية بدون موافقة موثقة مع طريقة إلغاء"),("الرد الأول","خلال يوم عمل"),("البيانات الحساسة","لا نطلب بيانات مرضى أو معلومات تعريفية من العملاء"),("النقاط","اقتراح للتجربة ويُعدَّل بعد أول 30 يومًا من البيانات")],2): row(r,i,list(x))
wb.save("ClinStat_UTM_and_Lead_Qualification.xlsx")
