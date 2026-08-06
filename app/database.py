import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()# load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")# same

# setup database engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# create base class for orm model
Base = declarative_base()

# dependency for managing database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    