"""python3 render.py <reel> <ar|en> test 2,8,13 | python3 render.py <reel> <ar|en> full out.mp4 audio.wav   (1080x1920, 24 fps, photo-based)"""
import sys, os, subprocess
import cv2, numpy as np
from PIL import Image
from cfg import REELS
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "..", "posts", "img")
FPS = 24; W, H = 1080, 1920
sm = lambda x: x * x * (3 - 2 * x); clamp = lambda x, a=0.0, b=1.0: min(b, max(a, x)); P = lambda t, a, b: clamp((t - a) / (b - a))
eio = lambda x: 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
name, lang = sys.argv[1], sys.argv[2]; C = REELS[name]; D = C["D"]; N = int(D * FPS)
SRC = {k: cv2.cvtColor(cv2.imread(f"{IMG}/{k}.png"), cv2.COLOR_BGR2RGB) for k in {s[0] for s in C["shots"]}}
LOGO = np.asarray(Image.open(f"{IMG}/logo.png").convert("RGBA")).astype(np.float32) / 255.0
def layer(k):
    f = f"{HERE}/layers/{name}_{lang}_{k}.png"; return np.asarray(Image.open(f).convert("RGBA")).astype(np.float32) / 255.0 if os.path.exists(f) else None
END = layer("end"); LABS = [layer(f"lab{i}") for i in range(len(C["shots"]))]
XF = 0.3
def warp(photo, a, b, u, t):
    s = a[0] + (b[0] - a[0]) * u; vx = a[1] + (b[1] - a[1]) * u + 2.2 * np.sin(t * 1.7) / s; vy = a[2] + (b[2] - a[2]) * u + 1.8 * np.sin(t * 1.3 + 1) / s
    mx, my = 540 / s + 4, 960 / s + 4; vx = clamp(vx, mx, 1080 - mx); vy = clamp(vy, my, 1440 - my)
    M = np.array([[s, 0, 540 - s * vx], [0, s, 960 - s * vy]], np.float32)
    return cv2.warpAffine(SRC[photo], M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT_101).astype(np.float32) / 255.0
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); VIG = (1.0 - .28 * np.clip(((xx - 540) / 700) ** 2 + ((yy - 960) / 1150) ** 2, 0, 1.3))[..., None]
def grade(x):
    x = np.clip(x, 0, 1); x = x + .12 * (sm(x) - x); l = x.mean(2, keepdims=True); x = l + (x - l) * 1.04
    return np.clip(x * np.array([1.03, 1.0, .965], np.float32) * VIG, 0, 1)
def blend(img, rgba, x, y, a):
    h, w = rgba.shape[:2]; x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    r = rgba[y0 - y:y1 - y, x0 - x:x1 - x]; al = r[..., 3:4] * a; img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - al) + r[..., :3] * al
def frame(i):
    t = i / FPS; sh = C["shots"]
    def render_shot(j):
        p, t0, t1, (a, b), *_ = sh[j]; lo, hi = t0 - XF, t1 + XF; return warp(p, a, b, eio(P(t, lo, hi)), t)
    j = next(k for k, s in enumerate(sh) if s[1] <= t < s[2]) if t < sh[-1][2] else len(sh) - 1
    img = render_shot(j)
    if j + 1 < len(sh):
        al = sm(P(t, sh[j][2] - XF, sh[j][2] + XF))
        if al > 0: img = img * (1 - al) + render_shot(j + 1) * al
    elif j > 0:
        pass
    if j > 0 and t < sh[j][1] + XF:    # incoming dissolve from previous shot handled via previous frame blend
        al = 1 - sm(P(t, sh[j][1] - XF, sh[j][1] + XF)); img = img * (1 - al) + render_shot(j - 1) * al
    img = grade(img)
    # shot label
    for k, L in enumerate(LABS):
        if L is not None:
            a = sm(P(t, sh[k][1] + .25, sh[k][1] + .6)) * (1 - sm(P(t, min(sh[k][2], C["end"]["t"]) - .35, min(sh[k][2], C["end"]["t"]) - .02)))
            if a > 0: blend(img, L, 0, int((1 - a) * 14), a)
    e = C["end"]; g = sm(P(t, e["t"] - .2, e["t"] + .6))
    if g > 0:
        ramp = np.clip((yy[:, :1] - 900) / 1020, 0, 1)[..., None] ** 1.3; img = img * (1 - .55 * g * ramp)
        a = sm(P(t, e["t"] + .1, e["t"] + .7))
        if a > 0: blend(img, END, 0, int((1 - a) * 16), a)
    lp = sm(P(t, C["logo"], C["logo"] + .55))
    if lp > 0: lh, lw = LOGO.shape[:2]; blend(img, LOGO, 540 - lw // 2, 1655 - lh // 2 + int((1 - lp) * 10), lp)
    gn = np.random.RandomState(900 + i).normal(0, .016, (H // 2, W // 2)).astype(np.float32); img = np.clip(img + cv2.resize(gn, (W, H))[..., None], 0, 1)
    f = min(1.0, i / 6.0) * min(1.0, (N - 1 - i) / 6.0)
    return (img * sm(f) * 255 + .5).astype(np.uint8)
if __name__ == "__main__":
    if sys.argv[3] == "test":
        for t in [float(x) for x in sys.argv[4].split(",")]:
            i = int(round(t * FPS)); Image.fromarray(frame(i)).save(f"/tmp/claude-0/swap/t_{name}_{lang}_{i:03d}.png"); print("frame", i)
    else:
        out, audio = sys.argv[4], sys.argv[5]
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
               "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-frames:v", str(N), "-c:a", "aac", "-b:a", "192k", "-t", str(D), "-movflags", "+faststart", out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(N): ff.stdin.write(frame(i).tobytes())
        ff.stdin.close(); ff.wait(); print("done", out)
