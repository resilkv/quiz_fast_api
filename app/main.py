from fastapi import FastAPI
from app.core.database import session
from app.api.quiz import router as quiz_router

app = FastAPI()


app.include_router(quiz_router)