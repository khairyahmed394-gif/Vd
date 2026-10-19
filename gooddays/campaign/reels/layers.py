"""Playwright -> transparent 1080x1920 PNG layers (end card text bars, shot labels)."""
import os, html
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = os.path.join(HERE, "..", "posts", "fonts")
CSS = lambda ar: f"""@font-face{{font-family:M;src:url(file://{FONTS}/Montserrat.ttf);font-weight:100 900}}@font-face{{font-family:P;src:url(file://{FONTS}/PlexAr-Bold.ttf);font-weight:700}}
*{{margin:0}}html,body{{background:transparent}}body{{width:1080px;height:1920px;position:relative;direction:{'rtl' if ar else 'ltr'};font-family:{'P' if ar else 'M'},sans-serif;color:#fff}}
.bar{{position:absolute;left:50%;transform:translateX(-50%);background:rgba(74,8,12,.86);padding:0 42px;height:122px;display:flex;align-items:center;white-space:nowrap;font-weight:{700 if ar else 800};text-transform:uppercase}}
.sub{{position:absolute;left:0;right:0;text-align:center;font-weight:{700 if ar else 700};text-transform:uppercase;letter-spacing:{0 if ar else 2}px;text-shadow:0 2px 14px rgba(0,0,0,.6)}}
.lab{{position:absolute;display:flex;align-items:center;gap:22px;font-weight:{700 if ar else 800};font-size:{70 if ar else 58}px;text-transform:uppercase;text-shadow:0 2px 18px rgba(0,0,0,.6);bottom:420px;{'right' if ar else 'left'}:64px}}
.lab i{{display:block;width:20px;height:{88 if ar else 74}px;background:#B30504}}"""
def bdi(s, ar): return s.replace("Trio Fitness Hub", "<bdi style='white-space:nowrap'>Trio Fitness Hub</bdi>") if ar else html.escape(s)
def end_html(d, lang):
    ar = lang == "ar"; ls = d[lang]; sub = d["sub_" + lang]; out = ""
    fs = (92 if ar else 84)
    longest = max(len(l) for l in ls)
    if longest > 14: fs = int(fs * 14 / longest * (1.1 if ar else 1.0))
    ys = [1180, 1312] if len(ls) == 2 else [1246]
    for l, y in zip(ls, ys): out += f'<div class="bar" style="top:{y - 61}px;font-size:{fs}px">{bdi(l, ar) if ar else html.escape(l)}</div>'
    out += f'<div class="sub" style="top:{ys[-1] + 92}px;font-size:{40 if ar else 34}px">{("<bdi dir='ltr'>" + html.escape(sub) + "</bdi>") if (ar and sub.isascii()) else (bdi(sub, ar) if ar else html.escape(sub))}</div>'
    return out
def build(cfgs, outdir):
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for name, c in cfgs.items():
            for lang in ("ar", "en"):
                items = {"end": end_html(c["end"], lang)}
                for i, sh in enumerate(c["shots"]):
                    lab = sh[4] if lang == "ar" else sh[5]
                    if lab: items[f"lab{i}"] = f'<div class="lab"><i></i><span>{html.escape(lab)}</span></div>'
                for k, body in items.items():
                    pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.set_content(f"<style>{CSS(lang == 'ar')}</style>{body}"); pg.wait_for_timeout(250)
                    pg.screenshot(path=f"{outdir}/{name}_{lang}_{k}.png", omit_background=True); pg.close()
        b.close()
if __name__ == "__main__":
    from cfg import REELS; build(REELS, os.path.join(HERE, "layers"))
