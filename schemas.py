"""
This file defines Pydantic models that describe the shape of data
going into and out of our API. These are used for request validation
and response serialization.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Account(BaseModel):
    """Used for user signup and login requests"""
    username: str
    password: str

class TweetBase(BaseModel):
    """Base tweet model with common fields"""
    username: str
    content: str

class TweetCreate(TweetBase):
    """Used when creating a new tweet"""
    pass  # Inherits username and content from TweetBase

class TweetUpdate(BaseModel):
    """Used when updating an existing tweet (only content can change)"""
    content: str

class TweetOut(TweetBase):
    """Used when returning tweet data to the client"""
    id: int
    created: datetime
    likes: int

    class Config:
        # Allows Pydantic to work with SQLAlchemy models
        from_attributes = True

# JWT Token related schemas
class Token(BaseModel):
    """Response model for login endpoint"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Internal model for JWT token payload"""
    id: Optional[str] = None