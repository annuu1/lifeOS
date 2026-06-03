## Project Name

LifeOS

---

# Vision

LifeOS is not a task manager.

LifeOS is an AI-powered Personal Life Operating System.

The system acts as:

* Personal Assistant
* Executive Assistant
* Caretaker
* Life Memory System
* Habit Tracker
* Goal Planner
* Reminder Engine
* Context-Aware AI Companion

The assistant must remember the user's life, understand their goals, maintain context over years, proactively assist them, and generate reminders and actions autonomously.

The user should feel like they are interacting with a trusted human assistant rather than a reminder application.

---

# Core Philosophy

Traditional reminder apps require users to think.

LifeOS should think for the user.

Example:

User:

"I have fever."

Traditional App:

Creates nothing.

LifeOS:

* Creates health event
* Asks if doctor has been consulted
* Asks about medicines
* Creates medicine reminders
* Creates hydration reminders
* Creates follow-up reminders
* Tracks recovery progress
* Marks illness resolved when recovered

The assistant should identify missing information and proactively gather it.

---

# Tech Stack

Backend:

* FastAPI
* SQLAlchemy
* SQLite
* APScheduler

Frontend:

* Next.js
* TypeScript
* TailwindCSS
* Shadcn UI

Containerization:

* Docker
* Docker Compose

Database:

* SQLite

SQLite file must persist using Docker volumes.

Example:

/data/lifeos.db

The database must never be lost when containers restart.

---

# AI Architecture

Primary AI Provider:

Grok API

Primary Model:

llama-8b-instant

Fallback Providers:

* OpenAI
* Gemini
* OpenRouter
* Local Models

AI Provider selection should be configurable.

Implement provider abstraction layer.

Example:

AIProvider

* GrokProvider
* OpenAIProvider
* GeminiProvider
* OpenRouterProvider

System should automatically fallback when primary provider fails.

---

# Core Entities

## User

Stores:

* telegram_chat_id
* profile
* preferences
* timezone

---

## Tasks

Stores:

* title
* description
* schedule
* recurrence
* status

---

## Goals

Stores:

* long term objectives
* priorities
* completion status

Examples:

* Build Autozonex
* Complete MCA
* Improve Health

---

## Projects

Examples:

* Autozonex
* MCA Studies

Stores:

* progress
* milestones
* status

---

## Habits

Examples:

* Review portfolio
* Take medicine
* Exercise

---

## Life Facts

Persistent user facts.

Examples:

* Owns electric scooter
* Has two children
* Married
* Vegetarian

Facts should contain:

* confidence score
* source
* status
* created_at
* updated_at

Facts should remain separate from summaries.

---

## Health Records

Health conditions must be first-class entities.

Example:

Condition:
Fever

Status:
Resolved

Started:
2026-05-01

Resolved:
2026-05-23

The system should maintain complete health history.

---

## Timeline Events

Stores life history.

Examples:

* Bought scooter
* Started project
* Got promotion
* Child started school

Timeline should never be deleted.

This becomes the user's life journal.

---

## AI Observations

AI-generated conclusions.

Example:

User usually reviews portfolio around 6 PM.

User skips study sessions on weekends.

User takes medicine late at night.

These observations should have confidence scores.

---

# Memory System

The memory system is the most important feature.

Memory must be divided into:

1. Facts
2. Timeline
3. Goals
4. Projects
5. Health
6. Habits
7. Tasks
8. AI Observations

Never rely solely on summaries.

Summaries are disposable.

Structured memory is permanent.

---

# Life Domains

The assistant should classify information into domains.

Domains:

* Health
* Family
* Career
* Finance
* Education
* Assets
* Projects
* Habits
* Travel
* Personal

Every event belongs to a domain.

---

# Domain Workflows

LifeOS should activate workflows automatically.

Example:

Health Domain

Trigger:

"I have fever."

Workflow:

* Ask doctor status
* Ask medicine details
* Create medicine reminders
* Create hydration reminders
* Create follow-up reminders
* Track recovery

---

Example:

Asset Domain

Trigger:

"I bought a scooter."

Workflow:

* Ask purchase date
* Ask insurance date
* Ask service schedule
* Create reminders

---

Example:

Finance Domain

Trigger:

"I trade stocks."

Workflow:

* Portfolio review reminders
* Journal reminders
* Monthly performance review reminders

---

# Proactive Assistant

The assistant must not wait for explicit instructions.

Examples:

User mentions fever.

Assistant should proactively ask relevant questions.

User mentions new vehicle.

Assistant should proactively ask insurance details.

User mentions exams.

Assistant should suggest study plans.

The assistant should think ahead.

---

# Decision Framework

Every AI action should have confidence levels.

High Confidence:

Assistant may act automatically.

Examples:

* Reschedule reminder
* Create recurring reminder

Medium Confidence:

Assistant should ask for confirmation.

Low Confidence:

Assistant must ask clarifying questions.

---

# Telegram Integration

Telegram is the primary interface.

Users interact through Telegram.

Notifications must include action buttons.

Examples:

Completed
Postpone
Skip
Remind Later

User feedback should continuously improve scheduling.

---

# Daily Summary

Generate every morning.

Include:

* Today's priorities
* Pending tasks
* Important reminders
* Goal progress

---

# Weekly Review

Generate every Sunday.

Include:

* Completed tasks
* Missed tasks
* Goal progress
* Health summary
* Project progress

---

# Architecture Rules

Follow Clean Architecture.

Layers:

* API Layer
* Service Layer
* AI Layer
* Repository Layer
* Database Layer

Never place business logic in routes.

Keep services isolated.

All AI functionality must be modular.

All workflows must be configurable.

---

# Future Vision

The final product should feel like:

"A trusted digital chief-of-staff and caretaker that understands the user's life, remembers important context for years, proactively assists with decisions, and helps the user achieve goals while managing daily responsibilities."

Every architectural decision should move the system toward this vision.

---

# Progress Tracker

## Module 1: Foundation & Database Architecture
- [x] Initialize FastAPI project structure
- [x] Define SQLAlchemy database models
- [x] Implement Repository layer
- [x] Setup Database migrations (optional/initial)
- [x] Verify with tests

## Module 2: AI Provider & Telegram Integration
- [x] Implement AIProvider abstraction layer
- [x] Integrate Grok API
- [x] Setup Telegram Bot API
- [x] Implement basic Chat Service

## Module 3: Core Memory & Extraction Engine
- [x] Design extraction prompts
- [x] Implement entity extraction service
- [x] Context injection logic

## Module 4: Domain Workflows & Proactive Assistance
- [x] Domain classification
- [x] Health workflow implementation
- [x] Confidence-based decision engine

## Module 5: Scheduling, Summaries, & Notifications
- [x] APScheduler integration
- [x] Daily/Weekly summary jobs
- [x] Telegram notification engine

## Module 6: Containerization (Docker)
- [x] Dockerfile for Backend
- [x] docker-compose.yml with persistent volumes

## Module 7: Next.js Frontend Dashboard
- [x] Initialize Next.js project
- [x] Frontend API integration
- [x] Dashboard UI components
