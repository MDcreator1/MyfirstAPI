
from pydantic import BaseModel, EmailStr, conint
from typing import Optional




class Usercreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id : int
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

class Postout(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore