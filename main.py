from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers import authentication, blog, user

models.Base.metadata.create_all(bind=engine)  # creates all database tables
app = FastAPI()
app.include_router(router=authentication.router)
app.include_router(router=blog.router)
app.include_router(router=user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
