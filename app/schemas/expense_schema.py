from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DebitCreate(BaseModel):
    description: str
    debit: float
    category_id: Optional[int] = None

class CreditCreate(BaseModel):
    description: str
    credit: float
    category_id: Optional[int] = None

class Expense(BaseModel):
    id: int
    description: str
    debit: float
    credit: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    user_id: int
    category_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    debit: Optional[float] = None
    credit: Optional[float] = None
    category_id: Optional[int] = None
