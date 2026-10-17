"""Original sound for the 15 s motion reel (numpy only, no samples). Events are synced to motion.html. python3 audio.py -> audio.wav"""
import wave, numpy as np
SR = 44100; D = 15.0; N = int(SR * D); t = np.arange(N) / SR; rs = np.random.RandomState(7)
mid = lambda m: 440.0 * 2 ** ((m - 69) / 12); ss = lambda x: (lambda y: y * y * (3 - 2 * y))(np.clip(x, 0, 1))
L = np.zeros(N); R = np.zeros(N)
def put(x, at, vol=1.0, pan=.5):
    s = int(at * SR); e = min(N, s + len(x))
    if s < N and e > s: L[s:e] += x[:e - s] * vol * (1 - pan) * 1.4; R[s:e] += x[:e - s] * vol * pan * 1.4
def noise(d, lo, hi):
    x = rs.randn(int(d * SR)); X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def pluck(m, d=.9, amp=.12):
    k = np.arange(int(d * SR)) / SR; f = mid(m); return (np.sin(2 * np.pi * f * k) + .35 * np.sin(2 * np.pi * 2 * f * k) + .12 * np.sin(2 * np.pi * 3 * f * k)) * np.exp(-k * 5) * np.minimum(k / .004, 1) * amp
# pad: C, Am, F, G (3.75 s each)
prog = [[48, 55, 59, 64], [45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59]]
for ci in range(5):
    a = ci * 3.75; env = ss((t - (a - .5)) / 1.4) * (1 - ss((t - (a + 3.75 - .3)) / 1.2))
    for k, m in enumerate(prog[ci % 4]):
        for side, det, arr in ((0, -3, L), (1, 3, R)):
            f = mid(m) * 2 ** (det / 1200); arr += env * (np.sin(2 * np.pi * f * t) + .22 * np.sin(2 * np.pi * 2 * f * t)) * (.05 if k else .09)
# groove: soft kick on beats from 4.2 s, plucks on eighths from 0.6
for i in range(int(D / .25)):
    at = i * .25 + .6
    if at > D - 1: break
    ch = prog[int(at // 3.75) % 4]; m = ch[[1, 2, 3, 2][i % 4]] + 12
    put(pluck(m, .8, .06 if at < 4.2 else .09), at, 1, .3 + .4 * ((i * 5) % 7) / 6)
for i in range(int(D / .5)):
    at = i * .5
    if 4.2 <= at <= 14.0:
        k = np.arange(int(.3 * SR)) / SR; x = np.sin(2 * np.pi * np.cumsum(48 + 90 * np.exp(-k * 28)) / SR) * np.exp(-k * 9) * .5; put(x, at, 1, .5)
        if i % 2: hh = noise(.08, 6000, 12000) * np.exp(-np.arange(int(.08 * SR)) / SR * 60) * .05; put(hh, at, 1, .6)
# events
for at in [1.95, 2.23, 2.51, 2.79, 3.07]:      # ice dropping into the cup
    k = np.arange(int(.5 * SR)) / SR; x = (noise(.5, 2500, 9000) * np.exp(-k * 22) * .35 + np.sin(2 * np.pi * (1400 + at * 20) * k) * np.exp(-k * 26) * .06); put(x, at + .2, 1, .5)
put(noise(2.7, 500, 2500) * ss(np.arange(int(2.7 * SR)) / SR / .5) * (1 - ss(np.arange(int(2.7 * SR)) / SR / 2.7)) * .16, 5.0, 1, .5)   # pour
for at in [.3, 4.85, 9.3, 12.5]:               # headline slams
    k = np.arange(int(.4 * SR)) / SR; put(np.sin(2 * np.pi * (60 + 80 * np.exp(-k * 30)) * k) * np.exp(-k * 8) * .45 + noise(.4, 200, 1800) * np.exp(-k * 20) * .12, at, 1, .5)
for at in [4.2, 9.0, 11.8]:                    # whooshes (wipes)
    k = np.arange(int(.9 * SR)) / SR; w = noise(.9, 400, 6000) * np.sin(np.pi * np.clip(k / .9, 0, 1)) ** 1.5 * .25; put(w, at - .1, 1, .5)
for at in [9.8, 10.08, 10.36]:                  # cups pop in
    k = np.arange(int(.25 * SR)) / SR; put(np.sin(2 * np.pi * (500 + 700 * k * 4) * k) * np.exp(-k * 18) * .3, at + .35, 1, .5)
for j, m in enumerate([72, 76, 79, 84]):         # end chime
    put(pluck(m, 1.6, .14), 13.8 + j * .12, 1, .5)
fade = ss(t / .4) * ss((D - t) / .6); L *= fade; R *= fade
m = max(np.abs(L).max(), np.abs(R).max()); st = np.stack([L, R], 1) / m * .85
with wave.open("audio.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())
print("audio ok")
