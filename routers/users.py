from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas
import utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/signup", status_code=201)
async def signup(account: schemas.Account, db: Session = Depends(get_db)):
    existing_user = db.query(models.Account).filter(models.Account.username == account.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already taken")

    try:
        new_account = models.Account(username=account.username, password=utils.hash_password(account.password))
        db.add(new_account)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=409, detail="Username already taken")
    
    return {"message": f"Account {account.username} created successfully."}