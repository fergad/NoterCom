from fastapi import APIRouter, Depends
from oldcode.SqModel import Task_create_model, Task, get_tasks_and_updates_by_id, get_tasks_by_status, \
    Update, Update_user_view, get_db, Session
import datetime
from typing import Union

router = APIRouter(
    prefix="/api/n",
    tags=['tasks']
)

@router.post("/create")  # , dependencies=[Depends(JWTBearer())]
def api_add_note(note: Task_create_model, db: Session = Depends(get_db)):
    #user.append(user.email)  # replace with db call, making sure to hash the password first
    #write_entitie(user)
    new_task = Task(**note.dict())      ###, start_date=datetime.datetime.now().timestamp())
    new_task.get_status()
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"data": "note created.", "note": new_task}

@router.post("/fill-tasks")
def api_fill_tasks(db = Depends(get_db)):
    tasks=[]
    tasks.append(Task(title="First testing record", comment='put it first', body='just for testing'))
    #tasks[-1].get_status()
    tasks.append(Task(title="Do the dishes", comment='today', body='if it had to be me, i will be very angry'))
    #tasks[-1].get_status()
    tasks.append(Task(title="Do homework", comment='becouse i have to', body='i will do it by myself'))
    #tasks[-1].get_status()
    tasks.append(Task(title="Wash the car", comment='until 2024', body='car should be clean'))
    #tasks[-1].get_status()
    tasks.append( Task( **{
      "title": "One more quest for my heroes",
      "comment": "Who are my heroes?",
      "status": "Opened",
      "id": 5,
      "body": "If no one comes, then i come to you"
    }))
    #tasks[-1].get_status()

    t = []
    u1=Update(title='I will do it', body='It pleasure to help you', status_change='in work')
    u2=Update(title='There are too many!!!', body='Save good memory!!!!', status_change='in work', task_id=1)
    u3=Update(title='Already done', body="Was not too hard", status_change='Done', task_id=3)

    tasks[1].updates.append(u1)
    tasks[1].get_status()
    tasks[1].updates.append(u2)
    tasks[1].get_status()
    tasks[3].updates.append(u3)
    tasks[3].get_status()
    for t in tasks:
        db.add(t)
    r = db.commit()
    return {"written tasks with id": r}




@router.get("/i/{id}")   # , dependencies=[Depends(JWTBearer())]
def api_note_for_pick(id:int):
    note, updates = get_tasks_and_updates_by_id(id=id)
    #filtred_updates= [up for up in updates for k,v in up.items() if k in Update_user_view.__fields__.keys()}]

    return { "note":note, 'updates':updates}



@router.get("/b", )  # , dependencies=[Depends(JWTBearer())]
def api_notes_for_pick():
    notes = get_tasks_by_status(status="Opened")
    return {"notes":notes}

@router.get("/w", )  # , dependencies=[Depends(JWTBearer())]
def api_notes_in_work():
    notes = get_tasks_by_status(status='in work')
    return {"notes":notes}

@router.get("/e", )  # , dependencies=[Depends(JWTBearer())]
def api_notes_closed():
    notes = get_tasks_by_status(status='Done')
    return {"notes":notes}

@router.get("/notes", )
def api_get_all_notes(db:Session = Depends(get_db)):                        # CRUSH /docs db = Depends(get_entities)):
    result = db.query(Task, Update).all()
    return {'data':result}
#SAWarning: SELECT statement has a cartesian product between FROM element(s) "task" and FROM element "update".  Apply join condition(s) between each element to resolve.
#  return super().execute(  # type: ignore

