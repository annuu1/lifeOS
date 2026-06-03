from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.db.database import get_db
from app.models.models import User, LifeFact, Task, HealthRecord, Goal, TimelineEvent
from app.schemas.schemas import TaskCreate, TaskUpdate, HealthCreate, FactCreate
from typing import List

router = APIRouter()

# --- Users ---
@router.get("/users", response_model=List[dict])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"id": u.id, "telegram_chat_id": u.telegram_chat_id} for u in users]

# --- Tasks ---
@router.get("/tasks/{user_id}")
async def get_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc()))
    return result.scalars().all()

@router.post("/tasks")
async def create_task(task_data: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = Task(**task_data.dict())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()
    return {"status": "success"}

@router.patch("/tasks/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    await db.execute(update(Task).where(Task.id == task_id).values(**task_data.dict(exclude_unset=True)))
    await db.commit()
    return {"status": "success"}

# --- Health ---
@router.get("/health/{user_id}")
async def get_health(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HealthRecord).filter(HealthRecord.user_id == user_id))
    return result.scalars().all()

@router.post("/health")
async def create_health(health_data: HealthCreate, db: AsyncSession = Depends(get_db)):
    new_record = HealthRecord(**health_data.dict())
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record

@router.delete("/health/{record_id}")
async def delete_health(record_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(HealthRecord).where(HealthRecord.id == record_id))
    await db.commit()
    return {"status": "success"}

# --- Life Facts ---
@router.get("/facts/{user_id}")
async def get_facts(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LifeFact).filter(LifeFact.user_id == user_id))
    return result.scalars().all()

@router.post("/facts")
async def create_fact(fact_data: FactCreate, db: AsyncSession = Depends(get_db)):
    new_fact = LifeFact(**fact_data.dict())
    db.add(new_fact)
    await db.commit()
    await db.refresh(new_fact)
    return new_fact

@router.delete("/facts/{fact_id}")
async def delete_fact(fact_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(LifeFact).where(LifeFact.id == fact_id))
    await db.commit()
    return {"status": "success"}
