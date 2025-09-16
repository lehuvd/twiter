from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class Account(Base):
    __tablename__ = "accounts"

    username = Column(String, nullable=False, primary_key=True)
    password = Column(String, nullable=False)

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    likes = Column(Integer, nullable=False)