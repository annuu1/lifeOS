from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User, LifeFact, Task, HealthRecord, Goal, TimelineEvent
from app.services.extraction_service import ExtractionService
from datetime import datetime
from typing import List, Dict, Any

class MemoryService:
    def __init__(self, db_session: AsyncSession, extraction_service: ExtractionService):
        self.db = db_session
        self.extraction_service = extraction_service

    async def process_user_input(self, telegram_chat_id: str, text: str):
        # 1. Get or create user
        query = select(User).filter(User.telegram_chat_id == telegram_chat_id)
        result = await self.db.execute(query)
        user = result.scalars().first()
        if not user:
            user = User(telegram_chat_id=telegram_chat_id)
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

        # 2. Extract entities
        entities = await self.extraction_service.extract(text)

        # 3. Save entities
        await self._save_entities(user.id, entities)
        return entities

    async def _save_entities(self, user_id: int, entities: Dict[str, Any]):
        # Save Life Facts
        for fact_data in entities.get("life_facts", []):
            fact = LifeFact(
                user_id=user_id,
                fact=fact_data["fact"],
                category=fact_data.get("category", "General"),
                confidence_score=fact_data.get("confidence", 1.0)
            )
            self.db.add(fact)

        # Save Tasks
        for task_data in entities.get("tasks", []):
            schedule = None
            if task_data.get("schedule"):
                try:
                    schedule = datetime.fromisoformat(task_data["schedule"])
                except:
                    pass
            task = Task(
                user_id=user_id,
                title=task_data["title"],
                description=task_data.get("description"),
                schedule=schedule,
                recurrence=task_data.get("recurrence")
            )
            self.db.add(task)

        # Save Health Records
        for health_data in entities.get("health_records", []):
            record = HealthRecord(
                user_id=user_id,
                condition=health_data["condition"],
                status=health_data.get("status", "active"),
                details=health_data.get("details", {})
            )
            self.db.add(record)

        # Save Goals
        for goal_data in entities.get("goals", []):
            target_date = None
            if goal_data.get("target_date"):
                try:
                    target_date = datetime.fromisoformat(goal_data["target_date"])
                except:
                    pass
            goal = Goal(
                user_id=user_id,
                title=goal_data["title"],
                description=goal_data.get("description"),
                target_date=target_date
            )
            self.db.add(goal)

        await self.db.commit()

    async def get_user_context(self, telegram_chat_id: str) -> str:
        query = select(User).filter(User.telegram_chat_id == telegram_chat_id)
        result = await self.db.execute(query)
        user = result.scalars().first()
        if not user:
            return "No previous context found."

        # Fetch facts
        facts_query = select(LifeFact).filter(LifeFact.user_id == user.id)
        facts_result = await self.db.execute(facts_query)
        facts = facts_result.scalars().all()
        
        # Fetch active health records
        health_query = select(HealthRecord).filter(HealthRecord.user_id == user.id, HealthRecord.status == "active")
        health_result = await self.db.execute(health_query)
        health = health_result.scalars().all()

        context_parts = []
        if facts:
            context_parts.append("Known Facts: " + ", ".join([f.fact for f in facts]))
        if health:
            context_parts.append("Current Health Conditions: " + ", ".join([h.condition for h in health]))
        
        return "\n".join(context_parts) if context_parts else "No specific context known yet."
