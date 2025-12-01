# app/models/rbac.py

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

# 1. Role aur Permission ko jodne wali Table
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id"))
)

# 2. Permission Model
class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True) # e.g. "Can Delete"
    slug = Column(String(50), unique=True) # e.g. "category:delete"

# 3. Role Model
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True) # e.g. "admin", "manager"
    
    # Relationships (String use kar rahe hain taaki error na aaye)
    permissions = relationship("Permission", secondary=role_permissions, backref="roles")
    users = relationship("User", back_populates="role")


    