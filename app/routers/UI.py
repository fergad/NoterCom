from typing import Optional

from fastapi import Depends, Request, Form, status, APIRouter, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import Session

from app.db.Get_db_engine import get_db
from app.settings import templates_dir, host_addr# DIRTY HACK

from app.db.Schemas import UpdateCreate, TaskReadWithUpdates, TaskStatus, TaskCreate, UserLoginSchema
from app.routers.notes import api_create_new_note, api_create_update, api_get_note_by_id_with_updates, \
    get_tasks_by_status, get_all_quited

from app.routers.users import api_login

from app.db.AuthJWT import get_auth_from_token_no_validation, validate_access_token

templates = Jinja2Templates(templates_dir)
print(">>>>>", templates_dir)

router = APIRouter(
    prefix="/notes",
    tags=['UI notes'],
    dependencies=[Depends(validate_access_token)]
)

router_without_auth = APIRouter(
    prefix="/notes",
    tags=['UI notes'],
)

@router_without_auth.get('/login')
def login_UI_form(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request, "send_data_to": "/notes/login"})

@router_without_auth.post('/login')
def login_from_UI_handler(request: Request, response: Response, login: str = Form(...), password: str = Form(...),
                          db=Depends(get_db)):

    user_login_data = UserLoginSchema(email=login, password=password)
    print("try to get user")
    #r = user_login(response=response, user = user_login_data, db=db)
    r = api_login(response=response, user_data = user_login_data, db=db)
    if r:
        response = templates.TemplateResponse("login_success.html", {"request": request, "send_data_to": "/notes/login"})
        #response.delete_cookie(key='access_token', httponly=True)
        response.set_cookie(key='access_token', value=r['access_token'], httponly=True)
        response.set_cookie(key='refresh_token', value=r['refresh_token'], httponly=True)
        print("token must be set as ", r['access_token'])
        return response




@router.get("/add", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def add_new_note(request: Request):
    return templates.TemplateResponse("create_note.html", {"request": request, "send_data_to": "/notes/add"})


@router.post("/add", response_class=RedirectResponse)
def add_note(request: Request, title: str = Form(...), body: str = Form(...),
             db=Depends(get_db), access_token = Cookie(include_in_schema=False)):
    auth_name = get_auth_from_token_no_validation(access_token)
    print("HER")
    n = TaskCreate(title=title, body=body)#, author=JWTBearer.decodeJWT(auth))
    try:
        r = api_create_new_note(note=n, auth=auth_name, db=db) #auth_name
    except Exception as err:
        print("THIS ERR",err)
        raise err
    return RedirectResponse(f'{host_addr}/notes/i/{r.id}', status_code=status.HTTP_303_SEE_OTHER)


@router.get("/i/{id}", response_class=HTMLResponse, name='note_by_id', response_model=TaskReadWithUpdates)
def show_note_by_id(request: Request, id: int, db=Depends(get_db)):
    # r= db.exec(select(Task).where(Task.id == id)).first()
    r = api_get_note_by_id_with_updates(id=id, db=db)
    return templates.TemplateResponse("note_by_id.html", {"request": request, "note": r})


@router.get("/b", response_class=HTMLResponse)
def notes_for_pick(request: Request, db: Session = Depends(get_db)):
    notes = get_tasks_by_status(db, TaskStatus.created)
    if notes:
        return templates.TemplateResponse("notes_show_category_simple_version.html",
                                      {"request": request, "notes": notes, "url_for_notes": host_addr + "/notes/i/"})
    else:
        return RedirectResponse(f'{host_addr}/notes/add', status_code=status.HTTP_303_SEE_OTHER)


@router.get("/w", response_class=HTMLResponse)
def notes_in_work(request: Request, db: Session = Depends(get_db)):
    notes = get_tasks_by_status(db, status=TaskStatus.in_work)

    if notes:
        return templates.TemplateResponse("notes_show_category_simple_version.html",
                                          {"request": request, "notes": notes, "url_for_notes": host_addr + "/notes/i/"})
    else:
        return RedirectResponse(f'{host_addr}/notes/add', status_code=status.HTTP_303_SEE_OTHER)


@router.get("/e", response_class=HTMLResponse)
def notes_closed(request: Request, db: Session = Depends(get_db)):
    notes = get_tasks_by_status(db, status=TaskStatus.done)

    if notes:
        return templates.TemplateResponse("notes_show_category_simple_version.html",
                                      {"request": request, "notes": notes, "url_for_notes": host_addr + "/notes/i/"})
    else:
        return RedirectResponse(f'{host_addr}/notes/add', status_code=status.HTTP_303_SEE_OTHER)


@router.get("/q", response_class=HTMLResponse)
def notes_closed(request: Request, db: Session = Depends(get_db)):
    notes = get_all_quited(db)
    if notes:
        return templates.TemplateResponse("notes_show_category_simple_version.html",
                                      {"request": request, "notes": notes, "url_for_notes": host_addr + "/notes/i/"})
    else:
        return RedirectResponse(f'{host_addr}/notes/add', status_code=status.HTTP_303_SEE_OTHER)

@router.post('/update_task')
def ui_create_update(task_id: int=Form(), title: str = Form(), body: str = Form(), new_status: str = Form(),
                     db: Session = Depends(get_db), access_token: str = Cookie(include_in_schema=False)):
    if new_status not in ['Created', 'in work', 'Done', 'Abandon']:
        raise HTTPException(status_code=404, detail="Wrong status")
    auth_name = get_auth_from_token_no_validation(access_token)
    print(task_id)
    new_update = UpdateCreate(task_id=task_id, title=title, body=body, status_change=new_status)
    r = api_create_update(new_update, auth=auth_name, db=db)
    return RedirectResponse(f'{host_addr}/notes/i/{task_id}', status_code=status.HTTP_303_SEE_OTHER)



@router.get('/update_task', response_class=HTMLResponse)
def ui_get_create_update_form(request: Request, task_id: Optional[int] = None):
    return templates.TemplateResponse("create_update.html",
                                      {"request": request, "task_id": task_id,
                                       "url_for_notes": host_addr + "/notes/" + str(task_id)})
