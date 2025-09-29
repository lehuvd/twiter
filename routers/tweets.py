"""
This file contains routes for tweet management (create, read, update, delete).
All tweet operations except reading require JWT authentication.
"""

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas, oauth2

# Create router for tweet endpoints
router = APIRouter(
    prefix="/tweets",  # All routes will start with /tweets
    tags=["Tweets"]  # Groups routes in API documentation
)

@router.get("/", response_model=list[schemas.TweetOut])
async def get_all_tweets(db: Session = Depends(get_db)):
    """
    Get all tweets ordered by creation time (newest first).
    
    This is a public endpoint - no authentication required.
    
    Args:
        db: Database session dependency
        
    Returns:
        List of all tweets with their details
    """
    tweets = db.query(models.Tweet).order_by(models.Tweet.created.desc()).all()
    return tweets

@router.post("/", status_code=201, response_model=schemas.TweetOut)
async def create_tweet(
    tweet: schemas.TweetCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Create a new tweet.
    
    Requires JWT authentication. Users can only create tweets for themselves.
    
    Args:
        tweet: Tweet data (username and content)
        db: Database session dependency
        current_user: Current authenticated user from JWT token
        
    Returns:
        The created tweet with its details
        
    Raises:
        HTTPException: If user tries to tweet as someone else
    """
    # Security check: users can only create tweets for themselves
    if tweet.username != current_user.id:
        raise HTTPException(status_code=403, detail="You can only create tweets for yourself")
    
    # Create new tweet in database
    new_tweet = models.Tweet(username=tweet.username, content=tweet.content)
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)  # Get the tweet back with auto-generated fields
    
    return new_tweet

@router.patch("/{tweet_id}", response_model=schemas.TweetOut)
async def edit_tweet(
    tweet_id: int, 
    tweet_update: schemas.TweetUpdate, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Edit an existing tweet.
    
    Requires JWT authentication. Users can only edit their own tweets.
    
    Args:
        tweet_id: ID of the tweet to edit
        tweet_update: New content for the tweet
        db: Database session dependency
        current_user: Current authenticated user from JWT token
        
    Returns:
        The updated tweet
        
    Raises:
        HTTPException: If tweet not found or user doesn't own the tweet
    """
    # Find the tweet to edit
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    # Security check: users can only edit their own tweets
    if tweet.username != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own tweets")
    
    # Update the tweet content
    db.query(models.Tweet).filter(models.Tweet.id == tweet_id).update({"content": tweet_update.content})
    db.commit()
    db.refresh(tweet)  # Get updated tweet
    
    return tweet

@router.delete("/{tweet_id}", status_code=204)
async def delete_tweet(
    tweet_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Delete a tweet.
    
    Requires JWT authentication. Users can only delete their own tweets.
    
    Args:
        tweet_id: ID of the tweet to delete
        db: Database session dependency
        current_user: Current authenticated user from JWT token
        
    Returns:
        None (204 No Content status)
        
    Raises:
        HTTPException: If tweet not found or user doesn't own the tweet
    """
    # Find the tweet to delete
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    # Security check: users can only delete their own tweets
    if tweet.username != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own tweets")
    
    # Delete the tweet
    db.delete(tweet)
    db.commit()
    
    return None  # 204 No Content

@router.post("/{tweet_id}/like", response_model=schemas.TweetOut)
async def like_tweet(
    tweet_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Like a tweet (increment the like count).
    
    Requires JWT authentication. Any authenticated user can like any tweet.
    
    Args:
        tweet_id: ID of the tweet to like
        db: Database session dependency
        current_user: Current authenticated user from JWT token
        
    Returns:
        The tweet with updated like count
        
    Raises:
        HTTPException: If tweet not found
    """
    # Find the tweet to like
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    
    # Increment like count
    tweet.likes += 1
    db.commit()
    db.refresh(tweet)
    
    return tweet