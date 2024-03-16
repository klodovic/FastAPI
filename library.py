from Model.Book import *
from Model.BookRequest import *
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

BOOKS = [
    Book(1, 'Computer science', 'Jonh Doe', 'Bestseller', 5, 2020),
    Book(2, 'Fast Api', 'Seve', 'Entry level', 2, 2015),
    Book(3, 'PHP', 'Let 3', 'Mid', 3, 2011),
    Book(4, 'C#', 'Agatha', 'Bestseller', 5, 2009),
    Book(5, 'Spring Boot', 'Pantic', 'Great', 4, 2023)
]

###End points###

#Get all books
@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS

#Get single book
@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def get_book(id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail='Book not found!')

#Get books by published date
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def get_books_by_publish_date(pub_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == pub_date:
            books_to_return.append(book)
    return books_to_return

#Create a new book
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(request: BookRequest):
    new_book = Book(**request.model_dump())
    BOOKS.append(find_book_id(new_book))

#Fetch books by rating
@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0, lt=6)):
    books_by_rating = []
    for book in BOOKS:
        if book.rating == rating:
            books_by_rating.append(book)
    return books_by_rating

#Update the book
@app.put("/books/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(request: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == request.id:
            BOOKS[i] = request
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')

#Delete book
@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')



#Methods
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book










