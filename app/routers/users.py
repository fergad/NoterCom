from db.JWTexample import JWTBearer
from fastapi import APIRouter, Body
from app.db.Tables.Schemas import CreateUser, ReadUserList, UserLoginSchema
from app.db.Tables.UsersCRUD import create_user, get_users, check_user
from typing import List
from app.db.JWTexample import JWTBearer

router = APIRouter(
    prefix="/api/users",
    tags=['users']
)


@router.get("/list", response_model=List[ReadUserList])
def get_users_list():
    return get_users()



@router.get('/testuser')
def check_user_security_data(token: str):
    data = JWTBearer.decodeJWT(token)
    result = JWTBearer.verify_jwt(token)
    return result, data
"""
@router.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user)  # replace with db call, making sure to hash the password first
    return JWTBearer.signJWT(user.email)
"""

@router.post("/signup")
def create_user_m(user: CreateUser):
    create_user(user)
    return JWTBearer.signJWT(user.email)




@router.post("/login")
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return JWTBearer.signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

"""
@router.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return JWTBearer.signJWT(user.email)
    return {"error": "Wrong login details!"}
"""
