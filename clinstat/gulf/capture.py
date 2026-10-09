import sys, os, subprocess, time, json
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); FPS=30; SUB=4; SHUTTER=0.5
mode=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--disable-gpu","--font-render-hinting=none","--allow-file-access-from-files"])
    pg=b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=1)
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
    pg.goto(f"file://{HERE}/index.html"); pg.wait_for_function("window.READY===true",timeout=30000); pg.wait_for_timeout(300)
    if mode=="test":
        for t in [float(x) for x in sys.argv[2].split(",")]:
            pg.evaluate(f"render({t})"); pg.screenshot(path=f"{HERE}/t_{t:.2f}.png")
    elif mode=="events":
        json.dump(pg.evaluate("window.EVENTS"),open(f"{HERE}/events.json","w")); print("events",len(pg.evaluate("window.EVENTS")))
    else:
        out,audio=sys.argv[2],sys.argv[3]; n=int(round(pg.evaluate("TOTAL")*FPS))
        ff=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","image2pipe","-framerate",str(FPS*SUB),"-c:v","mjpeg","-i","-","-i",audio,
            "-vf",f"tmix=frames={SUB},select='eq(mod(n\\,{SUB})\\,{SUB-1})',setpts=N/({FPS}*TB)","-r",str(FPS),"-frames:v",str(n),"-t","23",
            "-c:v","libx264","-preset","slow","-crf","14","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",out],stdin=subprocess.PIPE)
        t0=time.time()
        for i in range(n):
            for k in range(SUB):
                t=min(TOTAL:=23.0, max(0.0, i/FPS+(k-(SUB-1)/2)*(SHUTTER/FPS)/(SUB-1)))
                pg.evaluate(f"render({t})"); ff.stdin.write(pg.screenshot(type="jpeg",quality=96))
            if i%60==0: print(i,n,round(time.time()-t0),flush=True)
        ff.stdin.close(); ff.wait(); print("done",n,"errs",errs[:3])
    if errs: print("PAGE ERRORS",errs[:5])
    b.close()
