
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, or_

#from app.db.Tables.TasksCRUD import create_update
#from app.db.Tables.TasksCRUD import create_multiply_tasks, create_task, create_multiply_updates, get_task_by_id, \
#    get_tasks_by_status, TaskStatus, get_all_quited
#from app.db.Tables.TasksCRUD import get_tasks_by_status, TaskStatus

#from app.db.AuthHttpBasic import get_current_username

from app.db.Get_db_engine import get_db
from app.db.Schemas import UpdateCreate, TaskCreate, TaskRead, TaskReadWithUpdates, TaskStatus, UpdateRead
from app.db.TablesModels import Task, Update


from fastapi import Cookie
from app.db.AuthJWT import oauth2_scheme, get_auth_from_token_no_validation
from app.db.UsersCRUD import is_user_ok#, get_author_no_security_check

router = APIRouter(
    prefix="/api/v1/n",
    tags=['api notes'],
    #dependencies=[Depends(get_current_username)],#AuthHttpBasc
    #dependencies=[Depends(get_data_from_token)]
    #dependencies=[Depends(get_from_cookie_token)]
    dependencies=[Depends(is_user_ok)]
  )



@router.post('/create_note')#, response_model=TaskRead)  # , dependencies=[Depends(JWTBearer())])
def api_create_new_note(note: TaskCreate,
                         access_token = Cookie(default=None, include_in_schema=False),
                        auth: str | None = None,
                         db: Session = Depends(get_db)): #auth = Depends(JWTBearer())):
    if auth is None:
        if access_token:
            auth = get_auth_from_token_no_validation(access_token)
        else: raise HTTPException(status_code=404, detai='No author info provided')

    r = Task.from_orm(note)  # , start_date=datetime.now())
    r.author = auth

    #print(JWTBearer.decodeJWT(auth))
    #r.author = JWTBearer.decodeJWT(auth)['user_id']
    db.add(r)
    db.commit()
    db.refresh(r)
    print('r from api_create_new_note= ', r)
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")






@router.post('/create_update/', response_model=UpdateRead)  # , dependencies=[Depends(JWTBearer())])
def api_create_update(update: UpdateCreate, access_token=Cookie(default=None, include_in_schema=False),
                      auth : str|None = None,
                      task_id: int | None = None, db: Session = Depends(get_db)):
    if auth is None:
        if access_token:
            auth = get_auth_from_token_no_validation(access_token)
        else : raise HTTPException(status_code=404, detai='No author info provided')

    if not update.task_id:
        if task_id:
            update.task_id=task_id
        else:
            raise HTTPException(status_code=404, detail="No no no task id")

    u = Update.from_orm(update)  # , start_date=datetime.now())
    print("u for now: ", u)
    t = db.exec(select(Task).where(Task.id==u.task_id)).first()
    u.author = auth
    if t.executor:
        if auth not in t.executor:
            t.executor += auth
    else:
        t.executor=auth
    print("Task: ", t)
    print("Update: ", u)

    if not t:
        raise HTTPException(status_code=404, detail="Item not found")
    t.status = u.status_change
    print("WE ARE HERE AND NO PROBLEMS")
    db.add(t)
    db.add(u)
    print(" t and u added AND NO PROBLEMS")
    db.commit()
    return u



@router.get('/id/{id}', response_model=TaskReadWithUpdates)
def api_get_note_by_id_with_updates(id: int, db: Session = Depends(get_db)):
    statement = select(Task).where(Task.id == id)
    r = db.exec(statement).first()
    if not r:
        raise HTTPException(status_code=404, detail="Item not found")
    return r


@router.get('/bank', response_model=List[TaskRead], status_code=200)
def api_get_opened_notes(db: Session = Depends(get_db)):
    print("and now try to get notes_bank")
    r = get_tasks_by_status(db=db, status=TaskStatus.created)
    print("r",r)
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get('/inwork')
def api_get_inwork_notes(db: Session = Depends(get_db)):
    r = get_tasks_by_status(db=db, status=TaskStatus.in_work)
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get('/done')
def api_get_done_notes(db: Session = Depends(get_db)):
    r = get_tasks_by_status(db=db, status=TaskStatus.done)
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get('/quited')
def api_all_quited_notes(db: Session = Depends(get_db)):
    r = get_all_quited(db=db, status=TaskStatus.quit_status_list())
    if r:
        return r
    else:
        raise HTTPException(status_code=404, detail="Item not found")


def get_tasks_by_status(db: Session = Depends(get_db), status=TaskStatus.created):
    print(db)
    r = db.exec(select(Task).where(Task.status == status)).all()
    return r


def get_all_quited(db: Session = Depends(get_db)):
    try:
        r = db.exec(select(Task).where(or_(*[Task.status == s for s in TaskStatus.quit_status_list()]))).all()
        return r
    except Exception as err:
        print(err)
        return err



@router.post("/fill-light")
def api_fill_lite(db: Session = Depends(get_db)):

    t1 = Task(title="Помыть посуду", body='посуда в раковине', author="Leslie")
    db.add(t1)
    t2 = Task(title="Съесть пироженые", body='Они могут испортится!', author="Freeze")
    t2.updates.append(Update(title='Принялся за дело', body='Их очень много, не смогу справится за раз. Съел 3 из 5',
                             status_change=TaskStatus.in_work, author="Freeze"))
    t2.status = t2.updates[-1].status_change
    t2.executor = 'Freeze'
    db.add(t2)
    t3 = Task(title="Заварить чаю", body='Кончилась заварка', author="Awesome")
    t3.updates.append(Update(title='Заварила новую', body='Ричард, от ОА',
                             status_change=TaskStatus.done, author="Leslie"))
    t3.status = t3.updates[-1].status_change
    t3.executor = "Leslie"
    db.add(t3)
    db.commit()
    db.refresh(t1)
    db.refresh(t2)
    db.refresh(t3)
    return t1,t2,t3


