from fastapi import FastAPI, Depends, HTTPException, Path, Query, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from Model.CreateUserRequest import *
from Model.Token import *
from models import User
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import SessionLocal
from jose import jwt, JWTError
from datetime import timedelta, datetime


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

SECRET_KEY = 'fastApi'
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token') #decode


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.user_name == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if user_name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not valid user')
        return {'username': user_name, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not valid user')



#Register new user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(createUser: CreateUserRequest, db: Session = Depends(get_db)):

    new_user = User(
        email=createUser.email,
        user_name=createUser.user_name,
        first_name=createUser.first_name,
        last_name=createUser.last_name,
        role=createUser.role,
        hashed_password=bcrypt_context.hash(createUser.hashed_password),
        is_active=True
    )
    db.add(new_user)
    db.commit()
    return new_user


#Token
@router.post("/token", response_model=Token)
async def login_for_acces_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise  HTTPException(status_code=401, detail='Failed Authentnication', headers='')

    token = create_token(user.user_name, user.id, user.role,  timedelta(minutes=20))
    return  {'access_token': token, 'token_type': 'bearer'}
























