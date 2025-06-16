from pydantic import BaseModel
from datetime import datetime

class RequestOutResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    requested_at: datetime
    status: str

    class Config:
        model_config = {"from_attributes": True}