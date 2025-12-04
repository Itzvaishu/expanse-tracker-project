from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app import schemas
from app.models import Expense, Category, User, Transfer

def create_debit_expense(db: Session, expense: schemas.DebitCreate, user_id: int):
    # 1. Validate User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Validate Category (if provided)
    if expense.category_id:
        category = db.query(Category).filter(Category.id == expense.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    # 3. BUSINESS LOGIC: Dynamic Balance Check
    # Calculate Total Income (Transfers where user is receiver)
    total_income = db.query(func.sum(Transfer.amount)).filter(Transfer.receiver_id == user_id).scalar() or 0.0
    
    # Calculate Total Expense
    total_expense_db = db.query(func.sum(Expense.debit)).filter(Expense.user_id == user_id).scalar() or 0.0
    
    current_balance = total_income - total_expense_db

    # Check if user has enough money
    if current_balance < expense.debit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient funds! Available Balance: {current_balance}"
        )

    # 4. Create the Expense Record
    db_expense = Expense(
        description=expense.description,
        debit=expense.debit,
        # credit=0, # Removed credit field if your model doesn't use it for expenses anymore
        user_id=user_id,
        category_id=expense.category_id
    )

    # 5. Update user balance
    user.balance -= expense.debit

    # 6. Save Changes
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense

def create_credit_expense(db: Session, expense: schemas.CreditCreate, user_id: int):
    # Note: Income is usually handled by Transfer model now, 
    # but keeping this function for compatibility if used elsewhere.
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    category_id = expense.category_id if expense.category_id and expense.category_id > 0 else None
    
    # Ensure Category exists if ID is provided
    if category_id:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
             raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")

    db_expense = Expense(
        description=expense.description,
        debit=0.0,
        # credit=expense.credit, # Ensure your Expense model has 'credit' column if using this
        category_id=category_id,
        user_id=user_id
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Expense).filter(Expense.user_id == user_id).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int, user_id: int):
    return db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

def update_expense(db: Session, expense_id: int, expense_update: schemas.ExpenseUpdate, user_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

    if db_expense:
        old_debit = db_expense.debit
        update_data = expense_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'category_id':
                if value:
                    category = db.query(Category).filter(Category.id == value).first()
                    if not category:
                        raise HTTPException(status_code=404, detail=f"Category with id {value} not found")
                value = value if value and value > 0 else None

            if hasattr(db_expense, field):
                setattr(db_expense, field, value)

        # Adjust user balance if debit changed
        if 'debit' in update_data:
            new_debit = update_data['debit']
            user = db.query(User).filter(User.id == user_id).first()
            user.balance += old_debit - new_debit  # Add back old debit, subtract new debit

        db.commit()
        db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int, user_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense