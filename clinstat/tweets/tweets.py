"""All 24 tweets (+ the week-12 thread) of the ClinStat 3-month calendar, Arabic and English. python3 tweets.py -> tweets.md, tweets.csv, checks the 280-character limit (links count as 23)."""
import csv, datetime, re
START = datetime.date(2026, 10, 18)      # Sunday; change to the real launch Sunday
DAY = {"Sun": 0, "Wed": 3}
L = "[link]"
T = [  # wk, day, status in calendar, funnel, keyword/UTM tag, ar, en, note
 (1, "Sun", "ready", "EDU", "series", "إيه اللي بيخلّي نتيجة البحث موثوقة فعلًا؟\n\nمش الـp-value لوحدها.\nتصميم سليم، داتا نضيفة، تحليل مناسب، وتقرير شفاف.\n\nعلى مدار 12 أسبوع هنفكّكها نقطة نقطة.\n\nتابعنا لباقي السلسلة.",
  "What actually makes a research result reliable?\n\nNot the p-value alone.\nA sound design, clean data, the right analysis and transparent reporting.\n\nOver 12 weeks we'll unpack each one.\n\nFollow for the rest of the series.", ""),
 (1, "Wed", "ready", "EDU", "series", "محدش بينشر ورقة عن الـduplicate entry اللي اكتشفه في الأسبوع التاني.\n\nبس نتيجتك بتتوقف عليه.\n\nالداتا النضيفة هي اللي بتحدد إن كانت النتيجة ليها معنى.\n\nتابعنا لباقي السلسلة.",
  "Nobody publishes a paper about the duplicate entry they found in week two.\n\nBut your result depends on it.\n\nClean data decides whether a result means anything.\n\nFollow for the rest of the series.", ""),
 (2, "Sun", "ready", "EDU", "feasibility", f"قبل ما تقضي شهور على دراسة، اتأكد من تلات حاجات:\n\n1. سؤالك اتجاوب قبل كده؟\n2. فيه فجوة حقيقية في المعرفة؟\n3. الدراسة ممكن تتنفذ بالموارد المتاحة؟\n\nمش متأكد إن فكرتك جديدة؟ فحص جدوى مجاني 15 دقيقة {L}",
  f"Before you spend months on a study, check three things:\n\n1. Has your question been answered before?\n2. Is there a real gap in knowledge?\n3. Can the study be done with the resources you have?\n\nNot sure your idea is new? Free 15-minute feasibility check {L}", "The three checks are proposed here; the calendar only says 'three things'."),
 (2, "Wed", "ready", "EDU", "checklist", f"دراسة كويسة ممكن تترفض برضه.\n\nمش بسبب العلم، بسبب إحصاء ناقص، أو وثائق أخلاقيات مش مكتملة، أو نطاق مش مناسب للمجلة.\n\nنزّل GCC Submission Checklist المجاني {L}",
  f"A good study can still be rejected.\n\nNot because of the science: because of gaps in the statistics, incomplete ethics documents, or a poor fit with the journal's scope.\n\nDownload the free GCC Submission Checklist {L}", ""),
 (3, "Sun", "ready", "OFFER", "checklist", f"كتير من المخطوطات مبتترفضش بسبب العلم نفسه.\n\nبتترفض لأن ملف التقديم ناقص: إحصاء، أخلاقيات، أو نطاق.\n\nراجع كل ده قبل Submit.\n\nنزّل GCC Submission Checklist المجاني {L}",
  f"Many manuscripts aren't rejected because of the science itself.\n\nThey're rejected because the submission is incomplete: statistics, ethics or scope.\n\nCheck all of it before you press Submit.\n\nDownload the free GCC Submission Checklist {L}", "Sponsored. The calendar says 'most manuscripts'; softened to 'many' because no source is given."),
 (3, "Wed", "ready", "EDU", "results", f"p < 0.05 مش معناها إن دراستك كويسة.\n\nممكن العينة تكون صغيرة، أو التصميم ضعيف، أو التحليل اتختار بعد ما شفت النتيجة.\n\nالـp-value بتجاوب سؤال واحد بس.\n\nمراجعة نتايج مجانية 15 دقيقة {L}",
  f"p < 0.05 doesn't mean your study is good.\n\nThe sample can be small, the design weak, or the analysis chosen after you saw the result.\n\nA p-value answers one question only.\n\nFree 15-minute results review {L}", ""),
 (4, "Sun", "ready", "EDU", "sample", f"رقم واحد لازم تعرفه قبل أول مريض: حجم العينة.\n\nدراسة صغيرة ممكن تفوّت تأثير حقيقي. ودراسة أكبر من اللازم بتضيّع وقت وموارد.\n\nحجم العينة قرار تصميم، مش خطوة في الآخر.\n\nبتخطط لدراسة؟ استشارة مجانية 15 دقيقة {L}",
  f"One number to know before patient one: the sample size.\n\nA small study can miss a real effect. A needlessly large one wastes time and resources.\n\nSample size is a design decision, not a last step.\n\nPlanning a study? Free 15-minute consultation {L}", ""),
 (4, "Wed", "ready", "EDU", "analysis", f"قرار إحصائي غلط واحد ممكن يغيّر استنتاج البحث كله.\n\nاختبار مش مناسب للتوزيع، حذف قيم من غير توثيق، أو مقارنات كتير من غير تصحيح.\n\nمش متأكد إن تحليلك يناسب تصميمك؟ استشارة مجانية 15 دقيقة {L}",
  f"One wrong statistical decision can change a study's whole conclusion.\n\nA test that doesn't fit the distribution, values removed without documentation, or many comparisons with no correction.\n\nUnsure your analysis fits your design? Free 15-min consultation {L}", ""),
 (5, "Sun", "write", "EDU", "howwework", "تلات حاجات مش هنعملها لأي باحث أبدًا:\n\n1. نضمن قبول أو نشر.\n2. نغيّر نتيجة أو نخفي داتا.\n3. ندخل اسمنا مؤلف من غير مساهمة فعلية تحقق معايير ICMJE.\n\nتابعنا لتعرف طريقة شغلنا.",
  "Three things we will never do for any researcher:\n\n1. Guarantee acceptance or publication.\n2. Change a result or hide data.\n3. Add our names as authors without a real contribution that meets the ICMJE criteria.\n\nFollow to see how we work.", "[CONFIRM] The three commitments are proposed; ClinStat must approve them."),
 (5, "Wed", "write", "PROOF", "verification", "مين بيراجع التحليل بعد المحلل؟\n\nتحليل واحد من غير مراجعة هو مجرد رأي.\n\nالتحقق المستقل معناه إن محلل تاني يعيد الخطوات ويقارن النتايج قبل ما أي رقم يوصل للباحث.\n\nتابعنا لمزيد من كواليس المنهجية.",
  "Who checks the analysis after the analyst?\n\nAn analysis nobody has checked is just an opinion.\n\nIndependent verification means a second analyst repeats the steps and compares the results before any number reaches the researcher.\n\nFollow for more behind-the-scenes methodology.", "[CONFIRM] describe the real verification process."),
 (6, "Sun", "ready", "PROOF", "casestudy", f"مخطوطة اترفضت من أكتر من 10 مجلات مش دايمًا دراسة وحشة.\n\nأحيانًا المشكلة في المنهجية أو العرض، وبتتصلّح.\n\nشوف إزاي حالة واحدة وصلت من الرفض للقبول.\n\nدراسة الحالة كاملة على لينكدإن {L}",
  f"A manuscript rejected by 10+ journals isn't always a bad study.\n\nSometimes the problem is the methods or the presentation, and it can be fixed.\n\nSee how one case went from rejection to acceptance.\n\nFull case study on LinkedIn {L}", "[CONFIRM] case details and client approval."),
 (6, "Wed", "ready", "PROOF", "partnership", f"مؤسسة أكاديمية واحدة. حوالي 100 ورقة كل ربع سنة. 80% منشورة في مجلات عالية التأثير.\n\nنفس المعيار في كل ورقة.\n\nاستفسارات الشراكات المؤسسية {L}",
  f"One academic institution. About 100 papers a quarter. 80% published in high-impact journals.\n\nThe same standard on every paper.\n\nInstitutional partnership enquiries {L}", "[CONFIRM] figures and client approval."),
 (7, "Sun", "write", "EDU", "readiness", f"5 علامات إن مخطوطتك مش جاهزة للتقديم:\n\n1. مفيش primary outcome واضح\n2. الـmethods مش قابلة للتكرار\n3. وثائق الأخلاقيات ناقصة\n4. الـreporting guideline مش متّبع\n5. المجلة اتختارت بعد ما خلّصت الكتابة\n\nقيّم نفسك بـManuscript Readiness Checklist {L}",
  f"5 signs your manuscript isn't ready:\n\n1. No clear primary outcome\n2. Methods nobody can reproduce\n3. Missing ethics documents\n4. No reporting guideline followed\n5. Journal chosen after the writing\n\nScore yourself: free Manuscript Readiness Checklist {L}", ""),
 (7, "Wed", "write", "EDU", "ownership", f"\"هل ده ghostwriting؟\"\n\nلأ. إنت المؤلف: بتحتفظ بالملكية الفكرية والموافقة النهائية والمسؤولية.\n\nإحنا بندعم الجانب الإحصائي والمنهجي، ومش بنكتب بحثك باسمك.\n\nاقرأ طريقة شغلنا {L}",
  f"\"Is this ghostwriting?\"\n\nNo. You are the author: you keep the intellectual property, the final approval and the responsibility.\n\nWe support the statistical and methodological side. We don't write your research under your name.\n\nRead how we work {L}", "[CONFIRM] policy wording."),
 (8, "Sun", "ready", "PROOF", "mentoring", f"الهدف عمره ما كان إن الباحثين يفضلوا معتمدين علينا.\n\nكل مشروع بنحاول نسيب فيه الباحث أقدر يحلل ويفسّر ويدافع عن نتيجته بنفسه.\n\nمن باحث مدعوم لباحث مستقل.\n\nاسأل عن برامج الإرشاد عندنا {L}",
  f"The goal was never for researchers to stay dependent on us.\n\nIn every project we try to leave the researcher able to analyse, interpret and defend their own result.\n\nFrom supported researcher to independent researcher.\n\nAsk about our mentoring programmes {L}", ""),
 (8, "Wed", "write", "EDU", "services", f"ست ممارسات. معيار واحد.\n\n1. خطة تحليل قبل الداتا\n2. توثيق كل خطوة\n3. تحقق مستقل\n4. الأخلاقيات أولًا\n5. تقرير شفاف\n6. الباحث يحتفظ بملكية بحثه\n\nشوف خدماتنا {L}",
  f"Six practices. One standard.\n\n1. An analysis plan before the data\n2. Every step documented\n3. Independent verification\n4. Ethics first\n5. Transparent reporting\n6. The researcher keeps ownership\n\nSee our services {L}", "[CONFIRM] the six practices are proposed."),
 (9, "Sun", "ready", "EDU", "pico", f"لقيت تلات أو أربع أوراق؟ ده مش معناه تلقائيًا إنك تقدر تعمل meta-analysis.\n\nلازم: سؤال محدد (PICO)، دراسات متشابهة كفاية، ونتايج بنفس المقياس.\n\nابعتلنا الـPICO بتاعك لمراجعة جدوى مجانية {L}",
  f"Found three or four papers? That doesn't automatically mean you can run a meta-analysis.\n\nYou need a defined question (PICO), studies similar enough, and outcomes on the same measure.\n\nSend us your PICO for a free feasibility review {L}", ""),
 (9, "Wed", "edit", "EDU", "overlap", f"ورقتين. مجموعة مرضى واحدة. إنت عدّيتهم مرتين.\n\nلما دراستين بتنشر نفس المرضى (أو جزء منهم)، دخول الاتنين في meta-analysis بيضخّم الدقة ويزوّد التحيّز.\n\nهنفحص الدراسات المدرجة عندك لاكتشاف التداخل، مجانًا {L}",
  f"Two papers. One group of patients. You counted them twice.\n\nWhen two studies report the same patients (or some of them), including both in a meta-analysis overstates precision and adds bias.\n\nWe'll check your included studies for overlap, free {L}", ""),
 (10, "Sun", "edit", "EDU", "bias", f"الـmeta-analysis بتاعتك فيها الدراسات اللي اتنشرت بس.\n\nالدراسات اللي نتيجتها مش معنوية بتتنشر أقل، فالتقدير المجمّع ممكن يتضخم. الـfunnel plot بيساعد تشك في ده، لكنه مش بيحسمه.\n\nمراجعة مجانية لتقييم الـbias عندك {L}",
  f"Your meta-analysis only contains the studies that got published.\n\nNon-significant studies are published less often, so the pooled estimate can be inflated. A funnel plot helps you suspect it, but doesn't settle it.\n\nFree review of the bias in your work {L}", ""),
 (10, "Wed", "edit", "EDU", "grade", f"التقدير المجمّع مش هو نفسه الدليل المؤكد.\n\nالـGRADE بيقيّم certainty of evidence: risk of bias، inconsistency، indirectness، imprecision، وpublication bias.\n\nهنساعدك تخطط لتقييم certainty of evidence، مجانًا {L}",
  f"A pooled estimate isn't the same as certain evidence.\n\nGRADE rates the certainty of evidence: risk of bias, inconsistency, indirectness, imprecision and publication bias.\n\nWe'll help you plan the certainty-of-evidence assessment, free {L}", ""),
 (11, "Sun", "write", "OFFER", "consult", f"لسه بتفكر؟\n\n15 دقيقة مجانية عن بحثك. من غير أي التزام.\n\nاحجز استشارتك المجانية 15 دقيقة {L}",
  f"Still thinking about it?\n\n15 free minutes about your research. No obligation.\n\nBook your free 15-minute consultation {L}", "Sponsored."),
 (11, "Wed", "approval", "PROOF", "testimonial", f"[اقتباس عميل معتمد: يُستخدم فقط بعد موافقة كتابية]\n\n— [الاسم / المؤسسة]\n\nاحجز استشارة مجانية {L}",
  f"[Approved client quote: use only after written approval]\n\n— [Name / institution]\n\nBook a free consultation {L}", "PLACEHOLDER: do not publish without the client's written approval."),
 (12, "Wed", "write", "OFFER", "consult", f"مواعيد الاستشارة متاحة الأسبوع ده.\n\n15 دقيقة مجانية لمراجعة تصميمك أو تحليلك أو مخطوطتك.\n\nاحجز استشارة مجانية 15 دقيقة {L}",
  f"Consultation slots are open this week.\n\n15 free minutes to review your design, your analysis or your manuscript.\n\nBook a free 15-minute consultation {L}", "[CONFIRM] availability."),
]
THREAD = (12, "Sun", "write", "EDU", "thread", [
 "3 شهور من معايير البحث، في thread واحد.\n\nاحفظه. (1/6)",
 "1) التصميم: الفرضية والـprimary outcome وحجم العينة قبل أول مريض. (2/6)",
 "2) الداتا: افحص التكرارات والقيم الناقصة والمتطرفة. نتيجة قوية ممكن تطلع من خطأ إدخال. (3/6)",
 "3) التحليل: افحص افتراضات الاختبار، اختار الـtest من التصميم مش من p < 0.05، وصحّح تعدد الاختبارات. (4/6)",
 "4) التقرير: اتبع الـreporting guideline المناسب، وانشر كل النتايج المخطط لها حتى غير المعنوية. (5/6)",
 f"5) النشر: وثائق الأخلاقيات، معايير ICMJE للتأليف، ومجلة مناسبة.\n\nاحفظ الـthread. استشارة مجانية {L} (6/6)"],
 ["Three months of research standards, in one thread.\n\nSave it. (1/6)",
  "1) Design: the hypothesis, primary outcome and sample size before patient one. (2/6)",
  "2) Data: check duplicates, missing values and outliers. A strong result can come from an entry error. (3/6)",
  "3) Analysis: check test assumptions, pick the test from the design rather than from p < 0.05, and correct for multiple testing. (4/6)",
  "4) Reporting: follow the right reporting guideline and publish every pre-specified outcome, even non-significant ones. (5/6)",
  f"5) Publishing: ethics documents, ICMJE authorship criteria, and a suitable journal.\n\nSave the thread. Free consultation {L} (6/6)"])
def date(wk, day): return START + datetime.timedelta(days=(wk - 1) * 7 + DAY[day])
def n(s): return len(s.replace(L, "x" * 23))
def utm(wk, kw): return f"?utm_source=x&utm_medium=organic_social&utm_campaign=clinstat_2026q4&utm_content=clinstat_x_tweet_wk{wk}_{kw}"
rows = []
for wk, day, st, fu, kw, ar, en, note in T: rows.append((wk, day, str(date(wk, day)), st, fu, kw, ar, en, note))
rows.append((12, "Sun", str(date(12, "Sun")), "write", "EDU", "thread", "\n\n---\n\n".join(THREAD[5]), "\n\n---\n\n".join(THREAD[6]), "Thread of 6 tweets."))
rows.sort(key=lambda r: (r[0], DAY[r[1]]))
bad = 0
with open("tweets.md", "w", encoding="utf-8") as f:
    f.write("# ClinStat: 24 tweets (3-month calendar)\n\nArabic first, English below each. Limit 280 characters per tweet (a link counts as 23). `[link]` = your UTM link: `<URL>` + the UTM string shown. Start date: Sunday 18 Oct 2026 (change in `tweets.py`).\n\n")
    for wk, day, d, st, fu, kw, ar, en, note in rows:
        parts_ar = ar.split("\n\n---\n\n"); parts_en = en.split("\n\n---\n\n")
        for a, e in zip(parts_ar, parts_en):
            for s in (a, e):
                if n(s) > 280: bad += 1; print("TOO LONG", wk, day, n(s))
        f.write(f"## Week {wk}, {day} ({d}) — {fu} — {st}\n\n**AR**\n\n```\n{ar}\n```\n\n**EN**\n\n```\n{en}\n```\n\nUTM: `{utm(wk, kw)}`  \nCharacters (AR / EN): {' + '.join(str(n(x)) for x in parts_ar)} / {' + '.join(str(n(x)) for x in parts_en)}" + (f"  \nNote: {note}" if note else "") + "\n\n")
with open("tweets.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["week", "day", "date", "calendar_status", "funnel", "utm_suffix", "chars_ar", "chars_en", "tweet_ar", "tweet_en", "note"])
    for wk, day, d, st, fu, kw, ar, en, note in rows: w.writerow([wk, day, d, st, fu, utm(wk, kw), max(n(x) for x in ar.split("\n\n---\n\n")), max(n(x) for x in en.split("\n\n---\n\n")), ar, en, note])
print("tweets:", len(rows), "problems:", bad)
