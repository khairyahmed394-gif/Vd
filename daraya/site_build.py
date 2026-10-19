import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"site")
def mark(dark=False,h=44):
    f="#fff" if dark else "#0F1F3D"
    return f'''<svg viewBox="0 0 132 120" height="{h}" aria-hidden="true"><g fill="#12B5A6"><rect x="2" y="30" width="10" height="10" rx="2" opacity=".55"/><rect x="14" y="18" width="10" height="10" rx="2"/><rect x="14" y="42" width="10" height="10" rx="2" opacity=".8"/><rect x="2" y="54" width="10" height="10" rx="2"/></g>
<path d="M34 12h34a48 48 0 0 1 0 96H34z" fill="{f}"/><path d="M50 36l42 24-42 24z" fill="#12B5A6"/></svg>'''
I={ # icons (feather-like paths)
"web":'<path d="M3 5h18v14H3zM3 9h18M7 7h.01M10 7h.01"/>',"mob":'<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
"py":'<path d="M4 17l6-5-6-5M12 19h8"/>',"ai":'<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M19 5l-3 3M8 16l-3 3"/>',
"sec":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',"cloud":'<path d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1 0 9z"/>',
"erp":'<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 17h7M17.5 14v7"/>',
"chart":'<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',"bot":'<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M9 14h.01M15 14h.01"/>',
"chat":'<path d="M4 5h16v11H9l-5 4z"/>',"proj":'<path d="M3 7l9-4 9 4-9 4zM3 12l9 4 9-4M3 17l9 4 9-4"/>',"team":'<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 3-6 6-6s6 2.5 6 6M15 14c3 0 6 2 6 5"/>',
"link":'<path d="M10 14a4 4 0 0 0 5.6 0l3-3a4 4 0 0 0-5.6-5.6l-1 1M14 10a4 4 0 0 0-5.6 0l-3 3a4 4 0 0 0 5.6 5.6l1-1"/>',"globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>'}
ico=lambda k:f'<div class="ico"><svg viewBox="0 0 24 24">{I[k]}</svg></div>'
T={
"ar":dict(lang="ar",dir="rtl",other="en",otherlbl="EN",title="درايه — معرفة تُبنى | تعليم برمجي وحلول تقنية في الخليج",
 desc="درايه: أكاديمية تعليم برمجة وحلول تقنية للشركات في الخليج. تعلّم المهارات، ابنِ الحلول، ونفّذ معنا.",
 nav=[("#pillars","من نحن"),("#academy","أكاديمية درايه"),("#solutions","درايه سوليوشنز"),("#process","كيف نعمل"),("#contact","تواصل")],
 cta_nav="احجز استشارة",eyebrow="تعليم · مهارات · حلول تقنية",
 h1='من الفكرة<br>إلى <em>المنتج.</em>',lead="درايه تجمع بين التعليم البرمجي وتنفيذ الحلول التقنية في الخليج. تتعلّم من مشاريع حقيقية، ولما تحتاج تنفيذ، فريقنا يبني معك.",
 b1="ابدأ التعلّم",b2="احجز استشارة",steps=["LEARN","BUILD","IMPLEMENT"],
 chips=[("مشاريع","عملية"),("محتوى","بالعربي"),("تنفيذ","للشركات")],
 p_eye="من نحن",p_h="نظام واحد، وجهان",p_p="نعلّم الناس يبنون، ونبني مع الشركات. كل وجه يغذّي الآخر: المتدرب يتعلم على مشاريع حقيقية، والعميل يستفيد من فريق يعرف يعلّم ويُنفّذ.",
 a_tag="ACADEMY",a_h="أكاديمية درايه",a_p="تعلّم مهاراتك بالتطبيق.",a_li=["مسارات برمجة من الصفر للاحتراف","مشاريع عملية وإشراف مختص","شهادة وتوجيه مهني"],a_btn="استكشف المسارات",
 s_tag="SOLUTIONS",s_h="درايه سوليوشنز",s_p="من الفكرة إلى المنتج.",s_li=["مواقع وتطبيقات وأنظمة مخصصة","لوحات بيانات وأتمتة وذكاء اصطناعي","تدريب فريقك على ما بنيناه"],s_btn="ابدأ مشروعك",
 ac_eye="أكاديمية درايه",ac_h="مسارات تعليمية بتبني مهارة حقيقية",ac_p="كل مسار ينتهي بمشروع تقدر تعرضه. المحتوى مبدئي ونعدّله مع كل دفعة.",
 tracks=[("web","تطوير الويب","HTML وCSS وJavaScript وReact وواجهات خلفية، لحد نشر مشروع كامل."),("mob","تطبيقات الموبايل","بناء تطبيقات Android وiOS بتقنيات حديثة."),("py","Python وتحليل البيانات","من الأساسيات للتحليل والتقارير والأتمتة."),("ai","الذكاء الاصطناعي","أدوات الذكاء الاصطناعي في بناء حلول عملية."),("sec","الأمن السيبراني","أساسيات حماية الأنظمة والتطبيقات."),("cloud","السحابة وDevOps","النشر والبنية السحابية وأتمتة التشغيل.")],
 so_eye="درايه سوليوشنز",so_h="حلول تقنية تُنفَّذ بجودة وسرعة",so_p="نبني ما تحتاجه شركتك، ونسلّمه بتوثيق وتدريب لفريقك.",
 sols=[("web","مواقع ومتاجر إلكترونية","واجهات عربية RTL سريعة ومحسّنة لمحركات البحث."),("mob","تطبيقات موبايل","تطبيقات تخدم عملاءك وفريقك الميداني."),("erp","أنظمة داخلية","أنظمة إدارة مخصصة تربط عملياتك."),("chart","لوحات بيانات","تقارير حية تدعم قرارك."),("bot","أتمتة وذكاء اصطناعي","تقليل المهام اليدوية وتسريع الخدمة."),("chat","استشارات تقنية","تقييم واختيار الحل الأنسب قبل ما تبدأ.")],
 pr_eye="كيف نعمل",pr_h="من الفهم إلى الإطلاق، ثم التدريب",pr_p="مسار واضح من أول اجتماع إلى فريق يشغّل الحل بنفسه.",
 flow=[("فهم","نحدد الهدف والمتطلبات."),("تصميم","نرسم الحل والتجربة."),("بناء","نطوّر على مراحل قصيرة."),("إطلاق","نختبر وننشر."),("تدريب","نعلّم فريقك يشغّله.")],
 w_eye="لماذا درايه",w_h="الفرق اللي يحسّه عميلنا ومتدربنا",
 why=[("proj","التعلّم بالمشاريع","ما نعلّم نظري فقط، كل مسار فيه تطبيق."),("globe","محتوى عربي بروح خليجية","لغة قريبة وأمثلة من السوق المحلي."),("link","من التعلم للتنفيذ","نفس الفريق يعلّم ويبني، فالمعرفة متصلة بالواقع."),("team","مرافقة ودعم","متابعة ما بعد التسليم أو انتهاء الدورة.")],
 band_h="جاهز تبدأ؟",band_p="اكتب لنا هدفك (تعلّم مهارة أو تنفيذ مشروع) ونرد عليك بخطوة واضحة.",
 f_name="الاسم",f_mail="البريد الإلكتروني",f_type=["أريد التعلّم","أريد تنفيذ مشروع","استفسار آخر"],f_msg="رسالتك",f_send="أرسل",
 foot_p="معرفة تُبنى. تعليم برمجي وحلول تقنية في الخليج.",foot_h1="روابط",foot_h2="الأقسام",rights="جميع الحقوق محفوظة",tag="معرفة تُبنى",
 tr_pr="[\"احفظ\"]"),
"en":dict(lang="en",dir="ltr",other="ar",otherlbl="العربية",title="Deraya — Knowledge Builds | Tech education & solutions in the Gulf",
 desc="Deraya: a coding academy and technology solutions studio in the Gulf. Learn the skills, build the solutions, implement with us.",
 nav=[("#pillars","About"),("#academy","Deraya Academy"),("#solutions","Deraya Solutions"),("#process","How we work"),("#contact","Contact")],
 cta_nav="Book a consultation",eyebrow="Education · Skills · Technology Solutions",
 h1='From idea<br>to <em>product.</em>',lead="Deraya pairs coding education with technology delivery in the Gulf. You learn on real projects, and when you need something built, our team builds it with you.",
 b1="Start learning",b2="Book a consultation",steps=["LEARN","BUILD","IMPLEMENT"],
 chips=[("Hands-on","projects"),("Arabic-first","content"),("Delivery","for business")],
 p_eye="About",p_h="One system, two sides",p_p="We teach people to build, and we build with companies. Each side feeds the other: learners work on real projects, and clients get a team that can both teach and deliver.",
 a_tag="ACADEMY",a_h="Deraya Academy",a_p="Learn your skills by doing.",a_li=["Coding tracks from zero to pro","Hands-on projects with expert review","Certificate and career guidance"],a_btn="Explore tracks",
 s_tag="SOLUTIONS",s_h="Deraya Solutions",s_p="From idea to product.",s_li=["Custom websites, apps and systems","Dashboards, automation and AI","Training for your team on what we build"],s_btn="Start your project",
 ac_eye="Deraya Academy",ac_h="Learning tracks that build real skill",ac_p="Every track ends with a project you can show. Content is preliminary and refined with each cohort.",
 tracks=[("web","Web Development","HTML, CSS, JavaScript, React and backends, through to a deployed project."),("mob","Mobile Apps","Build Android and iOS apps with modern tools."),("py","Python & Data","From fundamentals to analysis, reporting and automation."),("ai","Artificial Intelligence","Use AI tools to build practical solutions."),("sec","Cybersecurity","Fundamentals of protecting systems and applications."),("cloud","Cloud & DevOps","Deployment, cloud infrastructure and operations automation.")],
 so_eye="Deraya Solutions",so_h="Technology solutions, delivered well and fast",so_p="We build what your company needs and hand it over with documentation and team training.",
 sols=[("web","Websites & e-commerce","Fast, SEO-ready Arabic RTL and bilingual interfaces."),("mob","Mobile apps","Apps that serve your customers and field teams."),("erp","Internal systems","Custom management systems that connect your operations."),("chart","Dashboards","Live reports that support better decisions."),("bot","Automation & AI","Cut manual work and speed up service."),("chat","Technical consulting","Assess and choose the right solution before you start.")],
 pr_eye="How we work",pr_h="From understanding to launch, then training",pr_p="A clear path from the first meeting to a team that runs the solution on its own.",
 flow=[("Understand","We define the goal and requirements."),("Design","We shape the solution and experience."),("Build","We develop in short iterations."),("Launch","We test and deploy."),("Train","We teach your team to run it.")],
 w_eye="Why Deraya",w_h="The difference our clients and learners feel",
 why=[("proj","Learning by projects","Not theory only. Every track has hands-on work."),("globe","Arabic content, Gulf spirit","Natural language and examples from the local market."),("link","From learning to delivery","The same team teaches and builds, so knowledge stays real."),("team","Support after the handover","Follow-up after delivery or after the course ends.")],
 band_h="Ready to start?",band_p="Tell us your goal, learn a skill or deliver a project, and we will reply with a clear next step.",
 f_name="Name",f_mail="Email",f_type=["I want to learn","I want a project built","Something else"],f_msg="Your message",f_send="Send",
 foot_p="Knowledge builds. Coding education and technology solutions in the Gulf.",foot_h1="Links",foot_h2="Sections",rights="All rights reserved",tag="Knowledge builds",tr_pr="")}
def page(t):
    L=t
    nav="".join(f'<li><a href="{h}">{n}</a></li>' for h,n in L["nav"])
    pill=lambda cls,tag,h,p,li,btn,href:f'<div class="pillar {cls} rv"><span class="tag">{tag}</span><h3>{h}</h3><p>{p}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul><a class="btn dark" href="{href}">{btn}</a>{mark(False,230).replace("<svg","<svg class=\'deco\'")}</div>'
    tracks="".join(f'<div class="card rv">{ico(k)}<h3>{n}</h3><p>{d}</p></div>' for k,n,d in L["tracks"])
    sols="".join(f'<div class="card rv" style="background:#ffffff0d;border-color:#ffffff1f">{ico(k)}<h3>{n}</h3><p style="color:#b7c3d6">{d}</p></div>' for k,n,d in L["sols"])
    flow="".join(f'<div class="rv"><div class="n">{i}</div><h4>{n}</h4><p>{d}</p></div>' for i,(n,d) in enumerate(L["flow"],1))
    why="".join(f'<div class="card rv">{ico(k)}<div><h3>{n}</h3><p>{d}</p></div></div>' for k,n,d in L["why"])
    chips="".join(f'<span class="chip"><b>{a}</b> {b}</span>' for a,b in L["chips"])
    steps="".join(f"<span>{s}</span>" for s in L["steps"])
    opts="".join(f"<option>{o}</option>" for o in L["f_type"])
    code='<span class="cm">// deraya.js</span>\n<span class="kw">const</span> skills = <span class="kw">await</span> <span class="kw">learn</span>(<span class="st">"web"</span>);\n<span class="kw">const</span> product = <span class="kw">build</span>(idea, skills);\n<span class="kw">return</span> <span class="kw">implement</span>(product); <span class="cm">// ✓ live</span>'
    return f'''<!doctype html><html lang="{L["lang"]}" dir="{L["dir"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{L["title"]}</title><meta name="description" content="{L["desc"]}"><meta property="og:title" content="{L["title"]}"><meta property="og:description" content="{L["desc"]}">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="alternate" hreflang="{L["other"]}" href="../{L["other"]}/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/style.css"></head><body>
<header><div class="wrap nav"><a class="brand" href="#top">{mark(False,44)}<div><b>{"دراية" if L["lang"]=="ar" else "Deraya"}</b><small>{"DERAYA" if L["lang"]=="ar" else "KNOWLEDGE BUILDS"}</small></div></a>
<nav id="menu"><ul>{nav}</ul></nav><div class="nav-r"><a class="lang" href="../{L["other"]}/">{L["otherlbl"]}</a><a class="btn amber" href="#contact">{L["cta_nav"]}</a><button class="burger" aria-label="menu" onclick="document.getElementById('menu').classList.toggle('open')"><i></i><i></i><i></i></button></div></div></header>
<main id="top"><div class="hero"><div class="wrap hero-g"><div><span class="eyebrow">{L["eyebrow"]}</span><h1>{L["h1"]}</h1><p class="lead">{L["lead"]}</p>
<div class="cta"><a class="btn amber" href="#academy">{L["b1"]}</a><a class="btn ghost" href="#contact">{L["b2"]}</a></div><div class="steps">{steps}</div></div>
<div><div class="codecard"><div class="bar"><i></i><i></i><i></i></div><pre>{code}</pre></div><div class="chips">{chips}</div></div></div></div>
<section id="pillars"><div class="wrap"><div class="sec-h rv"><span class="eyebrow">{L["p_eye"]}</span><h2>{L["p_h"]}</h2><p>{L["p_p"]}</p></div>
<div class="pillars">{pill("a",L["a_tag"],L["a_h"],L["a_p"],L["a_li"],L["a_btn"],"#academy")}{pill("s",L["s_tag"],L["s_h"],L["s_p"],L["s_li"],L["s_btn"],"#contact")}</div></div></section>
<section id="academy" style="padding-top:20px"><div class="wrap"><div class="sec-h rv"><span class="eyebrow">{L["ac_eye"]}</span><h2>{L["ac_h"]}</h2><p>{L["ac_p"]}</p></div><div class="grid3">{tracks}</div></div></section>
<section id="solutions" class="dark"><div class="wrap"><div class="sec-h rv"><span class="eyebrow">{L["so_eye"]}</span><h2>{L["so_h"]}</h2><p>{L["so_p"]}</p></div><div class="grid3">{sols}</div></div></section>
<section id="process"><div class="wrap"><div class="sec-h rv"><span class="eyebrow">{L["pr_eye"]}</span><h2>{L["pr_h"]}</h2><p>{L["pr_p"]}</p></div>
<div class="flow" style="color:var(--navy)">{flow.replace('class="n"','class="n" style="background:var(--cream)"').replace('<p>','<p style="color:var(--slate)">')}</div></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="sec-h rv"><span class="eyebrow">{L["w_eye"]}</span><h2>{L["w_h"]}</h2></div><div class="why">{why}</div></div></section>
<section id="contact" style="padding-top:20px"><div class="wrap"><div class="band rv"><div><h2>{L["band_h"]}</h2><p>{L["band_p"]}</p></div>
<form onsubmit="event.preventDefault();var f=this;location.href='mailto:?subject='+encodeURIComponent(f.type.value)+'&body='+encodeURIComponent(f.name.value+'\\n'+f.email.value+'\\n\\n'+f.msg.value)"><input name="name" placeholder="{L["f_name"]}" required><input name="email" type="email" placeholder="{L["f_mail"]}" required><select name="type">{opts}</select><textarea name="msg" rows="3" placeholder="{L["f_msg"]}"></textarea><button class="btn dark" type="submit">{L["f_send"]}</button></form></div></div></section></main>
<footer><div class="wrap"><div class="f-g"><div><div class="brand" style="margin-bottom:16px">{mark(True,40)}<div><b style="color:#fff">{"دراية" if L["lang"]=="ar" else "Deraya"}</b></div></div><p>{L["foot_p"]}</p></div>
<div><h5>{L["foot_h2"]}</h5><ul>{nav}</ul></div><div><h5>{L["foot_h1"]}</h5><ul><li><a href="../{L["other"]}/">{L["otherlbl"]}</a></li><li><a href="#contact">{L["cta_nav"]}</a></li></ul></div></div>
<div class="copy"><span>© 2026 Deraya. {L["rights"]}</span><span>{L["tag"]} · KNOWLEDGE BUILDS</span></div></div></footer>
<script>var io=new IntersectionObserver(function(e){{e.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target)}}}})}},{{threshold:.12}});document.querySelectorAll('.rv').forEach(function(n){{io.observe(n)}});document.querySelectorAll('nav a').forEach(function(a){{a.onclick=function(){{document.getElementById('menu').classList.remove('open')}}}})</script></body></html>'''
for k in("ar","en"): open(f"{OUT}/{k}/index.html","w").write(page(T[k]))
open(f"{OUT}/index.html","w").write('<!doctype html><meta charset=utf-8><meta http-equiv=refresh content="0;url=/ar/"><link rel=canonical href="/ar/"><script>location.replace("/ar/")</script>')
open(f"{OUT}/assets/favicon.svg","w").write(mark(False,64).replace("<svg",'<svg xmlns="http://www.w3.org/2000/svg" width="64"',1))
open(f"{OUT}/vercel.json","w").write('{"cleanUrls":true,"redirects":[{"source":"/","destination":"/ar","permanent":false}]}')
