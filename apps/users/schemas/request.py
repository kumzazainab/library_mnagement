from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    email: str
    password: str
