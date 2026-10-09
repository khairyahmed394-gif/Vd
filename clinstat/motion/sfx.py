import numpy as np, json, wave, subprocess
SR = 44100; DUR = 22.0; rng = np.random.RandomState(4)
def tt(d): return np.arange(int(d*SR))/SR
def env(n, a=.005, d=.2, curve=3.0): t = np.arange(n)/SR; return np.minimum(t/a, 1)*np.exp(-t*curve/d)
def lp(x, f):  # one-pole lowpass
    a = np.exp(-2*np.pi*f/SR); y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x): s = (1-a)*v + a*s; y[i] = s
    return y
def hp(x, f): return x-lp(x, f)
def noise(d): return rng.randn(int(d*SR))
def impact(v): t = tt(.9); f = 120*np.exp(-t*5)+38; x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*4.5); x += hp(lp(noise(.9), 2500), 300)*np.exp(-t*14)*.5; return x*.9*v
def tick(v): t = tt(.07); return (hp(noise(.07), 2500)*np.exp(-t*70)*.5 + np.sin(2*np.pi*2400*t)*np.exp(-t*90)*.35)*v
def whoosh(v):
    d = 1.0; n = noise(d); t = tt(d)
    out = np.zeros_like(n); s = 0.0
    for i in range(len(n)):
        f = 300+3800*np.sin(np.pi*min(1, t[i]/d))**1.5; a = np.exp(-2*np.pi*f/SR); s = (1-a)*n[i]+a*s; out[i] = s
    e = np.sin(np.pi*np.clip(t/d, 0, 1))**2; return hp(out, 200)*e*3.0*v
def pop(v, k=0): f0 = [880, 988, 1175, 784, 880, 1047][k % 6]; t = tt(.35); f = f0*(1+1.2*np.exp(-t*40)); return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*12)*.55 + np.sin(2*np.pi*np.cumsum(f*2)/SR)*np.exp(-t*20)*.12)*v
def thud(v, k=0): t = tt(.4); f = 110*np.exp(-t*14)+52; x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*.8; p = np.sin(2*np.pi*[1568, 1760, 1976, 1396, 1568, 2093][k % 6]*t)*np.exp(-t*7)*.14; return (x+p)*v
def chime(v, k=0): f0 = [523.25, 659.25, 783.99][k % 3]; t = tt(1.4); x = sum(a*np.sin(2*np.pi*f0*r*t)*np.exp(-t*dc) for r, a, dc in [(1, .5, 2.2), (2.01, .22, 3.2), (3.97, .1, 5), (5.4, .05, 7)]); return x*v
def bubble(v): t = tt(.25); f = 500*(1+2.5*t*4); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*16)*.4*v
def swell(v): t = tt(1.4); n = hp(lp(noise(1.4), 3500), 800); return n*np.sin(np.pi*np.clip(t/1.4, 0, 1))**2*.5*v
def draw(v): t = tt(1.2); f = 400+900*t/1.2; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*np.clip(t/1.2, 0, 1))**2*.12*v
def shimmer(v):
    t = tt(1.2); x = np.zeros_like(t)
    for i in range(14): a = int(i*.07*SR); tt2 = t[:len(t)-a]; x[a:] += np.sin(2*np.pi*(1800+i*230)*tt2)*np.exp(-tt2*10)*.07
    return x*v
def sparkle(v):
    t = tt(1.3); x = np.zeros_like(t)
    for i, f in enumerate([2093, 2637, 3136, 3951, 4186]): a = int(i*.09*SR); tt2 = t[:len(t)-a]; x[a:] += np.sin(2*np.pi*f*tt2)*np.exp(-tt2*5)*.12
    return x*v
G = {"impact": lambda v, k: impact(v), "tick": lambda v, k: tick(v), "whoosh": lambda v, k: whoosh(v), "pop": pop, "thud": thud, "chime": chime, "bubble": lambda v, k: bubble(v), "swell": lambda v, k: swell(v), "draw": lambda v, k: draw(v), "shimmer": lambda v, k: shimmer(v), "sparkle": lambda v, k: sparkle(v)}
ev = json.load(open("events.json")); L = np.zeros(int(DUR*SR)+SR*2); R = L.copy()
for i, e in enumerate(ev):
    x = G[e["k"]](e["v"], int(e.get("k2",0)))
    st = int(max(0, e["t"])*SR); pan = np.sin(i*2.3)*.35
    L[st:st+len(x)] += x*(1-pan)*.9; R[st:st+len(x)] += x*(1+pan)*.9
out = np.stack([L, R], 1)[:int(DUR*SR)]; out = np.clip(out/ max(1, np.abs(out).max()*1.0), -1, 1)*0.9
w = wave.open("sfx.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close(); print("sfx ok", out.shape)
