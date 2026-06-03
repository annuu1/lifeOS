import pytest
import asyncio
from app.db.database import SessionLocal, Base, engine
from app.models.models import User
from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_user():
    async with SessionLocal() as session:
        # Create a new user
        new_user = User(telegram_chat_id="123456789", timezone="Asia/Kolkata")
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        assert new_user.id is not None
        assert new_user.telegram_chat_id == "123456789"
        
        # Retrieve the user
        query = select(User).filter(User.telegram_chat_id == "123456789")
        result = await session.execute(query)
        user = result.scalars().first()
        
        assert user is not None
        assert user.timezone == "Asia/Kolkata"
        
        # Cleanup
        await session.delete(user)
        await session.commit()

if __name__ == "__main__":
    # This allows running the test script directly if needed
    asyncio.run(test_create_user())
