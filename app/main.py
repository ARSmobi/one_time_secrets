from fastapi import FastAPI
from app.api import secrets

app = FastAPI()

app.include_router(secrets.router)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
