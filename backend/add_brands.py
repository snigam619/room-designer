"""
Migration script: add `brand` column to the Supabase `products` table and
populate it with deterministic, realistic furniture brand names.

Usage:
    python3 backend/add_brands.py

Requires SUPABASE_URL and SUPABASE_ANON_KEY in
    /Users/snigam/Library/CloudStorage/OneDrive-RoomsToGo/Desktop/jira-workspace/room-designer/.env
or already set in the environment.
"""

import os
import sys
from pathlib import Path

# ── Load .env ─────────────────────────────────────────────────────────────────
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

# ── Brand mappings ────────────────────────────────────────────────────────────
BRANDS = {
    "modern":       ["West Elm", "CB2", "Article", "Blu Dot", "Muuto"],
    "scandinavian": ["IKEA", "Hay", "Muuto", "Menu", "String"],
    "mid-century":  ["Herman Miller", "Design Within Reach", "Article", "Kardiel", "Joybird"],
    "boho":         ["World Market", "Anthropologie", "Serena & Lily", "Arhaus", "Jungalow"],
    "industrial":   ["Restoration Hardware", "West Elm", "CB2", "Pottery Barn", "Wayfair"],
    "traditional":  ["Ethan Allen", "Pottery Barn", "Restoration Hardware", "Arhaus", "Bassett"],
}

CATEGORY_BRANDS = {
    "Sofa":         ["Pottery Barn", "West Elm", "Crate & Barrel", "Article", "Joybird", "Burrow"],
    "Coffee Table": ["CB2", "West Elm", "Article", "IKEA", "Blu Dot"],
    "Accent Chair": ["Article", "Anthropologie", "CB2", "West Elm", "Joybird"],
    "Floor Lamp":   ["CB2", "West Elm", "Rejuvenation", "Schoolhouse", "Arteriors"],
    "Area Rug":     ["Ruggable", "Loloi", "Dash & Albert", "Surya", "Nourison"],
    "Bookshelf":    ["West Elm", "IKEA", "CB2", "Crate & Barrel", "Article"],
    "Side Table":   ["CB2", "West Elm", "Article", "IKEA", "Blu Dot"],
    "Bed":          ["Purple", "Saatva", "Pottery Barn", "West Elm", "Restoration Hardware"],
    "Dining Table": ["Restoration Hardware", "Pottery Barn", "West Elm", "CB2", "Arhaus"],
    "Dresser":      ["West Elm", "Pottery Barn", "IKEA", "Article", "CB2"],
}


def pick_brand(product_id: int, category: str, style: str) -> str:
    """Return a stable brand name for the given product."""
    if category in CATEGORY_BRANDS:
        brands = CATEGORY_BRANDS[category]
    else:
        brands = BRANDS.get(style, list(BRANDS["modern"]))
    return brands[product_id % len(brands)]


# ── Supabase connection ───────────────────────────────────────────────────────
def get_client():
    try:
        from supabase import create_client
    except ImportError:
        sys.exit("supabase-py is not installed. Run: pip3 install supabase")

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        sys.exit(
            "SUPABASE_URL and/or SUPABASE_ANON_KEY are not set.\n"
            "Make sure they exist in your .env file or environment."
        )
    return create_client(url, key)


def add_brand_column(client) -> None:
    """
    Attempt to add the `brand` column via a raw SQL RPC call.

    This requires a Postgres function called `exec_sql` (or similar) exposed
    through Supabase RPC, OR a Supabase service-role key with DDL rights.

    If the RPC is not available (common with anon keys), the column must be
    added manually in the Supabase dashboard:
        ALTER TABLE products ADD COLUMN IF NOT EXISTS brand TEXT;

    The UPDATE step below will still succeed as long as the column exists.
    """
    sql = "ALTER TABLE products ADD COLUMN IF NOT EXISTS brand TEXT;"
    try:
        client.rpc("exec_sql", {"query": sql}).execute()
        print("ALTER TABLE succeeded via RPC.")
    except Exception as exc:
        print(
            f"[INFO] Could not add column via RPC ({exc}).\n"
            "       If the column does not already exist, add it manually:\n"
            "           ALTER TABLE products ADD COLUMN IF NOT EXISTS brand TEXT;\n"
            "       Continuing with UPDATE step…"
        )


def populate_brands(client) -> None:
    """Fetch every product and update its brand field deterministically."""
    print("Fetching all products…")
    result = client.table("products").select("id, category, style").execute()
    products = result.data or []

    if not products:
        print("[WARN] No products found in the table. Nothing to update.")
        return

    print(f"Found {len(products)} products. Updating brand values…")
    updated = 0
    errors = 0

    for p in products:
        product_id = p["id"]
        category   = p.get("category", "")
        style      = p.get("style", "modern")
        brand      = pick_brand(product_id, category, style)

        try:
            client.table("products").update({"brand": brand}).eq("id", product_id).execute()
            print(f"  id={product_id:>4}  category={category:<15}  style={style:<14}  → {brand}")
            updated += 1
        except Exception as exc:
            print(f"  [ERROR] id={product_id}: {exc}")
            errors += 1

    print(f"\nDone. {updated} rows updated, {errors} errors.")


def main() -> None:
    client = get_client()
    add_brand_column(client)
    populate_brands(client)


if __name__ == "__main__":
    main()
