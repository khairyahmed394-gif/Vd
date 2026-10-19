"""python3 render.py <en|ar> test 1,3,6,10,13 | python3 render.py <en|ar> full out.mp4 audio.wav  (1080x1920, 30 fps, 15 s)"""
import sys, subprocess, os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); FPS = 30; D = 15.0; N = int(FPS * D)
lang, mode = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.goto(f"file://{HERE}/motion.html#{lang}"); pg.reload(); pg.wait_for_timeout(600)
    if mode == "test":
        for t in [float(x) for x in sys.argv[3].split(",")]:
            pg.evaluate(f"render({t})"); pg.screenshot(path=f"/tmp/claude-0/swap/m_{lang}_{t:05.2f}.png"); print("t", t)
    else:
        out, audio = sys.argv[3], sys.argv[4]
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(D), "-movflags", "+faststart", out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(N):
            pg.evaluate(f"render({i / FPS})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=95))
        ff.stdin.close(); ff.wait(); print("done", out)
    b.close()
