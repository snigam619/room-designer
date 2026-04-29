from typing import List

# Each product belongs to a category+style. Multiple products per category = alternatives to swap between.
PRODUCTS = [
    # ── SOFA ──────────────────────────────────────────────────────────────────
    {"id": 1,  "name": "Low-Profile Linen Sofa",       "category": "Sofa", "style": "modern",        "origin_country": "China",          "unit_cost_usd": 420,  "weight_kg": 48, "hs_code": "940161"},
    {"id": 2,  "name": "Velvet Channel Sofa",           "category": "Sofa", "style": "modern",        "origin_country": "Vietnam",        "unit_cost_usd": 580,  "weight_kg": 52, "hs_code": "940161"},
    {"id": 3,  "name": "Chesterfield Leather Sofa",    "category": "Sofa", "style": "traditional",   "origin_country": "United Kingdom", "unit_cost_usd": 1100, "weight_kg": 65, "hs_code": "940161"},
    {"id": 4,  "name": "Rattan & Cushion Sofa",        "category": "Sofa", "style": "boho",          "origin_country": "Indonesia",      "unit_cost_usd": 490,  "weight_kg": 40, "hs_code": "940150"},
    {"id": 5,  "name": "Tufted Wingback Sofa",         "category": "Sofa", "style": "mid-century",   "origin_country": "China",          "unit_cost_usd": 650,  "weight_kg": 55, "hs_code": "940161"},
    {"id": 6,  "name": "Slim Oak-Leg Sofa",            "category": "Sofa", "style": "scandinavian",  "origin_country": "Poland",         "unit_cost_usd": 520,  "weight_kg": 45, "hs_code": "940161"},
    {"id": 7,  "name": "Metal Frame Industrial Sofa",  "category": "Sofa", "style": "industrial",    "origin_country": "China",          "unit_cost_usd": 460,  "weight_kg": 50, "hs_code": "940161"},

    # ── COFFEE TABLE ──────────────────────────────────────────────────────────
    {"id": 8,  "name": "Walnut Slab Coffee Table",     "category": "Coffee Table", "style": "modern",       "origin_country": "Vietnam",   "unit_cost_usd": 180, "weight_kg": 18, "hs_code": "940360"},
    {"id": 9,  "name": "Marble Top Coffee Table",      "category": "Coffee Table", "style": "modern",       "origin_country": "Italy",     "unit_cost_usd": 320, "weight_kg": 30, "hs_code": "940360"},
    {"id": 10, "name": "Hairpin Leg Coffee Table",     "category": "Coffee Table", "style": "mid-century",  "origin_country": "Vietnam",   "unit_cost_usd": 160, "weight_kg": 14, "hs_code": "940360"},
    {"id": 11, "name": "Rattan Woven Coffee Table",    "category": "Coffee Table", "style": "boho",         "origin_country": "Indonesia", "unit_cost_usd": 140, "weight_kg": 10, "hs_code": "940150"},
    {"id": 12, "name": "Reclaimed Wood Coffee Table",  "category": "Coffee Table", "style": "industrial",   "origin_country": "Vietnam",   "unit_cost_usd": 210, "weight_kg": 22, "hs_code": "940360"},
    {"id": 13, "name": "White Lacquer Coffee Table",   "category": "Coffee Table", "style": "scandinavian", "origin_country": "Poland",    "unit_cost_usd": 195, "weight_kg": 16, "hs_code": "940360"},

    # ── ACCENT CHAIR ─────────────────────────────────────────────────────────
    {"id": 14, "name": "Egg Accent Chair",             "category": "Accent Chair", "style": "mid-century",  "origin_country": "China",     "unit_cost_usd": 310, "weight_kg": 18, "hs_code": "940171"},
    {"id": 15, "name": "Boucle Accent Chair",          "category": "Accent Chair", "style": "modern",       "origin_country": "China",     "unit_cost_usd": 280, "weight_kg": 16, "hs_code": "940171"},
    {"id": 16, "name": "Rattan Lounge Chair",          "category": "Accent Chair", "style": "boho",         "origin_country": "Indonesia", "unit_cost_usd": 275, "weight_kg": 12, "hs_code": "940150"},
    {"id": 17, "name": "Wingback Armchair",            "category": "Accent Chair", "style": "traditional",  "origin_country": "China",     "unit_cost_usd": 480, "weight_kg": 28, "hs_code": "940161"},
    {"id": 18, "name": "Leather Sling Chair",          "category": "Accent Chair", "style": "industrial",   "origin_country": "China",     "unit_cost_usd": 320, "weight_kg": 15, "hs_code": "940171"},
    {"id": 19, "name": "Sheepskin Accent Chair",       "category": "Accent Chair", "style": "scandinavian", "origin_country": "Poland",    "unit_cost_usd": 350, "weight_kg": 14, "hs_code": "940171"},

    # ── FLOOR LAMP ────────────────────────────────────────────────────────────
    {"id": 20, "name": "Arc Brass Floor Lamp",         "category": "Floor Lamp", "style": "modern",       "origin_country": "China",     "unit_cost_usd": 120, "weight_kg": 6,  "hs_code": "940510"},
    {"id": 21, "name": "Tripod Walnut Floor Lamp",     "category": "Floor Lamp", "style": "mid-century",  "origin_country": "China",     "unit_cost_usd": 110, "weight_kg": 4,  "hs_code": "940510"},
    {"id": 22, "name": "Rattan Woven Floor Lamp",      "category": "Floor Lamp", "style": "boho",         "origin_country": "Indonesia", "unit_cost_usd": 95,  "weight_kg": 3,  "hs_code": "940510"},
    {"id": 23, "name": "Industrial Pipe Floor Lamp",   "category": "Floor Lamp", "style": "industrial",   "origin_country": "China",     "unit_cost_usd": 85,  "weight_kg": 5,  "hs_code": "940510"},
    {"id": 24, "name": "Slim White Floor Lamp",        "category": "Floor Lamp", "style": "scandinavian", "origin_country": "China",     "unit_cost_usd": 75,  "weight_kg": 3,  "hs_code": "940510"},

    # ── AREA RUG ──────────────────────────────────────────────────────────────
    {"id": 25, "name": "Abstract Wool Rug 5x8",        "category": "Area Rug", "style": "modern",       "origin_country": "India",   "unit_cost_usd": 130, "weight_kg": 8,  "hs_code": "570110"},
    {"id": 26, "name": "Persian-Style Rug 8x10",       "category": "Area Rug", "style": "traditional",  "origin_country": "Turkey",  "unit_cost_usd": 320, "weight_kg": 14, "hs_code": "570110"},
    {"id": 27, "name": "Woven Jute Rug 6x9",           "category": "Area Rug", "style": "boho",         "origin_country": "India",   "unit_cost_usd": 110, "weight_kg": 9,  "hs_code": "570390"},
    {"id": 28, "name": "Flatweave Geometric Rug",      "category": "Area Rug", "style": "scandinavian", "origin_country": "India",   "unit_cost_usd": 150, "weight_kg": 7,  "hs_code": "570110"},
    {"id": 29, "name": "Cowhide Patchwork Rug",        "category": "Area Rug", "style": "industrial",   "origin_country": "Brazil",  "unit_cost_usd": 260, "weight_kg": 10, "hs_code": "570110"},

    # ── BOOKSHELF / STORAGE ───────────────────────────────────────────────────
    {"id": 30, "name": "Minimalist Floating Shelf",    "category": "Bookshelf", "style": "modern",       "origin_country": "Vietnam", "unit_cost_usd": 120, "weight_kg": 8,  "hs_code": "940360"},
    {"id": 31, "name": "Pipe & Wood Shelf Unit",       "category": "Bookshelf", "style": "industrial",   "origin_country": "China",   "unit_cost_usd": 160, "weight_kg": 20, "hs_code": "940360"},
    {"id": 32, "name": "Rattan Storage Shelves",       "category": "Bookshelf", "style": "boho",         "origin_country": "Indonesia","unit_cost_usd": 180, "weight_kg": 15, "hs_code": "940150"},
    {"id": 33, "name": "Solid Oak Bookcase",           "category": "Bookshelf", "style": "scandinavian", "origin_country": "Poland",  "unit_cost_usd": 320, "weight_kg": 35, "hs_code": "940360"},

    # ── SIDE TABLE ────────────────────────────────────────────────────────────
    {"id": 34, "name": "Marble & Gold Side Table",     "category": "Side Table", "style": "modern",       "origin_country": "China",     "unit_cost_usd": 95,  "weight_kg": 6, "hs_code": "940360"},
    {"id": 35, "name": "Drum Rattan Side Table",       "category": "Side Table", "style": "boho",         "origin_country": "Indonesia", "unit_cost_usd": 75,  "weight_kg": 4, "hs_code": "940150"},
    {"id": 36, "name": "Hairpin Leg Side Table",       "category": "Side Table", "style": "mid-century",  "origin_country": "Vietnam",   "unit_cost_usd": 85,  "weight_kg": 5, "hs_code": "940360"},
    {"id": 37, "name": "Reclaimed Wood Side Table",    "category": "Side Table", "style": "industrial",   "origin_country": "Vietnam",   "unit_cost_usd": 90,  "weight_kg": 7, "hs_code": "940360"},
]

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
        # Find products matching this category + style
        matches = [p for p in PRODUCTS if p["category"].lower() == category.lower() and p["style"] == style]
        # Fallback: any product in this category regardless of style
        if not matches:
            matches = [p for p in PRODUCTS if p["category"].lower() == category.lower()]
        result[category] = matches[:max_per_category]

    return result


def get_wall_colors(mood: str) -> list:
    return WALL_COLORS.get(mood.lower(), WALL_COLORS["light"])


def get_wall_decor(style: str) -> list:
    style = style.lower().strip()
    matches = [d for d in WALL_DECOR if style in d["style"]]
    if not matches:
        matches = WALL_DECOR[:3]
    return matches
