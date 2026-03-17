from fastapi import FastAPI
from . import modals
from .database import engine
from .routers import posts, users, authantication, votes
from .config import Settings

settings = Settings()

modals.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authantication.router)
app.include_router(votes.router)