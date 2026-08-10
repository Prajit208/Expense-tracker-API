from fastapi import APIRouter,Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..import models

router=APIRouter(prefix='/expenses',tags=['Expenses'])

@router.get("/")
async def get_all_expenses(db: Session=Depends(get_db)):
    expenses=db.query(models.Expense).all()
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expenses not found")