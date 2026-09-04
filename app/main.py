from fastapi import FastAPI,APIRouter
from . import models
from.routers import expenses,users,auth
from .database import engine


models.Base.metadata.create_all(bind=engine)
app= FastAPI()

app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(auth.router)
@app.get("/")
async def root():
    return{"message":"API is running."}