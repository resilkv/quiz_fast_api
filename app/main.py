from fastapi import FastAPI
from app.core.database import session
from app.api.quiz import router as quiz_router
from app.api.question import router as question_router
from app.core.response_schema import ResponseSchema
from app.api.answer_submission import routers as answer_router
from app.api.accounts import router as auth_router
from app.api.analytics import router as analytic_router

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status

app = FastAPI()


app.include_router(quiz_router)
app.include_router(question_router)
app.include_router(answer_router)
app.include_router(auth_router)
app.include_router(analytic_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "status_code": 422,
            "message": "Validation Error",
            "error": exc.errors(),
            "data": None,
        },
    )
