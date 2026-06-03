from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    schedule: Optional[datetime] = None
    status: str = "pending"
    recurrence: Optional[str] = None

class TaskCreate(TaskBase):
    user_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    schedule: Optional[datetime] = None
    status: Optional[str] = None

class HealthBase(BaseModel):
    condition: str
    status: str = "active"
    details: Dict[str, Any] = {}

class HealthCreate(HealthBase):
    user_id: int

class FactBase(BaseModel):
    fact: str
    category: str = "General"
    confidence_score: float = 1.0

class FactCreate(FactBase):
    user_id: int
