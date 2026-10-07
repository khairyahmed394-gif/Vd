# ClinStat Research – video pipeline

- `brand.json` – everything extracted from the supplied images/videos (palette, messaging, charts, style, storyboard). The renderer reads the palette from it.
- `assets/` – logo mark, logo lockup, charts/map/phase diagram cropped from the supplied videos, icons cropped from the supplied posts.
- `pipeline/tts.py` – Egyptian Arabic narration (Edge TTS `ar-EG-ShakirNeural`) + subtitle text.
- `pipeline/presenter.py` – shaded illustrated presenter with audio-driven lip sync.
- `pipeline/render.py` – composes 1080x1920 video (ffmpeg), mixes the brand-video music under the narration.
