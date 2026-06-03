import httpx
import os
from typing import List, Dict, Any
from app.ai.provider import AIProvider
from dotenv import load_dotenv

load_dotenv()

class GroqProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("grok_api") # Using the key name from .env created earlier
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1024)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def extract_entities(self, text: str) -> Dict[str, Any]:
        # This will be implemented in Module 3
        return {}
