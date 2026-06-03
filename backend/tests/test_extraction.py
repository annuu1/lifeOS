import pytest
import asyncio
from app.ai.grok_provider import GroqProvider
from app.services.extraction_service import ExtractionService

@pytest.mark.asyncio
async def test_extraction():
    provider = GroqProvider()
    service = ExtractionService(provider)
    user_input = "I bought a new scooter today. Remind me to check insurance tomorrow at 10am. Also, I am allergic to peanuts."
    
    extracted = await service.extract(user_input)
    assert extracted is not None
    assert "life_facts" in extracted
    assert "tasks" in extracted
    
    # Check if scooter was captured as timeline event or fact
    found_scooter = any("scooter" in str(v).lower() for v in extracted.values())
    assert found_scooter
    
    # Check if peanut allergy was captured
    found_allergy = any("peanut" in str(v).lower() for v in extracted.values())
    assert found_allergy
    
    print(f"\nExtracted Entities: {extracted}")

if __name__ == "__main__":
    asyncio.run(test_extraction())
