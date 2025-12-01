from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/balance")
def get_user_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the current authenticated user's total balance.
    """
    # We fetch the user again to ensure we have the most up-to-date balance from the DB
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "balance": user.balance,
        "account_number": user.account_number
    }

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user details
    """
    return current_user
