from fastapi import FastAPI
from apps.users import users
from apps.books import books
from apps.requests import requests
from apps.returns import returns
from apps.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(requests.router)
app.include_router(returns.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System"}
