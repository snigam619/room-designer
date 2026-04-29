import anthropic
import base64
import json
import re

client = anthropic.Anthropic()


def analyze_room(image_bytes: bytes, media_type: str = "image/jpeg",
                 style: str = "modern", mood: str = "light", budget: str = "1000") -> dict:
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            f"You are an expert interior designer. Analyze this room photo and create a complete design plan.\n\n"
                            f"User preferences:\n"
                            f"- Style: {style}\n"
                            f"- Mood: {mood}\n"
                            f"- Budget: ${budget}\n\n"
                            f"Return ONLY valid JSON, no markdown, no explanation:\n"
                            f"{{\n"
                            f'  "room_type": "<living room|bedroom|dining room|home office>",\n'
                            f'  "design_summary": "<2-3 sentence design brief describing the vision>",\n'
                            f'  "wall_color": {{\n'
                            f'    "name": "<color name e.g. Warm White>",\n'
                            f'    "hex": "<hex code e.g. #F5F0E8>",\n'
                            f'    "description": "<one line why this color works>"\n'
                            f'  }},\n'
                            f'  "accent_color": {{\n'
                            f'    "name": "<accent color name>",\n'
                            f'    "hex": "<hex code>"\n'
                            f'  }},\n'
                            f'  "recommended_products": [\n'
                            f'    "<category1>", "<category2>", "<category3>", "<category4>", "<category5>"\n'
                            f'  ],\n'
                            f'  "wall_decor": {{\n'
                            f'    "primary": "<e.g. Abstract Canvas Print>",\n'
                            f'    "secondary": "<e.g. Floating Shelves with plants>"\n'
                            f'  }}\n'
                            f"}}"
                        ),
                    },
                ],
            }
        ],
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)
