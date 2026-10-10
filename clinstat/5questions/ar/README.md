# ClinStat – "5 questions…" Arabic version (20 s, 1080x1920, 30 fps, no voice-over)

- `clinstat_5questions_ar.mp4` – final video. Same timeline, score and sound design as the English version, mirrored for right-to-left reading (headline badge, question numbers, icon and footer curve moved to the right/mirrored; official logo unchanged and centred).
- `template.html` -> `build.py` -> `index.html`; `capture.py test|events|full`; `music.py` (same score, writes `score_raw.wav`); `audit.py` (exact Arabic copy, safe zone, overlap, page errors).
- Font: Cairo (SIL Open Font License), bundled as `Cairo.ttf`.
- Rebuild: `python3 build.py && python3 music.py && ffmpeg -y -i score_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=7 -ar 44100 audio.wav && python3 capture.py full clinstat_5questions_ar.mp4 audio.wav`
- Copy is Modern Standard Arabic and matches `clinstat/ads-campaign/arabic-ad-copy.md`. **Needs native-speaker review before use.**
- "50+ papers / h-index of 5+" is carried over from the English video's claim; confirm it is accurate for the team before running ads.
