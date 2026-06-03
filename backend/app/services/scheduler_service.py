from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.database import SessionLocal
from app.models.models import User, Task, Goal, HealthRecord
from sqlalchemy import select
from telegram import Bot
import os
from datetime import datetime, timedelta
import pytz

class SchedulerService:
    def __init__(self, bot_token: str):
        self.tz = pytz.timezone("Asia/Kolkata")
        self.scheduler = AsyncIOScheduler(timezone=self.tz)
        self.bot_token = bot_token
        self.bot = Bot(token=bot_token)

    async def send_daily_summary(self):
        async with SessionLocal() as session:
            # For now, we'll send to all users.
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            
            for user in users:
                summary = await self._generate_summary(session, user.id)
                try:
                    await self.bot.send_message(chat_id=user.telegram_chat_id, text=summary)
                except Exception as e:
                    print(f"Failed to send summary to {user.telegram_chat_id}: {e}")

    async def _generate_summary(self, session, user_id: int) -> str:
        # Fetch today's tasks
        today = datetime.now(self.tz).date()
        tasks_query = select(Task).filter(Task.user_id == user_id, Task.status == "pending")
        tasks_result = await session.execute(tasks_query)
        tasks = tasks_result.scalars().all()
        
        # Fetch active goals
        goals_query = select(Goal).filter(Goal.user_id == user_id, Goal.status == "active")
        goals_result = await session.execute(goals_query)
        goals = goals_result.scalars().all()

        summary = "☀️ Good Morning! Here is your LifeOS Daily Summary:\n\n"
        
        if tasks:
            summary += "📋 Pending Tasks:\n" + "\n".join([f"- {t.title}" for t in tasks]) + "\n\n"
        else:
            summary += "✅ No pending tasks for today!\n\n"
            
        if goals:
            summary += "🎯 Active Goals:\n" + "\n".join([f"- {g.title}" for g in goals]) + "\n\n"
            
        summary += "Have a great day!"
        return summary

    def setup_jobs(self):
        # Schedule daily summary at 8:00 AM IST
        self.scheduler.add_job(self.send_daily_summary, 'cron', hour=8, minute=0)

    def start(self):
        self.setup_jobs()
        self.scheduler.start()
        print("Scheduler started.")
