# ClinStat static posts (1080x1350, 4:5), Arabic RTL and English LTR

All 18 static-post slots of the 3-month calendar (24 images: the week-1 carousel is 7 slides).

- `out/ar/*.png`, `out/en/*.png` – 1080x1350; `out/<lang>/2x/` – 2160x2700 copies.
- `engine.py` – templates: cover, points, closing, list, quote, case, stats, table, promo, grid, forest (brand colours, IBM Plex Sans Arabic, traced logo).
- `cards.py` – all copy in both languages (edit here, then `python3 build.py all` or `python3 build.py en wk09_mon_forest_plot`). `build.py` also runs a layout audit (footer overlap, margins, row overlap).
- Slot-to-file mapping, dates and the "confirm before publishing" notes: `../ClinStat_Content_Pack_Index.xlsx` and `../CONTENT_PACK.md`.

Footers say "link in the caption": use a separate UTM link per post. No card promises acceptance or publication. Illustrative numbers are labelled.
