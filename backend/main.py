from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from typing import List

load_dotenv(Path(__file__).parent.parent / ".env")

from vision import analyze_room
from db import get_products_by_style_and_categories, get_wall_colors_for_mood, get_all_products_by_style
from sourcing import price_products
from image_gen import generate_room_render, _build_prompt

app = FastAPI(title="AI Room Designer", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


class RenderRequest(BaseModel):
    style: str
    wall_color_name: str
    wall_color_hex: str = ""
    room_type: str
    selected_products: List[str]
    accent_color_name: str = ""
    design_summary: str = ""
    custom_prompt: str = ""  # optional override


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-render")
async def generate_render(req: RenderRequest):
    # Use custom prompt if provided, otherwise build from params
    prompt = req.custom_prompt.strip() if req.custom_prompt.strip() else None
    image_data = generate_room_render(
        style=req.style,
        wall_color_name=req.wall_color_name,
        room_type=req.room_type,
        selected_products=req.selected_products,
        accent_color_name=req.accent_color_name,
        design_summary=req.design_summary,
        custom_prompt=prompt,
        wall_color_hex=req.wall_color_hex,
    )
    if image_data is None:
        raise HTTPException(status_code=503, detail="Image generation unavailable. Check HF_API_TOKEN or try again.")
    used_prompt = prompt or _build_prompt(
        req.style, req.wall_color_name, req.room_type, req.selected_products,
        accent_color=req.accent_color_name,
        wall_color_hex=req.wall_color_hex,
    )
    return {"image_data": image_data, "prompt_used": used_prompt}


@app.get("/all-products")
def all_products(style: str = "modern"):
    """Return every product category for a given style — used by the category filter bar."""
    raw = get_all_products_by_style(style)
    priced = {cat: price_products(products) for cat, products in raw.items() if products}
    return {"products_by_category": priced}


@app.post("/design-room")
async def design_room(
    image: UploadFile = File(...),
    style: str = Form(default="modern"),
    mood: str = Form(default="light"),
    budget: str = Form(default="1000"),
):
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, or WebP images are accepted.")

    image_bytes = await image.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image must be under 10 MB.")

    try:
        room_data = analyze_room(image_bytes, media_type=image.content_type,
                                 style=style, mood=mood, budget=budget)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Room analysis failed: {str(e)}")

    # Get product alternatives per recommended category (from Supabase, falls back to catalog)
    VALID_CATEGORIES = ["Sofa", "Coffee Table", "Accent Chair", "Floor Lamp", "Area Rug",
                        "Bookshelf", "Side Table", "Bed", "Dining Table", "Dresser"]
    raw_categories = room_data.get("recommended_products", [])
    # Filter to only recognized categories; fall back to default 4 if Claude returned nothing valid
    filtered_categories = [c for c in raw_categories if c in VALID_CATEGORIES]
    if not filtered_categories:
        filtered_categories = ["Sofa", "Coffee Table", "Accent Chair", "Floor Lamp"]

    raw_by_category = get_products_by_style_and_categories(
        style=style,
        categories=filtered_categories,
    )

    # Price every product in every category
    priced_by_category = {
        cat: price_products(products)
        for cat, products in raw_by_category.items()
        if products  # skip empty categories
    }

    # Enforce total budget ± 100: sort each category cheapest-first, then
    # greedily pick the cheapest combo that fits within budget+100.
    budget_int = int(budget) if str(budget).isdigit() else 1000
    budget_ceiling = budget_int + 100

    # Sort each category by price ascending
    for cat in priced_by_category:
        priced_by_category[cat].sort(key=lambda p: p["landed_cost_usd"])

    # Greedy: keep adding cheapest-per-category while total stays under ceiling
    selected_cats = list(priced_by_category.keys())
    min_total = sum(priced_by_category[c][0]["landed_cost_usd"] for c in selected_cats if priced_by_category[c])

    # If even the cheapest combo exceeds budget, drop the most expensive category
    while min_total > budget_ceiling and len(selected_cats) > 1:
        # Find which category contributes most to the overage and drop it
        selected_cats.sort(key=lambda c: priced_by_category[c][0]["landed_cost_usd"])
        selected_cats.pop()  # drop highest-cost category
        min_total = sum(priced_by_category[c][0]["landed_cost_usd"] for c in selected_cats if priced_by_category[c])

    priced_by_category = {c: priced_by_category[c] for c in selected_cats}

    # Wall color options based on mood
    wall_colors = get_wall_colors_for_mood(mood)

    # Default selected index 0 for each category (now budget-sorted)
    selected_products = {
        cat: products[0] if products else None
        for cat, products in priced_by_category.items()
    }

    total_landed_cost = round(
        sum(p["landed_cost_usd"] for p in selected_products.values() if p),
        2,
    )

    return {
        "room_type": room_data.get("room_type"),
        "design_summary": room_data.get("design_summary"),
        "wall_color": room_data.get("wall_color"),
        "accent_color": room_data.get("accent_color"),
        "wall_color_options": wall_colors,
        "products_by_category": priced_by_category,
        "total_landed_cost_usd": total_landed_cost,
        "accent_color_hex": room_data.get("accent_color", {}).get("hex", ""),
    }
