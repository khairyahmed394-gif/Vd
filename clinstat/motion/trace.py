import cv2, numpy as np, json
img = cv2.imread("brand/assets/map_gulf.png"); h, w = img.shape[:2]; print(w, h)
b, g, r = [img[..., i].astype(int) for i in range(3)]
light = (r > 205) & (g > 200) & (b > 185)
m = (light*255).astype(np.uint8)
# sea: large light regions (close small gaps cut by gold route lines)
sea = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, stats, _ = cv2.connectedComponentsWithStats(sea)
big = np.zeros_like(sea)
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] > 2500: big[lab == i] = 255
big = cv2.GaussianBlur(big, (0, 0), 2.0); big = (big > 127).astype(np.uint8)*255
def to_path(cnts, scale=1.5, eps=1.1, close=True):
    out = []
    for c in cnts:
        c = cv2.approxPolyDP(c, eps, close)
        if len(c) < 3: continue
        pts = c[:, 0, :]*scale
        out.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + ("Z" if close else ""))
    return " ".join(out)
cnts, hier = cv2.findContours(big, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
sea_path = to_path([c for c in cnts if cv2.contourArea(c) > 60])
# borders: bright thin stuff on land (not sea)
land_light = cv2.bitwise_and(m, cv2.bitwise_not(cv2.dilate(big, np.ones((5, 5), np.uint8))))
land_light = cv2.morphologyEx(land_light, cv2.MORPH_OPEN, np.ones((1, 1), np.uint8))
n2, lab2, st2, _ = cv2.connectedComponentsWithStats(land_light)
keep = np.zeros_like(land_light)
for i in range(1, n2):
    if st2[i, cv2.CC_STAT_AREA] > 40: keep[lab2 == i] = 255
sk = cv2.ximgproc.thinning(keep) if hasattr(cv2, "ximgproc") else keep
cb, _ = cv2.findContours(keep, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
border_path = to_path([c for c in cb if cv2.arcLength(c, True) > 50], eps=1.0)
print(len(sea_path), len(border_path))
json.dump({"sea": sea_path, "borders": border_path}, open("mg/map_paths.json", "w"))
# preview
prev = np.zeros((int(h*1.5), int(w*1.5), 3), np.uint8); prev[:] = (43, 59, 18)
cv2.imwrite("mg/prev_mask.png", cv2.resize(big, (w, h)))
