from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for persistence, path as specified in GEMINI.md
# In Docker, we will mount a volume to /data
DB_PATH = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////data/lifeos.db")

engine = create_async_engine(DB_PATH)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as session:
        yield session
