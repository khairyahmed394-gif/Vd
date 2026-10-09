import json, os
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"]); pg = b.new_page()
    pg.goto("file://"+os.getcwd()+"/index3.html"); pg.wait_for_function("window.READY===true"); ev = pg.evaluate("window.EVENTS"); b.close()
json.dump(ev, open("events.json", "w")); print(len(ev), "events", sorted({e["k"] for e in ev}))
