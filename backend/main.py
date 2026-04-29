from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent.parent / ".env")

from vision import analyze_room

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
    if len(image_bytes) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=400, detail="Image must be under 10 MB.")

    try:
        room_data = analyze_room(image_bytes, media_type=image.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Room analysis failed: {str(e)}")

    return room_data
