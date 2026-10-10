import os, sys, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
CASES={"r01":[3.0,7.0,11.0,15.0,19.5],"r02":[3.0,6.9,10.8,15.2,19.5],"r03":[3.0,7.0,11.0,15.0,19.5],"r04":[3.0,6.9,11.0,15.2,19.5]}
def bands(img):
    a=np.asarray(img.convert("L")).astype(float)
    med=np.median(a[:,60:1020],axis=1,keepdims=True)           # per-row background level
    ink=(np.abs(a-med)>26)[:, 60:1020].sum(1)>3
    out=[];start=None
    for y in range(240,1700):
        if ink[y] and start is None: start=y
        if not ink[y] and start is not None: out.append((start,y-1)); start=None
    if start is not None: out.append((start,1699))
    # merge bands closer than 8 px (letter-internal gaps)
    m=[]
    for b in out:
        if m and b[0]-m[-1][1]<=8: m[-1]=(m[-1][0],b[1])
        else: m.append(b)
    return m
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"])
    for reel,ts in CASES.items():
        pg=b.new_page(viewport={"width":1080,"height":1920}); pg.goto("file://"+os.getcwd()+f"/index.html?reel={reel}"); pg.wait_for_function("window.READY===true")
        for t in ts:
            pg.evaluate(f"render({t})"); pg.screenshot(path="/tmp/claude-0/_b.png"); bs=bands(Image.open("/tmp/claude-0/_b.png"))
            gaps=[bs[i+1][0]-bs[i][1] for i in range(len(bs)-1)]
            print(f"{reel} t={t}: "+"  ".join(f"[{a}-{b_}]" for a,b_ in bs)); print("      gaps:",gaps)
        pg.close()
    b.close()
