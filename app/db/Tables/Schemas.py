from typing import Optional, List
from sqlmodel import SQLModel


class UpdateCreate(SQLModel):
    title: str
    body: Optional[str]
    date: Optional[int]
    status_change: str
    task_id: int

class ReadUpdate(UpdateCreate):
    pass


class TaskCreate(SQLModel):
    title: str
    comment: str
    body: Optional[str]


class CreateUser(SQLModel):
    name: str
    email: str
    password: str
    age: Optional[int] = None


class UserLoginSchema(SQLModel):
    email: str#EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


class ReadUserList(SQLModel):
    name: str
    age: Optional[int] = None


class ReadTaskWithUpdates(TaskCreate):
    updates: List[ReadUpdate] = []

##############
class UpdateCreatePrepare(SQLModel):
    title: str
    body: Optional[str]
    date: Optional[int]
    status_change: str


'''class Update_create_prepare(SQLModel):
    title: str
    body: Optional[str]
    date: int = datetime.datetime.now().timestamp()
    status_change: Optional[str] = None'''
