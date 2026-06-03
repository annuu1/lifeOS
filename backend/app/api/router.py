from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.models import User, LifeFact, Task, HealthRecord, Goal, TimelineEvent
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[dict])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"id": u.id, "telegram_chat_id": u.telegram_chat_id} for u in users]

@router.get("/tasks/{user_id}")
async def get_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).filter(Task.user_id == user_id))
    tasks = result.scalars().all()
    return tasks

@router.get("/health/{user_id}")
async def get_health(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HealthRecord).filter(HealthRecord.user_id == user_id))
    health = result.scalars().all()
    return health

@router.get("/facts/{user_id}")
async def get_facts(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LifeFact).filter(LifeFact.user_id == user_id))
    facts = result.scalars().all()
    return facts
