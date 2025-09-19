from fastapi import HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
from database import get_db
import utils, oauth2

router = APIRouter(
    prefix="/users",
    tags=["User Authentication"]
)

@router.post("/login")
async def login(input_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Account).filter(models.Account.username == input_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    
    # Verify the password
    if not utils.verify_password(input_credentials.password, str(user.password)):
        raise HTTPException(status_code=404, detail="Invalid username or password")
    
    access_token = oauth2.create_access_token(data={"user_id": user.username})
    return {"access_token": access_token, "token_type": "bearer"}