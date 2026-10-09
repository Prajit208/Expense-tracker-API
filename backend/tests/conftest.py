import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("TEST_DATABASE_URL")
engine= create_engine(DATABASE_URL)
TestingSessionLocal=sessionmaker(bind=engine)

@pytest.fixture()
def session(): # create new session with fresh tables and drops all table afterwards
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture()
def client(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)    