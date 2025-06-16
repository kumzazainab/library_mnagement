from pydantic import BaseModel
from datetime import datetime

class ReturnBaseResponse(BaseModel):
    # user_id: int
    book_id: int

class ReturnOutResponse(ReturnBaseResponse):
    id: int
    returned_at: datetime

    class Config:
        orm_mode = True
