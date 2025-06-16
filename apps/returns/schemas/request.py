from pydantic import BaseModel

class ReturnCreateRequest(BaseModel):
    user_id: int
    book_id: int
