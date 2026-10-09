import cv2, numpy as np, json
S=6
im=cv2.imread("logo_official.png")[...,::-1].astype(float); white=np.array([255.,255,255])
nonw=1-im.min(axis=2)/255; n,lab,st,_=cv2.connectedComponentsWithStats((nonw>.06).astype(np.uint8),connectivity=8)
hx=lambda c:"#%02X%02X%02X"%tuple(int(round(v)) for v in c)
def ink(i):
    m=cv2.erode((lab==i).astype(np.uint8),np.ones((3,3),np.uint8))>0
    return np.median(im[m],axis=0) if m.any() else np.median(im[lab==i],axis=0)
def trace(i,eps=1.6):
    x,y,w,h,_=st[i]; p=5; x0,y0,x1,y1=max(0,x-p),max(0,y-p),min(1080,x+w+p),min(1080,y+h+p)
    c=ink(i); d=white-c; reg=im[y0:y1,x0:x1]; a=np.clip(((white-reg)@d)/(d@d),0,1)
    own=(lab[y0:y1,x0:x1]==i)|(cv2.dilate((lab[y0:y1,x0:x1]==i).astype(np.uint8),np.ones((5,5),np.uint8))>0)&(a>.02)
    a=a*own; up=cv2.resize(a,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC); up=cv2.GaussianBlur(up,(0,0),S*.28)
    cn,_=cv2.findContours((up>.5).astype(np.uint8),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE); cn=[k for k in cn if cv2.contourArea(k)>S*S*1.5]
    dd=" ".join("M"+" L".join(f"{p[0][0]/S+x0:.2f},{p[0][1]/S+y0:.2f}" for p in cv2.approxPolyDP(k,eps,True))+"Z" for k in cn)
    return dd,hx(c),(float(x),float(y),float(x+w),float(y+h))
pieces={}
for i in range(1,n):
    if st[i,4]<12: continue
    pieces[i]=trace(i)
out={"dots":[],"chev":[],"divider":None,"clin":[],"stat":[],"res":[]}
for i,(d,col,bb) in pieces.items():
    x,y,w,h,a=st[i]
    if col=="#D4BD9E":
        cx,cy=(bb[0]+bb[2])/2,(bb[1]+bb[3])/2; out["dots"].append({"cx":cx,"cy":cy,"r":max(bb[2]-bb[0],bb[3]-bb[1])/2,"color":col})
    elif w>=80 and h>=30: out["chev"].append({"d":d,"color":col,"bb":bb})
    elif w<=6 and h>100: out["divider"]={"d":d,"color":col,"bb":bb}
    elif col=="#B19063": out["res"].append({"d":d,"color":col,"x0":bb[0],"x1":bb[2],"y0":bb[1],"y1":bb[3]})
    else: (out["clin"] if col=="#003520" else out["stat"]).append({"d":d,"color":col,"x0":bb[0],"x1":bb[2],"y0":bb[1],"y1":bb[3]})
out["dots"].sort(key=lambda d:d["cy"]); out["chev"].sort(key=lambda c:c["bb"][1])
for k in ("clin","stat","res"): out[k].sort(key=lambda l:l["x0"])
# merge i-dot with its stem (x-overlap), keep order
def merge(ls):
    r=[]
    for l in ls:
        if r and l["x0"]<r[-1]["x1"]-1: r[-1]["d"]+=" "+l["d"]; r[-1]["x1"]=max(r[-1]["x1"],l["x1"]); r[-1]["y0"]=min(r[-1]["y0"],l["y0"])
        else: r.append(dict(l))
    return r
out["clin"]=merge(out["clin"])
allx=[p["bb"][0] for p in out["chev"]]+[d["cx"]-d["r"] for d in out["dots"]]; ally=[d["cy"]-d["r"] for d in out["dots"]]+[p["bb"][1] for p in out["chev"]]
out["mark"]={"x0":min(allx),"x1":max(p["bb"][2] for p in out["chev"]),"y0":min(ally),"y1":max(p["bb"][3] for p in out["chev"])}
out["word"]={"x0":min(l["x0"] for l in out["clin"]),"x1":max(l["x1"] for l in out["stat"]),"y0":min(l["y0"] for l in out["clin"]+out["stat"]),"y1":max(l["y1"] for l in out["res"])}
json.dump(out,open("logo_vec.json","w"))
print("dots",len(out["dots"]),"chev",len(out["chev"]),"Clin",len(out["clin"]),"Stat",len(out["stat"]),"RESEARCH",len(out["res"]),"divider",bool(out["divider"]))
print("mark",out["mark"],"word",out["word"]); print("colors:",{k:[x["color"] for x in out[k]][:2] for k in ("chev","clin","stat","res")})
