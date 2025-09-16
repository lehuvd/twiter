from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, get_db
import schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

logged_in = None

@router.post("/signup", status_code=201)
async def signup(account: schemas.Account, db: Session = Depends(get_db)):
    try:
        new_account = models.Account(username=account.username, password=account.password)
        db.add(new_account)
        db.commit()
    except:
        raise HTTPException(status_code=409, detail="Username already taken")
    return {"message": f"Account {account.username} created successfully."}


@router.post("/login")
async def login(account: schemas.Account, db: Session = Depends(get_db)):
    global logged_in
    acc_query = db.query(models.Account).filter(models.Account.username == account.username,
                                    models.Account.password == account.password).first()
    if not acc_query:
        raise HTTPException(status_code=404, detail="Username or password incorrect")
    if not logged_in:
        logged_in = account.username
        return {"message": "Logged in successfully"}
    elif logged_in != account.username:
        return {"message": "Already logged in with other account"}
    else:
        return {"message": "Already logged in"}


@router.post("/logout")
async def logout():
    global logged_in
    if not logged_in:
        return {"message": "Already logged out"}
    logged_in = None
    return {"message": "Logged out successfully"}