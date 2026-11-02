import asyncio,os
from data5 import *
FD=os.path.abspath("../../posts/fonts")
def tb(h,rows):return "<table><tr>"+"".join(f"<th>{x}</th>" for x in h)+"</tr>"+"".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)+"</table>"
css=f'''@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Regular.ttf);font-weight:400}}@font-face{{font-family:PX;src:url(file://{FD}/PlexAr-Bold.ttf);font-weight:700}}
@page{{size:A4;margin:14mm}}body{{font-family:PX;direction:rtl;color:#0B1F33;font-size:10.5pt;line-height:1.5}}
h1{{color:#103D2E;font-size:20pt;margin:0 0 2mm}}h2{{color:#103D2E;font-size:13pt;border-bottom:2px solid #A8854E;padding-bottom:1mm;margin:6mm 0 3mm}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt}}th{{background:#103D2E;color:#fff;padding:2mm;text-align:right}}td{{border:1px solid #d9d9d2;padding:2mm;vertical-align:top}}tr{{page-break-inside:avoid}}
.n{{color:#555;font-size:9pt;margin-top:3mm}}.pb{{page-break-before:always}}'''
b=f'''<html dir="rtl" lang="ar"><meta charset="utf-8"><style>{css}</style><body>
<h1>بوابات الاعتماد وإجراءات النشر</h1><p>ClinStat Research | Research that survives peer review</p>
<h2>بوابات الاعتماد (12 بندًا)</h2>{tb(["#","البوابة","المعيار","المسؤول"],GATES)}
<p class="n">لا يُنشر عنصر إلا إذا كانت كل البنود «نعم» أو «لا ينطبق».</p>
<div class="pb"></div><h2>مسار الحالة</h2>{tb(["الحالة","المسؤول","ما يُفحص"],FLOW)}
<h2>إجراءات النشر</h2>{tb(["الوقت","الإجراء"],SOP)}
<h2>مستويات التصعيد</h2>{tb(["المستوى","أمثلة","الإجراء"],ESC)}
<p class="n">زمن الرد المذكور في ملف Excel أرقام مقترحة قابلة للتعديل. أسماء المسؤولين [مطلوب].</p></body></html>'''
open("sop.html","w").write(b)
async def m():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome");pg=await br.new_page();await pg.goto("file://"+os.path.abspath("sop.html"));await pg.wait_for_timeout(500)
        await pg.pdf(path="ClinStat_Approval_and_Publishing_SOP_AR.pdf",format="A4",print_background=True,prefer_css_page_size=True);await br.close()
asyncio.run(m())
