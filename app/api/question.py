from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response_schema import ResponseSchema
from app.schemas.questions import QuestionCreate, QuestionResponse
from app.models.quiz import Questions

router = APIRouter(
    prefix=["/questions"],
    tags=["Question"]
)


@router.post("/",response_model=QuestionResponse)
def create_question(question: QuestionCreate,db: Session= Depends(get_db)):

    try:
        db_question = Questions(quiz_id=question.quiz_id,question=question.question,
                                type=question.type,options=question.options,correct_answer=question.correct_answer)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return ResponseSchema(
                status="success",
                status_code=201,
                message="Questions created successfully",
                data=db_question 
            )
    
    except Exception as e:
        db.rollback()
        return ResponseSchema(
                status="error",
                status_code=500,
                message="Question Creation Failed",
                error=str(e),        
                data=None
            )