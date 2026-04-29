from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent.parent / ".env")

from vision import analyze_room
from catalog import get_recommendations
from sourcing import price_products

app = FastAPI(title="AI Room Designer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze-room")
async def analyze_room_endpoint(image: UploadFile = File(...)):
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WebP, or GIF images are accepted.")

    image_bytes = await image.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image must be under 10 MB.")

    try:
        room_data = analyze_room(image_bytes, media_type=image.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Room analysis failed: {str(e)}")

    raw_products = get_recommendations(
        style=room_data.get("detected_style", "modern"),
        missing_items=room_data.get("missing_items", []),
    )
    priced_products = price_products(raw_products)

    total_landed_cost = round(sum(p["landed_cost_usd"] for p in priced_products), 2)

    return {
        **room_data,
        "recommendations": priced_products,
        "total_landed_cost_usd": total_landed_cost,
    }
