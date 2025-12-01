from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.services.category_service import create_category, get_categories, get_category, update_category, delete_category
from app.db.session import get_db
from app.core.security import get_current_user
from app.models import User

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=schemas.Category)
def create_category_endpoint(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_category(db=db, category=category, user_id=current_user.id)

@router.get("/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    categories = get_categories(db, user_id=current_user.id, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = get_category(db, category_id=category_id, user_id=current_user.id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category_endpoint(category_id: int, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = update_category(db, category_id=category_id, category_update=category_update, user_id=current_user.id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}")
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = delete_category(db, category_id=category_id, user_id=current_user.id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}
