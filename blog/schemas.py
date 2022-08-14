from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

    class Config:
        """"SQLAlchemy does not return a dictionary, which is what pydantic expects by default. You can configure
        your model to also support loading from standard orm parameters (i.e. attributes on the object instead of
        dictionary lookups) """
        orm_mode = True


class ShowBlog(BaseModel):
    title: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
