from fastapi import APIRouter

router = APIRouter(
    prefix="/returns",
    tags=["Returns"]
)

@router.get("/")
def get_returns():
    return {"message": "List of returns"}

@router.post("/")
def create_return(return_record: dict):
    return {"message": "Return created", "return": return_record}
