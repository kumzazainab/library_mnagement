from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from apps.database import Base

class BookReturn(Base):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    returned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    book = relationship("Book")
