from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AIProvider(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass

    @abstractmethod
    async def extract_entities(self, text: str) -> Dict[str, Any]:
        pass
