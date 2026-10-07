import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
S = 2
PW, PH = 760, 900
CX = 380
_OX = _OY = 0
_W, _H = PW, PH
def set_region(ox, oy, w, h):
    global _OX,_OY,_W,_H
    _OX,_OY,_W,_H = ox,oy,w,h

def _mask(draw_fn, blur=0):
    m = Image.new("L", (_W*S, _H*S), 0); d = ImageDraw.Draw(m)
    draw_fn(d); 
    if blur: m = m.filter(ImageFilter.GaussianBlur(blur*S))
    return m

def paint(canvas, mask, color, alpha=1.0, clip=None):
    if clip is not None: mask = ImageChops.multiply(mask, clip)
    layer = Image.new("RGBA", canvas.size, tuple(color)+(255,))
    if alpha != 1.0: mask = mask.point(lambda v: int(v*alpha))
    canvas.paste(layer, (0,0), mask)

def grad_paint(canvas, mask, c0, c1, axis="y", box=None):
    W, H = canvas.size
    x0,y0,x1,y1 = box or (0,0,W,H)
    g = np.zeros((H,W,3), np.float32)
    if axis=="y": t = np.clip((np.arange(H)[:,None]-y0)/max(1,y1-y0),0,1)*np.ones((1,W))
    else: t = np.clip((np.arange(W)[None,:]-x0)/max(1,x1-x0),0,1)*np.ones((H,1))
    for k in range(3): g[...,k] = c0[k]*(1-t)+c1[k]*t
    layer = Image.fromarray(g.astype(np.uint8)).convert("RGBA")
    canvas.paste(layer, (0,0), mask)

def E(d, b, **k): d.ellipse([(b[0]-_OX)*S,(b[1]-_OY)*S,(b[2]-_OX)*S,(b[3]-_OY)*S], **k)
def P(d, pts, **k): d.polygon([((x-_OX)*S,(y-_OY)*S) for x,y in pts], **k)
def R(d, b, r, **k): d.rounded_rectangle([(b[0]-_OX)*S,(b[1]-_OY)*S,(b[2]-_OX)*S,(b[3]-_OY)*S], r*S, **k)
def L(d, pts, w, **k): d.line([((x-_OX)*S,(y-_OY)*S) for x,y in pts], width=max(1,int(w*S)), **k)

SKIN=(206,158,124); SKIN_L=(228,184,150); SKIN_D=(170,120,90); SKIN_DD=(135,92,68)
HAIR=(28,22,20); HAIR_L=(70,56,48)
GREEN=(0,53,34); GREEN_L=(10,80,52); GOLD=(182,150,104); CREAM=(247,242,236)

def build_base():
    c = Image.new("RGBA", (PW*S, PH*S), (0,0,0,0))
    # ---- torso: dark-green blazer
    torso = _mask(lambda d: P(d, [(40,900),(62,700),(96,630),(170,574),(260,538),(300,520),(460,520),(500,538),(590,574),(664,630),(698,700),(720,900)], fill=255), 2.2)
    grad_paint(c, torso, GREEN_L, (0,38,25), "y", (0,520*S,0,900*S))
    # shoulder highlight / side shading
    paint(c, _mask(lambda d: P(d, [(40,900),(70,640),(120,600),(110,900)], fill=255), 18), (0,25,16), .55)
    paint(c, _mask(lambda d: P(d, [(720,900),(690,640),(640,600),(650,900)], fill=255), 18), (0,25,16), .55)
    # shirt V
    paint(c, _mask(lambda d: P(d, [(300,520),(460,520),(380,740)], fill=255), 1.0), CREAM)
    paint(c, _mask(lambda d: P(d, [(318,524),(360,524),(380,610),(345,560)], fill=255), 6), (205,198,188), .6)
    # collar open shirt
    paint(c, _mask(lambda d: P(d, [(300,520),(345,515),(370,600),(330,585)], fill=255), 1), (236,230,222))
    paint(c, _mask(lambda d: P(d, [(460,520),(415,515),(390,600),(430,585)], fill=255), 1), (236,230,222))
    # lapels
    for pts in ([(300,520),(380,740),(270,660),(215,560)], [(460,520),(380,740),(490,660),(545,560)]):
        paint(c, _mask(lambda d, p=pts: P(d, p, fill=255), 1.2), (0,30,20))
    # pocket square (gold)
    paint(c, _mask(lambda d: P(d, [(530,690),(590,675),(595,700),(535,712)], fill=255), 1), GOLD)
    paint(c, _mask(lambda d: P(d, [(540,684),(560,680),(565,692),(545,696)], fill=255), 1), (210,184,140))
    # ---- neck
    neck = _mask(lambda d: R(d, (318,430,442,590), 40, fill=255), 2)
    grad_paint(c, neck, SKIN, SKIN_D, "y", (0,430*S,0,590*S))
    # neck shadow under chin
    paint(c, _mask(lambda d: E(d, (300,470,460,560), fill=255), 14), SKIN_DD, .75, clip=neck)
    # ---- ears
    for ex, sgn in ((209,-1),(551,1)):
        paint(c, _mask(lambda d, ex=ex: E(d, (ex-18,305,ex+18,392), fill=255), 1.2), SKIN_D)
        paint(c, _mask(lambda d, ex=ex, sgn=sgn: E(d, (ex-8+sgn*2,325,ex+8+sgn*2,375), fill=255), 3), SKIN_DD, .5)
    # ---- head (egg: skull + jaw)
    head = _mask(lambda d: (E(d,(222,112,538,420),fill=255), E(d,(236,225,524,572),fill=255), P(d,[(226,300),(534,300),(500,500),(380,566),(260,500)],fill=255)), 1.5)
    grad_paint(c, head, SKIN_L, SKIN, "y", (0,120*S,0,560*S)); HC = head
    # side shading for volume (light from upper-left)
    paint(c, _mask(lambda d: E(d,(470,150,640,560), fill=255), 26), SKIN_D, .55, clip=HC)
    paint(c, _mask(lambda d: E(d,(130,150,260,560), fill=255), 28), SKIN_D, .35, clip=HC)
    # forehead & cheek highlights
    paint(c, _mask(lambda d: E(d,(300,150,420,240), fill=255), 24), (240,205,176), .55, clip=HC)
    paint(c, _mask(lambda d: E(d,(262,380,330,440), fill=255), 16), (228,150,128), .28, clip=HC)
    paint(c, _mask(lambda d: E(d,(430,380,498,440), fill=255), 16), (214,140,118), .22, clip=HC)
    # ---- beard (trimmed, soft edge) + stubble gradient on cheeks
    beard = _mask(lambda d: P(d,[(240,340),(246,428),(280,508),(380,556),(480,508),(514,428),(520,340),(496,414),(462,452),(430,446),(380,444),(330,446),(298,452),(264,414)], fill=255), 4.5)
    paint(c, beard, (38,30,27), .93, clip=head)
    paint(c, _mask(lambda d: P(d,[(240,340),(252,436),(292,468),(264,400)], fill=255), 14), (84,62,52), .5, clip=head)
    paint(c, _mask(lambda d: P(d,[(520,340),(508,436),(468,468),(496,400)], fill=255), 14), (84,62,52), .42, clip=head)
    # mustache
    paint(c, _mask(lambda d: P(d,[(322,452),(346,440),(380,446),(414,440),(438,452),(418,464),(380,458),(342,464)], fill=255), 3.0), (34,27,24), .95)
    # ---- hair
    def hair_shape(d):
        E(d,(222,90,538,310), fill=255)
        P(d,[(224,300),(226,230),(238,330),(250,350)], fill=255); P(d,[(536,300),(534,230),(522,330),(510,350)], fill=255)
        E(d,(262,196,498,350), fill=0)                       # forehead opening
        P(d,[(262,300),(262,240),(290,214),(330,200),(380,196),(430,200),(470,214),(498,240),(498,300)], fill=0)
    hair = _mask(hair_shape, 2.2)
    grad_paint(c, hair, HAIR_L, HAIR, "y", (0,90*S,0,260*S))
    h = Image.new("RGBA", c.size, (0,0,0,0)); hd = ImageDraw.Draw(h)
    rng = np.random.RandomState(7)
    for _ in range(160):
        x0 = rng.uniform(236,524); y0 = rng.uniform(100,200)
        L(hd, [(x0,y0),(x0+rng.uniform(-10,10)+(x0-380)*0.08,y0+rng.uniform(10,26))], 1.3, fill=(120,100,86,rng.randint(40,110)))
    h = h.filter(ImageFilter.GaussianBlur(.7*S)); h.putalpha(ImageChops.multiply(h.getchannel("A"), hair))
    c.alpha_composite(h)
    paint(c, _mask(lambda d: P(d,[(262,246),(290,220),(330,206),(380,202),(430,206),(470,220),(498,246),(474,230),(380,216),(286,230)], fill=255), 5), (70,48,36), .28, clip=head)
    # ---- nose
    paint(c, _mask(lambda d: P(d,[(366,322),(394,322),(404,400),(356,400)], fill=255), 10), SKIN_D, .35)
    paint(c, _mask(lambda d: E(d,(398,372,426,408), fill=255), 8), SKIN_D, .45)
    paint(c, _mask(lambda d: E(d,(340,386,420,418), fill=255), 5), (222,172,138))
    paint(c, _mask(lambda d: E(d,(352,388,408,404), fill=255), 4), (238,196,164), .8)
    for nx in (356,396): paint(c, _mask(lambda d, nx=nx: E(d,(nx,404,nx+16,414), fill=255), 1.5), SKIN_DD, .85)
    # ---- eye sockets, brows
    for cx in (312,448):
        paint(c, _mask(lambda d, cx=cx: E(d,(cx-40,300,cx+40,350), fill=255), 9), SKIN_D, .38)
    return c

def make_presenter():
    base = build_base()
    return base

def _brow(canvas, cx, sgn, lift):
    m = _mask(lambda d: P(d,[(cx-sgn*-0,0)]*0 or [(cx-44*sgn*-1*-1 if False else cx-44, 292-lift),(cx-10, 280-lift-1),(cx+40, 288-lift+1),(cx+42,298-lift),(cx+10,291-lift),(cx-40,302-lift)], fill=255), 1.4)
    paint(canvas, m, HAIR)

def frame(base, i, t, mouth, emph, vis):
    """base: prebuilt body; mouth 0..1 openness; emph 0..1 eyebrow raise; vis 0..1 round/wide viseme"""
    set_region(250,262,260,320)
    c = base.crop((250*S,262*S,510*S,582*S))
    # eyebrows (left brow slopes up toward temple, right mirrored)
    lift = 5*emph
    for cx, sg in ((312,1),(448,-1)):
        pts = [(cx-42,296-lift),(cx-14,282-lift),(cx+24,283-lift+(0)),(cx+44,292-lift),(cx+14,290-lift),(cx-16,291-lift),(cx-40,302-lift)] if sg==1 else [(cx-44,292-lift),(cx-24,283-lift),(cx+14,282-lift),(cx+42,296-lift),(cx+40,302-lift),(cx+16,291-lift),(cx-14,290-lift)]
        paint(c, _mask(lambda d, p=pts: P(d, p, fill=255), 1.2), (36,28,24))
    # eyes
    blink = (i % 118) in (0,1,2) or (i % 203) in (0,1)
    gx = math.sin(t*0.7)*3; gy = math.sin(t*0.5)*1.5
    for cx in (312,448):
        if blink:
            paint(c, _mask(lambda d, cx=cx: L(d,[(cx-24,330),(cx,334),(cx+24,330)], 3, fill=255), .6), (50,34,28))
        else:
            paint(c, _mask(lambda d, cx=cx: E(d,(cx-27,314,cx+27,346), fill=255), .5), (245,240,235))
            paint(c, _mask(lambda d, cx=cx: E(d,(cx-27,314,cx+27,326), fill=255), 3), (160,120,100), .5)   # upper lid shadow
            ix, iy = cx+gx, 330+gy
            paint(c, _mask(lambda d, ix=ix, iy=iy: E(d,(ix-13,iy-13,ix+13,iy+13), fill=255), .4), (92,58,36))
            paint(c, _mask(lambda d, ix=ix, iy=iy: E(d,(ix-8,iy-8,ix+8,iy+8), fill=255), .4), (46,28,20))
            paint(c, _mask(lambda d, ix=ix, iy=iy: E(d,(ix-4,iy-9,ix+3,iy-3), fill=255), .3), (255,255,255), .9)
            # lids
            paint(c, _mask(lambda d, cx=cx: L(d,[(cx-28,330),(cx-14,316),(cx+14,315),(cx+28,330)], 3, fill=255), .7), (60,42,34))
            paint(c, _mask(lambda d, cx=cx: L(d,[(cx-24,338),(cx,346),(cx+24,338)], 1.6, fill=255), .7), (150,100,82), .7)
    # mouth
    my = 484; w = (60 + 18*mouth) * (1 - 0.18*vis) 
    oh = 2 + mouth*34*(0.8+0.4*vis)
    # cavity
    paint(c, _mask(lambda d: E(d,(CX-w/2, my-oh/2, CX+w/2, my+oh/2), fill=255), .5), (70,22,26))
    if oh > 9:
        paint(c, _mask(lambda d: R(d,(CX-w/2+8, my-oh/2+1, CX+w/2-8, my-oh/2+min(11,oh*.4)), 4, fill=255), .4), (240,236,230))
    if oh > 22:
        paint(c, _mask(lambda d: E(d,(CX-w*0.28, my+oh*0.05, CX+w*0.28, my+oh/2-1), fill=255), 1.5), (176,84,88))
    # lips
    up = [(CX-w/2-2,my),(CX-w*0.28,my-oh/2-7),(CX-6,my-oh/2-3),(CX,my-oh/2-1),(CX+6,my-oh/2-3),(CX+w*0.28,my-oh/2-7),(CX+w/2+2,my),(CX+w*0.3,my-oh/2+1),(CX,my-oh/2+3),(CX-w*0.3,my-oh/2+1)]
    paint(c, _mask(lambda d: P(d, up, fill=255), 1.0), (176,104,98))
    lo = [(CX-w/2,my),(CX-w*0.3,my+oh/2-1),(CX,my+oh/2+1),(CX+w*0.3,my+oh/2-1),(CX+w/2,my),(CX+w*0.28,my+oh/2+11),(CX,my+oh/2+14),(CX-w*0.28,my+oh/2+11)]
    paint(c, _mask(lambda d: P(d, lo, fill=255), 1.0), (190,118,110))
    paint(c, _mask(lambda d: E(d,(CX-w*0.2,my+oh/2+3,CX+w*0.2,my+oh/2+9), fill=255), 2), (214,150,140), .8)
    # beard shadow under lip + smile creases
    paint(c, _mask(lambda d: E(d,(CX-w*0.3,my+oh/2+14,CX+w*0.3,my+oh/2+24), fill=255), 5), (28,22,20), .5)
    set_region(0,0,PW,PH)
    out = base.copy(); out.paste(c, (250*S, 262*S))
    return out
