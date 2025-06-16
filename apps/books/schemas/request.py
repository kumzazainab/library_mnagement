from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    available: bool | None = None
