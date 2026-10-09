# ClinStat Research – motion graphics

- `clinstat_motion.mp4` – **v3**: 15.0 s, 1080x1920, 30 fps, motion graphics only (no characters). Kinetic hook at frame 0, content from the supplied posts (desk-rejection reasons, survival analysis), Gulf network map, real traced logo end card. Cuts on a 120 BPM beat grid, synthesized SFX, mixed to -14 LUFS, true sub-frame motion blur, phone safe zones.
- `brand.json` – everything extracted from the supplied images/videos (palette, messaging, charts, style, storyboard).
- `assets/` – logo mark, lockup, charts/map/diagram crops from the supplied videos, icons from the posts.
- `motion/template.html` – the whole animation as one deterministic SVG/JS timeline (`render(t)`); `__SEA__` is replaced by the traced Gulf map from `map_paths.json`.
- `motion/extract_logo.py` – traces the supplied logo into exact vectors (3 chevrons, 3 dots, wordmark letters, divider) -> `logo_vector.json`; the video uses these, not a re-drawn logo.
- `motion/build.py` – injects `logo_vector.json` + `map_paths.json` into `template.html` -> `index.html`.
- `motion/trace.py` – vectorises the Gulf sea shapes from the supplied map frame (OpenCV).
- `motion/capture.py` – Playwright/Chromium frame capture -> ffmpeg (`python capture.py full out.mp4 audio.wav`; fonts: Be Vietnam Pro Bold/Medium next to the html).

## v3 pipeline
- `motion/template3.html` – the v3 timeline (`render(t)`); also exports `window.EVENTS` (sound-design cue list). `__SEA__`/`__LOGO__` are replaced by `map_paths.json` / `logo_vector.json` (same as `build.py`, output `index3.html`).
- `motion/events.py` -> `events.json`; `motion/sfx.py` -> `sfx.wav`; `motion/mix_audio.sh` -> `audio3.wav`.
- `motion/capture3.py out.mp4 audio3.wav` – Chromium frame capture, 4 sub-frames per frame (180° shutter) averaged by ffmpeg `tmix`. Fonts: Lexend (OFL) next to the html.
- The survival curves are illustrative (marked on screen), not real data.
