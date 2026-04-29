"""
One-time script to seed Supabase with all products from catalog.py.
Run once: python3 seed_supabase.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from supabase import create_client
from catalog import PRODUCTS, WALL_DECOR

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    print("ERROR: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")
    exit(1)

client = create_client(url, key)

print("Seeding products table...")
for product in PRODUCTS:
    row = {
        "name": product["name"],
        "category": product["category"],
        "style": product["style"],
        "origin_country": product["origin_country"],
        "unit_cost_usd": product["unit_cost_usd"],
        "weight_kg": product["weight_kg"],
        "hs_code": product["hs_code"],
        "image_url": None,
    }
    result = client.table("products").insert(row).execute()
    print(f"  ✓ {product['name']}")

print("\nSeeding wall_decor table...")
for item in WALL_DECOR:
    row = {
        "name": item["name"],
        "styles": item["style"],
        "origin_country": item["origin_country"],
        "unit_cost_usd": item["unit_cost_usd"],
        "weight_kg": item["weight_kg"],
        "hs_code": item["hs_code"],
        "image_url": None,
    }
    result = client.table("wall_decor").insert(row).execute()
    print(f"  ✓ {item['name']}")

print(f"\nDone! Seeded {len(PRODUCTS)} products and {len(WALL_DECOR)} wall decor items.")
print("Go to your Supabase dashboard → Table Editor to verify.")
