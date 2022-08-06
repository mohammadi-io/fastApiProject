from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):  # function variable name must be like in the path, str is the default for variable type
    return {"message": f"Hello {name}"}


@app.get("/blog")
def blog(limit: int = 10, published: bool = True):  # if we don't provide the parameter we get an error
    if published:
        return {'message': f'{limit} number of blog from DB'}
    return {'message': 'not published'}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    # published: bool = None # equal to above, the difference is just in editors
    # published: bool = True


@app.post('/blog')
def create_blog(blog: Blog):
    return f'The blog with title as {blog.title} is created!'


# if __name__ == '__main__': # to change the port of running application, you must run main.py for this
    # uvicorn.run(app=app, host='127.0.0.1', port=9000)
    # uvicorn.run(app=app, port=9000)
