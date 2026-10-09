import os,sys,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--allow-file-access-from-files"]);pg=b.new_page(viewport={"width":1080,"height":1920})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
    pg.goto("file://"+os.getcwd()+"/index.html");pg.wait_for_function("window.READY===true")
    json.dump([[q["n"],q["t0"],q["dur"]] for q in pg.evaluate("PRIN.map(p=>({n:p.n,t0:p.t0,dur:p.dur}))")],open("times.json","w"));print("errs",errs[:5]);b.close()
