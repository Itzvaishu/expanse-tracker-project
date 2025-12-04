# app/schemas/expense.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base Schema
class ExpenseBase(BaseModel):
    description: str
    debit: float
    category_id: Optional[int] = None

# Create Schemas
class DebitCreate(ExpenseBase):
    pass

class CreditCreate(BaseModel):
    description: str
    credit: float
    category_id: Optional[int] = None

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    debit: Optional[float] = None
    category_id: Optional[int] = None

# --- FIX IS HERE (Response Schema) ---
class Expense(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime

    # Maine yahan se extra fields hata diye hain
    # Jo database mein nahi the (credit, is_active, updated_at)

    class Config:
        orm_mode = True


