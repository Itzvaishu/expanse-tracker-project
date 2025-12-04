from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models import User, Transfer, Expense

def initialize_user_balances(db: Session):
    """
    Initialize user balances based on total transfers received minus total expenses debited.
    This should be run once to fix existing users' balances.
    """
    users = db.query(User).all()

    for user in users:
        # Calculate total income (transfers where user is receiver)
        total_income = db.query(func.sum(Transfer.amount)).filter(Transfer.receiver_id == user.id).scalar() or 0.0

        # Calculate total expenses
        total_expenses = db.query(func.sum(Expense.debit)).filter(Expense.user_id == user.id).scalar() or 0.0

        # Set balance
        user.balance = total_income - total_expenses

        print(f"User {user.username}: Income {total_income}, Expenses {total_expenses}, Balance {user.balance}")

    db.commit()
    print("User balances initialized successfully.")

if __name__ == "__main__":
    db = next(get_db())
    try:
        initialize_user_balances(db)
    finally:
        db.close()
