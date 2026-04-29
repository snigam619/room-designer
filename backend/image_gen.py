import os
import requests
import base64
import time
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"


def _build_prompt(style: str, wall_color: str, room_type: str, product_names: list) -> str:
    items = ", ".join(product_names[:5]) if product_names else "furniture"
    return (
        f"A professional interior design photo of a beautifully decorated {room_type}, "
        f"{style} style, {wall_color} painted walls, featuring {items}. "
        f"Natural lighting, high-end interior photography, architectural digest style, "
        f"photorealistic, no people, wide angle shot showing the full room."
    )


def generate_room_render(
    style: str,
    wall_color_name: str,
    room_type: str,
    selected_products: list,
    retries: int = 2,
) -> Optional[str]:
    token = os.getenv("HF_API_TOKEN")
    if not token:
        return None

    prompt = _build_prompt(style, wall_color_name, room_type, selected_products)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"inputs": prompt}

    for attempt in range(retries):
        try:
            response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)

            # Model loading — wait and retry
            if response.status_code == 503:
                wait = 20
                try:
                    wait = response.json().get("estimated_time", 20)
                except Exception:
                    pass
                time.sleep(min(wait, 30))
                continue

            if response.status_code != 200:
                print(f"HF error {response.status_code}: {response.text[:200]}")
                return None

            image_b64 = base64.b64encode(response.content).decode("utf-8")
            return f"data:image/jpeg;base64,{image_b64}"

        except requests.exceptions.Timeout:
            if attempt == retries - 1:
                return None
            time.sleep(5)
        except Exception as e:
            print(f"Image generation error: {e}")
            return None

    return None
