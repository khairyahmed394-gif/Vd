# ClinStat – Gulf Arabic version (23 s, 1080x1920, 30 fps, no voice-over)

- `clinstat_gulf_ar.mp4` – final video. Same five scenes, timing, score and sound design as the English Gulf video, mirrored for right-to-left reading: headlines right-aligned, the accelerated timeline and monthly chart run right to left, transition wipes sweep right to left, footer curve mirrored. The Gulf map is **not** mirrored (geography stays correct); city labels are in Arabic. Official logo unchanged.
- `scenes.js` + `core.js` + `head.html` + `tail.html` -> `build.py` -> `index.html`; `capture.py test|events|full`; `music.py`; `audit.py` (Arabic text present, safe margins, page errors).
- Font: Cairo (SIL Open Font License), bundled as `Cairo.ttf`. Letter-spacing is forced to 0 so Arabic letters stay joined.
- Rebuild: `python3 build.py && python3 capture.py events && python3 music.py && ffmpeg -y -i score_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=7 -ar 44100 audio.wav && python3 capture.py full clinstat_gulf_ar.mp4 audio.wav`
- Copy is Modern Standard Arabic; **needs native-speaker review before use.** The tagline "الدليل. الرؤية. الأثر." translates the English "Evidence. Insight. Impact."
- The chart and map are illustrative, not real data. The on-screen disclaimers are kept in Arabic.
