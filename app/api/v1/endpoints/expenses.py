from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.services.expense_service import create_debit_expense, create_credit_expense, get_expenses, get_expense, update_expense, delete_expense
from app.db.session import get_db
from app.core.security import get_current_user
from app.models import User

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/debit", response_model=schemas.Expense)
def create_debit_expense_endpoint(expense: schemas.DebitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_debit_expense(db=db, expense=expense, user_id=current_user.id)

@router.post("/credit", response_model=schemas.Expense)
def create_credit_expense_endpoint(expense: schemas.CreditCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_credit_expense(db=db, expense=expense, user_id=current_user.id)

@router.get("/", response_model=list[schemas.Expense])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expenses = get_expenses(db, user_id=current_user.id, skip=skip, limit=limit)
    return expenses

@router.get("/{expense_id}", response_model=schemas.Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_expense = get_expense(db, expense_id=expense_id, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense_endpoint(expense_id: int, expense_update: schemas.ExpenseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_expense = update_expense(db, expense_id=expense_id, expense_update=expense_update, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@router.delete("/{expense_id}")
def delete_expense_endpoint(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_expense = delete_expense(db, expense_id=expense_id, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}
