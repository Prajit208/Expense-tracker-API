from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..database import get_db
import schemas

router=APIRouter(prefix="/users",tag=['Users'])

@router.get("/")
async def get_all_users():
    return 

@router.post("/")
async def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    return