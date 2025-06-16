from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True
