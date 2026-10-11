# ClinStat: the full 3-month content pack (60 posts, Arabic + English)

Everything in the "ClinStat 3-Month Content Calendar (AR)" is generated. Start date in the calendar: Sunday 18 Oct 2026 (change it in `tweets/tweets.py` and `build_index.py`; the original xlsx formulas move the dates).

| Slots | Count | Where | Format |
| --- | --- | --- | --- |
| Tweets (24, week 12 Sunday is a 6-tweet thread) | 24 | `tweets/tweets.md`, `tweets/tweets.csv` | Arabic and English, 280-character limit checked, UTM suffix per tweet |
| Static posts | 18 slots = 24 images (the week-1 carousel is 7 slides) | `posts/out/ar/`, `posts/out/en/` | 1080x1350 PNG (+ 2160x2700 in `2x/`) |
| Reels | 18 | `reels/out/ar/`, `reels/out/en/` | 1080x1920, 20 s, 30 fps, original sound, burned-in captions |
| Index | 60 rows | `ClinStat_Content_Pack_Index.xlsx`, `content_pack_index.csv` | slot, date, topic, hook, CTA, files, what to confirm |

Brand: original colours (ivory, deep forest green, gold) for reels; navy / green / gold / sand from the calendar's formula guide for posts. Logo: the traced vector from the ClinStat videos. Fonts: IBM Plex Sans Arabic (OFL).

## What was written here (and needs an expert's eye)
- The calendar gave topics, hooks and CTAs only. All body text (tweets, the 15 checks, the reel beats, table/checklist contents) was written for this pack. A biostatistician should read the statistical wording before publishing.
- Illustrative numbers (p-values, Test A/B/C, forest plot, before/after methods sentence) are labelled on screen as illustrative.
- Arabic follows the calendar's colloquial tone. Have a native Gulf reader approve it if the audience is there.

## Confirm before publishing (also listed per slot in the index)
- **Placeholders, do not publish as is:** week 11 Wednesday tweet (client testimonial needs written approval).
- **Client or company facts taken from the calendar:** "50+ papers and h-index 5+ per member", "~100 papers a quarter, 80% published in high-impact journals", "10+ rejections, then accepted at the first journal after the review".
- **Proposed content that must match the real offer:** the three "what we will never do" commitments, the "six practices", the independent-verification description, the ghostwriting answer, the free-consultation steps, the GCC Submission Checklist and Manuscript Readiness Checklist contents, the Scale / Rescue / Independence descriptions, "last chance this month" and "slots open this week" (availability).
- **Offers:** every free 15-minute review, checklist and keyword auto-DM must exist and be deliverable. Give each keyword (DESIGN, TEST, MODEL, CHECKLIST, OUTCOME, MISSING, REVIEWERS, TRIAGE, METHODS, READY, JOURNAL, ETHICS, SENSITIVITY, I2, CONSULT) its own auto-DM and UTM link: `clinstat_[platform]_[format]_wk[#]_[keyword]`.
- Spell-check every card twice (the calendar asks for it).

## Regenerate
- Posts: `cd posts && python3 build.py all` (content in `cards.py`, templates in `engine.py`).
- Reels 1-4: `reels/reel.html` (`capture.py`, `audio.py`). Reels 5-18: `reels/reelgen.html` with the copy in `reels/cfg.js` (`capture_gen.py`, `audio.py`). `LANG_Q=en` renders English. `audit.py`, `bands.py`, `spacing.py` check layout.
- Tweets: `cd tweets && python3 tweets.py`. Index: `python3 build_index.py`.
