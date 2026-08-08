from fastapi import FastAPI,APIRouter
from . import models
from.routers import expenses,users

models.Base.metadata.create_all(bind=engine)
app= FastAPI()

app.include_router(expenses.router)
app.include_router(users.router)
@app.get("/")
async def root():
    return{"message":"API is running."}