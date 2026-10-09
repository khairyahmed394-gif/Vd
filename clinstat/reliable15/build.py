s=open("template.html").read().replace("__LOGO__",open("logo_vec.json").read()).replace("__SCENES__","\n".join(open(f).read() for f in ["scenes_a.js","scenes_b.js","scenes_c.js"]))
open("index.html","w").write(s)
