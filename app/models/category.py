from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to User
    user = relationship("User", back_populates="categories")

    # Relationship to Expense
    expenses = relationship("Expense", back_populates="category")

    __table_args__ = (UniqueConstraint('name', 'user_id', name='ix_categories_name_user_id'),)
