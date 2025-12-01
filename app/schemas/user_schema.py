from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

# 1. Shared Properties
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


# 2. Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# 3. Properties to return to client (Response)
class User(UserBase):
    id: int
    is_active: bool
    balance: int
    account_number: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TransferRequest(BaseModel):
    to_account_number: str
    amount: float
