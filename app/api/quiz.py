
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.response_schema import ResponseSchema
from app.models.quiz import Quiz
from app.schemas.quiz import QuizCreate,QuizResponse, QuizUpdate
from app.core.database import get_db
import app.models.quiz as QuizModel


router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)

@router.post("/",response_model=ResponseSchema[QuizResponse],status_code=201)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
   
    try:
        
        db_quiz = Quiz(title=quiz.title, description=quiz.description,passing_criteria=quiz.passing_criteria)
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
def get_quizes(id:Optional[int] = Query(None),db: Session=Depends(get_db),limit: int = Query(10,ge=1,le=100),offset: int = Query(0, ge=0)):
    
    try:

        if id:
            quiz = db.query(QuizModel.Quiz).filter(QuizModel.Quiz.id==id).first()
            if not quiz:
                return ResponseSchema(
                    status="Error",
                    status_code=404,
                    message = "Quiz Not found",
                    data = None
                )
            
            return ResponseSchema(
                    status="Success",
                    status_code=201,
                    message="Quiz fetched successfully",
                    data=quiz

            )

        total_quizzes = db.query(func.count(QuizModel.Quiz.id)).scalar()
        quizzes = db.query(QuizModel.Quiz).order_by(QuizModel.Quiz.id.desc()).offset(offset).limit(limit).all()
        return ResponseSchema(
            status="success",
            status_code=200,
            message="Quizzes fetched successfully",
            total = total_quizzes,
            data=quizzes 
        )

    except Exception as e:
        return ResponseSchema(
            status="error",
            status_code=500,
            message="Failed to fetch quizzes",
            error=str(e),
            data=[]
        )
    

@router.put("/quiz-update/{id}",response_model=ResponseSchema[QuizResponse],status_code=200)
def update_quiz(id:int,quiz:QuizUpdate,db:Session=Depends(get_db)):

    try:

        quiz_ = db.query(QuizModel.Quiz).filter(QuizModel.Quiz.id==id).first()
        if quiz_:
            update_data = quiz.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(quiz_, key, value)
            db.commit()
            db.refresh(quiz_)

            return ResponseSchema(
                status="update",
                status_code=200,
                message="Quiz Updated",
                data=quiz_

            )

        else:
            return ResponseSchema(
                status="Error",
                status_code=404,
                message="Quiz Not found",
                data=None

            )
    except Exception as e:
        db.rollback()
        return ResponseSchema(
            status="error",
            status_code=500,
            message="Failed to update quiz",
            error=str(e),
            data=[]
        )

@router.delete("/quiz/{id}",response_model=ResponseSchema[QuizResponse],status_code=200)
def delete_quiz(id:int,db:Session=Depends(get_db)):

    try:

        quiz = db.query(QuizModel.Quiz).filter(QuizModel.Quiz.id==id).first()

        if not quiz:
            return ResponseSchema(
                status="Error",
                status_code=500,
                message="Invalid ID",
                data=None

            )
                
            
        
        db.delete(quiz)
        db.commit()


        return ResponseSchema(
                status="update",
                status_code=200,
                message="Quiz Deleted",
                data=None
                )
    
    except Exception as e:
        db.rollback()
        return ResponseSchema(
            status="error",
            status_code=500,
            message="Failed to delete quiz",
            error=str(e),
            data=None
        )
