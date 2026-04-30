from typing import List

# Search URLs per brand — always land on a search results page so links never 404
_BRAND_URLS = {
    "West Elm":              "https://www.westelm.com/search/results.html?words={}",
    "Crate & Barrel":        "https://www.crateandbarrel.com/search?q={}",
    "Article":               "https://www.article.com/search?query={}",
    "Joybird":               "https://joybird.com/search/?q={}",
    "Burrow":                "https://burrow.com/search?q={}",
    "Pottery Barn":          "https://www.potterybarn.com/search/results.html?words={}",
    "CB2":                   "https://www.cb2.com/search?q={}",
    "IKEA":                  "https://www.ikea.com/us/en/search/?q={}",
    "Blu Dot":               "https://www.bludot.com/search/?q={}",
    "Anthropologie":         "https://www.anthropologie.com/search?q={}",
    "Rejuvenation":          "https://www.rejuvenation.com/search?q={}",
    "Schoolhouse":           "https://www.schoolhouse.com/search?q={}",
    "Arteriors":             "https://www.arteriorshome.com/search?q={}",
    "Ruggable":              "https://ruggable.com/search?q={}",
    "Loloi":                 "https://www.loloirugs.com/search?q={}",
    "Dash & Albert":         "https://www.dashandalbert.com/search?q={}",
    "Surya":                 "https://surya.com/search?q={}",
    "Nourison":              "https://www.nourison.com/search?q={}",
    "Herman Miller":         "https://www.hermanmiller.com/search/?q={}",
    "Design Within Reach":   "https://www.dwr.com/search?q={}",
    "Kardiel":               "https://www.kardiel.com/search?q={}",
    "World Market":          "https://www.worldmarket.com/search?keywords={}",
    "Serena & Lily":         "https://www.serenaandlily.com/search?q={}",
    "Arhaus":                "https://www.arhaus.com/search/?q={}",
    "Jungalow":              "https://www.jungalow.com/search?q={}",
    "Restoration Hardware":  "https://rh.com/search/results.jsp?query={}",
    "Ethan Allen":           "https://www.ethanallen.com/search?q={}",
    "Bassett":               "https://www.bassettfurniture.com/search?q={}",
    "Purple":                "https://purple.com/search?q={}",
    "Saatva":                "https://www.saatva.com/search?q={}",
    "Muuto":                 "https://muuto.com/search/?q={}",
    "Hay":                   "https://hay.dk/en/search?q={}",
    "Menu":                  "https://www.mooseinterior.com/search?q={}",
    "String":                "https://www.stringfurniture.com/search?q={}",
}

def _product_url(brand: str, name: str) -> str:
    import urllib.parse
    template = _BRAND_URLS.get(brand, "https://www.google.com/search?q={}+furniture")
    return template.format(urllib.parse.quote_plus(name))

# Each product belongs to a category+style. Multiple products per category = alternatives to swap between.
PRODUCTS = [
    # ── SOFA ──────────────────────────────────────────────────────────────────
    {"id": 1,  "name": "Low-Profile Linen Sofa",        "category": "Sofa", "style": "modern",       "brand": "West Elm",         "origin_country": "China",          "unit_cost_usd": 420,  "weight_kg": 48, "hs_code": "940161"},
    {"id": 2,  "name": "Velvet Channel Sofa",            "category": "Sofa", "style": "modern",       "brand": "Crate & Barrel",   "origin_country": "Vietnam",        "unit_cost_usd": 580,  "weight_kg": 52, "hs_code": "940161"},
    {"id": 3,  "name": "Cloud Modular Sofa",             "category": "Sofa", "style": "modern",       "brand": "Article",          "origin_country": "Vietnam",        "unit_cost_usd": 720,  "weight_kg": 60, "hs_code": "940161"},
    {"id": 4,  "name": "Chesterfield Leather Sofa",     "category": "Sofa", "style": "traditional",  "brand": "Joybird",          "origin_country": "United Kingdom", "unit_cost_usd": 1100, "weight_kg": 65, "hs_code": "940161"},
    {"id": 5,  "name": "Roll-Arm Fabric Sofa",          "category": "Sofa", "style": "traditional",  "brand": "Burrow",           "origin_country": "China",          "unit_cost_usd": 680,  "weight_kg": 58, "hs_code": "940161"},
    {"id": 6,  "name": "Rattan & Cushion Sofa",         "category": "Sofa", "style": "boho",         "brand": "Pottery Barn",     "origin_country": "Indonesia",      "unit_cost_usd": 490,  "weight_kg": 40, "hs_code": "940150"},
    {"id": 7,  "name": "Boho Woven Linen Sofa",         "category": "Sofa", "style": "boho",         "brand": "West Elm",         "origin_country": "India",          "unit_cost_usd": 530,  "weight_kg": 44, "hs_code": "940161"},
    {"id": 8,  "name": "Tufted Wingback Sofa",          "category": "Sofa", "style": "mid-century",  "brand": "Crate & Barrel",   "origin_country": "China",          "unit_cost_usd": 650,  "weight_kg": 55, "hs_code": "940161"},
    {"id": 9,  "name": "Low-Slung Walnut-Leg Sofa",     "category": "Sofa", "style": "mid-century",  "brand": "Article",          "origin_country": "Vietnam",        "unit_cost_usd": 780,  "weight_kg": 57, "hs_code": "940161"},
    {"id": 10, "name": "Slim Oak-Leg Sofa",             "category": "Sofa", "style": "scandinavian", "brand": "Joybird",          "origin_country": "Poland",         "unit_cost_usd": 520,  "weight_kg": 45, "hs_code": "940161"},
    {"id": 11, "name": "Light Grey Hygge Sofa",         "category": "Sofa", "style": "scandinavian", "brand": "Burrow",           "origin_country": "Poland",         "unit_cost_usd": 610,  "weight_kg": 48, "hs_code": "940161"},
    {"id": 12, "name": "Metal Frame Industrial Sofa",   "category": "Sofa", "style": "industrial",   "brand": "Pottery Barn",     "origin_country": "China",          "unit_cost_usd": 460,  "weight_kg": 50, "hs_code": "940161"},
    {"id": 13, "name": "Canvas Utility Sofa",           "category": "Sofa", "style": "industrial",   "brand": "West Elm",         "origin_country": "Vietnam",        "unit_cost_usd": 390,  "weight_kg": 46, "hs_code": "940161"},

    # ── COFFEE TABLE ──────────────────────────────────────────────────────────
    {"id": 20, "name": "Walnut Slab Coffee Table",      "category": "Coffee Table", "style": "modern",       "brand": "CB2",        "origin_country": "Vietnam",   "unit_cost_usd": 180, "weight_kg": 18, "hs_code": "940360"},
    {"id": 21, "name": "Marble Top Coffee Table",       "category": "Coffee Table", "style": "modern",       "brand": "West Elm",   "origin_country": "Italy",     "unit_cost_usd": 320, "weight_kg": 30, "hs_code": "940360"},
    {"id": 22, "name": "Smoked Glass Coffee Table",     "category": "Coffee Table", "style": "modern",       "brand": "Article",    "origin_country": "China",     "unit_cost_usd": 240, "weight_kg": 24, "hs_code": "940360"},
    {"id": 23, "name": "Hairpin Leg Coffee Table",      "category": "Coffee Table", "style": "mid-century",  "brand": "IKEA",       "origin_country": "Vietnam",   "unit_cost_usd": 160, "weight_kg": 14, "hs_code": "940360"},
    {"id": 24, "name": "Teak Round Coffee Table",       "category": "Coffee Table", "style": "mid-century",  "brand": "Blu Dot",    "origin_country": "Indonesia", "unit_cost_usd": 195, "weight_kg": 16, "hs_code": "940360"},
    {"id": 25, "name": "Rattan Woven Coffee Table",     "category": "Coffee Table", "style": "boho",         "brand": "CB2",        "origin_country": "Indonesia", "unit_cost_usd": 140, "weight_kg": 10, "hs_code": "940150"},
    {"id": 26, "name": "Mosaic Tile Coffee Table",      "category": "Coffee Table", "style": "boho",         "brand": "West Elm",   "origin_country": "India",     "unit_cost_usd": 175, "weight_kg": 20, "hs_code": "940360"},
    {"id": 27, "name": "Reclaimed Wood Coffee Table",   "category": "Coffee Table", "style": "industrial",   "brand": "Article",    "origin_country": "Vietnam",   "unit_cost_usd": 210, "weight_kg": 22, "hs_code": "940360"},
    {"id": 28, "name": "Pipe & Steel Coffee Table",     "category": "Coffee Table", "style": "industrial",   "brand": "IKEA",       "origin_country": "China",     "unit_cost_usd": 185, "weight_kg": 26, "hs_code": "940360"},
    {"id": 29, "name": "White Lacquer Coffee Table",    "category": "Coffee Table", "style": "scandinavian", "brand": "Blu Dot",    "origin_country": "Poland",    "unit_cost_usd": 195, "weight_kg": 16, "hs_code": "940360"},
    {"id": 30, "name": "Birch Nest Coffee Tables",      "category": "Coffee Table", "style": "scandinavian", "brand": "CB2",        "origin_country": "Poland",    "unit_cost_usd": 170, "weight_kg": 12, "hs_code": "940360"},

    # ── ACCENT CHAIR ─────────────────────────────────────────────────────────
    {"id": 40, "name": "Boucle Accent Chair",           "category": "Accent Chair", "style": "modern",       "brand": "Article",       "origin_country": "China",     "unit_cost_usd": 280, "weight_kg": 16, "hs_code": "940171"},
    {"id": 41, "name": "Swivel Barrel Chair",           "category": "Accent Chair", "style": "modern",       "brand": "Anthropologie", "origin_country": "China",     "unit_cost_usd": 340, "weight_kg": 20, "hs_code": "940171"},
    {"id": 42, "name": "Egg Accent Chair",              "category": "Accent Chair", "style": "mid-century",  "brand": "CB2",           "origin_country": "China",     "unit_cost_usd": 310, "weight_kg": 18, "hs_code": "940171"},
    {"id": 43, "name": "Tulip Pedestal Chair",          "category": "Accent Chair", "style": "mid-century",  "brand": "West Elm",      "origin_country": "Vietnam",   "unit_cost_usd": 295, "weight_kg": 15, "hs_code": "940171"},
    {"id": 44, "name": "Rattan Lounge Chair",           "category": "Accent Chair", "style": "boho",         "brand": "Joybird",       "origin_country": "Indonesia", "unit_cost_usd": 275, "weight_kg": 12, "hs_code": "940150"},
    {"id": 45, "name": "Macrame Hanging Chair",         "category": "Accent Chair", "style": "boho",         "brand": "Article",       "origin_country": "India",     "unit_cost_usd": 230, "weight_kg": 8,  "hs_code": "940150"},
    {"id": 46, "name": "Wingback Armchair",             "category": "Accent Chair", "style": "traditional",  "brand": "Anthropologie", "origin_country": "China",     "unit_cost_usd": 480, "weight_kg": 28, "hs_code": "940161"},
    {"id": 47, "name": "Button-Tufted Club Chair",      "category": "Accent Chair", "style": "traditional",  "brand": "CB2",           "origin_country": "Vietnam",   "unit_cost_usd": 420, "weight_kg": 24, "hs_code": "940161"},
    {"id": 48, "name": "Leather Sling Chair",           "category": "Accent Chair", "style": "industrial",   "brand": "West Elm",      "origin_country": "China",     "unit_cost_usd": 320, "weight_kg": 15, "hs_code": "940171"},
    {"id": 49, "name": "Sheepskin Accent Chair",        "category": "Accent Chair", "style": "scandinavian", "brand": "Joybird",       "origin_country": "Poland",    "unit_cost_usd": 350, "weight_kg": 14, "hs_code": "940171"},
    {"id": 50, "name": "Curved Ash-Wood Chair",         "category": "Accent Chair", "style": "scandinavian", "brand": "Article",       "origin_country": "Poland",    "unit_cost_usd": 310, "weight_kg": 12, "hs_code": "940171"},

    # ── FLOOR LAMP ────────────────────────────────────────────────────────────
    {"id": 60, "name": "Arc Brass Floor Lamp",          "category": "Floor Lamp", "style": "modern",       "brand": "CB2",          "origin_country": "China",     "unit_cost_usd": 120, "weight_kg": 6,  "hs_code": "940510"},
    {"id": 61, "name": "Concrete Base Floor Lamp",      "category": "Floor Lamp", "style": "modern",       "brand": "West Elm",     "origin_country": "China",     "unit_cost_usd": 145, "weight_kg": 9,  "hs_code": "940510"},
    {"id": 62, "name": "Tripod Walnut Floor Lamp",      "category": "Floor Lamp", "style": "mid-century",  "brand": "Rejuvenation", "origin_country": "China",     "unit_cost_usd": 110, "weight_kg": 4,  "hs_code": "940510"},
    {"id": 63, "name": "Sputnik Globe Floor Lamp",      "category": "Floor Lamp", "style": "mid-century",  "brand": "Schoolhouse",  "origin_country": "China",     "unit_cost_usd": 130, "weight_kg": 5,  "hs_code": "940510"},
    {"id": 64, "name": "Rattan Woven Floor Lamp",       "category": "Floor Lamp", "style": "boho",         "brand": "Arteriors",    "origin_country": "Indonesia", "unit_cost_usd": 95,  "weight_kg": 3,  "hs_code": "940510"},
    {"id": 65, "name": "Bamboo Shade Floor Lamp",       "category": "Floor Lamp", "style": "boho",         "brand": "CB2",          "origin_country": "Vietnam",   "unit_cost_usd": 85,  "weight_kg": 4,  "hs_code": "940510"},
    {"id": 66, "name": "Industrial Pipe Floor Lamp",    "category": "Floor Lamp", "style": "industrial",   "brand": "West Elm",     "origin_country": "China",     "unit_cost_usd": 85,  "weight_kg": 5,  "hs_code": "940510"},
    {"id": 67, "name": "Edison Cage Floor Lamp",        "category": "Floor Lamp", "style": "industrial",   "brand": "Rejuvenation", "origin_country": "China",     "unit_cost_usd": 75,  "weight_kg": 4,  "hs_code": "940510"},
    {"id": 68, "name": "Slim White Floor Lamp",         "category": "Floor Lamp", "style": "scandinavian", "brand": "Schoolhouse",  "origin_country": "China",     "unit_cost_usd": 75,  "weight_kg": 3,  "hs_code": "940510"},
    {"id": 69, "name": "Beech Wood Arc Lamp",           "category": "Floor Lamp", "style": "scandinavian", "brand": "Arteriors",    "origin_country": "Poland",    "unit_cost_usd": 105, "weight_kg": 5,  "hs_code": "940510"},

    # ── AREA RUG ──────────────────────────────────────────────────────────────
    {"id": 80, "name": "Abstract Wool Rug 5x8",         "category": "Area Rug", "style": "modern",       "brand": "Ruggable",      "origin_country": "India",     "unit_cost_usd": 130, "weight_kg": 8,  "hs_code": "570110"},
    {"id": 81, "name": "Shaggy Ivory Rug 6x9",          "category": "Area Rug", "style": "modern",       "brand": "Loloi",         "origin_country": "India",     "unit_cost_usd": 160, "weight_kg": 10, "hs_code": "570110"},
    {"id": 82, "name": "Persian-Style Rug 8x10",        "category": "Area Rug", "style": "traditional",  "brand": "Dash & Albert", "origin_country": "Turkey",    "unit_cost_usd": 320, "weight_kg": 14, "hs_code": "570110"},
    {"id": 83, "name": "Floral Hand-Knotted Rug",       "category": "Area Rug", "style": "traditional",  "brand": "Surya",         "origin_country": "India",     "unit_cost_usd": 290, "weight_kg": 12, "hs_code": "570110"},
    {"id": 84, "name": "Woven Jute Rug 6x9",            "category": "Area Rug", "style": "boho",         "brand": "Nourison",      "origin_country": "India",     "unit_cost_usd": 110, "weight_kg": 9,  "hs_code": "570390"},
    {"id": 85, "name": "Kilim Patchwork Rug",           "category": "Area Rug", "style": "boho",         "brand": "Ruggable",      "origin_country": "Turkey",    "unit_cost_usd": 200, "weight_kg": 11, "hs_code": "570110"},
    {"id": 86, "name": "Flatweave Geometric Rug",       "category": "Area Rug", "style": "scandinavian", "brand": "Loloi",         "origin_country": "India",     "unit_cost_usd": 150, "weight_kg": 7,  "hs_code": "570110"},
    {"id": 87, "name": "Cowhide Patchwork Rug",         "category": "Area Rug", "style": "industrial",   "brand": "Dash & Albert", "origin_country": "Brazil",    "unit_cost_usd": 260, "weight_kg": 10, "hs_code": "570110"},
    {"id": 88, "name": "Low-Pile Charcoal Rug 5x8",     "category": "Area Rug", "style": "industrial",   "brand": "Surya",         "origin_country": "India",     "unit_cost_usd": 145, "weight_kg": 8,  "hs_code": "570110"},

    # ── BOOKSHELF / STORAGE ───────────────────────────────────────────────────
    {"id": 100, "name": "Minimalist Floating Shelf",    "category": "Bookshelf", "style": "modern",       "brand": "West Elm",        "origin_country": "Vietnam", "unit_cost_usd": 120, "weight_kg": 8,  "hs_code": "940360"},
    {"id": 101, "name": "Modular Cube Shelving",        "category": "Bookshelf", "style": "modern",       "brand": "IKEA",            "origin_country": "Vietnam", "unit_cost_usd": 200, "weight_kg": 18, "hs_code": "940360"},
    {"id": 102, "name": "Pipe & Wood Shelf Unit",       "category": "Bookshelf", "style": "industrial",   "brand": "CB2",             "origin_country": "China",   "unit_cost_usd": 160, "weight_kg": 20, "hs_code": "940360"},
    {"id": 103, "name": "Iron & Reclaimed Wood Shelf",  "category": "Bookshelf", "style": "industrial",   "brand": "Crate & Barrel",  "origin_country": "India",   "unit_cost_usd": 185, "weight_kg": 22, "hs_code": "940360"},
    {"id": 104, "name": "Rattan Storage Shelves",       "category": "Bookshelf", "style": "boho",         "brand": "Article",         "origin_country": "Indonesia","unit_cost_usd": 180, "weight_kg": 15, "hs_code": "940150"},
    {"id": 105, "name": "Solid Oak Bookcase",           "category": "Bookshelf", "style": "scandinavian", "brand": "West Elm",        "origin_country": "Poland",  "unit_cost_usd": 320, "weight_kg": 35, "hs_code": "940360"},
    {"id": 106, "name": "Ladder Shelf Birch",           "category": "Bookshelf", "style": "scandinavian", "brand": "IKEA",            "origin_country": "Poland",  "unit_cost_usd": 175, "weight_kg": 14, "hs_code": "940360"},

    # ── SIDE TABLE ────────────────────────────────────────────────────────────
    {"id": 120, "name": "Marble & Gold Side Table",     "category": "Side Table", "style": "modern",       "brand": "CB2",      "origin_country": "China",     "unit_cost_usd": 95,  "weight_kg": 6,  "hs_code": "940360"},
    {"id": 121, "name": "Acrylic Ghost Side Table",     "category": "Side Table", "style": "modern",       "brand": "West Elm", "origin_country": "China",     "unit_cost_usd": 80,  "weight_kg": 3,  "hs_code": "940360"},
    {"id": 122, "name": "Drum Rattan Side Table",       "category": "Side Table", "style": "boho",         "brand": "Article",  "origin_country": "Indonesia", "unit_cost_usd": 75,  "weight_kg": 4,  "hs_code": "940150"},
    {"id": 123, "name": "Wicker & Glass Side Table",    "category": "Side Table", "style": "boho",         "brand": "IKEA",     "origin_country": "India",     "unit_cost_usd": 85,  "weight_kg": 5,  "hs_code": "940150"},
    {"id": 124, "name": "Hairpin Leg Side Table",       "category": "Side Table", "style": "mid-century",  "brand": "Blu Dot",  "origin_country": "Vietnam",   "unit_cost_usd": 85,  "weight_kg": 5,  "hs_code": "940360"},
    {"id": 125, "name": "Tulip Side Table",             "category": "Side Table", "style": "mid-century",  "brand": "CB2",      "origin_country": "China",     "unit_cost_usd": 90,  "weight_kg": 4,  "hs_code": "940360"},
    {"id": 126, "name": "Reclaimed Wood Side Table",    "category": "Side Table", "style": "industrial",   "brand": "West Elm", "origin_country": "Vietnam",   "unit_cost_usd": 90,  "weight_kg": 7,  "hs_code": "940360"},
    {"id": 127, "name": "Solid Pine Side Table",        "category": "Side Table", "style": "scandinavian", "brand": "Article",  "origin_country": "Poland",    "unit_cost_usd": 70,  "weight_kg": 5,  "hs_code": "940360"},

    # ── BED ───────────────────────────────────────────────────────────────────
    {"id": 140, "name": "Upholstered Platform Bed",     "category": "Bed", "style": "modern",       "brand": "Purple",               "origin_country": "China",     "unit_cost_usd": 480,  "weight_kg": 55, "hs_code": "940310"},
    {"id": 141, "name": "Floating Walnut Bed Frame",    "category": "Bed", "style": "modern",       "brand": "Saatva",               "origin_country": "Vietnam",   "unit_cost_usd": 620,  "weight_kg": 58, "hs_code": "940310"},
    {"id": 142, "name": "Canopy Four-Poster Bed",       "category": "Bed", "style": "traditional",  "brand": "Pottery Barn",         "origin_country": "India",     "unit_cost_usd": 890,  "weight_kg": 80, "hs_code": "940310"},
    {"id": 143, "name": "Sleigh Bed Frame",             "category": "Bed", "style": "traditional",  "brand": "West Elm",             "origin_country": "China",     "unit_cost_usd": 720,  "weight_kg": 72, "hs_code": "940310"},
    {"id": 144, "name": "Rattan Headboard Bed",         "category": "Bed", "style": "boho",         "brand": "Restoration Hardware", "origin_country": "Indonesia", "unit_cost_usd": 510,  "weight_kg": 45, "hs_code": "940310"},
    {"id": 145, "name": "Macrame-Wrapped Bed Frame",    "category": "Bed", "style": "boho",         "brand": "Purple",               "origin_country": "India",     "unit_cost_usd": 430,  "weight_kg": 40, "hs_code": "940310"},
    {"id": 146, "name": "Low Profile Teak Bed",         "category": "Bed", "style": "mid-century",  "brand": "Saatva",               "origin_country": "Indonesia", "unit_cost_usd": 680,  "weight_kg": 60, "hs_code": "940310"},
    {"id": 147, "name": "Tapered-Leg Walnut Bed",       "category": "Bed", "style": "mid-century",  "brand": "Pottery Barn",         "origin_country": "Vietnam",   "unit_cost_usd": 740,  "weight_kg": 62, "hs_code": "940310"},
    {"id": 148, "name": "Solid Pine Slatted Bed",       "category": "Bed", "style": "scandinavian", "brand": "West Elm",             "origin_country": "Poland",    "unit_cost_usd": 550,  "weight_kg": 50, "hs_code": "940310"},
    {"id": 149, "name": "White Ash Storage Bed",        "category": "Bed", "style": "scandinavian", "brand": "Restoration Hardware", "origin_country": "Poland",    "unit_cost_usd": 680,  "weight_kg": 65, "hs_code": "940310"},
    {"id": 150, "name": "Industrial Pipe Bed Frame",    "category": "Bed", "style": "industrial",   "brand": "Purple",               "origin_country": "China",     "unit_cost_usd": 390,  "weight_kg": 48, "hs_code": "940310"},

    # ── DINING TABLE ─────────────────────────────────────────────────────────
    {"id": 160, "name": "Marble & Brass Dining Table",  "category": "Dining Table", "style": "modern",       "brand": "Restoration Hardware", "origin_country": "Italy",     "unit_cost_usd": 640,  "weight_kg": 55, "hs_code": "940360"},
    {"id": 161, "name": "Extendable Oak Dining Table",  "category": "Dining Table", "style": "modern",       "brand": "Pottery Barn",         "origin_country": "Vietnam",   "unit_cost_usd": 480,  "weight_kg": 42, "hs_code": "940360"},
    {"id": 162, "name": "Farmhouse Pedestal Table",     "category": "Dining Table", "style": "traditional",  "brand": "West Elm",             "origin_country": "China",     "unit_cost_usd": 520,  "weight_kg": 50, "hs_code": "940360"},
    {"id": 163, "name": "Solid Mahogany Dining Table",  "category": "Dining Table", "style": "traditional",  "brand": "CB2",                  "origin_country": "Indonesia", "unit_cost_usd": 780,  "weight_kg": 70, "hs_code": "940360"},
    {"id": 164, "name": "Round Rattan Dining Table",    "category": "Dining Table", "style": "boho",         "brand": "Arhaus",               "origin_country": "Indonesia", "unit_cost_usd": 350,  "weight_kg": 30, "hs_code": "940150"},
    {"id": 165, "name": "Mango Wood Boho Table",        "category": "Dining Table", "style": "boho",         "brand": "Restoration Hardware", "origin_country": "India",     "unit_cost_usd": 420,  "weight_kg": 38, "hs_code": "940360"},
    {"id": 166, "name": "Tulip Round Dining Table",     "category": "Dining Table", "style": "mid-century",  "brand": "Pottery Barn",         "origin_country": "China",     "unit_cost_usd": 390,  "weight_kg": 32, "hs_code": "940360"},
    {"id": 167, "name": "Hairpin-Leg Dining Table",     "category": "Dining Table", "style": "mid-century",  "brand": "West Elm",             "origin_country": "Vietnam",   "unit_cost_usd": 340,  "weight_kg": 28, "hs_code": "940360"},
    {"id": 168, "name": "Drop-Leaf Pine Table",         "category": "Dining Table", "style": "scandinavian", "brand": "CB2",                  "origin_country": "Poland",    "unit_cost_usd": 380,  "weight_kg": 30, "hs_code": "940360"},
    {"id": 169, "name": "Reclaimed Plank Dining Table", "category": "Dining Table", "style": "industrial",   "brand": "Arhaus",               "origin_country": "Vietnam",   "unit_cost_usd": 410,  "weight_kg": 45, "hs_code": "940360"},

    # ── DRESSER ───────────────────────────────────────────────────────────────
    {"id": 180, "name": "6-Drawer Walnut Dresser",      "category": "Dresser", "style": "modern",       "brand": "West Elm",     "origin_country": "Vietnam",   "unit_cost_usd": 420,  "weight_kg": 50, "hs_code": "940330"},
    {"id": 181, "name": "Lacquer High-Gloss Dresser",   "category": "Dresser", "style": "modern",       "brand": "Pottery Barn", "origin_country": "China",     "unit_cost_usd": 360,  "weight_kg": 45, "hs_code": "940330"},
    {"id": 182, "name": "Antique White Dresser",        "category": "Dresser", "style": "traditional",  "brand": "IKEA",         "origin_country": "China",     "unit_cost_usd": 490,  "weight_kg": 60, "hs_code": "940330"},
    {"id": 183, "name": "Rattan-Front Boho Dresser",    "category": "Dresser", "style": "boho",         "brand": "Article",      "origin_country": "Indonesia", "unit_cost_usd": 380,  "weight_kg": 42, "hs_code": "940330"},
    {"id": 184, "name": "Tapered-Leg Teak Dresser",     "category": "Dresser", "style": "mid-century",  "brand": "CB2",          "origin_country": "Indonesia", "unit_cost_usd": 510,  "weight_kg": 55, "hs_code": "940330"},
    {"id": 185, "name": "Solid Birch 5-Drawer Dresser", "category": "Dresser", "style": "scandinavian", "brand": "West Elm",     "origin_country": "Poland",    "unit_cost_usd": 480,  "weight_kg": 52, "hs_code": "940330"},
    {"id": 186, "name": "Black Iron & Wood Dresser",    "category": "Dresser", "style": "industrial",   "brand": "Pottery Barn", "origin_country": "India",     "unit_cost_usd": 390,  "weight_kg": 48, "hs_code": "940330"},
]

# Inject product_url into every product at module load time
for _p in PRODUCTS:
    _p["product_url"] = _product_url(_p["brand"], _p["name"])

# Wall colors per mood
WALL_COLORS = {
    "light": [
        {"name": "Warm White",    "hex": "#F5F0E8", "description": "Brightens the space without feeling cold"},
        {"name": "Soft Linen",    "hex": "#EDE8DE", "description": "Warm neutral that works with any wood tone"},
        {"name": "Pale Sage",     "hex": "#D4DDD0", "description": "Calming green-grey, brings nature indoors"},
        {"name": "Creamy Pearl",  "hex": "#F0EBE0", "description": "Classic warm off-white, timeless and versatile"},
    ],
    "dark": [
        {"name": "Charcoal Slate", "hex": "#3A3D42", "description": "Dramatic backdrop that makes furniture pop"},
        {"name": "Deep Forest",    "hex": "#2D3B30", "description": "Rich green creates a cozy, enveloping feel"},
        {"name": "Midnight Navy",  "hex": "#1E2A3A", "description": "Sophisticated and moody, great for evening rooms"},
        {"name": "Espresso Brown", "hex": "#2C1F1A", "description": "Warm dark tone, pairs well with brass accents"},
    ],
    "warm": [
        {"name": "Terracotta Blush", "hex": "#D4907A", "description": "Earthy warmth inspired by Mediterranean tones"},
        {"name": "Dusty Peach",      "hex": "#E8BEA8", "description": "Flattering warm tone, glows in natural light"},
        {"name": "Golden Wheat",     "hex": "#D4B483", "description": "Honey-warm, pairs beautifully with dark wood"},
        {"name": "Burnt Sienna",     "hex": "#C4724A", "description": "Bold earthy statement for accent walls"},
    ],
    "cool": [
        {"name": "Mist Blue",     "hex": "#B8C8D4", "description": "Serene and airy, ideal for bedrooms"},
        {"name": "Soft Lavender", "hex": "#C8C0D4", "description": "Calming purple-grey, adds sophistication"},
        {"name": "Steel Blue",    "hex": "#6E8FA8", "description": "Strong cool tone, pairs with white trim"},
        {"name": "Pale Aqua",     "hex": "#A8C8C4", "description": "Fresh coastal feel, bright and refreshing"},
    ],
}

# Wall decor options
WALL_DECOR = [
    {"id": "wd1", "name": "Abstract Canvas Print",       "style": ["modern", "scandinavian"],             "origin_country": "China",   "unit_cost_usd": 85,  "weight_kg": 2, "hs_code": "970110"},
    {"id": "wd2", "name": "Macrame Wall Hanging",         "style": ["boho"],                               "origin_country": "India",   "unit_cost_usd": 45,  "weight_kg": 1, "hs_code": "630790"},
    {"id": "wd3", "name": "Sunburst Mirror",              "style": ["mid-century", "traditional"],         "origin_country": "Mexico",  "unit_cost_usd": 120, "weight_kg": 4, "hs_code": "700990"},
    {"id": "wd4", "name": "Industrial Metal Wall Art",    "style": ["industrial"],                         "origin_country": "China",   "unit_cost_usd": 95,  "weight_kg": 3, "hs_code": "830240"},
    {"id": "wd5", "name": "Gallery Wall Frame Set (5pc)", "style": ["modern", "scandinavian", "boho"],     "origin_country": "China",   "unit_cost_usd": 60,  "weight_kg": 2, "hs_code": "442190"},
    {"id": "wd6", "name": "Woven Tapestry",               "style": ["boho", "traditional"],               "origin_country": "India",   "unit_cost_usd": 70,  "weight_kg": 1, "hs_code": "580500"},
    {"id": "wd7", "name": "Brass Geometric Wall Panels",  "style": ["modern", "mid-century"],             "origin_country": "India",   "unit_cost_usd": 110, "weight_kg": 3, "hs_code": "830240"},
    {"id": "wd8", "name": "Floating Wood Shelves + Vases","style": ["scandinavian", "modern", "boho"],     "origin_country": "Vietnam", "unit_cost_usd": 90,  "weight_kg": 4, "hs_code": "940360"},
]


def get_recommendations(style: str, recommended_categories: list, max_per_category: int = 3) -> dict:
    style = style.lower().strip()
    result = {}

    for category in recommended_categories:
        matches = [p for p in PRODUCTS if p["category"].lower() == category.lower() and p["style"] == style]
        if not matches:
            matches = [p for p in PRODUCTS if p["category"].lower() == category.lower()]
        result[category] = matches[:max_per_category]

    return result


def get_all_by_style(style: str, max_per_category: int = 3) -> dict:
    """Return all categories for a given style — used for the browse-all view."""
    style = style.lower().strip()
    all_categories = sorted(set(p["category"] for p in PRODUCTS))
    result = {}
    for cat in all_categories:
        matches = [p for p in PRODUCTS if p["category"] == cat and p["style"] == style]
        if not matches:
            matches = [p for p in PRODUCTS if p["category"] == cat]
        result[cat] = matches[:max_per_category]
    return result


def get_wall_colors(mood: str) -> list:
    return WALL_COLORS.get(mood.lower(), WALL_COLORS["light"])


def get_wall_decor(style: str) -> list:
    style = style.lower().strip()
    matches = [d for d in WALL_DECOR if style in d["style"]]
    if not matches:
        matches = WALL_DECOR[:3]
    return matches
