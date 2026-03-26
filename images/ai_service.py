import base64
import json

from decouple import config
from openai import OpenAI

PROMPT = (
    "Analyze this image and respond with valid JSON only — no markdown, no code fences. "
    "The JSON must have exactly two keys: "
    '"tags" (an array of descriptive keyword strings) and '
    '"description" (a single sentence describing the image).'
)


def analyze_image(image_path: str) -> dict:
    client = OpenAI(api_key=config('OPENAI_API_KEY'))

    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{encoded}',
                        },
                    },
                    {
                        'type': 'text',
                        'text': PROMPT,
                    },
                ],
            }
        ],
        max_tokens=500,
    )

    raw = response.choices[0].message.content.strip()
    result = json.loads(raw)

    return {
        'tags': result['tags'],
        'description': result['description'],
    }
