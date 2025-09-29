"""
This file contains routes for user management (signup, profile, etc).
Currently only handles user registration.
"""

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas
import utils

# Create router for user management endpoints
router = APIRouter(
    prefix="/users",  # All routes will start with /users
    tags=["Users"]  # Groups routes in API documentation
)

@router.post("/signup", status_code=201)
async def signup(account: schemas.Account, db: Session = Depends(get_db)):
    """
    Create a new user account.
    
    This endpoint creates a new user with a hashed password.
    Usernames must be unique.
    
    Args:
        account: User account data (username and password)
        db: Database session dependency
        
    Returns:
        Success message with username
        
    Raises:
        HTTPException: If username is already taken
    """
    # Check if username already exists
    existing_user = db.query(models.Account).filter(models.Account.username == account.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already taken")

    try:
        # Hash the password before storing (never store plain text passwords!)
        hashed_password = utils.hash_password(account.password)
        
        # Create new user account
        new_account = models.Account(username=account.username, password=hashed_password)
        
        # Add to database and save
        db.add(new_account)
        db.commit()
        
        return {"message": f"Account {account.username} created successfully."}
        
    except Exception as e:
        # Roll back any changes if something goes wrong
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating account")
