"""python3 build.py [ar|en|all] -> out/<lang>/<card>.png 1080x1350 (+2x/)"""
import os, sys, html
from playwright.sync_api import sync_playwright
from cards import C
HERE = os.path.dirname(os.path.abspath(__file__)); RED = "#B30504"
def css(lang):
    ar = lang == "ar"
    return f"""
@font-face{{font-family:M;src:url(fonts/Montserrat.ttf);font-weight:100 900}}
@font-face{{font-family:P;src:url(fonts/PlexAr-Bold.ttf);font-weight:700}}
@font-face{{font-family:P;src:url(fonts/PlexAr-Medium.ttf);font-weight:500}}
*{{margin:0;box-sizing:border-box}} body{{width:1080px;height:1350px;position:relative;overflow:hidden;background:#111;direction:{'rtl' if ar else 'ltr'};font-family:{'P' if ar else 'M'},sans-serif;color:#fff}}
.ph{{position:absolute;inset:0;background-size:cover}}
.sh{{position:absolute;inset:0}}
.logo{{position:absolute;left:50%;bottom:44px;transform:translateX(-50%);width:230px}}
.blk{{position:absolute;{'right' if ar else 'left'}:0;width:86px;background:linear-gradient(#8F0000,{RED} 55%,#6A0100)}}
h1{{font-weight:{700 if ar else 800};line-height:{1.22 if ar else 1.04};letter-spacing:{0 if ar else '-.5px'};text-transform:uppercase;text-shadow:0 2px 22px rgba(0,0,0,.35)}}
.sub{{font-weight:{500 if ar else 600};font-size:{36 if ar else 33}px;line-height:1.4;opacity:.95;text-shadow:0 2px 14px rgba(0,0,0,.5)}}
"""
def photo(p, y, extra=""):
    return f'<div class="ph" style="background-image:url(img/{p}.png);background-position:50% {y}%;{extra}"></div>'
def lines(ls, size):
    return "".join(f'<h1 style="font-size:{size}px">{html.escape(l)}</h1>' for l in ls)
def fit(ls, lang, base):
    n = max(len(l) for l in ls)
    lim = 14 if lang == "ar" else 14
    return base if n <= lim else max(58, int(base * lim / n * (1.12 if lang == "ar" else 1.0)))
def page(c, lang):
    d = c[lang]; ar = lang == "ar"; l = c["l"]; side = "right" if ar else "left"; body = ""
    if l == "A":
        sz = fit(d["lines"], lang, 118 if ar else 112)
        if len(d["lines"]) >= 3: sz = 78 if ar else 98
        body = photo(c["p"], c["y"]) + '<div class="sh" style="background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0) 38%,rgba(0,0,0,0) 62%,rgba(0,0,0,.72))"></div>'
        n = len(d["lines"]); hh = int(sz * (1.22 if ar else 1.04) * n)
        top = 90
        body += f'<div class="blk" style="top:{top}px;height:{hh + 20}px"></div>'
        body += f'<div style="position:absolute;top:{top + 6}px;{side}:{86 + 36}px;max-width:820px">{lines(d["lines"], sz)}'
        if d.get("sub"): body += f'<div class="sub" style="margin-top:26px;max-width:700px">{html.escape(d["sub"])}</div>'
        body += "</div>"
    elif l == "B":
        sz = fit(d["lines"], lang, 104 if ar else 98)
        body = photo(c["p"], c["y"]) + '<div class="sh" style="background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.35) 55%,rgba(0,0,0,.88))"></div>'
        body += f'<div class="blk" style="bottom:250px;height:{int(sz*(1.22 if ar else 1.04)*len(d["lines"]))+20}px"></div>'
        body += f'<div style="position:absolute;bottom:{250}px;{side}:{86+36}px;right:{86+36 if ar else 60}px;left:{60 if ar else 86+36}px;padding-top:6px">{lines(d["lines"], sz)}'
        if d.get("sub"): body += f'<div class="sub" style="margin-top:22px">{html.escape(d["sub"])}</div>'
        body += "</div>"
    elif l in ("C", "H"):
        body = photo(c["p"], c["y"], "filter:blur(%dpx) brightness(.38)" % (10 if l == "H" else 6)) + f'<div class="blk" style="top:120px;height:160px"></div>'
        body += f'<div style="position:absolute;top:126px;{side}:{86+36}px;left:60px;right:60px;padding-{side}:{86+36-60}px"><h1 style="font-size:{ (84 if ar else 70) if l=="C" else (90 if ar else 80)}px">{html.escape(d["title"])}</h1></div>'
        if l == "C":
            body += '<div style="position:absolute;top:430px;left:100px;right:100px">'
            for i, it in enumerate(d["items"], 1):
                num = "٣٢١"[3 - i] if ar else str(i)
                body += f'<div style="display:flex;align-items:center;gap:36px;margin-bottom:46px"><div style="width:96px;height:96px;border:5px solid {RED};background:{RED};border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:54px;font-weight:{700 if ar else 800}">{num}</div><div style="font-size:{62 if ar else 52}px;font-weight:{700 if ar else 700}">{html.escape(it)}</div></div>'
            body += "</div>"
        else:
            body += f'<div style="position:absolute;top:470px;left:60px;right:60px;text-align:center"><div style="font-size:{150 if ar else 104}px;white-space:nowrap;font-weight:{700 if ar else 800};line-height:1.15"><bdi>{html.escape(d["big"])}</bdi></div><div class="sub" style="margin-top:50px;font-size:{40 if ar else 36}px">{html.escape(d["sub"])}</div></div>'
    elif l == "S":
        body = f'<div class="blk" style="top:70px;height:120px"></div><div style="position:absolute;top:76px;{side}:{86+36}px;left:60px;right:60px;padding-{side}:0"><h1 style="font-size:{ 56 if ar else 44}px;max-width:820px;{"text-transform:none" if ar else ""}">{d["title"].replace("Trio Fitness Hub","<bdi style='white-space:nowrap'>Trio Fitness Hub</bdi>") if ar else html.escape(d["title"])}</h1></div>'
        for i, (p, it) in enumerate(zip(c["ps"], d["items"])):
            y0 = 290 + i * 300
            body += f'<div style="position:absolute;left:60px;right:60px;top:{y0}px;height:276px;border-radius:14px;overflow:hidden"><div class="ph" style="background-image:url(img/{p}.png);background-position:50% 40%"></div><div class="sh" style="background:linear-gradient(90deg,rgba(0,0,0,.7),rgba(0,0,0,0) 70%);{"transform:scaleX(-1)" if ar else ""}"></div><div style="position:absolute;{side}:34px;bottom:26px;font-size:{58 if ar else 46}px;font-weight:{700 if ar else 800};text-transform:uppercase">{html.escape(it)}</div></div>'
        body = '<div class="ph" style="background:#0d0d0d"></div>' + body
    return f'<!doctype html><meta charset="utf-8"><style>{css(lang)}</style>{body}<img class="logo" src="img/logo.png">'
def render(langs, only=None):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for lang in langs:
            os.makedirs(f"{HERE}/out/{lang}", exist_ok=True)
            for name, c in C.items():
                if only and name not in only: continue
                f = f"{HERE}/_{name}.html"; open(f, "w").write(page(c, lang))
                pg = b.new_page(viewport={"width": 1080, "height": 1350}); pg.goto("file://" + f); pg.wait_for_timeout(300)
                pg.screenshot(path=f"{HERE}/out/{lang}/{name}.png"); pg.close(); os.remove(f)
            print(lang, "done")
        b.close()
if __name__ == "__main__":
    a = sys.argv[1:]; render(["ar", "en"] if not a or a[0] == "all" else [a[0]], a[1:] or None)
