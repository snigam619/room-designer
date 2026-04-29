from typing import List

PRODUCTS = [
    # --- MODERN ---
    {"id": 1, "name": "Low-Profile Sofa", "category": "Sofa", "style": "modern", "origin_country": "China", "unit_cost_usd": 420, "weight_kg": 48, "hs_code": "940161"},
    {"id": 2, "name": "Walnut Coffee Table", "category": "Coffee Table", "style": "modern", "origin_country": "Vietnam", "unit_cost_usd": 180, "weight_kg": 18, "hs_code": "940360"},
    {"id": 3, "name": "Geometric Floor Lamp", "category": "Floor Lamp", "style": "modern", "origin_country": "China", "unit_cost_usd": 95, "weight_kg": 5, "hs_code": "940510"},
    {"id": 4, "name": "Minimalist Bookshelf", "category": "Bookshelf", "style": "modern", "origin_country": "Vietnam", "unit_cost_usd": 210, "weight_kg": 25, "hs_code": "940360"},
    {"id": 5, "name": "Abstract Area Rug 5x8", "category": "Area Rug", "style": "modern", "origin_country": "India", "unit_cost_usd": 130, "weight_kg": 8, "hs_code": "570110"},

    # --- MID-CENTURY ---
    {"id": 6, "name": "Walnut Credenza", "category": "Sideboard", "style": "mid-century", "origin_country": "Vietnam", "unit_cost_usd": 520, "weight_kg": 45, "hs_code": "940360"},
    {"id": 7, "name": "Tulip Dining Table", "category": "Dining Table", "style": "mid-century", "origin_country": "Italy", "unit_cost_usd": 680, "weight_kg": 35, "hs_code": "940360"},
    {"id": 8, "name": "Egg Accent Chair", "category": "Accent Chair", "style": "mid-century", "origin_country": "China", "unit_cost_usd": 310, "weight_kg": 18, "hs_code": "940171"},
    {"id": 9, "name": "Tripod Floor Lamp", "category": "Floor Lamp", "style": "mid-century", "origin_country": "China", "unit_cost_usd": 110, "weight_kg": 4, "hs_code": "940510"},
    {"id": 10, "name": "Sunburst Wall Clock", "category": "Wall Decor", "style": "mid-century", "origin_country": "Mexico", "unit_cost_usd": 65, "weight_kg": 2, "hs_code": "910590"},

    # --- BOHO ---
    {"id": 11, "name": "Rattan Pendant Light", "category": "Pendant Light", "style": "boho", "origin_country": "Indonesia", "unit_cost_usd": 85, "weight_kg": 3, "hs_code": "940590"},
    {"id": 12, "name": "Macrame Wall Hanging", "category": "Wall Decor", "style": "boho", "origin_country": "India", "unit_cost_usd": 45, "weight_kg": 1, "hs_code": "630790"},
    {"id": 13, "name": "Woven Jute Rug 6x9", "category": "Area Rug", "style": "boho", "origin_country": "India", "unit_cost_usd": 110, "weight_kg": 9, "hs_code": "570390"},
    {"id": 14, "name": "Rattan Lounge Chair", "category": "Accent Chair", "style": "boho", "origin_country": "Indonesia", "unit_cost_usd": 275, "weight_kg": 12, "hs_code": "940150"},
    {"id": 15, "name": "Terracotta Plant Pots Set", "category": "Decor", "style": "boho", "origin_country": "Mexico", "unit_cost_usd": 40, "weight_kg": 4, "hs_code": "690910"},

    # --- SCANDINAVIAN ---
    {"id": 16, "name": "Oak Dining Chairs (Set of 2)", "category": "Dining Chair", "style": "scandinavian", "origin_country": "Poland", "unit_cost_usd": 290, "weight_kg": 14, "hs_code": "940161"},
    {"id": 17, "name": "Sheepskin Throw Blanket", "category": "Throw", "style": "scandinavian", "origin_country": "New Zealand", "unit_cost_usd": 75, "weight_kg": 1, "hs_code": "630120"},
    {"id": 18, "name": "Solid Pine Bed Frame", "category": "Bed Frame", "style": "scandinavian", "origin_country": "Poland", "unit_cost_usd": 450, "weight_kg": 55, "hs_code": "940390"},
    {"id": 19, "name": "White Linen Curtains", "category": "Curtains", "style": "scandinavian", "origin_country": "Portugal", "unit_cost_usd": 90, "weight_kg": 2, "hs_code": "630391"},
    {"id": 20, "name": "Minimalist Desk Lamp", "category": "Desk Lamp", "style": "scandinavian", "origin_country": "China", "unit_cost_usd": 55, "weight_kg": 2, "hs_code": "940520"},

    # --- INDUSTRIAL ---
    {"id": 21, "name": "Metal & Wood Dining Table", "category": "Dining Table", "style": "industrial", "origin_country": "China", "unit_cost_usd": 390, "weight_kg": 42, "hs_code": "940360"},
    {"id": 22, "name": "Pipe Shelf Unit", "category": "Bookshelf", "style": "industrial", "origin_country": "China", "unit_cost_usd": 160, "weight_kg": 20, "hs_code": "940360"},
    {"id": 23, "name": "Edison Bulb Pendant", "category": "Pendant Light", "style": "industrial", "origin_country": "China", "unit_cost_usd": 70, "weight_kg": 2, "hs_code": "940590"},
    {"id": 24, "name": "Leather Bar Stools (Set of 2)", "category": "Bar Stool", "style": "industrial", "origin_country": "China", "unit_cost_usd": 220, "weight_kg": 16, "hs_code": "940171"},
    {"id": 25, "name": "Reclaimed Wood Console Table", "category": "Console Table", "style": "industrial", "origin_country": "Vietnam", "unit_cost_usd": 295, "weight_kg": 22, "hs_code": "940360"},

    # --- TRADITIONAL ---
    {"id": 26, "name": "Chesterfield Sofa", "category": "Sofa", "style": "traditional", "origin_country": "United Kingdom", "unit_cost_usd": 1100, "weight_kg": 65, "hs_code": "940161"},
    {"id": 27, "name": "Persian-Style Area Rug 8x10", "category": "Area Rug", "style": "traditional", "origin_country": "Turkey", "unit_cost_usd": 320, "weight_kg": 14, "hs_code": "570110"},
    {"id": 28, "name": "Brass Table Lamp", "category": "Table Lamp", "style": "traditional", "origin_country": "India", "unit_cost_usd": 95, "weight_kg": 3, "hs_code": "940520"},
    {"id": 29, "name": "Wingback Armchair", "category": "Armchair", "style": "traditional", "origin_country": "China", "unit_cost_usd": 480, "weight_kg": 28, "hs_code": "940161"},
    {"id": 30, "name": "Dark Wood Buffet Cabinet", "category": "Buffet", "style": "traditional", "origin_country": "Malaysia", "unit_cost_usd": 560, "weight_kg": 50, "hs_code": "940360"},
]


def get_recommendations(style: str, missing_items: List[str], max_results: int = 6) -> List[dict]:
    style = style.lower().strip()
    style_matches = [p for p in PRODUCTS if p["style"] == style]

    if not style_matches:
        style_matches = PRODUCTS  # fallback: return anything

    # Prefer products whose category overlaps with missing_items keywords
    scored = []
    for product in style_matches:
        score = 0
        for missing in missing_items:
            missing_lower = missing.lower()
            if any(word in product["name"].lower() or word in product["category"].lower()
                   for word in missing_lower.split()):
                score += 1
        scored.append((score, product))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:max_results]]
