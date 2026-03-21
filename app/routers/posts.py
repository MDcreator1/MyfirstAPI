from ..schemas import PostCreate, Post, Postout
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, responses
from sqlalchemy.orm import Session
from .. import modals
from ..database import get_db
from ..oauth2 import get_current_user
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# @router.get("/", response_model=list[Post])
@router.get("/", response_model=list[Postout])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(modals.Post).filter(modals.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(modals.Post, func.count(modals.votes.post_id).label("votes")).join(modals.votes, modals.votes.post_id == modals.Post.id, isouter=True).group_by(modals.Post.id)
    posts = posts.filter(modals.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = list(map(lambda x : x._mapping, posts)) 

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_id = user.id
    new_post = modals.Post(**post.dict(), owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=Postout)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(modals.Post, func.count(modals.votes.post_id).label("votes")).join(modals.votes, modals.votes.post_id == modals.Post.id, isouter=True).group_by(modals.Post.id).first()
    
    # post = db.query(modals.Post).filter(modals.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, user = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(modals.Post).filter(modals.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post) # post.delete(synchronize_session=False) --- IGNORE --- for this we have post query = db.query(modals.Post).filter(modals.Post.id == id) and then we can use post_query.delete(synchronize_session=False), in this casw we not not use .first() because we are not interested in the post object but just want to delete it
    db.commit()
    return responses.Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, user = Depends(get_current_user),  db: Session = Depends(get_db)):
    post_to_update = db.query(modals.Post).filter(modals.Post.id == id)
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post_to_update.first().owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # for key, value in post.dict().items():
    #     setattr(post_to_update, key, value)
    post_to_update.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_to_update.first()