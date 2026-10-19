"""GOOD DAYS static posts (18). Fields: layout, photo, pos (object-position y %), zoom, ar/en = dict(lines, sub, items, title, big)."""
C = {
 "w01_mon_reset": dict(l="A", p="p6", y=0, ar=dict(lines=["اهدا.", "اشحن.", "كرّر."]), en=dict(lines=["RESET.", "RECHARGE.", "REPEAT."])),
 "w02_mon_quiet_corner": dict(l="A", p="p5", y=40, ar=dict(lines=["ركن هادي.", "وقتك."], sub="مكان تقعد فيه وتنسى الساعة."), en=dict(lines=["A QUIET CORNER.", "YOUR TIME."], sub="Sit down. Lose track of time.")),
 "w02_thu_hour_here": dict(l="C", p="p2", y=40, ar=dict(title="ساعة عندنا", items=["اقعد", "اتنفس", "اطلب"]), en=dict(title="AN HOUR WITH US", items=["Sit.", "Breathe.", "Order."])),
 "w03_mon_earned_it": dict(l="B", p="p8", y=30, ar=dict(lines=["استحقيتها."], sub="بعد التمرين، مشروبك مستنيك."), en=dict(lines=["YOU EARNED IT."], sub="After the workout, your drink is waiting.")),
 "w04_mon_sun": dict(l="B", p="p5", y=100, ar=dict(lines=["الشمس بتحلّي القعدة."], sub="ضوء طبيعي وخضرة وترابيزة مستنياك."), en=dict(lines=["SUN MAKES", "IT BETTER."], sub="Natural light, greenery, and a table waiting.")),
 "w04_thu_outside": dict(l="C", p="p6", y=40, ar=dict(title="٣ أسباب تقعد برّه", items=["ضوء طبيعي", "قعدة في الهوا", "خضرة حواليك"]), en=dict(title="3 REASONS TO SIT OUTSIDE", items=["Natural light", "Open air", "Green all around"])),
 "w05_mon_menu": dict(l="B", p="p3", y=45, ar=dict(lines=["منيو كبير.", "بيتغيّر."], sub="قهوتك المعتادة ومشروبات صحية. اسأل عن مشروب النهارده."), en=dict(lines=["A BIG MENU.", "ALWAYS CHANGING."], sub="Your usual coffee and healthy drinks. Ask about today's.")),
 "w06_mon_first_coffee": dict(l="A", p="p2", y=35, ar=dict(lines=["أول قهوة", "في يومك."], sub="بنفتح ١٠ الصبح."), en=dict(lines=["FIRST COFFEE", "OF THE DAY."], sub="We open at 10 AM.")),
 "w06_thu_hours": dict(l="H", p="p1", y=30, ar=dict(title="مواعيدنا", big="١٠ ص — ١٢ م", sub="مفتوح لكل الناس. مش لازم تكون عضو."), en=dict(title="OPEN HOURS", big="10 AM — 12 AM", sub="Open to everyone. No membership needed.")),
 "w07_mon_late": dict(l="B", p="p1", y=30, ar=dict(lines=["بنسهر معاك", "لحد ١٢."], sub="القهوة مستنياك."), en=dict(lines=["WE STAY UP", "WITH YOU TILL 12."], sub="Your coffee is waiting.")),
 "w08_mon_whole_day": dict(l="S", ps=["p1", "p5", "p2"], ar=dict(title="يوم كامل في Trio Fitness Hub", items=["تمرين", "قهوة", "شغل وقعدة"]), en=dict(title="A FULL DAY AT TRIO FITNESS HUB", items=["Train", "Coffee", "Work & chill"])),
 "w08_thu_no_membership": dict(l="B", p="p2", y=35, ar=dict(lines=["مش لازم", "تكون عضو."], sub="الكافيه مفتوح لكل الناس."), en=dict(lines=["NO MEMBERSHIP", "NEEDED."], sub="The cafe is open to everyone.")),
 "w09_mon_healthy": dict(l="B", p="p1", y=20, ar=dict(lines=["الصحي", "جنب المعتاد."], sub="مشروباتك المعتادة ومشروبات صحية في نفس المنيو."), en=dict(lines=["HEALTHY,", "NEXT TO YOUR USUAL."], sub="Your usual drinks and healthy ones, on one menu.")),
 "w10_mon_company": dict(l="B", p="p7", y=40, ar=dict(lines=["القعدة الحلوة", "من الناس."]), en=dict(lines=["GOOD COMPANY", "MAKES IT GOOD."])),
 "w10_thu_bring": dict(l="A", p="p4", y=50, ar=dict(lines=["جيب صحابك."], sub="وخلّي القعدة أحلى."), en=dict(lines=["BRING", "YOUR PEOPLE."], sub="Make the table better.")),
 "w11_mon_habit": dict(l="A", p="p3", y=40, ar=dict(lines=["كل زيارة", "بتبقى عادة."]), en=dict(lines=["EVERY VISIT", "BECOMES A HABIT."])),
 "w12_mon_earned_part": dict(l="A", p="p6", y=0, ar=dict(lines=["الجزء ده", "استحقيته."]), en=dict(lines=["YOU EARNED", "THIS PART."])),
 "w12_thu_thanks": dict(l="B", p="p5", y=100, ar=dict(lines=["شكراً.", "الجاي أحلى."], sub="من ١٠ ص لـ١٢ م."), en=dict(lines=["THANK YOU.", "THE BEST IS NEXT."], sub="10 AM to 12 AM.")),
}
assert len(C) == 18
