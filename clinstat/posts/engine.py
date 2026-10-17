"""ClinStat static-post engine v2: 1080x1350 (4:5), Arabic RTL or English LTR, brand navy / green / gold / sand, IBM Plex Sans Arabic."""
import json, os, re, html, math
HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, GREEN, GOLD, SAND = "#0B1F33", "#103D2E", "#A8854E", "#F7F4ED"
LG = json.load(open(os.path.join(HERE, "logo_vec.json")))
LANG = {"v": "ar"}
def rtl(): return LANG["v"] == "ar"
def AL(): return "right" if rtl() else "left"          # start-side alignment for LTR islands
LAT = re.compile(r"\(?[A-Za-z0-9~][A-Za-z0-9 .,<>=/+()%~\-'’·–²]*[A-Za-z0-9)%²]|\(?[A-Za-z0-9~]")
def t(s):
    """escape and isolate Latin runs in RTL text (no-op wrapper in English)"""
    s = str(s)
    if not rtl(): return html.escape(s, quote=False)
    out, pos = [], 0
    for m in LAT.finditer(s):
        out.append(html.escape(s[pos:m.start()], quote=False)); out.append(f'<bdi dir="ltr">{html.escape(m.group(0), quote=False)}</bdi>'); pos = m.end()
    out.append(html.escape(s[pos:], quote=False)); return "".join(out)
def logo(light=False, w=250):
    x0, x1, y0, y1 = LG["mark"]["x0"], LG["word"]["x1"], LG["mark"]["y0"], LG["mark"]["y1"]
    def col(c):
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        return SAND if light and (0.299 * r + 0.587 * g + 0.114 * b) < 90 else c
    parts = [f'<circle cx="{d["cx"]}" cy="{d["cy"]}" r="{d["r"]}" fill="{col(d["color"])}"/>' for d in LG["dots"]]
    parts += [f'<path d="{c["d"]}" fill="{col(c["color"])}" fill-rule="evenodd"/>' for c in LG["chev"]]
    parts.append(f'<path d="{LG["divider"]["d"]}" fill="{col(LG["divider"]["color"])}"/>')
    for k in ("clin", "stat", "res"): parts += [f'<path d="{l["d"]}" fill="{col(l["color"])}" fill-rule="evenodd"/>' for l in LG[k]]
    h = w * (y1 - y0) / (x1 - x0)
    return f'<svg class="logo" dir="ltr" width="{w}" height="{h:.0f}" viewBox="{x0} {y0} {x1-x0} {y1-y0}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'
def chevrons(color, op):
    paths = "".join(f'<path d="{c["d"]}" fill="{color}" fill-rule="evenodd"/>' for c in LG["chev"])
    return f'<svg class="wm" dir="ltr" viewBox="{LG["mark"]["x0"]} {LG["mark"]["y0"]+70} {LG["mark"]["x1"]-LG["mark"]["x0"]} {LG["mark"]["y1"]-LG["mark"]["y0"]-70}" style="opacity:{op}" xmlns="http://www.w3.org/2000/svg">{paths}</svg>'
ICON_SAVE = '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-6-4-6 4z"/></svg>'
ICON_SEND = '<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 3 10 14"/><path d="M21 3l-7 18-4-7-7-4z"/></svg>'
ICON_CHECK = f'<svg viewBox="0 0 24 24" width="46" height="46" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 6.5"/></svg>'
CSS = f"""
@font-face{{font-family:PX;src:url(fonts/PlexAr-Regular.ttf);font-weight:400}}
@font-face{{font-family:PX;src:url(fonts/PlexAr-Medium.ttf);font-weight:500}}
@font-face{{font-family:PX;src:url(fonts/PlexAr-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:PX;src:url(fonts/PlexAr-Bold.ttf);font-weight:700}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:{SAND}}}
body{{font-family:PX,sans-serif;color:{NAVY}}}
.card{{position:relative;width:1080px;height:1350px;padding:84px 88px 0;overflow:hidden}}
.card.sand{{background:{SAND};color:{NAVY}}} .card.navy{{background:{NAVY};color:{SAND}}} .card.green{{background:{GREEN};color:{SAND}}}
.wm{{position:absolute;left:-150px;top:340px;width:760px;pointer-events:none}}
.head{{display:flex;justify-content:space-between;align-items:center;height:60px}}
.tag{{font-size:27px;font-weight:600;letter-spacing:0;color:{GOLD};border:2px solid {GOLD};border-radius:40px;padding:8px 26px 10px}}
.cnt{{font-size:28px;font-weight:500;opacity:.7}}
.foot{{position:absolute;left:88px;right:88px;bottom:70px;display:flex;justify-content:space-between;align-items:center}}
.foot .cta{{font-size:28px;font-weight:500;opacity:.78}}
.rule{{width:132px;height:7px;background:{GOLD};border-radius:4px}}
h1,h2{{font-weight:700;line-height:1.22}}
bdi{{unicode-bidi:isolate;white-space:nowrap}}
.rows{{position:absolute;right:88px;left:88px}}
.row{{display:flex;gap:34px;align-items:flex-start;padding:40px 0;border-top:2px solid rgba(11,31,51,.12)}}
.row:first-child{{border-top:0}}
.num{{flex:0 0 100px;height:100px;border-radius:50%;background:{NAVY};color:{SAND};font-size:44px;font-weight:700;display:flex;align-items:center;justify-content:center;padding-top:4px}}
.num.gold{{background:{GOLD};color:{NAVY}}}
.row h3{{font-size:45px;font-weight:600;line-height:1.36}}
.row p{{font-size:33px;font-weight:400;line-height:1.45;margin-top:12px;color:#4A5A66}}
.navy .row,.green .row{{border-color:rgba(247,244,237,.16)}}
.navy .row p,.green .row p{{color:rgba(247,244,237,.74)}}
.pill{{display:inline-flex;align-items:center;gap:16px;border-radius:60px;padding:22px 40px 24px;font-size:36px;font-weight:600}}
.trow{{display:flex;gap:30px;align-items:center;padding:24px 0;border-top:2px solid rgba(11,31,51,.12)}}
.trow:first-child{{border-top:0}}
.tname{{flex:0 0 330px;font-size:40px;font-weight:700;color:{GREEN};direction:ltr;text-align:start;unicode-bidi:isolate}}
.tdesc{{font-size:35px;font-weight:500;line-height:1.38}}
"""
def shell(cls, body, wm=None):
    d = "rtl" if rtl() else "ltr"
    return f'<!doctype html><html lang="{LANG["v"]}" dir="{d}"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="card {cls}">{wm or ""}{body}</div></body></html>'
def head(tag, cnt=None): return f'<div class="head"><span class="tag">{t(tag)}</span><span class="cnt" dir="ltr">{cnt or ""}</span></div>'
def foot(cta, light=False): return f'<div class="foot"><span class="cta">{t(cta)}</span>{logo(light)}</div>'
def title_block(title, size=70, mt=44, hook=None):
    h = f'<p style="font-size:35px;line-height:1.45;margin-top:22px;font-weight:400;opacity:.85">{t(hook)}</p>' if hook else ""
    return f'<div style="margin-top:{mt}px"><h2 style="font-size:{size}px;line-height:1.25">{t(title)}</h2><div class="rule" style="margin-top:24px"></div>{h}</div>'
# ------------------------------------------------------------------ templates
def tpl_cover(c):
    return shell("navy", f"""{head(c["tag"], c["cnt"])}
<div style="position:absolute;right:88px;left:88px;top:250px">
  <div style="font-size:400px;font-weight:700;line-height:.9;color:{GOLD};letter-spacing:-6px;text-align:{AL() if False else ('right' if rtl() else 'left')}" dir="ltr">{c["big"]}</div>
  <h1 style="font-size:84px;margin-top:20px">{t(c["title"])}</h1><div class="rule" style="margin:36px 0 34px"></div>
  <p style="font-size:42px;line-height:1.45;font-weight:400;opacity:.88;max-width:860px">{t(c["hook"])}</p></div>
{foot(c["foot"], True)}""", chevrons(SAND, .05))
def tpl_points(c):
    rows = "".join(f'<div class="row"><div class="num{" gold" if c.get("gold") else ""}">{n}</div><div><h3>{t(h)}</h3>{f"<p>{t(p)}</p>" if p else ""}</div></div>' for n, h, p in c["rows"])
    return shell(c.get("bg", "sand"), f"""{head(c["tag"], c.get("cnt"))}
<div style="margin-top:56px"><h2 style="font-size:78px">{t(c["title"])}</h2><div class="rule" style="margin-top:26px"></div></div>
<div class="rows" style="top:340px;bottom:178px;display:flex;flex-direction:column;justify-content:center">{rows}</div>
{foot(c["foot"])}""")
def tpl_closing(c):
    return shell("green", f"""{head(c["tag"], c.get("cnt"))}
<div style="position:absolute;right:88px;left:88px;top:250px">
  <h1 style="font-size:104px">{t(c["title"])}</h1><div class="rule" style="margin:36px 0 40px"></div>
  <p style="font-size:44px;line-height:1.5;opacity:.92;max-width:860px">{t(c["body"])}</p>
  <div style="display:flex;gap:26px;margin-top:70px"><span class="pill" style="background:{GOLD};color:{NAVY}">{ICON_SAVE}<span>{t(c["btn1"])}</span></span><span class="pill" style="border:3px solid {SAND}">{ICON_SEND}<span>{t(c["btn2"])}</span></span></div></div>
<div style="position:absolute;right:88px;left:88px;bottom:178px;font-size:30px;opacity:.7;line-height:1.5"><bdi dir="ltr" style="unicode-bidi:isolate">{html.escape(c["note"])}</bdi></div>
{foot(c.get("foot",""), True)}""", chevrons(SAND, .05))
def tpl_list(c):
    rows = "".join(f'<div class="row" style="padding:{c.get("pad",19)}px 0"><div class="num gold" style="flex:0 0 74px;height:74px;font-size:34px">{n}</div><div><h3 style="font-size:{c.get("fs",36)}px;line-height:1.34">{t(h)}</h3></div></div>' for n, h in c["rows"])
    return shell("sand", f"""{head(c["tag"], None)}{title_block(c["title"], 70)}
<div class="rows" style="top:{c.get("top", 436)}px">{rows}</div>
<div style="position:absolute;right:88px;left:88px;bottom:176px;background:{GREEN};color:{SAND};border-radius:20px;padding:26px 36px 30px;font-size:33px;line-height:1.45;font-weight:500">{t(c["band"])}</div>
{foot(c["foot"])}""")
def tpl_quote(c):
    rows = "".join(f'<div class="row" style="padding:34px 0"><div class="num gold" style="flex-basis:84px;height:84px;font-size:38px">{n}</div><div><h3 style="font-size:54px;font-weight:700">{t(h)}</h3></div></div>' for n, h in c["rows"])
    return shell("green", f"""{head(c["tag"], None)}
<div style="position:absolute;inset-inline-start:88px;top:200px;font-size:300px;line-height:1;color:{GOLD};opacity:.9;font-weight:700" dir="ltr">{'”' if rtl() else '“'}</div>
<div style="position:absolute;right:88px;left:88px;top:430px"><h1 style="font-size:84px;line-height:1.25">{t(c["title"])}</h1><div class="rule" style="margin-top:28px"></div></div>
<div class="rows" style="top:706px">{rows}</div>{foot(c["foot"], True)}""", chevrons(SAND, .05))
def tpl_case(c):
    arrow = "←" if rtl() else "→"
    return shell("navy", f"""{head(c["tag"], None)}
<div style="position:absolute;right:88px;left:88px;top:320px">
  <div style="display:flex;align-items:flex-end;gap:36px;justify-content:space-between">
    <div><div dir="ltr" style="font-size:300px;font-weight:700;line-height:.95;color:rgba(247,244,237,.55);text-align:start">{c["n1"]}</div><div style="font-size:44px;font-weight:600;opacity:.8;margin-top:6px">{t(c["l1"])}</div></div>
    <div style="font-size:120px;color:{GOLD};padding-bottom:70px" dir="ltr">{arrow}</div>
    <div><div dir="ltr" style="font-size:300px;font-weight:700;line-height:.95;color:{GOLD};text-align:start">{c["n2"]}</div><div style="font-size:44px;font-weight:600;margin-top:6px">{t(c["l2"])}</div></div></div>
  <div class="rule" style="margin:70px 0 40px"></div><p style="font-size:56px;line-height:1.38;font-weight:600">{t(c["body"])}</p></div>
{foot(c["foot"], True)}""", chevrons(SAND, .05))
def tpl_stats(c):
    al = "right" if rtl() else "left"
    blocks = "".join(f'<div style="padding:46px 0;border-top:2px solid rgba(247,244,237,.16)"><div dir="ltr" style="text-align:{al};font-size:230px;font-weight:700;line-height:1;color:{GOLD}">{n}</div><div style="font-size:54px;font-weight:600;line-height:1.3;margin-top:8px">{t(l)}</div></div>' for n, l in c["stats"])
    return shell("navy", f"""{head(c["tag"], None)}
<div style="position:absolute;right:88px;left:88px;top:208px"><h2 style="font-size:70px">{t(c["title"])}</h2><div class="rule" style="margin-top:24px;margin-bottom:34px"></div>{blocks}</div>
{foot(c["foot"], True)}""", chevrons(SAND, .04))
def tpl_table(c):
    rows = "".join(f'<div class="trow"><div class="tname">{html.escape(n)}</div><div class="tdesc">{t(d)}</div></div>' for n, d in c["rows"])
    return shell("sand", f"""{head(c["tag"], None)}{title_block(c["title"], 68, 40, c.get("hook"))}
<div class="rows" style="top:{c.get("top", 500)}px;bottom:170px;display:flex;flex-direction:column;justify-content:center">{rows}</div>{foot(c["foot"])}""")
def tpl_promo(c):
    bl = "".join(f'<div style="display:flex;gap:22px;align-items:center;padding:14px 0"><span style="flex:0 0 46px">{ICON_CHECK}</span><span style="font-size:41px;font-weight:600;line-height:1.35">{t(b)}</span></div>' for b in c["bullets"])
    return shell("green", f"""{head(c["tag"], None)}
<div style="position:absolute;right:88px;left:88px;top:230px"><h1 dir="ltr" style="font-size:86px;line-height:1.14;text-align:start">{html.escape(c["title"])}</h1><div class="rule" style="margin:34px 0 30px"></div>
  <p style="font-size:42px;line-height:1.45;opacity:.92">{t(c["hook"])}</p><div style="margin-top:36px">{bl}</div>
  <div style="margin-top:48px"><span class="pill" style="background:{GOLD};color:{NAVY};font-size:40px">{ICON_SAVE}<span>{t(c["btn"])}</span></span></div></div>
{foot(c["foot"], True)}""", chevrons(SAND, .05))
def tpl_grid(c):
    cells = "".join(f'<div style="display:flex;gap:22px;align-items:center;padding:6px 0"><div class="num gold" style="flex:0 0 70px;height:70px;font-size:32px">{n}</div><div style="font-size:33px;font-weight:600;line-height:1.35">{t(tx)}</div></div>' for n, tx in c["items"])
    return shell("sand", f"""{head(c["tag"], None)}{title_block(c["title"], 66, 40)}
<div style="position:absolute;right:88px;left:88px;top:360px;bottom:190px;display:grid;grid-auto-flow:column;grid-template-rows:repeat(5,1fr);grid-template-columns:1fr 1fr;column-gap:36px">{cells}</div>{foot(c["foot"])}""")
def tpl_forest(c):
    X = lambda v: 480 + math.log(v) * 120
    studies = [("Study A", 0.60, 0.35, 1.05, 26), ("Study B", 0.85, 0.60, 1.20, 46), ("Study C", 0.55, 0.30, 1.00, 20), ("Study D", 0.75, 0.55, 1.02, 40)]
    sv = []; y = 60
    for nme, e, lo, hi, s in studies:
        sv.append(f'<text x="60" y="{y+9}" font-size="32" font-weight="500" fill="{NAVY}">{nme}</text><line x1="{X(lo):.0f}" x2="{X(hi):.0f}" y1="{y}" y2="{y}" stroke="{NAVY}" stroke-width="5"/><rect x="{X(e)-s/2:.0f}" y="{y-s/2:.0f}" width="{s}" height="{s}" fill="{GREEN}"/><text x="720" y="{y+9}" font-size="30" fill="{NAVY}" opacity=".8">{e:.2f} [{lo:.2f}, {hi:.2f}]</text>'); y += 68
    pv = (0.72, 0.58, 0.90); py = y + 14
    dia = f'<polygon points="{X(pv[1]):.0f},{py} {X(pv[0]):.0f},{py-20} {X(pv[2]):.0f},{py} {X(pv[0]):.0f},{py+20}" fill="{GOLD}"/><text x="60" y="{py+9}" font-size="32" font-weight="700" fill="{NAVY}">Pooled</text><text x="720" y="{py+9}" font-size="30" font-weight="700" fill="{NAVY}">{pv[0]:.2f} [{pv[1]:.2f}, {pv[2]:.2f}]</text>'
    axy = py + 52
    ticks = "".join(f'<line x1="{X(v):.0f}" x2="{X(v):.0f}" y1="{axy}" y2="{axy+10}" stroke="{NAVY}" stroke-width="3"/><text x="{X(v):.0f}" y="{axy+40}" text-anchor="middle" font-size="25" fill="{NAVY}" opacity=".8">{v}</text>' for v in (0.2, 0.5, 1, 2, 5))
    svg = f'<svg dir="ltr" width="1080" height="{axy+60}" viewBox="0 0 1080 {axy+60}" xmlns="http://www.w3.org/2000/svg"><style>text{{font-family:PX,sans-serif}}</style><line x1="{X(1):.0f}" x2="{X(1):.0f}" y1="14" y2="{axy}" stroke="{NAVY}" stroke-width="4" stroke-dasharray="3 0"/>{"".join(sv)}{dia}<line x1="{X(0.2):.0f}" x2="{X(5):.0f}" y1="{axy}" y2="{axy}" stroke="{NAVY}" stroke-width="3"/>{ticks}</svg>'
    ic = lambda inner: f'<svg width="56" height="44" viewBox="0 0 56 44" dir="ltr">{inner}</svg>'
    icons = [ic(f'<rect x="20" y="8" width="28" height="28" fill="{GREEN}"/>'), ic(f'<line x1="2" x2="54" y1="22" y2="22" stroke="{NAVY}" stroke-width="5"/><rect x="21" y="14" width="14" height="16" fill="{GREEN}"/>'),
             ic(f'<rect x="6" y="4" width="36" height="36" fill="{GREEN}"/><rect x="42" y="14" width="10" height="10" fill="{GREEN}" opacity=".5"/>'), ic(f'<line x1="28" x2="28" y1="0" y2="44" stroke="{NAVY}" stroke-width="5"/>'), ic(f'<polygon points="2,22 28,6 54,22 28,38" fill="{GOLD}"/>')]
    leg = "".join(f'<div style="display:flex;gap:24px;align-items:center;padding:7px 0"><span style="flex:0 0 56px">{icons[i]}</span><span style="font-size:34px;font-weight:500;line-height:1.3">{t(tx)}</span></div>' for i, tx in enumerate(c["legend"]))
    return shell("sand", f"""{head(c["tag"], None)}{title_block(c["title"], 66, 36)}
<div style="position:absolute;left:0;right:0;top:318px;direction:ltr">{svg}</div>
<div style="position:absolute;left:88px;right:88px;top:{318+axy+66}px">{leg}</div>
<div style="position:absolute;left:88px;right:88px;bottom:140px;font-size:26px;opacity:.6">{t(c["note"])}</div>{foot(c["foot"])}""")
TPL = dict(cover=tpl_cover, points=tpl_points, closing=tpl_closing, list=tpl_list, quote=tpl_quote, case=tpl_case, stats=tpl_stats, table=tpl_table, promo=tpl_promo, grid=tpl_grid, forest=tpl_forest)
