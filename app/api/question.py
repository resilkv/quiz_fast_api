from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response_schema import ResponseSchema
from app.schemas.questions import BulkQuestionCreate, QuestionCreate, QuestionResponse, QuestionUpdate
from app.models.quiz import Questions


router = APIRouter(
    prefix="/questions",
    tags=["Question"]
)


@router.post("/",response_model=ResponseSchema[QuestionResponse],status_code=201)
def create_question(question: QuestionCreate,db: Session= Depends(get_db)):

    try:
        db_question = Questions(quiz_id=question.quiz_id,question=question.question,points=question.points,metadata_value=question.metadata_value,
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



@router.post("/bulk-question",response_model=ResponseSchema[List[QuestionResponse]],status_code=201)
def create_bulk_question(questions:BulkQuestionCreate,db: Session= Depends(get_db)):

    try:
       
        created_questions = []

        for question in questions.questions:
            db_question = Questions(quiz_id=questions.quiz_id,question=question.question,points=question.points,metadata_value=question.metadata_value,
                                    type=question.type,options=question.options,correct_answer=question.correct_answer)
            db.add(db_question)
            created_questions.append(db_question)
        
        db.commit()

        for question in created_questions:
            db.refresh(question)

        return ResponseSchema(
                status="success",
                status_code=201,
                message=f"{len(created_questions)} Questions created successfully",
                data=created_questions
            )


    except Exception as e:
        db.rollback()
        return ResponseSchema(
            status="error",
            status_code=500,
            message="Questions Creation Failed",
            error=str(e),
            data=None
        )


@router.get("/question-list",response_model=ResponseSchema[Union[QuestionResponse,List[QuestionResponse]]],status_code=200)
def get_questions(quiz_id: Optional[int] = Query(None), id: Optional[int] = Query(None),db : Session= Depends(get_db)):

    try:
        questions = db.query(Questions).order_by(Questions.id.desc())

        if quiz_id:

            questions = questions.filter(Questions.quiz_id==quiz_id)
        
        if id:
            questions = questions.filter(Questions.id==id).first()

        return ResponseSchema(
            status="success",
            status_code=200,
            message="Questions fetched successfully",
            data=questions 
        )

    except Exception as e:
        return ResponseSchema(
            status="error",
            status_code=500,
            message="Failed to fetch Questions",
            error=str(e),
            data=[]
        )

@router.put("question-update",response_model=ResponseSchema[QuestionCreate],status_code=200)
def update_question(question:QuestionUpdate, id : int ,db : Session=Depends(get_db)):

    try:

        question_db = db.query(Questions).filter(Questions.id==id).first()
        if not question_db:
            return ResponseSchema(
                status="error",
                status_code=404,
                message="Questions Not Found",
                error="Invalid ID" 
            )
        
        update_data = question.model_dump(exclude_unset=True)
        for key,val in update_data.items():
            setattr(question_db,key,val)
            db.commit()
            db.refresh(question_db)

        return ResponseSchema(
            status="update",
            status_code=200,
            message="Question Updated",
            data=question_db

        )

    except Exception as e:
        db.rollback()
        return ResponseSchema(
            status="error",
            status_code=500,
            message="Failed to update Question",
            error=str(e),
            data=[]
        )

@router.delete("/delete-questions",status_code=200)
def delete_quiz(ids:List[int],db:Session=Depends(get_db)):

    try:

        for id in ids:

            question = db.query(Questions).filter(Questions.id==id).first()

            if not question:
                return {
                    "status":"Error",
                    "status_code":500,
                    "message":"Invalid ID",
                    "data":None

                }
            
            db.delete(question)
            db.commit()


        return ResponseSchema(
                status="update",
                status_code=200,
                message="Questions Deleted",
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