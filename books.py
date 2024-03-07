from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Zebra", "author":"Benn Hill", "category": "science"},
    {"title": "Ptica", "author":"Bill Astron", "category": "science"},
    {"title": "Hrana", "author":"Jen Pal", "category": "math"},
    {"title": "Tisina", "author":"Ivo Jima", "category": "math"},
    {"title": "Njiva", "author":"Cahtie Hill", "category": "math"},
    {"title": "Sela", "author":"Jen Pal", "category": "math"}
]

@app.get("/books") #get all the books from the list
async def getAllBooks():
    return BOOKS


@app.get("/books/{title}") #http://127.0.0.1:8000/books/njiva (get book by title)
async def getSingleBook(title: str):
    for book in BOOKS:
        if book.get('title').casefold() == title.casefold():
            return book



@app.get("/books/") #http://127.0.0.1:8000/books/?category=science (query with parameters)
async def category_by_query(category: str):
    books_to_return= []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return



@app.get("/books/{author}/") #http://127.0.0.1:8000/books/Jen%20Pal/?category=math (query author and category)
async def author_category_by_query(author: str, category: str):
    books_to_return= []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and \
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


#Create new book
@app.post("/books/create")
async def create(new_book=Body()):
    BOOKS.append(new_book)
    return 200


#Update book by title
@app.put("/books/update")
async def update_book(updated_book = Body()):
    print("usao sam")
    for i in range(len(BOOKS)):
        if updated_book.get('title').casefold() == BOOKS[i].get('title').casefold():
            BOOKS[i] = updated_book
    return 200


#Delete book by title
@app.delete("/books/delete/{title}")
async def detele_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == title.casefold():
            BOOKS.pop(i)
    return 200

