from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import schemas
from app.models import expense as expense_model, Category, User, Expense



def create_debit_expense(db: Session, expense: schemas.DebitCreate, user_id: int):
    # 1. Get User and Category
    user = db.query(User).filter(User.id == user_id).first()
    category = db.query(Category).filter(Category.id == expense.category_id).first()

    # 2. Validation: Check if User and Category exist
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # 3. BUSINESS LOGIC: Check Balance
    # If the user creates a 'debit' (spending), they must have enough money.
    if user.balance < expense.debit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. You have {user.balance}, but tried to spend {expense.debit}."
        )

    # 4. Deduct Balance
    # We subtract the expense amount from the user's wallet
    user.balance = user.balance - expense.debit

    # 5. Create the Expense Record
    db_expense = Expense(
        description=expense.description,
        debit=expense.debit,
        credit=0, # Debit means no credit
        user_id=user_id,
        category_id=expense.category_id
    )

    # 6. Save Changes
    db.add(db_expense)
    db.add(user) # IMPORTANT: We must add 'user' to save the new balance
    db.commit()
    db.refresh(db_expense)
    db.refresh(user)

    return db_expense

def create_credit_expense(db: Session, expense: schemas.CreditCreate, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if expense.category_id:
        category = db.query(Category).filter(Category.id == expense.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Category with id {expense.category_id} not found")
    category_id = expense.category_id if expense.category_id and expense.category_id > 0 else None
    db_expense = expense_model.Expense(
        description=expense.description,
        debit=0.0,
        credit=expense.credit,
        category_id=category_id,
        user_id=user_id
    )
   
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(expense_model.Expense).filter(expense_model.Expense.user_id == user_id).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int, user_id: int):
    return db.query(expense_model.Expense).filter(expense_model.Expense.id == expense_id, expense_model.Expense.user_id == user_id).first()

def update_expense(db: Session, expense_id: int, expense_update: schemas.ExpenseUpdate, user_id: int):
    db_expense = db.query(expense_model.Expense).filter(expense_model.Expense.id == expense_id, expense_model.Expense.user_id == user_id).first()
    if db_expense:
        update_data = expense_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'category_id':
                if value:
                    category = db.query(Category).filter(Category.id == value).first()
                    if not category:
                        raise HTTPException(status_code=404, detail=f"Category with id {value} not found")
                value = value if value and value > 0 else None
            setattr(db_expense, field, value)
        db.commit()
        db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int, user_id: int):
    db_expense = db.query(expense_model.Expense).filter(expense_model.Expense.id == expense_id, expense_model.Expense.user_id == user_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense
