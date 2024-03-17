from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, Query, APIRouter
import models
from models import ToDo
from Model.ToDoRequest import *
from database import engine, SessionLocal
from starlette import status
from pydantic import BaseModel, Field



router = APIRouter(
    tags=['ToDo']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#get all Todos
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: Session = Depends(get_db)):
    return db.query(ToDo).all()



#get single Todo
@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def get_todo(id: int = Path(gt=0), db: Session = Depends(get_db)):
    todo = db.query(ToDo).filter(ToDo.id == id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail='Not found')


#create new Todo
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_new(request: ToDoRequest, db: Session = Depends(get_db)):
    todo = ToDo(**request.dict())
    db.add(todo)
    db.commit()
    return HTTPException(status_code=200, detail='Created', headers='')


#update Todo
@router.put("/todo/{id}", status_code=status.HTTP_200_OK)
async def update_todo(id: int, request: ToDoRequest, db: Session = Depends(get_db)):
    todo = db.query(ToDo).filter(ToDo.id == id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='Not found')

    todo.title = request.title
    todo.description = request.description
    todo.priority = request.priority
    todo.complite = request.complite

    db.add(todo)
    db.commit()
    return HTTPException(status_code=200, detail='Updated', headers='')


#delete todo
@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_todo(id:int = Path(gt=0), db: Session = Depends(get_db)):
    todo = db.query(ToDo).filter(ToDo.id == id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='Not found')

    db.query(ToDo).filter(ToDo.id == id).delete()
    db.commit()
    return HTTPException(status_code=200, detail='Deleted', headers='')





















