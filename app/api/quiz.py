
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.response_schema import ResponseSchema
from app.models.quiz import Quiz
from app.schemas.quiz import QuizCreate,QuizResponse
from app.core.database import get_db
import app.models.quiz as QuizModel


router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)

@router.post("/",response_model=ResponseSchema[QuizResponse],status_code=201)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):

    try:
        db_quiz = Quiz(title=quiz.title, description=quiz.description)
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return ResponseSchema(
                status="success",
                status_code=201,
                message="Quiz created successfully",
                data=db_quiz 
            )
    except Exception as e:
        db.rollback()
        return ResponseSchema(
                status="error",
                status_code=500,
                message="Quiz Creation Failed",
                error=str(e),
                data=None
            )

@router.get("/get-quizzes",response_model=ResponseSchema[Union[QuizResponse, List[QuizResponse]]],status_code=200)
def get_quizes(id:Optional[int] = Query(None),db: Session=Depends(get_db)):
    
    try:

        if id:
            quiz = db.query(QuizModel.Quiz).filter(QuizModel.Quiz.id==id).first()
            if not quiz:
                return {
                    "status":"Error",
                    "status_code":404,
                    "message":"Quiz Not found",
                    "data":[]

                }

            return {
                    "status":"Success",
                    "status_code":201,
                    "message":"Quiz fetched successfully",
                    "data":quiz

                }

        quizzes = db.query(QuizModel.Quiz).order_by(QuizModel.Quiz.id.desc()).all()
        return ResponseSchema(
            status="success",
            status_code=200,
            message="Quizzes fetched successfully",
            data=quizzes 
        )

    except Exception as e:
        db.rollback()
        return ResponseSchema(
            status="error",
            status_code=500,
            message="Failed to fetch quizzes",
            error=str(e),
            data=[]
        )
    

@router.put("/quiz-update/{id}",response_model=ResponseSchema[QuizResponse],status_code=200)
def update_quiz(id:int,quiz:QuizCreate,db:Session=Depends(get_db)):

    quiz_ = db.query(QuizModel.Quiz).filter(QuizModel.Quiz.id==id).first()
    if quiz_:
        quiz_.title = quiz.title
        quiz_.description = quiz.description
        quiz_.passing_criteria = quiz.passing_criteria
        db.commit()
        db.refresh(quiz_)
        return {
            "status":"update",
            "status_code":200,
            "message":"Quiz Updated",
            "data":quiz_

        }

    else:
        return {
            "status":"Error",
            "status_code":404,
            "message":"Quiz Not found",
            "data":[]

        }
    

@router.delete("/quiz/{id}",response_model=ResponseSchema[QuizResponse],status_code=200)
def delete_quiz(id:int,db:Session=Depends(get_db)):

    quiz = db.query(QuizModel.Quiz).filter(QuizModel.Quiz.id==id).first()

    if not quiz:
        return {
            "status":"Error",
            "status_code":500,
            "message":"Invalid ID",
            "data":None

        }
    
    db.delete(quiz)
    db.commit()


    return {
            "status":"update",
            "status_code":200,
            "message":"Quiz Deleted",
            "data":None

        }
