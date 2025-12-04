from sqlalchemy.orm import Session
from app.models.user import User
from app.models.expense import Expense
from app.schemas.transfer_schema import TransferCreate, TransferResponse
from app.db.session import get_db
from decimal import Decimal

def create_transfer(db: Session, transfer: TransferCreate, current_user: User):
    # Validate sender has sufficient balance
    if current_user.balance < transfer.amount:
        raise ValueError("Insufficient balance")

    # Find receiver by account number
    receiver = db.query(User).filter(User.account_number == transfer.to_account_number).first()
    if not receiver:
        raise ValueError("Receiver account not found")

    # Update balances
    current_user.balance -= transfer.amount
    receiver.balance += transfer.amount

    # Create expense records for both parties
    sender_expense = Expense(
        user_id=current_user.id,
        category_id=None,  # Assuming transfers don't have categories
        debit=transfer.amount,
        credit=0,
        description=f"Transfer to {receiver.email}"
    )
    receiver_expense = Expense(
        user_id=receiver.id,
        category_id=None,
        debit=0,
        credit=transfer.amount,
        description=f"Transfer from {current_user.email}"
    )

    db.add(sender_expense)
    db.add(receiver_expense)
    db.commit()
    db.refresh(sender_expense)
    db.refresh(receiver_expense)

    # Send email notifications
    from app.services.email_service import send_transfer_notification
    send_transfer_notification(
        sender_email=current_user.email,
        receiver_email=receiver.email,
        amount=float(transfer.amount),
        description=transfer.description or f"Transfer to {receiver.email}"
    )

    return TransferResponse(
        id=sender_expense.id,  # Using expense id as transfer id
        from_account=current_user.account_number,
        to_account=transfer.to_account_number,
        amount=transfer.amount,
        description=transfer.description or f"Transfer to {receiver.email}",
        created_at=sender_expense.created_at,
        updated_at=sender_expense.updated_at
    )

def transfer_money(db: Session, from_account: str, to_account: str, amount: float):
    current_user = db.query(User).filter(User.account_number == from_account).first()
    if not current_user:
        raise ValueError("Sender not found")
    transfer = TransferCreate(to_account_number=to_account, amount=amount, description="Transfer")
    return create_transfer(db, transfer, current_user)

def validate_account(db: Session, account_number: str) -> bool:
    user = db.query(User).filter(User.account_number == account_number).first()
    return user is not None
