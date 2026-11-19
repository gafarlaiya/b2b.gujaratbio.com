# Events: GBO at trade shows. One page per event, with our own photos.

_ev_path = "/events/soms-2026-gandhinagar"
_ev_faq = [
    ("What is SOMS?", "SOMS is the Specialty Fertilizer Summit and B2B Expo organised by the Soluble Fertilizer Industry Association (SFIA). It brings together makers and buyers of soluble, organic and micronutrient fertilizers and biostimulants."),
    ("Where and when was SOMS 2026?", "At the Helipad Exhibition Centre, Gandhinagar, Gujarat, on 3 and 4 July 2026."),
    ("I visited the GBO stall. How do I follow up?", "Send us a WhatsApp message on +91 99787 91167 or email sales@gujaratbio.com with the grades you discussed, the quantity and your location. We reply with a quote and send samples."),
    ("Can I get samples of the granules shown at the stall?", "Yes. Samples are free; the buyer pays courier or freight. Tell us which grades you want to test."),
]
_ev_ph = lambda n, alt, cap: img(n, alt, caption=cap)
_ev_body = hero("Gujarat Bio Organics at SOMS 2026, Gandhinagar",
                "We exhibited at SOMS 2026, the Specialty Fertilizer Summit and B2B Expo, on 3 and 4 July 2026 at the Helipad Exhibition Centre, Gandhinagar.",
                [("About", "/about"), ("SOMS 2026", None)])
_ev_body += sec(f'''<div class="split"><div class="prose">{answer("Gujarat Bio Organics (GBO) took part in SOMS 2026, organised by the Soluble Fertilizer Industry Association (SFIA). At our stall we met dealers, distributors, brand owners and export buyers looking for biostimulants, humic and seaweed granules, amino acids and organic fertilizers for bulk supply and private label.")}
<h3>What we showed</h3>{ul(["Our B2B range: biostimulants, biofertilizers, organic fertilizers, humic and fulvic, seaweed extracts and amino acids, in liquid, powder and granules",
 "Humic acid and seaweed granule samples, with specification sheets for each grade",
 "Buyer guides on how to check humic granules, seaweed granules and amino acids before you buy",
 "Private label, bulk and export terms: no minimum order, dispatch in about one week"])}
<p>Missed us at the expo? See the <a href="/bulk-supply">bulk supply</a>, <a href="/private-label-oem">private label</a> and <a href="/export">export</a> pages, or <a href="/contact">contact us</a> for a quote and samples.</p></div>
<div>{_ev_ph("soms-2026-gbo-stall", "Visitors at the Gujarat Bio Organics stall at SOMS 2026, Gandhinagar", "Our stall at SOMS 2026")}</div></div>''')
_ev_body += sec('<div class="split">' + _ev_ph("soms-2026-entrance", "Entrance of SOMS 2026, Specialty Fertilizer Summit and B2B Expo, Gandhinagar, organised by SFIA", "SOMS 2026 entrance, Gandhinagar")
                + _ev_ph("soms-2026-panels", "Gujarat Bio Organics buyer guide panels on humic granules, amino acids, seaweed granules and humic acid at SOMS 2026", "Our buyer guides on humic, seaweed and amino acid quality") + "</div>"
                + '<div class="split" style="margin-top:1.6rem">' + _ev_ph("soms-2026-buyer-meeting", "The GBO team talking with a visitor about humic and seaweed granules at SOMS 2026", "Talking through granule samples and specification sheets")
                + _ev_ph("soms-2026-stall-visitors", "Visitors at the Gujarat Bio Organics stall at SOMS 2026, Gandhinagar", "Dealers and buyers at the stall") + "</div>"
                + '<div class="split" style="margin-top:1.6rem">' + _ev_ph("soms-2026-students", "Students and visitors at the Gujarat Bio Organics stall at SOMS 2026", "Students and young agronomists visited too") + "<div></div></div>",
                "From the expo")
_ev_body += sec(f'<div class="prose"><p>The buyer guides at our stall are also on this site: <a href="/resources/humic-acid-uses-in-agriculture">humic acid uses</a>, <a href="/resources/seaweed-extract-uses-in-agriculture">seaweed extract uses</a>, <a href="/resources/protein-hydrolysate-vs-amino-acid">protein hydrolysate vs amino acid</a> and <a href="/fco-schedule-vi-biostimulants">FCO Schedule VI biostimulants</a>.</p></div>'
                + faq_html(_ev_faq), "Questions from the expo", cls="tint")
_ev_body += cta("Met us at SOMS 2026?", "Send the grades and quantity you discussed. We reply with a quote and send samples.", "Hello Gujarat Bio Organics, we met at SOMS 2026. Please send a quote for: ___")
page(_ev_path, "GBO at SOMS 2026, Gandhinagar: Specialty Fertilizer Expo",
     "Gujarat Bio Organics exhibited biostimulants, humic and seaweed granules and organic fertilizers at SOMS 2026, the SFIA specialty fertilizer B2B expo in Gandhinagar.",
     _ev_body, [("About", "/about"), ("SOMS 2026", None)],
     [faq_ld(_ev_faq), {"@context": "https://schema.org", "@type": "Event", "name": "SOMS 2026: Specialty Fertilizer Summit and B2B Expo",
       "startDate": "2026-07-03", "endDate": "2026-07-04", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
       "location": {"@type": "Place", "name": "Helipad Exhibition Centre", "address": {"@type": "PostalAddress", "addressLocality": "Gandhinagar", "addressRegion": "Gujarat", "addressCountry": "IN"}},
       "organizer": {"@type": "Organization", "name": "Soluble Fertilizer Industry Association (SFIA)"},
       "performer": {"@type": "Organization", "name": "Gujarat Bio Organics Pvt. Ltd.", "url": SITE + "/"},
       "image": [SITE + "/assets/img/soms-2026-entrance.webp", SITE + "/assets/img/soms-2026-gbo-stall.webp"]}],
     "0.6", "/assets/img/soms-2026-gbo-stall.webp")
kw(_ev_path, "gujarat bio organics soms 2026", ["soms 2026 gandhinagar", "specialty fertilizer expo gandhinagar", "sfia soms expo exhibitor biostimulant"],
   [q for q, _ in _ev_faq], "Trust / brand", "Dealers, distributors, brand owners, importers")
