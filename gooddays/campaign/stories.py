"""New designs: 24 Instagram/Facebook Story cards (1080x1920) for the text/poll posts + 6 red typographic feed cards (1080x1350). python3 stories.py"""
import os, html, sys
sys.path.insert(0, "posts")
from playwright.sync_api import sync_playwright
from content import TEXT
HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = f"{HERE}/posts/fonts"; IMG = f"{HERE}/posts/img"; RED = "#B30504"
PH = ["p6", "p5", "p2", "p4", "p1", "p8", "p3", "p7"]
def base(ar, w, h): return f"""@font-face{{font-family:M;src:url(file://{FONTS}/Montserrat.ttf);font-weight:100 900}}@font-face{{font-family:P;src:url(file://{FONTS}/PlexAr-Bold.ttf);font-weight:700}}
*{{margin:0;box-sizing:border-box}}html{{overflow:hidden}}body{{width:{w}px;height:{h}px;position:relative;overflow:hidden;direction:{'rtl' if ar else 'ltr'};font-family:{'P' if ar else 'M'},sans-serif;color:#fff;background:#111}}
.ph{{position:absolute;inset:0;background-size:cover}}.logo{{position:absolute;left:50%;transform:translateX(-50%);width:230px}}
h1{{font-weight:{700 if ar else 800};text-transform:uppercase;line-height:{1.28 if ar else 1.1};text-shadow:0 2px 22px rgba(0,0,0,.4)}}"""
def txt(s): return "<br>".join(html.escape(x) for x in s.split("\n"))
def story(i, ar_txt, en_txt, poll, lang, p):
    ar = lang == "ar"; text = ar_txt if ar else en_txt; opts = (poll[0] if ar else poll[1]) if poll else None
    parts = text.split("\n"); head = parts[0]; sub = " ".join(parts[1:]); side = "right" if ar else "left"
    hs = 80 if ar else 66; ss = 46 if ar else 38
    body = f'<div class="ph" style="background-image:url({IMG}/{p}.png);background-position:50% 40%;filter:brightness({.45 if opts else .85}) {"blur(5px)" if opts else ""}"></div><div class="ph" style="background:linear-gradient(180deg,rgba(0,0,0,.6),rgba(0,0,0,0) 40%,rgba(0,0,0,.85))"></div>'
    inner = f'<h1 style="font-size:{hs}px">{html.escape(head)}</h1>' + (f'<div style="margin-top:28px;font-size:{ss}px;font-weight:{600 if not ar else 700};line-height:1.4;opacity:.95;text-shadow:0 2px 14px rgba(0,0,0,.6)">{html.escape(sub)}</div>' if sub else "")
    pos = "top:230px" if opts else "bottom:330px"
    body += f'<div style="position:absolute;{pos};left:60px;right:60px;"><div style="position:absolute;{side}:0;top:0;bottom:0;width:22px;background:linear-gradient({RED},#6A0100)"></div><div style="padding-{side}:56px;">{inner}</div></div>'
    if opts:
        for k, o in enumerate(opts):
            body += f'<div style="position:absolute;left:100px;right:100px;top:{900+k*190}px;height:150px;border:5px solid #fff;border-radius:75px;display:flex;align-items:center;justify-content:center;font-size:{64 if ar else 52}px;font-weight:700;background:rgba(255,255,255,.08)">{html.escape(o)}</div>'
    body += '<img class="logo" src="' + IMG + '/logo.png" style="bottom:110px">'
    return f"<style>{base(ar, 1080, 1920)}</style>{body}"
def card(q, lang):
    ar = lang == "ar"; n = max(len(l) for l in q.split("\n")); fs = 124 if ar else 100
    body = f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 20% 15%,#D01212,{RED} 45%,#6A0100)"></div><div style="position:absolute;{"left" if ar else "right"}:20px;top:40px;font-size:1000px;font-weight:800;font-family:M;color:transparent;-webkit-text-stroke:5px rgba(255,255,255,.28);line-height:1">?</div>'
    body += f'<div style="position:absolute;left:80px;right:80px;top:340px"><h1 style="font-size:{fs}px">{txt(q)}</h1></div><img class="logo" src="{IMG}/logo.png" style="bottom:60px">'
    return f"<style>{base(ar, 1080, 1350)}</style>{body}"
CARDS = [("q1", "اهدا. اشحن. كرّر.\nإيه اللي بتحتاجه النهارده؟", "RESET. RECHARGE. REPEAT.\nWHAT DO YOU NEED TODAY?"),
 ("q2", "قهوة ولا مشروب بارد؟", "COFFEE OR\nA COLD DRINK?"), ("q3", "صبح ولا ليل؟", "MORNING OR\nNIGHT?"),
 ("q4", "مين بيشرب قهوته\nبعد التمرين؟", "WHO DRINKS THEIR\nCOFFEE AFTER TRAINING?"), ("q5", "تيجي لوحدك\nولا مع صحابك؟", "COME ALONE\nOR WITH FRIENDS?"), ("q6", "مفتوحين من ١٠ ص\nلـ١٢ م", "OPEN 10 AM\nTO 12 AM")]
def main():
    out = f"{HERE}/stories/out"; os.makedirs(f"{out}/ar", exist_ok=True); os.makedirs(f"{out}/en", exist_ok=True); os.makedirs(f"{HERE}/cards/out/ar", exist_ok=True); os.makedirs(f"{HERE}/cards/out/en", exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        def shot(html_, path, w, h):
            f = path + ".html"; open(f, "w").write(f'<!doctype html><meta charset="utf-8">' + html_); pg = b.new_page(viewport={"width": w, "height": h}); pg.goto("file://" + f); pg.wait_for_timeout(300); pg.screenshot(path=path + ".png"); pg.close(); os.remove(f)
        for i, (w, d, ar, en, pa, pe) in enumerate(TEXT):
            name = f"wk{w:02d}_{'sun' if d == 'الأحد' else 'wed'}"
            for lang in ("ar", "en"): shot(story(i, ar, en, (pa, pe) if pa else None, lang, PH[i % 8]), f"{out}/{lang}/{name}", 1080, 1920)
        for k, a, e in CARDS:
            for lang, q in (("ar", a), ("en", e)): shot(card(q, lang), f"{HERE}/cards/out/{lang}/{k}", 1080, 1350)
        b.close()
main()
