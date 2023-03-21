from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, create_engine
from datetime import datetime


class BaseUpdate(SQLModel):
    title: str
    body: Optional[str]
    status_change: Optional[str] = None
    author: Optional[str] = None


class Update(BaseUpdate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[datetime] = Field(default_factory=datetime.now)

    task_id: Optional[int] = Field(default=None, foreign_key='task.id')
    question: Optional['Task'] = Relationship(back_populates="updates")


class BaseTask(SQLModel):
    title: str
    body: Optional[str]


class Task(BaseTask, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_date: datetime = Field(default_factory=datetime.now)
    author: Optional[str]
    executor: Optional[str] = None
    #weight: int = Field(default=0)

    updates: List['Update'] = Relationship(back_populates='question')
    status: str = Field(default="Created")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    email: str = Field(default=None, unique=True)
    hashed_password: str = None
    age: Optional[int] = None
    #refresh_token: str | None = None
    disabled: bool | None = None
    clients: List['RefreshToken'] = Relationship(back_populates='owner')


class RefreshToken(SQLModel, table=True):
    client_id: str = Field(primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    token: str = Field()
    date: Optional[datetime] = Field(default_factory=datetime.now)

    owner: User = Relationship(back_populates="clients")

