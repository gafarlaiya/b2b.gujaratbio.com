# One page per Schedule VI grade (36) and per biofertiliser type (11).

# Short use phrases for meta descriptions (same meaning as GROUP_INFO uses).
SHORT_USES = {"humic": "soil conditioning, holding nutrients near roots, root growth", "seaweed": "heat, drought and salt stress, flowering and fruit set, roots",
              "botanical": "plant-based foliar programmes and formulations", "blends": "two or more biostimulant actions in one application",
              "protein": "stress recovery, early growth, flowering and fruit set", "other": "low-dose bio-chemical input for formulations"}
# Shorter names for long blend grades in titles only.
TITLE_NAME = {"Seaweed + humic and fulvic acid + amino acids + vitamins": "Seaweed + Humic + Amino + Vitamins",
              "Humic acid + amino acid + vitamins + bio-chemicals": "Humic + Amino + Vitamins Blend",
              "Kappaphycus alvarezii + Sargassum swartzii (1:1)": "Kappaphycus + Sargassum (1:1)",
              "2-Bromo-(1H)-indole-3-carboxaldehyde 1 ppm": "2-Bromo-indole-3-carboxaldehyde 1 ppm",
              "Vinasse residue (glutamic acid 18%)": "Vinasse (Glutamic Acid 18%)"}
FORM_WORD = {"Liquid": "liquid", "Powder": "powder", "Granular": "granular", "Granules": "granules", LAF: "liquid, granule or powder"}

for g, n, f in GRADES:
    p = grade_path(n, f)
    gi = GROUP_INFO[g]
    note = GRADE_NOTE[f"{n}|{f}"]
    fw = FORM_WORD[f]
    display = f"{n} ({fw})"
    liquid = f in ("Liquid", LAF)
    solid = f in ("Powder", "Granular", "Granules", LAF)
    h1 = f"{esc(n)} {fw}: uses and bulk supply from the manufacturer" if f != LAF else f"{esc(n)}: uses, forms and bulk supply"
    trail = [("Products", "/products"), (gi["cat_name"], gi["cat"]), (n, None)]
    siblings = [(grade_path(n2, f2), f"{n2} ({FORM_WORD[f2]})", "") for g2, n2, f2 in GRADES if g2 == g and (n2, f2) != (n, f)][:6]
    faq = [
        (f"What is {n} used for?", f"{note} It is commonly used for: " + "; ".join(u.lower() for u in gi["uses"][:3]) + "."),
        (f"How is {n} applied?", "Common methods are " + ", ".join(m.lower() for m in gi["methods"]) + ". The dose is printed on the label, and we send a crop-wise dose chart with every quote."),
        (f"Is {n} an approved grade?", f"Yes. {n} ({fw}) is a grade specified in Schedule VI of the Fertiliser (Inorganic, Organic or Mixed) (Control) Order 1985, and it is covered by the No Objection Certificate issued to Gujarat Bio Organics by the Directorate of Agriculture, Government of Gujarat."),
        (f"What is the price of {n}?", PRICE_A),
        (f"Can I buy {n} under my own brand?", "Yes. We manufacture and pack it under your private label with no minimum order quantity, in " + ("liquid packs from 250 mL to 1000 L IBC" if liquid else "") + (" and " if liquid and solid else "") + ("solid packs from 1 kg buckets to 1000 kg jumbo bags" if solid else "") + "."),
        (f"Do you export {n}?", "Yes. We ship FOB or CIF from Pipavav, Kandla, Dahej, Mundra, JNPT and other Indian ports to GCC countries, Africa, the Russian Federation, Europe and the Americas."),
    ]
    image = GRADE_IMG_MAP.get(f"{n}|{f}")
    pic = img(image, f"{n} {fw}, illustrative sample image", caption="Illustrative sample image, not a lab photograph.") if image else ""
    top = answer(f"{esc(n)} ({fw}) is a {gi['cat_name'].lower()} biostimulant grade listed under Schedule VI of India's Fertiliser Control Order. {esc(note)} "
                 f"It is mainly used for " + "; ".join(u[0].lower() + u[1:] for u in gi["uses"][:3]) + ". "
                 f"Gujarat Bio Organics manufactures it at Shihor, Bhavnagar, Gujarat, for bulk, private-label and export buyers.")
    specs = spec([("Grade", esc(n)), ("Form", fw.capitalize()), ("Product family", f'<a href="{gi["cat"]}">{gi["cat_name"]}</a>'),
                  ("Regulatory", "Schedule VI listed grade, covered by our Gujarat Directorate of Agriculture NOC")])
    body = hero(h1, esc(note), trail)
    body += sec(f'<div class="split"><div>{top}{specs}{quote_btns(f"Hello Gujarat Bio Organics, please quote {n} ({fw}). Quantity: ___ Destination: ___")}</div><div>{pic or buy_block(liquid, solid)}</div></div>')
    body += sec(f'<div class="split"><div class="prose"><h3>What it is</h3><p>{gi["what"]}</p><h3>Uses of {esc(n)}</h3>{ul(gi["uses"])}</div>'
                f'<div><h3>How to use it</h3>{ul(gi["methods"])}<p>The dose depends on crop, stage and method. It is printed on the label, and we send a crop-wise dose chart with every quote.</p>'
                f'<h3>Mixing</h3><p>{gi["compat"]}</p></div></div>' + CLAIM_NOTE, f"{esc(n)}: uses, benefits and how to apply", cls="tint")
    if pic:
        body += sec(buy_block(liquid, solid), "Buying terms")
    body += sec(faq_html(faq) + links(siblings + [(gi["cat"], f"All {gi['cat_name'].lower()} grades", "Category page")] + ([("/granular-biostimulants-manufacturer-india", "All biostimulant granules", "Granule range"), ("/zyme-granules-manufacturer", "Zyme granules", "")] if f in ("Granular", "Granules", LAF) else []), "Related grades"), "Questions about this grade", cls="" if pic else "")
    body += cta(f"Need {esc(n)}?", "Send the quantity and destination. We reply with a quote and a free sample.", f"Hello Gujarat Bio Organics, please quote {n} ({fw}).")
    ft = fw.title() if f != LAF else "Liquid, Granule, Powder"
    tname = TITLE_NAME.get(n, n.replace(", ", " "))
    ft_t = "" if f == LAF else " " + ft
    title = next(t for t in (f"{tname}{ft_t}: Uses, Benefits & Bulk Supply | GBO", f"{tname}{ft_t}: Uses & Bulk Supply | GBO", f"{tname}{ft_t}: Uses & Supply | GBO",
                             f"{tname}{ft_t}: Uses | GBO", f"{tname}: Uses & Supply | GBO", f"{tname}: Uses | GBO") if len(t) <= 60 or t == f"{tname}: Uses | GBO")
    su = SHORT_USES[g]
    desc = next(d for d in (f"{n} ({fw}) uses: {su}. How to apply, FCO Schedule VI status, bulk and private-label supply from Gujarat.",
                            f"{tname}{ft_t} uses: {su}. How to apply, FCO grade, bulk and private-label supply from Gujarat.",
                            f"{tname} uses: {su}. How to apply, FCO grade, bulk and private label from Gujarat.",
                            f"{tname}: uses, how to apply, FCO Schedule VI grade. Bulk and private label from Gujarat.") if len(d) <= 158 or d.startswith(f"{tname}: uses, how"))
    page(p, title, desc, body, trail, [faq_ld(faq)], "0.7",
         f"/assets/img/{image}.webp" if image else None)
    base = n.lower().replace("%", "").replace("(", "").replace(")", "").replace(",", "")
    kw(p, f"{base} {fw if f != LAF else ''}".strip(), [f"{base} manufacturer", f"{base} price", f"{base} uses", f"{base} supplier india"],
       [q for q, _ in faq], "Commercial", "Formulators, brands, distributors, importers")

# ------------------------------------------------------------------ biofertilisers
# Names as people search them (Google India: "azotobacter biofertilizer", "psb biofertilizer", "mycorrhiza").
BIO_TN = {"Azotobacter": "Azotobacter Biofertilizer", "Azospirillum": "Azospirillum Biofertilizer", "Acetobacter": "Acetobacter Biofertilizer",
          "Rhizobium": "Rhizobium Biofertilizer", "Phosphate solubilising bacteria": "PSB Biofertilizer",
          "Potash mobilising bacteria (KMB)": "KMB / KSB Biofertilizer", "Zinc solubilising bacteria": "Zinc Solubilizing Bacteria (ZSB)",
          "Phosphate solubilising fungal biofertilisers": "Phosphate Solubilizing Fungi", "Mycorrhizal biofertilisers": "Mycorrhiza Biofertilizer (VAM)",
          "Carrier-based consortia": "NPK Consortia Biofertilizer", "Liquid consortia": "Liquid NPK Consortia Biofertilizer"}
assert set(BIO_TN) == set(BIOS)
for b in BIOS:
    p, desc_txt, role, crops = BIO_INFO[b]
    trail = [("Products", "/products"), ("Biofertilisers", "/biofertilisers-manufacturer-india"), (b, None)]
    liquid_note = "Available in liquid and carrier-based forms on request." if "consortia" not in b.lower() else ""
    faq = [
        (f"What is {b}?", desc_txt),
        (f"Which crops is {b} used for?", "Commonly: " + ", ".join(crops) + "."),
        (f"How is {b} applied?", "Common methods are seed treatment, seedling root dip, soil application mixed with compost or farmyard manure, and drip application for liquid forms. Follow the label for dose and method."),
        (f"Can {b} be mixed with chemical fertilizers or fungicides?", "Do not mix biofertilisers directly with chemical fungicides, bactericides or concentrated fertilizers, because they can kill the organisms. Apply them separately, a few days apart, or follow the label."),
        (f"How should {b} be stored?", "Store in a cool, shaded place away from direct sunlight and heat, and use within the shelf life printed on the pack."),
        (f"Is {b} an approved product?", f"Yes. {b} is among the 11 biofertiliser types specified in Schedule III of the Fertiliser Control Order that are covered by the No Objection Certificate issued to Gujarat Bio Organics by the Directorate of Agriculture, Government of Gujarat."),
        (f"What is the price of {b}?", PRICE_A),
    ]
    others = [(BIO_INFO[o][0], o, BIO_INFO[o][2]) for o in BIOS if o != b][:6]
    tn = BIO_TN[b]
    body = hero(f"{esc(tn)}: uses, crops and bulk supply", esc(desc_txt), trail)
    body += sec(f'<div class="split"><div>{answer(esc(desc_txt) + " Gujarat Bio Organics manufactures it at Shihor, Bhavnagar, Gujarat, for bulk, private-label and export buyers.")}'
                f'{spec([("Type", esc(b)), ("Role", role), ("Main crops", ", ".join(crops)), ("Regulatory", "Schedule III biofertiliser, covered by our Gujarat Directorate of Agriculture NOC")])}'
                f'<p class="mute" style="margin-top:1rem">{liquid_note}</p>{quote_btns(f"Hello Gujarat Bio Organics, please quote {b}. Form: ___ Quantity: ___")}</div>'
                f'<div>{buy_block(True, True)}</div></div>')
    body += sec(f'<div class="split"><div class="prose"><h3>How it works</h3><p>{esc(desc_txt)}</p><p>Biofertilisers work best in soil with organic matter, moisture and a near-neutral pH. They add to, rather than replace, a balanced fertilizer programme, and they take time to establish, so apply them early in the crop.</p></div>'
                f'<div><h3>Application methods</h3>{ul(["Seed treatment before sowing", "Seedling root dip before transplanting", "Soil application mixed with compost or farmyard manure", "Drip application (liquid forms)"])}'
                f'<h3>Handling</h3>{ul(["Store cool and shaded, away from sunlight", "Keep apart from chemical fungicides and bactericides", "Use within the printed shelf life"])}</div></div>' + CLAIM_NOTE, f"{esc(tn)}: how it works and how to apply", cls="tint")
    body += sec(faq_html(faq) + links(others + [("/biofertilisers-manufacturer-india", "All biofertiliser types", "Category page"), ("/resources/types-of-biofertilizers", "Types of biofertilizers", "Guide")], "Other biofertilisers"), "Questions about this biofertiliser")
    body += cta(f"Need {esc(b)}?", "Tell us the form, pack and quantity.", f"Hello Gujarat Bio Organics, please quote {b}.")
    _c = [f"{tn}: Uses, Benefits & Bulk Supply | GBO", f"{tn}: Uses & Bulk Supply | GBO", f"{tn}: Uses & Supply | GBO", f"{tn}: Uses | GBO"]
    title = next((x for x in _c if len(x) <= 60), _c[-1])
    _d = [f"{tn}, {role[0].lower() + role[1:]} biofertilizer: uses in {', '.join(c.lower() for c in crops[:2])}, how to apply, FCO Schedule III. Bulk and private label from Gujarat.",
          f"{tn}, {role[0].lower() + role[1:]} biofertilizer: uses, crops, how to apply, FCO Schedule III. Bulk and private label from Gujarat.",
          f"{tn}: uses, crops and how to apply. FCO Schedule III. Bulk and private label from Gujarat."]
    desc = next((x for x in _d if len(x) <= 158), _d[-1])
    page(p, title, desc, body, trail, [faq_ld(faq)], "0.6")
    bl = b.lower().replace("(kmb)", "").strip()
    kw(p, tn.lower(), [f"{bl} biofertilizer manufacturer", f"{bl} uses", f"{bl} for crops", f"liquid {bl}"],
       [q for q, _ in faq], "Commercial", "Distributors, brands, growers")
