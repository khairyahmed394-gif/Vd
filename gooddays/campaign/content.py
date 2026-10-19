"""GOOD DAYS copy: 24 text/poll posts, 18 static captions, 8 reel briefs (AR + EN). python3 content.py -> content.md + content.csv"""
import csv
TAGS_AR = "#جود_دايز #GoodDays #TrioFitnessHub"; TAGS_EN = "#GoodDays #TrioFitnessHub"
# (week, day, ar, en, poll_ar, poll_en)  poll = list of options or None
TEXT = [
 (1,"الأحد","في مكان بيهدّيك، وفي قهوة تستاهله.\nجود دايز وصل Trio Fitness Hub.\nبنفتح من ١٠ الصبح لحد ١٢ منتصف الليل.","A place that slows you down. Coffee worth the stop.\nGOOD DAYS is now at Trio Fitness Hub.\nOpen 10 AM to 12 AM.",None,None),
 (1,"الأربعاء","أول حاجة بتعملها لما تدخل مكان هادي؟","The first thing you do when you walk into a calm place?",["قهوة","كتاب","صمت"],["Coffee","A book","Silence"]),
 (2,"الأحد","قعدة هادية، ترابيزة بيضا، شمس وخضرة.\nمش لازم تعمل حاجة غير إنك تقعد.","A calm seat, a white table, sun and greenery.\nYou don't have to do anything except sit.",None,None),
 (2,"الأربعاء","تحدّي النهارده: ٢٠ دقيقة من غير شاشة.\nجرّبت؟ قول لنا حصل إيه.","Today's challenge: 20 minutes without a screen.\nDid you try? Tell us how it went.",["عملتها","لسه"],["Did it","Not yet"]),
 (3,"الأحد","تمرين وبعده قهوة؟ اتفقنا.\nأنت بتشتهي إيه بعد التمرين؟","A workout, then a coffee? Deal.\nWhat do you crave after training?",None,None),
 (3,"الأربعاء","بعد التمرين: مشروب بارد ولا سخن؟","After training: a cold drink or a hot one?",["بارد","سخن"],["Cold","Hot"]),
 (4,"الأحد","الشمس بعد الضهر بتخلّي القعدة برّه أحلى.\nالترابيزة مستنياك.","The afternoon sun makes sitting outside better.\nYour table is waiting.",None,None),
 (4,"الأربعاء","مين بيحب القعدة برّه؟\nابعتلنا صورة قعدتك المفضلة.","Who loves sitting outside?\nSend us a picture of your favourite spot.",None,None),
 (5,"الأحد","المنيو عندنا كبير وبيتغيّر.\nقهوتك المعتادة موجودة، ومعاها مشروبات صحية.\nاسأل عن مشروب النهارده.","Our menu is big and keeps changing.\nYour usual coffee is there, with healthy drinks beside it.\nAsk about today's drink.",None,None),
 (5,"الأربعاء","مشروب نفسك تلاقيه في المنيو؟ اكتبه في الكومنت.","A drink you wish was on the menu? Drop it in the comments.",None,None),
 (6,"الأحد","أول قهوة في يومك؟ بنفتح ١٠ الصبح.","Your first coffee of the day? We open at 10 AM.",None,None),
 (6,"الأربعاء","مين أول زبون عندنا الصبح؟ اكتب «أنا».","Who is our first customer of the morning? Type “me”.",None,None),
 (7,"الأحد","مش لازم تروّح بدري.\nبنسهر معاك لحد ١٢ منتصف الليل.","No need to head home early.\nWe stay up with you until 12 AM.",None,None),
 (7,"الأربعاء","أنت من ناس الصبح ولا الليل؟","Are you a morning person or a night person?",["الصبح","الليل"],["Morning","Night"]),
 (8,"الأحد","يوم كامل في Trio Fitness Hub:\nتمرين، قهوة، وقعدة تفصل بيها.","A full day at Trio Fitness Hub:\ntrain, coffee, and a seat to switch off.",None,None),
 (8,"الأربعاء","مين بيتمرن هنا ويعدّي علينا؟ ابعتلنا مشروبك المفضل بعد التمرين.","Who trains here and stops by? Tell us your favourite post-workout drink.",None,None),
 (9,"الأحد","مشروباتك المعتادة ومشروبات صحية في نفس المنيو.\nاختار على مزاجك النهارده.","Your usual drinks and healthy ones, on the same menu.\nPick what suits your mood today.",None,None),
 (9,"الأربعاء","لو هتجرّب مشروب صحي النهارده: بارد ولا سخن؟","If you try a healthy drink today: cold or hot?",["بارد","سخن"],["Cold","Hot"]),
 (10,"الأحد","القعدة الحلوة بتتحسب من الناس اللي معاك.\nجيبهم وتعالى.","A good seat is judged by who sits with you.\nBring them along.",None,None),
 (10,"الأربعاء","اذكر الصاحب اللي لازم ييجي معاك المرة الجاية.","Tag the friend who has to come with you next time.",None,None),
 (11,"الأحد","الحاجة الحلوة بتتعاد.\nReset. Recharge. Repeat.","Good things get repeated.\nReset. Recharge. Repeat.",None,None),
 (11,"الأربعاء","أكتر مشروب بتكرره عندنا؟","The drink you order again and again?",None,None),
 (12,"الأحد","١٢ أسبوع من القعدات الحلوة.\nشكراً إنك كنت جزء منها.","12 weeks of good sittings.\nThank you for being part of them.",None,None),
 (12,"الأربعاء","جود دايز مفتوح من ١٠ الصبح لـ١٢ منتصف الليل.\nالجاي أحلى.","GOOD DAYS is open from 10 AM to 12 AM.\nThe best is next.",None,None),
]
# static captions (key = file stem)
CAP = {
 "w01_mon_reset": ("اهدا. اشحن. كرّر.\nجود دايز في Trio Fitness Hub، من ١٠ الصبح لـ١٢ منتصف الليل.","Reset. Recharge. Repeat.\nGOOD DAYS at Trio Fitness Hub, 10 AM to 12 AM."),
 "w02_mon_quiet_corner": ("مكان تقعد فيه وتنسى الساعة.","A place to sit and lose track of time."),
 "w02_thu_hour_here": ("ساعة عندنا: اقعد، اتنفس، واطلب.","An hour with us: sit, breathe, order."),
 "w03_mon_earned_it": ("بعد التمرين، مشروبك مستنيك.","After the workout, your drink is waiting."),
 "w04_mon_sun": ("ضوء طبيعي وخضرة وترابيزة مستنياك.","Natural light, greenery, and a table waiting."),
 "w04_thu_outside": ("٣ أسباب تقعد برّه: ضوء طبيعي، قعدة في الهوا، وخضرة حواليك.","3 reasons to sit outside: natural light, open air, green all around."),
 "w05_mon_menu": ("منيو كبير وبيتغيّر: قهوتك المعتادة ومشروبات صحية.\nاسأل عن مشروب النهارده.","A big, changing menu: your usual coffee and healthy drinks.\nAsk about today's."),
 "w06_mon_first_coffee": ("أول قهوة في يومك؟ بنفتح ١٠ الصبح.","Your first coffee of the day? We open at 10 AM."),
 "w06_thu_hours": ("مواعيدنا: من ١٠ الصبح لـ١٢ منتصف الليل.\nمفتوح لكل الناس، مش لازم تكون عضو في Trio Fitness Hub.","Open hours: 10 AM to 12 AM.\nOpen to everyone, no Trio Fitness Hub membership needed."),
 "w07_mon_late": ("بنسهر معاك لحد ١٢. القهوة مستنياك.","We stay up with you until 12 AM. Your coffee is waiting."),
 "w08_mon_whole_day": ("يوم كامل في Trio Fitness Hub: تمرين، قهوة، وقعدة.","A full day at Trio Fitness Hub: train, coffee, and a seat to switch off."),
 "w08_thu_no_membership": ("مش لازم تكون عضو. الكافيه مفتوح لكل الناس.","No membership needed. The cafe is open to everyone."),
 "w09_mon_healthy": ("الصحي جنب المعتاد في نفس المنيو.","Healthy, right next to your usual, on the same menu."),
 "w10_mon_company": ("القعدة الحلوة من الناس.","Good company makes it good."),
 "w10_thu_bring": ("جيب صحابك، وخلّي القعدة أحلى.","Bring your people and make the table better."),
 "w11_mon_habit": ("كل زيارة بتبقى عادة. Reset. Recharge. Repeat.","Every visit becomes a habit. Reset. Recharge. Repeat."),
 "w12_mon_earned_part": ("الجزء ده استحقيته.\nYOU EARNED THIS PART.","You earned this part.\nYOU EARNED THIS PART."),
 "w12_thu_thanks": ("شكراً. الجاي أحلى.\nمن ١٠ الصبح لـ١٢ منتصف الليل.","Thank you. The best is next.\n10 AM to 12 AM."),
}
# reel briefs: (week, slug, status, ar_title, brief_ar, brief_en, onscreen_ar, onscreen_en)
REELS = [
 (1,"wk01_tue_gym_to_cafe","جاهز","من الجيم للكافيه (٢٠ث)","ريل جاهز: gooddays/reel/gooddays_reel_20s_delivery.mp4","Ready: gooddays/reel/gooddays_reel_20s_delivery.mp4","YOU EARNED THIS PART.","YOU EARNED THIS PART."),
 (2,"wk02_tue_listen","يتبني من الصور","اسمع المكان (١٥ث)","٤ لقطات بطيئة: كباية بتتحط على الترابيزة، الشمس على الحيطة، الخضرة، ابتسامة. صوت: أوراق شجر وتلج. كابشن واحد في الآخر.","4 slow shots: cup set on the table, sun on the wall, foliage, a smile. Sound: leaves and ice. One caption at the end.","اسمع المكان قبل ما تشوفه.","Hear the place before you see it."),
 (4,"wk04_tue_sun","يتبني من الصور","من الضل للشمس (١٥ث)","لقطتين نفس الزاوية: الترابيزة في الضل ثم في الشمس. نص: «مفيش وقت أحلى من دلوقتي.»","Same angle twice: the table in shade, then in sun. Text: “No better time than now.”","مفيش وقت أحلى من دلوقتي.","No better time than now."),
 (6,"wk06_tue_first_hour","يحتاج تصوير","أول ساعة بعد الفتح (١٥ث)","تصوير ١٠ الصبح: فتح الباب، أول كباية، أول زبون. ٣ لقطات. ينتهي بـ«بنفتح ١٠ الصبح».","Shoot at 10 AM: door opens, first cup, first guest. 3 shots. Ends “We open at 10 AM”.","بنفتح ١٠ الصبح.","We open at 10 AM."),
 (8,"wk08_tue_full_day","يحتاج تصوير","يوم كامل في Trio Fitness Hub (٢٠ث)","٨ لقطات سريعة: تمرين، ممر، الكافيه، كباية، قعدة، الغروب، إضاءة الليل، ١٢. صوت أصلي.","8 fast shots: training, walkway, the cafe, a cup, seating, sunset, night lights, 12 AM. Original sound.","يوم كامل في ٢٠ ثانية.","A full day in 20 seconds."),
 (9,"wk09_tue_pour","يحتاج تصوير","تحضير مشروب (١٥ث)","كلوز-أب لتحضير مشروب من منيو الأسبوع (الخطوات الفعلية بيحددها الباريستا)، من غير أي ادعاء صحي.","Close-up of a drink from the week's menu being made (steps set by the barista), no health claims.","من المنيو: مشروب النهارده.","From the menu: today's drink."),
 (11,"wk11_tue_repeat","يحتاج تصوير","الزبون الدايم (١٥ث)","نفس الزبون في ٣ زيارات (يوم/وقت مختلف) بنفس الكرسي. تصريح استخدام الصورة مطلوب.","The same guest across 3 visits on different days/times, same chair. Written image consent needed.","كل زيارة بتبقى عادة.","Every visit becomes a habit."),
 (12,"wk12_tue_best_of","يتجمّع من اللي قبله","أحسن لحظات ٣ شهور (٢٠ث)","مونتاج من أفضل لقطات الحملة، ينتهي بـ YOU EARNED THIS PART. ومواعيد الشغل.","Montage of the campaign's best shots, ending on YOU EARNED THIS PART. and opening hours.","شكراً. الجاي أحلى.","Thank you. The best is next."),
]
if __name__ == "__main__":
    md = ["# GOOD DAYS: النصوص (عربي + إنجليزي)\n", "## ٢٤ بوست نصي/تفاعلي (فيسبوك + ستوري إنستجرام)\nالاستطلاع يتحوّل لملصق Poll في الستوري وزرار تصويت في فيسبوك.\n"]
    rows = []
    for w, d, ar, en, pa, pe in TEXT:
        md.append(f"### أسبوع {w}، {d}\n**AR:** {ar}\n\n**EN:** {en}\n" + (f"\n**Poll:** {' / '.join(pa)} | {' / '.join(pe)}\n" if pa else "") + f"\n{TAGS_AR}\n")
        rows.append([w, d, "text", ar, en, " / ".join(pa) if pa else "", " / ".join(pe) if pe else ""])
    md.append("## ١٨ كابشن للبوستات الثابتة (الصور في `posts/out/ar|en/`)\n")
    for k, (a, e) in CAP.items():
        md.append(f"### {k}\n**AR:** {a}\n\n**EN:** {e}\n\n{TAGS_AR}\n"); rows.append([k[1:3], "", "static:" + k, a, e, "", ""])
    md.append("## ٨ ريلز: ملخص الإنتاج\n")
    for w, slug, st, title, ba, be, oa, oe in REELS:
        md.append(f"### أسبوع {w}: {title} ({st})\n**AR:** {ba}\n\n**EN:** {be}\n\n**On-screen:** {oa} | {oe}\n"); rows.append([w, "الثلاثاء", "reel:" + slug, ba, be, oa, oe])
    open("content.md", "w", encoding="utf-8").write("\n".join(md))
    with open("content.csv", "w", encoding="utf-8-sig", newline="") as f: wr = csv.writer(f); wr.writerow(["week", "day", "item", "AR", "EN", "extra_AR", "extra_EN"]); wr.writerows(rows)
    print(len(TEXT), len(CAP), len(REELS))
