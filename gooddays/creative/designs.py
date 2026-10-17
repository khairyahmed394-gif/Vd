"""GOOD DAYS creative collection: 14 concepts + 4 carousel/menu slides + 2 reel covers. python3 designs.py -> out/<id>.png.
If img/gen/<id>.jpg exists (AI-generated photo from prompts.md) it replaces the vector stand-in in that design's product slot."""
import os, sys
from playwright.sync_api import sync_playwright
from svg import *
HERE = os.path.dirname(os.path.abspath(__file__)); F = f"file://{HERE}/fonts"
GREEN, OLIVE, CREAM, ESP, CARA, BLUSH = "#17251D", "#747A50", "#F2EBDD", "#493020", "#B9835B", "#E8B9B5"
CSS = f"""@font-face{{font-family:A;src:url({F}/Anton.ttf)}}@font-face{{font-family:C;src:url({F}/Caveat.ttf);font-weight:400 700}}@font-face{{font-family:S;src:url({F}/Playfair.ttf);font-weight:400 900}}@font-face{{font-family:D;src:url({F}/DMSans.ttf);font-weight:100 1000}}
*{{margin:0;box-sizing:border-box}}html{{overflow:hidden}}body{{position:relative;overflow:hidden;font-family:D,sans-serif}}
.a{{font-family:A;text-transform:uppercase;line-height:.98;letter-spacing:.5px}}.c{{font-family:C;font-weight:700;line-height:.95}}.s{{font-family:S;font-weight:600}}.d{{font-family:D;font-weight:600;letter-spacing:3px;text-transform:uppercase;line-height:1.5}}
.p{{position:absolute}}svg.f{{position:absolute;inset:0;width:100%;height:100%}}.logo{{position:absolute;-webkit-mask:url(img/logo.png) center/contain no-repeat;mask:url(img/logo.png) center/contain no-repeat}}
.pill{{position:absolute;padding:20px 44px;border-radius:60px;font-family:D;font-weight:700;letter-spacing:2px;text-transform:uppercase;font-size:30px}}"""
W, H = 1080, 1350
def logo(x, y, w, c): return f'<div class="logo" style="left:{x}px;top:{y}px;width:{w}px;height:{w*135/223}px;background:{c}"></div>'
def T(cls, x, y, s, c, txt, extra=""): return f'<div class="p {cls}" style="left:{x}px;top:{y}px;font-size:{s}px;color:{c};{extra}">{txt}</div>'
def slot(id_, x, y, w, h, r=30, rot=0):
    f = f"img/gen/{id_}.jpg"
    return f'<img class="p" src="{f}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;border-radius:{r}px;transform:rotate({rot}deg)">' if os.path.exists(os.path.join(HERE, f)) else None
def svg(inner, w=W, h=H): return f'<svg class="f" viewBox="0 0 {w} {h}">{inner}</svg>'
COF = [("#5a3a24", .22), ("#E9D9BF", .3), ("#6b4a30", .48)]
def d01():
    s = slot("d01", 330, 300, 560, 900) or svg(f'<path d="M610,0 C600,120 620,200 612,330" stroke="#8a5a34" stroke-width="30" fill="none" stroke-linecap="round"/>' + cup(380, 330, 460, 740, [("#E9D9BF", .12), ("#7a4e2e", .88)], marble="#E9D9BF", uid="d1"))
    return GREEN, (s if s.startswith("<img") else s) + T("c", 70, 110, 128, CREAM, "Good<br>Coffee<br>Better<br>Days.", "transform:rotate(-6deg)") + svg(smiley(150, 650, 38, CREAM)) + T("d", 70, 1120, 26, CREAM, "Same energy.<br>Different day.") + logo(790, 1190, 220, CREAM)
def d02():
    s = slot("d02", 330, 260, 540, 860) or svg(f'<ellipse cx="560" cy="1130" rx="330" ry="60" fill="#d8cdb8"/>' + cup(380, 330, 420, 740, [("#8DA25B", .3), ("#F6EFE2", .28), ("#C23A5C", .42)], uid="d2") + strawberry(300, 1010, 130) + strawberry(760, 1030, 110) + strawberry(640, 1070, 90))
    return CREAM, s + T("c", 70, 110, 120, GREEN, "Matcha<br>Meets<br>Berry<br>Mood", "transform:rotate(-5deg)") + svg(heart(240, 640, 38, GREEN)) + T("d", 800, 90, 22, GREEN, "Good<br>Ingredients<br>Good<br>Mood<br>Always", "text-align:right;left:auto;right:60px") + logo(70, 1210, 200, GREEN)
def d03():
    s = slot("d03", 70, 300, 940, 800) or svg(f'<circle cx="540" cy="880" r="400" fill="{CREAM}"/><circle cx="540" cy="880" r="340" fill="none" stroke="#d8cdb8" stroke-width="6"/>' + croissant(300, 960, 300) + cup(600, 520, 240, 400, [("#5a3a24", .3), ("#E9D9BF", .3), ("#8a5a34", .4)], uid="d3"))
    return GREEN, s + T("c", 560, 70, 130, CREAM, "Brunch<br>Hits<br>Different", "transform:rotate(-5deg)") + svg(star(980, 210, 30, CREAM) + heart(930, 520, 34, CREAM)) + T("d", 70, 1180, 24, CREAM, "Good food<br>Good people<br>Good conversations") + logo(780, 1200, 220, CREAM)
def d04():
    s = slot("d04", 300, 560, 560, 700) or svg(cup(600, 640, 340, 560, [("#C9D3A0", .35), ("#F2EBDD", .35), ("#A9B46F", .3)], uid="d4"))
    return CREAM, f'<div class="p" style="left:0;top:0;width:{W}px;height:520px;background:{BLUSH};clip-path:polygon(0 0,100% 0,100% 86%,94% 92%,88% 85%,80% 94%,72% 86%,62% 95%,52% 87%,42% 94%,32% 86%,22% 95%,12% 87%,5% 93%,0 86%)"></div>' + T("a", 70, 90, 250, ESP, "New<br>in town") + T("c", 70, 700, 80, GREEN, "say hi to<br>the new one") + svg(arrow(280, 900, 420, 960, -50, GREEN) + star(960, 600, 30, ESP)) + s + logo(790, 1210, 220, GREEN) if False else (CREAM, f'<div class="p" style="left:0;top:0;width:{W}px;height:520px;background:{BLUSH};clip-path:polygon(0 0,100% 0,100% 86%,94% 92%,88% 85%,80% 94%,72% 86%,62% 95%,52% 87%,42% 94%,32% 86%,22% 95%,12% 87%,5% 93%,0 86%)"></div>' + T("a", 70, 80, 250, ESP, "New<br>in town") + T("c", 70, 700, 84, GREEN, "say hi to<br>the new one") + svg(arrow(380, 960, 580, 1010, -50, GREEN) + star(960, 620, 30, ESP)) + s + logo(80, 1190, 200, GREEN))
def d05():
    return CREAM, T("a", 120, 120, 215, GREEN, "A good<br>day<br>starts<br>here") + svg(scribble(120, 1050, 520) + smiley(900, 880, 52, GREEN) + star(900, 220, 34, ESP)) + T("c", 120, 1120, 66, ESP, "more than coffee.<br>a better you.") + logo(790, 1190, 220, GREEN)
def d06():
    s = slot("d06", 70, 110, 700, 1000, 40) or svg(f'<rect x="70" y="110" width="700" height="1000" rx="40" fill="#2c3a2d"/><circle cx="560" cy="360" r="130" fill="{CARA}"/><path d="M70,1110 L70,760 C240,700 420,760 770,640 L770,1110z" fill="{OLIVE}"/>')
    return GREEN, s + T("c", 660, 140, 120, CREAM, "Your<br>Kind of<br>Good", "transform:rotate(-6deg)") + svg(heart(900, 620, 38, CREAM)) + T("d", 90, 1160, 26, CREAM, "Work · Chill<br>Meet · Repeat") + logo(790, 1190, 220, CREAM)
def d07():
    cols = [OLIVE, CARA, BLUSH]; out = ""
    for i, (x, y, r) in enumerate([(70, 160, -7), (460, 100, 5), (250, 640, -3)]):
        out += f'<div class="p" style="left:{x}px;top:{y}px;width:400px;height:480px;background:#fff;padding:24px 24px 90px;transform:rotate({r}deg);box-shadow:0 14px 30px rgba(0,0,0,.18)"><div style="width:100%;height:100%;background:{cols[i]};border-radius:6px;overflow:hidden">{slot(f"d07_{i+1}",0,0,352,366,6) or ('<svg viewBox="0 0 352 366" width="352" height="366">' + cup(110, 80, 130, 210, [("#5a3a24", .3), ("#E9D9BF", .3), ("#6b4a30", .4)], uid=f"p{i}") + '</svg>')}</div></div>'
    return CREAM, out + svg(f'<circle cx="260" cy="330" r="0"/>') + T("c", 620, 700, 120, GREEN, "Good<br>People<br>Better<br>Days", "transform:rotate(-6deg)") + svg(heart(960, 1180, 36, GREEN)) + logo(70, 1190, 220, GREEN)
def d08():
    cups = cup(80, 520, 250, 400, [("#5a3a24", .3), ("#E9D9BF", .3), ("#6b4a30", .4)], uid="m1") + cup(420, 480, 250, 400, [("#9CB06A", .5), ("#CFE0A0", .5)], uid="m2") + cup(760, 520, 250, 400, [("#D9738E", .5), ("#F2B8C6", .5)], uid="m3")
    return CREAM, svg(cups + arrow(220, 470, 330, 380, -40, GREEN) + arrow(570, 440, 700, 360, -40, GREEN) + arrow(900, 480, 760, 390, -40, GREEN)) + T("c", 70, 90, 150, GREEN, "Pick your<br>mood") + T("c", 70, 960, 100, ESP, "focus") + T("c", 450, 960, 100, OLIVE, "chill") + T("c", 780, 960, 100, "#B54A68", "social") + T("d", 70, 1150, 26, GREEN, "Which one's your mood today?<br>Tell us below.") + logo(790, 1190, 220, GREEN)
def d09():
    return CREAM, f'<div class="p" style="left:0;top:0;width:540px;height:{H}px;background:{GREEN}"></div><div class="p" style="left:540px;top:0;width:540px;height:{H}px;background:{BLUSH}"></div>' + svg(cup(130, 380, 300, 480, [("#5a3a24", .3), ("#E9D9BF", .3), ("#6b4a30", .4)], uid="t1") + mug(640, 520, 300, 300, ESP) + f'<circle cx="540" cy="675" r="80" fill="{CREAM}"/>') + T("c", 478, 630, 80, GREEN, "or") + T("a", 60, 110, 130, CREAM, "Iced") + T("a", 640, 110, 130, ESP, "Hot") + T("c", 120, 930, 76, CREAM, "cold &amp; bold") + T("c", 640, 930, 76, ESP, "warm &amp; slow") + T("d", 0, 1200, 28, GREEN, "Which team are you? Tell us below.", f"width:{W}px;text-align:center;background:{CREAM};padding:26px 0;top:1060px") + logo(450, 1180, 180, GREEN)
def slide(n, kind):
    base = {"cover": (GREEN, CREAM), "1": (CREAM, GREEN), "2": (BLUSH, GREEN), "3": (GREEN, CREAM)}[n]
    bg, fg = base; body = ""
    if n == "cover": body = T("a", 70, 140, 165, fg, "Build<br>your perfect<br>coffee day") + svg(cup(700, 760, 260, 400, [("#5a3a24", .3), ("#E9D9BF", .3), ("#8a5a34", .4)], uid="s0") + smiley(160, 900, 44, fg)) + T("c", 70, 1100, 80, CARA, "swipe →")
    if n == "1": body = T("a", 70, 140, 120, CARA, "01") + T("a", 70, 300, 170, fg, "Pick<br>your drink") + T("d", 70, 820, 34, fg, "Iced, hot, fruity or creamy.<br>The menu keeps changing.<br>The mood stays.") + svg(cup(700, 760, 240, 380, [("#9CB06A", .5), ("#CFE0A0", .5)], uid="s1") + star(900, 300, 34, fg))
    if n == "2": body = T("a", 70, 140, 120, ESP, "02") + T("a", 70, 300, 135, fg, "Pair it<br>with something<br>good") + T("d", 70, 780, 34, fg, "A little something to eat.<br>Because good days<br>deserve good company.") + svg(croissant(560, 1120, 200) + heart(920, 300, 40, fg))
    if n == "3": body = T("a", 70, 140, 120, CARA, "03") + T("a", 70, 300, 170, fg, "Pick<br>your moment") + T("c", 70, 820, 100, BLUSH, "work. chill.<br>meet. repeat.") + T("d", 70, 1120, 30, fg, "Save this for your next visit.") + svg(smiley(900, 400, 50, fg))
    return bg, body + logo(790 if n != "1" else 790, 1190, 220, fg) + T("d", 70, 1270, 20, fg, f"{ {'cover':'1','1':'2','2':'3','3':'4'}[n]} / 4", "opacity:.7;left:auto;right:70px;top:90px")
def m_cover():
    return GREEN, T("a", 70, 150, 215, CREAM, "The<br>good<br>menu") + T("c", 70, 880, 90, CARA, "changes often.<br>good always.") + svg(cup(700, 700, 280, 440, [("#C23A5C", .3), ("#F6EFE2", .3), ("#8DA25B", .4)], uid="mc") + star(900, 300, 34, CREAM)) + logo(70, 1190, 220, CREAM)
def m_slide():
    return CREAM, f'<div class="p" style="left:70px;top:70px;width:940px;height:80px;border-bottom:4px solid {GREEN}"></div>' + T("d", 70, 90, 24, GREEN, "The good menu · 01") + svg(cup(520, 250, 400, 650, [("#5a3a24", .3), ("#E9D9BF", .3), ("#6b4a30", .4)], uid="ms")) + T("s", 70, 300, 100, ESP, "[Drink<br>name]") + T("d", 70, 640, 30, GREEN, "[One line about the drink]<br>[Ingredients, as supplied]") + f'<div class="pill" style="left:70px;top:960px;background:{ESP};color:{CREAM}">[Price]</div>' + logo(70, 1190, 220, GREEN)
def d12():
    return GREEN, T("a", 70, 100, 175, CREAM, "It's brunch<br>o'clock") + svg(f'<circle cx="320" cy="1010" r="230" fill="{CREAM}"/><circle cx="800" cy="960" r="190" fill="{CARA}"/>' + croissant(200, 1050, 240) + f'<circle cx="800" cy="960" r="140" fill="none" stroke="{CREAM}" stroke-width="6"/>' + arrow(560, 740, 700, 790, -50, CREAM)) + T("d", 70, 520, 30, CREAM, "Great food.<br>Better company.<br>10 AM — 12 AM") + f'<div class="pill" style="left:610px;top:1230px;background:{CARA};color:{GREEN}">Come hungry</div>' + logo(70, 1220, 200, CREAM)
def d13():
    s = slot("d13", 560, 420, 420, 800) or svg(cup(700, 560, 260, 520, [("#E9D9BF", .2), ("#8a5a34", .8)], uid="d13", marble="#E9D9BF"))
    return "#0f1712", T("a", 70, 110, 165, CREAM, "Good<br>fuel for<br>better<br>days.") + s + T("d", 70, 1000, 28, CARA, "Coffee<br>Healthy drinks<br>Good food") + logo(70, 1210, 200, CREAM)
def d14():
    s = slot("d14", 270, 280, 540, 780) or svg(f'<ellipse cx="540" cy="1090" rx="260" ry="46" fill="#e4d4bb"/>' + cup(380, 330, 320, 740, [("#E9D9BF", .2), ("#B9835B", .3), ("#5a3a24", .5)], uid="d14"))
    return "#EBD8BC", T("s", 70, 90, 70, ESP, "The Signature<br>Drink", "text-align:left") + s + T("c", 770, 480, 76, ESP, "[Drink<br>name]", "transform:rotate(-5deg)") + T("d", 70, 1100, 26, ESP, "[Key ingredients, as supplied]") + f'<div class="pill" style="left:70px;top:1190px;background:{GREEN};color:{CREAM};font-size:26px;padding:16px 36px">Try it today</div>' + logo(800, 1200, 200, GREEN)
def r1():
    return GREEN, T("c", 70, 180, 150, CREAM, "watch<br>this pour") + svg(f'<path d="M540,0 C530,300 550,500 545,700" stroke="#8a5a34" stroke-width="34" fill="none" stroke-linecap="round"/>' + cup(300, 760, 480, 760, [("#E9D9BF", .12), ("#7a4e2e", .88)], marble="#E9D9BF", uid="r1"), W, 1920) + logo(430, 1740, 220, CREAM)
def r2():
    return CREAM, T("c", 70, 180, 190, GREEN, "pick<br>your mood") + svg(cup(90, 900, 260, 420, [("#5a3a24", .3), ("#E9D9BF", .3), ("#6b4a30", .4)], uid="q1") + cup(410, 860, 260, 420, [("#9CB06A", .5), ("#CFE0A0", .5)], uid="q2") + cup(730, 900, 260, 420, [("#D9738E", .5), ("#F2B8C6", .5)], uid="q3"), W, 1920) + logo(430, 1740, 220, GREEN)
DESIGNS = {"d01_good_coffee": d01, "d02_matcha_berry": d02, "d03_brunch_hits_different": d03, "d04_new_in_town": d04, "d05_good_day_starts_here": d05, "d06_your_kind_of_good": d06, "d07_good_people": d07, "d08_pick_your_mood": d08, "d09_this_or_that": d09,
 "d10_carousel_1": lambda: slide("cover", 0), "d10_carousel_2": lambda: slide("1", 0), "d10_carousel_3": lambda: slide("2", 0), "d10_carousel_4": lambda: slide("3", 0), "d11_menu_cover": m_cover, "d11_menu_slide_template": m_slide, "d12_brunch_oclock": d12, "d13_good_fuel": d13, "d14_signature_drink": d14,
 "r1_cover_pour": r1, "r2_cover_mood": r2}
def main(only=None):
    os.makedirs(f"{HERE}/out", exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for n, fn in DESIGNS.items():
            if only and n not in only: continue
            bg, body = fn(); h = 1920 if n.startswith("r") else H
            f = f"{HERE}/_{n}.html"; open(f, "w").write(f'<!doctype html><meta charset="utf-8"><style>{CSS}body{{width:{W}px;height:{h}px;background:{bg}}}</style>{body}')
            pg = b.new_page(viewport={"width": W, "height": h}); pg.goto("file://" + f); pg.wait_for_timeout(350); pg.screenshot(path=f"{HERE}/out/{n}.png"); pg.close(); os.remove(f)
        b.close()
if __name__ == "__main__": main(sys.argv[1:] or None)
