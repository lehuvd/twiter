"""
This file handles JSON Web Tokens (JWT) for user authentication.
JWTs are secure tokens that contain user information and expire after a set time.
"""

from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# OAuth2 scheme - tells FastAPI where to find the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# JWT Configuration
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"  # Hashing algorithm for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tokens expire after 30 minutes

def create_access_token(data: dict):
    """
    Creates a JWT token containing user information.
    
    Args:
        data: Dictionary containing user info (usually user_id)
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    # Add expiration time to the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Create and return the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """
    Verifies and decodes a JWT token.
    
    Args:
        token: The JWT token to verify
        credentials_exception: Exception to raise if verification fails
        
    Returns:
        TokenData object containing user info from the token
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user ID from the token
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
            
        # Return token data
        token_data = schemas.TokenData(id=id)
    except JWTError:
        # Token is invalid or expired
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    FastAPI dependency that extracts the current user from the JWT token.
    This function can be used in route parameters to require authentication.
    
    Args:
        token: JWT token from the Authorization header
        
    Returns:
        TokenData object containing current user info
        
    Raises:
        HTTPException if token is invalid or missing
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)