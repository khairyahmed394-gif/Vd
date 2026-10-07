import sys, os, subprocess, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); FPS = 30
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
mode = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(f"file://{HERE}/index.html"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
    if errs: print("ERRORS", errs[:5])
    if mode == "test":
        for t in [float(x) for x in sys.argv[2].split(",")]:
            pg.evaluate(f"render({t})"); pg.screenshot(path=f"{HERE}/t_{t:.1f}.png")
    else:
        total = pg.evaluate("TOTAL"); n = int(total*FPS)
        out = sys.argv[2]
        ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-", "-i", sys.argv[3],
            "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(n):
            pg.evaluate(f"render({i/FPS})"); ff.stdin.write(pg.screenshot(type="png"))
            if i % 60 == 0: print(i, n, round(time.time()-t0), flush=True)
        ff.stdin.close(); ff.wait(); print("done", n)
    if errs: print("ERRORS", errs[:5])
    b.close()
