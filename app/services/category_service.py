from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import schemas
from app.models import Category

# --- CREATE ---
def create_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    """
    Creates a new category.
    Fixes IntegrityError by checking if category already exists.
    """
    # 1. Clean whitespace
    clean_name = category.name.strip()

    # 2. Check if category already exists for this user
    existing_category = db.query(Category).filter(
        Category.name == clean_name,
        Category.user_id == user_id
    ).first()

    # 3. If it exists, return the existing one (Don't crash)
    if existing_category:
        return existing_category

    # 4. If not exists, create new
    try:
        db_category = Category(
            name=clean_name,
            user_id=user_id
        )
        
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    except IntegrityError:
        # Safety net: If a race condition happens, rollback and return existing
        db.rollback()
        return db.query(Category).filter(
            Category.name == clean_name, 
            Category.user_id == user_id
        ).first()
        
    except Exception as e:
        db.rollback()
        raise e

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
        
        try:
            db.commit()
            db.refresh(db_category)
        except Exception as e:
            db.rollback()
            raise e
        
    return db_category

# --- DELETE ---
def delete_category(db: Session, category_id: int, user_id: int):
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    
    if db_category:
        db.delete(db_category)
        db.commit()
        
    return db_category