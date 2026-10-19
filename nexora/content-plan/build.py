"""NEXORA 12-week content plan: calendar.xlsx/csv + NEXORA_Content_Plan.pdf. Change START to move all dates. python3 build.py"""
import os, csv, datetime, html, collections
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from playwright.sync_api import sync_playwright
from core import CORE
from assets import *
HERE = os.path.dirname(os.path.abspath(__file__))
START = datetime.date(2026, 11, 1)   # proposed Sunday start, change as needed
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu"]
# weekly rhythm: (day index, platform, core slot A/B/C or REEL)
RHYTHM = [(0, "LinkedIn", "A"), (1, "Facebook", "A"), (1, "LinkedIn", "B"), (2, "Instagram", "A"), (2, "Facebook", "B"), (2, "Reels (IG + FB)", "R"), (3, "Instagram", "B"), (3, "LinkedIn", "C"), (4, "Facebook", "C"), (4, "Instagram", "C")]
TAGS = {"Diagnose": ("#BusinessGrowth #SME #Egypt", "#نمو_الأعمال #مصر #أصحاب_الأعمال"), "Systems": ("#Operations #SOP #Egypt", "#إدارة_العمليات #SOP #مصر"), "Numbers": ("#KPIs #BusinessPerformance #Egypt", "#مؤشرات_الأداء #إدارة_الأداء #مصر"),
        "People": ("#Leadership #Training #Egypt", "#التدريب #القيادة #مصر"), "Proof": ("#CaseStudy #BusinessGrowth #Egypt", "#دراسة_حالة #نمو_الأعمال #مصر"), "Brand": ("#NEXORA #BuildBetterGrowSmarter #Egypt", "#NEXORA #ابنِ_أفضل #مصر"),
        "Marketing": ("#Marketing #BusinessGrowth #Egypt", "#التسويق #نمو_الأعمال #مصر"), "Sector": ("#Fitness #Hospitality #Egypt", "#اللياقة #الضيافة #مصر"), "Objection": ("#BusinessAdvice #SME #Egypt", "#نصائح_أعمال #مصر"), "Sales": ("#Sales #FollowUp #Egypt", "#المبيعات #المتابعة #مصر")}
SIZE = {"LinkedIn": "1200x627 image, or 1080x1350 PDF carousel", "Facebook": "1080x1350", "Instagram": "1080x1350", "Reels (IG + FB)": "1080x1920, 12-20 s"}
LANG = {"LinkedIn": "EN first, AR line below", "Facebook": "AR first, short EN line", "Instagram": "AR caption, EN title on image", "Reels (IG + FB)": "AR + EN on-screen text"}
def date_of(w, d): return START + datetime.timedelta(days=(w - 1) * 7 + d)
def platform_format(fmt, plat):
    if plat == "LinkedIn": return {"Carousel": "Document carousel (PDF)", "Infographic": "Image", "Checklist image": "Image", "Event invite": "Image + event link", "Case study": "Long post + image"}.get(fmt, "Text + image")
    return {"Carousel": "Carousel", "Infographic": "Image", "Checklist image": "Image", "Event invite": "Image + event link", "Case study": "Carousel", "Text + image": "Image post"}.get(fmt, fmt)
rows = []
for w in range(1, 13):
    cs = {s: CORE[(w - 1) * 3 + i] for i, s in enumerate("ABC")}
    for d, plat, slot in RHYTHM:
        dt = date_of(w, d)
        if slot == "R":
            r = REELS[w - 1]
            rows.append([w, DAYS[d], dt.isoformat(), plat, "Reel", "Short video", "Aware", r[1], r[2], "On-screen: " + r[4] + " | " + r[5], r[8], r[9], r[10], "Cover: " + r[7] + ". " + SIZE[plat], "#NEXORA #BusinessGrowth | #NEXORA #نمو_الأعمال", f"nexora_reels_wk{w}_{w}R", "3s hold, completion, saves", ""])
            continue
        c = cs[slot]; i, pillar, stage, fmt, title, he, be, ce, ha, ba, ca, vis, kpi, flag = c
        pf = platform_format(fmt, plat); tags = TAGS.get(pillar, TAGS["Brand"])
        if plat == "LinkedIn": hook, body, cta = he, be, ce; second = "AR: " + ha
        else: hook, body, cta = ha, ba, ca; second = "EN: " + he
        rows.append([w, DAYS[d], dt.isoformat(), plat, pf, pillar, stage, title, hook, body + "\n\n" + second, cta, f"{vis}. Size: {SIZE[plat]}. Language: {LANG[plat]}", tags[0] if plat == "LinkedIn" else tags[1], "", f"nexora_{plat[:2].lower()}_{pf[:3].lower()}_wk{w}_{i}", kpi, flag])
        rows[-1][13] = rows[-1].pop(13) if False else rows[-1][13]
HEAD = ["Week", "Day", "Date", "Platform", "Format", "Pillar", "Funnel stage", "Working title", "Hook (first line)", "Copy (primary + secondary language)", "CTA", "Visual brief", "Hashtags", "-", "UTM suffix", "KPI to watch", "Needs confirmation"]
# fix the column mismatch for reel rows (they have 18 values) -> normalise to HEAD length
norm = []
for r in rows:
    if r[3].startswith("Reels"):
        norm.append([r[0], r[1], r[2], r[3], r[4], "Short video", r[6], r[7], r[8], r[9], r[12], r[13], r[14], "", r[15], r[16], r[17]])
    else: norm.append(r)
rows = [r for r in norm]
for r in rows: r.pop(13)
HEAD.pop(13)
rows.sort(key=lambda r: (r[0], r[2], ["LinkedIn", "Facebook", "Instagram", "Reels (IG + FB)"].index(r[3])))
events = [[4, "Thu", date_of(4, 4).isoformat(), "Workshop 1", WORKSHOPS[0][0], "Free, 45 min (invite in 4C)"], [8, "Thu", date_of(8, 4).isoformat(), "Workshop 2", WORKSHOPS[1][0], "Free, 45 min (invite in 8C)"], [12, "Wed", date_of(12, 3).isoformat(), "Workshop 3", WORKSHOPS[2][0], "Free, 45 min (invite via newsletter and stories)"],
          [4, "Thu", date_of(4, 4).isoformat(), "Newsletter", NEWS[0][0], NEWS[0][1][0]], [8, "Thu", date_of(8, 4).isoformat(), "Newsletter", NEWS[1][0], NEWS[1][1][0]], [12, "Thu", date_of(12, 4).isoformat(), "Newsletter", NEWS[2][0], NEWS[2][1][0]],
          [3, "Thu", date_of(3, 4).isoformat(), "Lead magnet", "Business Health Scorecard", "Launch (3C)"], [4, "Sun", date_of(4, 0).isoformat(), "Lead magnet", "SOP starter template", "Release (4A)"], [5, "Tue", date_of(5, 2).isoformat(), "Lead magnet", "Sales follow-up checklist", "Release (3A, 5B follow-up in DMs)"], [7, "Wed", date_of(7, 3).isoformat(), "Lead magnet", "Weekly KPI dashboard", "Release (7C)"]]
wb = openpyxl.Workbook()
def sheet(name, head, data, widths):
    ws = wb.create_sheet(name); ws.append(head)
    for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="101C2C"); c.alignment = Alignment(wrap_text=True, vertical="center")
    for r in data: ws.append(r)
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
wb.remove(wb.active)
sheet("Calendar", HEAD, rows, [6, 6, 11, 14, 18, 11, 10, 24, 40, 70, 28, 50, 28, 26, 22, 24])
sheet("Core copy", ["ID", "Week", "Pillar", "Stage", "Format", "Title", "Hook EN", "Body EN", "CTA EN", "Hook AR", "Body AR", "CTA AR", "Visual", "KPI", "Needs confirmation"], [[c[0], (i // 3) + 1, c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13]] for i, c in enumerate(CORE)], [6, 6, 11, 10, 14, 24, 40, 70, 28, 40, 70, 28, 40, 18, 30])
sheet("Reels", ["Week", "Title", "Hook", "Beats", "On-screen EN", "On-screen AR", "Sound", "Cover", "Caption EN", "Caption AR", "CTA"], [list(r) for r in REELS], [6, 22, 28, 50, 36, 36, 22, 24, 40, 40, 18])
sheet("Carousels", ["Carousel", "Slide", "EN", "AR"], [[k, i + 1, a, b] for k, v in CAROUSELS.items() for i, (a, b) in enumerate(v)], [20, 6, 50, 50])
sheet("Lead magnets", ["Name", "Content"], [[k, v] for k, v in MAGNETS.items()], [28, 120])
sheet("Scorecard", ["#", "Area", "Question EN", "Question AR", "Score"], [[i + 1, a, b, c, "0 no / 1 partly / 2 yes"] for i, (a, b, c) in enumerate(SCORE_Q)], [4, 12, 70, 60, 22])
sheet("Workshops", ["Title", "For", "45-min agenda", "Exercise", "Follow-up offer"], [list(w) for w in WORKSHOPS], [32, 22, 80, 30, 24])
sheet("Newsletters", ["Issue", "Subject EN", "Subject AR", "Sections"], [[n[0], n[1][0], n[1][1], "; ".join(n[2])] for n in NEWS], [10, 40, 40, 80])
sheet("Outreach", ["Message", "EN", "AR"], [list(o) for o in OUTREACH], [28, 80, 80])
sheet("Stories", ["Week", "Theme", "Sun", "Tue", "Thu"], [[w, STORY_THEMES[w]] + [f"{k}: {STORY_THEMES[w]}" for k in STORY_KIND] for w in range(1, 13)], [6, 18, 44, 44, 44])
sheet("Events and releases", ["Week", "Day", "Date", "Type", "Title", "Note"], events, [6, 6, 11, 14, 40, 44])
sheet("KPIs", ["Area", "Metrics", "Review"], [list(k) for k in KPIS], [14, 100, 12])
sheet("Repurposing", ["Source asset", "Becomes"], [list(r) for r in REPURPOSE], [22, 100])
wb.save(f"{HERE}/NEXORA_Content_Calendar.xlsx")
with open(f"{HERE}/NEXORA_Content_Calendar.csv", "w", encoding="utf-8-sig", newline="") as f: w = csv.writer(f); w.writerow(HEAD); w.writerows(rows)
# ------------------------------------------------ PDF
e = html.escape
mix = collections.Counter(c[1] for c in CORE); stg = collections.Counter(c[2] for c in CORE)
CSS = """@font-face{font-family:D;src:url(DMSans.ttf);font-weight:100 1000}@font-face{font-family:P;src:url(PlexAr-Regular.ttf);font-weight:400}@font-face{font-family:P;src:url(PlexAr-Medium.ttf);font-weight:500}@font-face{font-family:P;src:url(PlexAr-Bold.ttf);font-weight:700}
@page{size:A4;margin:0}*{box-sizing:border-box;margin:0}body{font-family:D,sans-serif;color:#101C2C;font-size:9.3px;line-height:1.42;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:794px;padding:34px 44px 26px;page-break-after:always;background:#F5F7FA;min-height:1123px}.dk{background:#101C2C;color:#fff}.top{display:flex;justify-content:space-between;font-size:8.5px;letter-spacing:2px;color:#536273;border-bottom:1px solid #DDE2E8;padding-bottom:8px;margin-bottom:14px}.top b{display:flex;gap:6px;align-items:center;color:#101C2C}.top img{height:14px}
.k{color:#19C6B4;font-weight:700;letter-spacing:2.5px;font-size:8.5px;text-transform:uppercase}h1{font-size:23px;line-height:1.2;margin:2px 0 8px}h2{font-size:13px;margin:12px 0 4px}p{color:#536273;margin-bottom:5px}ul{list-style:none;margin:3px 0 6px}li{position:relative;padding-left:12px;margin-bottom:2px}li:before{content:"";position:absolute;left:0;top:6px;width:4px;height:4px;background:#19C6B4;border-radius:50%}
table{width:100%;border-collapse:collapse;margin:6px 0 8px;font-size:8.8px}th{background:#101C2C;color:#fff;text-align:left;padding:4px 6px}td{padding:4px 6px;border:1px solid #DDE2E8;background:#fff;vertical-align:top}
.card{background:#fff;border:1px solid #DDE2E8;border-left:4px solid #19C6B4;padding:7px 10px;margin:5px 0;break-inside:avoid}.card h3{font-size:11px;margin-bottom:2px}.meta{font-size:8px;color:#536273;margin-bottom:4px}.en{white-space:pre-line}.ar{direction:rtl;text-align:right;font-family:P,sans-serif;white-space:pre-line;font-size:9.8px;line-height:1.55;background:#F5F7FA;padding:4px 7px;margin-top:3px}
.flag{display:inline-block;background:#FFF3D6;color:#8A5A00;font-size:8px;font-weight:700;padding:1px 6px;border-radius:8px}.call{background:#E4F7F4;border-left:4px solid #19C6B4;padding:8px 12px;margin:6px 0}.call p{margin:0;color:#101C2C}
"""
def hd(): return '<div class="top"><b><img src="mark.png">NEXORA</b><span>12-WEEK CONTENT PLAN</span></div>'
def sec(k, t, body): return f'<section class="pg">{hd()}<div class="k">{k}</div><h1>{t}</h1>{body}</section>'
def tbl(head, rws): return "<table><tr>" + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr>" + "".join("<tr>" + "".join(f"<td dir=auto>{e(str(c))}</td>" for c in r) + "</tr>" for r in rws) + "</table>"
def ul(*a): return "<ul>" + "".join(f"<li>{x}</li>" for x in a) + "</ul>"
pdf = []
pdf.append(f'<section class="pg dk" style="min-height:1123px"><img src="mark.png" style="height:56px"><div class="k" style="margin-top:16px">NEXORA · BUSINESS DEVELOPMENT &amp; PERFORMANCE</div><h1 style="font-size:40px;margin-top:230px;line-height:1.1">12-week content plan</h1><p style="color:#B9C6D6;font-size:14px;max-width:480px;margin-top:14px">LinkedIn, Facebook, Instagram and Reels for owner-led businesses in Egypt. English and Arabic copy, ready to schedule.</p><p style="position:absolute;bottom:60px;color:#8FA1B5">Proposed start: {START.strftime("%A %d %B %Y")} (change in build.py) · Working draft</p></section>')
pdf.append(sec("Summary", "How the plan works", f'<div class="call"><p><b>Goal:</b> earn trust and qualified conversations with owner-led businesses in Egypt, recruit 3 pilot partners, and turn them into published, verified results. Sectors: fitness and wellness, food and hospitality, professional services.</p></div>'
 + "<h2>Volume (12 weeks)</h2>" + tbl(["Channel", "Items", "Language", "Notes"], [["LinkedIn", "36 posts (3 per week)", "EN first, AR line", "Founder voice; carousels as PDF documents"], ["Facebook", "36 posts (3 per week)", "AR first", "Owner-facing; groups and shares"], ["Instagram", "36 feed posts or carousels + stories on Sun, Tue, Thu", "AR caption, EN on image", "Saves and DMs are the goal"], ["Reels (IG + FB)", "12 (1 per week)", "AR + EN on-screen", "Fewer videos by design; text motion graphics"], ["Newsletter", "3 (weeks 4, 8, 12)", "EN + AR", ""], ["Workshops", "3 free (weeks 4, 8, 12)", "AR/EN", ""], ["Lead magnets", "4 releases (weeks 3, 4, 5, 7)", "EN + AR", ""]])
 + "<h2>Weekly rhythm (Sunday to Thursday)</h2>" + tbl(["Day", "Posts"], [["Sun", "LinkedIn: idea A · Stories (poll)"], ["Mon", "Facebook: idea A · LinkedIn: idea B"], ["Tue", "Instagram: idea A · Facebook: idea B · Reel (IG + FB) · Stories (question)"], ["Wed", "Instagram: idea B · LinkedIn: idea C"], ["Thu", "Facebook: idea C · Instagram: idea C · Stories (behind the scenes)"]])
 + "<p>Each week has three core ideas (A, B, C). Each idea is published once on every channel on consecutive days, adapted to the channel, so the same effort feeds three audiences.</p>"
 + "<h2>Content mix (36 core ideas)</h2>" + tbl(["Pillar", "Ideas", "Share"], [[k, v, f"{round(100*v/36)}%"] for k, v in mix.most_common()]) + tbl(["Funnel stage", "Ideas", "Share"], [[k, v, f"{round(100*v/36)}%"] for k, v in stg.most_common()])))
pdf.append(sec("Rules and assumptions", "Read before publishing", ul("No client names, results, testimonials or logos unless provided and approved. Items marked <span class='flag'>NEEDS CONFIRMATION</span> contain a placeholder or a claim.", "No guaranteed results; no market-leader claims; hypothetical examples are labelled.", "All <b>[placeholders]</b> must be replaced: dates, links, fees, seat counts, discounts, contact details.", "Keywords for DMs (SCORE, KPI, SOP, DASH, CASE, SPRINT, REVIEW, PILOT, PARTNER, CALL, ASSESS, GYM, CAFE, COST, WORKSHOP, ASSESS) need a person or an auto-reply to answer within 2 working hours.", "Arabic is written as clear Egyptian business Arabic; have a native reader approve it before publishing.", "Weeks 8 and 11 contain pilot and case-study content: publish only if real, approved and verified. Otherwise swap in a Systems or Numbers idea.", "UTM suffix pattern: nexora_[platform]_[format]_wk[#]_[id].") +
 "<h2>Assumptions used</h2>" + ul("Start date " + START.isoformat() + "; Sunday to Thursday working week.", "Entry offer: Business Performance Assessment, fixed fee, about 3 weeks [confirm].", "Pilot programme: 3 places, discount in exchange for permission to publish verified results [confirm].", "A person is available for community management (comments and DMs) every working day.", "Free workshops are online [confirm platform].") + "<h2>Questions I still need answered</h2>" + ul("Who delivers the work, and what is the capacity?", "Which sector and city first?", "Monthly budget (tools, design, any ads)?", "Assessment price level and pilot terms?", "Any real client, testimonial or partner already?", "Is the Gulf in scope for year one?")))
# calendar overview by week
for w0 in range(1, 13, 2):
    body = ""
    for w in range(w0, w0 + 2):
        rs = [r for r in rows if r[0] == w]
        body += f"<h2>Week {w} · {date_of(w,0).strftime('%d %b')} to {date_of(w,4).strftime('%d %b %Y')} · {STORY_THEMES[w]}</h2>" + tbl(["Day", "Platform", "Format", "Pillar", "Title / hook"], [[r[1] + " " + r[2][5:], r[3], r[4], r[5], r[7] + ": " + r[8][:80]] for r in rs])
    pdf.append(sec("Calendar", f"Weeks {w0} and {w0+1}", body))
# core copy
for w in range(1, 13):
    cards = ""
    for i, c in enumerate(CORE[(w - 1) * 3:(w - 1) * 3 + 3]):
        idn, pillar, stage, fmt, title, he, be, ce, ha, ba, ca, vis, kpi, flag = c
        cards += (f'<div class="card"><h3>{e(idn)} · {e(title)}</h3><div class="meta">{e(pillar)} · {e(stage)} · {e(fmt)} · KPI: {e(kpi)} {"<span class=flag>NEEDS CONFIRMATION: " + e(flag) + "</span>" if flag else ""}</div>'
                  f'<div class="en"><b>{e(he)}</b>\n{e(be)}\n<i>CTA: {e(ce)}</i></div><div class="ar"><b>{e(ha)}</b>\n{e(ba)}\nالدعوة: {e(ca)}</div><div class="meta" style="margin-top:4px">Visual: {e(vis)}</div></div>')
    pdf.append(sec(f"Core copy · Week {w}", f"Week {w}: {STORY_THEMES[w]}", cards + f'<div class="meta">Published as: {", ".join(f"{p} (idea {s})" for _, p, s in RHYTHM if s != "R")} + Reel.</div>'))
# reels
rb = ""
for r in REELS: rb += f'<div class="card"><h3>Week {r[0]} · {e(r[1])}</h3><div class="meta">Hook: {e(r[2])} · Sound: {e(r[6])} · Cover: {e(r[7])}</div><div class="en">Beats: {e(r[3])}\nOn-screen EN: {e(r[4])}\nCaption: {e(r[8])}\nCTA: {e(r[10])}</div><div class="ar">النص على الشاشة: {e(r[5])}\nالكابشن: {e(r[9])}</div></div>'
pdf.append(sec("Reels", "12 short videos", "<p>12 to 20 seconds, text-on-screen motion graphics (no on-camera person needed). Silent-friendly with light sound.</p>" + rb))
cb = ""
for k, v in CAROUSELS.items(): cb += f'<div class="card"><h3>{e(k)}</h3>' + "".join(f'<div class="en"><b>{i+1}.</b> {e(a)} <span style="color:#536273">| {e(b)}</span></div>' for i, (a, b) in enumerate(v)) + "</div>"
pdf.append(sec("Carousels", "Slide-by-slide scripts", "<p>One idea per slide; final slide is the CTA. Brand: navy, teal, numbered sections.</p>" + cb))
pdf.append(sec("Lead magnets", "Four free assets", "".join(f'<div class="card"><h3>{e(k)}</h3><div class="en">{e(v)}</div></div>' for k, v in MAGNETS.items()) + "<h2>Business Health Scorecard: the 10 questions</h2>" + tbl(["#", "Area", "Question", "السؤال"], [[i + 1, a, b, c] for i, (a, b, c) in enumerate(SCORE_Q)]) + tbl(["Score", "Band", "Band (AR)", "Advice"], [list(b) for b in SCORE_BANDS])))
pdf.append(sec("Workshops and newsletters", "Events and email", "".join(f'<div class="card"><h3>Workshop {i+1}: {e(w[0])}</h3><div class="meta">For: {e(w[1])} · Exercise: {e(w[3])} · Follow-up: {e(w[4])}</div><div class="en">Agenda: {e(w[2])}</div></div>' for i, w in enumerate(WORKSHOPS)) + tbl(["Issue", "Subject EN", "Subject AR", "Sections"], [[n[0], n[1][0], n[1][1], "; ".join(n[2])] for n in NEWS]) + "<h2>Events and releases</h2>" + tbl(["Week", "Day", "Date", "Type", "Title", "Note"], events)))
pdf.append(sec("Outreach kit", "Messages (EN + AR)", "".join(f'<div class="card"><h3>{e(o[0])}</h3><div class="en">{e(o[1])}</div><div class="ar">{e(o[2])}</div></div>' for o in OUTREACH) + "<p>Rules: personalise the first line, never mass-send, follow up on day 2, 5, 10 and 20 only, stop when asked.</p>"))
pdf.append(sec("Stories, KPIs and reuse", "Stories, measurement, repurposing", "<h2>Stories (Sun, Tue, Thu)</h2>" + tbl(["Day", "Format"], [["Sun", STORY_KIND[0]], ["Tue", STORY_KIND[1]], ["Thu", STORY_KIND[2]]]) + "<p>Theme per week: " + "; ".join(f"W{w} {t}" for w, t in STORY_THEMES.items()) + ".</p><h2>KPI sheet</h2>" + tbl(["Area", "Metrics", "Review"], [list(k) for k in KPIS]) + "<p>Targets are set as hypotheses after four weeks of baseline. Weekly 15-minute review; monthly 30-minute review of mix and what to stop.</p><h2>Repurposing map</h2>" + tbl(["Source", "Becomes"], [list(r) for r in REPURPOSE])))
open(f"{HERE}/plan.html", "w", encoding="utf-8").write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>' + "".join(pdf))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
    pg = b.new_page(); pg.goto(f"file://{HERE}/plan.html"); pg.wait_for_timeout(700)
    pg.pdf(path=f"{HERE}/NEXORA_Content_Plan.pdf", format="A4", print_background=True, margin=dict(top="0", bottom="0", left="0", right="0")); b.close()
print(len(rows), "calendar rows")
