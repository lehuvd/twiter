from pydantic import BaseModel
from datetime import datetime

class Account(BaseModel):
    username: str
    password: str

class TweetBase(BaseModel):
    username: str
    content: str

class TweetCreate(TweetBase):
    pass

class TweetUpdate(BaseModel):
    content: str

class TweetOut(TweetBase):
    id: int
    created: datetime
    likes: int 

    class Config:
        from_attributes = True
