from fastapi import HTTPException, Depends, status
from apps.users.models import User
from apps.users.auth import get_current_user

def require_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user

def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can perform this action!"
        )
    return current_user
