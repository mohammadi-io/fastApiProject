from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get(path='/blog', response_model=List[schemas.Blog], tags=['Blog'])  # we use List for list of objects
def all(db: Session = Depends(dependency=get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post(path='/blog', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_bolg = models.Blog(title=request.title, body=request.body, creator_id=request.creator_id)
    db.add(instance=new_bolg)
    db.commit()
    db.refresh(instance=new_bolg)  # refresh attributes on the given instance
    return new_bolg


@router.get(path='/blog/{id}', response_model=schemas.ShowBlog, tags=['Blog'])
def get_blog(id: int, db: Session = Depends(dependency=get_db)):
    # def get_blog(id: int, response: Response, db: Session = Depends(dependency=get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id equal to {id} doesn't exist!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id equal to {id} doesn't exist!"}
    return blog


@router.delete(path='/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def delete_a_blog(id: int, db: Session = Depends(dependency=get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id equal to {id} doesn't exist!")
    db.commit()
    return {'detail': f'Blog with the id equal to {id} deleted!'}  # not shown!


@router.put(path='/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id: int, request: schemas.Blog, db: Session = Depends(dependency=get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id equal to {id} doesn't exist!")
    blog.update(values={'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return f'Blog with the id equal to {id} updated.'
