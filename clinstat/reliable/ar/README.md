# ClinStat – "What makes a research finding reliable?" Arabic version (20 s, 1080x1920, 30 fps, no voice-over)

- `clinstat_reliable_ar.mp4` – final video. Same timeline, score and sound design as the English version, mirrored for right-to-left reading: headline and statement right-aligned, "10" badge on the right, studies flow right to left into the funnel, effect-plot labels swapped, footer curve mirrored. Official logo unchanged.
- `template.html` -> `build.py` -> `index.html`; `capture.py test|events|full`; `music.py` (writes `score_raw.wav`); `audit.py` (exact Arabic copy, safe zone, overlap, page errors).
- Font: Cairo (SIL Open Font License), bundled as `Cairo.ttf`. Letter-spacing is forced to 0 so Arabic letters stay joined.
- Rebuild: `python3 build.py && python3 music.py && ffmpeg -y -i score_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=7 -ar 44100 audio.wav && python3 capture.py full clinstat_reliable_ar.mp4 audio.wav`
- Copy is Modern Standard Arabic; **needs native-speaker review before use.**
- As in the English version, the source infographic was never supplied; the composition was reconstructed from the written brief.
