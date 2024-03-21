from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, Query, APIRouter
import models
from models import ToDo
from Model.ToDoRequest import *
from database import engine, SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]



@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: Session = Depends(get_db)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')

    return db.query(ToDo).all()


@router.delete("/todo/{id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, db: Session = Depends(get_db), id: int= Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo_model = db.query(ToDo).filter(ToDo.id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.query(ToDo).filter(ToDo.id == id).delete()
    db.commit()

    return HTTPException(status_code=200, detail='Deleted', headers='')




