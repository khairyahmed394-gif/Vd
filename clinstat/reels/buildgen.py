s=open("reelgen.html").read().replace("__LOGO__",open("logo_vec.json").read()); open("index_gen.html","w").write(s)
