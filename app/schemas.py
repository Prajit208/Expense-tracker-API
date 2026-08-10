# Schema are pydantic class that define the shape of data coming aand going out of the API
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):# what clients send
    password: str
    
class UserOut(UserBase):# what API sends back
    id: int
    created_at: datetime
    model_config=ConfigDict(from_attributes=True)    
    
    
class ExpenseBase(BaseModel):
    title: str
    description: str | None = None
    amount: float
    category:str
    date: datetime
        
class ExpenseCreate(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    id: int
    user_id:int
    created_at: datetime
    model_config=ConfigDict(from_attributes=True)        