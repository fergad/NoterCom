import datetime
from typing import Optional, List
from sqlmodel import  SQLModel

class Update_create(SQLModel):
    title: str
    body: Optional[str]
    date: Optional[int]
    status_change:str
    task_id: int

class Task_create_model(SQLModel):
    title: str
    comment: str
    body: Optional[str]

class Create_User(SQLModel):
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


class Read_user_list(SQLModel):
    name: str
    age: Optional[int] = None




##############
class Update_create_prepare(SQLModel):
    title: str
    body: Optional[str]
    date: Optional[int]
    status_change:str

'''class Update_create_prepare(SQLModel):
    title: str
    body: Optional[str]
    date: int = datetime.datetime.now().timestamp()
    status_change: Optional[str] = None'''
