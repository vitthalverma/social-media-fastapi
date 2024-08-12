from fastapi import FastAPI
from app import models
from .database import engine
from app.routers import post_router, user_router, auth_router, vote_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

#models.Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(vote_router.router)


@app.get("/")
def home():
    return {"message": "Hello, World!"}

