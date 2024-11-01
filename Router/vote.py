from fastapi import FastAPI, status, HTTPException, Depends, Response, APIRouter
from app import schemas, database, models, oauth
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def votes( vote : schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id:{vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.email} has already voted for the post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "Vote created"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{current_user.email} has not voted for the post {vote.post_id}")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "Vote deleted"}