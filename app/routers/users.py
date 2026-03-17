from ..schemas import UserOut, Usercreate
from ..utells import hash_password
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, responses
from sqlalchemy.orm import Session
from .. import modals
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: Usercreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = modals.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(modals.User).filter(modals.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user


