# ClinStat Paid Social Campaign: Final Summary

**Client:** ClinStat Research (clinical research and biostatistics consultancy)
**Goal:** client acquisition
**Markets:** Saudi Arabia, UAE, Qatar (GCC, first wave)
**Budget:** 50,000 EGP **[CONFIRM: monthly or total; billing currency]**
**Platforms:** LinkedIn, Facebook, Instagram (paid); X (organic for now)

---

## 1. What was produced

| Deliverable | Location | Status |
| --- | --- | --- |
| Campaign plan (audiences, funnel, budget, English ad copy, tracking, compliance, timeline) | `clinstat/ads-campaign/campaign-plan.md` | Done, merged |
| Arabic ad copy (LinkedIn, Meta, X) | `clinstat/ads-campaign/arabic-ad-copy.md` | Done, merged. Needs native review |
| Arabic video: "5 questions before hiring a biostatistician" | `clinstat/5questions/ar/clinstat_5questions_ar.mp4` | Done, on branch, not yet in a PR |
| Arabic video: "What makes a research finding reliable?" | `clinstat/reliable/ar/clinstat_reliable_ar.mp4` | Done, on branch, not yet in a PR |
| `claude-ads` plugin (paid-media toolkit) | `claude-ads/` and `.claude/settings.json` | Imported and enabled, merged |

Both Arabic videos are 20 s, 1080×1920, 30 fps, right-to-left, with the original ClinStat logo and score. Source files and rebuild instructions are in each `ar/` folder.

## 2. The plan in brief

**Message:** most research problems that get papers rejected are avoidable with one expert review before submission.

**Audiences:** clinician-researchers, academic researchers, pharma/device sponsors, journal authors.

**Funnel:** awareness 30% (reels), consideration 30% (education), conversion 40% (free 15-minute consultation).

**Budget (50,000 EGP):**

| Platform | EGP | Share |
| --- | --- | --- |
| LinkedIn | 22,000 | 44% |
| Facebook + Instagram | 22,000 | 44% |
| Testing reserve | 6,000 | 12% |
| X (paid) | 0 | organic only |

Why X is unpaid: about USD 1,000 is too thin to learn anything from four paid platforms. Add paid X later if the first two work.

**Within each platform:** Saudi Arabia 45%, UAE 35%, Qatar 20% (starting guess). Language: Arabic first in Saudi Arabia, English first in the UAE, both in Qatar.

**Timeline:** week 0 setup, week 1 launch, week 2 first read, week 3 retargeting, week 4 review and plan month 2.

## 3. Which creative goes where

| Asset | Use |
| --- | --- |
| English and Arabic "5 questions" reel | Instagram and Facebook Reels, Stories, LinkedIn video |
| English and Arabic "reliable findings" reel | LinkedIn video, X, awareness |
| Static cover (`5questions/cover_*.png`) | Feed image |

Not yet made: Arabic versions of the "3 factors" and Gulf videos, and 1:1 or 4:5 feed crops of the reels (all video files are 9:16).

## 4. Open items before launch

1. **Budget:** confirm whether 50,000 EGP is monthly or total, and the billing currency. The USD figure is approximate.
2. **Arabic review:** have a native Gulf Arabic speaker check the ad copy, the technical terms and the on-screen video text.
3. **Team claim:** the "5 questions" video says every team member has "50+ papers and an h-index of 5+". It comes from the English video. Confirm it is true before running it.
4. **Landing page:** one page per offer, Arabic and English, a consultation form and a privacy notice. Not built.
5. **Tracking:** LinkedIn Insight Tag, Meta Pixel and Conversions API, UTM tags. Not set up.
6. **Accounts:** confirm the LinkedIn Page, Facebook Page, Instagram and X accounts and ad-account access.
7. **Compliance:** check current LinkedIn, Meta and X health-advertising policies, and data-protection rules in the three countries, before launch.
8. **Reliable video source:** the original infographic for this video was never supplied, so it was reconstructed from the written brief.

## 5. What was not done

- No ads, campaigns or accounts were created on any platform. Everything here is ready-to-use material, not live.
- No performance numbers or benchmarks are included, because there is no account data yet to ground them.
- The `claude-ads` plugin was imported and enabled for this project but not run on any account, since no ad data was available.

## 6. Recommended next steps

1. Answer the open items above (budget, accounts, claim check).
2. Get the Arabic copy and videos reviewed.
3. Build the landing page and tracking.
4. Launch LinkedIn and Meta with 2 to 3 ads per ad set, one ad set per country.
5. Review after week 2 on cost per qualified lead. Move the reserve to the winner.
6. Once ads have spend, run the plugin's Google/Meta/LinkedIn audits on exported data to find waste and gaps.
