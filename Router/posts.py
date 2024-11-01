from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from fastapi import FastAPI, status, HTTPException, Depends, Response, APIRouter
from typing import Optional, List, Dict
from app import oauth
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


# @router.get("/", response_model=List[schemas.Post])
def group_by(id):
    pass


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user),limit: int=10,skip:int=0,search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results = list(map(lambda x: x._mapping, results))
    return posts

@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)):
    print(current_user.email)
    print(current_user.id)
    new = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


# @app.get("/posts/{id}")
# def get_post(id: int, db: Session = Depends(get_db)):
#
#     posts = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} not found"
#         )
#     return {"data": post}


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth.get_current_user)):
    print(current_user.email)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    return post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user), oauth=None):
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to delete this post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {"seccesfully": "deleted"}


@router.put("/{id}", response_model=List[schemas.Post])
def update_post(id: int, post_update: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)):
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to update  this post")
    post_query.update(post_update.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
