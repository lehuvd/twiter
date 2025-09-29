"""
This file defines the structure of our database tables using SQLAlchemy ORM.
Each class represents a table, and each attribute represents a column.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class Account(Base):
    """
    Represents the users table in the database.
    Stores user account information including username and hashed password.
    """
    __tablename__ = "users"  # The actual table name in PostgreSQL

    # Primary key - uniquely identifies each user
    username = Column(String, nullable=False, primary_key=True)
    
    # Store hashed passwords, never plain text!
    password = Column(String, nullable=False)

class Tweet(Base):
    """
    Represents the tweets table in the database.
    Stores tweet information including content, author, timestamp, and likes.
    """
    __tablename__ = "tweets"  # The actual table name in PostgreSQL

    # Auto-incrementing primary key
    id = Column(Integer, primary_key=True, nullable=False)
    
    # Who posted this tweet (links to Account.username)
    username = Column(String, nullable=False)
    
    # The actual tweet content
    content = Column(String, nullable=False)
    
    # When the tweet was created - automatically set to current time
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
    # Number of likes - defaults to 0
    likes = Column(Integer, nullable=False, default=0)