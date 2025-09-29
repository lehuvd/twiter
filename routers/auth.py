"""
This file contains routes for user authentication (login).
It handles user login and returns JWT tokens for authenticated users.
"""

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
from database import get_db
import utils, oauth2, schemas

# Create router for authentication endpoints
router = APIRouter(
    prefix="/auth",  # All routes will start with /auth
    tags=["Authentication"]  # Groups routes in API documentation
)

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.
    
    This endpoint accepts username and password via form data (OAuth2 standard)
    and returns a JWT token if credentials are valid.
    
    Args:
        user_credentials: Form data containing username and password
        db: Database session dependency
        
    Returns:
        JWT token and token type
        
    Raises:
        HTTPException: If username or password is incorrect
    """
    # Look up user in database by username
    user = db.query(models.Account).filter(models.Account.username == user_credentials.username).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Verify the password against the stored hash
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create JWT token containing the user's username
    access_token = oauth2.create_access_token(data={"user_id": user.username})
    
    # Return token in OAuth2 standard format
    return {"access_token": access_token, "token_type": "bearer"}