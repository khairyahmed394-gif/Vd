# ClinStat Research – "The Desk Review" (30 s, 1080x1920, 30 fps, English + Arabic, no voice-over)

Concept: editors screen a manuscript in minutes. Three gates (Statistics, Ethics, Scope) each flag an avoidable problem, the paper is stamped DESK REJECTED, then one expert review turns every flag into a check and the paper becomes READY TO SUBMIT. Close: free 15-minute pre-submission consultation.

- `deskreview_en.mp4`, `deskreview_ar.mp4` – final videos (900 frames, exactly 30.000 s, original score + sound design, -14 LUFS).
- `template.html` -> `build.py` -> `index.html` (`?lang=en|ar`); `capture.py test|events|full <lang> ...`; `music.py` (score + SFX from `events.json`, then `ffmpeg -af loudnorm=I=-14:TP=-1.5` -> `audio.wav`); `audit.py <lang>` (exact copy, safe zone, overlap, page-error sweep).
- Fonts: Lexend (English) and Cairo (Arabic), both OFL. Logo is the traced vector in `logo_vec.json`.
- Schedule: 0-3.4 hook | 3.4-5.6 manuscript | 5.6-15.9 three gates | 16-18.3 rejection stamp | 18.3-24.3 review and checks, READY stamp | 24.4-30 logo and call to action.
- **[CONFIRM]** the free 15-minute consultation offer, and have a native Gulf Arabic speaker approve the Arabic copy. The text makes no promise of acceptance; the closing line says acceptance is the journal's decision.
- `audit.py ar` reports bounding-box overlaps because Cairo's line metrics are tall; the Arabic frames were checked visually and the glyphs do not collide.
