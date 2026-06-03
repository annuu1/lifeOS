import json
from datetime import datetime
from typing import Dict, Any
from app.ai.grok_provider import GroqProvider
from app.ai.prompts import EXTRACTION_PROMPT

class ExtractionService:
    def __init__(self, ai_provider: GroqProvider):
        self.ai_provider = ai_provider

    async def extract(self, user_input: str) -> Dict[str, Any]:
        current_time = datetime.utcnow().isoformat()
        prompt = EXTRACTION_PROMPT.format(user_input=user_input, current_time=current_time)
        
        messages = [
            {"role": "system", "content": "You are a specialized JSON extraction assistant."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response_text = await self.ai_provider.generate_response(messages, temperature=0.1)
            # Find the JSON part in the response (sometimes models add chatter)
            start_index = response_text.find("{")
            end_index = response_text.rfind("}") + 1
            if start_index != -1 and end_index != -1:
                json_str = response_text[start_index:end_index]
                return json.loads(json_str)
            return {}
        except Exception as e:
            print(f"Extraction error: {e}")
            return {}
