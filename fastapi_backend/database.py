from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  

DATABASE_URL = 'sqlite:///sqlite.db'  # Adjust for your database

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Use the session
    finally:
        db.close()  # Close the session when done