from pydantic import BaseModel

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    available: bool

    class Config:
        orm_mode = True
