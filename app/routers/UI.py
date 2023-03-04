from fastapi import Depends, Request, Form, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlmodel import Session, select
from fastapi import HTTPException
from app.db.Get_db_engine import get_db

from app.settings import templates_dir

from db.Tables.TasksCRUD import get_task_by_id, get_tasks_by_status, TaskStatus, create_task, get_all_quited
from db.Tables.Schemas import TaskCreate, ReadTaskWithUpdates

from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.routers.notes import a1_get_opened_notes
from app.db.Tables.TablesModels import Task


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
def add_note(request: Request, title: str = Form(...), comment: str = Form(...), body: str = Form(...), db = Depends(get_db)):#, db = Depends(get_db)):
    #print(form.__dict__)
    #n = TaskCreate(title=title, comment=comment, body=body)
    #created_id=create_task(n)
    n = Task(title=title, comment=comment, body=body)
    db.add(n)
    db.commit()
    db.refresh(n)
    return RedirectResponse(f'http://127.0.0.1:8000/notes/i/{n.id}', status_code=status.HTTP_303_SEE_OTHER)


@router.get("/i/{id}", response_class=HTMLResponse, name='note_by_id', response_model=ReadTaskWithUpdates)  # , dependencies=[Depends(JWTBearer())]
def show_note_by_id(request: Request, id: int, db = Depends(get_db)):
    statement = select(Task).where(Task.id == id)
    r = db.exec(statement).first()
    if not r:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("note_by_id.html", {"request": request, "note": r})


@router.get("/b", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def notes_for_pick(request: Request, db:Session = Depends(get_db)):
    notes = get_tasks_by_status(db, TaskStatus.created)
    #notes=a1_get_opened_notes(db=db)
    return templates.TemplateResponse("notes_show_category_simple_version.html", {"request": request, "notes": notes, "url_for_notes":server_url+"i/"})


@router.get("/w", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def notes_in_work(request: Request, db:Session = Depends(get_db)):
    notes = get_tasks_by_status(db, status=TaskStatus.in_work)
    return templates.TemplateResponse("notes_show_category_simple_version.html", {"request": request, "notes": notes,"url_for_notes":server_url+"i/"})


@router.get("/e", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def notes_closed(request: Request, db:Session = Depends(get_db)):
    notes = get_tasks_by_status(db, status=TaskStatus.done)
    return templates.TemplateResponse("notes_show_category_simple_version.html", {"request": request, "notes": notes,"url_for_notes":server_url+"i/"})

@router.get("/q", response_class=HTMLResponse)  # , dependencies=[Depends(JWTBearer())]
def notes_closed(request: Request, db:Session = Depends(get_db)):
    notes = get_all_quited(db)
    return templates.TemplateResponse("notes_show_category_simple_version.html", {"request": request, "notes": notes,"url_for_notes":server_url+"i/"})