from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, responses
from ..oauth2 import get_current_user
from ..schemas import Vote
from ..utells import hash_password
from sqlalchemy.orm import Session
from .. import modals
from ..database import get_db



router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), user = Depends(get_current_user)):

    post = db.query(modals.votes).filter(modals.votes.post_id == vote.post_id, modals.votes.user_id == user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")
    
    if vote.dir == 1:
        found_vote = db.query(modals.votes).filter(modals.votes.post_id == vote.post_id, modals.votes.user_id == user.id).first()
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with id: {user.id} has already voted on post with id: {vote.post_id}")
        new_vote = modals.votes(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        found_vote = db.query(modals.votes).filter(modals.votes.post_id == vote.post_id, modals.votes.user_id == user.id).first()
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")
        db.delete(found_vote)
        db.commit()
        return {"message": "successfully deleted vote"}