from typing import List

# Duty rates by HS chapter + origin country (simplified)
# Key: (hs_chapter, origin_country) → duty rate as decimal
DUTY_RATES = {
    # Furniture (HS chapter 94)
    ("94", "China"): 0.25,
    ("94", "Vietnam"): 0.00,
    ("94", "India"): 0.00,
    ("94", "Indonesia"): 0.00,
    ("94", "Mexico"): 0.00,
    ("94", "Poland"): 0.00,
    ("94", "Portugal"): 0.00,
    ("94", "Italy"): 0.00,
    ("94", "Malaysia"): 0.03,
    ("94", "United Kingdom"): 0.00,
    ("94", "New Zealand"): 0.00,
    ("94", "Turkey"): 0.05,
    # Textiles / rugs (HS chapter 57, 63)
    ("57", "China"): 0.25,
    ("57", "India"): 0.07,
    ("57", "Turkey"): 0.07,
    ("63", "China"): 0.12,
    ("63", "India"): 0.10,
    ("63", "Portugal"): 0.00,
    ("63", "New Zealand"): 0.00,
    # Clocks / instruments (HS chapter 91)
    ("91", "China"): 0.04,
    ("91", "Mexico"): 0.00,
    # Default fallback
    ("default", "China"): 0.15,
    ("default", "default"): 0.03,
}

# Freight cost in USD per kg by origin country
FREIGHT_PER_KG = {
    "China": 2.50,
    "Vietnam": 3.00,
    "India": 3.20,
    "Indonesia": 3.50,
    "Mexico": 1.80,
    "Poland": 4.00,
    "Portugal": 4.50,
    "Italy": 4.50,
    "Malaysia": 3.20,
    "United Kingdom": 4.80,
    "New Zealand": 5.50,
    "Turkey": 3.80,
    "default": 4.00,
}


def _get_duty_rate(hs_code: str, origin: str) -> float:
    chapter = hs_code[:2]
    rate = DUTY_RATES.get((chapter, origin))
    if rate is None:
        rate = DUTY_RATES.get(("default", origin))
    if rate is None:
        rate = DUTY_RATES.get(("default", "default"), 0.03)
    return rate


def calculate_landed_cost(product: dict) -> dict:
    origin = product["origin_country"]
    unit_cost = product["unit_cost_usd"]
    weight_kg = product["weight_kg"]
    hs_code = product["hs_code"]

    duty_rate = _get_duty_rate(hs_code, origin)
    freight_per_kg = FREIGHT_PER_KG.get(origin, FREIGHT_PER_KG["default"])

    duty_amount = round(unit_cost * duty_rate, 2)
    freight_amount = round(weight_kg * freight_per_kg, 2)
    landed_cost = round(unit_cost + duty_amount + freight_amount, 2)

    return {
        **product,
        "duty_rate_pct": round(duty_rate * 100, 1),
        "duty_amount_usd": duty_amount,
        "freight_usd": freight_amount,
        "landed_cost_usd": landed_cost,
    }


def price_products(products: List[dict]) -> List[dict]:
    return [calculate_landed_cost(p) for p in products]
