from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.users.models import User
from apps.users.schemas.request import UserCreate, UserLogin
from apps.users.schemas.response import UserOut, TokenResponse
from apps.utils import hash_password, verify_password
from apps.tokens import create_access_token


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_pwd, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token({"user_id": db_user.id, "role": db_user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role
    }