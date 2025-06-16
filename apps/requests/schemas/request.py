from pydantic import BaseModel

class RequestCreateRequest(BaseModel):
    # user_id: int
    book_id: int
