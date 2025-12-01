from sqlalchemy.orm import Session
from app import schemas
from app.models import Category

# --- CREATE ---
def create_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    # FIX: Removed 'description' argument because the Category model 
    # in your database only has 'id', 'name', and 'user_id'.
    db_category = Category(
        name=category.name,
        user_id=user_id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- READ ---
def get_categories(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Category).filter(Category.user_id == user_id).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()

# --- UPDATE ---
def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate, user_id: int):
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    
    if db_category:
        # We convert the Pydantic model to a dictionary, excluding unset values
        update_data = category_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            # Only update fields that actually exist on the database model
            if hasattr(db_category, field):
                setattr(db_category, field, value)
        
        db.commit()
        db.refresh(db_category)
        
    return db_category

# --- DELETE ---
def delete_category(db: Session, category_id: int, user_id: int):
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    
    if db_category:
        db.delete(db_category)
        db.commit()
        
    return db_category