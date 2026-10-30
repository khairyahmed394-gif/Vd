import asyncio,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));OUT=f"{HERE}/../covers/reels_en"
J=[("r01","wk01_tue_assumptions"),("r02","wk02_tue_design"),("r03","wk02_thu_test"),("r04","wk12_tue_model")]
for l in open(f"{HERE}/jobs.txt"):
    a=l.split()
    if len(a)==2: J.append((a[0],a[1]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox","--disable-gpu","--font-render-hinting=none","--allow-file-access-from-files"])
        for scale,suf in((1,"1080x1920"),(2,"2160x3840")):
            for r,n in J:
                pg=await b.new_page(viewport={"width":1080,"height":1920},device_scale_factor=scale)
                f="index.html" if r in("r01","r02","r03","r04") else "index_gen.html"
                await pg.goto(f"file://{HERE}/{f}?reel={r}&lang=en");await pg.wait_for_function("window.READY===true",timeout=30000);await pg.wait_for_timeout(300)
                await pg.evaluate("render(2.9)");await pg.wait_for_timeout(150)
                await pg.evaluate("""()=>{
 const L=[...SC[0].g.querySelectorAll('text')].map(t=>({s:t.textContent,f:t.getAttribute('fill'),z:parseFloat(t.getAttribute('font-size')),y:parseFloat(t.getAttribute('y'))})).filter(t=>t.y<1050&&t.s.trim()&&!/^p\\s*=|^\\s*[0-9.]+$/.test(t.s));
 L.sort((a,b)=>a.y-b.y);
 [...svg.children].forEach(c=>{if(c.tagName!=='defs')svg.removeChild(c);});
 const bgr=el('rect',{width:1080,height:1920,fill:'#F9F5EF'},svg);
 el('circle',{cx:1000,cy:1500,r:700,fill:'#B19063',opacity:.06},svg);
 const lg=lockup(svg,false);place(lg,540,340,1.2);
 const tmp=L.map(t=>{const x=T(svg,t.s,0,0,100,700,t.f);const w=x.getBBox().width;svg.removeChild(x);return w;});
 let sz=Math.min(124,...tmp.map(w=>100*900/w));const lh=sz*1.32;
 let y=1010-(L.length*lh)/2+sz*.8;
 L.forEach((t,i)=>{T(svg,t.s,540,y,sz,700,t.f,{'text-anchor':'middle'});y+=lh;});
 el('rect',{x:440,y:y-40,width:200,height:7,rx:3.5,fill:'#B19063'},svg);
 el('path',{d:'M360,1920 C730,1919 950,1872 1080,1778 L1080,1920 Z',fill:'#B19063'},svg);
 el('path',{d:'M360,1920 C730,1919 950,1872 1080,1778 L1080,1750 C960,1840 760,1896 470,1920 Z',fill:'#025130'},svg);
 }""")
                await pg.screenshot(path=f"{OUT}/cover_{n}_{suf}.png");await pg.close()
        await b.close()
asyncio.run(main())
