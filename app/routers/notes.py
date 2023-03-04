from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

#from app.db.Tables.TasksCRUD import create_update
#from app.db.Tables.TasksCRUD import create_multiply_tasks, create_task, create_multiply_updates, get_task_by_id, \
#    get_tasks_by_status, TaskStatus, get_all_quited
from app.db.Get_db_engine import get_db
from app.db.Tables.TasksCRUD import get_tasks_by_status, TaskStatus

from app.db.Tables.Schemas import UpdateCreate, TaskCreate, ReadTaskWithUpdates
from app.db.Tables.TablesModels import Task
from app.db.JWTexample import JWTBearer

router = APIRouter(
    prefix="/av1/n",
    tags=['api notes'],
    #dependencies=[Depends(JWTBearer())],

  )
'''
@router.get('/id/{id}')
def a1_get_note_by_id_with_updates(id: int, db: Session = Depends(get_db)):
    r = get_task_by_id(id, db=db, updates=True)
    return {'note': r[0], 'updates': r[1]}
'''
@router.get('/id/{id}', response_model=ReadTaskWithUpdates)
def a1_get_note_by_id_with_updates(id: int, db: Session = Depends(get_db)):
        statement = select(Task).where(Task.id == id)
        r = db.exec(statement).first()
        if not r:
            raise HTTPException(status_code=404, detail="Item not found")
        return r


@router.get('/bank')
def a1_get_opened_notes(db: Session = Depends(get_db)):
    r = get_tasks_by_status(db=db, status=TaskStatus.created)
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get('/inwork')
def a1_get_opened_notes(db: Session = Depends(get_db)):
    r = get_tasks_by_status(db=db, status=TaskStatus.in_work)
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get('/done')
def a1_get_opened_notes(db: Session = Depends(get_db)):
    r = get_tasks_by_status(db=db, status=TaskStatus.done)
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get('/quited')
def a1_all_quited_notes(db: Session = Depends(get_db)):
    r = get_tasks_by_status(db=db, status=TaskStatus.quit_status_list())
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post('/create_note')  # , dependencies=[Depends(JWTBearer())])
def a1_create_new_note(note: TaskCreate, db: Session = Depends(get_db)):
    r = Task(note.from_orm())  # , start_date=datetime.now())
    db.add(r)
    db.commit()
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/fill-notes")
def api_fill_notes(db: Session = Depends(get_db)):
    tasks = [TaskCreate(title="First testing record", comment='put it first', body='just for testing'),
             TaskCreate(title="Do the dishes", comment='today', body='if it had to be me, i will be very angry'),
             TaskCreate(title="Do homework", comment='becouse i have to', body='i will do it by myself'),
             TaskCreate(title="Wash the car", comment='until 2024', body='car should be clean'),
             TaskCreate(**{
                 "title": "One more quest for my heroes",
                 "comment": "Who are my heroes?",
                 "status": "Opened",
                 # "id": 5,
                 "body": "If no one comes, then i come to you"
             }), TaskCreate(title="Get salary", comment='need to find nearest bank', body='not tinkoff'),
             TaskCreate(title="FastAPI Lesson", comment='Ill be bisy at wendsday',
                        body='will learn something new!'),
             TaskCreate(title="Take bottles to woodhouse", comment='its getting warmer',
                        body='may be take someone with me?'),
             TaskCreate(title="Check check engine light", comment='really need cable to look up for errors',
                        body='')]

    for t in tasks:
        db.add(t)

    upds = [UpdateCreate(title='No need to do it', body='even I have what to do ', status_change='closed', task_id=1),
            UpdateCreate(title='I will do it', body='It pleasure to help you', status_change='in work', task_id=1),
            UpdateCreate(title='There are too many!!!', body='Save good memory!!!!', status_change='in work',
                         task_id=2),
            UpdateCreate(title='Already done', body="Was not too hard", status_change='Done', task_id=3)]


    for u in upds:
        db.add(u)

    db.commit()


    return {"result": "ok"}
