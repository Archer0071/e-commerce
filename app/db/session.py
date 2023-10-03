from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

# Load the database URL from the environment file
DATABASE_URL = config("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create a Session class for session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()