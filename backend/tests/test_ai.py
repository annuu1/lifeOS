import pytest
import asyncio
from app.ai.grok_provider import GroqProvider

@pytest.mark.asyncio
async def test_ai_response():
    provider = GroqProvider()
    messages = [
        {"role": "user", "content": "Hello, who are you?"}
    ]
    response = await provider.generate_response(messages)
    assert response is not None
    assert len(response) > 0
    print(f"\nAI Response: {response}")

if __name__ == "__main__":
    asyncio.run(test_ai_response())
