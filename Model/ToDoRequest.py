from pydantic import BaseModel, Field
from typing import Optional

class ToDoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length=100)
    priority: int = Field(gt= 0, lt=6)
    complete: bool

    class Config:
        json_schema_extra = {
            'example':{
                'title': 'A new Todo task',
                'description': 'A new description of the to do task',
                'priority': 5,
                'complete': False
            }
        }

