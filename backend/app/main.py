from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.services.telegram_service import TelegramService
from app.services.scheduler_service import SchedulerService
from app.db.init_db import init_db
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    
    # Initialize services
    print("Initializing services...")
    bot_service = TelegramService()
    scheduler_service = SchedulerService(os.getenv("bot_token"))
    
    # Start bot
    print("Starting Telegram Bot...")
    await bot_service.start()
    
    # Start scheduler
    print("Starting Scheduler...")
    scheduler_service.start()
    
    print("Lifespan startup complete.")
    yield
    
    # Shutdown logic
    await bot_service.stop()
    scheduler_service.scheduler.shutdown()

app = FastAPI(title="LifeOS API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "LifeOS API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
