from sqlalchemy.orm import Session
from app import models, schemas, hashing
from app.database import get_db
from fastapi import FastAPI, status, HTTPException, Depends, Response, APIRouter
from typing import Optional,List
from app import oauth
router=APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hashing.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    return user
