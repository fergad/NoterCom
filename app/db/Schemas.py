from typing import Optional, List
from sqlmodel import SQLModel
from datetime import datetime
from app.db.TablesModels import User



class RefreshToken(SQLModel):
    client_id: str
    user_id: User
    token: str




class Token(SQLModel):
    access_token: str
    token_type: str


class TokenDataValidated(SQLModel):
    username: str #| None = None
    client_id: str #| None = None
    #exp: str #| None = None
    expired: bool #| None = None


class UpdateCreate(SQLModel):
    title: str
    body: Optional[str]
    status_change: str
    task_id: int | None = None

class UpdateRead(UpdateCreate):
    date: Optional[datetime]

class TaskCreate(SQLModel):
    title: str
    body: Optional[str]
    #status: Optional[str]

class TaskRead(TaskCreate):
    id: int
    author: str|None = None
    executor: str | None = None

class TaskReadWithUpdates(TaskRead):
    updates: List[UpdateRead] = []


class CreateUser(SQLModel):
    name: str
    email: str
    password: str
    age: Optional[int] = None

class UserOpenData(SQLModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    pass

class UserLoginSchema(SQLModel):
    name: str#EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                #"email": "abdulazeez@x.com",
                "name": "popug",
                "password": "weakpassword"
            }
        }


class ReadUser(SQLModel):
    name: str
    age: Optional[int] = None




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


class TaskStatus:
    created = "Created"
    in_work = "in work"
    done = "Done"
    merged = "Merged"
    canceled = "Canceled"

    @classmethod
    def quit_status_list(cls):
        return [cls.done, cls.merged, cls.canceled]

class UserFull(User):
    pass