from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from .transfer import Transfer

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    account_number = Column(String(20), nullable=True)
    balance = Column(Float, default=0.0)
    profile_picture = Column(String(255), nullable=True)
    
    # --- NEW COLUMNS FOR OTP ---
    reset_otp = Column(String(10), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    # ... baaki relationships same rahenge ...
    expenses = relationship("Expense", back_populates="user")
    categories = relationship("Category", back_populates="user")
    sent_transfers = relationship("Transfer", foreign_keys="[Transfer.sender_id]", back_populates="sender")
    received_transfers = relationship("Transfer", foreign_keys="[Transfer.receiver_id]", back_populates="receiver")





