# Auto-publishing runbook: b2b.gujaratbio.com

A scheduled task runs this every day. Goal: **up to 10 new knowledge-centre guides a day** for agri-input marketers, brand owners, dealers, blenders, co-operatives, importers and agronomists. Topics are pillars 1 to 5 with the buyer and technical angle: how materials are made, specified, tested and bought; FCO rules; private label; state partners; bulk granules; export. Until fcobiostimulants.com can be auto-published, its share (the neutral science of seaweed, humic, amino and biofertilisers) is written here too. Farmer how-to-apply articles belong to www.gujaratbio.com; don't write them here.

## Steps

1. `git pull`. Read `AUTOPUBLISH-LOG.csv` and the existing `/resources/` guides (`ext_50_resources.py`, `ext_50b_formulation_guides.py`, `content/auto/`) so nothing is repeated.
2. Pick today's topics: about 4 from this month's science pillar, 3 from rules and business (this month's B2B theme first), 2 product-material comparisons or quality tests, and 1 crop programme for buyers. Include at least 1 Hindi-language guide a week for Hindi-speaking dealers (write it fully in Hindi).
3. Research and write. Use one sub-agent per article if helpful; each gets this runbook. Save each as `content/auto/<slug>.json` with these fields: `slug`, `date` (YYYY-MM-DD), `h1`, `title` (≤ 60 chars, ends "| GBO" if room), `desc` (≤ 155 chars), `answer` (40 to 60 words), `sections` (list of `[id, heading, html]`, 4 to 7 sections, html uses `<p>`, `<ul><li>`, `<table>` with `<thead>` and `<tbody>`, `<strong>`, and links to existing pages such as `/seaweed-extract-manufacturer-india`, `/private-label-oem`, `/state-partner-programme`, `/fco-schedule-vi-biostimulants`, `/granular-biostimulants-manufacturer-india`, `/contact`), `faq` (4 to 6 `[q, a]`), `related` (3 to 4 `[path, title, ""]` existing pages), `keyword` (the main search phrase), `keywords` (4 to 6 secondary), `audience`, `sources` (`[title, url]` you opened).
4. `python3 build.py` (it regenerates the pages, sitemap and llms.txt). Fix any error.
5. Run the quality checks below. Delete any file that fails.
6. Add one line per published guide to `AUTOPUBLISH-LOG.csv` (`date,site,slug,title,pillar,crop,headline_style`). Commit (`Auto-publish <date>: N guides`) and `git push`. Hostinger deploys automatically.
7. Report (step 8 of the task prompt).
## Rules every piece must pass (from Gafar Laiya, owner; do not relax them)

1. **One real question per piece.** It answers something a buyer or farmer actually searches. Never a near-duplicate of an existing page on this or another GBO site: check `AUTOPUBLISH-LOG.csv` and the site's existing pages first. If no genuinely new, useful topic is left for today, publish fewer. Never pad.
2. **Farmer results only as a named farmer's own experience**, with "one farmer's experience, not a promise; results vary with soil, water, weather and management". Never promise yield, income or disease control. Known farmer: Vishalkumar Satishbhai Patel, Ashtagam, Navsari, 707 sugarcane; in his own words 30 to 35 t went to 45 t per vigha with lower chemical spend. Do not invent farmers, quotes, photos, trials, prices, ratings, reviews or statistics.
3. **Fear headlines only when the risk is real** (field experience or an official source). The fix appears in the first three lines. At most 1 headline in 4 is a fear headline. Use "may" or "can" when it isn't always true.
4. **Never name or attack a competitor or brand.** Say "cheap powders", "some products".
5. **Facts come from sources you opened** (FCO gazette and agriwelfare.gov.in, ICAR institutes, state agriculture universities, peer-reviewed papers, FAO). Link them in Sources. If you can't verify a fact, leave it out. Legal points end with "check with your state agriculture department".
6. **Something only GBO can say**, in every piece: own plant at GIDC Shihor, Bhavnagar (100 KL liquid and 2,500 t solid a month); working with farmers since 2006; Gujarat NOCs for 36 FCO Schedule VI biostimulant grades and 11 biofertiliser types; mild in-house extraction of seaweed and humic without harsh chemicals, very high pH or heat. The brand for the state partner programme is undecided, so don't promise any brand to marketers. Never mention "Plantonics".
7. **Contact details stay exactly as on the site**: +91 99787 91167 (call or WhatsApp), sales@gujaratbio.com. One call to action per piece.
8. **Plain words**: short sentences, no hype words ("revolutionary", "miracle", "best in India"), sentence-case headings. Start with a 40 to 60-word direct answer.

## Headline styles (rotate)

- The difference: "Original seaweed extract vs. messy powders: what really reaches your plant"
- Fear, but true: "The '98% humic acid' on your bag may not mean what you think"
- Home test: "5 home tests to check your seaweed before you pay for it"
- Myth-buster: "'More dose, more yield' is costing you money"
- Countdown: "Mango flowering: what to do in the next 15 days"
- The real question: "Which humic acid is best for drip irrigation?"
- Farmer story (only with a real, named farmer)
- Insider: "Inside a biostimulant plant: what a good seaweed batch looks like"

## Topic tree (pillars; pick from these following the calendar)

1. Seaweed extract: original extract vs. messy powders; Ascophyllum, Sargassum, Kappaphycus and Indian seaweeds; mild vs. harsh extraction; what's inside (alginates, mannitol, betaines, natural growth signals); home tests; when to spray (flowering, fruit set, heat, cold, drought); granules vs. liquid vs. flakes; FCO seaweed grades; seaweed by crop.
2. Humic and fulvic: sources (leonardite, lignite, humalite and others; no source is "best" on paper, only tests and trials decide); KOH vs. NaOH; the "98%" label; humic vs. fulvic; saline and sodic soils; with phosphorus; drip and tank mixing; a simple acid test; cost per acre.
3. Amino acids and protein hydrolysates: plant vs. animal source; enzymatic vs. acid hydrolysis; free vs. total amino; chloride from acid hydrolysis; what each amino acid does; flowering, fruit set, stress recovery.
4. Other biostimulants, biofertilisers, micronutrients: 11 biofertiliser types; mycorrhiza, PSB, KSB, Azotobacter; chelates (EDTA, EDDHA, amino); the FCO biostimulant categories.
5. Rules and business: FCO Schedule VI and the 2025 cancellations; labelling; NOCs; starting a brand; private label vs. contract manufacturing; choosing a manufacturer; state partner model; export; bulk granules for blenders and co-operatives.
6. High-value horticulture crops, 8 articles per crop (nutrition calendar by stage, top 10 problems, state-wise guide, flowering and fruit set, fruit size and colour, stress, farmer experiences, FAQs): mango, apple, pomegranate, grapes, banana, citrus (kinnow, mosambi, Nagpur orange), papaya, guava, strawberry, dragon fruit, avocado, coconut, chilli, tomato, capsicum, onion, potato, cucumber, cumin, cardamom, tea, sugarcane, cotton.
7. Problems and symptoms: zinc, boron, calcium, magnesium, iron and potassium deficiency; flower drop, fruit drop, cracking, sunburn, poor colour, small fruit; salty water, white roots, root rot, heat waves, frost, waterlogging; soil health.

## Calendar (science focus; crops in season, written 2 to 4 weeks before the stage; B2B theme)

| Month | Science | Crops in season | B2B theme |
| --- | --- | --- | --- |
| Nov | Seaweed | Mango pre-flowering, potato bulking, cumin and wheat sowing, apple leaf fall, grapes after pruning | FCO Schedule VI, cancelled registrations |
| Dec | Humic and fulvic | Mango flowering, grapes fruit set, apple dormancy and pruning, potato | Own brand, private label |
| Jan | Amino acids | Sugarcane planting, mango fruit set and drop, cumin flowering, strawberry | State partner programme |
| Feb | Biofertilisers | Mango fruit size, sugarcane, grapes harvest, citrus flowering | Choosing a manufacturer |
| Mar | Seaweed for heat | Apple bud break (Himachal), mango, pomegranate, summer vegetables | Bulk granules for kharif |
| Apr | Micronutrients, chelates | Apple flowering and fruit set, mango harvest, heat stress | Dealer stocking for kharif |
| May | Water and salinity | Pomegranate flowering, banana, apple fruit size, summer orchard care | Export, private label abroad |
| Jun | Soil health, humic | Cotton and groundnut sowing, banana planting, mango post-harvest | Blenders and co-operatives |
| Jul | Biofertilisers at sowing | Cotton, paddy, sugarcane, mango post-harvest nutrition | State partners for rabi |
| Aug | Seaweed and amino for quality | Apple colour and size, cotton flowering, citrus | Labelling and claims |
| Sep | Humic for rabi | Apple harvest, potato planting prep, grapes pruning prep | Manufacturing plans |
| Oct | Review and refresh | Potato planting, grapes October pruning, mango post-monsoon, cumin | Results and plant visits |

## Quality checks before anything goes live (a piece that fails any check is held back, not published)

1. Every fact matches a source you opened, or GBO's own facts above.
2. No promise; every result is a named farmer's own words.
3. Headline rules followed (fear ≤ 1 in 4 today).
4. Not a duplicate: title and main question differ from everything in the log and on the site.
5. All internal links point to pages that exist; external links are the sources you opened.
6. Build succeeds; JSON-LD is valid JSON.
7. Contact details unchanged.
8. Words: 700 to 1,500 for English pieces; 500 to 1,000 for Gujarati.

## Gemini mode (from 10 Nov 2026)

Daily publishing now runs as a GitHub Action (`.github/workflows/gemini-autopub.yml`) using `gemini/autopub.py` and the repo secret `GEMINI_API_KEY`, so it uses no Claude allowance. It reads this file as its rulebook, researches with Google Search grounding (only grounded links become Sources), checks banned phrases, phone numbers, length, duplicates and internal links, makes one illustration per piece (captioned "Illustration"), translates, and publishes only if the build is complete. Run it by hand from GitHub → Actions → "Gemini auto-publish" → Run workflow. Claude's role is a light weekly quality review.
