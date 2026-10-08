import json
s = open("template.html").read()
s = s.replace("__SEA__", json.load(open("map_paths.json"))["sea"]).replace("__LOGO__", open("logo_vector.json").read())
open("index.html", "w").write(s)
