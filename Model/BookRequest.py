from pydantic import BaseModel, Field
from typing import Optional


class BookRequest(BaseModel):
    id: Optional[int] = Field(None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt= 0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        json_schema_extra = {
            'example':{
                'title': 'A new book',
                'author': 'John Doe',
                'description': 'A new description of the book',
                'rating': 5,
                'published_date': 2029
            }
        }