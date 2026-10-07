import os, asyncio, json, certifi
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
import edge_tts
# (spoken text with Arabic transliteration of the brand, on-screen subtitle with Latin brand)
LINES = [
 ("أهلاً، أنا أحمد خيري من كلينستات ريسيرش.", "أهلاً، أنا أحمد خيري من ClinStat Research."),
 ("إحنا متخصصين في الإحصاء الحيوي والأبحاث السريرية، وشغالين في منطقة الخليج.", "إحنا متخصصين في الإحصاء الحيوي والأبحاث السريرية، وشغالين في منطقة الخليج."),
 ("هدفنا نسرّع التجارب السريرية، ونحافظ على سلامة البيانات في كل مرحلة.", "هدفنا نسرّع التجارب السريرية، ونحافظ على سلامة البيانات في كل مرحلة."),
 ("من أهم الأساليب عندنا تحليل البقاء، اللي بيتنبأ بالوقت لحد حدوث أي حدث.", "من أهم الأساليب عندنا تحليل البقاء، اللي بيتنبأ بالوقت لحد حدوث أي حدث."),
 ("وقبل ما أي ورقة بحثية توصل للتحكيم، بنراجع الإحصاء والأخلاقيات ونطابق نطاق المجلة.", "وقبل ما أي ورقة بحثية توصل للتحكيم، بنراجع الإحصاء والأخلاقيات ونطابق نطاق المجلة."),
 ("خليكم معانا، وتابعوا كل جديد في عالم الأبحاث. شكراً ليكم.", "خليكم معانا، وتابعوا كل جديد في عالم الأبحاث. شكراً ليكم."),
]
async def main():
    for i,(t,_) in enumerate(LINES):
        await edge_tts.Communicate(t, "ar-EG-ShakirNeural", rate="-4%", proxy=os.environ["HTTPS_PROXY"]).save(f"cs/line{i}.mp3")
asyncio.run(main())
json.dump([s for _,s in LINES], open("cs/lines.json","w"), ensure_ascii=False)
