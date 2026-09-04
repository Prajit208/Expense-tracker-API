from fastapi import APIRouter,Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..import models,schemas,oauth2

router=APIRouter(prefix='/expenses',tags=['Expenses'])

@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_expenses(db: Session=Depends(get_db),current_user: models.User=Depends(oauth2.get_current_user)):
    expenses=db.query(models.Expense).filter(models.Expense.user_id==current_user.id).all()
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expenses not found")
    return expenses

@router.post("/",response_model=schemas.ExpenseOut,status_code=status.HTTP_201_CREATED)
async def add_expense(expense: schemas.ExpenseCreate,db : Session=Depends(get_db),current_user: models.User=Depends(oauth2.get_current_user)):
    new_expense=models.Expense(**expense.model_dump(),user_id=current_user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.put("/{id}",response_model=schemas.ExpenseOut,status_code=status.HTTP_200_OK)
async def update_expenses(id: int,update_expense:schemas.ExpenseCreate,db: Session= Depends(get_db),current_user: models.User=Depends(oauth2.get_current_user)):
    expense=db.query(models.Expense).filter(models.Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=404,detail="Expense not found")
    
    if expense.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden") 
    update_expenses=db.query(models.Expense).filter(models.Expense.id==id).update(update_expense.model_dump(),synchronize_session=False)
                
    db.commit()
    update_expenses=db.query(models.Expense).filter(models.Expense.id==id).first()
    return update_expenses

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_expenses(id: int, db: Session=Depends(get_db),current_user: models.User=Depends(oauth2.get_current_user)):
    expense=db.query(models.Expense).filter(models.Expense.id==id).first()
    if not expense:
        raise HTTPException(status_code=404,detail="Expense not found")
    if expense.user_id !=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden") 
    db.delete(expense)
    db.commit()