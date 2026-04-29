import os
from supabase import create_client, Client
from catalog import get_recommendations, get_wall_colors, get_wall_decor

_client: Client | None = None


def _get_client() -> Client | None:
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if url and key:
            _client = create_client(url, key)
    return _client


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

        by_category = {}
        for category in categories:
            matches = [p for p in all_products if p["category"].lower() == category.lower()]
            if not matches:
                # fallback: any style for this category
                fallback = (
                    client.table("products")
                    .select("*")
                    .eq("category", category)
                    .limit(3)
                    .execute()
                )
                matches = fallback.data or []
            by_category[category] = matches[:3]

        # If Supabase returned nothing at all, fall back to hardcoded catalog
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
    # Wall colors are mood-based, not stored in Supabase — use catalog directly
    return get_wall_colors(mood)
