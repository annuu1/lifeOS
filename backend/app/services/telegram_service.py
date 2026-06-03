from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
from app.ai.grok_provider import GroqProvider
from app.services.memory_service import MemoryService
from app.services.extraction_service import ExtractionService
from app.services.workflow_service import WorkflowService
from app.db.database import SessionLocal

load_dotenv()

class TelegramService:
    def __init__(self):
        self.token = os.getenv("bot_token")
        self.ai_provider = GroqProvider()
        self.extraction_service = ExtractionService(self.ai_provider)
        self.workflow_service = WorkflowService(self.token)
        self.app = ApplicationBuilder().token(self.token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to LifeOS. I am your AI assistant. I will remember what you tell me.")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        chat_id = str(update.effective_chat.id)
        tz = pytz.timezone("Asia/Kolkata")

        from app.models.models import Task
        from sqlalchemy import update as sqlalchemy_update

        if data.startswith("task_"):
            parts = data.split("_")
            action = parts[1]
            task_id = int(parts[2])

            async with SessionLocal() as session:
                if action == "done":
                    await session.execute(sqlalchemy_update(Task).where(Task.id == task_id).values(status="completed"))
                    await session.commit()
                    await query.edit_message_text(text=f"✅ Task marked as completed!")
                
                elif action == "skip":
                    await session.execute(sqlalchemy_update(Task).where(Task.id == task_id).values(status="skipped"))
                    await session.commit()
                    await query.edit_message_text(text=f"❌ Task skipped.")

                elif action == "later":
                    keyboard = [
                        [
                            InlineKeyboardButton("15m", callback_data=f"snooze_{task_id}_15"),
                            InlineKeyboardButton("30m", callback_data=f"snooze_{task_id}_30")
                        ],
                        [
                            InlineKeyboardButton("1h", callback_data=f"snooze_{task_id}_60"),
                            InlineKeyboardButton("Custom", callback_data=f"snooze_{task_id}_custom")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await query.edit_message_text(text="How much later?", reply_markup=reply_markup)

                elif action == "postpone":
                    await query.edit_message_text(text="Please tell me when you want to postpone this to (e.g., 'tomorrow at 10am')")

        elif data.startswith("snooze_"):
            parts = data.split("_")
            task_id = int(parts[1])
            minutes = parts[2]
            
            if minutes == "custom":
                await query.edit_message_text(text="Type how much later you want this task (e.g., '2 hours')")
            else:
                new_time = datetime.now(tz) + timedelta(minutes=int(minutes))
                async with SessionLocal() as session:
                    await session.execute(
                        sqlalchemy_update(Task)
                        .where(Task.id == task_id)
                        .values(schedule=new_time.replace(tzinfo=None), status="pending")
                    )
                    await session.commit()
                await query.edit_message_text(text=f"⏰ Task snoozed for {minutes} minutes. New time: {new_time.strftime('%I:%M %p')}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        chat_id = str(update.effective_chat.id)
        
        async with SessionLocal() as session:
            memory_service = MemoryService(session, self.extraction_service)
            
            # 1. Get user context
            user_context = await memory_service.get_user_context(chat_id)
            
            # 2. Process input (extract and save)
            extracted = await memory_service.process_user_input(chat_id, user_text)
            
            # 3. Trigger proactive actions
            proactive_actions = await self.workflow_service.trigger_proactive_actions(chat_id, extracted)
            
            # 4. Generate response with context
            system_prompt = f"""You are LifeOS, a personal life operating system.
Current User Context:
{user_context}

Be helpful, proactive, and acknowledge if you've learned something new.
If the Workflow Service suggested proactive actions, incorporate them naturally into your response or add them after.
Proactive Suggestions: {proactive_actions}"""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ]
            
            try:
                response = await self.ai_provider.generate_response(messages)
                await update.message.reply_text(response)
            except Exception as e:
                await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")

    async def start(self):
        print("Bot is starting...", flush=True)
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def stop(self):
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()

    def run(self):
        # Keep this for backward compatibility or direct script execution
        print("Bot is starting...", flush=True)
        self.app.run_polling()

if __name__ == "__main__":
    service = TelegramService()
    service.run()
