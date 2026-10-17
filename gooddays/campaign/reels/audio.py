"""Original warm sound bed for the photo reels (numpy only, no samples, no voice). python3 audio.py <reel> -> audio/<reel>.wav"""
import sys, os, wave, numpy as np
from cfg import REELS
SR = 44100
def mid(m): return 440.0 * 2 ** ((m - 69) / 12)
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def make(name):
    C = REELS[name]; D = C["D"]; N = int(SR * D); t = np.arange(N) / SR; rs = np.random.RandomState(sum(map(ord, name)))
    L = np.zeros(N); R = np.zeros(N)
    prog = [[48, 55, 59, 64, 67], [45, 52, 57, 60, 64], [41, 48, 55, 57, 64], [43, 50, 55, 59, 62]]   # Cmaj7 Am7 Fmaj7 G6, slow
    cl = 3.75
    for ci in range(int(np.ceil(D / cl)) + 1):
        a = ci * cl; notes = prog[ci % 4]; env = ss((t - (a - .8)) / 1.6) * (1 - ss((t - (a + cl - .4)) / 1.2))
        for k, m in enumerate(notes):
            for side, det, arr in ((0, -3, L), (1, 3, R)):
                f = mid(m) * 2 ** (det / 1200); lfo = 1 + .1 * np.sin(2 * np.pi * (.06 + .011 * k) * t + k + side)
                arr += env * lfo * (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t) + .08 * np.sin(2 * np.pi * 3 * f * t)) * (.05 if k else .1)
    # airy plucks every 0.75 s from the chord tones
    for i in range(int(D / .75)):
        at = i * .75 + .2
        if at > D - 1: break
        m = prog[int(at // cl) % 4][[2, 3, 4, 3][i % 4]] + 12; k = np.arange(int(1.2 * SR)) / SR
        x = (np.sin(2 * np.pi * mid(m) * k) + .3 * np.sin(2 * np.pi * 2 * mid(m) * k)) * np.exp(-k * 4.5) * np.minimum(k / .004, 1) * .07
        s = int(at * SR); e = min(N, s + len(x)); pan = .3 + .4 * ((i * 7) % 5) / 4
        L[s:e] += x[:e - s] * (1 - pan) * 1.4; R[s:e] += x[:e - s] * pan * 1.4
    # soft ice/cup tick on each cut and a gentle "air" bed
    X = rs.randn(N); F = np.fft.rfft(X); fr = np.fft.rfftfreq(N, 1 / SR); F[(fr < 2500) | (fr > 7500)] = 0; air = np.fft.irfft(F, N) * .0035
    L += air; R += air
    for sh in C["shots"][1:]:
        at = sh[1] - .05; k = np.arange(int(.5 * SR)) / SR; x = rs.randn(len(k)) * np.exp(-k * 28); x = np.convolve(x, np.ones(4) / 4, "same") * .1 + np.sin(2 * np.pi * 1760 * k) * np.exp(-k * 22) * .03
        s = int(at * SR); e = min(N, s + len(x)); L[s:e] += x[:e - s]; R[s:e] += x[:e - s]
    # end swell
    e0 = C["end"]["t"]; k = ss((t - e0) / .9) * (1 - ss((t - (D - .2)) / .2)); L += k * np.sin(2 * np.pi * mid(60) * t) * .02; R += k * np.sin(2 * np.pi * mid(67) * t) * .02
    fade = ss(t / .6) * ss((D - t) / .8); L *= fade; R *= fade
    m = max(np.abs(L).max(), np.abs(R).max(), 1e-6); st = np.stack([L, R], 1) / m * .8
    os.makedirs("audio", exist_ok=True)
    with wave.open(f"audio/{name}.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())
if __name__ == "__main__": make(sys.argv[1])
