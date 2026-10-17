"""moodboard.png (palette, type, graphic language, designs) and grid.png (recommended 3x4 Instagram grid). python3 board.py"""
import os
from playwright.sync_api import sync_playwright
from designs import CSS, F, GREEN, OLIVE, CREAM, ESP, CARA, BLUSH, HERE
GRID = ["d01_good_coffee", "d05_good_day_starts_here", "d08_pick_your_mood", "d04_new_in_town", "d06_your_kind_of_good", "d12_brunch_oclock", "d02_matcha_berry", "d09_this_or_that", "d13_good_fuel", "d14_signature_drink", "d03_brunch_hits_different", "d07_good_people"]
def board():
    sw = "".join(f'<div style="width:150px"><div style="height:150px;border-radius:50%;background:{c};border:3px solid rgba(0,0,0,.08)"></div><div class="d" style="font-size:17px;margin-top:12px;color:{GREEN}">{n}<br>{c}</div></div>' for c, n in [(GREEN, "Forest"), (OLIVE, "Olive"), (CREAM, "Cream"), (ESP, "Espresso"), (CARA, "Caramel"), (BLUSH, "Blush")])
    th = "".join(f'<img src="out/{g}.png" style="width:300px;height:375px;object-fit:cover;border-radius:10px">' for g in GRID[:8])
    return f'''<div style="position:absolute;inset:0;background:{CREAM};padding:70px">
<div class="a" style="font-size:120px;color:{GREEN}">Good Days</div><div class="d" style="font-size:24px;color:{GREEN};margin-top:6px">at Trio Cafe · creative direction · moodboard</div>
<div style="display:flex;gap:30px;margin-top:60px">{sw}</div>
<div style="display:flex;gap:70px;margin-top:70px;align-items:flex-end"><div><div class="d" style="font-size:18px;color:{CARA}">Headline · Anton</div><div class="a" style="font-size:110px;color:{GREEN}">Good Fuel</div></div><div><div class="d" style="font-size:18px;color:{CARA}">Editorial · Playfair</div><div class="s" style="font-size:90px;color:{ESP}">The Good Menu</div></div><div><div class="d" style="font-size:18px;color:{CARA}">Handwritten · Caveat</div><div class="c" style="font-size:110px;color:{ESP}">Your kind of good</div></div></div>
<div style="display:flex;gap:30px;margin-top:70px">{th[:0]}{"".join(f'<img src="out/{g}.png" style="width:310px;height:388px;object-fit:cover;border-radius:10px">' for g in GRID[:6])}</div>
<div class="d" style="font-size:22px;color:{GREEN};margin-top:40px;line-height:1.9">Rules: cream + forest green lead · caramel and espresso for coffee · olive and blush for colourful drinks · one headline per design · doodles used sparingly · real photography for product, vectors for graphics</div></div>'''
def grid():
    cells = "".join(f'<img src="out/{g}.png" style="width:350px;height:437px;object-fit:cover;margin:0 5px 5px 0">' for g in GRID)
    return f'<div style="position:absolute;inset:0;background:#fff;padding:20px;display:flex;flex-wrap:wrap;align-content:flex-start">{cells}</div>'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
    for name, fn, w, h in (("moodboard", board, 2200, 1500), ("grid", grid, 1090, 1790)):
        f = f"{HERE}/_{name}.html"; open(f, "w").write(f'<!doctype html><meta charset="utf-8"><style>{CSS}body{{width:{w}px;height:{h}px;background:#fff}}</style>{fn()}')
        pg = b.new_page(viewport={"width": w, "height": h}); pg.goto("file://" + f); pg.wait_for_timeout(500); pg.screenshot(path=f"{HERE}/{name}.png"); pg.close(); os.remove(f)
    b.close()
