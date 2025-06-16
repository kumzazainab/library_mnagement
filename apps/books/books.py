from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.books.models import Book
from apps.books.schemas.request import BookCreate, BookUpdate
from apps.books.schemas.response import BookOut
from apps.tokens import create_access_token, get_current_user
from apps.users.models import User
from apps.dependencies import admin_only

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/create", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    books = db.query(Book).all()
    return books


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/update/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/delete/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
