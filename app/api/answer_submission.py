from typing import List, Union
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from fastapi import Depends
from app.api.accounts import get_current_user
from app.core.database import get_db
from app.core.response_schema import ResponseSchema
from app.models.accounts import Student
from app.models.quiz import Questions
from app.schemas.student_submission import AnswerSubmissionResponse, AnswerSubmissionSchema, StudentAnswerSchema, StudentEvaluation
from app.models.student import QuizStatus, StudentAnswer,StudentQuizSubmission
from sqlalchemy import func



routers = APIRouter(
    prefix="/answer-submission",
    tags=["Answers"]

)

@routers.post("/",response_model=ResponseSchema[AnswerSubmissionSchema],status_code=201)
def submit_answer(answers:StudentAnswerSchema,db: Session=Depends(get_db) ,current_user: Student = Depends(get_current_user)):

    total_marks = 0
    actual_marks = 0
    quiz_id = None
    student_id = current_user.id 

    

    submission = StudentQuizSubmission(
        student_id=student_id,
        quiz_id=None,
        total_score=0,
        status='pass'
    )
    db.add(submission)
    db.flush()

    previous_attempt = db.query(StudentQuizSubmission).filter(StudentQuizSubmission.quiz_id==quiz_id,StudentQuizSubmission.student_id==student_id).count()
   
    for answer in answers.answer:

        question = db.query(Questions).filter(Questions.id==answer.question_id).first()
        if not question:
            return ResponseSchema(
                status="error",
                status_code=500,
                message="Questions Does Not exists",
                data=None
            )
        
        points = 0
        quiz_id = question.quiz_id

        is_correct = False
        if answer.answer:
            points = question.points
            actual_marks += points

            if question.type in ['multiple_choice', 'true_false']:
                if question.correct_answer == answer.answer:
                
                    total_marks += points

                    is_correct = True
            else:
                total_marks += points

        
        student_answer_db = StudentAnswer(submission_id=submission.id,question_id=question.id,student_answer=answer.answer,is_correct=is_correct,points=points,feed_back=None)
    
        db.add(student_answer_db)
    
   
    
    total_percentage = (total_marks/actual_marks)*100  if actual_marks else 0

    
    
    
    if total_percentage<50:
        submission.status = QuizStatus.FAIL

    submission.quiz_id = quiz_id
    submission.total_score = total_marks
    submission.attempt = previous_attempt+1
    db.commit()
    db.refresh(submission)

    return ResponseSchema(
        status="success",
        status_code=200,
        message="Answer Submitted successfully",
        data=submission 
    )




@routers.get("/list-submissions",response_model=ResponseSchema[Union[AnswerSubmissionResponse,List[AnswerSubmissionResponse]]],status_code=200)
def list_submissions(student_id: int = Query(None),quiz_id : int = Query(None),id : int = Query(None),db: Session=Depends(get_db)):

    submissions = db.query(StudentQuizSubmission)

    if student_id:
        submissions = submissions.filter(StudentQuizSubmission.student_id==student_id)
    if quiz_id:
        submissions = submissions.filter(StudentQuizSubmission.quiz_id==quiz_id)

    if id:
        submissions = submissions.filter(StudentQuizSubmission.id==id).first()
    
    else:

        submissions = submissions.all()

    return ResponseSchema(
        status="success",
        status_code=200,
        message="Submitted Quiz Fetched Successfully",
        data=submissions 
    )


@routers.put("/feedback/{id}",response_model=ResponseSchema[StudentEvaluation],status_code=200)
def update_feedback(id:int,feedback : StudentEvaluation , db: Session=Depends(get_db)):

    student_answer = db.query(StudentAnswer).filter(StudentAnswer.id==id).first()

    quiz_id = student_answer.question.quiz_id
    actual_marks = (
        db.query(func.sum(Questions.points))
        .filter(Questions.quiz_id == quiz_id)
        .scalar()
    ) or 0
   

    if not student_answer:
        return ResponseSchema(
            status="Error",
            status_code=404,
            message="Answer not found",
            data=None
        )

    answer_data = feedback.model_dump()



    for key,val in answer_data.items():
        setattr(student_answer, key,val)


    db.commit()
    db.refresh(student_answer)

    

    total_marks = (
        db.query(func.sum(StudentAnswer.points))
            .join(StudentQuizSubmission, StudentAnswer.submission_id == StudentQuizSubmission.id)
            .filter(
                StudentQuizSubmission.quiz_id == quiz_id,
                StudentQuizSubmission.student_id == student_answer.student_submission.student_id
            )
            .scalar()
        ) or 0
    
    total_percentage = (total_marks / actual_marks) * 100 if actual_marks else 0
    

    submission = student_answer.student_submission

    submission.total_score = total_marks
    submission.status = (
        QuizStatus.FAIL if total_percentage < 50 else QuizStatus.PASS
    )

    db.commit()
    db.refresh(submission)
    
    return ResponseSchema(
            status="Success",
            status_code=200,
            message="Feedback added",
            data=answer_data
        )