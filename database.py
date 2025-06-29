from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Database URL - using SQLite for simplicity
DATABASE_URL = "sqlite:///./tasks.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session 
