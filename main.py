from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routers import users, tweets, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(auth.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all domains
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

@app.get("/home")
async def home_feed(
    filter_type: str = "new",
    amount: int = 10,
    time_period_days: int = 30,
    db: Session = Depends(get_db)
):
    tweets = db.query(models.Tweet).order_by(models.Tweet.created.desc()).all()
    return {"posts": tweets}