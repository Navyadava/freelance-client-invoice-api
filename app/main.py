from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import clients, invoices


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(clients.router)
app.include_router(invoices.router)

@app.get("/")
def home():
    return {"message": "Welcome to my API"}

@app.get("/health")
def health():
    return {"status": "healthy"}