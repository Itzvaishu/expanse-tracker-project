from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import TransferRequest
from app.services.transfer_service import transfer_money, validate_account
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
 
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/transfers", tags=["transfers"])

@router.post("/transfer")
def transfer(request: TransferRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = transfer_money(db, current_user.account_number, request.to_account_number, request.amount)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/validate-account")
@cache(expire=60)
def validate_account_endpoint(account_number: str, db: Session = Depends(get_db)):
    is_valid = validate_account(db, account_number)
    return {"is_valid": is_valid}
