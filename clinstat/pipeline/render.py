"""ClinStat Research branded vertical video. Reads palette/content from ../brand/brand.json."""
import json, math, subprocess, sys, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import presenter as pr

HERE = os.path.dirname(os.path.abspath(__file__))
BR = os.path.join(HERE, "..", "brand")
brand = json.load(open(f"{BR}/brand.json"))
pal = brand["palette"]
def hx(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
GREEN, GOLD, CREAM, SAND, VBG = hx(pal["dark_green"]), hx(pal["gold"]), hx(pal["cream_post_bg"]), hx(pal["sand"]), hx(pal["cream_video_bg"])
CHART_G = hx(pal["chart_green"])

W, H, FPS = 1080, 1920, 30
LINES = json.load(open(f"{HERE}/lines.json"))
GAP = 0.45
FD = "/tmp/claude-0/-home-user-Vd/ee1f7c43-4b6d-5f7b-99f3-dbdc662667e5/scratchpad/mpt/repo/resource/fonts"
F_B = lambda n: ImageFont.truetype(f"{FD}/BeVietnamPro-Bold.ttf", n)
F_M = lambda n: ImageFont.truetype(f"{FD}/BeVietnamPro-Medium.ttf", n)
AR_B = lambda n: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", n)

def A(name): return Image.open(f"{BR}/assets/{name}").convert("RGB")

# ------------------------------------------------------------------ audio
pcm, timings, t = [np.zeros(int(0.5*24000), np.int16)], [], 0.5
for i in range(len(LINES)):
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i",f"{HERE}/line{i}.mp3","-ac","1","-ar","24000",f"{HERE}/seg{i}.wav"], check=True)
    w = wave.open(f"{HERE}/seg{i}.wav"); d = np.frombuffer(w.readframes(w.getnframes()), np.int16); w.close()
    timings.append((t, t+len(d)/24000)); pcm += [d, np.zeros(int(GAP*24000), np.int16)]; t += len(d)/24000 + GAP
pcm.append(np.zeros(int(0.7*24000), np.int16))
audio = np.concatenate(pcm); total = len(audio)/24000
w = wave.open(f"{HERE}/voice.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(audio.tobytes()); w.close()
nf = int(total*FPS); a = audio.astype(np.float32)/32768
env = np.array([np.sqrt(np.mean(a[int(i/FPS*24000):int((i+1)/FPS*24000)]**2)+1e-9) for i in range(nf)])
env = np.clip(env/(np.percentile(env, 95)+1e-9), 0, 1)
sm = env.copy()
for i in range(1, nf): sm[i] = 0.55*env[i] + 0.45*sm[i-1]
emph = np.clip(np.convolve(np.maximum(np.diff(sm, prepend=0), 0), np.ones(6)/6, "same")*6, 0, 1)

# ------------------------------------------------------------------ static background
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
bg = np.ones((H, W, 3), np.float32)*np.array(CREAM, np.float32)
def glow(cx, cy, r, col, k): d = np.sqrt((xx-cx)**2+(yy-cy)**2)/r; return np.exp(-d*d)[..., None]*np.array(col, np.float32)*k
bg -= glow(540, 520, 520, (30, 30, 30), 0.0)
bg += glow(540, 520, 430, (255, 255, 255), 0.35) - glow(900, 1500, 600, (20, 24, 28), 0.10)
bgim = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")
d = ImageDraw.Draw(bgim, "RGBA")
for x in range(0, W, 72): d.line([(x, 0), (x, H)], fill=GOLD+(18,), width=1)
for y in range(0, H, 72): d.line([(0, y), (W, y)], fill=GOLD+(18,), width=1)
for k in range(6):  # topographic contours
    d.arc([-300-k*60, 300-k*40, 900+k*90, 1500+k*40], 200, 330, fill=GOLD+(30,), width=2)
rng = np.random.RandomState(3)
for _ in range(46):   # gold/green data dots (logo motif)
    x, y, r = rng.randint(30, W-30), rng.randint(20, 1000), rng.randint(3, 9)
    col = (GOLD if rng.rand() < .6 else CHART_G) + (rng.randint(50, 130),)
    d.ellipse([x-r, y-r, x+r, y+r], fill=col)
# halo ring behind presenter
d.ellipse([140, 130, 940, 930], outline=GOLD+(120,), width=3)
d.ellipse([170, 160, 910, 900], outline=GOLD+(60,), width=2)
# footer band + gold swoosh (as in the posts)
d.rectangle([0, 1838, W, H], fill=GREEN+(255,))
sw = [(W*0.30, H)] + [(W*0.30+ (W*0.70)*t/40, H - 52*math.sin(math.pi*min(1, t/40)**0.8)*(1-0.15*t/40)) for t in range(41)] + [(W, H)]
d.polygon(sw, fill=GOLD+(255,))
lock = A("lockup_light.png"); lw = 560; lock = lock.resize((lw, int(lock.height*lw/lock.width)), Image.LANCZOS)
la = np.array(lock).astype(float); al = np.clip((246-la.min(axis=2))/(246-215), 0, 1)
lock_rgba = Image.fromarray(np.dstack([la, al*255]).astype(np.uint8), "RGBA")
bgim.alpha_composite(lock_rgba, ((W-lw)//2, 36))

# ------------------------------------------------------------------ presenter
base = pr.make_presenter()
PX, PY = (W-pr.PW)//2, 150

# ------------------------------------------------------------------ panels (960x500 cards)
CW, CH, CX0, CY0 = 960, 500, 60, 1005
def card(bgcol): im = Image.new("RGBA", (CW, CH), bgcol+(255,)); return im
def fit(img, w, h):  # contain
    s = min(w/img.width, h/img.height); return img.resize((int(img.width*s), int(img.height*s)), Image.LANCZOS)
def center(dst, img, dy=0): dst.alpha_composite(img.convert("RGBA"), ((CW-img.width)//2, (CH-img.height)//2+dy))
def chip(dst, x, y, text, fill=GREEN, fg=CREAM, size=28):
    dd = ImageDraw.Draw(dst); f = F_B(size); wd = dd.textlength(text, font=f)
    dd.rounded_rectangle([x, y, x+wd+36, y+size+26], 16, fill=fill+(235,)); dd.text((x+18, y+11), text, font=f, fill=fg)

lock_big = A("lockup_light.png"); lock_big = lock_big.resize((840, int(lock_big.height*840/lock_big.width)), Image.LANCZOS)
map_src = A("map_gulf.png"); donut = A("chart_donut.png"); bars = A("chart_bars_lines.png"); phases = A("phases.png").crop((30, 380, 700, 930))
icons = [(A("icon_stats.png"), "Statistical\nreporting gaps"), (A("icon_ethics.png"), "Incomplete ethics\ndocumentation"), (A("icon_scope.png"), "Scope\nmismatch")]

def panel(seg, tl):
    """tl = seconds since segment start"""
    if seg == 0:
        c = card(CREAM); center(c, lock_big, -40)
        dd = ImageDraw.Draw(c); f = F_B(40)
        s1, s2 = "DATA INTEGRITY", "  ·  ACCELERATED TRIALS"
        w1, w2 = dd.textlength(s1, font=f), dd.textlength(s2, font=f); x = (CW-w1-w2)/2
        dd.text((x, 392), s1, font=f, fill=GREEN); dd.text((x+w1, 392), s2, font=f, fill=GOLD)
        dd.line([(CW/2-80, 372), (CW/2+80, 372)], fill=GOLD, width=3)
        return c
    if seg == 1:
        z = 1.0+0.06*min(1, tl/6); src = map_src.crop((0, 400, 720, 400+int(720*CH/CW)))
        im = src.resize((int(CW*z), int(CH*z)), Image.LANCZOS); c = card(GREEN)
        c.alpha_composite(im.convert("RGBA").crop(((im.width-CW)//2, (im.height-CH)//2, (im.width+CW)//2, (im.height+CH)//2)))
        chip(c, 28, 424, "Gulf region  ·  Medical insights"); return c
    if seg == 2:
        c = card(VBG); x = min(1, max(0, (tl-3.0)/0.6))
        a_ = fit(donut, 900, 480); b_ = fit(bars, 900, 480)
        t1 = Image.new("RGBA", c.size, (0, 0, 0, 0)); center(t1, a_); t2 = Image.new("RGBA", c.size, (0, 0, 0, 0)); center(t2, b_)
        t1.putalpha(t1.getchannel("A").point(lambda v: int(v*(1-x)))); t2.putalpha(t2.getchannel("A").point(lambda v: int(v*x)))
        c.alpha_composite(t1); c.alpha_composite(t2); chip(c, 28, 28, "Trial insights", size=26); return c
    if seg == 3:
        c = card(CREAM); dd = ImageDraw.Draw(c, "RGBA")
        x0, y0, x1, y1 = 110, 130, 900, 410
        for g in range(5): dd.line([(x0, y0+g*(y1-y0)/4), (x1, y0+g*(y1-y0)/4)], fill=GOLD+(70,), width=1)
        dd.line([(x0, y0), (x0, y1), (x1, y1)], fill=GREEN, width=3)
        for k, lab in enumerate(["0", "6", "12", "18", "24"]): dd.text((x0+k*(x1-x0)/4-8, y1+10), lab, font=F_M(22), fill=GREEN)
        for k, lab in enumerate(["100%", "75%", "50%", "25%", "0%"]): dd.text((26, y0+k*(y1-y0)/4-12), lab, font=F_M(22), fill=GREEN)
        dd.text((CW/2-60, y1+36), "Months", font=F_M(22), fill=GOLD)
        prog = min(1, tl/3.2)
        def km(rates, col, wd):
            pts, s, tt = [(0, 1.0)], 1.0, 0
            for ti, drop in rates: pts += [(ti, s), (ti, s-drop)]; s -= drop
            pts.append((24, s)); xs = [(x0+(x1-x0)*ti/24, y1-(y1-y0)*sv) for ti, sv in pts]
            cut = x0+(x1-x0)*prog; out = [(min(px, cut), py) for px, py in xs if px <= cut+0.01] or [xs[0]]
            dd.line(out, fill=col, width=wd, joint="curve")
            for px, py in out[1::2]: dd.line([(px, py-9), (px, py+9)], fill=col, width=2)
        km([(2, .06), (5, .09), (8, .07), (11, .08), (15, .07), (19, .06), (22, .04)], GREEN, 6)
        km([(1.5, .09), (3.5, .12), (6, .12), (9, .11), (12, .10), (16, .10), (20, .07)], GOLD, 6)
        chip(c, 640, 100, "Treatment", fill=GREEN, size=22); chip(c, 640, 150, "Control", fill=GOLD, size=22)
        dd.text((28, 24), "Survival analysis", font=F_B(34), fill=GREEN); dd.text((28, 62), "time until any event: relapse · discharge · device failure", font=F_M(20), fill=GOLD)
        return c
    if seg == 4:
        c = card(CREAM); dd = ImageDraw.Draw(c); dd.text((CW/2, 34), "Pre-submission review", font=F_B(36), fill=GREEN, anchor="ma")
        dd.line([(CW/2-70, 86), (CW/2+70, 86)], fill=GOLD, width=3)
        for k, (ic, cap) in enumerate(icons):
            p = min(1, max(0, (tl-0.4-k*1.6)/0.5));
            if p <= 0: continue
            sc = 0.6+0.4*p; im = ic.resize((int(240*sc), int(240*sc)), Image.LANCZOS).convert("RGBA")
            im.putalpha(Image.new("L", im.size, int(255*p))); cx = 170+k*310
            c.alpha_composite(im, (cx-im.width//2, 110+(240-im.height)//2))
            dd.multiline_text((cx, 372), cap, font=F_B(26), fill=GREEN, anchor="ma", align="center", spacing=6)
        return c
    c = card(CREAM); ph = fit(phases, 440, 480); c.alpha_composite(ph.convert("RGBA"), (20, (CH-ph.height)//2))
    dd = ImageDraw.Draw(c); x = 500
    for k, (txt, col) in enumerate([("DATA", GREEN), ("INTEGRITY", GREEN), ("ACCELERATED", GOLD), ("TRIALS", GOLD)]):
        p = min(1, max(0, (tl-0.3-k*0.35)/0.4)); dd.text((x+int(30*(1-p)), 100+k*64), txt, font=F_B(52), fill=col if p > .5 else CREAM)
    dd.line([(x, 372), (x+150, 372)], fill=GOLD, width=3); dd.text((x, 392), "ClinStat Research", font=F_B(30), fill=GREEN)
    return c

shadow = Image.new("RGBA", (CW+80, CH+80), (0, 0, 0, 0)); ImageDraw.Draw(shadow).rounded_rectangle([40, 52, CW+40, CH+52], 36, fill=(0, 20, 12, 80)); shadow = shadow.filter(ImageFilter.GaussianBlur(14))
cmask = Image.new("L", (CW, CH), 0); ImageDraw.Draw(cmask).rounded_rectangle([0, 0, CW-1, CH-1], 32, fill=255)

def draw_name_chip(img, alpha):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); o = ImageDraw.Draw(ov); a = int(235*alpha)
    o.rounded_rectangle([50, 880, 560, 984], 18, fill=GREEN+(a,)); o.rectangle([50, 880, 60, 984], fill=GOLD+(int(255*alpha),))
    o.text((84, 890), "Ahmed Khairi", font=F_B(36), fill=CREAM+(int(255*alpha),)); o.text((84, 940), "Research Developer · ClinStat Research", font=F_M(21), fill=SAND+(int(255*alpha),))
    return Image.alpha_composite(img, ov)

def subtitle(img, text):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); o = ImageDraw.Draw(ov); f = AR_B(44)
    words = text.split(); lines = [text]
    if o.textlength(text, font=f) > 980:
        lines = []; cur = ""
        for wd in words:
            t2 = (cur+" "+wd).strip()
            if o.textlength(t2, font=f) > 940 and cur: lines.append(cur); cur = wd
            else: cur = t2
        lines.append(cur)
    lh = 70; h = lh*len(lines)+30; y0 = 1700-h//2+10
    o.rounded_rectangle([60, y0, W-60, y0+h], 26, fill=GREEN+(228,)); o.rounded_rectangle([60, y0, 72, y0+h], 6, fill=GOLD+(255,))
    for k, l in enumerate(lines): o.text((W/2, y0+16+k*lh), l, font=f, fill=CREAM+(255,), anchor="ma")
    return Image.alpha_composite(img, ov)

music = f"{HERE}/../brand/music.wav"
TEST = os.environ.get("TEST")
TEST_FRAMES = [int(x) for x in TEST.split(",")] if TEST else []
ff = None if TEST else subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-i", f"{HERE}/voice.wav", "-stream_loop", "-1", "-i", music,
    "-filter_complex", f"[2:a]volume=0.16,afade=t=in:d=1.5,afade=t=out:st={total-2:.2f}:d=2,atrim=0:{total:.2f}[m];[1:a]volume=1.0[v];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{HERE}/../clinstat_video.mp4"], stdin=subprocess.PIPE)

seg_start = [s for s, _ in timings]
for i in (TEST_FRAMES if TEST else range(nf)):
    t = i/FPS; frame = bgim.copy()
    p = pr.frame(base, i, t, float(sm[i]), float(emph[i]), 0.5+0.5*math.sin(t*6.3+i*0.2))
    p = p.resize((pr.PW, pr.PH), Image.LANCZOS)
    p = p.rotate(math.sin(t*1.1)*0.7, resample=Image.BICUBIC, center=(380, 700))
    frame.alpha_composite(p, (PX+int(math.sin(t*0.8)*4), PY+int(math.sin(t*1.5)*3)))
    seg = max(k for k, s in enumerate(seg_start) if t >= s-0.05) if t >= seg_start[0]-0.05 else 0
    tl = t-seg_start[seg]; x = min(1, max(0, tl/0.45)); slide = int(60*(1-x)**2)
    c = panel(seg, max(0, tl)); frame.alpha_composite(shadow, (CX0-40, CY0-40+slide+6))
    cc = c.copy(); cc.putalpha(cmask.point(lambda v: int(v*max(0.0, x)))); frame.alpha_composite(cc, (CX0, CY0+slide))
    frame = draw_name_chip(frame, min(1, max(0, (t-0.4)/0.5)))
    cur = next((k for k, (s, e) in enumerate(timings) if s-0.05 <= t <= e+0.2), None)
    if cur is not None: frame = subtitle(frame, LINES[cur])
    if TEST: frame.convert("RGB").save(f"{HERE}/test_{i}.png"); continue
    ff.stdin.write(frame.convert("RGB").tobytes())
if ff: ff.stdin.close(); ff.wait()
print("frames", nf, "dur", round(total, 2))
