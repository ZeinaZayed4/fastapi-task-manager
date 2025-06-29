from datetime import datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session
from contextlib import asynccontextmanager

from models import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    HealthResponse, APIInfo, TaskStatus, TaskPriority
)
from database import get_session, create_db_and_tables
import crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI and SQLModel",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/", response_model=APIInfo, tags=["Root"])
def read_root():
    return APIInfo(
        name="Task Management API",
        version="1.0.0",
        description="A simple task management API built with FastAPI and SQLModel",
        endpoints=[
            "GET / - API Information",
            "GET /health - Health Check",
            "POST /tasks - Create Task",
            "GET /tasks - List Tasks",
            "GET /tasks/{task_id} - Get Task",
            "PUT /tasks/{task_id} - Update Task",
            "DELETE /tasks/{task_id} - Delete Task",
            "GET /tasks/status/{status} - Get Tasks by Status",
            "GET /tasks/priority/{priority} - Get Tasks by Priority"
        ]
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@app.post("/tasks", response_model=TaskResponse, status_code=201, tags=["Tasks"])
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    return crud.create_task(session, task)


@app.get("/tasks", response_model=TaskListResponse, tags=["Tasks"])
def read_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    tasks, total = crud.get_tasks(session, skip=skip, limit=limit)
    return TaskListResponse(
        tasks=tasks,
        total=total,
        skip=skip,
        limit=limit
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    task = crud.update_task(session, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=200, tags=["Tasks"])
def delete_task(task_id: int, session: Session = Depends(get_session)):
    success = crud.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.get("/tasks/status/{status}", response_model=TaskListResponse, tags=["Filtering"])
def read_tasks_by_status(
    status: TaskStatus,
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    tasks, total = crud.get_tasks_by_status(session, status, skip=skip, limit=limit)
    return TaskListResponse(
        tasks=tasks,
        total=total,
        skip=skip,
        limit=limit
    )


@app.get("/tasks/priority/{priority}", response_model=TaskListResponse, tags=["Filtering"])
def read_tasks_by_priority(
    priority: TaskPriority,
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    tasks, total = crud.get_tasks_by_priority(session, priority, skip=skip, limit=limit)
    return TaskListResponse(
        tasks=tasks,
        total=total,
        skip=skip,
        limit=limit
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
