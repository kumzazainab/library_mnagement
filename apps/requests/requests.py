from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.requests.models import BookRequest
from apps.requests.schemas.request import RequestCreateRequest
from apps.requests.schemas.response import RequestOutResponse
from apps.dependencies import require_authenticated_user, admin_only
from apps.users.models import User

router = APIRouter(prefix="/requests", tags=["requests"])


#Create request by users
@router.post("/create", response_model=RequestOutResponse)
def create_request(
    request_data: RequestCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated_user)
):
    new_request = BookRequest(
        user_id=current_user.id,
        book_id=request_data.book_id,
        requested_at = datetime.utcnow()
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

#Filter all requests by Admin
@router.get("/", response_model=list[RequestOutResponse])
def list_requests(
    user_id: int = Query(None, description="Optional user_id to filter requests"),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    if user_id:
        requests = db.query(BookRequest).filter(BookRequest.user_id == user_id).all()
    else:
        requests = db.query(BookRequest).all()
    return requests

#View own requests (user too)
@router.get("/my-requests", response_model=list[RequestOutResponse])
def get_my_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated_user)
):
    requests = db.query(BookRequest).filter(BookRequest.user_id == current_user.id).all()
    return requests

#Get book requests by ID (User or Admin)
@router.get("/{request_id}", response_model=RequestOutResponse)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated_user)
):
    book_request = db.query(BookRequest).filter(BookRequest.id == request_id).first()
    if not book_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if current_user.role != "admin" and book_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")

    return book_request

# Admin: Update Request Status
@router.put("/{request_id}")
def update_request_status(
    request_id: int,
    status_update: dict,  # Example: {"status": "approved"}
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    book_request = db.query(BookRequest).filter(BookRequest.id == request_id).first()
    if not book_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if status_update.get("status") not in ["approved", "rejected", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status value")

    book_request.status = status_update.get("status")
    db.commit()
    db.refresh(book_request)
    return {"message": "Request status updated", "request": book_request}


#Cancel Request (User can delete  his own, Admin can delete any)
@router.delete("/{request_id}")
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated_user)
):
    book_request = db.query(BookRequest).filter(BookRequest.id == request_id).first()
    if not book_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if current_user.role != "admin" and book_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this request")

    db.delete(book_request)
    db.commit()
    return {"message": "Request deleted successfully"}


#return book
ALLOWED_BORROW_DAYS = 5
FINE_PER_DAY = 10

@router.put("/{request_id}/return")
def return_book(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_authenticated_user)):
    book_request = db.query(BookRequest).filter(BookRequest.id == request_id).first()
    if not book_request:
        raise HTTPException(status_code=404, detail="Request not found")
    if book_request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only return books you have requested")

    if book_request.returned_at is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    borrowed_days = (datetime.utcnow() - book_request.requested_at).days
    fine = 0
    if borrowed_days > ALLOWED_BORROW_DAYS:
        fine = (borrowed_days - ALLOWED_BORROW_DAYS) * FINE_PER_DAY
    book_request.returned_at = datetime.utcnow()
    book_request.status = "returned"
    db.commit()
    db.refresh(book_request)

    return {
        "message": "Book returned successfully",
        "borrowed_days": borrowed_days,
        "fine": fine
    }


