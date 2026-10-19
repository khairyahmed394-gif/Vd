"""GOOD DAYS at TRIO CAFE - 20 s "Gym to Cafe" photo reel (1080x1920, 24 fps).
Built only from the supplied photographs (text/logo removed with LaMa inpainting, see inpaint.py).
usage: python3 render.py test 0.5,9.5 | python3 render.py full out.mp4 audio.wav [silent]"""
import sys, subprocess, math
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 24; TOTAL = 20.0; N = int(FPS * TOTAL); W, H = 1080, 1920
SRC = {k: cv2.cvtColor(cv2.imread(f"clean/{k}.png"), cv2.COLOR_BGR2RGB) for k in ["p8", "p3", "p1", "p5", "p2", "p6"]}
LOGO = np.asarray(Image.open("logo_extracted.png").convert("RGBA")).astype(np.float32) / 255.0

sm = lambda x: x * x * (3 - 2 * x)
clamp = lambda x, a=0.0, b=1.0: min(b, max(a, x))
P = lambda t, a, b: clamp((t - a) / (b - a))
eio = lambda x: 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
eout = lambda x: 1 - (1 - x) ** 3

# ------------------------------------------------------------------ the match-cut geometry (cup on both sides of the cut)
HC, YT = 880.0, 1000.0                       # cup height and centre y on the canvas at the cut
CUP1 = (607.0, 690.0, 470.0)                 # smoothie cup in p1: cx, cy, height (source px)
CUP5 = (542.0, 817.0, 565.0)                 # orange drink in p5
s1c = HC / CUP1[2]; v1c = (CUP1[0], CUP1[1] + (960 - YT) / s1c)
s5c = HC / CUP5[2]; v5c = (CUP5[0], CUP5[1] + (960 - YT) / s5c)

# shot: name, t0, t1, (s,vx,vy) start, (s,vx,vy) end, ease, handheld amplitude
SHOTS = [
 ("p8", 0.0, 3.25, (1.55, 470, 640), (1.82, 500, 760), eio, 1.0),
 ("p3", 3.25, 6.5, (1.42, 400, 790), (1.75, 380, 880), eio, 1.0),
 ("p1", 6.5, 9.625, (1.50, 560, 720), (s1c, *v1c), eio, 1.0),
 ("p5", 9.625, 13.25, (s5c, *v5c), (1.36, 540, 735), eout, .45),
 ("p2", 13.25, 15.75, (1.40, 690, 745), (1.50, 440, 720), eio, .45),
 ("p6", 15.75, 20.0, (1.40, 600, 720), (1.60, 690, 705), eio, .4),
]
CUTS = [3.25, 6.5, 9.625, 13.25, 15.75]
MATCH = 9.625

def shot_at(t):
    for sh in SHOTS:
        if sh[1] <= t < sh[2]: return sh
    return SHOTS[-1]

def camera(t):
    name, t0, t1, a, b, ease, hh = shot_at(t); u = ease(P(t, t0, t1))
    s = a[0] + (b[0] - a[0]) * u; vx = a[1] + (b[1] - a[1]) * u; vy = a[2] + (b[2] - a[2]) * u
    # handheld drift, eased out around the match-cut so the cup lines up exactly
    near = min(abs(t - MATCH), 9) ; damp = sm(clamp((near - 0.0) / 0.5)) if abs(t - MATCH) < .5 else 1.0
    k = hh * damp
    vx += k * (3.0 * math.sin(2 * math.pi * .43 * t + 1.1) + 1.4 * math.sin(2 * math.pi * 1.13 * t + 2.3)) / s * 1.6
    vy += k * (2.4 * math.sin(2 * math.pi * .37 * t + .4) + 1.1 * math.sin(2 * math.pi * 1.31 * t + 3.1)) / s * 1.6
    rot = k * .10 * math.sin(2 * math.pi * .31 * t + .7)
    # keep the view inside the photograph (small margin for the rotation)
    mx, my = 540 / s + 8 / s, 960 / s + 8 / s
    vx = clamp(vx, mx, 1080 - mx); vy = clamp(vy, my, 1440 - my)
    return name, s, vx, vy, rot

def warp(name, s, vx, vy, rot):
    th = math.radians(rot); c, sn = math.cos(th), math.sin(th)
    tx = 540 - s * (c * vx - sn * vy); ty = 960 - s * (sn * vx + c * vy)
    M = np.array([[s * c, -s * sn, tx], [s * sn, s * c, ty]], np.float32)
    return cv2.warpAffine(SRC[name], M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT_101).astype(np.float32) / 255.0

# ------------------------------------------------------------------ look
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = 1.0 - .30 * np.clip(((xx - 540) / 700) ** 2 + ((yy - 960) / 1150) ** 2, 0, 1.3)
VIG = VIG[..., None]
rngd = np.random.RandomState(5); DAP = [cv2.resize(rngd.rand(24, 14).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC) for _ in range(2)]

def grade(img, cafe, t):
    x = np.clip(img, 0, 1)
    x = x + .13 * (sm(x) - x)                               # gentle S-curve
    lum = x.mean(2, keepdims=True); x = lum + (x - lum) * (1.04 if cafe else 1.02)
    x = x * (np.array([1.035, 1.0, .955], np.float32) if cafe else np.array([1.0, .995, 1.012], np.float32))
    if cafe:                                                # dappled sunlight drifting across the scene
        sx = int(t * 18) % W; sy = int(t * 7) % H
        d = np.roll(np.roll(DAP[0], sx, 1), sy, 0) * .6 + np.roll(DAP[1], -sx // 2, 1) * .4
        x = x * (1 + .09 * (d[..., None] - .5))
    return np.clip(x * VIG, 0, 1)

def whip(img, amount):
    if amount < 1: return img
    k = int(amount) | 1; ker = np.zeros((k, k), np.float32); ker[k // 2, :] = 1.0 / k
    return cv2.filter2D(img, -1, ker, borderType=cv2.BORDER_REFLECT)

# ------------------------------------------------------------------ overlay (text + logo), matches the existing ad series
FONT = ImageFont.truetype("Montserrat.ttf", 108); FONT.set_variation_by_name("ExtraBold")
LINES = ["YOU EARNED", "THIS PART."]; YS = [1372, 1500]
def line_layers():
    out = []
    for txt, cy in zip(LINES, YS):
        bb = FONT.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        bw, bh = tw + 84, 122
        bar = np.zeros((bh, bw, 4), np.float32); bar[..., 0], bar[..., 1], bar[..., 2], bar[..., 3] = 74 / 255, 8 / 255, 12 / 255, .84
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((bw / 2 - tw / 2 - bb[0], bh / 2 - th / 2 - bb[1]), txt, font=FONT, fill=(255, 255, 255, 255))
        out.append((bar, np.asarray(im).astype(np.float32) / 255.0, 540 - bw // 2, cy - bh // 2))
    return out
LL = line_layers()

def blend(img, rgba, x, y, a):
    h, w = rgba.shape[:2]; x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    r = rgba[y0 - y:y1 - y, x0 - x:x1 - x]; al = (r[..., 3:4] * a)
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - al) + r[..., :3] * al

T_TEXT, T_LOGO = 17.4, 18.5
def overlay(img, t):
    g = sm(P(t, T_TEXT - .15, T_TEXT + .6))                  # soft darkening behind the lower third
    if g > 0:
        ramp = np.clip((yy[:, :1] - 950) / 970, 0, 1)[..., None] ** 1.4
        img[:] = img * (1 - .50 * g * ramp)
    for i, (bar, txt, x, y) in enumerate(LL):
        t0 = T_TEXT + i * .22
        wp = eout(P(t, t0, t0 + .40))
        if wp > 0:
            bw = bar.shape[1]; cw = max(1, int(bw * wp)); blend(img, bar[:, :cw], x, y, 1.0)
        tp = eout(P(t, t0 + .12, t0 + .55))
        if tp > 0:
            dy = int((1 - tp) * 14); blend(img, txt, x, y + dy, tp)
    lp = sm(P(t, T_LOGO, T_LOGO + .55))
    if lp > 0:
        lh, lw = LOGO.shape[:2]; blend(img, LOGO, 540 - lw // 2, 1655 - lh // 2 + int((1 - lp) * 10), lp)

CUTSET = {c: i for i, c in enumerate(CUTS)}
def frame(i):
    t = i / FPS
    name, s, vx, vy, rot = camera(t)
    img = grade(warp(name, s, vx, vy, rot), name in ("p5", "p2", "p6"), t)
    # whip-blur into / out of every cut (strongest on the match-cut)
    for c in CUTS:
        d = round((t - c) * FPS); mult = 1.0 if c == MATCH else .55; amt = 0
        if -3 <= d < 0: amt = [8, 22, 44][d + 3] * mult
        elif 0 <= d < 3: amt = [44, 22, 8][d] * mult
        if amt: img = whip(img, amt); img = np.clip(img * (1 + .04 * (amt / 44)), 0, 1)
    # slight flash on the match-cut frame
    if abs(t - MATCH) < .5 / FPS: img = np.clip(img + .06, 0, 1)
    overlay(img, t)
    # film grain
    gn = np.random.RandomState(1000 + i).normal(0, .018, (H // 2, W // 2)).astype(np.float32)
    img = np.clip(img + cv2.resize(gn, (W, H), interpolation=cv2.INTER_LINEAR)[..., None], 0, 1)
    # fade in / out
    f = min(1.0, i / 6.0) * min(1.0, (N - 1 - i) / 4.0)
    img = img * sm(f)
    return (img * 255 + .5).astype(np.uint8)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "test":
        for t in [float(x) for x in sys.argv[2].split(",")]:
            i = int(round(t * FPS)); Image.fromarray(frame(i)).save(f"test_{i:03d}.png"); print("frame", i)
    else:
        out, audio = sys.argv[2], sys.argv[3]; silent = len(sys.argv) > 4
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
        if not silent: cmd += ["-i", audio]
        cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-r", str(FPS), "-frames:v", str(N)]
        cmd += (["-an"] if silent else ["-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL)]) + ["-movflags", "+faststart", out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(N):
            ff.stdin.write(frame(i).tobytes())
            if i % 60 == 0: print(i, N, flush=True)
        ff.stdin.close(); ff.wait(); print("done")
