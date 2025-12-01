from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TransferCreate(BaseModel):
    to_account_number: str
    amount: float
    description: str

class TransferResponse(BaseModel):
    id: int
    from_account: str
    to_account: str
    amount: float
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TransferUpdate(BaseModel):
    to_account_number: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
