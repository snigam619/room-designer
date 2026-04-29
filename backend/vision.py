import anthropic
import base64
import json
import re


client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment


def analyze_room(image_bytes: bytes, media_type: str = "image/jpeg") -> dict:
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
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
                            "Analyze this room photo carefully. "
                            "Return ONLY a valid JSON object — no explanation, no markdown, no code fences. "
                            "Use exactly this structure:\n"
                            "{\n"
                            '  "detected_style": "<one of: modern, mid-century, boho, scandinavian, industrial, traditional>",\n'
                            '  "room_type": "<one of: living room, bedroom, dining room, home office>",\n'
                            '  "existing_items": ["list of items you can see in the room"],\n'
                            '  "missing_items": ["up to 5 furniture or decor items that would complete this room"],\n'
                            '  "color_palette": ["3 dominant colors in the room"]\n'
                            "}"
                        ),
                    },
                ],
            }
        ],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if Claude wraps the response anyway
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)
