from fastapi import FastAPI
from app.core.database import session
from app.api.quiz import router as quiz_router
from app.api.question import router as question_router
from app.core.response_schema import ResponseSchema
from app.api.answer_submission import routers as answer_router
from app.api.accounts import router as auth_router
from app.api.analytics import router as analytic_router

app = FastAPI()


app.include_router(quiz_router)
app.include_router(question_router)
app.include_router(answer_router)
app.include_router(auth_router)
app.include_router(analytic_router)

