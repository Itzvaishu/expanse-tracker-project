from fastapi import APIRouter
from app.api.v1.endpoints import auth, expenses, categories, users, transfers

router = APIRouter()

router.include_router(auth, prefix="/auth", tags=["auth"])
router.include_router(expenses, prefix="/expenses", tags=["expenses"])
router.include_router(categories, prefix="/categories", tags=["categories"])
router.include_router(users, prefix="/users", tags=["users"])
router.include_router(transfers, prefix="/transfers", tags=["transfers"])
