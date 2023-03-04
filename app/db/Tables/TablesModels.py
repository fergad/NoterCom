from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, create_engine
from datetime import datetime


class Update(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: Optional[str]
    date: Optional[datetime] = None
    status_change: Optional[str] = None

    task_id: Optional[int] = Field(default=None, foreign_key='task.id')
    question: Optional['Task'] = Relationship(back_populates="updates")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    comment: str
    body: Optional[str]
    start_date: datetime = Field(default_factory=datetime.now)

    updates: List['Update'] = Relationship(back_populates='question')
    status: str = Field(default="Created")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = None
    email: str = None
    password: str = None
    age: Optional[int] = None




