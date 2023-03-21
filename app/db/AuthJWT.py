from datetime import datetime, timedelta
import jose.exceptions
from fastapi import Depends,  HTTPException, status, Response, Cookie, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyCookie
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db.Schemas import TokenDataValidated
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

user_schema_example = {
    "johndoe": {
        "username": "popug",
        "email": "popug@x.com",
        "hashed_password": '$2b$12$4O6AGK1VAopb6oElcbMiWu0ffQNKB10xJ4N3ckAUCbciaDAlSZw8S',
        "age": 10,

        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
path_to_token_endpoint ='/api/v1/users'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=path_to_token_endpoint+"/token")

 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def validate_access_token(access_token: str | None = Cookie(alias='access_token', include_in_schema=False, default=None)
                          ) -> TokenDataValidated:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Visit login page",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print("get data from token=", access_token)

    if access_token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload: ", payload)
        username = payload.get('sub')
        client_id = payload.get('client_id')
        #exp = payload.get('exp')
        if username is None or client_id is None:
            raise credentials_exception
        token_data = TokenDataValidated(username=username, client_id=client_id, expired=False)
        print("token data=", token_data)
        return token_data
    except jose.exceptions.ExpiredSignatureError as err:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM], options={
            #"verify_signature": False,
            "verify_exp": False})
        token_data = TokenDataValidated(username=payload.get('sub'), client_id=payload.get('client_id'), expired=True)
        print('return expired token data')
        return token_data
    except JWTError:
        raise credentials_exception


def get_auth_from_token_no_validation(access_token):
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM], options={
        "verify_signature": False,
        "verify_exp": False})
    return payload.get('sub')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
