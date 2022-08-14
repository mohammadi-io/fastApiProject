from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(path='/user', response_model=schemas.ShowUser, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(dependency=get_db)):
    hashed_password = pwd_context.hash(secret=request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(instance=new_user)
    db.commit()
    db.refresh(instance=new_user)
    return new_user


@router.get(path='/user/{id}', response_model=schemas.ShowUser, tags=['User'])
def get_user(id: int, db: Session = Depends(dependency=get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id equal to {id} not found!')
    return user
