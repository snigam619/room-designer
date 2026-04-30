import os
from typing import Optional
from supabase import create_client, Client
from catalog import get_recommendations, get_wall_colors, get_wall_decor, get_all_by_style

_client: Optional[Client] = None


def _get_client() -> Optional[Client]:
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if url and key:
            _client = create_client(url, key)
    return _client


def _inject_brands(supabase_products: list, catalog_products: list) -> list:
    """Backfill brand and product_url from catalog by product id."""
    catalog_by_id = {p["id"]: p for p in catalog_products}
    for p in supabase_products:
        cat = catalog_by_id.get(p["id"], {})
        if not p.get("brand"):
            p["brand"] = cat.get("brand", "")
        if not p.get("product_url"):
            p["product_url"] = cat.get("product_url", "")
    return supabase_products


def get_products_by_style_and_categories(style: str, categories: list) -> dict:
    client = _get_client()
    if client is None:
        return get_recommendations(style, categories)

    try:
        result = (
            client.table("products")
            .select("*")
            .eq("style", style.lower())
            .execute()
        )
        all_products = result.data or []

        # Import catalog for brand backfill
        from catalog import PRODUCTS as catalog_all
        _inject_brands(all_products, catalog_all)

        by_category = {}
        for category in categories:
            matches = [p for p in all_products if p["category"].lower() == category.lower()]
            if not matches:
                fallback = (
                    client.table("products")
                    .select("*")
                    .eq("category", category)
                    .limit(3)
                    .execute()
                )
                matches = fallback.data or []
                _inject_brands(matches, catalog_all)
            by_category[category] = matches[:3]

        if not any(by_category.values()):
            return get_recommendations(style, categories)

        return by_category

    except Exception:
        return get_recommendations(style, categories)


def get_wall_decor_by_style(style: str) -> list:
    client = _get_client()
    if client is None:
        return get_wall_decor(style)

    try:
        result = (
            client.table("wall_decor")
            .select("*")
            .contains("styles", [style.lower()])
            .execute()
        )
        items = result.data or []
        if not items:
            result = client.table("wall_decor").select("*").limit(4).execute()
            items = result.data or []
        return items if items else get_wall_decor(style)

    except Exception:
        return get_wall_decor(style)


def get_wall_colors_for_mood(mood: str) -> list:
    return get_wall_colors(mood)


def get_all_products_by_style(style: str) -> dict:
    """Return all categories for a style — used for the browse-all category filter."""
    client = _get_client()
    if client is None:
        return get_all_by_style(style)

    try:
        result = (
            client.table("products")
            .select("*")
            .eq("style", style.lower())
            .execute()
        )
        all_products = result.data or []
        if not all_products:
            return get_all_by_style(style)

        from catalog import PRODUCTS as catalog_all
        _inject_brands(all_products, catalog_all)

        by_category = {}
        for p in all_products:
            cat = p["category"]
            by_category.setdefault(cat, [])
            if len(by_category[cat]) < 3:
                by_category[cat].append(p)

        return by_category

    except Exception:
        return get_all_by_style(style)
