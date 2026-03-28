from fastapi import FastAPI
from .database import Base, engine
from .routes import user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router, prefix="/auth", tags=["Auth"])