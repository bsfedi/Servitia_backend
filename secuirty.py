import functools
from fastapi import  Request, Response, status,HTTPException,Depends
import jwt
# from main import app
from database import db
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

SECRET_KEY="M$iY#u$Fn9r=avs$n9$iY#u$F$iY#u$Fn9r=avsn9r=avsn9r=ar=a6n9r=a$iY#u$Fn9Mn9r=amn9r=aOo0n9r=a)#"
JWT_SECRET = "mysecretkey"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt



async def token_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")
    if not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload


def generate_jwt(uid):
    expiration_date = datetime.utcnow() + timedelta(days=120)
    token = jwt.encode({'exp': expiration_date, 'uid': uid}, SECRET_KEY, 'HS256')
    return token