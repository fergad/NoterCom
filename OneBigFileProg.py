from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import Session, create_engine, select

import uvicorn
from fastapi import FastAPI

from typing import List, Optional

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path


class Update(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: Optional[str]
    date: Optional[int] = None
    status_change: Optional[str] = None


    task_id: Optional[int]  = Field(default=None, foreign_key='task.id')
    question: Optional['Task'] = Relationship(back_populates="updates")


class Task(SQLModel, table=True):
    @property
    def get_status(self):
        if self.updates:
            return self.updates[-1].status_change
        else:
            return 'Created'
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    comment: str
    body: Optional[str]
    start_date: Optional[int] = None
    updates: List['Update'] = Relationship(back_populates='question')#not task_id, but question
    #status: str = "Opened"
    status: str = get_status

    @property
    def status(self):
        if self.updates:
            return self.updates[-1].status_change
        else:
            return 'Created'


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]= None
    email: Optional[str]= None
    password: Optional[str]= None
    age: Optional[int] = None


#first = User(name="First", email='first@x.com', password='123456', age=31)

class Create_User(SQLModel):
    name: str
    email: str
    password: str
    age: Optional[int] = None

class Read_user_list(SQLModel):
    name: str
    age: Optional[int] = None


class Post(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str
    #password_for_edit: str
    date: Optional[int] = None #change to date format


engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)



def fill_db():
    users = []
    first = User(name="First", email='first@x.com', password='123456', age=31)
    users.append(first)
    users.append(User(name='Second', email='second@x.com', password='223456', age=32))
    users.append(User(name='Third', email='third@x.com', password='323456', age=33))
    users.append(User(name='Second', email='fourth@x.com', password='423456', age=34))
    users.append(User(name='Second', email='fifth@x.com', password='523456', age=35))



    with Session(engine) as session:
        for u in users:
            session.add(u)
        session.commit()

app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount('/static', StaticFiles(directory=os.path.join(current_dir, 'static')), name='static')

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "static")), name="static")

@app.get("/fill_db", tags=['test'], )
def fill_empty_db():
    fill_db()
    return('do what i can')

@app.get("/get_task")
def get_task():
    with Session(engine) as ses:
        first_tasks = ses.exec(select(Task)).first()
        all_updates = ses.exec(select(Update)).all()
        return {"tasks":first_tasks,"status":first_tasks.status, "all_updates": all_updates, }

@app.get('/create_test_task')
def test_task():
    task1 = Task(title="Do the dishes!",
                 comment="Some one must do the dishes",
                 body="ASAP PLEASE",
    )

    task1.updates.append(
        Update(title="I'll do it!", body="you will own me!", status_change="Done")
    )
    with Session(engine) as ses:
        ses.add(task1)
        ses.commit()
        ses.refresh(task1)

        print(task1)
        print(task1.updates)
        #print(task1.updates.status_change)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000 )

