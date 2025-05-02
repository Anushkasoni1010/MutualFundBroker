from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import db_url

# Connect to your existing SQLite database
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()