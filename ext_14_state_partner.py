# State Partner Programme: one established agri-input marketer per state, GBO as the approved manufacturer.
# Rules for this file: the pack brand is NOT promised either way (still open), no partner is named, no prices,
# no yield promises. Farmer results only as named growers' own reports. Legal points say "check with your state".

P = "/state-partner-programme"
trail = [("State Partner Programme", None)]

sp_faq = [
    ("What is the GBO State Partner Programme?",
     "It is a partnership for established agri-input marketers. One partner per state handles sales, marketing, accounts and local licences; Gujarat Bio Organics manufactures the products at its own plant and supports the partner's field team."),
    ("Who can apply?",
     "Companies and firms that already sell fertilizers, biostimulants or other agri inputs in a state, usually with sales of about Rs 2 to 10 crore a year, their own field team and a network of retailers."),
    ("Will the products carry my brand or yours?",
     "That is agreed with each partner. The pack carries the marketer's and the manufacturer's details as the rules require; the brand name is decided together before the first order."),
    ("Are the products legal to sell after the 2025 FCO changes?",
     "We make only Schedule VI listed biostimulant grades. Our Gujarat Directorate of Agriculture NOCs cover 36 biostimulant grades and 11 biofertiliser types. Your own authorisation to sell in your state is also needed; check with your state agriculture department."),
    ("Is the territory exclusive?",
     "Yes, one partner per state. Rights are given for one year at a time and renewed when the agreed minimum purchase is met."),
    ("How do we start?",
     "Send the form or a WhatsApp message. We hold a video call, check documents, invite you to our plant in Shihor, Bhavnagar, and then start with a trial order for one or two crops."),
    ("What are the payment terms?",
     "For the first year we work on advance payment or a letter of credit, because we produce each order for you. Credit terms can follow after a clean record."),
]

sp_form = form("Apply to become a state partner", "State partner application", [
    field("name", "Your name", req=True),
    field("company", "Company or firm name", req=True),
    field("state", "State you want to cover", "select", True,
          ["Punjab", "Uttar Pradesh", "Maharashtra", "Assam", "Haryana", "Himachal Pradesh", "Rajasthan", "Madhya Pradesh",
           "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Telangana", "West Bengal", "Bihar", "Odisha", "Other"]),
    field("sales", "Your yearly agri-input sales", "select", True, ["Below Rs 1 crore", "Rs 1 to 2 crore", "Rs 2 to 5 crore", "Rs 5 to 10 crore", "Above Rs 10 crore"]),
    field("products", "What you sell now (products or brands)", ph="e.g. biostimulants, organic manure, micronutrients"),
    field("team", "Field team size", "select", False, ["1 to 5", "6 to 15", "16 to 40", "More than 40"]),
    field("phone", "Phone or WhatsApp", "tel", True),
    field("email", "Email", "email"),
    field("message", "Districts you cover and anything else we should know", "textarea"),
], note="We reply within one working day. Your details are used only for this partnership enquiry.")

body = hero("State Partner Programme: build your state's biostimulant business with an approved manufacturer",
            "One established marketer per state. You know your farmers; we make what works for them, in our own plant, with Schedule VI approved grades.", trail)

body += sec(
    '<div class="cols"><div>'
    + answer("Gujarat Bio Organics is looking for one established agri-input marketer in each state. You run sales, marketing, accounts and local licences; "
             "we manufacture Schedule VI listed biostimulants, biofertilisers and organic inputs at our own plant in Bhavnagar, Gujarat, and support your field team. "
             "Priority states now: Punjab, Uttar Pradesh, Maharashtra and Assam. Other states are welcome to apply.")
    + '<h2>Why marketers are looking for a manufacturer now</h2>'
    + '<p>Since 17 June 2025, biostimulants can be sold in India only if their grade is listed in Schedule VI of the Fertiliser Control Order. '
      'All 9,352 provisional registrations were cancelled, and many marketers lost products their retailers and farmers relied on. '
      'If you have the farmer network but need approved products that keep coming, that is the gap we fill.</p>'
    + ul(["NOCs from the Directorate of Agriculture, Government of Gujarat, for 36 Schedule VI biostimulant grades and 11 biofertiliser types",
          "Our own plant at GIDC Shihor, Bhavnagar: 100 KL liquid and 2,500 tonnes solid products a month",
          "Working with farmers since 2006, with crop programmes developed on farms from Kashmir to Kanyakumari",
          "One manufacturer for the whole crop calendar: granules, liquids, biofertilisers and micronutrients"])
    + '<p class="mute">See <a href="/fco-schedule-vi-biostimulants">FCO Schedule VI explained</a> and <a href="/quality-compliance">our approvals</a>.</p>'
    + f'</div><div>{sp_form}</div></div>')

body += sec(
    table(["You get", "We keep"], [
        ["Sole rights for one state, renewed each year on an agreed minimum purchase", "Formulations, process know-how and quality control"],
        ["Schedule VI approved products, with label and document support", "Registrations and NOCs in our name"],
        ["A crop-wise range for your state's main crops", "Approval of labels and marketing claims, so both companies stay safe"],
        ["Crop schedules in your state's language, training and field-team support", "A farmer helpline on the pack, shared with you"],
        ["A state page on our farmer website that sends local enquiries to you", "Supply planning based on your district sales"],
        ["First access to new products developed for your crops", "Advance or LC payment in the first year"]]),
    "What the partnership looks like", "You run the market. We run the plant and the science.", cls="tint")

body += sec(
    '<div class="prose">'
    + '<p>Every crop programme we make started with a problem farmers could not solve. These are some of them, with results as the growers themselves report them.</p>'
    + table(["Crop programme", "Where it began", "The problem farmers brought"], [
        ["Sugarcane", "South Gujarat", "Land under cane for about five decades, rising chemical use, falling yields"],
        ["Apple", "Himachal Pradesh and Kashmir", "Orchards losing trees, poor quality, rising input costs"],
        ["Potato", "Punjab and Haryana", "Falling yields, fewer and smaller tubers, high fertiliser needs"],
        ["Mango", "Across India", "Tree decline, alternate bearing and fruit drop"],
        ["Banana", "Central Gujarat", "Plant losses from wilt and leaf spot"]])
    + '<p>One example: <strong>Vishalkumar Satishbhai Patel</strong> of Ashtagam, Navsari grows the 707 sugarcane variety. In his own words, his yield went from 30 to 35 tonnes to 45 tonnes per vigha after he used our sugarcane programme, with lower spending on chemicals. '
      'This is one farmer\'s experience, not a promise; results vary with soil, water, weather and management.</p>'
    + '<p>Watch grower videos on our <a href="/impact">story and grower videos</a> page, or come to Shihor and see the plant, the lab and a farm we work with.</p></div>',
    "Products built on farms, proven by farmers")

body += sec(
    '<ol class="steps">'
    + "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in [
        ("First contact.", "Send the form or a WhatsApp message with your state and what you sell now."),
        ("Video call.", "30 minutes on your market, your crops and the products you need."),
        ("Document check.", "GST returns for two years, your dealer authorisation and two supplier references."),
        ("Plant visit.", "See our factory in Shihor, Bhavnagar and, if you like, a farm we work with."),
        ("Trial order.", "One or two crops for one season, to test the products in your market."),
        ("State agreement.", "One-year sole rights with an agreed minimum purchase, renewed each year.")])
    + '</ol>', "How to become a state partner", cls="tint")

body += sec(
    '<div lang="hi" class="prose"><h2>हिंदी में: राज्य पार्टनर प्रोग्राम</h2>'
    '<p>गुजरात बायो ऑर्गेनिक्स हर राज्य में एक अनुभवी कृषि-इनपुट मार्केटर ढूंढ रहा है। बिक्री, मार्केटिंग, हिसाब-किताब और लाइसेंस आप संभालें; '
    'Schedule VI में शामिल biostimulant, biofertiliser और organic products हम अपनी फैक्ट्री (शिहोर, भावनगर) में बनाएंगे और आपकी फील्ड टीम को सपोर्ट देंगे।</p>'
    + ul(["36 biostimulant grades और 11 biofertiliser types के लिए गुजरात कृषि निदेशालय की NOC",
          "अपनी फैक्ट्री: हर महीने 100 KL liquid और 2,500 टन solid products",
          "2006 से किसानों के साथ काम",
          "एक राज्य में सिर्फ़ एक पार्टनर, हर साल तय न्यूनतम खरीद पर नवीनीकरण"])
    + f'<p>आवेदन के लिए ऊपर का फ़ॉर्म भरें या WhatsApp करें: <a href="{wa("नमस्ते Gujarat Bio Organics, मैं अपने राज्य के लिए State Partner बनना चाहता हूँ। राज्य: ___")}">{PHONE}</a></p></div>')

body += sec(faq_html(sp_faq) + links([
    ("/become-a-distributor", "Become a distributor", "District level"),
    ("/private-label-oem", "Private label and OEM", ""),
    ("/manufacturing-facility", "Our plant", ""),
    ("/fco-schedule-vi-biostimulants", "FCO Schedule VI", "What buyers check")]), "State partner questions", cls="tint")

body += cta("Want to build your state's biostimulant business with us?",
            "One partner per state. Tell us your state and what you sell now.",
            "Hello Gujarat Bio Organics, I want to become your state partner. State: ___ What I sell now: ___")

page(P, "State Partner Programme | Biostimulant Manufacturer for Your State",
     "One established agri-input marketer per state. Schedule VI approved biostimulants made in our own plant in Gujarat, with field support. Apply online.",
     body, trail,
     [faq_ld(sp_faq),
      {"@context": "https://schema.org", "@type": "Service", "name": "State Partner Programme",
       "description": "Whole-state marketing partnership for agri-input marketers, with Gujarat Bio Organics as the manufacturer of Schedule VI listed biostimulants and biofertilisers.",
       "url": SITE + P, "serviceType": "Contract manufacturing and state distribution partnership",
       "provider": {"@id": SITE + "/#org"}, "areaServed": "IN"}], "0.9")
kw(P, "biostimulant manufacturer for state distributor",
   ["state distributor biostimulant", "third party biostimulant manufacturer India", "biostimulant manufacturer for my brand",
    "FCO approved biostimulant manufacturer", "agri input marketing company partnership"],
   [q for q, _ in sp_faq], "Commercial", "Agri-input marketers, state distributors")
