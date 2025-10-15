from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.questions import QuestionResponse
from app.schemas.quiz import QuizBase


class AnswerSubmission(BaseModel):

    question_id : int
    answer : str

class StudentAnswerSchema(BaseModel):

    answer : List[AnswerSubmission]
   

class AnswerSubmissionSchema(BaseModel):

    id : int
    status: str

class StudentAnswerResponse(BaseModel):
    id: int
    submission_id: int
    question_id: int
    student_answer: str
    is_correct: Optional[bool]
    points: Optional[int]
    feed_back: Optional[str]
    question  : Optional[QuestionResponse] = None
    
    class Config:
        from_attributes = True



class AnswerSubmissionResponse(BaseModel):

    id : int
    student_id : int
    quiz_id : int
    quiz : Optional[QuizBase]
    created_at : datetime
    status : str
    total_score : int
    answers: List[StudentAnswerResponse] = []

class StudentEvaluation(BaseModel):

    feed_back : str
    points : Optional[str] = None
    

    

