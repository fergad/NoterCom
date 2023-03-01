import datetime
from typing import Optional
from sqlmodel import SQLModel
from sqlmodel import Session, create_engine, select
from db.Tables.TablesModels import Update, Task, User

class Update_user_view(SQLModel):
    title: str
    body: Optional[str]
    date: Optional[int]
    status_change:str

class Task_create_model(SQLModel):
    title: str
    comment: str
    body: Optional[str]



def create_task(task_param: Task_create_model):
    return Task(**task_param.dict())

def create_update_with_task_class(upd:Update_user_view, task:Task):
    update = Update(**upd.dict())
    if not update.date: update.date = datetime.datetime.now().timestamp()
    task.updates.append(update)
    task.status = update.status_change
    return update

def create_update_with_task_id(upd:Update, task_id:int):
    if not upd.date: upd.date = datetime.datetime.now().timestamp()
    data=upd.dict()
    return Update(**data, task_id=task_id)


def create_user(usr:User):
    return User(**usr.dict())






class Create_User(SQLModel):
    name: str
    email: str
    password: str
    age: Optional[int] = None

class Read_user_list(SQLModel):
    name: str
    age: Optional[int] = None


engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)



def get_tasks_and_updates_by_id(id=''):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == id)
        result = session.exec(statement).first()
        if result:
            return result, result.updates
        else:
            return

def get_tasks_by_status(status="Created"):
    with Session(engine) as session:
        statement = select(Task).where(Task.status == status)
        return session.exec(statement).all()

def get_users():
    #elem=User or elem=Post
    elem=User
    with Session(engine) as session:
        statement = select(elem)#.where(User.name == "Spider-Boy")
        return session.exec(statement).all()

def write_entitie(elem):
    with Session(engine) as session:
        session.add(elem)
        session.commit()

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def create_user(user: Create_User):
    db=Session(engine)
    db.add(User(**user.dict()))
    db.commit()

def delete_user(user_id: int):
    db=Session(engine)
    target_user = db.query(User).filter(User.id == user_id).first()

    if target_user == None:
        return -1

    target_user.delete(synchronize_session=False)
    db.commit()

    return 1



def get_task_info():
    with Session(engine) as ses:
        first_tasks = ses.exec(select(Task)).first()
        all_updates = ses.exec(select(Update)).all()
        return {"tasks":first_tasks,"status":first_tasks.status, "all_updates": all_updates, }
