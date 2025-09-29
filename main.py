"""
This is the main application file that brings everything together.
It creates the FastAPI app, includes all the routers, sets up middleware,
and creates the database tables.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routers import users, tweets, auth

# Create database tables based on our models
# This will create the tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI(
    title="Twitter Clone API",
    description="A simple Twitter-like API with JWT authentication",
    version="1.0.0"
)

# Include all our routers (route groups)
app.include_router(users.router)    # /users/* routes
app.include_router(tweets.router)   # /tweets/* routes  
app.include_router(auth.router)     # /auth/* routes

# Add CORS middleware to allow requests from web browsers
# In production, you should specify specific origins instead of "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["http://localhost:3000", "https://yourapp.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    """
    Root endpoint - returns a welcome message.
    This is useful for checking if the API is running.
    """
    return {"message": "Welcome to the Twitter Clone API! Visit /docs for API documentation."}

@app.get("/home")
async def home_feed(
    filter_type: str = "new",
    amount: int = 10,
    time_period_days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get a home feed of tweets.
    
    Currently returns all tweets ordered by creation time.
    The parameters are accepted but not yet implemented - they're here
    for future enhancement.
    
    Args:
        filter_type: How to filter tweets (not implemented)
        amount: How many tweets to return (not implemented)
        time_period_days: Time period for tweets (not implemented)
        db: Database session dependency
        
    Returns:
        All tweets in reverse chronological order
    """
    # TODO: Implement filtering based on parameters
    tweets = db.query(models.Tweet).order_by(models.Tweet.created.desc()).all()
    return {"posts": tweets}