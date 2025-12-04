from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schema import User, UserCreate, Token, LoginRequest
from app.services.auth_service import create_user, authenticate_user, create_access_token_for_user, get_user_balance
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # NOTE: Swagger sends the email in the 'username' field
    email = form_data.username 
    password = form_data.password

    user = authenticate_user(db, email, password)
    
    if not user:
        # We use 401 (Unauthorized) here instead of 400.
        # This helps you distinguish between "Bad Data Format" (400) and "Wrong Password" (401)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}









