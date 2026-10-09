import json
h=open("head.html").read().replace("__LOGO__",open("logo_vec.json").read()).replace("__MAP__",open("map.json").read())
core=open("core.js").read();sc=open("scenes.js").read();tl=open("tail.html").read()
k=sc.index("// ------------------------------------------------------------------ S1")
pre,body=sc[:k],sc[k:]
tl=tl.replace("function build(){","function build(){buildScenes();")
open("index.html","w").write(h+core+pre+"function buildScenes(){\n"+body+"\n}\n"+tl)
