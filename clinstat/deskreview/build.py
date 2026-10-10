s=open("template.html").read().replace("__LOGO__",open("logo_vec.json").read()); open("index.html","w").write(s)
