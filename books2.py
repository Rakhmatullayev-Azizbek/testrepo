from typing import Optional

from fastapi import FastAPI, Path,Query, Body
from pydantic import BaseModel, Field
app=FastAPI()

class Book:
    id: int
    published_date: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self,id,published_date, title,author,description,rating):
        self.id = id
        self.published_date=published_date
        self.title = title
        self.author = author
        self.description=description
        self.rating=rating

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="ID is not needed on create", default=None)
    published_date: int=Field(gt=1999, lt=2027)
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1, lt=6)

    model_config={
        "json_schema_extra":{
            "example":{
                "published_date": "2026",
                "title": "A new book",
                "author": "Coding with",
                "description": "A new description of a book",
                "rating": 5,
            }

        }
    }

BOOKS=[
    Book(1,2025,"Computer science", "codingwith","A very nice book", 3),
    Book(2,2012,"Pyhton","Angela Yu","really good course",5),
    Book(3,2023,"Elcetronic ", "John","A nice course", 4),
    Book(4,2005,"math","Yu"," good course",3),
    Book(5,2026,"Computer engineering", "the real one","A very nice course", 3),
    Book(6,2022,"pythics","Master","not bad",2),
]

BOOK_ID=[]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/publish/")
async def read_date_of_book(book_date: int=Query(gt=1989, lt=2027)):
    books_to_return=[]
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date==book_date:
            books_to_return.append(BOOKS[i])
            return books_to_return
    return None

# async def date(publish_date: int):
#     to_return=[]
#     for book in BOOKS:
#         if book.published_date==publish_date:
#             to_return.append(book)
#             return to_return
#     return None
#

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book=Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(add_id(new_book))

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
    return BOOKS[i]

@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int=Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break



@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            # BOOK_ID.append(book)
            return book
    return None


# @app.get("/books/{published_date}")
# async def get_book_by_date(published_date: int):
#     books_by_date=[]
#     for book in BOOKS:
#         if book.published_date==published_date:
#             books_by_date.append(book)
#             return books_by_date
#     return None
#









@app.get("/books/")
async def read_book_by_rating(book_rating: int=Query(gt=-1, lt=6)):
    books_to_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return

# def find_book_id(book: Book):
#     if len(BOOKS)>0:
#         book.id=BOOKS[-1].id+1
#     else:
#         book.id=1
#     return


def add_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book



