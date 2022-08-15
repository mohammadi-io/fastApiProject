from fastapi import FastAPI
from . import models
from .database import engine
from .routers import authentication, blog, user

models.Base.metadata.create_all(bind=engine)  # creates all database tables
app = FastAPI()
app.include_router(router=authentication.router)
app.include_router(router=blog.router)
app.include_router(router=user.router)
