from fastapi import FastAPI
from app import models
from app.database import engine
from Router import user, posts, auth,vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_password)
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def index():
    return {"message": "Hello World"}