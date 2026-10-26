import base64
img=base64.b64encode(open("ref.jpg","rb").read()).decode()
def tbl(head,rows,cls=""):
    h="".join(f"<th>{x}</th>" for x in head)
    r="".join("<tr>"+"".join(f"<td>{c}</td>" for c in row)+"</tr>" for row in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'
V='<span class="b v">Verified</span>';O='<span class="b o">Marketer-reported</span>';P='<span class="b p">Public report</span>';H='<span class="b h">Hypothesis</span>';N='<span class="b n">NEED</span>';R='<span class="b r">Recommendation</span>'
def sec(i,t,body,lead=""):
    return f'<section id="d{i}"><header class="sh"><span class="no">{i}</span><div><h2>{t}</h2>{("<p class=lead>"+lead+"</p>") if lead else ""}</div></header>{body}</section>'
S=[]
# 1
S.append(sec(1,"Executive summary",f'''
<div class="kpis"><div><b>Stage</b><span>Pre-opening. Premises contracted, not yet designed</span></div><div><b>Opening window</b><span>1 to 3 months (marketer-reported)</span></div><div><b>Product</b><span>Specialty coffee with desserts and pastries</span></div><div><b>Ad budget</b><span>EGP 5,000 to 15,000 per month, excluding fees</span></div></div>
<p><b>Business.</b> مسكوب (MASKOOB Café) is a new café in 10th of Ramadan City, Sharqia. Everything below that concerns the business itself comes from the marketer's own briefing in this session {O}. Searches on 26 Oct 2026 found no public footprint for the name (no Instagram, Facebook, Maps listing or website), which is consistent with a business that has not opened.</p>
<p><b>What this means.</b> There is no live brand to audit and no public customer data. The work is therefore a <em>pre-launch</em> engagement: confirm the identity, finish the visual system while the premises are still undesigned, then run a short, measurable launch.</p>
<p><b>Preliminary opportunity.</b> The city is a very large industrial employment base ({P} Al-Ahram, Sept 2025: about 6,000 companies and 400,000 workers, as stated by the head of the investors association). Public directory listings show only a few organised cafés. That does not prove an unmet need. It is a <em>hypothesis</em> that a distinctive specialty café with a strong identity can own a clear position, to be tested by field research in the first two weeks.</p>
<p><b>Biggest decision now.</b> The premises are contracted but undesigned, so the identity can still shape the interior brief. That is the highest-leverage and time-limited part of the engagement.</p>
<div class="note">Not claimed anywhere in this document: revenue forecasts, guaranteed results, competitor performance, or owner approval of any brand direction.</div>''', "Built from the briefing, the supplied concept board and public research."))
# 2
S.append(sec(2,"Client intelligence profile",f'''
<p>Each field shows value, source and confidence. Searches run on 26 Oct 2026 in Arabic and English.</p>
{tbl(["Field","Value","Source","Confidence"],[
["Arabic name","مسكوب (primary)","Marketer briefing","High as an instruction; not publicly verifiable"],
["English spelling","MASKOOB Café (provisional)","Briefing","Low. Owner must confirm spelling"],
["City / governorate","10th of Ramadan City, Sharqia","Marketer answer in this session","High as an instruction"],
["Street, neighbourhood, phase","[NEED]","None","n/a"],
["Business stage","Not opened. Premises contracted, not designed. Opening in 1 to 3 months","Marketer answer","Medium. Dates not confirmed by owner"],
["Product direction","Specialty coffee with desserts and pastries","Marketer answer","Medium. Menu not seen"],
["Commercial relationship","Client, contract pending","Marketer answer","High as an instruction"],
["Owner name, decision-maker, contact","[NEED]","None","n/a"],
["Instagram / Facebook / TikTok","None found. [NEED handles]","Web searches 26 Oct 2026","Medium. Search coverage is limited"],
["Google Maps listing, website, menu, hours, reviews","None found. [NEED]","Web searches 26 Oct 2026","Medium"],
["Ambiguity check","No other business named مسكوب or Maskoob surfaced in results for Egypt","Web searches 26 Oct 2026","Low. Search is not exhaustive. Confirm handles with the owner before publishing"],
])}
<h3>About the city (public context)</h3>
{tbl(["Fact","Detail","Source and date"],[
["Location","Sharqia governorate, about 46 km from Cairo on the Cairo to Ismailia desert road; founded 1977; about 384 km²","<a href='https://www.edarabia.com/ar/%d9%87%d9%84-%d8%aa%d8%b9%d9%84%d9%85-%d8%b4%d9%8a%d8%a6%d8%a7-%d8%b9%d9%86-%d9%85%d8%af%d9%8a%d9%86%d8%a9-%d8%a7%d9%84%d8%b9%d8%a7%d8%b4%d8%b1-%d9%85%d9%86-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-%d8%9f/'>Edarabia</a>, undated"],
["Industrial base","About 6,000 companies and 400,000 workers (statement by investors association head)","<a href='https://gate.ahram.org.eg/News/5287558.aspx'>Al-Ahram Gate</a>, 17 Sept 2025"],
["Factory count","About 2,700 factories in 2018; a later ministerial statement cites 2,997 factories and 500,000 jobs (undated)","<a href='https://www.masrawy.com/news/news_regions/details/2018/7/26/1400284/'>Masrawy</a>, 2018; figures differ by date and definition"],
["Population","[NEED]. No current figure found. Check CAPMAS","Not found"],
])}''', "Verified facts, owner-provided facts and gaps, kept apart."))
# 3
S.append(sec(3,"Brand audit",f'''
<p>MASKOOB has no operating presence, so there is no existing brand to audit. What can be assessed is the <strong>supplied concept board</strong>, which I inspected directly. It is a visualization, not an approved identity.</p>
<figure><img src="data:image/jpeg;base64,{img}" alt="Supplied MASKOOB concept board: wordmark, palette, materials, applications"><figcaption>Supplied concept board. Reference only. Labeled as visualization.</figcaption></figure>
{tbl(["#","Observation","Evidence","Business implication","Improvement","Priority","Effort"],[
["1","The wordmark is the strongest asset. A single flowing script with a long swash reads as hand-poured and fits the name","Board, section 01","Memorable and ownable if the artwork is rebuilt properly","Rebuild as clean vector by a lettering designer. Do not use the generated artwork in production","High","Medium"],
["2","The tagline lockup uses thin rules on both sides","Section 01 and cup mockups","Thin strokes and small tagline text disappear on cups, sleeves and small social avatars","Create a compact logo without tagline. Set a minimum size for the lockup","High","Low"],
["3","The palette is coherent. Blue is controlled and warm neutrals dominate","Section 02","Distinctive among cafés that default to brown and green","Lock Deep Blue as the primary and give each colour a role (see 6)","Medium","Low"],
["4","Terrazzo pattern is rich on cups and menus","Sections 05 to 07","Pattern behind small Arabic text hurts legibility and raises print cost","Use pattern as a border or panel only. Keep text on flat colour","High","Low"],
["5","Sand (#AA9470) and Dusty Blue (#587B90) on Chalk White have low contrast (see 6)","Computed contrast","Unsafe for body text and small labels","Use for fills, lines and large type only","High","Low"],
["6","Interior mood shows arches, olive trees, terrazzo counter and blue seating","Sections 08 and hero","Attractive but costly. The premises are contracted and undesigned, so feasibility is unknown","Prepare a tiered interior brief: essential, preferred, optional","High","Medium"],
["7","Menu mock contains [price] placeholders","Section 07","Sample only","Do not publish until real products and prices are confirmed [NEED]","Medium","Low"],
])}
<p class="small">Interior and signage cannot be assessed because no photographs of the real premises are available. [NEED REAL PHOTOGRAPHS]</p>''', "No live brand exists yet. This audits the proposed concept."))
# 4
S.append(sec(4,"Local market and competitor analysis",f'''
<p><strong>Evidence status.</strong> Searches in Arabic and English returned no reviews, ratings or social pages for cafés in 10th of Ramadan City. The only local evidence is directory listings, with no performance data. The matrix below is therefore a <em>research worklist</em>, not a finding.</p>
{tbl(["Candidate","Location (as listed)","Source","What is verified","What is unknown"],[
["Star View Cafe","El Ordoneya, inside El Gawhara Mall, ground floor","<a href='https://yellowpages.com.eg/en/map-category/cafes-and-coffee-shops/p161'>Yellow Pages Egypt</a>","Listing exists","Menu, price, social accounts, reviews, current status"],
["Amazon Coffee Shop","El Ordeneya, inside El Ordeneya Center, Phase 3, first floor","<a href='https://yellowpages.com.eg/en/map-category/cafes-and-coffee-shops/p59'>Yellow Pages Egypt</a>","Listing exists","Same"],
["Ekhnatoun Restaurant & Cafe","Abou Bakr El Seddik St, El Ordoneya, inside El Hegaz International Center, shop 13","<a href='https://yellowpages.com.eg/en/map-category/cafes-and-coffee-shops/p161'>Yellow Pages Egypt</a>","Listing exists","Same"],
["Others [NEED]","Add 2 to 5 more from Google Maps and Instagram","Field research","n/a","n/a"],
])}
<h3>Field research protocol (week 1)</h3>
<ol><li>On Google Maps, search "كافيه" and "قهوة مختصة" within 5 km of the premises. Record rating, review count, review themes, photos, hours.</li><li>On Instagram, search city hashtags and tagged locations. Record posting frequency and format mix. Do not treat followers as sales.</li><li>Visit the shortlisted cafés at two day parts. Note price of a flat white or cappuccino and a dessert, seating, crowd and Wi-Fi.</li><li>Include non-café substitutes: mall food courts, bakeries, delivery chains, factory canteens.</li></ol>
<h3>Market context</h3>
<p>A secondary publisher estimates Egypt's coffee-shop market at <strong>USD 1.8 billion in 2025</strong>, growing at about 4.6% a year to 2034 ({P} <a href="https://deepmarketinsights.com/vista/insights/coffee-shops-market/egypt">Deep Market Insights</a>; methodology not visible, treat as indicative). Euromonitor reports specialty coffee leading café-category growth in 2025 ({P} <a href="https://www.euromonitor.com/cafes-bars-in-egypt/report">Euromonitor</a>, paywalled). Neither is specific to 10th of Ramadan City.</p>
<h3>Gap hypotheses, ranked</h3>
{tbl(["Hypothesis","Impact","Evidence confidence","Effort","Cost","Time to test"],[
["Distinctive Arabic identity and a place worth photographing is rare locally","High","Low","Medium","Medium","2 weeks (field research)"],
["Specialty coffee with an easy-to-read menu is under-served near workplaces","High","Low","Low","Low","2 to 4 weeks (soft-opening data)"],
["Local search presence (Google Business Profile) is weak across competitors","Medium","Low","Low","Low","1 week (check listings)"],
["Takeaway for shift workers and office staff is a repeat-visit driver","High","Low","Low","Low","First month of trading"],
["Corporate orders and meeting-room demand from factories and offices","Medium","Low","Medium","Low","Outreach test in month 2"],
["Dessert and pastry range can lift average ticket","Medium","Low","Medium","Medium","Menu test"],
])}
<p class="small">Every row stays a hypothesis until field research or opening-month data confirms it.</p>''', "A worklist with honest evidence labels."))
# 5
S.append(sec(5,"Customer and positioning hypotheses",f'''
<p>No customer data exists for MASKOOB. These segments are {H} derived from location, product and the city's profile.</p>
{tbl(["Segment","Need and occasion","Why choose MASKOOB","Why not","Discovery","Test"],[
["Office and admin staff in nearby companies","Morning takeaway, meetings, breaks","Quality coffee and a calm space","Price, distance, short breaks","Maps, WhatsApp groups, referrals","Offer card at nearby offices"],
["Local residents","Evening seating, desserts, meeting friends","A new, photogenic place","Habit, prices, parking","Instagram, Facebook, word of mouth","Opening-week traffic count"],
["Business owners and visiting professionals","Meetings, hosting guests","Professional setting for conversations","Wi-Fi, privacy, seating","Referrals, Maps","Short interview with 5 owners"],
["Specialty coffee enthusiasts","Better beans and brewing","Credible craft and clear menu","If quality is not proven","Instagram, coffee communities","Cupping or tasting event"],
["Groups and families","Weekend outing, dessert","Atmosphere, dessert range","Seating capacity, noise","Instagram, Facebook","Weekend promos"],
["Students [if relevant]","Study, low-cost drinks","Study-friendly zone","Price sensitivity","Campus groups","Check if universities are near"],
])}
<p><strong>Validation.</strong> Five owner interviews, ten quick intercept conversations near the site, a two-question card at the soft opening, and A/B tested messages on a small ad budget. Segments that do not show repeat intent get dropped.</p>''', "Hypotheses with a plan to prove or drop them."))
# 6 brand strategy + guidelines
sw=[("Chalk White","#E5E5DF","229, 229, 223","Primary background"),("Light Greige","#C5C6C1","197, 198, 193","Secondary neutral, dividers"),("Sand","#AA9470","170, 148, 112","Warm accent, fills, large type"),("Rust Brown","#75432D","117, 67, 45","Earthy accent, text on light"),("Slate Grey","#7C8788","124, 135, 136","Material cue, icons, captions (large)"),("Dusty Blue","#587B90","88, 123, 144","Secondary blue, shapes"),("Deep Blue","#24485F","36, 72, 95","Primary brand colour"),("Charcoal","#303938","48, 57, 56","Body text, dark neutral")]
swatches="".join(f'<div class="sw"><i style="background:{h}"></i><b>{n}</b><code>{h}</code><span>RGB {r}</span><small>{u}</small></div>' for n,h,r,u in sw)
S.append(sec(6,"Brand strategy and identity guidelines",f'''
<h3>Strategy (all items need owner validation)</h3>
{tbl(["Element","Proposal {working}","Status"],[
["Brand purpose","Make a good cup of coffee feel like a small occasion","[NEED OWNER VALIDATION]"],
["Brand promise","Specialty coffee, made with care, in a space that feels considered","[NEED OWNER VALIDATION]"],
["Positioning (draft)","For people in 10th of Ramadan who want better coffee and a place to meet, MASKOOB is the specialty café with a distinct Arabic character and warm, contemporary space","Hypothesis"],
["Personality and voice","Warm, calm, precise. Friendly Egyptian Arabic, short sentences, no hype","Proposal"],
["Values","Craft, welcome, consistency","[NEED OWNER VALIDATION]"],
["Customer experience principles","Clear menu, fast takeaway, knowledgeable staff, consistent quality","Proposal"],
["Reasons to believe","Beans and equipment, barista training, menu clarity [all NEED]","[NEED]"],
["Mission and vision","Not drafted. Needs the owner's input","[NEED]"],
])}
<h3>Tagline options</h3>
<ul><li><strong>قهوة بطابعها</strong> (working suggestion, supplied). Short and ties to the "character" idea. Check that "بطابعها" reads naturally to local customers.</li><li><strong>اتسكبت على مهلها</strong>: plays on the name; slower, relaxed tone.</li><li><strong>مسكوب… وبس</strong>: playful, colloquial, short.</li></ul>
<p class="small">Options two and three are drafts for owner and customer testing, not approved lines. Have a native copywriter review them.</p>
<h3>When the Mediterranean direction may not fit</h3>
<ul><li>If the premises cannot support terrazzo, arches or generous seating, the identity must still work on flat colour and simple materials.</li><li>If the local customer expects a lively, sociable, lower-price venue, a calm minimal look may feel formal. Test with the interviews.</li><li>If specialty coffee is not yet understood locally, the brand needs education content, not just aesthetics.</li></ul>
<h3>Colour system</h3>
<div class="sws">{swatches}</div>
<p class="small">Values are approximate screen references from the supplied board, not sampled from physical materials. CMYK and Pantone are [NEED] until print proofs exist.</p>
<h4>Contrast checks (WCAG ratios computed from the HEX values)</h4>
{tbl(["Pair","Ratio","Use"],[
["Charcoal on Chalk White","9.39","Body text. Passes AA and AAA"],
["Deep Blue on Chalk White","7.66","Headlines and links. Passes AA and AAA"],
["Rust Brown on Chalk White","6.39","Accent text. Passes AA"],
["Chalk White on Deep Blue","7.66","Reversed logo. Passes AA and AAA"],
["Light Greige on Deep Blue","5.64","Secondary text on blue. Passes AA"],
["Sand on Deep Blue","3.31","Large text only (3:1)"],
["Dusty Blue on Chalk White","3.57","Large text and graphics only"],
["Slate Grey on Chalk White","2.92","Decorative only. Fails for text"],
["Sand on Chalk White","2.31","Decorative only. Never for text"],
])}
<p><strong>Digital hierarchy (illustrative, not the interior ratio).</strong> Chalk White and Greige for backgrounds, Deep Blue for headlines and key surfaces, Charcoal for body, Sand and Rust for highlights, Dusty Blue and Slate for supporting shapes. The identity must still read without the terrazzo pattern.</p>
<h3>Typography</h3>
{tbl(["Role","Typeface","Notes"],[
["Arabic wordmark","Custom lettering (supplied concept)","Rebuild and proof in vector. Do not use generated artwork as final"],
["Arabic headlines","Amiri (Regular, Bold)","Expressive, high contrast. Check licence (SIL OFL) and test at small sizes"],
["Arabic body and UI","Cairo (Regular, SemiBold)","Highly legible. Also supplies Latin text, so two families cover everything"],
["Scale","Headline 32 to 48, subhead 20 to 24, body 16 to 18, caption 13 to 14","Line height 1.7 for Arabic body; right-aligned"],
])}
<h3>Logo system</h3>
<ul><li><strong>Primary:</strong> Arabic wordmark with tagline lockup.</li><li><strong>Compact:</strong> wordmark alone for cups, avatars, stamps.</li><li><strong>One-colour and reversed:</strong> Deep Blue on light, Chalk White on Deep Blue.</li><li><strong>Clear space:</strong> equal to the height of the wordmark's tall letter on every side. Minimum size to be set after the vector rebuild [NEED].</li><li><strong>Misuse:</strong> no stretching, no pattern behind the wordmark, no low-contrast colours, no effects.</li></ul>
<h3>Graphic language and photography</h3>
<ul><li><strong>Pour line:</strong> single thin line, used as divider or link between sections.</li><li><strong>Terrazzo pattern:</strong> border or panel only; keep text on flat colour.</li><li><strong>Type grid:</strong> margins based on the wordmark's proportions.</li><li><strong>Photography:</strong> soft natural side light, warm neutral grading, hands and process shots, wide interiors in daylight. Real MASKOOB photographs for final use; concept images stay labeled as visualizations. Get written consent from anyone identifiable.</li></ul>
<h3>Applications (concepts only, none approved)</h3>
<p>Signage, brand wall, cups and sleeves, bags, menu, aprons, loyalty card, social posts, ads. Concept mockups appear on the supplied board. Final artwork needs the rebuilt logo, confirmed prices and real photography.</p>''', "A usable system, with every limit stated."))
# 7 marketing strategy
S.append(sec(7,"Marketing strategy",f'''
<p>Plan assumes an opening in 1 to 3 months, an ad budget of EGP 5,000 to 15,000 a month, and specialty coffee with desserts and pastries. All stay assumptions until the owner confirms.</p>
<h3>Phases</h3>
{tbl(["Phase","Timing","Goal","Main actions"],[
["Foundation","Weeks 1 to 2","Verify and align","Field research, owner interview, confirm handles, interior brief, logo rebuild"],
["Pre-launch","Weeks 3 to 6","Build a reason to visit","Create Instagram, Facebook, Google Business Profile; behind-the-scenes content; waitlist for soft opening"],
["Soft opening","1 to 2 weeks before","Learn quietly","Invited groups, feedback card, real photography"],
["Launch","Opening month","Trial and first repeat","Local ads, offer card for nearby offices, opening events"],
["Retention","Month 2 onward","Habit","Loyalty card, new item drops, feedback loop"],
])}
<h3>Channels</h3>
{tbl(["Channel","Fit","Notes"],[
["Instagram and Reels","High","Primary visual channel. Product, process, space"],
["Facebook","High in this market","Local reach and ads; check audience on the ground"],
["Google Business Profile and Maps","High","Directions and reviews drive walk-ins. Set up before opening"],
["Paid social (Meta)","Medium","Small local tests only"],
["TikTok","Medium","Short videos reuse; confirm resources first"],
["WhatsApp (broadcast, groups)","Medium","Opt-in only. Good for office orders"],
["Local partnerships and referrals","High","Companies, gyms, bakeries, pharmacies"],
])}
<h3>Conversion path</h3>
<p>Discover on Instagram, Facebook or Maps → see menu and photos → check location, hours and phone → visit or order takeaway → leave a review. Needs accurate address, a clear menu link, Maps pin, a phone or WhatsApp number [NEED]. Do not assume delivery, reservations or online ordering exist.</p>
<h3>Retention</h3>
<p>Paper or digital loyalty card, a "bring a colleague" mechanism, seasonal drinks, a review request after the first visit. Collect contact details only with a stated purpose and consent; check the Egyptian Personal Data Protection Law (Law 151 of 2020) with legal counsel before building any customer database.</p>''', "Sequenced around the opening date."))
# 8 content
S.append(sec(8,"Content strategy and 30-day pre-launch calendar",f'''
{tbl(["Pillar","Objective","Formats","Example","Needs","CTA","Metric"],[
["Products and drinks","Show what is on offer","Close-ups, Reels","First pour of the house espresso","Real photography","Save and follow","Saves, shares"],
["Atmosphere","Build the feeling","Photo series, short video","Construction to final materials","Access to site","Follow for the opening","Followers, reach"],
["Craft and quality","Earn trust","Process Reels, carousels","How we dial in a shot","Barista time","Comment a question","Comments"],
["People and community","Local belonging","Team intros, neighbours","The team behind the bar","Consent","Tag a friend","Tags"],
["Offers and conversion","Drive the first visit","Stories, ads","Opening-week invite","Confirmed offer","Directions, WhatsApp","Direction taps, visits"],
])}
<h3>Calendar (placeholders in [ ]; nothing below is a confirmed product, price or hour)</h3>
{tbl(["Week","Day","Format","Idea","Arabic caption (draft)"],[
["1","1","Post","Announce the name and the idea","مسكوب جاي. كوباية قهوة بطابعها، في العاشر من رمضان"],
["1","3","Reel","Meaning of the name: pour","سكبة واحدة، وتبقى اللحظة. تابعونا"],
["1","5","Story","Poll: what do you want to see first?","إيه أول حاجة نفسك تشوفها عندنا؟"],
["2","8","Carousel","From idea to site: the design journey","من الورقة للمكان. مسكوب بتتبني"],
["2","10","Reel","Wordmark animation","اسمنا بيتكتب بإيدنا"],
["2","12","Post","Materials: terrazzo, wood, blue","خامات المكان، واحدة واحدة"],
["3","15","Reel","Meet the coffee [bean origin NEED]","من أنهي بن؟ هنحكيلكم قريب"],
["3","17","Story","Behind the bar: equipment","جهزنا الأجهزة. باقي حاجة صغيرة"],
["3","19","Post","Desserts and pastries preview [NEED menu]","حلويات تستاهل [اسم المنتج]"],
["4","22","Reel","Team preview","ناسنا اللي هيستقبلوكم"],
["4","25","Post","Soft-opening invitation [date, NEED]","دعوة خاصة. [التاريخ] في [العنوان]"],
["4","28","Reel","Countdown and directions","الأسبوع الجاي نفتح. هنستناكم"],
])}
<p class="small">Copy is in friendly Egyptian Arabic and avoids exaggeration. No testimonials, prices or opening hours are invented.</p>''', "Built for a 1 to 3 month runway."))
# 9 commercial opportunity
S.append(sec(9,"Commercial opportunity assessment",f'''
<p>Top opportunities, each with the reasoning and its limits.</p>
{tbl(["#","Opportunity","Why it may matter","Limit"],[
["1","Shape the interior brief with the identity before design is locked","Premises are contracted but undesigned. Cheap to fix now, expensive later","Needs the owner's budget for materials [NEED]"],
["2","Own the Google Maps and Instagram presence before opening","No footprint exists today, so a complete profile is a clean start","Needs address and phone [NEED]"],
["3","A distinctive Arabic wordmark as a recognisable local asset","Few local cafés appear to use strong Arabic identity (unverified)","Depends on field research"],
["4","Workplace takeaway offer for nearby companies","Large employment base in the city (Al-Ahram, Sept 2025)","Distance and shift patterns unknown"],
["5","A short, measured launch test on a modest ad budget","Budget range supports small local tests","Attribution to sales is weak"],
])}
<p><strong>Limits.</strong> Social popularity is not sales. The city's industrial scale is not proof of demand for a premium café. Prices and costs are unknown.</p>''', "Where marketing can plausibly help, and where it cannot."))
# 10 pitch
S.append(sec(10,"Performance framework, service options and client pitch",f'''
<h3>Paid media framework (no cost or result assumptions)</h3>
{tbl(["Objective","When","Needed before spend"],[
["Local awareness","Pre-launch and launch","Real photos, location, Maps pin"],
["Video engagement","Pre-launch","Reels ready"],
["Directions and calls","Launch month","Verified address, phone"],
["Offer redemption","Launch month","Confirmed offer and a way to count redemptions"],
["Retention","Month 2+","Loyalty mechanism and consent"],
])}
<p>Start with two small tests (two audiences, two creatives) for 7 to 10 days, then decide. Agency fees are separate from ad spend. Report reach, cost per direction tap, redemptions and walk-in feedback, and flag that offline visits cannot be attributed precisely.</p>
<h3>Service packages (scope proposals; prices not stated)</h3>
{tbl(["","Foundation","Growth","Full Marketing"],[
["Focus","Identity completion, profiles, launch plan","Foundation plus monthly content and local ads","Growth plus video, retention and partnerships"],
["Creative assets / month","8 (proposal)","16 (proposal)","24 (proposal)"],
["Video","Up to 2 Reels","Up to 6","Up to 10 plus launch film"],
["Community management","Setup only","Replies and posting","Full, with reviews"],
["Paid ads management","Not included","Included, one campaign line","Included, multiple"],
["Reporting and meetings","Monthly report","Monthly plus a mid-month check","Bi-weekly"],
["Revisions","2 rounds","2 rounds","3 rounds"],
["Client provides","Approvals, menu, photos access","Plus feedback in 48 hours","Plus on-site access for shoots"],
["Exclusions","Print, signage fabrication, interior design","Same","Same"],
])}
<p class="small">Counts are a starting proposal to be adjusted with the owner. Recommended starting point: <strong>Foundation</strong> for weeks 1 to 4, moving to <strong>Growth</strong> at the soft opening, then reassessing.</p>
<h3>Discovery meeting agenda (45 minutes)</h3>
<ol><li>Owner's goals and definition of success</li><li>Customer and location</li><li>Product, menu and pricing intent</li><li>Premises and design status</li><li>Budget and timeline</li><li>Decision process and next step</li></ol>
<h3>Pitch in one paragraph</h3>
<p>"You are opening in one to three months, and the premises are not designed yet. This is the best window to make the brand and space work together. We will confirm who your customers are, finish the identity, prepare a launch plan, and run a small, measured campaign. We will not promise numbers. We will show what works and adjust."</p>
<h3>Follow-up message (Egyptian Arabic)</h3>
<blockquote>أهلاً [اسم صاحب المكان]، شكراً على وقتك النهاردة. اللي اتفقنا عليه: نبدأ بأسبوعين لتأكيد العملاء والمكان وإكمال الهوية، وبعدها خطة الافتتاح. هبعتلك ملخص الاجتماع وأسئلة قصيرة تجاوب عليها. إيه أنسب معاد للمتابعة؟</blockquote>
<h3>Likely objections</h3>
{tbl(["Objection","Response"],[
["We are not open yet","That is why now is useful: identity and space can be aligned before spending on construction"],
["Can you guarantee sales?","No one honestly can. We set measurable targets for reach, directions and visits, and review them with you"],
["Budget is small","The framework starts with small tests and scales only what works"],
["We can post ourselves","Yes. We will give you a system and templates. The agency role is strategy and consistency"],
])}
<p><strong>Next step:</strong> book the discovery meeting this week, send the questionnaire beforehand.</p>''', "Ready to use in the first conversation."))
# 11
S.append(sec(11,"Owner questionnaire, open questions and action plan",f'''
{tbl(["Question","Why it matters"],[
["What does success look like in month 3?","Defines the targets"],
["Who do you picture as the regular customer?","Tests the segments"],
["Exact address, floor, parking, nearby companies?","Maps, ads and offers"],
["Final menu, best-sellers and pricing intent?","Content, positioning"],
["Average ticket and peak hours you expect (if you want to share)?","Offer design"],
["Opening date and soft-opening plan?","Calendar"],
["Budget for design and materials?","Interior brief"],
["Who approves content and how fast?","Production speed"],
["Any previous agency or freelancer experience?","Expectations"],
["Existing social handles or domain?","Avoid conflicts"],
["Delivery, reservations or online ordering planned?","Conversion path"],
["Comfort sharing basic financials?","Optional; never required"],
])}
<h3>Open items and order</h3>
{tbl(["#","Item","Owner","When"],[
["1","Confirm Arabic and English spelling, handles, address","Owner","Week 1"],
["2","Field research on 5 to 8 cafés and substitutes","Marketer","Week 1 to 2"],
["3","Owner interview and goals","Marketer and owner","Week 1"],
["4","Interior brief tiers, share with the designer","Marketer","Week 2"],
["5","Rebuild wordmark in vector, define minimum sizes","Designer","Week 2 to 3"],
["6","Real photography plan","Marketer","Week 3"],
["7","Create Maps, Instagram, Facebook profiles","Marketer","Week 3"],
["8","Confirm menu and prices","Owner","Before week 4"],
["9","Soft opening and launch test","Both","Month 2 to 3"],
])}''', "What to ask, and in what order."))
toc="".join(f'<a href="#d{i}"><b>{i}</b>{t}</a>' for i,t in [(1,"Summary"),(2,"Client profile"),(3,"Brand audit"),(4,"Market and competitors"),(5,"Customers"),(6,"Strategy and identity"),(7,"Marketing strategy"),(8,"Content"),(9,"Opportunities"),(10,"Pitch and packages"),(11,"Questions and plan")])
CSS='''
/* layout: report with sticky contents rail, brand palette from the supplied board */
:root{--bg:#F4F3EE;--paper:#FFFFFF;--ink:#303938;--head:#24485F;--mut:#5A6564;--line:#D9D9D2;--sand:#AA9470;--rust:#75432D;--blue:#587B90;--tint:#E5E5DF;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font:400 17px/1.8 Cairo,"Noto Naskh Arabic",system-ui,sans-serif;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.layout{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:230px minmax(0,1fr);gap:48px;padding-block:32px 80px}
.rail{position:sticky;top:calc(24px + env(safe-area-inset-top,0px));align-self:start;display:flex;flex-direction:column;gap:2px}
.rail small{font-weight:700;letter-spacing:.12em;color:var(--mut);margin-bottom:8px;font-size:12px}
.rail a{display:flex;gap:10px;align-items:baseline;padding:6px 10px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:15px}
.rail a b{color:var(--sand);font-weight:700;min-width:18px}.rail a:hover{background:var(--tint)}
main{min-width:0}
.hero{background:var(--head);color:#F4F3EE;border-radius:20px;padding:40px;margin-bottom:36px}
.hero h1{font:700 clamp(34px,5vw,56px)/1.15 Amiri,serif;margin-bottom:12px;text-wrap:balance}
.hero p{max-width:60ch;color:#C5C6C1}.hero .tag{display:inline-block;margin-top:18px;font-size:13px;letter-spacing:.1em;border:1px solid #ffffff44;border-radius:30px;padding:4px 14px;color:#E5E5DF}
section{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:34px;margin-bottom:24px}
.sh{display:flex;gap:18px;align-items:flex-start;margin-bottom:22px}
.no{font:700 34px/1 Amiri,serif;color:var(--paper);background:var(--rust);border-radius:12px;min-width:52px;height:52px;display:grid;place-items:center;flex:none}
h2{font:700 clamp(26px,3.2vw,34px)/1.25 Amiri,serif;color:var(--head)}.lead{color:var(--mut);margin-top:4px;font-size:16px}
h3{font:700 22px/1.4 Amiri,serif;color:var(--head);margin:26px 0 8px}h4{font-size:16px;margin:18px 0 6px;color:var(--head)}
p,li{max-width:78ch}p{margin:10px 0}ul,ol{padding-inline-start:22px;margin:8px 0}li{margin:5px 0}
a{color:var(--blue)}strong,b{font-weight:700}
.small{font-size:14px;color:var(--mut)}
.note{background:var(--tint);border-inline-start:4px solid var(--sand);padding:12px 16px;border-radius:8px;margin-top:14px;font-size:15px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:14px}
.kpis div{border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;background:var(--bg)}
.kpis b{font-size:12px;letter-spacing:.1em;color:var(--mut);text-transform:uppercase}.kpis span{font-weight:600;color:var(--head)}
.tw{overflow-x:auto;margin:12px 0;border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:14.5px}
th{background:var(--head);color:#F4F3EE;text-align:start;padding:10px 12px;font-weight:600;white-space:nowrap}
td{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top;line-height:1.6}tr:nth-child(even) td{background:#FAFAF7}
.b{font-size:12px;padding:1px 9px;border-radius:20px;border:1px solid;font-weight:600;white-space:nowrap}
.b.o{color:var(--rust);border-color:var(--rust)}.b.p{color:var(--blue);border-color:var(--blue)}.b.h{color:#7a5f1e;border-color:var(--sand)}.b.n{color:#a02828;border-color:#a02828}.b.v{color:#2d6a3e;border-color:#2d6a3e}
figure{margin:14px 0}figure img{width:100%;border-radius:12px;border:1px solid var(--line);display:block}figcaption{font-size:13px;color:var(--mut);margin-top:6px}
.sws{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:12px 0}
.sw{display:flex;flex-direction:column;gap:2px;font-size:13px}.sw i{height:74px;border-radius:10px;border:1px solid #0001;margin-bottom:6px}.sw b{font-size:14px}.sw code{font-family:ui-monospace,monospace}.sw small{color:var(--mut)}
blockquote{background:var(--bg);border-inline-start:4px solid var(--blue);padding:12px 16px;border-radius:8px;margin:10px 0}
@media(max-width:900px){.layout{grid-template-columns:1fr;gap:18px}.rail{position:static;flex-direction:row;flex-wrap:wrap;gap:6px}.rail small{width:100%}.rail a{background:var(--paper);border:1px solid var(--line)}section{padding:22px}.hero{padding:26px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
html=f'''<title>MASKOOB Café Brief</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<div class="layout"><nav class="rail" aria-label="Contents"><small>CONTENTS</small>{toc}</nav>
<main><div class="hero"><h1>مسكوب · MASKOOB Café</h1><p>Client intelligence, brand direction and marketing opportunity assessment for a new specialty café in 10th of Ramadan City. Research date: 26 October 2026. Verified facts, owner-reported facts and hypotheses are labeled separately.</p><span class="tag">PRE-OPENING · DRAFT FOR OWNER REVIEW</span></div>
{"".join(S)}</main></div>'''
open("maskoob.html","w").write(html);print(len(html))
