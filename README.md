# LifeOS

AI-powered Personal Life Operating System.

## Features

- **Telegram Bot Interface:** Primary interface for interacting with your AI caretaker.
- **Entity Extraction:** Automatically extracts Tasks, Facts, Health Records, and Goals from messages.
- **Memory System:** Long-term persistence of your life data.
- **Proactive Assistant:** Health and Asset workflows that ask follow-up questions.
- **Daily Summaries:** Automated morning summaries of your tasks and goals.
- **Frontend Dashboard:** Next.js dashboard to visualize your life history and data.
- **Dockerized:** Easy deployment with persistent SQLite storage.

## Setup & Running

### 1. Requirements
- Docker and Docker Compose
- Groq API Key
- Telegram Bot Token

### 2. Environment Variables
Create a `.env` file in the root (already created during development):
```
grok_api=your_groq_key
bot_token=your_telegram_bot_token
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

### 4. Local Development (Alternative)
**Backend:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
python3 backend/app/main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, SQLite, APScheduler
- **AI:** Groq API (llama-3.1-8b-instant)
- **Frontend:** Next.js, TypeScript, TailwindCSS
- **Deployment:** Docker
