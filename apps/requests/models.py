from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from apps.database import Base
from sqlalchemy.sql import func

class BookRequest(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    status = Column(String, default="pending", nullable=False)
    requested_at = Column(DateTime, server_default=func.now(), nullable=False)
    returned_at = Column(DateTime, nullable=True)


