# Schema are pydantic class that define the shape of data coming aand going out of the API
import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):# what clients send
    password: str
    
class UserOut(UserBase):# what API sends back
    id: int
    created_at: datetime
    model_config=ConfigDict(from_attributes=True)    