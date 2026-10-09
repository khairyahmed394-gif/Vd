# ClinStat – "3 Factors of Reliability" (20 s, 1080x1920, 30 fps, no voice-over)

- `clinstat_3factors.mp4` – final video (600 frames, exactly 20.000 s; original synthesized ambient score + sound design, -14 LUFS).
- `template.html` – the whole timeline (`render(t)`); `__LOGO__` is replaced by `logo_vector.json` (the supplied logo traced 1:1) via `build.py` -> `index.html`.
- `capture.py test|events|full` – Chromium frame capture (4 sub-frames/frame), `music.py` – score + SFX from `events.json`, `audit.py` – exact-copy / safe-zone / overlap / page-error audit.
- Scenes: 0-3 brand opening, 3-8 factor 01, 8-12 factor 02, 12-17 factor 03, 17-20 closing.
- The supplied logo contains only the mark, "ClinStat" and "RESEARCH" (no Arabic name, no "INSTITUTE"); it is used unchanged. "CLINSTAT RESEARCH INSTITUTE" is set as separate typography. Add the Arabic name once the official artwork/text is supplied.
