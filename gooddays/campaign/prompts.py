"""Image-generation prompt pack for GOOD DAYS: one DIFFERENT scene per design (18 posts + 24 stories + reel shots). python3 prompts.py -> image-prompts.md, image-prompts.csv"""
import csv
MASTER = ("Photorealistic premium lifestyle advertising photograph, natural skin texture, realistic hands and anatomy, shallow depth of field, shot on a 35mm lens, "
 "warm natural sunlight with deep contrast, charcoal and neutral tones with restrained deep-red accents. Location: an outdoor cafe terrace in Egypt: white round tables, white perforated plastic chairs, "
 "dark grey stone-block wall with small square niches, black metal railing, green foliage in soft focus. Cups are clear plastic cups with black straws and NO printed text or logo (the real GOOD DAYS logo is added in post). "
 "Leave the described clean space for text. No text, no letters, no logos, no watermarks.")
CHAR = ("CHARACTERS (attach the reference photos and say 'same person as the reference' every time): Guy A: late 20s, short dark curly hair, light stubble, grey oversized t-shirt, black smartwatch. "
 "Guy B: athletic man in his 20s, black t-shirt, short dark curls. Older man C: white hair and short white beard, olive-green shirt. Woman D: late 20s, long dark hair tied back, beige linen shirt. Use a different person or a different crop in every image: never the same pose twice.")
NEG = "Negative: extra fingers, deformed hands, morphing face, plastic skin, text, letters, logos, watermark, brand names, cartoon, over-sharpened, duplicate people, extra limbs."
# (id, ratio, text space, scene)
POSTS = [
 ("w01_mon_reset","4:5","upper-left empty","Wide shot of the empty sunlit terrace at opening time: tables set, chairs tucked in, dappled light on the stone wall, a single blank iced coffee on one table. No people."),
 ("w02_mon_quiet_corner","4:5","upper-left","Guy A reading a paperback at a corner table, seen from behind and the side, blurred foliage in front, a black coffee beside him."),
 ("w02_thu_hour_here","4:5","centre, darkened","Close-up of a hand placing a clear cup of iced orange drink on a white table, motion-free, sun flare on the wall behind."),
 ("w03_mon_earned_it","4:5","lower third","Guy B in gym clothes, towel on his shoulders, sitting on a terrace chair, taking the first sip through a straw, eyes closed, relieved."),
 ("w04_mon_sun","4:5","lower third","Low angle across a white table surface toward the sun, a clear iced coffee glowing with backlight, leaves in the corner."),
 ("w04_thu_outside","4:5","centre, darkened","Woman D laughing with her face turned toward the sun, sunglasses on her head, a cup in her hand, shot from the shoulders up."),
 ("w05_mon_menu","4:5","lower third","Top-down flat lay of three different clear cups (pale green, pink, creamy coffee) on a white table with sunlight shadows of the railing."),
 ("w06_mon_first_coffee","4:5","upper-left","Morning light at 10 AM: Older man C stepping onto the terrace holding a small black espresso cup, long soft shadows."),
 ("w06_thu_hours","4:5","centre, darkened","A wall clock-free detail: the black metal railing and the stone wall in warm light with out-of-focus foliage, empty frame (texture background)."),
 ("w07_mon_late","4:5","lower third","Evening terrace with warm string lights, Guy A and Woman D at a table, laughing, cups glowing, blue-hour sky behind."),
 ("w08_mon_whole_day","4:5","top title","Vertical triptych source: three separate images are needed (gym bench with water bottle / terrace cup / night terrace). Generate each as its own 4:5 image."),
 ("w08_thu_no_membership","4:5","left half empty","A stranger-friendly moment: Woman D in casual street clothes (no gym wear) arrives at the terrace with a tote bag, smiling, looking for a table."),
 ("w09_mon_healthy","4:5","lower third","Macro of a clear cup with a pale green drink and ice next to a black iced coffee cup, water droplets, bright background bokeh."),
 ("w10_mon_company","4:5","lower third","Four friends at one table seen from slightly above, mixed ages, hands reaching for cups, candid laughter (no one looking at the camera)."),
 ("w10_thu_bring","4:5","upper-left","Over-the-shoulder shot of Guy B waving two friends toward an empty table with the sun behind them."),
 ("w11_mon_habit","4:5","upper-left","The same corner table shown with a regular's usual items: black coffee, a phone face-down, a notebook, golden hour."),
 ("w12_mon_earned_part","4:5","upper-left","Guy A leaning back in the chair, arms behind his head, satisfied smile, eyes closed in the sun, cup on the table."),
 ("w12_thu_thanks","4:5","lower third","Wide golden-hour shot of the full terrace with six guests in the distance and warm light flares, cheerful and quiet."),
]
STORY = [
 ("s01","9:16","bottom third","Hands wrapped around a blank clear cup from the barista side, an open door and daylight behind."),
 ("s02","9:16","top","Guy B walking up the terrace steps with a gym bag, morning shadows."),
 ("s03","9:16","top","Close-up of a coffee cup and saucer with latte art, sunlit white table, foliage blur."),
 ("s04","9:16","centre darkened","Overhead of a notebook, a pen, and a black coffee on a white table."),
 ("s05","9:16","top","Woman D laughing with a friend at a table, shot from behind a plant, soft focus foreground."),
 ("s06","9:16","bottom third","Close-up of ice cubes and orange slices in a clear cup against the sky."),
 ("s07","9:16","top","Older man C sipping coffee and smiling at the sunlight."),
 ("s08","9:16","bottom third","Table by the stone wall with a long late-afternoon shadow of the railing across it."),
 ("s09","9:16","centre darkened","A hand holding a cup toward the camera against green foliage."),
 ("s10","9:16","bottom third","Two cups clinking, side view, bright background."),
 ("s11","9:16","top","Man on a bench with headphones and a cup, low angle, sky behind."),
 ("s12","9:16","bottom third","Blurred terrace at dusk with warm lights, one empty chair in focus."),
 ("s13","9:16","top","Barista hands (no face) pouring a drink into a clear cup, macro."),
 ("s14","9:16","centre darkened","A smartwatch and a cup on a table, wrist only, golden light."),
 ("s15","9:16","bottom third","Friends' feet and chairs at a table from a low angle, relaxed, sun patches on the floor."),
 ("s16","9:16","top","Pink smoothie in a clear cup held up against a window of light."),
 ("s17","9:16","bottom third","Woman D reading on her phone with a green drink, caught mid-smile."),
 ("s18","9:16","top","Chairs stacked neatly at opening time, morning light on the floor."),
 ("s19","9:16","centre darkened","Macro of condensation drops on a clear cup."),
 ("s20","9:16","bottom third","Guy A typing on a laptop at a table with an iced drink, side view, sunglasses on."),
 ("s21","9:16","top","Hands passing a cup across the table between two people."),
 ("s22","9:16","bottom third","Wide night shot of the terrace with warm lights and two guests in the distance."),
 ("s23","9:16","top","Three cups lined up on a railing ledge in golden hour."),
 ("s24","9:16","bottom third","Guest waving goodbye at the terrace entrance with a to-go cup, sun setting behind."),
]
REEL = [
 ("wk02_tue_listen","Shot 1: ice cubes dropping into a clear cup, macro, 3 s. Shot 2: breeze moves the leaves over the stone wall, 3 s. Shot 3: a hand sets the cup on the table, 3 s. Shot 4: a smile, sunlight flare, 3 s."),
 ("wk04_tue_sun","Shot 1: table fully in shade. Shot 2: shadow slides away, the table lights up (same frame, locked camera). Shot 3: Guy A lifts his face to the sun."),
 ("wk06_tue_first_hour","Shot 1: staff hands unlock and open the glass door, daylight pours in. Shot 2: first cup slides across the counter. Shot 3: first guest sits down and exhales."),
 ("wk08_tue_full_day","Eight 2.5 s shots: gym rack / gym towel / walkway / terrace cup / laptop / golden hour / string lights / the last light turned off at 12."),
 ("wk09_tue_pour","Barista pours a pale green drink over ice (macro), then a black iced coffee, then both cups side by side."),
 ("wk11_tue_repeat","Same guest, same chair, three visits: morning, afternoon, evening (different clothes, same camera angle)."),
 ("wk12_tue_best_of","Pick the six best generated stills and animate each with a slow push-in (image-to-video, 3 s each)."),
]
if __name__ == "__main__":
    md = ["# GOOD DAYS: برومبتات توليد الصور (كل ديزاين بصورة مختلفة)\n", "**الاستخدام:** ولّد كل صورة على حدة بأداة صور، وارفق صور الشخصيات والمكان الأصلية كمرجع. سمّي الملف باسم الـid (مثلاً `w01_mon_reset.jpg`) وحطه في `posts/img/gen/`، وأنا أركّبه على التصميم. اللوجو والنصوص بتتحط في المونتاج، فاطلب من الأداة صورة من غير أي كتابة.\n",
          "## بلوك ثابت (حطه في أول كل برومبت)\n", MASTER, "\n", CHAR, "\n", NEG, "\n## ١٨ صورة للبوستات (4:5، ١٠٨٠×١٣٥٠)\n"]
    rows = []
    for i, r, sp, sc in POSTS: md.append(f"- **{i}** ({r}، مساحة النص: {sp}): {sc}"); rows.append([i, "post", r, sp, sc])
    md.append("\n## ٢٤ صورة للستوريز (9:16، ١٠٨٠×١٩٢٠)\n")
    for i, r, sp, sc in STORY: md.append(f"- **{i}** ({r}، مساحة النص: {sp}): {sc}"); rows.append([i, "story", r, sp, sc])
    md.append("\n## ٧ ريلز: لقطات image-to-video\n")
    for i, sc in REEL: md.append(f"- **{i}**: {sc}"); rows.append([i, "reel", "9:16", "", sc])
    open("image-prompts.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
    with open("image-prompts.csv", "w", encoding="utf-8-sig", newline="") as f: w = csv.writer(f); w.writerow(["id", "type", "ratio", "text_space", "scene"]); w.writerows(rows)
    print(len(POSTS), len(STORY), len(REEL))
