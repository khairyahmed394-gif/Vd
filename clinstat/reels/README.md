# ClinStat reels (20 s, 1080x1920, 30 fps, Arabic, burned-in captions, original sound)

Palette: original brand colours (ivory #F9F5EF, deep forest #003520, forest #025130, gold #B19063; logo in its own colours). The earlier navy version is in `out/navy_version/`.

Built from the "ClinStat 3-Month Content Calendar (AR)" reel rows (spec: hook 0-3 s, three beats, CTA frame with the keyword, on-screen keywords not full sentences, burned-in captions, slow reveals).

| File | Calendar slot | Hook | CTA keyword |
| --- | --- | --- | --- |
| `out/wk01_tue_assumptions.mp4` | Week 1 Tuesday | الـp-value بتاعك ملهوش قيمة لو تخطيت الخطوة دي | follow (no keyword) |
| `out/wk02_tue_design.mp4` | Week 2 Tuesday | أغلى غلطة في البحث بتحصل قبل أول مريض | DESIGN |
| `out/wk02_thu_test.mp4` | Week 2 Thursday | متختارش الـtest على أساس إنه بيدّي p أقل | TEST |
| `out/wk12_tue_model.mp4` | Week 12 Tuesday | 15 متغير في الـmodel و30 حدث بس | MODEL |

Timeline of each reel: hook 0-3.5 s | beat 1 3.2-7.6 | beat 2 7.4-11.6 | beat 3 11.4-15.8 | CTA 15.6-20 s.

- `reel.html` (all four reels, `?reel=r01..r04`) -> `build.py` -> `index.html`; `capture.py test|events|full <reel> ...`; `audio.py <reel>` (score + sound design from `events_<reel>.json`, then `ffmpeg loudnorm -14 LUFS`); `audit.py <reel>` (safe zone 240-1590 px, overlap, page-error sweep).
- Fonts: IBM Plex Sans Arabic (OFL). Logo: traced vector from the ClinStat videos.

## Before publishing
- The calendar has hooks only, so the three beats are written here. A statistician should check the wording.
- Numbers in the p-value and Test A/B/C visuals are illustrative and labelled on screen. They are not real data.
- "10 events per variable" is shown as an approximate rule of thumb, not a hard rule.
- Wire each keyword to an auto-DM with its own UTM link (`clinstat_ig_reel_wk[#]_[keyword]`). The offers (free 15-minute reviews) need to be deliverable.
- Native Arabic review (colloquial copy follows the calendar; Gulf audience may prefer lighter wording).
- 14 more reel hooks are in the calendar and 14 in the reserve bank; add a function in `reel.html` for each.
