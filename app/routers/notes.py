from fastapi import APIRouter, Depends

from app.db.Tables.TasksCRUD import create_update

from app.db.Tables.TasksCRUD import create_multiply_tasks,create_task, create_multiply_updates, get_task_by_id,\
    get_tasks_by_status, TaskStatus, get_all_quited

from app.db.Tables.Schemas import Update_create, Task_create_model

from app.db.JWTexample import JWTBearer

router = APIRouter(
    prefix="/av1/n",
    tags=['api notes']
)


@router.get('/id/{id}')
def a1_get_note_by_id_with_updates(id:int):
    r = get_task_by_id(id, updates=True)
    return {'note': r[0], 'updates': r[1]}


@router.get('/bank')
def a1_get_opened_notes():
    r = get_tasks_by_status(status=TaskStatus.created)
    return {'notes': r}

@router.get('/inwork')
def a1_get_opened_notes():
    r = get_tasks_by_status(status =TaskStatus.in_work)
    return {'notes': r}

@router.get('/done')
def a1_get_opened_notes():
    r = get_tasks_by_status(status =TaskStatus.done)
    return {'notes': r}

@router.get('/quited')
def a1_all_quited_notes():
    r = get_all_quited()
    return r


@router.post('/create_note', dependencies=[Depends(JWTBearer())])
def a1_create_new_note(note: Task_create_model):
    r = create_task(note)
    return r































@router.post("/fill-notes")
def api_fill_notes():
    tasks=[]
    tasks.append(Task_create_model(title="First testing record", comment='put it first', body='just for testing'))
    tasks.append(Task_create_model(title="Do the dishes", comment='today', body='if it had to be me, i will be very angry'))
    tasks.append(Task_create_model(title="Do homework", comment='becouse i have to', body='i will do it by myself'))
    tasks.append(Task_create_model(title="Wash the car", comment='until 2024', body='car should be clean'))
    tasks.append( Task_create_model( **{
      "title": "One more quest for my heroes",
      "comment": "Who are my heroes?",
      "status": "Opened",
      #"id": 5,
      "body": "If no one comes, then i come to you"
    }))
    tasks.append(Task_create_model(title="Get salary", comment='need to find nearest bank', body='not tinkoff'))
    tasks.append(Task_create_model(title="FastAPI Lesson", comment='Ill be bisy at wendsday', body='will learn something new!'))
    tasks.append(Task_create_model(title="Take bottles to woodhouse", comment='its getting warmer', body='may be take someone with me?'))
    tasks.append(Task_create_model(title="Check check engine light", comment='really need cable to look up for errors', body=''))

    r = create_multiply_tasks(tasks)


    upds=[]
    upds.append(Update_create(title='No need to do it', body='even I have what to do ', status_change='closed', task_id=1))
    upds.append(Update_create(title='I will do it', body='It pleasure to help you', status_change='in work', task_id=1))
    upds.append(Update_create(title='There are too many!!!', body='Save good memory!!!!', status_change='in work',task_id=2))#, task_id=1)
    upds.append(Update_create(title='Already done', body="Was not too hard", status_change='Done', task_id=3))#, task_id=3)


    create_update(upds[0])


    create_update(upds[1])
    create_update(upds[2])

    create_update(upds[3])


    print(r)


    return {"result": r}