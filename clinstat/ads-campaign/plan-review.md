# ClinStat Campaign Plan: Review Against the Marketing Skills

**Reviewed:** `campaign-plan.md` (Draft v1)
**Method:** checked against the `ads` skill and its references (`linkedin-b2b-playbook`, `meta-andromeda-playbook`, `meta-decision-system`, `b2b-paid-playbook`).
**Caveat:** every benchmark below is a practitioner-reported B2B SaaS range from those playbooks, not Gulf clinical-research data. Treat the maths as order-of-magnitude, and replace it with your own numbers after week 2.

Budget used: 50,000 EGP ≈ USD 1,000/month (the plan's own estimate, itself marked [CONFIRM]).

---

## Verdict

The plan is a solid first draft: clear positioning, honest claims, good compliance section, sensible "concentrate on LinkedIn + Meta". The main problem is **scope versus budget**. It describes about 3 countries × 2 languages × 2 platforms × 3 ads, which this budget cannot feed. The second problem is that **no target cost per lead is defined**, so none of the pause/keep/scale decisions can be made. The rest are fixable details.

---

## 1. Must fix before launch

### 1.1 Too many ads and ad sets for the budget
Meta/LinkedIn playbooks cap active ads at `(daily budget × 14) / (2 × target cost per qualified lead)`, so each ad can get a fair read within 14 days.

| Platform | Monthly budget | Daily | Assumed target CPL (placeholder) | Ad ceiling |
| --- | --- | --- | --- | --- |
| LinkedIn | 22,000 EGP ≈ $440 | ≈ $14.7 | $100 | **≈ 1 ad** |
| Meta | 22,000 EGP ≈ $440 | ≈ $14.7 | $25 | **≈ 4 ads** |

The plan has 3 LinkedIn ads and 3 Meta ads, each split by country (3) and language (2), which is up to 18 variants per platform.

**Fix**
- **LinkedIn:** one campaign, one audience covering all three countries together, one or two ads. Read country performance from the demographics report instead of separate ad sets.
- **Meta:** one campaign, 3 to 4 ads total. Treat language as an ad-level variable, not a separate ad set per country.
- Keep the country budget split (45/35/20) as a reporting target, not three separate budgets.

### 1.2 No target cost per qualified lead (TCPL), so no kill rules
Section 8 says "set targets once you have a baseline [CONFIRM]". The playbooks say to derive the target from deal maths first:
- Breakeven CPL = average project value × lead-to-close rate. Example with placeholders: 15,000 EGP project × 20% close rate = 3,000 EGP breakeven CPL.
- Set the working target below breakeven by your required margin.

Once TCPL exists, use these kill rules instead of "after 7 days or 50 clicks":
- **New ad:** pause at 2 to 3× TCPL spent with zero qualified leads.
- **Ad older than 7 to 14 days:** pause when cost per qualified lead runs 1.5 to 2× over TCPL.
- Never pause a producing ad without a replacement ready.

**Needs from ClinStat:** average project/service price, rough close rate on consultations, gross margin.

### 1.3 Can this budget reach a workable number of leads at all?
Using the playbooks' LinkedIn ranges (CPC $8 to $22, Lead Gen Form CPL $50 to $200):
- 22,000 EGP on LinkedIn ≈ **2 to 9 leads/month** via Lead Gen Forms, or **1 to 3** via a landing page at 5% conversion.
- That is not enough data to optimise within a month. Expect to learn only from month 2 or 3.

**Fix:** tell ClinStat now that month 1 is a learning month, and set the success bar as "a defined cost per qualified lead from real data", not "X clients".

### 1.4 Ad copy contradicts the plan's own "no guarantees" rule
- LinkedIn Ad 1: "All three are avoidable with one review before submission."
- X post 1: "One pre-submission review fixes all three."

"Fixes" implies a guaranteed outcome. Rewrite as "helps catch all three before submission". Apply the same wording in the Arabic file.

---

## 2. Should fix: strategy

### 2.1 Meta targeting: flip the test arm and the main arm
The plan uses manual interests + job titles as the main arm and Advantage+ as the test. The Andromeda-era playbook says the reverse: **creative is the targeting.**
- Make the main arm **broad (country only)** with specific creative; keep one interest-based arm as the control.
- Use **identity-trigger variants**: duplicate your best ad and put the audience in the headline, e.g. "for residents", "for cardiology researchers", "for PhD students", "for oncology trials". This maps directly onto your four segments.
- **Long-form primary text** tends to beat short copy; the current Meta copy is short.
- **Statics often beat video** and are far cheaper to produce. The plan leans on the existing 9:16 videos. Keep them for reach, but add 3 to 5 static carousels/images from the infographic and icons.
- Make ads look native: use the repo's existing explainer videos, not polished-ad styling.

### 2.2 LinkedIn setup gaps
- **Audience Expansion OFF and Audience Network OFF.** Not mentioned in the plan; both waste B2B spend.
- **Use job function + seniority instead of a long job-title list.** Title lists are small and expensive, and titles and seniority cannot be combined. Expect to add negative titles weekly for the first 2 months.
- **Audience size:** at least about 15K members per cold campaign, ideally 50K to 300K. Qatar alone will fall below this, which is another reason to combine the three countries.
- **Create retargeting audiences before launch.** LinkedIn audiences are not retroactive: site visitors, 50%+ video viewers, lead-form openers, page visitors. The plan only mentions the Insight Tag.
- **Bidding:** week 1 automated, then from week 2 manual CPC about 20% below the observed average.
- **Thought leader ads:** promoting a post from a ClinStat biostatistician's profile typically delivers about 3 to 6× the CTR of a company-page ad. Run it organically first, and promote the post that does best. This suits a consultancy where the expert is the product.
- **Document ad for the lead magnet:** the "pre-submission checklist" fits a 5 to 7 slide document ad (1080×1350), which is a cheaper-to-buy format than single images.

### 2.3 Funnel split is top-heavy for this budget
The plan puts 30% awareness / 30% consideration / 40% conversion. The B2B playbook says to build from the bottom up, because top-of-funnel is the slowest and most expensive to pay back, and it advises small budgets or small audiences to run one campaign with all layers rather than separate funnel stages.
- Shift to roughly **60 to 70% conversion/capture** (free consultation) plus **retargeting of video viewers**.
- Get awareness from **organic posting** (X, LinkedIn, Instagram) and cheap video-view campaigns whose only job is to fill the retargeting pool.

### 2.4 Sponsors (segment C) are the wrong job for paid LinkedIn
Pharma/device/CRO decision-makers in three countries are a small, named audience, and LinkedIn CPCs of $8 to $22 are costly for it.
- Build a **named-account list** (Gulf CROs, pharma country offices, device distributors) and reach it by **cold email + ABM-style retargeting** (see the `cold-email`, `prospecting` skills and `abm-playbook.md`).
- Keep paid LinkedIn for clinician-researchers and academics, who are the larger pools.

### 2.5 Lead quality: score it, don't just count it
- Add a **qualifying question** to the lead forms (study stage or manuscript status). Instant forms generate low-intent leads otherwise.
- Score each consultation lead on **Urgency / Budget / Fit (0 to 3 each, max 9)**, log it against the originating ad, and after about 20 scored calls rank ads by average quality score, not CPL or CTR.
- Send the qualified-lead event back to the platforms (LinkedIn conversion API, Meta Conversions API) so they learn from qualified consultations, not raw form fills. At this volume it will be slow; start with "consultation booked" as the optimisation event.
- Reconcile platform numbers against your own lead sheet monthly; **your sheet wins**.

---

## 3. Smaller points

- **Internal inconsistency:** the budget table reserves 6,000 EGP (12%), but the timeline says "move the 10% reserve". Pick one.
- **Arabic dialect:** the plan marks this [CONFIRM]. The brand file uses Egyptian Arabic for video narration, but written ads for Saudi/UAE/Qatar professionals are usually safer in Modern Standard Arabic with light local phrasing. Have a native Gulf speaker review.
- **Scheduling:** LinkedIn resets its ad day at UTC midnight. Run ads in weekday working hours in the audience's time zone, and check the weekend differs by country [CONFIRM].
- **Social proof:** nothing in the copy uses proof, because there are no testimonials yet (open question 7). Until then, lead with process, credentials and the specific mistakes you catch.
- **Landing page (section 7):** this is the weakest section and the biggest lever on conversion. Run the `cro` skill on it once the page exists.
- **Retargeting window:** the plan launches conversion ads in week 3. Start collecting retargeting audiences from day 1.

---

## 4. Suggested revised budget and structure

| Item | EGP/month | What it runs |
| --- | --- | --- |
| LinkedIn | 20,000 | 1 campaign: researchers/academics, GCC-wide, 1 to 2 ads; add a promoted expert post once one performs organically |
| Meta (FB + IG) | 22,000 | 1 campaign: broad country targeting, 3 to 4 ads (2 static, 1 to 2 video), identity-trigger variants, Arabic and English |
| Retargeting (both) | 4,000 | Video viewers and site visitors; free-consult offer |
| Testing reserve | 4,000 | Winner scaling or one new angle after week 2 |
| X paid | 0 | Organic only |
| Sponsors (segment C) | 0 paid | Cold email / ABM outside the ad budget |

This is a proposal; it needs ClinStat's input on price, close rate and services.

---

## 5. Open items for ClinStat (adds to the plan's own list)
1. Average project price, gross margin, and expected consultation-to-client rate (needed for TCPL).
2. Is month 1 acceptable as a learning month, given the lead volume the budget allows?
3. Who will score consultation leads and log the source?
4. Can ClinStat provide a named list of target sponsor accounts?
5. Which expert's profile can be used for thought leader ads?
