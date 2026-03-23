from fastapi import FastAPI
from . import modals
from .database import engine
from .routers import posts, users, authantication, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# modals.Base.metadata.create_all(bind=engine)

arigins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = arigins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authantication.router)
app.include_router(votes.router)

@app.get("/")
def get_posts():
    result = {
        "detail": "hello world, this is the aera of new creations!"
    }
    return result