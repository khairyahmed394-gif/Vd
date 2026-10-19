import asyncio
from playwright.async_api import async_playwright
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--allow-file-access-from-files"])
        for name,w,h,lang in [("ar_desktop",1440,900,"ar"),("en_desktop",1440,900,"en"),("ar_mobile",390,844,"ar")]:
            pg=await b.new_page(viewport={"width":w,"height":h});await pg.goto(f"file:///home/user/Vd/daraya/site/{lang}/index.html");await pg.wait_for_timeout(500)
            await pg.evaluate("document.querySelectorAll('.rv').forEach(n=>n.classList.add('in'))");await pg.wait_for_timeout(900)
            await pg.screenshot(path=f"/tmp/cs/site_{name}.png",full_page=True)
        await b.close()
asyncio.run(m())
