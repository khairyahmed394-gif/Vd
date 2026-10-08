import cv2, numpy as np, json, sys
B = "../brand/"
def poly_path(c, scale=1.0, eps=0.7, ox=0, oy=0):
    c = cv2.approxPolyDP(c, eps, True); pts = c[:, 0, :].astype(float)/scale
    return "M" + " L".join(f"{x+ox:.2f},{y+oy:.2f}" for x, y in pts) + "Z"
def alpha_from(img, bg, ink):
    bg = np.array(bg, float); ink = np.array(ink, float); d = bg-ink
    a = ((bg-img.astype(float)) @ d)/(d @ d); return np.clip(a, 0, 1)
# ---------------------------------------------------------------- MARK (master logo, white bg)
im = cv2.imread(B+"49ad48b2-image.png"); rgb = im[..., ::-1].astype(float)
nonwhite = np.clip((250-rgb.min(axis=2))/40, 0, 1)
mask = (cv2.GaussianBlur((nonwhite*255).astype(np.uint8), (0, 0), 0.8) > 110).astype(np.uint8)
n, lab, st, cen = cv2.connectedComponentsWithStats(mask)
pieces = []
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] < 300: continue
    m = (lab == i).astype(np.uint8)
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); c = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c); area = cv2.contourArea(c)
    (cx, cy), r = cv2.minEnclosingCircle(c); circ = area/(np.pi*r*r)
    er = cv2.erode(m, np.ones((5, 5), np.uint8)).astype(bool)
    col = lambda sl: np.median(rgb[sl][er[sl]], axis=0) if er[sl].any() else np.median(rgb[er], axis=0)
    top = col((slice(y, y+max(3, h//4)), slice(x, x+w))); bot = col((slice(y+h-max(3, h//4), y+h), slice(x, x+w)))
    hx = lambda c: "#%02X%02X%02X" % tuple(int(v) for v in c)
    p = {"c0": hx(top), "c1": hx(bot), "bbox": [x, y, w, h]}
    if circ > 0.9 and abs(w-h) < 0.15*max(w, h): p.update(type="circle", cx=float(cx), cy=float(cy), r=float(r))
    else: p.update(type="poly", d=poly_path(c, eps=2.6), npts=len(cv2.approxPolyDP(c, 2.6, True)))
    pieces.append(p)
pieces.sort(key=lambda p: p["bbox"][1])
dots = [p for p in pieces if p["type"] == "circle"]; chev = [p for p in pieces if p["type"] == "poly"]
print("mark pieces: dots", len(dots), "chevrons", len(chev), [p.get("npts") for p in chev])
allx0 = min(p["bbox"][0] for p in pieces); allx1 = max(p["bbox"][0]+p["bbox"][2] for p in pieces); ally0 = min(p["bbox"][1] for p in pieces); ally1 = max(p["bbox"][1]+p["bbox"][3] for p in pieces)
mark = {"dots": dots, "chevrons": chev, "x0": allx0, "x1": allx1, "y0": ally0, "y1": ally1}
# ---------------------------------------------------------------- WORDMARK (post image)
S = 8
src = cv2.imread(B+"6f193b89-image.png"); X0, Y0 = 520, 60
reg = src[Y0:Y0+130, X0:X0+380]; bgc = np.median(src[20:40, 300:340].reshape(-1, 3), axis=0)[::-1]
up = cv2.resize(reg, None, fx=S, fy=S, interpolation=cv2.INTER_LANCZOS4)[..., ::-1]
dark = np.array([2, 56, 33]); gold = np.array([182, 150, 104])
def letters(win, ink):  # win = (x0,y0,x1,y1) in source px relative to region
    a = alpha_from(up, bgc, ink)
    m = np.zeros_like(a); x0, y0, x1, y1 = [int(v*S) for v in win]; m[y0:y1, x0:x1] = a[y0:y1, x0:x1]
    m = cv2.GaussianBlur(m, (0, 0), S*0.35); b = (m > 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(b); comps = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 40*S*S*0.02: continue
        comps.append([i, st[i, 0], st[i, 0]+st[i, 2]])
    comps.sort(key=lambda c: c[1]); groups = []
    for c in comps:  # merge by x-overlap (i dot + stem)
        if groups and c[1] < groups[-1][2]-0.3*(min(c[2]-c[1], groups[-1][2]-groups[-1][1])): groups[-1][0].append(c[0]); groups[-1][2] = max(groups[-1][2], c[2])
        else: groups.append([[c[0]], c[1], c[2]])
    out = []
    for ids, gx0, gx1 in groups:
        gm = np.isin(lab, ids).astype(np.uint8)
        cnts, hier = cv2.findContours(gm, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        d = " ".join(poly_path(c, scale=S, eps=2.2, ox=X0, oy=Y0) for c in cnts if cv2.contourArea(c) > 30)
        ys, xs = np.where(gm > 0); out.append({"d": d, "x0": X0+xs.min()/S, "x1": X0+xs.max()/S, "y0": Y0+ys.min()/S, "y1": Y0+ys.max()/S})
    return out
clin = letters((20, 8, 372, 80), dark); res = letters((20, 86, 372, 124), gold)
print("ClinStat letters", len(clin), "RESEARCH letters", len(res))
# divider = thin tall component left of the text
dv = letters((0, 8, 20, 124), dark)
hexc = lambda c: "#%02X%02X%02X" % tuple(int(v) for v in c)
wm = {"clin": clin, "res": res, "divider": dv, "clinColor": hexc(dark), "resColor": hexc(gold), "bbox": [min(l["x0"] for l in clin), min(l["y0"] for l in clin), max(l["x1"] for l in clin), max(l["y1"] for l in res)]}
json.dump({"mark": mark, "wm": wm}, open("logo_vector.json", "w"))
print("mark bbox", allx0, ally0, allx1, ally1, "| wm bbox", wm["bbox"], "| colors", mark["chevrons"][0]["c0"], mark["chevrons"][1]["c0"], mark["chevrons"][2]["c0"])
