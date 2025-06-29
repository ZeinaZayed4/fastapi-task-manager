from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select, func
from models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority


def create_task(session: Session, task: TaskCreate) -> Task:
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_task(session: Session, task_id: int) -> Optional[Task]:
    statement = select(Task).where(Task.id == task_id)
    return session.exec(statement).first()


def get_tasks(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None
) -> tuple[List[Task], int]:
    statement = select(Task)
    
    if status:
        statement = statement.where(Task.status == status)
    if priority:
        statement = statement.where(Task.priority == priority)
    
    count_statement = select(func.count(Task.id))
    if status:
        count_statement = count_statement.where(Task.status == status)
    if priority:
        count_statement = count_statement.where(Task.priority == priority)
    
    total = session.exec(count_statement).first()
    
    statement = statement.offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    
    return tasks, total


def get_tasks_by_status(session: Session, status: TaskStatus, skip: int = 0, limit: int = 100) -> tuple[List[Task], int]:
    return get_tasks(session, skip=skip, limit=limit, status=status)


def get_tasks_by_priority(session: Session, priority: TaskPriority, skip: int = 0, limit: int = 100) -> tuple[List[Task], int]:
    return get_tasks(session, skip=skip, limit=limit, priority=priority)


def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    db_task = get_task(session, task_id)
    if not db_task:
        return None
    
    update_data = task_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.now()
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    
    return db_task


def delete_task(session: Session, task_id: int) -> bool:
    db_task = get_task(session, task_id)
    if not db_task:
        return False
    
    session.delete(db_task)
    session.commit()
    return True 
