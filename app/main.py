from fastapi import FastAPI
from app.routers import clients


app = FastAPI()

app.include_router(clients.router)

@app.get("/")
def home():
    return {"message": "Welcome to my API"}

@app.get("/health")
def health():
    return {"status": "healthy"}