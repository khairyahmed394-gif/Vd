# GOOD DAYS at TRIO CAFE – "Gym to Cafe" photo reel (20 s, 1080x1920, 24 fps)

Built only from the supplied photographs. No people, hands or drinks were generated.

- `gooddays_reel_20s_delivery.mp4` (with sound) and `..._delivery_silent.mp4` – 480 frames, exactly 20.000 s, -13.7 LUFS. `cover_1080x1920.png` – cover frame (19.0 s).
- `render.py` – camera moves, grade, whip-blur cuts, text and logo overlay. `audio.py` – original score and sound design (no samples, no voice). `inpaint.py` – removes the baked-in headlines, red bars and logos from the source ads with LaMa (`clean/`, not committed; needs the `big-lama.pt` model and `LAMA_MODEL` set).
- `src/` – the supplied ads. `logo_extracted.png` – the logo extracted from the supplied ad (white, 223x135 px). **Replace it with the original logo file when available.**

## Timeline
| Time | Shot | Move |
| --- | --- | --- |
| 0.00–3.25 | gym bench, chocolate drink | push-in, handheld |
| 3.25–6.50 | gym cup close-up | push-in on the logo |
| 6.50–9.625 | gym, smoothie held to camera | push-in, cup scaled to 880 px high and centred at y=1000 |
| **9.625** | **match-cut on the cup** | whip-blur, riser then ice-and-cup hit |
| 9.625–13.25 | cafe, orange drink | pull-back, cup starts at the same size and position |
| 13.25–15.75 | cafe, laptop | pan from drink to man |
| 15.75–20.0 | cafe, phone and smile | push-in, overlay from 17.4 s, logo from 18.5 s |

Overlay: **YOU EARNED THIS PART.** (Montserrat ExtraBold on a maroon bar), logo bottom centre.

## Known limits
- Source photos are 1080x1440, so push-ins soften slightly (strongest at the match-cut frame, covered by the whip-blur).
- Inpainting leaves a faint ghost of the straw top in the cup close-up and a smooth wall where the cafe headline was.
- The cup print is part of the supplied photos (not replaced).
