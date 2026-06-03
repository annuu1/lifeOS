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

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

...

    async def check_pending_tasks(self):
        print(f"Checking for pending tasks at {datetime.now(self.tz)}...", flush=True)
        async with SessionLocal() as session:
            now = datetime.now(self.tz).replace(tzinfo=None)
            query = select(Task).filter(Task.status == "pending", Task.schedule <= now)
            result = await session.execute(query)
            tasks = result.scalars().all()
            
            print(f"Found {len(tasks)} tasks to notify.", flush=True)
            for task in tasks:
                user_query = select(User).filter(User.id == task.user_id)
                user_result = await session.execute(user_query)
                user = user_result.scalars().first()
                
                if user:
                    print(f"Sending notification for task {task.id} to {user.telegram_chat_id}...", flush=True)
                    message = f"📌 *Task Reminder*\n\n*Title:* {task.title}\n*Description:* {task.description or 'No description'}\n\n*Status:* Pending"
                    
                    keyboard = [
                        [
                            InlineKeyboardButton("✅ Done", callback_data=f"task_done_{task.id}"),
                            InlineKeyboardButton("⏰ Later", callback_data=f"task_later_{task.id}")
                        ],
                        [
                            InlineKeyboardButton("📅 Postpone", callback_data=f"task_postpone_{task.id}"),
                            InlineKeyboardButton("❌ Skip", callback_data=f"task_skip_{task.id}")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    try:
                        await self.bot.send_message(
                            chat_id=user.telegram_chat_id, 
                            text=message, 
                            parse_mode="Markdown",
                            reply_markup=reply_markup
                        )
                        # We change status to "notified" instead of "completed" so we know it is out but not yet acted upon
                        task.status = "notified" 
                        print(f"Successfully sent notification for task {task.id}.", flush=True)
                    except Exception as e:
                        print(f"Failed to send notification for task {task.id}: {e}", flush=True)
            
            await session.commit()

    def setup_jobs(self):
        # Schedule daily summary at 8:00 AM IST
        self.scheduler.add_job(self.send_daily_summary, 'cron', hour=8, minute=0)
        # Check for pending tasks every 10 seconds for faster testing
        self.scheduler.add_job(self.check_pending_tasks, 'interval', seconds=10)

    def start(self):
        print("Scheduler is starting...", flush=True)
        self.setup_jobs()
        self.scheduler.start()
        print(f"Scheduler started with {len(self.scheduler.get_jobs())} jobs.", flush=True)
