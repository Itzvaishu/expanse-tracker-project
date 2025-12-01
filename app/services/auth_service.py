import random
import string
from sqlalchemy.orm import Session
# Import 'or_' to allow login by Username OR Email (optional but recommended)
from sqlalchemy import or_ 
from app.models import user as user_model
from app.schemas import user_schema as user_schema
from app.core.security import get_password_hash, verify_password, create_access_token

def generate_account_number():
    import uuid
    return str(uuid.uuid4().int)[:20]

def create_user(db: Session, user: user_schema.UserCreate):
    existing_user = db.query(user_model.User).filter(
        (user_model.User.email == user.email) | (user_model.User.username == user.username)
    ).first()
    if existing_user:
        raise ValueError("User with this email or username already exists")
    hashed_password = get_password_hash(user.password)
    account_number = generate_account_number()
    db_user = user_model.User(username=user.username, email=user.email, hashed_password=hashed_password, account_number=account_number, balance=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, identifier: str, password: str):
    # --- THE FIX IS HERE ---
    # We check if the input matches the Email OR the Username.
    # This ensures it works whether they type "vaishu" or "vaishu@gmail.com"
    user = db.query(user_model.User).filter(
        or_(
            user_model.User.email == identifier,
            user_model.User.username == identifier
        )
    ).first()
    
    if not user:
        return False
    
    # Verify the password
    if not verify_password(password, user.hashed_password):
        return False
        
    return user

def create_access_token_for_user(user: user_model.User):
    # Ensure you are encoding the subject as a string (usually email or ID)
    access_token = create_access_token(subject=str(user.email))
    return access_token

def get_user_balance(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return user.balance








'''import random
import string
from sqlalchemy.orm import Session
from app.models import user as user_model
from app.schemas import user_schema as user_schema
from app.core.security import get_password_hash, verify_password, create_access_token

def generate_account_number():
    import uuid
    return str(uuid.uuid4().int)[:20]

def create_user(db: Session, user: user_schema.UserCreate):
    existing_user = db.query(user_model.User).filter(
        (user_model.User.email == user.email) | (user_model.User.username == user.username)
    ).first()
    if existing_user:
        raise ValueError("User with this email or username already exists")
    hashed_password = get_password_hash(user.password)
    account_number = generate_account_number()
    db_user = user_model.User(username=user.username, email=user.email, hashed_password=hashed_password, account_number=account_number, balance=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(user_model.User).filter(user_model.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token_for_user(user: user_model.User):
    access_token = create_access_token(subject=user.email)
    return access_token'''
