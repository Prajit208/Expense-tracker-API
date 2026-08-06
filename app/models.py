from .database import Base

from sqlalchemy import TIMESTAMP, Column, Integer,Boolean,String, text,ForeignKey,Numeric,DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id= Column(Integer,primary_key=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
class Expense(Base):
    __tablename__="expenses"
    id=Column(Integer,primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    title=Column(String, nullable=False)
    description=Column(String, nullable=False)
    amount=Column(Numeric,nullable=False)
    category=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    date=Column(DateTime(timezone=True),nullable=False)