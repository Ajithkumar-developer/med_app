# app/main.py

from fastapi import FastAPI
from app.sql_database import Base, engine
from app.routers import user_routes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API")

# user routes
app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "User API is running 🚀"}
