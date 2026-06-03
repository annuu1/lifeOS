from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
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
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to LifeOS. I am your AI assistant. I will remember what you tell me.")

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
