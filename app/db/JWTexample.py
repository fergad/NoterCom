from app.db.Tables.Schemas import UserLoginSchema
from typing import Dict
import time

# The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from decouple import config


class JWTBearer(HTTPBearer):
    JWT_SECRET = config("secret")  #
    JWT_ALGORITHM = config("algorithm")

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def token_response(token: str):
        return {
            "access_token": token
        }

    # function used for signing the JWT string
    @staticmethod
    def signJWT(user_id: str) -> Dict[str, str]:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 600
        }
        token = jwt.encode(payload, JWTBearer.JWT_SECRET, algorithm=JWTBearer.JWT_ALGORITHM)
        return JWTBearer.token_response(token)

    @staticmethod
    def decodeJWT(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWTBearer.JWT_SECRET, algorithms=[JWTBearer.JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = JWTBearer.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid



