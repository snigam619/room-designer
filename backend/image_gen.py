import os
import requests
import base64
import time
import urllib.parse
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

STYLE_KEYWORDS = {
    "modern":       "clean lines, minimalist, contemporary, neutral tones, sleek surfaces",
    "mid-century":  "organic shapes, tapered legs, warm walnut wood tones, retro 1960s feel",
    "boho":         "layered textures, macrame, rattan, woven natural fibers, plants, eclectic",
    "scandinavian": "hygge warmth, white walls, light birch wood, cozy textiles, functional simplicity",
    "industrial":   "exposed brick, black metal frames, reclaimed wood, raw materials, Edison bulbs",
    "traditional":  "classic elegance, rich upholstery, ornate details, symmetry, warm wood tones",
}

# Map product name keywords to visual descriptors for the prompt
PRODUCT_VISUALS = {
    "sofa":          "a large sofa centered against the back wall",
    "bed":           "a bed with headboard centered against the back wall",
    "dining table":  "a dining table centered in the room with chairs around it",
    "coffee table":  "a coffee table centered in front of the sofa on the rug",
    "accent chair":  "an accent chair to the left of the sofa",
    "floor lamp":    "a floor lamp standing in the right rear corner behind the sofa",
    "area rug":      "a large area rug anchoring the seating area in the center of the room",
    "bookshelf":     "a bookshelf against the right wall",
    "side table":    "a side table to the right of the sofa",
    "dresser":       "a dresser against the left wall",
}


def _build_prompt(style: str, wall_color: str, room_type: str, product_names: list,
                  accent_color: str = "", design_summary: str = "",
                  wall_color_hex: str = "") -> str:
    style_desc = STYLE_KEYWORDS.get(style.lower(), style)

    # Map each selected product name to a specific visual description
    furniture_parts = []
    for name in product_names[:8]:
        name_lower = name.lower()
        matched = False
        for keyword, visual in PRODUCT_VISUALS.items():
            if keyword in name_lower:
                furniture_parts.append(f"{visual} — specifically a '{name}'")
                matched = True
                break
        if not matched:
            furniture_parts.append(f"'{name}' prominently visible")

    furniture_str = ", ".join(furniture_parts) if furniture_parts else "sofa, coffee table, floor lamp"

    # Use hex for precise wall color
    color_desc = f"{wall_color} (hex {wall_color_hex})" if wall_color_hex else wall_color
    accent_part = f", {accent_color} accent decor" if accent_color else ""

    # Room layout anchor — matches the static base images in frontend/rooms/
    ROOM_LAYOUT = {
        "living room":  "spacious living room with hardwood floor, large sliding glass door on the left wall letting in bright natural light, one square window on the back wall, modern fireplace on the right wall, recessed ceiling lights, white baseboards, wide-angle view",
        "bedroom":      "rectangular bedroom with hardwood floor, large window on the left wall with natural light, doorway on the right wall, tray ceiling with recessed lights, white baseboards, wide-angle view",
        "dining room":  "dining room with hardwood floor, two windows on the right wall with natural light, arched doorway on the left, crown molding, pendant light hanging from ceiling, wide-angle view",
        "home office":  "home office with hardwood floor, window with natural light, white walls, recessed lights, wide-angle view",
    }
    layout = ROOM_LAYOUT.get(room_type.lower().strip(), ROOM_LAYOUT["living room"])

    return (
        f"Interior design photograph of a {style} style {room_type}. "
        f"Room layout: {layout}. "
        f"Walls painted {color_desc} — this exact color must cover all walls visibly. "
        f"{accent_part}. "
        f"Style: {style_desc}. "
        f"Furniture placed in the room: {furniture_str}. "
        f"Same wide-angle perspective, natural daylight from windows, "
        f"Architectural Digest quality, photorealistic, no people, no text. 8K."
    )


def generate_room_render(
    style: str,
    wall_color_name: str,
    room_type: str,
    selected_products: list,
    accent_color_name: str = "",
    design_summary: str = "",
    custom_prompt: Optional[str] = None,
    wall_color_hex: str = "",
    retries: int = 2,
) -> Optional[str]:
    prompt = custom_prompt if custom_prompt else _build_prompt(
        style, wall_color_name, room_type, selected_products,
        accent_color=accent_color_name, design_summary=design_summary,
        wall_color_hex=wall_color_hex,
    )

    # 1. HuggingFace FLUX.1-schnell — WORKING, free tier (primary)
    hf_token = os.getenv("HF_API_TOKEN")
    if hf_token:
        result = _try_hf(prompt, hf_token, retries)
        if result:
            return result

    # 2. Segmind — free 100 credits on signup
    segmind_key = os.getenv("SEGMIND_API_KEY")
    if segmind_key:
        result = _try_segmind(prompt, segmind_key)
        if result:
            return result

    # 3. Clipdrop — free 100 credits/day
    clipdrop_key = os.getenv("CLIPDROP_API_KEY")
    if clipdrop_key:
        result = _try_clipdrop(prompt, clipdrop_key)
        if result:
            return result

    # 4. Pollinations.AI — free, no key (blocked on company wifi, works on hotspot)
    result = _try_pollinations(prompt)
    if result:
        return result

    # 5. DALL-E 3 — best quality (needs funded OpenAI account)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        result = _try_dalle3(prompt, openai_key)
        if result:
            return result

    # 6. Stability AI
    stability_key = os.getenv("STABILITY_API_KEY")
    if stability_key:
        return _try_stability(prompt, stability_key)

    # 7. fal.ai
    fal_key = os.getenv("FAL_KEY")
    if fal_key:
        return _try_fal(prompt, fal_key)

    return None


def _try_segmind(prompt: str, api_key: str) -> Optional[str]:
    """Segmind — free 100 credits on signup, no credit card.
    Sign up at segmind.com → API Keys → copy key → add SEGMIND_API_KEY to .env
    """
    try:
        response = requests.post(
            "https://api.segmind.com/v1/flux-schnell",
            headers={"x-api-key": api_key, "Content-Type": "application/json"},
            json={
                "prompt": prompt,
                "steps": 4,
                "seed": int(time.time()) % 9999,
                "width": 1024,
                "height": 576,
                "base64": True,
            },
            timeout=60,
        )
        if response.status_code == 200:
            b64 = response.json().get("image", "")
            if b64:
                return f"data:image/jpeg;base64,{b64}"
        print(f"Segmind error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"Segmind error: {e}")
    return None


def _try_clipdrop(prompt: str, api_key: str) -> Optional[str]:
    """Clipdrop by Stability AI — free 100 credits/day, no credit card.
    Sign up at clipdrop.co/apis → copy key → add CLIPDROP_API_KEY to .env
    """
    try:
        response = requests.post(
            "https://clipdrop-api.co/text-to-image/v1",
            headers={"x-api-key": api_key},
            files={"prompt": (None, prompt[:500])},
            timeout=60,
        )
        if response.status_code == 200:
            b64 = base64.b64encode(response.content).decode()
            return f"data:image/jpeg;base64,{b64}"
        print(f"Clipdrop error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"Clipdrop error: {e}")
    return None


def _try_dalle3(prompt: str, api_key: str) -> Optional[str]:
    """DALL-E 3 via OpenAI — ~$0.04/image at 1024x1024 standard quality.
    You already have OPENAI_API_KEY in .env. 20-30 demo renders ≈ $0.80-$1.20 total.
    """
    try:
        client = OpenAI(api_key=api_key)
        # Truncate prompt to DALL-E's 4000 char limit
        safe_prompt = prompt[:3900]
        response = client.images.generate(
            model="dall-e-3",
            prompt=safe_prompt,
            size="1792x1024",
            quality="standard",
            n=1,
            response_format="b64_json",
        )
        b64 = response.data[0].b64_json
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"DALL-E 3 error: {e}")
    return None


def _try_stability(prompt: str, api_key: str) -> Optional[str]:
    try:
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={"authorization": f"Bearer {api_key}", "accept": "image/*"},
            files={"none": ""},
            data={"prompt": prompt, "output_format": "jpeg", "aspect_ratio": "16:9"},
            timeout=60,
        )
        if response.status_code == 200:
            return f"data:image/jpeg;base64,{base64.b64encode(response.content).decode()}"
        print(f"Stability AI error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"Stability AI error: {e}")
    return None


def _try_fal(prompt: str, api_key: str) -> Optional[str]:
    """fal.ai — free $1 trial on signup, no credit card. ~200 images free.
    Sign up at https://fal.ai → Dashboard → Keys → Create key
    Add FAL_KEY=your_key to room-designer/.env
    """
    try:
        response = requests.post(
            "https://fal.run/fal-ai/flux/schnell",
            headers={
                "Authorization": f"Key {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 4,
                "num_images": 1,
                "enable_safety_checker": False,
            },
            timeout=60,
        )
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("images", [{}])[0].get("url", "")
            if image_url:
                img_resp = requests.get(image_url, timeout=30)
                if img_resp.status_code == 200:
                    b64 = base64.b64encode(img_resp.content).decode()
                    content_type = img_resp.headers.get("content-type", "image/jpeg").split(";")[0]
                    return f"data:{content_type};base64,{b64}"
        print(f"fal.ai error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"fal.ai error: {e}")
    return None


def _try_pollinations(prompt: str) -> Optional[str]:
    """Pollinations.AI — completely free, no API key, no signup.
    Uses FLUX model. First call may take 15-30s (cold start), subsequent calls faster.
    """
    try:
        encoded = urllib.parse.quote(prompt)
        url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            f"?width=1280&height=720&model=flux&nologo=true&seed={int(time.time()) % 9999}"
        )
        response = requests.get(url, timeout=90)
        if response.status_code == 200 and response.content:
            b64 = base64.b64encode(response.content).decode()
            return f"data:image/jpeg;base64,{b64}"
        print(f"Pollinations error {response.status_code}")
    except Exception as e:
        print(f"Pollinations error: {e}")
    return None


def _try_hf(prompt: str, token: str, retries: int = 3) -> Optional[str]:
    """HuggingFace FLUX.1-schnell via router — confirmed working with fine-grained token."""
    HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for attempt in range(retries):
        try:
            response = requests.post(
                HF_MODEL_URL, headers=headers,
                json={"inputs": prompt, "parameters": {"width": 1024, "height": 576}},
                timeout=60,
            )
            if response.status_code == 503:
                wait = 20
                try:
                    wait = response.json().get("estimated_time", 20)
                except Exception:
                    pass
                time.sleep(min(wait, 30))
                continue
            if response.status_code == 402:
                print("HF credits depleted")
                return None
            if response.status_code != 200:
                print(f"HF error {response.status_code}: {response.text[:200]}")
                return None
            ct = response.headers.get("content-type", "")
            mime = ct.split(";")[0] if ct else "image/jpeg"
            return f"data:{mime};base64,{base64.b64encode(response.content).decode()}"
        except requests.exceptions.Timeout:
            if attempt == retries - 1:
                return None
            time.sleep(5)
        except Exception as e:
            print(f"HF error: {e}")
            return None
    return None
