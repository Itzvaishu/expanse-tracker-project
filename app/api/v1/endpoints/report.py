from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models import Expense, Transfer

def get_monthly_expense_report(db: Session, user):
    """
    Calculates total expenses for the current month.
    Returns a FLOAT (e.g., 500.0), not a List.
    """
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year

    # .scalar() use karte hain taaki single value mile, list nahi
    total = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user.id,
        extract('month', Expense.created_at) == current_month,
        extract('year', Expense.created_at) == current_year
    ).scalar()

    # Agar total None hai (koi expense nahi), toh 0.0 return karein
    return total if total is not None else 0.0

def get_monthly_transfers(db: Session, user):
    """
    Calculates total transfers for the current month.
    """
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year

    total = db.query(func.sum(Transfer.amount)).filter(
        Transfer.user_id == user.id,
        extract('month', Transfer.created_at) == current_month,
        extract('year', Transfer.created_at) == current_year
    ).scalar()

    return total if total is not None else 0.0

def get_recent_expenses(db: Session, user, limit: int = 5):
    return db.query(Expense).filter(
        Expense.user_id == user.id
    ).order_by(Expense.created_at.desc()).limit(limit).all()

def get_recent_transfers(db: Session, user, limit: int = 5):
    return db.query(Transfer).filter(
        Transfer.user_id == user.id
    ).order_by(Transfer.created_at.desc()).limit(limit).all()