from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from typing import List

load_dotenv(Path(__file__).parent.parent / ".env")

from vision import analyze_room
from db import get_products_by_style_and_categories, get_wall_decor_by_style, get_wall_colors_for_mood
from sourcing import price_products
from image_gen import generate_room_render

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
    room_type: str
    selected_products: List[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-render")
async def generate_render(req: RenderRequest):
    image_data = generate_room_render(
        style=req.style,
        wall_color_name=req.wall_color_name,
        room_type=req.room_type,
        selected_products=req.selected_products,
    )
    if image_data is None:
        raise HTTPException(status_code=503, detail="Image generation unavailable. Check HF_API_TOKEN or try again.")
    return {"image_data": image_data}


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
    raw_by_category = get_products_by_style_and_categories(
        style=style,
        categories=room_data.get("recommended_products", []),
    )

    # Price every product in every category
    priced_by_category = {
        cat: price_products(products)
        for cat, products in raw_by_category.items()
    }

    # Wall color options based on mood
    wall_colors = get_wall_colors_for_mood(mood)

    # Wall decor options based on style (from Supabase, falls back to catalog)
    wall_decor_options = price_products(get_wall_decor_by_style(style))

    # Default selected index 0 for each category
    selected_products = {
        cat: products[0] if products else None
        for cat, products in priced_by_category.items()
    }

    total_landed_cost = round(
        sum(p["landed_cost_usd"] for p in selected_products.values() if p) +
        (wall_decor_options[0]["landed_cost_usd"] if wall_decor_options else 0),
        2,
    )

    return {
        "room_type": room_data.get("room_type"),
        "design_summary": room_data.get("design_summary"),
        "wall_color": room_data.get("wall_color"),
        "accent_color": room_data.get("accent_color"),
        "wall_color_options": wall_colors,
        "wall_decor_options": wall_decor_options,
        "products_by_category": priced_by_category,
        "total_landed_cost_usd": total_landed_cost,
    }
