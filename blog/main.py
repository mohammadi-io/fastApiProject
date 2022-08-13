from fastapi import Depends, FastAPI, HTTPException, Response, status
from typing import List
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)  # creates all database tables
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(path='/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_bolg = models.Blog(title=request.title, body=request.body)
    db.add(instance=new_bolg)
    db.commit()
    db.refresh(instance=new_bolg)  # refresh attributes on the given instance
    return new_bolg


@app.get(path='/blog', response_model=List[schemas.Blog])  # we use List for list of objects
def all_blogs(db: Session = Depends(dependency=get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(path='/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(id: int, db: Session = Depends(dependency=get_db)):
    # def get_blog(id: int, response: Response, db: Session = Depends(dependency=get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id equal to {id} doesn't exist!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id equal to {id} doesn't exist!"}
    return blog


@app.delete(path='/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_blog(id: int, db: Session = Depends(dependency=get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id equal to {id} doesn't exist!")
    db.commit()
    return {'detail': f'Blog with the id equal to {id} deleted!'}  # not shown!


@app.put(path='/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(dependency=get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id equal to {id} doesn't exist!")
    blog.update(values={'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return f'Blog with the id equal to {id} updated.'
