import secrets

from fastapi import Depends, FastAPI, HTTPException, status, Request
from sqlmodel import Session, select
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.db.Get_db_engine import get_db
from app.db.TablesModels import User
#from app.db.Schemas import UserFull

import uvicorn
app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    print("TRY TO FIND USERNAME=", credentials.username)
    visitor = db.exec(select(User).where(User.email == credentials.username)).first()
    print("Find ", visitor)
    if visitor:
        if credentials.password == visitor.hashed_password:
            print("Gonna return ", credentials.username)
            return visitor.name

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def logout_user(credentials: HTTPBasicCredentials = Depends(security)):
    print("TRY TO FIND USERNAME=", credentials.username)
    credentials.username=''
    credentials.password=''
    return 'bye'
