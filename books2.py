from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
app=FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description=description
        self.rating=rating

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="ID is not needed on create", default=None)
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1, lt=6)

    model_config={
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "Codingwith",
                "description": "A new description of a book",
                "rating": 5,
            }

        }
    }

BOOKS=[
    Book(1,"Computer science", "codingwith","A very nice book", 3),
    Book(2,"Pyhton","Angela Yu","really good course",5),
    Book(3,"Elcetronic ", "John","A nice course", 4),
    Book(4,"math","Yu"," good course",1),
    Book(5,"Computer engineering", "the real one","A very nice course", 3),
    Book(6,"pythics","Master","not bad",2),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book=Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(add_id(new_book))

#
# def find_book_id(book: Book):
#     if len(BOOKS)>0:
#         book.id=BOOKS[-1].id+1
#     else:
#         book.id=1
#     return


def add_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book



