from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, Query, APIRouter
import models
from models import ToDo, User
from Model.ToDoRequest import *
from Model.UserVerification import *
from database import engine, SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/user',
    tags=['User']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise  HTTPException(status_code=401, detail='Failed Authentnication', headers='')
    return  db.query(User).filter(User.id == user.get('id')).first()



@router.put("/password", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, user_verification: UserVerification, db: Session = Depends(get_db)):

    if user is None:
        raise  HTTPException(status_code=401, detail='Failed Authentnication', headers='')

    user_model = db.query(User).filter(User.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change', headers='')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    return HTTPException(status_code=200, detail='Password successfully changed', headers='')























