from fastapi import FastAPI
from . import models

models.Base.metadata.create_all(bind=engine)
app= FastAPI()

@app.get("/")
async def root():
    return{"message":"API is running."}