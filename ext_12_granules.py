# Granule money pages: the biostimulant granule cluster (hub + humic, seaweed, amino/protein + buyer pages).
# Only grades already in GRADES (our Gujarat NOC list) are named. No granule size, density or price is published
# because those depend on the grade and batch: the specification sheet carries them.

def _rows(pairs):
    out = []
    for n, f in pairs:
        out.append([f'<a href="{grade_path(n, f)}">{esc(n)}</a>', esc(f if f != LAF else "Granule (also liquid, powder)"), esc(GRADE_NOTE[f"{n}|{f}"])])
    return out

G_HUMIC = [("Humic acid 51%", "Granular"), ("Humic acid 1.5%", "Granules"), ("Humic acid + seaweed extract", "Granules")]
G_SEAWEED = [("Sargassum tenerrimum 2%", "Granular"), ("Humic acid + seaweed extract", "Granules")]
G_AMINO = [("Protein hydrolysate, plant source 25%", LAF), ("Protein hydrolysate, plant source 16.9%", LAF), ("Protein hydrolysate, plant source 1.5%", LAF),
           ("Protein hydrolysate, plant source 27%", LAF), ("Amino acid 5%", LAF), ("Amino acid 10%", LAF), ("Amino acid 20%", LAF)]
G_ALL = G_HUMIC[:2] + [G_SEAWEED[0], G_HUMIC[2]] + G_AMINO

def _il(pairs):
    return [(grade_path(n, f), f"{n} ({'granule' if f == LAF else f.lower()})") for n, f in pairs]

GRAN_SPEC = ('<p>Every granule grade ships with a specification sheet. Ask for it with your quote: it carries the active content, granule size range, '
             'moisture and packing for the batch, so you can compare suppliers on facts instead of price per kg. The No Objection Certificate copy '
             'and a third-party test report are available on request.</p>')

# =============================================================== HUB
cat_page(dict(
 path="/granular-biostimulants-manufacturer-india", crumb="Biostimulant granules",
 title="Biostimulant Granules Manufacturer India | Humic & Seaweed | GBO",
 desc="Humic acid, seaweed and amino acid granules from our Gujarat plant. 2,500 t solid capacity a month, no MOQ, private label and export. Free samples.",
 h1="Biostimulant granules manufacturer in India: humic, seaweed and amino acid",
 lead="Broadcast-ready granules for distributors, fertilizer brands, blenders and importers. One plant in Bhavnagar, no minimum order, your brand or ours.",
 answer="Gujarat Bio Organics manufactures biostimulant granules at its own plant in Shihor, Bhavnagar, Gujarat: humic acid granules, seaweed (Sargassum) granules, humic plus seaweed granules, and plant-source protein hydrolysate and amino acid granules. Solid capacity is 2,500 tonnes a month, there is no minimum order quantity, and we supply in bulk, under your private label or for export, with free samples.",
 grades=_rows(G_ALL), grades_title="Every granule grade we make", ilist=_il(G_ALL), groups=[],
 intro=('<h2>Find your granule</h2>' + hub([
   ("/humic-acid-granules-manufacturer-india", "Humic acid granules", "51% and 1.5% granules, plus humic with seaweed."),
   ("/seaweed-extract-granules-manufacturer-india", "Seaweed extract granules", "Sargassum tenerrimum 2% granular and humic plus seaweed."),
   ("/amino-acid-granules-manufacturer-india", "Amino acid and protein granules", "Plant-source protein hydrolysate and amino acid grades."),
   ("/zyme-granules-manufacturer", "Zyme granules", "The trade name for seaweed and humic broadcast granules."),
   ("/private-label-zyme-granules", "Private label granules", "Your brand, your bag, our plant."),
   ("/granules-for-npk-blenders", "Granules for blenders", "Biostimulant granules to add to a fertilizer blend.")])),
 what=("<p>A granule is the easiest way to put a biostimulant into the root zone: it is broadcast with basal fertilizer, banded near the row or "
       "applied at earthing up, with no spraying and no tank mix. That is why granules sell well through dealers in field crops, sugarcane, "
       "banana, potato and orchards.</p><h3>What decides a good granule</h3><ul>"
       "<li><strong>The listed grade.</strong> In India a biostimulant has to be specified in Schedule VI of the Fertiliser Control Order to be sold. "
       'Check the grade on the bag against the notified list. See our <a href="/fco-schedule-vi-biostimulants">Schedule VI guide</a>.</li>'
       "<li><strong>Active content.</strong> A 51% humic granule and a 1.5% humic granule are used at very different rates. Compare the active per acre, not the price per kg.</li>"
       "<li><strong>Granule quality.</strong> Even size, low dust and a dry granule spread well and store well. Ask for the batch specification.</li>"
       "<li><strong>Supply.</strong> A plant that quotes against your volume, packs in your sizes and ships on time protects your own season.</li></ul>"
       + GRAN_SPEC),
 what_title="How to choose biostimulant granules",
 uses_head=["Your business", "Where granules fit", "Start with"],
 uses=[["Fertilizer or agri-input brand", "A granule line sold through your dealers, under your name", '<a href="/private-label-zyme-granules">Private label granules</a>'],
       ["NPK or compound blender", "A biostimulant granule added to a blend", '<a href="/granules-for-npk-blenders">Granules for blenders</a>'],
       ["Distributor or large dealer", "A steady granule range with bulk prices", '<a href="/become-a-distributor">Distributor page</a>'],
       ["Importer or exporter", "Granules packed and shipped FOB or CIF", '<a href="/export">Export page</a>'],
       ["Sugar mill, cooperative or FPO", "Bulk supply for member growers", '<a href="/bulk-supply">Bulk supply</a>']],
 uses_title="Who buys biostimulant granules from us",
 methods=["Broadcast with basal fertilizer", "Band placement near the root zone", "At earthing up or top dressing"],
 wa="Hello Gujarat Bio Organics, please quote biostimulant granules. Grade: ___ Pack: ___ Quantity: ___ Destination: ___", liquid=False,
 faq=[("Who is a biostimulant granules manufacturer in India?", "Gujarat Bio Organics Pvt. Ltd. makes humic acid, seaweed and amino acid granules at its own plant in Shihor, Bhavnagar, Gujarat, and supplies them in bulk, under private label and for export."),
      ("What types of biostimulant granules do you make?", "Humic acid 51% granular, humic acid 1.5% granules, Sargassum tenerrimum 2% granular, humic acid plus seaweed extract granules, and plant-source protein hydrolysate and amino acid grades that can be made as granules."),
      ("What is the monthly capacity for granules?", "Our plant makes 2,500 tonnes of solid products a month and 100 KL of liquids. Tell us your volume and we confirm the schedule."),
      ("Is there a minimum order quantity for granules?", "No. We quote trial quantities as well as bulk orders."),
      ("What is the price of biostimulant granules per kg or tonne?", PRICE_A),
      ("What pack sizes are available?", "1, 2, 4, 5, 8, 10 and 20 kg bags or buckets, 25 and 50 kg bags, and 600 kg and 1000 kg jumbo bags."),
      ("Can I get a free sample?", "Yes. Samples are free. Freight or courier, customs duty and other charges are paid by the buyer."),
      ("Do you export biostimulant granules?", "Yes, FOB or CIF from Pipavav, Kandla, Dahej, Mundra and JNPT to the Gulf, Africa, the Russian Federation, Europe and the Americas. Ask about the registration your destination needs.")],
 related=[("/humic-acid-granules-manufacturer-india", "Humic acid granules", ""), ("/seaweed-extract-granules-manufacturer-india", "Seaweed granules", ""),
          ("/amino-acid-granules-manufacturer-india", "Amino acid granules", ""), ("/zyme-granules-manufacturer", "Zyme granules", ""),
          ("/private-label-zyme-granules", "Private label granules", ""), ("/bulk-pricing-and-quotes", "How bulk pricing works", "")],
 kw=("biostimulant granules manufacturer india", ["granular biostimulants manufacturer", "biostimulant granules supplier", "organic granules manufacturer india", "soil granules manufacturer", "biostimulant granules bulk"]),
 og="/assets/img/humic-seaweed-granules.webp"))

# =============================================================== HUMIC GRANULES
cat_page(dict(
 path="/humic-acid-granules-manufacturer-india", crumb="Humic acid granules",
 title="Humic Acid Granules Manufacturer India: 51% & 1.5% | GBO",
 desc="Humic acid granules manufacturer in Gujarat: 51% granular and 1.5% granules, plus humic with seaweed. Bulk, private label, export. No MOQ. Free samples.",
 h1="Humic acid granules manufacturer in India",
 lead="High-content 51% humic granules and low-dose 1.5% soil granules from our own plant in Bhavnagar. Bulk, private label and export, with no minimum order.",
 answer="Humic acid granules are a solid, broadcast form of humic acid that is applied to the soil with basal fertilizer to condition the soil and support root growth. Gujarat Bio Organics manufactures humic acid 51% granular and humic acid 1.5% granules, and humic plus seaweed granules, at its own plant in Shihor, Bhavnagar, Gujarat, for distributors, brands and exporters.",
 grades=_rows(G_HUMIC), grades_title="Humic granule grades", ilist=_il(G_HUMIC), groups=[],
 what=("<p>Humic acid is the stable, dark fraction of decomposed organic matter. In granule form it is easy to spread, so growers broadcast it with "
       "basal fertilizer at sowing or apply it at top dressing. It is used to condition compact or low organic-matter soils and to hold applied "
       "nutrients near the roots.</p><h3>51% granular or 1.5% granules?</h3>"
       "<p>The two are very different products. Humic acid 51% granular is a concentrated grade, so the dose per acre is small and the "
       "cost per unit of humic is the figure to compare. Humic acid 1.5% granules are a low-dose soil granule, usually sold in larger "
       "quantities per acre and bought by farmers as a ready broadcast product. Choose by the active humic you need per acre, not the price per kg.</p>"
       "<h3>Humic granules or powder?</h3><p>Granules suit basal broadcast and blending. Soluble powders, such as potassium humate 49% powder, suit drip, drench and liquid formulation. "
       'See <a href="/resources/potassium-humate-vs-humic-acid">potassium humate vs humic acid</a> and <a href="/resources/humic-acid-vs-fulvic-acid">humic vs fulvic acid</a>.</p>'
       "<h3>Five questions before you buy</h3><p>Ask any supplier about the source, the mining and storage, the extraction, the formulation and the active humic per acre. "
       'Our <a href="/humic-acid-manufacturer-india">humic acid page</a> sets out the five questions in full.</p>' + GRAN_SPEC),
 what_title="Humic acid granules: what to know before you buy",
 uses_head=["Crop stage", "How granules are used", "Grade to ask for"],
 uses=[["Land preparation and sowing", "Broadcast with basal fertilizer", "Humic acid 51% granular, humic acid 1.5% granules"],
       ["Earthing up and top dressing", "Spread at the row or at earthing up", "Humic acid 1.5% granules"],
       ["Blends and private label", "Added to a fertilizer blend or packed under your brand", "Humic acid 51% granular, humic + seaweed granules"],
       ["Retail buckets for dealers", "Packed in 1 to 20 kg buckets", "Any granular humic grade"]],
 uses_title="Where humic acid granules are used",
 methods=["Broadcast with basal fertilizer", "Band placement near the root zone", "At earthing up or top dressing"],
 wa="Hello Gujarat Bio Organics, please quote humic acid granules. Grade: ___ Pack: ___ Quantity: ___ Destination: ___", liquid=False,
 faq=[("Who is a humic acid granules manufacturer in India?", "Gujarat Bio Organics makes humic acid 51% granular and humic acid 1.5% granules at its own plant in Shihor, Bhavnagar, Gujarat, for bulk, private-label and export buyers."),
      ("What are humic acid granules used for?", "They condition the soil and support root growth when broadcast with basal fertilizer or applied at top dressing, so crops make better use of the fertilizer already applied."),
      ("What is the difference between humic acid 51% granular and 1.5% granules?", "The active humic content. The 51% grade is concentrated and used at a small dose per acre; the 1.5% grade is a low-dose soil granule used at a larger quantity per acre."),
      ("What is the price of humic acid granules per kg or per tonne?", PRICE_A),
      ("Can I buy humic acid granules under my own brand?", "Yes. We pack granules under your label, in buckets, bags or jumbo bags, with no minimum order quantity."),
      ("Can humic granules be mixed with NPK, urea or DAP?", "Humic granules are broadcast along with basal fertilizer, and humic acid mixes with most fertilizers. Do a small trial mix first if you are blending at scale."),
      ("Do you make humic granules for export?", "Yes, FOB or CIF from Indian ports. Tell us the grade, quantity and destination and ask what registration the destination needs."),
      ("Do you give free samples of humic granules?", "Yes. Samples are free; the buyer pays freight or courier, customs duty and other charges.")],
 related=[("/products/humic-acid-51-granular", "Humic acid 51% granular", ""), ("/products/humic-acid-1-5-granules", "Humic acid 1.5% granules", ""),
          ("/products/humic-acid-plus-seaweed-extract-granules", "Humic + seaweed granules", ""), ("/granular-biostimulants-manufacturer-india", "All granule grades", ""),
          ("/humic-acid-manufacturer-india", "Humic acid manufacturer", ""), ("/private-label-zyme-granules", "Private label granules", "")],
 kw=("humic acid granules manufacturer", ["humic acid granules", "humic granules manufacturer", "humic acid granules price", "humic acid 51 granular", "humic acid granules bulk", "humic acid granules for soil", "humic acid granules exporter"]),
 og="/assets/img/humic-acid-51-granular.webp"))

# =============================================================== SEAWEED GRANULES
cat_page(dict(
 path="/seaweed-extract-granules-manufacturer-india", crumb="Seaweed extract granules",
 title="Seaweed Extract Granules Manufacturer India | GBO",
 desc="Seaweed granules from our Gujarat plant: Sargassum tenerrimum 2% granular and humic plus seaweed granules. Bulk, private label, export. No MOQ.",
 h1="Seaweed extract granules manufacturer in India",
 lead="Sargassum seaweed granules and humic plus seaweed granules, made at our plant in Bhavnagar for distributors, brands and exporters. No minimum order.",
 answer="Seaweed extract granules carry seaweed on a granule so it can be broadcast with basal fertilizer instead of sprayed. Gujarat Bio Organics manufactures Sargassum tenerrimum 2% granular and humic acid plus seaweed extract granules at its own plant in Shihor, Bhavnagar, Gujarat, in buckets, bags and jumbo bags, for bulk, private-label and export buyers.",
 grades=_rows(G_SEAWEED), grades_title="Seaweed granule grades", ilist=_il(G_SEAWEED), groups=[],
 what=("<p>Seaweed extracts are mostly sold as liquids for spraying. Granules bring seaweed into the root zone, so it is broadcast with basal "
       "fertilizer or at top dressing. This is the product that many Indian buyers call seaweed granules or zyme granules.</p>"
       "<h3>Which seaweed granules do we make?</h3><p>Our granular seaweed grades are Sargassum tenerrimum 2% and humic acid plus seaweed extract. "
       'Kappaphycus and Ascophyllum extracts are supplied as liquids; see the <a href="/seaweed-extract-manufacturer-india">seaweed extract page</a>. '
       'If you need another seaweed on a granule, send the specification and we say what we can make.</p>'
       "<h3>Seaweed granules or humic granules?</h3><p>Humic granules mainly condition the soil and support roots; seaweed granules add seaweed to the root zone. "
       'Our humic plus seaweed granules combine both. Read <a href="/resources/humic-vs-seaweed-granules">humic vs seaweed granules</a> and '
       '<a href="/resources/kappaphycus-vs-ascophyllum-vs-sargassum">which seaweed to choose</a>.</p>' + GRAN_SPEC),
 what_title="Seaweed granules: what to know before you buy",
 uses_head=["Application point", "Granule to ask for"],
 uses=[["Basal with fertilizer at sowing or planting", "Humic acid + seaweed extract granules"],
       ["Earthing up and top dressing", "Sargassum tenerrimum 2% granular"],
       ["Retail buckets for dealers", "Either grade in 1 to 20 kg buckets"],
       ["Private label seaweed granules", "Either grade under your brand"]],
 uses_title="Where seaweed granules are used",
 methods=["Broadcast with basal fertilizer", "Band placement near the root zone", "At earthing up or top dressing"],
 wa="Hello Gujarat Bio Organics, please quote seaweed granules. Grade: ___ Pack: ___ Quantity: ___ Destination: ___", liquid=False,
 faq=[("Who is a seaweed granules manufacturer in India?", "Gujarat Bio Organics makes Sargassum tenerrimum 2% granular and humic acid plus seaweed extract granules at its own plant in Shihor, Bhavnagar, Gujarat."),
      ("What are seaweed granules used for?", "They are broadcast with basal fertilizer or at top dressing to bring seaweed into the root zone and support root growth and the crop's response to stress."),
      ("What is the price of seaweed granules per kg?", PRICE_A),
      ("Do you make Kappaphycus or Ascophyllum granules?", "Our granular seaweed grades are Sargassum tenerrimum 2% and humic plus seaweed extract. Kappaphycus and Ascophyllum are supplied as liquids. Send us your specification for any other granule."),
      ("Can I sell seaweed granules under my brand?", "Yes. We pack seaweed granules under your label with no minimum order quantity."),
      ("Are seaweed granules the same as zyme granules?", "Zyme granules is a trade name in India for broadcast granules that carry seaweed, humic acid or protein hydrolysate. Seaweed granules are one kind of zyme granule."),
      ("What pack sizes are available?", "1, 2, 4, 5, 8, 10 and 20 kg bags or buckets, 25 and 50 kg bags, and 600 kg and 1000 kg jumbo bags."),
      ("Do you export seaweed granules?", "Yes, FOB or CIF from Indian ports. Ask what registration the destination country needs.")],
 related=[("/products/sargassum-tenerrimum-2-granular", "Sargassum tenerrimum 2% granular", ""), ("/products/humic-acid-plus-seaweed-extract-granules", "Humic + seaweed granules", ""),
          ("/granular-biostimulants-manufacturer-india", "All granule grades", ""), ("/seaweed-extract-manufacturer-india", "Seaweed extract manufacturer", ""),
          ("/resources/humic-vs-seaweed-granules", "Humic vs seaweed granules", "Guide"), ("/zyme-granules-manufacturer", "Zyme granules", "")],
 kw=("seaweed extract granules manufacturer", ["seaweed granules manufacturer", "seaweed granules fertilizer", "seaweed granules price", "sargassum granules", "seaweed granules bulk", "seaweed granules exporter"]),
 og="/assets/img/humic-seaweed-granules.webp"))

# =============================================================== AMINO ACID GRANULES
cat_page(dict(
 path="/amino-acid-granules-manufacturer-india", crumb="Amino acid granules",
 title="Amino Acid Granules Manufacturer India: Plant-Source | GBO",
 desc="Amino acid and plant-source protein hydrolysate granules made to order at our Gujarat plant. Bulk, private label, export. No MOQ. Free samples.",
 h1="Amino acid granules manufacturer in India",
 lead="Amino acid and plant-source protein hydrolysate granules, made to order at our plant in Bhavnagar. Seven grades, no minimum order, bulk or private label.",
 answer="Amino acid granules carry free amino acids or protein hydrolysate on a granule so they can be broadcast or blended instead of sprayed. Gujarat Bio Organics makes amino acid 5%, 10% and 20% and plant-source protein hydrolysate 1.5%, 16.9%, 25% and 27% in liquid, granule or powder form at its own plant in Shihor, Bhavnagar, Gujarat, to order, for bulk, private-label and export buyers.",
 grades=_rows(G_AMINO), grades_title="Amino acid and protein granule grades", ilist=_il(G_AMINO), groups=[],
 what=("<p>Amino acids and protein hydrolysates are normally sold as liquids or soluble powders for spraying and drip. A granule makes them easy "
       "to broadcast with basal fertilizer or to blend, which suits dealers and brands that sell solid products.</p>"
       "<h3>Amino acid or protein hydrolysate?</h3><p>Amino acid grades are free amino acids at a stated percentage. Protein hydrolysates are "
       'mixtures of amino acids and short peptides made by breaking down plant protein. Read <a href="/resources/protein-hydrolysate-vs-amino-acid">protein hydrolysate vs amino acid</a>.</p>'
       "<h3>Which grades are made as granules?</h3><p>The seven plant-source and amino acid grades above are listed in liquid, granule or powder form, so we can make "
       "them as granules to order. Animal-source protein hydrolysate is a liquid grade and is not made as a granule. Tell us the grade, the active content you need and "
       "the pack, and we confirm the granule specification before a production order.</p>" + GRAN_SPEC),
 what_title="Amino acid granules: what to know before you buy",
 uses_head=["Use", "Grade to ask for"],
 uses=[["Vegetable and horticulture beds", "Protein hydrolysate or amino acid granules"],
       ["Blending with other granules", "Amino acid 5% or plant-source protein hydrolysate 1.5%"],
       ["Higher-content products and brands", "Amino acid 20%, protein hydrolysate 25% or 27%"],
       ["Private label amino granules", "Any grade above, under your brand"]],
 uses_title="Where amino acid granules are used",
 methods=["Broadcast with basal fertilizer", "Band placement near the root zone", "Blended into a granular product"],
 wa="Hello Gujarat Bio Organics, please quote amino acid granules. Grade: ___ Pack: ___ Quantity: ___ Destination: ___", liquid=False,
 faq=[("Who is an amino acid granules manufacturer in India?", "Gujarat Bio Organics makes amino acid and plant-source protein hydrolysate grades, including as granules to order, at its own plant in Shihor, Bhavnagar, Gujarat."),
      ("Which amino acid granule grades do you make?", "Amino acid 5%, 10% and 20%, and plant-source protein hydrolysate 1.5%, 16.9%, 25% and 27%, each listed in liquid, granule or powder form."),
      ("Are amino acid granules made to order?", "Yes. Tell us the grade, active content and pack, and we confirm the granule specification and send a sample before a production order."),
      ("What is the price of amino acid granules per kg?", PRICE_A),
      ("Do you make animal-source amino acid granules?", "No. Our animal-source protein hydrolysate is a liquid grade. Our granule grades are plant-source protein hydrolysate and amino acid."),
      ("Can I sell amino acid granules under my brand?", "Yes. We pack under your label with no minimum order quantity."),
      ("Do you export amino acid granules?", "Yes, FOB or CIF from Indian ports. Ask what registration the destination country needs."),
      ("What pack sizes are available?", "1, 2, 4, 5, 8, 10 and 20 kg bags or buckets, 25 and 50 kg bags, and 600 kg and 1000 kg jumbo bags.")],
 related=[("/amino-acid-protein-hydrolysate-manufacturer-india", "Amino acid and protein hydrolysate", ""), ("/products/amino-acid-20", "Amino acid 20%", ""),
          ("/granular-biostimulants-manufacturer-india", "All granule grades", ""), ("/resources/protein-hydrolysate-vs-amino-acid", "Protein hydrolysate vs amino acid", "Guide"),
          ("/private-label-zyme-granules", "Private label granules", ""), ("/bulk-pricing-and-quotes", "How bulk pricing works", "")],
 kw=("amino acid granules manufacturer", ["amino acid granules", "amino acid granules fertilizer", "protein hydrolysate granules", "amino acid granules price", "amino acid granules bulk", "plant based amino acid granules"])))

# =============================================================== PRIVATE LABEL GRANULES
cat_page(dict(
 path="/private-label-zyme-granules", crumb="Private label granules",
 title="Private Label Zyme & Biostimulant Granules Manufacturer | GBO",
 desc="Sell humic, seaweed and amino acid granules under your own brand. We formulate, make and pack at our Gujarat plant. No MOQ, free samples, fast repeats.",
 h1="Private label zyme and biostimulant granules, made for your brand",
 lead="You sell and market. We make and pack. Your label, your bag, our plant in Bhavnagar, with no minimum order and about one week from confirmed order.",
 answer="Private label granules means we manufacture humic, seaweed or amino acid granules and pack them under your brand name, label and pack design. Gujarat Bio Organics supplies private-label and OEM granules from its own plant in Shihor, Bhavnagar, Gujarat, with no minimum order quantity, free samples and a lead time of about one week from a confirmed order.",
 forms=["Humic acid, seaweed, humic plus seaweed and amino acid granules under your brand", "Buckets, bags and jumbo bags in your artwork",
        "Trial batches before you commit to volume", "A specification sheet, NOC copy and test report to support your own registration and dealer pitch",
        "Repeat batches on a schedule you set"],
 forms_title="What we do for brand owners",
 what=("<h3>How it works</h3><ol><li><strong>You tell us</strong> the grade, the pack sizes and the volume you expect.</li>"
       "<li><strong>We send a sample</strong> of the granule and the specification sheet.</li>"
       "<li><strong>You approve</strong> the sample and send your label artwork.</li>"
       "<li><strong>We make a trial batch</strong> in your packing and ship it.</li>"
       "<li><strong>You reorder</strong> on a schedule that fits your season.</li></ol>"
       "<h3>Registration for your own brand</h3><p>Check with your state agriculture department what registration a product sold under your own brand needs. "
       "We share our NOC, specification and test report to support your application, and we confirm the grade and label wording against the Fertiliser Control Order before artwork is final.</p>"
       '<p>See also our general <a href="/private-label-oem">private label and OEM</a> page and <a href="/resources/how-to-start-a-fertilizer-brand-private-label">how to start a fertilizer brand</a>.</p>'),
 what_title="Private label granules, step by step",
 uses_head=["What you bring", "What we do"],
 uses=[["Your brand, label and pack design", "Print-ready artwork guidance and packing in your sizes"],
       ["Your target grade and volume", "Sample, specification sheet and a quote against your volume"],
       ["Your dealer network", "Consistent batches and repeat supply for your season"],
       ["Your destination", "Domestic dispatch or export documents, FOB or CIF"]],
 uses_title="Who does what",
 wa="Hello Gujarat Bio Organics, I want private label granules. Grade: ___ Pack: ___ Volume: ___ Market: ___", liquid=False,
 faq=[("Do you make private label zyme granules?", "Yes. We make humic, seaweed, humic plus seaweed and plant-source amino acid granules and pack them under your brand."),
      ("What is the minimum order for private label granules?", "There is no minimum order quantity. Trial batches are quoted as well as bulk."),
      ("How long does a private label granule order take?", "About one week from a confirmed order. Tell us your season and we plan backwards from it."),
      ("Do you supply a specification sheet and NOC copy?", "Yes, on request. They support your dealer pitch and your own registration."),
      ("What pack sizes can you do?", "1, 2, 4, 5, 8, 10 and 20 kg bags or buckets, 25 and 50 kg bags, and 600 kg and 1000 kg jumbo bags."),
      ("Can you export private label granules?", "Yes, FOB or CIF from Indian ports to your destination."),
      ("Who owns the formula and the brand?", "You own your brand and label. We keep our formulation know-how private. Agree the terms in writing before the first batch.")],
 related=[("/granular-biostimulants-manufacturer-india", "All granule grades", ""), ("/private-label-oem", "Private label and OEM", ""),
          ("/bulk-pricing-and-quotes", "How bulk pricing works", ""), ("/humic-acid-granules-manufacturer-india", "Humic acid granules", ""),
          ("/seaweed-extract-granules-manufacturer-india", "Seaweed granules", ""), ("/export", "Export", "")],
 kw=("private label zyme granules", ["private label granules manufacturer", "oem humic granules", "private label seaweed granules", "contract manufacturing biostimulant granules", "own brand granules"]), aud="Brand owners, dealers, importers"))

# =============================================================== BLENDERS
cat_page(dict(
 path="/granules-for-npk-blenders", crumb="Granules for blenders",
 title="Biostimulant Granules for NPK & Fertilizer Blenders | GBO",
 desc="Humic, seaweed and amino acid granules to add to NPK and compound fertilizer blends. Bulk supply from Gujarat. Samples to match your base granule. No MOQ.",
 h1="Biostimulant granules for NPK and fertilizer blenders",
 lead="Add a humic, seaweed or amino acid granule to your blend. We supply by the tonne and send a sample so you can test the mix before you order.",
 answer="Fertilizer blenders and granulators add a biostimulant granule to an NPK or compound blend to offer a value-added product. Gujarat Bio Organics supplies humic acid, seaweed and amino acid granules in bulk from its own plant in Shihor, Bhavnagar, Gujarat, with no minimum order and free samples, so you can test the blend with your own base granule before a production order.",
 forms=["Humic acid 51% granular and 1.5% granules for blends", "Humic plus seaweed and Sargassum granules for blends", "Plant-source amino acid and protein hydrolysate granules, made to order",
        "Jumbo bags of 600 and 1000 kg for blending plants", "A sample to test with your base granule before a production order"],
 forms_title="What we supply to blenders",
 what=("<h3>What to check before you blend</h3><ul>"
       "<li><strong>Granule size.</strong> A granule that differs in size from the base granule can separate during handling. Send us your base granule size and we confirm what we can supply.</li>"
       "<li><strong>Bulk density.</strong> Match density to your base product so the blend stays even from the plant to the field.</li>"
       "<li><strong>Moisture and dust.</strong> A dry, low-dust granule blends cleanly and stores well.</li>"
       "<li><strong>Compatibility.</strong> Humic acid mixes with most fertilizers. Do a small trial blend first, and check any strongly acidic or very hygroscopic component.</li>"
       "<li><strong>Label.</strong> The final blend carries its own grade and label under the Fertiliser Control Order. Check what your blend needs with your state agriculture department.</li></ul>"
       + GRAN_SPEC),
 what_title="Adding a biostimulant granule to a blend",
 uses_head=["Your need", "What to ask us"],
 uses=[["A humic granule for a premium NPK line", "Humic acid 51% granular or 1.5% granules, with the specification sheet"],
       ["A seaweed granule in a blend", "Sargassum tenerrimum 2% granular or humic plus seaweed granules"],
       ["An amino acid granule in a blend", "Amino acid or plant-source protein hydrolysate granule, made to order"],
       ["Regular supply to a blending plant", "Jumbo bags on a delivery schedule"]],
 uses_title="Blender checklist",
 wa="Hello Gujarat Bio Organics, I blend fertilizers and want biostimulant granules. Base granule size: ___ Grade: ___ Monthly volume: ___", liquid=False,
 faq=[("Can biostimulant granules be added to an NPK blend?", "Yes. Many blenders add a humic, seaweed or amino acid granule to a blend as a value-added product. Test a small trial blend first."),
      ("What granule size do you supply for blending?", "It depends on the grade and batch. Send us your base granule size and we confirm what we can supply and send a sample."),
      ("Do you supply jumbo bags to blenders?", "Yes, 600 kg and 1000 kg jumbo bags, as well as 25 and 50 kg bags."),
      ("Is there a minimum order for blenders?", "No. We quote trial quantities and regular supply."),
      ("Do you give samples for blending trials?", "Yes. Samples are free; the buyer pays freight or courier and other charges."),
      ("What is the price per tonne of biostimulant granules?", PRICE_A)],
 related=[("/granular-biostimulants-manufacturer-india", "All granule grades", ""), ("/humic-acid-granules-manufacturer-india", "Humic acid granules", ""),
          ("/custom-fertilizer-blends", "Custom blends", ""), ("/bulk-supply", "Bulk supply", ""),
          ("/slow-release-fertilizer", "Slow-release fertilizer", ""), ("/bulk-pricing-and-quotes", "How bulk pricing works", "")],
 kw=("biostimulant granules for npk blenders", ["humic granules for npk blending", "fertilizer blenders humic granules supplier", "value added npk granules", "bulk humic granules for blending"]), aud="Blenders, granulators, fertilizer companies"))
