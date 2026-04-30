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
                            f"You are an expert interior designer. Carefully analyze this room photo.\n\n"
                            f"User preferences:\n"
                            f"- Style: {style}\n"
                            f"- Mood: {mood}\n"
                            f"- Budget: ${budget} total for all furniture combined\n\n"
                            f"IMPORTANT: Look at what furniture and items are actually visible in this room photo. "
                            f"Only recommend product categories that are relevant to what you see. "
                            f"For example: if it's a bedroom, recommend Bed, Dresser, Side Table — not Sofa or Dining Table. "
                            f"If it's a living room, recommend Sofa, Coffee Table, Accent Chair — not Bed or Dresser. "
                            f"Pick 3-5 categories maximum that are the most impactful for this specific room. "
                            f"The total estimated cost across all recommended categories must stay within ${budget} ± $100. "
                            f"Prioritize fewer, higher-impact pieces if the budget is tight.\n\n"
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
                            f'  "detected_items": ["<list furniture/items you can actually see in the photo>"],\n'
                            f'  "recommended_products": [\n'
                            f'    "<pick 3-5 from ONLY these exact values based on what makes sense for this room: Sofa, Coffee Table, Accent Chair, Floor Lamp, Area Rug, Bookshelf, Side Table, Bed, Dining Table, Dresser>"\n'
                            f'  ]\n'
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
