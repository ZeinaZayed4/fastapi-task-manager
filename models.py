from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    assigned_to: Optional[str] = Field(default=None, max_length=100)


class TaskCreate(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = Field(default=None)
    assigned_to: Optional[str] = Field(default=None, max_length=100)

    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v <= datetime.now():
            raise ValueError('Due date must be in the future')
        return v


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = Field(default=None)
    priority: Optional[TaskPriority] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    assigned_to: Optional[str] = Field(default=None, max_length=100)

    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Title cannot be empty or whitespace only')
            return v.strip()
        return v

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v <= datetime.now():
            raise ValueError('Due date must be in the future')
        return v


class TaskResponse(SQLModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]


class TaskListResponse(SQLModel):
    tasks: list[TaskResponse]
    total: int
    skip: int
    limit: int


class HealthResponse(SQLModel):
    status: str
    timestamp: datetime


class APIInfo(SQLModel):
    name: str
    version: str
    description: str
    endpoints: list[str] 
