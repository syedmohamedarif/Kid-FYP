import json
import os
from typing import Any, Dict

import httpx

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

SYSTEM_PROMPT = (
    "You are AuraSense, a music assistant. Always respond with only valid JSON, "
    "with keys: intent, mood, genre, language, activity, duration. "
    "Never include additional text. Do not mention any APIs or platforms. "
    "Genre must be an array of strings. Duration must be a number in minutes."
)


class GroqClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def chat(self, message: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            "temperature": 0.3,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        content = data["choices"][0]["message"]["content"]
        return _parse_json(content)


def _parse_json(content: str) -> Dict[str, Any]:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            return json.loads(content[start : end + 1])
    return {
        "intent": "CREATE_PLAYLIST",
        "mood": "relaxed",
        "genre": ["melody"],
        "language": "English",
        "activity": "focus",
        "duration": 30,
    }
