# GOOD DAYS at TRIO CAFE: creative direction and social design system

Status: the reference board and master prompt are the **direction**. The layouts in `out/` are the **built designs** (vector stand-ins for the product photos). The photography is **not generated yet**: section 8 has production-ready prompts. Names, prices, ingredients and offers are placeholders in `[brackets]` until supplied. The real logo is used (tinted), never redrawn.

## 1. Art-direction summary
**Idea:** coffee is the excuse, the good day is the product. Warm, optimistic, premium but approachable. Core line: *More than coffee. A better you.*
**Look:** cream and forest green lead; caramel and espresso carry coffee; olive and blush bring colour. Bold condensed headlines, an editorial serif for premium moments, handwriting for personality, plain sans for facts. Photography is real and appetising; graphics are flat and confident.
**Rules:** one message per design · one hero per design · doodles are seasoning, not the meal · never repeat the same background, image position or headline position in consecutive posts · no health claims, no invented prices or ingredients.

## 2. Design system
| Token | Value |
|---|---|
| Forest / Olive / Cream | #17251D / #747A50 / #F2EBDD |
| Espresso / Caramel / Blush | #493020 / #B9835B / #E8B9B5 |
| Headline | Anton (OFL), uppercase, tight |
| Editorial | Playfair Display (OFL) |
| Handwriting | Caveat (OFL), annotations only, max 4 words per line |
| Body | DM Sans (OFL), tracked caps for labels |
| Doodles | smiley, asterisk, heart, hand arrow, scribble underline (`svg.py`) |
| Formats | feed 1080×1350 · story/reel 1080×1920 · carousel 4 slides, same size |
| Safe margins | 70 px sides · logo block 220 px wide, bottom corner (moves with the composition) |
| Logo | `img/logo.png` tinted forest on light, cream on dark |
Reuse: add a concept in `designs.py` (function returning background + body), run `python3 designs.py`. Drop an AI photo at `img/gen/<id>.jpg` and the stand-in is replaced in the product slot.

## 3. Moodboard and grid
`moodboard.png` (palette, type, key designs) · `grid.png` (recommended 3×4 feed). Grid order, left to right, top to bottom: **D01 hero coffee · D05 poster · D08 pick your mood | D04 new in town · D06 your kind of good · D12 brunch o'clock | D02 matcha berry · D09 this or that · D13 good fuel | D14 signature · D03 brunch hits different · D07 good people.** Each row mixes dark, light and colour; product, type and lifestyle alternate; no two neighbours share a background.

## 4. The 14 concepts
Format is 4:5 unless noted. "Photo" = what replaces the vector stand-in.

### Category 1: hero product
**D01 Good Coffee, Better Days** (Bold Editorial). Objective: signature iced-coffee awareness. Audience: daily coffee drinkers, gym crowd. Idea: the pour is the hook, handwriting makes it personal. Composition: cup right of centre, script headline top-left tilted -6°, tiny sign-off bottom-left. Photo: espresso pouring into milk and ice, dark green backdrop, rim light. Copy: *Good Coffee Better Days.* / *Same energy. Different day.* CTA: none (brand). Caption: "One pour, one better day. ☕ Tag who you'd share it with." 
**D02 Matcha Meets Berry Mood** (Playful Contemporary). Objective: showcase a colourful drink. Audience: younger drinkers, Instagram sharers. Idea: three clear layers are the story. Composition: cup centre on a stone slab, strawberries at the base, script top-left, five-line label top-right. Photo: matcha, milk and berry layers, hard sun, strawberry props. Copy: *Matcha Meets Berry Mood.* Caption: "Green on top, pink below, good in between. [Drink name] is here." (confirm the drink exists)
**D03 Brunch Hits Different** (Premium Food Editorial). Objective: brunch traffic. Audience: weekend groups. Composition: plate and cup, script headline upper right, three-line list bottom-left. Photo: top-down plate with croissant/toast and an iced coffee, directional window light, crumbs and texture. Copy: *Brunch Hits Different.* / *Good food · Good people · Good conversations.* Caption: "Slow table, good plates. Who's your brunch person?" (use only dishes on the menu)
**D04 New in Town** (Bold Editorial). Objective: launch any new item. Composition: torn blush paper top, oversized headline, script note with arrow to the product. Photo: product cut-out on stone, soft shadow. Copy: *New in town.* / *say hi to the new one.* Caption: "[Name] just landed. First sip is on you to judge." CTA: "Try it today."

### Category 2: brand story
**D05 A Good Day Starts Here** (Minimal Luxury / typographic). Objective: brand recall. Composition: stacked condensed headline, scribble underline, smiley, tagline in script. No photo. Caption: "More than coffee. A better you."
**D06 Your Kind of Good** (Analog Lifestyle). Objective: show real café moments. Photo: candid, flash-lit or sunlit, a guest laughing with a drink, no eye contact with camera. Copy: *Your Kind of Good.* / *Work · Chill · Meet · Repeat.* Caption: "Whatever good looks like for you today, it fits here."
**D07 Good People, Better Days** (Analog Lifestyle collage). Objective: community. Composition: three tilted polaroids, script headline. Photo: three separate candid moments (friends, a laugh, hands and cups), film grain. Caption: "Tag the people who make your days better."

### Category 3: interactive
**D08 Pick Your Mood** (Playful). Three drinks = Focus, Chill, Social, labelled by mood, not by ingredient. Hand arrows, handwritten labels. Photo: top-down trio on a stone surface. CTA: "Which one's your mood today? Tell us below." Story version: add a poll sticker.
**D09 This or That** (Bold split). Iced vs hot, green vs blush panels, centre "or". Photo: one iced cup and one hot cup, each on its colour. CTA: "Which team are you?" 
**D10 Build Your Perfect Coffee Day** (carousel, 4 slides). Cover → 01 Pick your drink → 02 Pair it with something good → 03 Pick your moment ("work. chill. meet. repeat."). Last slide: "Save this for your next visit." Photo option: one image per slide (drink, pairing, moment).

### Category 4: product and sales
**D11 The Good Menu** (carousel template). Cover + one slide per hero product: `[Drink name]`, one line, `[ingredients as supplied]`, `[price]`. The menu changes, so the template is reusable weekly. Photo: one hero per slide, same angle and light for consistency.
**D12 It's Brunch O'Clock** (promo). Objective: brunch visits. Composition: oversized headline, two plates, hand arrow, pill CTA. Photo: two plates top-down. Copy: *It's brunch o'clock.* / *Great food. Better company. 10 AM — 12 AM.* CTA: "Come hungry." Offer line only if a real offer exists.
**D13 Good Fuel for Better Days** (Bold, dark). Objective: introduce the healthier side of the menu. Copy: *Good fuel for better days.* / *Coffee · Healthy drinks · Good food.* No claims about benefits, protein or calories unless supplied and approved. Photo: hand holding a cup in the gym-lit café corner, dark and moody.
**D14 The Signature Drink** (repeatable spotlight). Hero, name, key ingredients, CTA. Use monthly with a different drink and background colour.

## 5. Reels (6)
Each: hook · storyboard · camera/light · on-screen copy · sound · rhythm · cover · caption/CTA · AI video prompt. All 9:16, 12-15 s, real-looking motion only, no text generated inside the video.

**R1 The Pour (D01).** Hook: espresso hits the ice at 0.0 s. Storyboard: 0-2 s macro of a pour into milk and ice · 2-5 s the swirl settling, condensation · 5-8 s cup lifted into frame · 8-12 s sip, smile · 12-15 s cup on table, end card. Camera: macro, slow 5% push-in; light: dark background, rim light. Copy: "Good coffee" (3 s) → "Better days." (9 s). Sound: ice clink, pour, soft warm beat in from 5 s. Rhythm: cuts on the ice sounds. Cover: `r1_cover_pour`. Caption: "One pour. One better day. Tag your coffee person." CTA: "Come by today." Prompt: *Macro commercial shot of espresso being poured into a clear plastic cup with milk and ice cubes, swirling marbled layers, condensation drops, shallow depth of field, rim light, dark forest-green background, 24 fps, slow push-in, realistic liquid physics, no text.*
**R2 Pick Your Mood (D08).** Hook: three cups slide into frame on the beat. Storyboard: 0-3 s cups enter · 3-5 s "Focus" close-up · 5-7 s "Chill" · 7-9 s "Social" · 9-12 s all three, hands grab · 12-15 s end card with question. Copy: Focus / Chill / Social, then "Pick yours." Sound: three-note motif, one note per cup. Cover: `r2_cover_mood`. Caption: "Focus, chill or social? Tell us in the comments." Prompt: *Top-down tabletop video, three clear cups (coffee, pale green drink, pink drink) sliding onto a stone surface one by one, bright natural light, soft shadows, crisp condensation, hands entering to pick them up, realistic motion, no text.*
**R3 Matcha Meets Berry (D02).** Hook: the layers separate. Storyboard: 0-3 s pink berry base poured · 3-6 s milk · 6-9 s matcha on top, layers hold · 9-12 s strawberry drop · 12-15 s product + tagline. Prompt: *Close-up video of layered pink berry, milk and green matcha being poured in a clear cup, clean layers, strawberries on a stone slab, hard sunlight, shallow depth of field, slow motion 60% speed, realistic liquids, no text.* Sound: pour and ice, rising synth pad. Caption: "Matcha, milk, berry. Layers on purpose."
**R4 Brunch O'Clock (D12).** Hook: a croissant tears open. Storyboard: 0-2 s tear · 2-5 s table top-down, plates enter · 5-8 s hands reach, coffee cheers · 8-12 s laughter wide · 12-15 s "It's brunch o'clock." + hours. Prompt: *Cinematic top-down brunch table, hands entering to tear a croissant and pick up an iced coffee, warm window light, crumbs, steam, handheld feel, realistic food, no text.* Use only dishes on the menu.
**R5 A Good Day at Good Days (D06/D07).** Hook: 10:00, the door opens. Storyboard: opening, first cup, work, a laugh with friends, golden hour, night lights, 12:00 closing. Eight 2 s shots, whip pans on beats. Copy: "10 AM" ... "12 AM" timestamps, end "A good day starts here." Prompt per shot in section 8 (each shot a different scene).
**R6 New in Town (D04).** Hook: paper tears to reveal the new drink. Storyboard: 0-2 s paper tear (blush) · 2-5 s product reveal on stone · 5-8 s pour and ice · 8-12 s first sip · 12-15 s name card. Caption: "[Name] is here. Say hi." Prompt: *Product reveal video, blush paper tearing away to show a clear cup of [drink] on a stone slab, soft window light, ice and condensation, subtle push-in, realistic, no text.*

## 6. Copy bank (distinctive, short)
Hooks: "Same energy. Different day." · "Green on top, pink below, good in between." · "Which one's your mood?" · "Slow table, good plates." · "Work. Chill. Meet. Repeat."
CTAs: Come hungry · Try it today · Save for your next visit · Tag your coffee person · Tell us below.
Avoid: "best coffee in town", "perfect taste", "ultimate destination".

## 7. Quality check (done on every built design)
Readable on a phone (headline ≥ 110 px at 1080 wide) · one hero · palette only · hierarchy clear · no overlaps · different from neighbours · logo real · nothing invented. Known limits: the product art is vector illustration; photography replaces it for the premium result.

## 8. Image-generation prompts (photography)
**Master block (start every prompt):** *Photorealistic premium specialty-coffee advertising photograph, real food and drinks, natural imperfections, shallow depth of field, 50mm lens, warm natural light with soft shadows, palette of forest green, cream, espresso brown, caramel and blush, clean negative space for text, no text, no letters, no logos, no watermark. Cups are clear plastic cups with black straws and no printing.*
**Negative:** *deformed hands, extra fingers, plastic skin, text, logos, watermarks, cartoon, over-sharpened, impossible liquid physics, duplicate cups.*
Save each result as `img/gen/<id>.jpg` at 4:5 (D01 pour, D02, D03, D04, D13, D14) and 3:4 for polaroids `d07_1..3`.
- **d01:** iced coffee with milk marbling being poured, espresso stream, ice, condensation, dark green backdrop, rim light, cup right of centre, empty upper-left.
- **d02:** clear cup with three layers (matcha green, milk white, berry pink), strawberries around the base on a pale stone slab, hard sunlight, dappled shadows, empty upper-left.
- **d03:** top-down plate with croissant and avocado toast, iced coffee beside it, directional window light, crumbs, linen, empty upper-right.
- **d04:** a single new drink on a rough stone slab, soft window light, cream backdrop, empty upper third.
- **d06 (story/post):** candid lifestyle: a woman in sunglasses laughing with an iced drink, golden hour, film grain, empty lower-left. **Use a different person from the other images.**
- **d07_1/2/3:** three separate candid moments (two friends laughing over cups; hands cheering; a laptop and a latte), direct-flash analog look, film grain.
- **d08:** top-down trio of cups (coffee, pale green drink, pink drink) on a stone surface, bright light, hand-drawn-friendly empty space around.
- **d09:** left: iced coffee on dark green; right: a hot coffee mug on blush. Two separate images, same angle.
- **d12:** two brunch plates, top-down, bold colours, warm light, empty upper third.
- **d13:** hand holding a plain takeaway-style clear cup in a dimly lit gym corner, dumbbells blurred, moody, empty left side.
- **d14:** signature drink on cream stone, hero shot at eye level, rim light, empty lower third.
- **Reel R5 shots:** (1) door opening to a bright terrace 10:00, (2) first cup on the counter, (3) laptop and iced drink, (4) friends laughing, (5) golden-hour terrace, (6) string lights at night, (7) a hand switching off the light, (8) empty chair at 12:00.
**Production rule:** generate clean images, add logo, text and prices in the editor. Never generate the brand name.

## 9. Open items
1. Real drink and dish names, descriptions, prices.
2. Confirm any food shown is on the menu and that "healthy drinks" wording is approved.
3. Original logo file (the current one is extracted from your photos).
4. Instagram handle for CTAs.
5. Image-model choice: say which tool you use and I'll adapt the prompts and place the photos.
