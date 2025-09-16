from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, get_db
import schemas

router = APIRouter(
    prefix="/tweet",
    tags=["Tweets"]
)

@router.post("/", status_code=201)
async def tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    global logged_in
    if tweet.username == logged_in:
        new_tweet = models.Tweet(username=tweet.username, content=tweet.content, likes=0)
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        return new_tweet
    elif logged_in != None:
        raise HTTPException(status_code=403, detail=f"Not logged in as {tweet.username}")
    else:
        raise HTTPException(status_code=401, detail="Log in to tweet")


@router.patch("/{id}")
async def edit_tweet(id: int, tweet_update: schemas.TweetUpdate, db: Session = Depends(get_db)):
    global logged_in
    db_tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not db_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    elif db_tweet.username == logged_in:
        db_tweet.content = tweet_update.content
        db.commit()
        db.refresh(db_tweet)
        return db_tweet
    elif logged_in != None:
        raise HTTPException(status_code=403, detail=f"Not logged in as {db_tweet.username}")
    else:
        raise HTTPException(status_code=401, detail="Log in to edit tweets")


@router.delete("/{id}", status_code=204)
async def delete_tweet(id: int, db: Session = Depends(get_db)):
    global logged_in
    db_tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not db_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    elif db_tweet.username == logged_in:
        db.delete(db_tweet)
        db.commit()
        return None
    elif logged_in != None:
        raise HTTPException(status_code=403, detail=f"Not logged in as {db_tweet.username}")
    else:
        raise HTTPException(status_code=401, detail="Log in to delete tweets")


@router.post("/{id}/like", status_code=200)
async def like_tweet(id: int, db: Session = Depends(get_db)):
    db_tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not db_tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    db_tweet.likes += 1
    db.commit()
    db.refresh(db_tweet)
    return db_tweet