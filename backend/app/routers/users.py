from fastapi import APIRouter, HTTPException,status,Depends,Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schemas
from .. import utils
router= APIRouter(prefix="/users",tags=['User']) 
# @router.get("/")
# async def get_all_user(db:Session=Depends(get_db)):
#     user=db.query(models.User).all()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Users not found")
#     return user

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exist")
    hashed_password=utils.hash_password(user.password)# call a hashing function to hash the password
    user.password=hashed_password# storing the hashed password in password filed instead of raw password
    new_user= models.User(**user.model_dump()) # converts pydantic object to dict object,** unpacks dict object to keyword arguments
    db.add(new_user)# add it to database
    db.commit()
    db.refresh(new_user)
    return new_user

# @router.get("/{id}",status_code=status.HTTP_200_OK)
# async def get_user(id: int, db: Session = Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id).first()# queries user table by id and get the first match
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
#     return user
    
    