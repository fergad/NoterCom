print("TaskCRUD begin")

from datetime import datetime
from typing import List
from sqlmodel import Session, select, or_
from fastapi import Depends

from app.db.Tables.TablesModels import Task, Update
from app.db.Tables.Schemas import TaskCreate, UpdateCreate
from app.db.Get_db_engine import get_db

class TaskStatus:
    created = "Created"
    in_work = "in work"
    done = "Done"
    merged = "Merged"
    canceled = "Canceled"

    @classmethod
    def quit_status_list(cls):
        return [cls.done, cls.merged, cls.canceled]


def get_tasks_by_status(db:Session=Depends(get_db), status=TaskStatus.created):
    print(db)
    r = db.exec(select(Task).where(Task.status == status)).all()
    return r

def get_all_quited(db:Session=Depends(get_db)):
    try:
        r = db.exec(select(Task).where(or_(*[Task.status == s for s in TaskStatus.quit_status_list()]))).all()
        return r
    except Exception as err:
        print(err)
        return err


















#####  DELETE ALL FROM HERE #################################################


def create_task(task_param: TaskCreate, db:Session=Depends(get_db)) -> int:
    try:
        t = Task(**task_param.dict())#, start_date=datetime.now())
        db.add(t)
        db.commit()
        return t.id
    except Exception as err:
        print(err)
        return -1


def create_update(upd: UpdateCreate, db:Session=Depends(get_db)) :
    data = upd.dict()
    try:
        u = Update(**data, data=datetime.now())
        task = db.exec(select(Task).where(Task.id == u.task_id)).first()
        task.updates.append(u)
        task.status = u.status_change
        db.add(task)
        db.commit()
        db.refresh(u)
        return u
    except Exception as err:
        print(err)
        return -1


def get_task_by_id(t_id: int, db:Session=Depends(get_db), updates=True) -> tuple | Exception:
    try:
        statement = select(Task).where(Task.id == t_id)
        r = db.exec(statement).first()
        if updates:
            upd = r.updates
            return r, upd  # return r, upd
        return (r, [])
    except Exception as err:
        print(err)
        return err







def get_all_quited(db:Session=Depends(get_db)):
    try:
        r = db.exec(select(Task).where(or_(*[Task.status == s for s in TaskStatus.quit_status_list()]))).all()
        return r
    except Exception as err:
        print(err)
        return err


def create_multiply_tasks(*,db:Session=Depends(get_db), tasks: List[TaskCreate]):
    tasks_count_added = 0
    try:
        for elem in tasks:
            data = elem.dict()
            print(data)
            t = Task(**data, start_date=datetime.now())
            db.add(t)
            tasks_count_added += 1
        db.commit()
        print(f'added {tasks_count_added} records')
        return tasks_count_added
    except Exception as err:
        print(err)
        return err


def create_multiply_updates(upds: List[UpdateCreate], db:Session=Depends(get_db)):
    updates_assigned = 0
    try:
        for elem in upds:
            data = elem.dict()
            u = Update(**data)
            db.add(u)
            updates_assigned += 1
        db.commit()
        return updates_assigned
    except Exception as err:
        return err


def create_multiply_updates_with_runtime_tasks(upds: List[UpdateCreate], db:Session=Depends(get_db)):
    updates_assigned = 0
    try:
        for elem in upds:
            data = elem.dict()
            u = Update(**data)
            db.add(u)
            updates_assigned += 1
        db.commit()
        return updates_assigned
    except Exception as err:
        return err


def ADMIN_DELETE_ENTITY(*,db:Session=Depends(get_db), entity, search_field, search_value, delete=False):
    target = select(entity).where(search_field == search_value)
    result = db.exec(target).first()
    if result and delete:
        db.delete(result)
        db.commit()
        return "Result: ", result, "by request: ", target, "Deleted"
    else:
        return result
