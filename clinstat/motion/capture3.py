import sys, os, subprocess, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); FPS = 30; SUB = 8; SHUTTER = 0.5
out, audio = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"file://{HERE}/index3.html"); pg.wait_for_function("window.READY===true", timeout=30000); pg.wait_for_timeout(300)
    pg.evaluate("window.NOBLUR=true")          # blur comes from sub-frame accumulation instead
    n = int(pg.evaluate("TOTAL")*FPS)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS*SUB), "-c:v", "mjpeg", "-i", "-", "-i", audio,
        "-vf", f"tmix=frames={SUB},select='eq(mod(n\\,{SUB})\\,{SUB-1})',setpts=N/({FPS}*TB)", "-r", str(FPS),
        "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(n):
        T = i/FPS
        for k in range(SUB):
            t = max(0.0, T + (k-(SUB-1)/2)*(SHUTTER/FPS)/(SUB-1))
            pg.evaluate(f"render({t})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=95))
        if i % 30 == 0: print(i, n, round(time.time()-t0), flush=True)
    ff.stdin.close(); ff.wait(); print("done", n, "errs", errs[:3])
    b.close()
