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
    tags=['ToDo']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]

# get all Todos
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(ToDo).filter(ToDo.owner_id == user.get('id')).all()



#get single Todo
@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, id: int = Path(gt=0), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo = db.query(ToDo).filter(ToDo.id == id).filter(ToDo.owner_id == user.get('id')).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail='Not found')


#create new Todo
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_new(request: ToDoRequest, user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo = ToDo(**request.dict(), owner_id = user.get('id'))
    db.add(todo)
    db.commit()
    return HTTPException(status_code=200, detail='Created', headers='')


#update Todo
@router.put("/todo/{id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency, request: ToDoRequest, id: int = Path(gt=0), db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    todo = db.query(ToDo).filter(ToDo.id == id).filter(ToDo.owner_id == user.get('id')).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='Not found')

    todo.title = request.title
    todo.description = request.description
    todo.priority = request.priority
    todo.complete = request.complete

    db.add(todo)
    db.commit()
    return HTTPException(status_code=200, detail='Updated', headers='')


#delete Todo
@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, id:int = Path(gt=0), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    todo = db.query(ToDo).filter(ToDo.id == id).filter(ToDo.owner_id == user.get('id')).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='Not found')

    db.query(ToDo).filter(ToDo.id == id).filter(ToDo.owner_id == user.get('id')).delete()
    db.commit()
    return HTTPException(status_code=200, detail='Deleted', headers='')





















