from fastapi import Depends, Request, Form, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from app.settings import templates_dir

from db.Tables.TasksCRUD import get_task_by_id, get_tasks_by_status, TaskStatus, create_task
from db.Tables.Schemas import Task_create_model

from fastapi.templating import Jinja2Templates
from datetime import datetime



templates = Jinja2Templates(templates_dir)
print(">>>>>",templates_dir)



router = APIRouter(
    prefix="/notes",
    tags=['UI notes']
)


#DIRTY HACK
server_url = "http://127.0.0.1:8000/notes/"


@router.get("/add", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def add_new_note(request: Request):
    return templates.TemplateResponse("create_note.html", {"request": request, "send_data_to": "/notes/add"})


@router.post("/add", response_class=RedirectResponse)
def add_note(request: Request, title: str = Form(...), comment: str = Form(...), body: str = Form(...)):#, db = Depends(get_db)):#, db = Depends(get_db)):
    #print(form.__dict__)
    n = Task_create_model(title=title, comment=comment, body=body)
    created_id=create_task(n)
    return RedirectResponse(f'http://127.0.0.1:8000/notes/i/{created_id}', status_code=status.HTTP_303_SEE_OTHER)


@router.get("/i/{id}", response_class=HTMLResponse, name='note_by_id',)  # , dependencies=[Depends(JWTBearer())]
def show_note_by_id(request: Request, id: int):
    note = get_task_by_id(id=id)
    if note:
        task = note[0]
        updates=note[1]
        return templates.TemplateResponse("note_by_id.html", {"request": request, "note": task, "updates":updates})


@router.get("/b", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def notes_for_pick(request: Request):
    notes = get_tasks_by_status(TaskStatus.created)
    #change url_for_notes in return;
    return templates.TemplateResponse("notes_show_category.html", {"request": request, "notes": notes, "url_for_notes":server_url+"i/"})


@router.get("/w", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def notes_in_work(request: Request):
    notes = get_tasks_by_status(status=TaskStatus.in_work)
    return templates.TemplateResponse("notes_show_category.html", {"request": request, "notes": notes,"url_for_notes":server_url+"i/"})


@router.get("/e", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def notes_closed(request: Request):
    notes = get_tasks_by_status(status=TaskStatus.done)
    return templates.TemplateResponse("notes_show_category.html", {"request": request, "notes": notes,"url_for_notes":server_url+"i/"})
