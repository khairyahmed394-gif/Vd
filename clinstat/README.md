# ClinStat Research – motion graphics

- `clinstat_motion.mp4` – 14.2 s, 1080x1920, 30 fps, motion graphics only (no characters), brand music + transition whooshes.
- `brand.json` – everything extracted from the supplied images/videos (palette, messaging, charts, style, storyboard).
- `assets/` – logo mark, lockup, charts/map/diagram crops from the supplied videos, icons from the posts.
- `motion/template.html` – the whole animation as one deterministic SVG/JS timeline (`render(t)`); `__SEA__` is replaced by the traced Gulf map from `map_paths.json`.
- `motion/extract_logo.py` – traces the supplied logo into exact vectors (3 chevrons, 3 dots, wordmark letters, divider) -> `logo_vector.json`; the video uses these, not a re-drawn logo.
- `motion/build.py` – injects `logo_vector.json` + `map_paths.json` into `template.html` -> `index.html`.
- `motion/trace.py` – vectorises the Gulf sea shapes from the supplied map frame (OpenCV).
- `motion/capture.py` – Playwright/Chromium frame capture -> ffmpeg (`python capture.py full out.mp4 audio.wav`; fonts: Be Vietnam Pro Bold/Medium next to the html).
