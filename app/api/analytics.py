from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.sql import func
from app.core.database import get_db
from app.core.response_schema import ResponseSchema
from app.models.accounts import Student
from app.models.quiz import Quiz
from app.models.student import StudentQuizSubmission
from app.schemas.analytics import PlatformPerformance, QuizAnalytics, StudentRankingSchema


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/quiz-analytics",response_model=ResponseSchema[List[QuizAnalytics]],status_code=200)
def get_quiz_analytics(db:Session=Depends(get_db)):

    quizzes = db.query(Quiz).all()
    analytics = []


    for quiz in quizzes:

        submissions = db.query(StudentQuizSubmission).filter(StudentQuizSubmission.quiz_id == quiz.id)
        total_attempts = submissions.count()

        if total_attempts == 0:
            analytics.append({
                "quiz_id": quiz.id,
                "quiz_title": quiz.title,
                "total_attempts": 0,
                "average_score": 0.0,
                "highest_score":0,
                "lowest_score":0,
            })
            continue
        
        avg_score = db.query(func.avg(StudentQuizSubmission.total_score).label('average')).filter(StudentQuizSubmission.quiz_id==quiz.id).scalar()
        highest_score = db.query(func.max(StudentQuizSubmission.total_score)).filter(StudentQuizSubmission.quiz_id == quiz.id).scalar() or 0
        lowest_score = db.query(func.min(StudentQuizSubmission.total_score)).filter(StudentQuizSubmission.quiz_id == quiz.id).scalar() or 0
        analytics.append({
            "quiz_id": quiz.id,
            "quiz_title": quiz.title,
            "total_attempts": total_attempts,
            "average_score": float(round(avg_score, 2)),
            "highest_score": highest_score,
            "lowest_score": lowest_score,
           
        })

   
    return ResponseSchema(
            status="success",
            status_code=200,
            message="Quiz Analytics created successfully",
            data=analytics
        )


@router.get("/student-ranking",response_model=ResponseSchema[List[StudentRankingSchema]],status_code=200)
def get_quiz_analytics(db:Session=Depends(get_db)):

    
    submissions = (db.query(Student.username,func.sum(StudentQuizSubmission.total_score).label("total_score")).join(Student, Student.id == StudentQuizSubmission.student_id).group_by(Student.id).all())
    
    totals = {student: total_score for student, total_score in submissions}

    ranked_students = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    rankings = [
        {
            "rank": rank,
            "username": student,
            "total_score": total_score
        }
        for rank, (student, total_score) in enumerate(ranked_students, start=1)
    ]

    return ResponseSchema(
        status="success",
        status_code=200,
        message="Quiz Analytics created successfully",
        data=rankings
    )

@router.get("/platform-performance",response_model=ResponseSchema[PlatformPerformance],status_code=200)
def get_quiz_analytics(db:Session=Depends(get_db)):
    
    total_student = db.query(func.count(Student.id)).scalar()
    total_quizes =db.query(func.count(Quiz.id)).scalar()
    total_attended_quiz = db.query(func.count(func.distinct(StudentQuizSubmission.quiz_id))).scalar()

    data = {
        "total_student":total_student,
        "total_quizes":total_quizes,
        "total_attended_quiz":total_attended_quiz,
    }   

    return ResponseSchema(
        status="success",
        status_code=200,
        message="Platform Analytics created successfully",
        data=data
    )
