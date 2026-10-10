"""Synth sound design: crack + rumble collapse, rising build thumps, lights-on chime, light beat. Original, no samples."""
import numpy as np, wave
SR = 44100; D = 9.2; N = int(SR*D); rs = np.random.RandomState(3)
T_COL, T_BUILD, T_ON = 1.7, 3.05, 5.7
L = np.zeros(N); R = np.zeros(N)
def put(x, at, vol=1, pan=.5):
    s = int(at*SR); e = min(N, s+len(x))
    if s < N and e > s: L[s:e] += x[:e-s]*vol*(1-pan)*1.4; R[s:e] += x[:e-s]*vol*pan*1.4
def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tone(f, d, dec, parts=((1, 1),)):
    k = np.arange(int(d*SR))/SR; return sum(a*np.sin(2*np.pi*f*h*k) for h, a in parts)*np.exp(-k*dec)*np.minimum(k/.003, 1)
def kick(v=1): k = np.arange(int(.32*SR))/SR; return np.sin(2*np.pi*(48*k+ 90*(1-np.exp(-k*30))/30))*np.exp(-k*9)*v
def hat(v=1): n = int(.06*SR); return bp(rs.randn(n), 6000, 16000)*np.exp(-np.arange(n)/SR*70)*v*.5
def thud(f, v=1): k = np.arange(int(.45*SR))/SR; return (np.sin(2*np.pi*f*k*(1+.5*np.exp(-k*20)))+.4*bp(rs.randn(len(k)), 60, 400))*np.exp(-k*11)*v
# 1) pre-collapse creak/crack
put(bp(rs.randn(int(.5*SR)), 800, 4000)*np.exp(-np.arange(int(.5*SR))/SR*7)*.5, T_COL-.35, .5, .4)
put(bp(rs.randn(int(.25*SR)), 200, 6000)*np.exp(-np.arange(int(.25*SR))/SR*18), T_COL, 1.0)
# 2) rumble + debris
n = int(1.9*SR); k = np.arange(n)/SR; env = np.minimum(k/.2, 1)*np.exp(-k*1.3)
put(bp(rs.randn(n), 25, 220)*env*2.2, T_COL, .9)
put(bp(rs.randn(n), 400, 3000)*env*np.exp(-k*1.5)*.35, T_COL, .5)
for i in range(46):
    at = T_COL+.15+rs.rand()**.8*1.5; put(thud(rs.choice([55, 70, 90, 120]), .25+.3*rs.rand()), at, .5, .2+.6*rs.rand())
# 3) riser into build, thumps climbing, lights-on hit
n = int((T_ON-T_BUILD+.1)*SR); k = np.arange(n)/SR; x = bp(rs.randn(n), 300, 9000)*(k/k[-1])**2.2*.35; put(x, T_BUILD-.05, .5)
for i in range(18):
    at = T_BUILD+.05+i*(T_ON-T_BUILD-.2)/18; put(thud(70+i*5, .55), at, .6, .5+.2*np.sin(i))
    put(tone(440*2**((i%8)/12*2+.0)*1.0, .18, 18, ((1, 1), (2, .3)))*.4, at+.02, .12, .5)
for k_, f in enumerate([523, 659, 784, 1047, 1319, 1568]):     # lights-on chime arpeggio
    put(tone(f, 1.8, 2.6, ((1, 1), (2.76, .3), (5.4, .1)))*.5, T_ON+k_*.07, .22, .3+.08*k_)
put(kick(1.2), T_ON, 1.0); put(bp(rs.randn(int(1.2*SR)), 1000, 12000)*np.exp(-np.arange(int(1.2*SR))/SR*3)*.4, T_ON, .3)
# 4) beat 118 bpm from lights-on
bpm = 118; b = 60/bpm; t0 = T_ON+b
for i in range(int((D-t0)/b)+1):
    at = t0+i*b; put(kick(.9), at, .8)
    put(hat(.8), at+b/2, .4, .65)
    if i % 2 == 1: put(bp(rs.randn(int(.15*SR)), 1500, 7000)*np.exp(-np.arange(int(.15*SR))/SR*25)*.7, at, .35)   # clap
    m = [0, 0, 3, 5][i % 4]; put(tone(55*2**(m/12), b*.9, 4, ((1, 1), (2, .25))), at, .35, .5)
pad = [(220, 262, 330), (196, 247, 294)]
for j, (ts_, te_) in enumerate([(T_ON, T_ON+3.6)]):
    for f in (220, 262, 330, 392):
        n = int((te_-ts_)*SR); k = np.arange(n)/SR; w = np.sin(2*np.pi*f*k)*np.minimum(k/.8, 1)*np.minimum((k[-1]-k)/1.2, 1)*.05; put(w, ts_, 1, .5)
# master: fade out, soft clip
fo = np.minimum(1, (D-np.arange(N)/SR)/.8); L *= fo; R *= fo
m = max(np.abs(L).max(), np.abs(R).max()); L = np.tanh(L/m*1.4)*.9; R = np.tanh(R/m*1.4)*.9
pcm = (np.stack([L, R], 1)*32767).astype("<i2")
with wave.open("/home/user/Vd/gooddays/audio.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("audio ok")
