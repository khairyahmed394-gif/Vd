import re,os
src=open("site_build.py").read().split("for k in(")[0]
exec(src)
css=open("site/assets/style.css").read()
# strip font-face (use Google Fonts) and old root
css=re.sub(r"@font-face\{[^}]*\}\n","",css)
css=css.replace(":root{--navy:#0F1F3D;--navy2:#0b1730;--teal:#12B5A6;--amber:#E8A33D;--cream:#F7F4EE;--slate:#5B6B82;--line:#0F1F3D1a;--r:22px;--max:1180px}","")
css=css.replace("font-family:Plex,Manrope,Inter,system-ui,sans-serif;background:var(--cream);color:var(--navy)","font-family:'IBM Plex Sans Arabic','Manrope',system-ui,sans-serif;background:var(--bg);color:var(--fg)")
css=css.replace("[lang=en] body{font-family:Manrope,Inter,Plex,system-ui,sans-serif}","[lang=en]{font-family:'Manrope','IBM Plex Sans Arabic',system-ui,sans-serif}")
css=css.replace("header{position:sticky;top:0;z-index:50;background:#F7F4EEdd","header{position:sticky;top:env(safe-area-inset-top,0px);z-index:50;background:var(--hdr)")
css=css.replace(".wrap{max-width:var(--max);margin:0 auto;padding:0 24px}",".wrap{max-width:var(--max);margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}")
css=css.replace(".card{background:#fff;",".card{background:var(--card);")
css=css.replace(".burger i{display:block;height:2.5px;background:var(--navy)",".burger i{display:block;height:2.5px;background:var(--fg)")
css=css.replace("input,select,textarea{font:inherit;width:100%;padding:15px 18px;border-radius:14px;border:1.5px solid #0f1f3d26;background:#fff;color:var(--navy)}","input,select,textarea{font:inherit;width:100%;padding:15px 18px;border-radius:14px;border:1.5px solid #0f1f3d26;background:#fff;color:#0F1F3D}")
css=css.replace(".btn.dark{background:var(--navy);color:#fff}.btn.dark:hover{background:var(--teal);color:var(--navy)}",".btn.dark{background:var(--navy);color:#fff}.btn.dark:hover{background:#fff;color:var(--navy)}")
css=css.replace(".nav a:hover",".nav a:hover")
css=css.replace(".pillar{border-radius:30px;",".pillar{color:#0F1F3D;border-radius:30px;")
css=css.replace(".lang{font-weight:600;",".lang{background:none;color:inherit;cursor:pointer;font-weight:600;")
css=css.replace(".rv{opacity:0;transform:translateY(22px);transition:.7s cubic-bezier(.2,.7,.2,1)}.rv.in{opacity:1;transform:none}","")
css=css.replace("@media(prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}html{scroll-behavior:auto}}","@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.btn,.card{transition:none}}")
css=css.replace(".ico{width:54px",".ico{border:1px solid #12B5A640;width:54px").replace("border-bottom:1px solid var(--line)}\n.nav","border-bottom:1px solid var(--line)}\n.nav")
css=css.replace("footer{background:var(--navy2)","footer{background:#0b1730")
css=css.replace(".flow .n{",".flow .n{color:var(--teal);").replace("flow h4","flow h4")
css=css.replace("nav{display:none;position:absolute;top:78px;inset-inline:0;background:var(--cream)","nav{display:none;position:absolute;top:78px;inset-inline:0;background:var(--bg)")
css=css.replace("body{","body{padding-block:0;",1)
css+="\n.msg{font-weight:600;background:#0F1F3D;color:#fff;border-radius:14px;padding:14px 18px}\n.lang:focus-visible,.btn:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid var(--amber);outline-offset:2px}\n"
tokens=""":root{--navy:#0F1F3D;--navy2:#0b1730;--teal:#12B5A6;--amber:#E8A33D;--slate:#5B6B82;--r:22px;--max:1180px;--bg:#F7F4EE;--fg:#0F1F3D;--card:#fff;--line:#0F1F3D1a;--hdr:#F7F4EEdd;--mut:#5B6B82}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0b1730;--fg:#F7F4EE;--card:#13264b;--line:#ffffff1f;--hdr:#0b1730dd;--mut:#9fb0c8;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0b1730;--fg:#F7F4EE;--card:#13264b;--line:#ffffff1f;--hdr:#0b1730dd;--mut:#9fb0c8;color-scheme:dark}
"""
css=css.replace("color:var(--slate)","color:var(--mut)")
ids="top pillars academy solutions process contact menu".split()
def grab(L):
    h=page(L)
    k=L["lang"]
    parts=[re.search(r"<header>.*?</footer>",h,re.S).group(0)]
    s=parts[0]
    s=s.replace(f'href="../{L["other"]}/"',f'href="#" data-go="{L["other"]}"')
    for i in ids:
        s=s.replace(f'id="{i}"',f'id="{i}-{k}"').replace(f'href="#{i}"',f'href="#{i}-{k}"').replace(f"getElementById('{i}')",f"getElementById('{i}-{k}')")
    s=re.sub(r'<form onsubmit="[^"]*"',f'<form data-k="{k}"',s)
    for n in("name","email","type","msg"):
        s=s.replace(f'name="{n}"',f'name="{n}" id="{n}-{k}"')
    s=s.replace("</form>",f'<p class="msg" hidden>{"هذا نموذج تجريبي. اربطه بقناة استقبال قبل النشر." if k=="ar" else "This is a demo form. Connect it to an inbox before launch."}</p></form>')
    s=s.replace('<header>',f'<header>',1)
    return f'<div dir="{L["dir"]}" lang="{k}" data-l="{k}"{"" if k=="ar" else " hidden"}>{s}</div>'
body=grab(T["ar"])+grab(T["en"])
body=body.replace('class="rv"','').replace("card rv","card").replace("pillar a rv","pillar a").replace("pillar s rv","pillar s").replace("sec-h rv","sec-h").replace("band rv","band")
body=re.sub(r' class="rv"','',body)
body=body.replace('<div class="rv"><div class="n"','<div><div class="n"')
body=body.replace(' style="background:#ffffff0d;border-color:#ffffff1f"',' style="background:#ffffff0d;border-color:#ffffff1f;color:#fff"')
body=body.replace('class="n" style="background:var(--cream)"','class="n" style="background:var(--bg)"')
html=f'''<title>Deraya Website</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* layout: navy hero + cream sections, two-sided (Academy / Solutions) bilingual one-pager */
{tokens}
{css}
</style>
{body}
<script>
document.querySelectorAll('[data-go]').forEach(function(a){{a.addEventListener('click',function(e){{e.preventDefault();var t=a.getAttribute('data-go');document.querySelectorAll('[data-l]').forEach(function(d){{d.hidden=d.getAttribute('data-l')!==t}});window.scrollTo(0,0)}})}});
document.querySelectorAll('form[data-k]').forEach(function(f){{f.addEventListener('submit',function(e){{e.preventDefault();f.querySelector('.msg').hidden=false}})}});
document.querySelectorAll('nav a').forEach(function(a){{a.addEventListener('click',function(){{a.closest('nav').classList.remove('open')}})}});
</script>'''
open("artifact.html","w").write(html)
print(len(html))
