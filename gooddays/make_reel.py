"""Good Days at Trio Cafe: old look collapses, new look builds. Pure PIL/numpy + ffmpeg."""
import numpy as np, subprocess, os, sys, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps
W, H, FPS, D = 1080, 1920, 30, 9.2
HERE = os.path.dirname(os.path.abspath(__file__)); A = HERE + "/assets/"
rs = np.random.RandomState(7)
import math
FB = "/usr/share/fonts/opentype/inter/Inter-Black.otf"; FM = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
def cover(p):
    im = Image.open(p).convert("RGB"); s = H/im.height; im = im.resize((round(im.width*s), H), Image.LANCZOS)
    x = (im.width-W)//2; return im.crop((x, 0, x+W, H))
OLD, NEW = cover(A+"old.jpg"), cover(A+"new.jpg")
def zoom(im, s, dx=0, dy=0):
    w, h = W/s, H/s; x = min(W-w, max(0, (W-w)/2+dx)); y = min(H-h, max(0, (H-h)/2+dy))
    return im.resize((W, H), Image.BICUBIC, box=(x, y, x+w, y+h))
def ss(x): x = min(1, max(0, x)); return x*x*(3-2*x)
def eob(x, c=1.5):
    x = min(1, max(0, x)); return 1+(c+1)*(x-1)**3+c*(x-1)**2

from PIL import ImageEnhance
T_COL, T_BUILD, T_ON, T_END = 1.7, 3.05, 5.7, 8.1
POLY = [(x*1.5-180, y*1.5) for x, y in [(150, 340), (812, 255), (836, 1195), (836, 1250), (298, 1250), (298, 850), (190, 850), (190, 600)]]
mk = Image.new("L", (W, H), 0); ImageDraw.Draw(mk).polygon(POLY, fill=255); MASK = mk.filter(ImageFilter.GaussianBlur(2.5))
def with_alpha(im): o = im.convert("RGBA"); o.putalpha(MASK); return o
def fill_hole(im):                                                  # empty lot behind the kiosk: soft night gradient + faint blueprint grid
    a = np.asarray(im).astype(np.float32); m = (np.asarray(mk.filter(ImageFilter.GaussianBlur(10))).astype(np.float32)/255)[..., None]
    y = np.linspace(0, 1, H)[:, None, None]; x = np.linspace(-1, 1, W)[None, :, None]
    top = np.array([14, 24, 52], np.float32); mid = np.array([30, 40, 68], np.float32); bot = np.array([58, 62, 78], np.float32)
    g = np.where(y < .5, top+(mid-top)*(y/.5), mid+(bot-mid)*((y-.5)/.5))*(1-.2*x*x)
    gl = np.zeros((H, W, 1), np.float32); gl[::64, :] = 1; gl[:, ::64] = 1; gl = np.asarray(Image.fromarray((gl[..., 0]*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8))).astype(np.float32)[..., None]/255
    g = g+gl*20+(np.random.RandomState(1).randn(H, W, 1)*1.5)
    return Image.fromarray(np.clip(a*(1-m)+g*m, 0, 255).astype(np.uint8))
PLATE_OLD, PLATE_NEW = fill_hole(OLD), fill_hole(NEW)
OLDA, NEWA = with_alpha(OLD), with_alpha(NEW)
TW, TH = 60, 64; COLS, ROWS = W//TW, H//TH+1
bx0, by0, bx1, by1 = MASK.getbbox()
def tiles(img):
    out = {}
    for r in range(ROWS):
        for c in range(COLS):
            t = img.crop((c*TW, r*TH, c*TW+TW, r*TH+TH))
            if t.getchannel("A").getextrema()[1] > 8: out[(r, c)] = t
    return out
OT, NT = tiles(OLDA), tiles(NEWA)
keys = sorted(set(OT) | set(NT))
def ny(r): return min(1, max(0, (r*TH+TH/2-by0)/(by1-by0)))
c_delay = {k: .5*rs.rand()+.5*ny(k[0]) for k in keys}                 # roof/sign first, base last
c_vx = {k: (rs.rand()-.5)*220 for k in keys}; c_vy = {k: -rs.rand()*140 for k in keys}; c_rot = {k: (rs.rand()-.5)*480 for k in keys}
b_delay = {k: .7*(1-ny(k[0]))+.3*rs.rand() for k in keys}             # builds from the floor up
b_dx = {k: (rs.rand()-.5)*260 for k in keys}; b_rot = {k: (rs.rand()-.5)*120 for k in keys}; b_dy = {k: 500+rs.rand()*700 for k in keys}
B_DUR = 0.62
NP = 150; pxy = np.stack([bx0+rs.rand(NP)*(bx1-bx0), by0+rs.rand(NP)*(by1-by0)*.9], 1); pv = (rs.rand(NP, 2)-.5)*np.array([90, 50]); pt = T_COL+rs.rand(NP)*1.4; ps = 3+rs.rand(NP)*10
GLOW = ImageEnhance.Brightness(NEW.filter(ImageFilter.GaussianBlur(30))).enhance(1.5)
def paste_tile(cv, tile, x, y, ang, a=1.0, bright=0, dim=1.0):
    t = tile
    if dim < 1: al = t.getchannel("A"); t = ImageEnhance.Brightness(t.convert("RGB")).enhance(dim).convert("RGBA"); t.putalpha(al)
    if bright: rgb = Image.blend(t.convert("RGB"), Image.new("RGB", t.size, (255, 244, 220)), min(1, bright)); al = t.getchannel("A"); t = rgb.convert("RGBA"); t.putalpha(al)
    if abs(ang) > .3: t = t.rotate(ang, Image.BILINEAR, expand=True)
    if a < 1: t.putalpha(t.getchannel("A").point(lambda v: int(v*a)))
    cv.paste(t, (int(x-t.width/2), int(y-t.height/2)), t)
def dust(cv, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(NP):
        k = t-pt[i]
        if k < 0 or k > 2.2: continue
        a = int(80*np.sin(np.pi*min(1, k/2.2))); x, y = pxy[i]+pv[i]*k+np.array([0, -30*k]); r = ps[i]*(1+k)
        d.ellipse((x-r, y-r, x+r, y+r), fill=(200, 192, 180, a))
    ov = ov.filter(ImageFilter.GaussianBlur(6)); cv.paste(ov, (0, 0), ov)
FONT_B = ImageFont.truetype(FB, 120); FONT_S = ImageFont.truetype(FM, 44); FONT_T = ImageFont.truetype(FM, 38)
LOGO = ImageOps.invert(Image.open(A+"logo.jpg").convert("L"))
bb = LOGO.point(lambda v: 255 if v > 40 else 0).getbbox(); LOGO = LOGO.crop(bb); LOGO = LOGO.resize((760, round(LOGO.height*760/LOGO.width)), Image.LANCZOS)
def text_c(cv, s, font, y, a, fill=(255, 255, 255), dy=0, spacing=0):
    if a <= 0: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    w = d.textlength(s, font=font)+spacing*(len(s)-1); x = (W-w)/2; yy = y+dy
    for ch in s:
        d.text((x+3, yy+4), ch, font=font, fill=(0, 0, 0, int(120*a))); d.text((x, yy), ch, font=font, fill=fill+(int(255*a),)); x += d.textlength(ch, font=font)+spacing
    cv.paste(ov, (0, 0), ov)
def shake(t, amp): return amp*np.sin(t*91)*np.cos(t*57), amp*np.sin(t*73+1)
def frame(t):
    if t >= T_ON+.05:                                                # 4) hold on the finished new look
        z = 1+.06*((t-T_ON)/(D-T_ON)); cv = zoom(NEW, z)
    else:
        mix = ss((t-T_BUILD)/(T_ON-T_BUILD))
        po = Image.blend(OLD, PLATE_OLD, ss((t-T_COL)/.35)); pn = Image.blend(PLATE_NEW, NEW, ss((t-(T_ON-.6))/.6))
        cv = Image.blend(po, pn, mix)
        dim = .62+.38*ss((t-T_ON)/.5) if t > T_BUILD else 1.0
        if dim < 1: cv = ImageEnhance.Brightness(cv).enhance(dim)
        if t < T_BUILD+.2:                                           # 1+2) old kiosk stands, vibrates, then collapses; scenery stays
            tt = t-T_COL
            for k in sorted(OT, key=lambda k: k[0]):
                r, c = k; x0 = c*TW+TW/2; y0 = r*TH+TH/2; kk = tt-c_delay[k]*1.05
                if kk < 0:
                    amp = 5*ss((tt+.55)/.55)*(1-ss((tt-.05)/.1)) if tt > -.55 else 0       # whole kiosk trembles before it goes
                    j = 3*ss((kk+.2)/.2)
                    paste_tile(cv, OT[k], x0+math.sin(t*85)*amp+math.sin(t*90+c*1.7)*j, y0+math.cos(t*77)*amp*.7+math.cos(t*70+r)*j, 0); continue
                y = y0+c_vy[k]*kk+.5*3600*kk*kk
                if y > H+260: continue
                paste_tile(cv, OT[k], x0+c_vx[k]*kk, y, c_rot[k]*kk, 1-ss((kk-.6)/.45))
            dust(cv, t)
        if t >= T_BUILD-.1:                                          # 3) new kiosk builds from the floor up
            tb = t-T_BUILD
            for k in sorted(NT, key=lambda k: -k[0]):
                r, c = k; kk = (tb-b_delay[k]*1.45)/B_DUR
                if kk <= 0: continue
                x0 = c*TW+TW/2; y0 = r*TH+TH/2; p = eob(kk, 1.2); q = 1-p
                land = max(0, tb-b_delay[k]*1.45-B_DUR); fl = .45*np.exp(-land*9) if kk >= 1 else 0
                paste_tile(cv, NT[k], x0+b_dx[k]*q, y0+b_dy[k]*q, b_rot[k]*q, min(1, kk*3), fl, dim)
        if T_ON-.05 < t < T_ON+1.1:
            g = np.sin(np.pi*min(1, (t-(T_ON-.05))/1.15))**1.4
            cv = ImageChops.screen(cv, ImageEnhance.Brightness(GLOW).enhance(.55*g))
    if t < T_COL: text_c(cv, "BEFORE", FONT_S, 150, ss((t-.15)/.35)*(1-ss((t-(T_COL-.3))/.3)), spacing=14)
    if t > T_ON+.15 and t < T_END+.3:
        a = ss((t-(T_ON+.35))/.4)*(1-ss((t-(T_END-.15))/.4))
        text_c(cv, "THE NEW LOOK", FONT_B, 1470, a, dy=(1-ss((t-(T_ON+.35))/.5))*60)
        text_c(cv, "GOOD DAYS  ·  AT TRIO CAFE", FONT_S, 1625, a*ss((t-(T_ON+.6))/.4), spacing=6)
    if t > T_END-.2:
        u = ss((t-(T_END-.2))/.6); end = Image.new("RGB", (W, H), (8, 8, 8)); end.paste(LOGO, ((W-LOGO.width)//2, 720), LOGO)
        cv = Image.blend(cv, end, u); text_c(cv, "Come see the new look", FONT_T, 1180, ss((t-(T_END+.5))/.5), fill=(220, 220, 220))
    return cv

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for s in sys.argv[2:]: frame(float(s)).save(f"{HERE}/frames/s_{float(s):.2f}.jpg", quality=88)
    else:
        n = int(D*FPS); ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-", "-i", sys.argv[2],
            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", sys.argv[3]], stdin=subprocess.PIPE)
        import io
        for i in range(n):
            b = io.BytesIO(); frame(i/FPS).save(b, "JPEG", quality=95); ff.stdin.write(b.getvalue())
            if i % 30 == 0: print(i, n, flush=True)
        ff.stdin.close(); ff.wait(); print("done")
