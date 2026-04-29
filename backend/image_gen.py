import os
import requests
import base64
import time
from typing import Optional

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


def _build_prompt(style: str, wall_color: str, room_type: str, product_names: list) -> str:
    items = ", ".join(product_names[:5]) if product_names else "furniture"
    return (
        f"A professional interior design photo of a beautifully decorated {room_type}, "
        f"{style} style, {wall_color} painted walls, featuring {items}, "
        f"natural lighting, high-end interior photography, 4k, photorealistic, "
        f"architectural digest style, no people"
    )


def generate_room_render(
    style: str,
    wall_color_name: str,
    room_type: str,
    selected_products: list,
    retries: int = 3,
) -> Optional[str]:
    if not HF_API_TOKEN:
        return None

    prompt = _build_prompt(style, wall_color_name, room_type, selected_products)
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": 768,
            "height": 512,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        },
    }

    for attempt in range(retries):
        try:
            response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)

            # Model is loading — wait and retry
            if response.status_code == 503:
                wait = response.json().get("estimated_time", 20)
                time.sleep(min(wait, 30))
                continue

            if response.status_code != 200:
                return None

            # Response is raw image bytes — convert to base64 data URL
            image_b64 = base64.b64encode(response.content).decode("utf-8")
            return f"data:image/jpeg;base64,{image_b64}"

        except requests.exceptions.Timeout:
            if attempt == retries - 1:
                return None
            time.sleep(5)
        except Exception:
            return None

    return None
