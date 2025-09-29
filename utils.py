"""
This file contains utility functions for securely hashing and verifying passwords.
We use bcrypt which is a secure hashing algorithm that includes salt generation.
"""

from passlib.context import CryptContext

# Create password context - bcrypt is currently the recommended algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Takes a plain text password and returns a secure hash.
    The hash includes a random salt, so the same password will
    generate different hashes each time.
    
    Args:
        plain_password: The user's password in plain text
        
    Returns:
        A bcrypt hash string that can be safely stored in the database
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain text password matches a stored hash.
    
    Args:
        plain_password: The password the user entered
        hashed_password: The hash stored in the database
        
    Returns:
        True if the password is correct, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
