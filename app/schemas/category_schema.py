from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
