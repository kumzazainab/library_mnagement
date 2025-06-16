from sqlalchemy import Column, String, Integer, Boolean
from apps.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True)
    available = Column(Boolean, default=True)
    borrow_days = Column(Integer, default=5, nullable=False)


