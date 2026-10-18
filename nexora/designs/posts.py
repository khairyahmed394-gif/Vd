"""NEXORA feed designs: 1080x1350 PNG for every core idea (EN + AR); carousels as slides. python3 posts.py"""
import os, re, html, math, random, sys
from playwright.sync_api import sync_playwright
from core import CORE
from assets import CAROUSELS
HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, TEAL, BG, MUTED, LINE = "#101C2C", "#19C6B4", "#F5F7FA", "#536273", "#DDE2E8"
e = html.escape
CSS = f"""@font-face{{font-family:M;src:url(fonts/Manrope.ttf);font-weight:200 800}}@font-face{{font-family:I;src:url(fonts/Inter.ttf);font-weight:100 900}}
@font-face{{font-family:P;src:url(fonts/PlexAr-Regular.ttf);font-weight:400}}@font-face{{font-family:P;src:url(fonts/PlexAr-Medium.ttf);font-weight:500}}@font-face{{font-family:P;src:url(fonts/PlexAr-Bold.ttf);font-weight:700}}
*{{margin:0;box-sizing:border-box}}html{{overflow:hidden}}body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:M,sans-serif}}
body.ar{{direction:rtl;font-family:P,sans-serif}}body.ar .en{{font-family:M}}.dark{{background:{NAVY};color:#fff}}.light{{background:{BG};color:{NAVY}}}
.ab{{position:absolute}}.top{{position:absolute;top:58px;inset-inline:70px;display:flex;justify-content:space-between;align-items:center}}.top .lg{{display:flex;align-items:center;gap:12px;font-weight:700;letter-spacing:5px;font-size:22px;direction:ltr}}.top img{{height:40px}}
.kick{{color:{TEAL};font-weight:700;letter-spacing:5px;font-size:21px;text-transform:uppercase}}body.ar .kick{{letter-spacing:0;font-size:25px}}
h1{{font-weight:800;line-height:1.14;letter-spacing:-1px}}body.ar h1{{font-weight:700;line-height:1.35;letter-spacing:0}}
.sub{{font-size:34px;line-height:1.55;font-weight:500}}.dark .sub{{color:#C7D3E0}}.light .sub{{color:{MUTED}}}body.ar .sub{{font-size:35px;line-height:1.7}}
.cta{{position:absolute;bottom:128px;inset-inline:70px;height:96px;border-radius:48px;background:{TEAL};color:{NAVY};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:30px;padding:0 40px;text-align:center}}body.ar .cta{{font-weight:700;font-size:32px}}
.foot{{position:absolute;bottom:52px;inset-inline:70px;display:flex;justify-content:space-between;font-size:19px;letter-spacing:4px;color:#8394A8;direction:ltr}}body.ar .foot{{letter-spacing:0;direction:rtl;font-size:22px}}
.bar{{width:90px;height:7px;background:{TEAL};margin:28px 0}}.item{{display:flex;gap:24px;align-items:flex-start;background:#fff;border:1px solid {LINE};border-inline-start:8px solid {TEAL};padding:20px 26px;margin-bottom:16px;font-size:30px;line-height:1.5;font-weight:600;color:{NAVY}}}.item b{{color:{TEAL};font-size:34px;min-width:48px}}
.dark .item{{background:#17273A;border-color:#2A4358;border-inline-start-color:{TEAL};color:#fff}}
"""
KICK = {"Diagnose": ("DIAGNOSE", "تشخيص"), "Systems": ("SYSTEMS", "أنظمة"), "Numbers": ("NUMBERS", "أرقام"), "People": ("PEOPLE", "الأفراد"), "Proof": ("PROOF", "إثبات"), "Brand": ("NEXORA", "NEXORA"), "Marketing": ("MARKETING", "تسويق"), "Sector": ("SECTORS", "قطاعات"), "Objection": ("STRAIGHT TALK", "كلام صريح"), "Sales": ("SALES", "المبيعات")}
def nodes(seed, dark=True, w=1080, h=1350, mirror=False):
    rnd = random.Random(seed); n = 6; cx0 = w * .62; pts = [(cx0 + rnd.uniform(-190, 290), h * .66 + rnd.uniform(-190, 180)) for _ in range(n)]
    if mirror: pts = [(w - x, y) for x, y in pts]
    ln = "".join(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}" stroke="{TEAL}" stroke-opacity=".30" stroke-width="2"/>' for i, j in [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (2, 4)])
    return f'<svg class="ab" style="left:0;top:0" width="{w}" height="{h}">{ln}' + "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{TEAL}"/>' for x, y in pts) + "</svg>"
def short(t, n):
    t = t.strip().replace("\n", " ")
    ss = re.split(r"(?<=[.!?؟])\s+", t); out = ""
    for s in ss:
        if len(out) + len(s) <= n: out = (out + " " + s).strip()
        else: break
    return out or t[:n].rsplit(" ", 1)[0] + "…"
def hsize(t, ar):
    n = len(t); return (86 if n <= 38 else 74 if n <= 58 else 64 if n <= 80 else 56) * (0.86 if ar else 1)
def shell(body, dark, ar, idx, label):
    k = ""
    return f'<body class="{"ar " if ar else ""}{"dark" if dark else "light"}"><div class="top"><div class="lg"><img src="img/mark.png"><span style="color:{"#fff" if dark else NAVY}">NEXORA</span></div><div class="kick">{label}</div></div>{body}<div class="foot"><span>{idx}</span><span>{"ابنِ أفضل. انمُ بذكاء." if ar else "BUILD BETTER. GROW SMARTER."}</span></div></body>'
def statement(c, ar, dark, n):
    idn, pillar, stage, fmt, title, he, be, ce, ha, ba, ca, vis, kpi, flag = c
    hook, body, cta = (ha, ba, ca) if ar else (he, be, ce); k = KICK.get(pillar, KICK["Brand"])[1 if ar else 0]
    first = body.split("\n\n")[0] if "\n\n" in body else body
    sub = short(first, 170)
    return shell(nodes(idn, dark, mirror=ar) + f'<div class="ab" style="inset-inline:70px;top:250px;width:760px"><h1 style="font-size:{hsize(hook, ar)}px">{e(hook)}</h1><div class="bar"></div><div class="sub">{e(sub)}</div></div><div class="cta">{e(cta)}</div>', dark, ar, f"{n:02d}", k)
def listcard(c, ar, items, n):
    idn, pillar, stage, fmt, title, he, be, ce, ha, ba, ca, vis, kpi, flag = c
    hook, cta = (ha, ca) if ar else (he, ce); k = KICK.get(pillar, KICK["Brand"])[1 if ar else 0]
    its = "".join(f'<div class="item"><b>{i+1:02d}</b><span>{e(t)}</span></div>' for i, t in enumerate(items[:6]))
    return shell(f'<div class="ab" style="inset-inline:70px;top:210px"><h1 style="font-size:{hsize(hook, ar)*0.78}px">{e(hook)}</h1><div class="bar" style="margin:22px 0 30px"></div>{its}</div><div class="cta">{e(cta)}</div>', False, ar, f"{n:02d}", k)
def offer(c, ar, n):
    idn, pillar, stage, fmt, title, he, be, ce, ha, ba, ca, vis, kpi, flag = c
    hook, body, cta = (ha, ba, ca) if ar else (he, be, ce); k = KICK.get(pillar, KICK["Brand"])[1 if ar else 0]
    when = "[التاريخ · الوقت · المنصة]" if ar else "[Date · time · platform]"
    box = f'<div class="ab" style="inset-inline:70px;top:760px;height:130px;border:3px dashed {TEAL};border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:34px;color:{TEAL};font-weight:700">{when}</div>' if idn in ("4C", "8C") else ""
    sub = short(body.split("\n\n")[0], 150)
    return shell(nodes(idn, True, mirror=ar) + f'<div class="ab" style="inset-inline:70px;top:250px;width:790px"><h1 style="font-size:{hsize(hook, ar)}px">{e(hook)}</h1><div class="bar"></div><div class="sub">{e(sub)}</div></div>{box}<div class="cta">{e(cta)}</div>', True, ar, f"{n:02d}", k)
def casecard(c, ar, n):
    idn = c[0]; G = (["قطاع العميل", "التحدي", "الوضع الأولي", "نطاق العمل", "الحل", "المخرجات", "منهج القياس", "النتائج الموثقة", "شهادة العميل"] if ar else ["Client industry", "Challenge", "Initial situation", "Scope", "Solution", "Deliverables", "Measurement", "Verified outcomes", "Client quote"])
    cells = "".join(f'<div style="width:300px;height:150px;background:{"#17273A" if i==7 else "#fff"};color:{"#fff" if i==7 else NAVY};border:1px solid {LINE};padding:20px;font-size:25px;font-weight:700"><div style="color:{TEAL};font-size:22px">{i+1:02d}</div>{e(g)}</div>' for i, g in enumerate(G))
    return shell(f'<div class="ab" style="inset-inline:70px;top:210px"><h1 style="font-size:{64 if not ar else 56}px">{"دراسة حالة (قالب)" if ar else "Case study (template)"}</h1><div class="bar"></div><div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:10px;width:960px">{cells}</div><div style="margin-top:26px;color:{TEAL};font-weight:700;font-size:28px">{"استخدمها فقط ببيانات موثقة وموافقة مكتوبة" if ar else "Use only with verified data and written approval"}</div></div>', False, ar, f"{n:02d}", "PROOF" if not ar else "إثبات")
def cslide(kind, text, i, total, ar, c):
    dark = kind != "mid"; k = KICK.get(c[1], KICK["Brand"])[1 if ar else 0]; num = f"{i+1}/{total}"
    if kind == "cover": body = nodes(c[0], True, mirror=ar) + f'<div class="ab" style="inset-inline:70px;top:330px;width:800px"><h1 style="font-size:{hsize(text, ar)*1.05}px">{e(text)}</h1><div class="bar"></div><div class="sub">{"اسحب لقراءة المزيد" if ar else "Swipe to read"}</div></div>'
    elif kind == "cta": body = f'<div class="ab" style="inset-inline:70px;top:380px;width:800px"><h1 style="font-size:{hsize(text, ar)}px">{e(text)}</h1><div class="bar"></div></div>'
    else:
        m = re.match(r"^([0-9٠-٩]+)[.\s:)-]+\s*(.*)$", text); n_, tx = (m.group(1), m.group(2)) if m else (f"{i:02d}", text)
        body = f'<div class="ab" style="inset-inline:70px;top:250px"><div style="color:{TEAL};font-weight:800;font-size:150px;line-height:1">{e(n_)}</div><h1 style="font-size:{hsize(tx, ar)*0.9}px;margin-top:20px">{e(tx)}</h1></div>'
    return shell(body, dark, ar, num, k)
def strip(t): return re.sub(r"^(Cover|CTA|الغلاف|ابعت|CTA):?\s*", "", t) if t.startswith(("Cover", "CTA", "الغلاف")) else t
SPECIAL = {"2B": "list", "6B": "stmt", "4C": "offer", "8C": "offer", "3C": "offer", "7C": "offer", "10C": "offer", "11C": "offer", "12B": "offer", "11B": "stmt", "12C": "offer", "2C": "offer", "11A": "case"}
CAR = {"2A": "2A Six stages", "3A": "3A Follow-up leaks", "4A": "4A SOP", "5A": "5A KPI review", "6C": "6C Assessment", "12A": "12A Lessons"}
def numbered(body):
    return [re.sub(r"^[0-9٠-٩]+[.\s]+", "", l).strip() for l in body.split("\n") if re.match(r"^[0-9٠-٩]+[.\s]", l)]
def build(only=None):
    out = []
    for n, c in enumerate(CORE, 1):
        idn = c[0]
        for lang in ("en", "ar"):
            ar = lang == "ar"; name = f"wk{int(re.match(r'\d+', idn).group()):02d}_{idn}_{re.sub(r'[^a-z0-9]+', '-', c[4].lower())[:32] if not ar else 'ar'}".strip("-")
            if idn in CAR:
                sl = CAROUSELS[CAR[idn]]; texts = [strip(s[1 if ar else 0]) for s in sl]; tot = len(texts)
                for i, t in enumerate(texts):
                    kind = "cover" if i == 0 else "cta" if i == tot - 1 else "mid"
                    out.append((f"{lang}/wk{int(re.match(r'\d+', idn).group()):02d}_{idn}/slide{i+1:02d}", cslide(kind, t, i, tot, ar, c)))
            elif c[3] == "Carousel" and numbered(c[9 if ar else 6]) and len(numbered(c[9 if ar else 6])) >= 4:
                its = numbered(c[9 if ar else 6]); tot = len(its) + 2; texts = [c[8 if ar else 5]] + [f"{j+1}. {t}" for j, t in enumerate(its)] + [c[10 if ar else 7]]
                for i, t in enumerate(texts):
                    kind = "cover" if i == 0 else "cta" if i == tot - 1 else "mid"
                    out.append((f"{lang}/wk{int(re.match(r'\d+', idn).group()):02d}_{idn}/slide{i+1:02d}", cslide(kind, t, i, tot, ar, c)))
            else:
                sp = SPECIAL.get(idn)
                if sp == "list": out.append((f"{lang}/wk{int(re.match(r'\d+', idn).group()):02d}_{idn}", listcard(c, ar, numbered(c[9 if ar else 6]), n)))
                elif sp == "offer": out.append((f"{lang}/wk{int(re.match(r'\d+', idn).group()):02d}_{idn}", offer(c, ar, n)))
                elif sp == "case": out.append((f"{lang}/wk{int(re.match(r'\d+', idn).group()):02d}_{idn}", casecard(c, ar, n)))
                else: out.append((f"{lang}/wk{int(re.match(r'\d+', idn).group()):02d}_{idn}", statement(c, ar, n % 2 == 1, n)))
    return out
def main():
    items = build(); print(len(items), "images")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for path, body in items:
            f = f"{HERE}/out/{path}.png"; os.makedirs(os.path.dirname(f), exist_ok=True); h = f"{HERE}/_t.html"
            open(h, "w", encoding="utf-8").write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{body}')
            pg = b.new_page(viewport={"width": 1080, "height": 1350}); pg.goto("file://" + h); pg.wait_for_timeout(120); pg.screenshot(path=f); pg.close()
        b.close()
    os.remove(f"{HERE}/_t.html")
main()
