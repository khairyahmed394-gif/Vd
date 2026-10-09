s=open("template.html").read().replace("__LOGO__",open("logo_vector.json").read()); open("index.html","w").write(s)
