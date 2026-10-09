from fastapi import FastAPI,APIRouter
from . import models
from.routers import expenses,users,auth
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app= FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(auth.router)
@app.get("/")
async def root():
    return{"message":"API is running."}