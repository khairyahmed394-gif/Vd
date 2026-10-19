"""Builds the content-pack index (xlsx + csv + md) that maps every slot of the 60-post calendar to the generated files."""
import csv, datetime, os, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
CAL = "/root/.claude/uploads/df449ede-5117-59e3-8a34-d2bd6e6d8a4b/95addd34-ClinStat_3-Month_Content_Calendar_AR.xlsx"
START = datetime.date(2026, 10, 18); DAYN = {"الأحد": 0, "الإثنين": 1, "الثلاثاء": 2, "الأربعاء": 3, "الخميس": 4}
POST = {(1,"الإثنين"):["wk01_mon_s1_cover","wk01_mon_s2_design","wk01_mon_s3_data","wk01_mon_s4_analysis","wk01_mon_s5_interpretation","wk01_mon_s6_reporting","wk01_mon_s7_save"],(1,"الخميس"):["wk01_thu_study_design"],(2,"الإثنين"):["wk02_mon_reporting_guidelines"],(3,"الإثنين"):["wk03_mon_gcc_checklist"],(3,"الخميس"):["wk03_thu_five_questions"],(4,"الإثنين"):["wk04_mon_editor_first_minute"],(5,"الإثنين"):["wk05_mon_ownership"],(5,"الخميس"):["wk05_thu_team"],(6,"الإثنين"):["wk06_mon_case_study"],(7,"الإثنين"):["wk07_mon_readiness_checklist"],(7,"الخميس"):["wk07_thu_icmje"],(8,"الإثنين"):["wk08_mon_scale_rescue_independence"],(9,"الإثنين"):["wk09_mon_forest_plot"],(9,"الخميس"):["wk09_thu_effect_measures"],(10,"الإثنين"):["wk10_mon_risk_of_bias"],(11,"الإثنين"):["wk11_mon_free_consultation"],(11,"الخميس"):["wk11_thu_partnership"],(12,"الإثنين"):["wk12_mon_readiness_10"]}
REEL = {(1,"الثلاثاء"):"wk01_tue_assumptions",(2,"الثلاثاء"):"wk02_tue_design",(2,"الخميس"):"wk02_thu_test",(3,"الثلاثاء"):"wk03_tue_rejected",(4,"الثلاثاء"):"wk04_tue_outcome",(4,"الخميس"):"wk04_thu_missing",(5,"الثلاثاء"):"wk05_tue_reviewers",(6,"الثلاثاء"):"wk06_tue_triage",(6,"الخميس"):"wk06_thu_methods",(7,"الثلاثاء"):"wk07_tue_desk_rejection",(8,"الثلاثاء"):"wk08_tue_predatory",(8,"الخميس"):"wk08_thu_ethics",(9,"الثلاثاء"):"wk09_tue_fixed_random",(10,"الثلاثاء"):"wk10_tue_sensitivity",(10,"الخميس"):"wk10_thu_i2",(11,"الثلاثاء"):"wk11_tue_three_results",(12,"الثلاثاء"):"wk12_tue_model",(12,"الخميس"):"wk12_thu_last_batch"}
CONFIRM = {"wk05_mon_ownership":"","wk05_thu_team":"50+ papers / h-index 5+ per member: confirm","wk06_mon_case_study":"case figures: confirm with the client","wk11_thu_partnership":"~100 papers per quarter, 80% published: confirm","wk03_mon_gcc_checklist":"checklist contents are generic: replace with the real GCC checklist","wk07_mon_readiness_checklist":"bullets are generic: match the real checklist","wk08_mon_scale_rescue_independence":"descriptions are generic: no case numbers","wk11_mon_free_consultation":"process steps are proposed: confirm","wk12_mon_readiness_10":"10 items are proposed: match the real checklist","wk01_mon_s2_design":"15 checks written here: statistician to review"}
tw = {}
for r in csv.DictReader(open("tweets/tweets.csv", encoding="utf-8-sig")): tw[(int(r["week"]), r["day"])] = r
TDAY = {"Sun": "الأحد", "Wed": "الأربعاء"}
tw = {(w, TDAY[d]): r for (w, d), r in tw.items()}
ws = openpyxl.load_workbook(CAL)["التقويم"]; rows = []
for r in ws.iter_rows(min_row=5, values_only=True):
    if not (r[0] and str(r[0]).startswith("الشهر")): continue
    wk, day, fmt = int(r[1]), r[2], r[4]; date = START + datetime.timedelta(days=(wk - 1) * 7 + DAYN[day])
    if fmt == "تويتة": ar = f"tweets/tweets.md (week {wk}, {['Sun','Wed'][0 if day=='الأحد' else 1]})"; en = ar; note = tw[(wk, day)]["note"]; files = ""
    elif fmt == "بوست ثابت":
        names = POST[(wk, day)]; ar = " + ".join(f"posts/out/ar/{n}.png" for n in names); en = " + ".join(f"posts/out/en/{n}.png" for n in names); note = "; ".join(CONFIRM[n] for n in names if CONFIRM.get(n))
    else: n = REEL[(wk, day)]; ar = f"reels/out/ar/{n}.mp4"; en = f"reels/out/en/{n}.mp4"; note = "script written here; calendar had only the hook" + ("; confirm the offer/availability" if n in ("wk12_thu_last_batch",) else "") + ("; confirm the case/results wording" if n == "wk11_tue_three_results" else "")
    rows.append([r[0], wk, day, str(date), fmt, r[5], r[6], r[7], r[8], r[9], r[10], ar, en, note])
hdr = ["الشهر / Month", "الأسبوع / Week", "اليوم / Day", "التاريخ / Date", "الصيغة / Format", "المنصة / Platform", "الموضوع / Topic", "الـHook", "Funnel", "CTA", "حالة الكتابة (التقويم) / Calendar status", "الملفات العربية / Arabic files", "English files", "ملاحظات قبل النشر / Before publishing"]
wb = openpyxl.Workbook(); sh = wb.active; sh.title = "Content pack"; sh.sheet_view.rightToLeft = True; sh.append(hdr)
for c in sh[1]: c.font = Font(bold=True, color="F7F4ED"); c.fill = PatternFill("solid", fgColor="103D2E"); c.alignment = Alignment(wrap_text=True, vertical="center")
for r in rows: sh.append(r)
for i, wdt in enumerate([9, 9, 10, 12, 12, 20, 38, 38, 10, 38, 14, 60, 60, 50], 1): sh.column_dimensions[get_column_letter(i)].width = wdt
for row in sh.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
sh.freeze_panes = "A2"; wb.save("ClinStat_Content_Pack_Index.xlsx")
with open("content_pack_index.csv", "w", encoding="utf-8-sig", newline="") as f: w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
missing = [p for r in rows for p in (r[11].split(" + ") + r[12].split(" + ")) if p.endswith((".png", ".mp4")) and not os.path.exists(p)]
print(len(rows), "slots; missing files:", missing)
