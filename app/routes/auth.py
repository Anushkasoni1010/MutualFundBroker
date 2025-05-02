from app.token.token import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from models import User
from pydantic import BaseModel
from app.db import get_db
from sqlalchemy.orm import Session
import bcrypt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Request Model for Sign-Up
class UserCreate(BaseModel):
    email: str
    password: str

# Request Model for Login
class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/signup/")
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if the user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.warning(f"Signup attempt with existing email: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        # Securely hash the password
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Add new user to the database
        db_user = User(email=user.email, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"New user created: {db_user.email}")
        return {"message": "User created successfully", "user": {"email": db_user.email}}
    except Exception as e:
        logger.error(f"Error during signup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during signup")


@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            logger.warning(f"Login failed: User not found - {user.email}")
            raise HTTPException(status_code=401, detail="User does not exist")

        if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
            logger.warning(f"Login failed: Invalid password for {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate JWT token
        access_token = create_access_token(data={"sub": db_user.email})
        logger.info(f"User logged in: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during login: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during login")