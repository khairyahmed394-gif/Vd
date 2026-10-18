"""python3 reels.py  -> out/reels/<lang>/wkNN_<slug>.mp4 (1080x1920, 30 fps, original sound). Uses assets.REELS."""
import os, sys, re, json, subprocess, wave
import numpy as np
from playwright.sync_api import sync_playwright
from assets import REELS
HERE = os.path.dirname(os.path.abspath(__file__)); FPS = 30
MOTIF = {1: "nodes", 2: "cycle", 3: "funnel", 4: "grid", 5: "timer", 6: "nodes", 7: "nodes", 8: "nodes", 9: "grid", 10: "funnel", 11: "cycle", 12: "grid"}
D = {w: 15.0 for w in range(1, 13)}
def scenes(r, ar):
    txt = (r[5] if ar else r[4]); parts = [p.strip() for p in re.split(r"\s*/\s*|\s*>\s*", txt) if p.strip()]
    sc = []
    for i, p in enumerate(parts[:6]):
        sc.append(dict(t=p, y=700 if len(p) < 28 else 640, size=(112 if len(p) < 20 else 92 if len(p) < 36 else 76) * (0.9 if ar else 1), teal=(i == len(parts[:6]) - 1)))
    return sc
def cfg_for(w, ar):
    r = REELS[w - 1]; kick = r[1].upper() if not ar else r[1]
    return dict(D=D[w], kick=("WEEK %02d" % w) if not ar else "الأسبوع %02d" % w, scenes=scenes(r, ar), motifName=MOTIF[w])
def audio(w, path, dur):
    SR = 44100; N = int(SR * dur); t = np.arange(N) / SR; rs = np.random.RandomState(w * 7); L = np.zeros(N); R = np.zeros(N)
    mid = lambda m: 440.0 * 2 ** ((m - 69) / 12); ss = lambda x: (lambda y: y * y * (3 - 2 * y))(np.clip(x, 0, 1))
    prog = [[50, 57, 62, 65], [48, 55, 60, 64], [46, 53, 58, 62], [45, 52, 57, 60]]
    for ci in range(int(dur / 3.75) + 2):
        a = ci * 3.75; env = ss((t - (a - .5)) / 1.4) * (1 - ss((t - (a + 3.75 - .3)) / 1.2))
        for k, m in enumerate(prog[ci % 4]):
            f = mid(m)
            for arr, det in ((L, -3), (R, 3)): arr += env * (np.sin(2 * np.pi * f * 2 ** (det / 1200) * t) + .2 * np.sin(2 * np.pi * 2 * f * t)) * (.05 if k else .09)
    def put(x, at, vol=1., pan=.5):
        s = int(at * SR); e = min(N, s + len(x))
        if s < N and e > s: L[s:e] += x[:e - s] * vol * (1 - pan) * 1.4; R[s:e] += x[:e - s] * vol * pan * 1.4
    for i in range(int(dur / .5)):
        at = i * .5 + .4
        if at > dur - 1: break
        m = prog[int(at // 3.75) % 4][[1, 2, 3, 2][i % 4]] + 12; k = np.arange(int(.7 * SR)) / SR
        put((np.sin(2 * np.pi * mid(m) * k) + .3 * np.sin(2 * np.pi * 2 * mid(m) * k)) * np.exp(-k * 6) * np.minimum(k / .004, 1) * .07, at, 1, .3 + .4 * ((i * 5) % 7) / 6)
    n = len(scenes(REELS[w - 1], False)); span = (dur - 3.0 - .4) / max(n, 1)
    for i in range(n):                                  # tick on every scene change
        k = np.arange(int(.25 * SR)) / SR; x = np.sin(2 * np.pi * 1500 * k) * np.exp(-k * 30) * .1 + rs.randn(len(k)) * np.exp(-k * 40) * .05; put(x, .4 + i * span, 1, .5)
    k = np.arange(int(1.4 * SR)) / SR                    # end chime
    for j, m in enumerate([72, 76, 79]): put((np.sin(2 * np.pi * mid(m) * k)) * np.exp(-k * 3) * np.minimum(k / .004, 1) * .1, dur - 3.0 + j * .12, 1, .5)
    f = ss(t / .4) * ss((dur - t) / .6); L *= f; R *= f; m = max(np.abs(L).max(), np.abs(R).max()); st = np.stack([L, R], 1) / m * .85
    with wave.open(path, "wb") as wv: wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((st * 32767).astype("<i2").tobytes())
def render(weeks, langs):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for w in weeks:
            slug = re.sub(r"[^a-z0-9]+", "-", REELS[w - 1][1].lower()).strip("-")
            wav = f"{HERE}/out/reels/audio_{w:02d}.wav"; os.makedirs(os.path.dirname(wav), exist_ok=True); audio(w, wav, D[w])
            for lang in langs:
                ar = lang == "ar"; out = f"{HERE}/out/reels/{lang}/wk{w:02d}_{slug}.mp4"; os.makedirs(os.path.dirname(out), exist_ok=True)
                pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.goto(f"file://{HERE}/reel.html#{lang}"); pg.reload(); pg.wait_for_timeout(500)
                m = cfg_for(w, ar); pg.evaluate("(m)=>{const c=JSON.parse(m);c.motif=window.MOT[c.motifName];setup(c)}", json.dumps(m)); pg.wait_for_timeout(200)
                ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-t", str(D[w]), "-movflags", "+faststart", out], stdin=subprocess.PIPE)
                for i in range(int(D[w] * FPS)): pg.evaluate(f"frame({i / FPS})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
                ff.stdin.close(); ff.wait(); pg.close(); print("done", out, flush=True)
        b.close()
if __name__ == "__main__":
    ws = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else list(range(1, 13)); lg = sys.argv[2].split(",") if len(sys.argv) > 2 else ["en", "ar"]
    render(ws, lg)
