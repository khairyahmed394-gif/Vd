import os, numpy as np, cv2
from PIL import Image
os.environ["LAMA_MODEL"]="/tmp/claude-0/big-lama.pt"
from simple_lama_inpainting import SimpleLama
L=SimpleLama()
LOGO=[425,1245,660,1392]
R={ "p1":[[222,992,862,1220],LOGO],
    "p2":[[138,1075,942,1175],LOGO],
    "p3":[[0,85,925,325],LOGO],
    "p5":[[165,100,915,340],LOGO],
    "p6":[[0,90,745,425],LOGO],
    "p8":[[0,925,845,1195],LOGO] }
os.makedirs("clean",exist_ok=True)
for k,rects in R.items():
    im=Image.open(f"src/{k}.jpg").convert("RGB"); m=np.zeros((im.height,im.width),np.uint8)
    for x0,y0,x1,y1 in rects: m[y0:y1,x0:x1]=255
    Image.fromarray(m).save(f"clean/{k}_mask.png")
    out=L(im,Image.fromarray(m)); out.save(f"clean/{k}.png"); print(k,"ok",flush=True)
