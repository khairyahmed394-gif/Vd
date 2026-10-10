# ClinStat static-post templates (1080x1350, 4:5, Arabic RTL)

Built from the "ClinStat 3-Month Content Calendar (AR)". Specs follow its formula guide: 1080x1350 px, headline + 3 to 5 points, brand mark, CTA footer, about 40 words per slide, one idea per slide, navy / green / gold / sand, IBM Plex Sans (Arabic), no stock doctor photos.

- `out/` – final PNGs at 1080x1350; `out/2x/` – 2160x2700 copies; `out/clinstat_posts_1080x1350.zip` – the 1080 set; `out/contact_sheet.png` – overview.
- `build.py` – template engine (`cover`, `points`, `closing`, `list`, `quote`, `case`, `stats`) and the content in `CARDS`. `python3 build.py [card_name ...]` re-renders and runs a layout audit (footer overlap, margins, row overlap).
- Colours: navy `#0B1F33`, deep green `#103D2E`, gold `#A8854E`, sand `#F7F4ED`. Logo: the traced vector from the ClinStat videos (`logo_vec.json`).

## Cards
| File | Calendar slot | Status |
| --- | --- | --- |
| `wk01_mon_s1..s7` | Week 1 Monday, carousel "15 نقطة لنتيجة بحثية موثوقة" (7 slides: cover, 5 axes x 3 checks, save slide) | text written here, review the statistics wording |
| `wk03_thu_five_questions` | Week 3 Thursday, 5 questions before hiring a biostatistician | from the existing video; "50+ papers / h-index 5+" line needs confirming |
| `wk05_mon_ownership` | Week 5 Monday, researcher ownership statement | from the calendar |
| `wk06_mon_case_study` | Week 6 Monday, "10+ rejections, 1 acceptance" | figures come from the calendar; confirm with the client before publishing |
| `wk11_thu_partnership` | Week 11 Thursday, institutional partnership numbers | "~100 papers per quarter, 80% published" comes from the calendar; confirm and document |

## Before publishing
- Spell-check every card twice (the calendar asks for it); check Arabic wording with a native reader, the copy follows the calendar's colloquial tone.
- Footers say "link in the caption": use a separate UTM link per post (`clinstat_[platform]_[format]_wk[#]_[keyword]`).
- No claims of guaranteed acceptance or publication appear in any card.
