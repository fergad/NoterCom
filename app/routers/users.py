from typing import List
from fastapi import APIRouter, Body, Depends, Response, Request, HTTPException, Cookie
from sqlmodel import Session
from app.db.Schemas import CreateUser, ReadUser, UserLoginSchema
from app.db.UsersCRUD import create_user, get_users,  get_user_from_db, create_refresh_token, is_user_ok
from uuid import uuid4
from app.db.Get_db_engine import get_db

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.db.AuthJWT import verify_password, create_access_token, validate_access_token
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/api/v1/users",
    tags=['users'],
    dependencies=[Depends(validate_access_token)]
)

router_without_auth = APIRouter(
    prefix="/api/v1/users",
    tags=['users'],
)


@router_without_auth.post('/login')
def api_login(response: Response, user_data:UserLoginSchema,
              access_token = Cookie(default=None, include_in_schema=False),
              refresh_token = Cookie(default=None, include_in_schema=False),
              db:Session=Depends(get_db)):
    if access_token and refresh_token:
        try:
            r = is_user_ok(response=response, access_token=access_token, refresh_token=refresh_token, db=db)
            return r
        except HTTPException as http_err:
            if http_err.status_code==403:
                pass
    r=get_user_from_db(user_data.name, db=db)
    if not r:
        raise HTTPException()
    client_id = uuid4()
    #scope = 'notes:read notes:write'

    client_id = str(uuid4())
    access_token = create_access_token({'sub': user_data.name, 'client_id': client_id})
    refresh_token = create_refresh_token(client_id=client_id, user_id=r.id, db=db)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post("/signup") #if user exist
def create_user_m(response: Response, user: CreateUser, db: Session = Depends(get_db)):
    r = create_user(user, db=db)
    print("User created:", r.name)
    client_id = str(uuid4())
    access_token = create_access_token({'sub': r.name, 'client_id': client_id})
    refresh_token = create_refresh_token(r.id, client_id, db=db)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
    return {"msg": "you have been registered! Welcome to login."}




@router.get("/list", response_model=None)
def get_users_list(db=Depends(get_db)):
    """__for develeop only. Delte or define response model__"""
    return get_users(db=db)


@router.get("/id/{id}", response_model=ReadUser)
def get_users_by_login(id: int, db=Depends(get_db)):
    return get_user_from_db(user_pointer=id, db=db)


@router_without_auth.get("/gh", tags=['Headers'])
def check_headers(response: Response, req: Request):
    return {"response H":response.headers, "Request H":req.headers}


@router_without_auth.post("/token")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    """Обработчик встроенной зеленой кнопки Authorize справа вверху"""
    print('we in the /token url')
    username = form_data.username
    password = form_data.password
    print('prepare to request db')
    r = get_user_from_db(username, db=db)
    print('after request db')
    if not r:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(password, r.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
    data={"sub": r.name}, expires_delta=access_token_expires
    )
    print('Before return')

    #response.set_cookie(key="access_token", value='Bearer '+access_token, httponly=True)
    response.co(key="access_token", value='Bearer '+access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

