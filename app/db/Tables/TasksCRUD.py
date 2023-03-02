print("TaskCRUD begin")

from datetime import datetime
from typing import List
from sqlmodel import Session, select, or_
from fastapi import Depends


from app.db.Tables.TablesModels import Task, Update
from app.db.Tables.Schemas import Task_create_model, Update_create
from app.db.Get_db_engine import engine


class TaskStatus:
    created = "Created"
    in_work = "in work"
    done = "Done"
    merged = "Merged"
    canceled = "Canceled"

    @classmethod
    def quit_status_list(cls):
        return [cls.done, cls.merged, cls.canceled]


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def create_task(task_param: Task_create_model):
    if not True:
        return "NOOOOO"
    try:
        with Session(engine) as session:
            t = Task(**task_param.dict(), start_date=datetime.now())
            session.add(t)
            session.commit()
            return t.id
    except Exception as err:
        return err


def create_update(upd: Update_create):  # , db: Session = Depends(get_db)):
    # db = Session(engine)
    data = upd.dict()
    try:
        with Session(engine) as db:
            u = Update(**data, data=datetime.now())
            task = db.exec(select(Task).where(Task.id == u.task_id)).first()
            task.updates.append(u)
            task.status = u.status_change
            db.add(task)
            db.commit()
        return
    except Exception as err:
        print(err)
        return err


def get_task_by_id(t_id: int, updates=True) -> tuple | Exception:
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.id == t_id)
            r = session.exec(statement).first()
            if updates:
                upd = r.updates
                return r, upd  # return r, upd
            return (r, [])
    except Exception as err:
        print(err)
        return err


def get_tasks_by_status(status=TaskStatus.created):
    try:
        with Session(engine) as session:
            r = session.exec(select(Task).where(Task.status == status)).all()
        return r
    except Exception as err:
        print(err)
        return err


def get_all_quited():
    try:
        with Session(engine) as session:
            r = session.exec(select(Task).where(or_(*[Task.status == s for s in TaskStatus.quit_status_list()]))).all()
        return r
    except Exception as err:
        print(err)
        return err


def create_multiply_tasks(tasks: List[Task_create_model]):  # , db:Session = Depends(get_db)):
    db = Session(engine)
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


def create_multiply_updates(upds: List[Update_create], db: Session = Depends(get_db)):
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


def create_multiply_updates_with_runtime_tasks(upds: List[Update_create], db: Session = Depends(get_db)):
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


def ADMIN_DELETE_ENTITY(entity, search_field, search_value, delete=False):
    with Session(engine) as session:
        target = select(entity).where(search_field == search_value)
        result = session.exec(target).first()
        if result and delete:
            session.delete(result)
            session.commit()
            return "Result: ", result, "by request: ", target, "Deleted"
        else:
            return result
