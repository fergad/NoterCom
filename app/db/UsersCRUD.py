import uuid
import logging
print("UsersCRUD begin")

import datetime

from sqlmodel import Session, select
from app.db.TablesModels import User,RefreshToken
from app.db.Schemas import CreateUser, UserLoginSchema, TokenDataValidated
from app.db.AuthJWT import get_password_hash, verify_password, create_access_token, validate_access_token


from fastapi import HTTPException, Cookie, Depends, Response, status
from app.db.Get_db_engine import get_db
import logging


def is_user_ok(response: Response,
               access_token=Cookie(include_in_schema=False),
               refresh_token=Cookie(include_in_schema=False),
               db: Session= Depends(get_db)) -> Response | bool:
    access_token_data = validate_access_token(access_token=access_token)
    if access_token_data.expired:
        db_refresh_token_data = db.exec(select(RefreshToken).where(RefreshToken.client_id == access_token_data.client_id)).first()
        print('check refresh with db_refersh: ', refresh_token,'==',db_refresh_token_data.token)
        if refresh_token==db_refresh_token_data.token:
            new_access_token = create_access_token({'sub': access_token_data.username, 'client_id': access_token_data.client_id})
            db_refresh_token_data.token = uuid.uuid4().hex
            db_refresh_token_data.date = datetime.datetime.now()
            db.add(db_refresh_token_data)
            db.commit()
            response.set_cookie(key='access_token', value=new_access_token, httponly=True)
            response.set_cookie(key='refresh_token', value=db_refresh_token_data, httponly=True)
            print('"Is user ok" end. Cookie set')
            return response
        print('refresh token validate FAIL:', refresh_token, '!=', db_refresh_token_data.token)
        raise HTTPException(403, detail="Forbidden for you")
    print("is_user_ok_says: USER_OK")
    return True


def get_author_no_security_check(access_token = Cookie(include_in_schema=False)) -> str:
    token_data = validate_access_token(access_token=access_token)
    print('get_author_no_security_check return author:', token_data.username)
    return token_data.username


def get_user_from_db(user_pointer: str | int, db: Session) -> User:
    if type(user_pointer) == str:
        result = db.exec(select(User).where(User.email == user_pointer)).first()
        print("Take user from db by login: ", result)
    else:
        result = db.exec(select(User).where(User.id == user_pointer)).first()
        print("Take user from db by id: ", result)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
    #return {'login': result.email, 'password':result.hashed_password}


def create_user(user: CreateUser, db: Session) -> User:
    new_user = User.from_orm(user)
    new_user.hashed_password = get_password_hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session) -> dict[User, list[str | None]]:
    elem = User
    statement = select(elem)  #.where(User.name == "Spider-Boy")
    result = db.exec(statement).all()
    cl=[]
    for e in result:
        cl.append(e.clients)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result, cl


def delete_user(user_id: int, db: Session) -> User:
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Item not found")
    target_user.delete(synchronize_session=False)
    db.commit()
    return target_user


def create_refresh_token(user_id: str, client_id: str, db: Session = Depends(get_db)):
    token = uuid.uuid4().hex
    refresh_token = RefreshToken(client_id=client_id, user_id=user_id, token=token)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token.token



'''
def update_refresh_token(client_id:str, user_id, db: Session = Depends(get_db)):
    token = uuid.uuid4().hex
    print("generate new refresh token", token)
    #refresh_token = RefreshToken(client_id=client_id, user_id=user_id, token=token)
    refresh_token = db.exec(select(RefreshToken).where(RefreshToken.client_id==client_id)).first()
    print('get refresh token from db for update:',refresh_token)
    refresh_token.token = token
    refresh_token.date = datetime.datetime.now()
    print('Now refresh token:', refresh_token)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    print('gonna retrurn refresh token', refresh_token)
    return refresh_token.token


def get_refresh_token_from_db(username:str, db:Session = Depends(get_db)):
    r = db.exec(select(User).where(User.name==username)).first()
    if r:
        return User.refresh_token
    return None
'''