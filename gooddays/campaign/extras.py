"""Photo-free extra designs (AR + EN): hours poster, changing-menu poster, 3-slide Reset/Recharge/Repeat carousel, no-membership card, 5 highlight covers. python3 extras.py"""
import os, html
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = f"{HERE}/posts/fonts"; IMG = f"{HERE}/posts/img"; RED = "#B30504"
def css(ar, w, h, bg, fg="#fff"): return f"""@font-face{{font-family:M;src:url(file://{FONTS}/Montserrat.ttf);font-weight:100 900}}@font-face{{font-family:P;src:url(file://{FONTS}/PlexAr-Bold.ttf);font-weight:700}}
*{{margin:0;box-sizing:border-box}}html{{overflow:hidden}}body{{width:{w}px;height:{h}px;position:relative;overflow:hidden;direction:{'rtl' if ar else 'ltr'};font-family:{'P' if ar else 'M'},sans-serif;color:{fg};background:{bg}}}
h1{{font-weight:{700 if ar else 800};text-transform:uppercase;line-height:{1.25 if ar else 1.05}}}.logo{{position:absolute;left:50%;transform:translateX(-50%);width:230px;bottom:56px}}
.abs{{position:absolute}}"""
S = lambda body, c="#fff", w=3: f'stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
ICON = {
 "cup": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M28 30h44l-6 56H34z" {S(0,c,4)}/><path d="M24 30h52" {S(0,c,4)}/><path d="M56 30l8-22" {S(0,c,4)}/><path d="M36 52h28" {S(0,c,3)}/></svg>',
 "clock": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><circle cx="50" cy="50" r="38" {S(0,c,4)}/><path d="M50 26v26l16 10" {S(0,c,4)}/></svg>',
 "leaf": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M20 80C20 40 45 20 82 20c0 38-22 62-58 60z" {S(0,c,4)}/><path d="M20 80C38 58 52 46 68 36" {S(0,c,4)}/></svg>',
 "bolt": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M56 8L26 56h22l-6 36 32-50H52z" {S(0,c,4)}/></svg>',
 "loop": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M22 46a30 30 0 0 1 52-14" {S(0,c,4)}/><path d="M76 14v20H56" {S(0,c,4)}/><path d="M78 54a30 30 0 0 1-52 14" {S(0,c,4)}/><path d="M24 86V66h20" {S(0,c,4)}/></svg>',
 "menu": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M22 28h56M22 50h56M22 72h36" {S(0,c,5)}/></svg>',
 "play": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><rect x="14" y="22" width="72" height="56" rx="10" {S(0,c,4)}/><path d="M42 36l24 14-24 14z" {S(0,c,4)}/></svg>',
 "pin": lambda c="#fff": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M50 90S22 60 22 40a28 28 0 0 1 56 0c0 20-28 50-28 50z" {S(0,c,4)}/><circle cx="50" cy="40" r="10" {S(0,c,4)}/></svg>',
}
def hours(l):
    ar = l == "ar"; big = "١٠ ص — ١٢ م" if ar else "10 AM — 12 AM"
    return css(ar, 1080, 1350, f"radial-gradient(circle at 20% 10%,#D01212,{RED} 50%,#6A0100)"), f'''<div class="abs" style="left:440px;top:120px;width:200px;height:200px">{ICON["clock"]()}</div>
<div class="abs" style="left:40px;right:40px;top:400px;text-align:center"><h1 style="font-size:{170 if ar else 120}px;white-space:nowrap">{html.escape(big)}</h1><div style="margin-top:50px;font-size:{60 if ar else 46}px;font-weight:700">{"مواعيد جود دايز" if ar else "GOOD DAYS OPEN HOURS"}</div><div style="margin-top:34px;font-size:{40 if ar else 32}px;opacity:.9">{"مفتوح لكل الناس. مش لازم تكون عضو." if ar else "Open to everyone. No membership needed."}</div></div><img class="logo" src="{IMG}/logo.png">'''
def menu(l):
    ar = l == "ar"; cols = ["#F2A33A", "#E8587A", "#D9C3A1"]; x = [90, 420, 750]
    cups = "".join(f'<div class="abs" style="left:{xx}px;top:{430+dy}px;width:240px;height:320px"><svg viewBox="0 0 100 130" width="100%" height="100%"><path d="M22 28h56l-7 90H29z" fill="{c}"/><path d="M18 28h64" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M58 28l10-26" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="42" cy="60" r="7" fill="rgba(255,255,255,.35)"/><circle cx="58" cy="82" r="6" fill="rgba(255,255,255,.35)"/></svg></div>' for xx, c, dy in zip(x, cols, [30, 0, 40]))
    return css(ar, 1080, 1350, "#111"), f'''<div class="abs" style="left:0;right:0;top:0;height:40px;background:{RED}"></div><div class="abs" style="left:70px;right:70px;top:120px"><h1 style="font-size:{104 if ar else 88}px">{"منيو كبير. بيتغيّر." if ar else "A BIG MENU. ALWAYS CHANGING."}</h1></div>{cups}<div class="abs" style="left:70px;right:70px;top:900px;text-align:center;font-size:{54 if ar else 42}px;font-weight:700">{"قهوتك المعتادة + مشروبات صحية" if ar else "Your usual coffee + healthy drinks"}</div><div class="abs" style="left:70px;right:70px;top:1010px;text-align:center;font-size:{40 if ar else 32}px;opacity:.85">{"اسأل عن مشروب النهارده." if ar else "Ask about today's drink."}</div><img class="logo" src="{IMG}/logo.png">'''
def slide(l, k):
    ar = l == "ar"; D = {"reset": ("اهدا.", "RESET.", "leaf", f"radial-gradient(circle at 20% 10%,#D01212,{RED} 55%,#6A0100)", "#fff", "ابدأ بقعدة هادية.", "Start with a calm seat."),
        "recharge": ("اشحن.", "RECHARGE.", "bolt", "#111", "#fff", "مشروبك مستنيك.", "Your drink is waiting."), "repeat": ("كرّر.", "REPEAT.", "loop", "#F7F2EA", "#111", "الحاجة الحلوة بتتعاد.", "Good things come back.")}[k]
    c = D[4]; icc = RED if k == "repeat" else "#fff"
    return css(ar, 1080, 1350, D[3], c), f'''<div class="abs" style="left:440px;top:150px;width:200px;height:200px">{ICON[D[2]](icc)}</div><div class="abs" style="left:40px;right:40px;top:470px;text-align:center"><h1 style="font-size:{230 if ar else 150}px">{D[0] if ar else D[1]}</h1><div style="margin-top:44px;font-size:{58 if ar else 44}px;font-weight:700">{D[5] if ar else D[6]}</div></div><div class="abs" style="left:0;right:0;top:1180px;text-align:center;font-size:30px;letter-spacing:6px;opacity:.7">{"١ / ٣" if ar and k=="reset" else "٢ / ٣" if ar and k=="recharge" else "٣ / ٣" if ar else {"reset":"1 / 3","recharge":"2 / 3","repeat":"3 / 3"}[k]}</div><img class="logo" src="{IMG}/logo.png" style="{"filter:invert(1)" if k=="repeat" else ""}">'''
def nomember(l):
    ar = l == "ar"
    return css(ar, 1080, 1350, "#F7F2EA", "#111"), f'''<div class="abs" style="left:0;right:0;top:0;height:46px;background:{RED}"></div><div class="abs" style="left:70px;right:70px;top:250px"><h1 style="font-size:{150 if ar else 120}px;color:{RED}">{"مش لازم<br>تكون عضو." if ar else "NO MEMBERSHIP<br>NEEDED."}</h1><div style="margin-top:60px;font-size:{56 if ar else 44}px;font-weight:700;max-width:800px;line-height:1.35">{"الكافيه مفتوح لكل الناس، من ١٠ ص لـ١٢ م." if ar else "The cafe is open to everyone, 10 AM to 12 AM."}</div></div><img class="logo" src="{IMG}/logo.png" style="filter:invert(1)">'''
HL = [("menu", "المنيو", "MENU"), ("clock", "المواعيد", "HOURS"), ("play", "ريلز", "REELS"), ("leaf", "صحي", "HEALTHY"), ("pin", "زورنا", "VISIT")]
def hl(l, k):
    ic, a, e = HL[k]; ar = l == "ar"
    return css(ar, 1080, 1920, "#111"), f'''<div class="abs" style="left:240px;top:660px;width:600px;height:600px;border-radius:50%;background:{RED}"></div><div class="abs" style="left:390px;top:810px;width:300px;height:300px">{ICON[ic]()}</div><div class="abs" style="left:0;right:0;top:1330px;text-align:center"><h1 style="font-size:{90 if ar else 72}px">{a if ar else e}</h1></div>'''
def main():
    jobs = []
    for l in ("ar", "en"):
        jobs += [(l, "e1_hours", hours(l), 1350), (l, "e2_menu", menu(l), 1350), (l, "e3_reset", slide(l, "reset"), 1350), (l, "e3_recharge", slide(l, "recharge"), 1350), (l, "e3_repeat", slide(l, "repeat"), 1350), (l, "e4_no_membership", nomember(l), 1350)]
        jobs += [(l, f"h{k+1}_{HL[k][2].lower()}", hl(l, k), 1920) for k in range(5)]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for l, n, (c, body), h in jobs:
            os.makedirs(f"{HERE}/extras/out/{l}", exist_ok=True); f = f"{HERE}/extras/out/{l}/{n}.html"; open(f, "w").write(f'<!doctype html><meta charset="utf-8"><style>{c}</style>{body}')
            pg = b.new_page(viewport={"width": 1080, "height": h}); pg.goto("file://" + f); pg.wait_for_timeout(300); pg.screenshot(path=f[:-5] + ".png"); pg.close(); os.remove(f)
        b.close()
main()
