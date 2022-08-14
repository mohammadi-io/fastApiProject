from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str
    creator_id: int

    class Config:
        """"SQLAlchemy does not return a dictionary, which is what pydantic expects by default. You can configure
        your model to also support loading from standard orm parameters (i.e. attributes on the object instead of
        dictionary lookups) """
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []  # Exact name in the models.py

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser  # exactly like the name in models.py

    class Config:
        orm_mode = True
