from sqlalchemy import Column, ForeignKey, Integer,DateTime,Boolean, Text
from app.models.quiz import Base,Quiz,Questions
from datetime import datetime
from sqlalchemy.orm import relationship
from enum import Enum 
from sqlalchemy.dialects.postgresql import ENUM
from app.models.accounts import Student

class QuizStatus(str , Enum):
    
    PASS = "pass",
    FAIL = "Fail"




class StudentQuizSubmission(Base):

    __tablename__ = "student_quiz_submission"

    id = Column(Integer,primary_key=True,index=True)
    student_id = Column(Integer,ForeignKey("students.id"), nullable=False)

    student = relationship("Student", back_populates="submissions")

    quiz_id = Column(Integer,ForeignKey('quiz.id'))
    quiz = relationship("Quiz", back_populates="submissions")

    created_at = Column(DateTime,default=datetime.now())
    total_score = Column(Integer,nullable=False)
    status = Column(ENUM(QuizStatus), nullable = False)
    attempt = Column(Integer)

    answers = relationship('StudentAnswer', back_populates="student_submission")


class StudentAnswer(Base):

    __tablename__ = "student_answer"
    
    id = Column(Integer,primary_key=True,index=True)
    submission_id = Column(Integer,ForeignKey('student_quiz_submission.id'),nullable=False)
    question_id = Column(Integer,ForeignKey('questions.id'),nullable=False)
    student_answer = Column(Text,nullable=False)
    is_correct = Column(Boolean,nullable=True)
    points = Column(Integer,nullable=True)
    feed_back = Column(Text,nullable=True)

    student_submission = relationship('StudentQuizSubmission')
    question = relationship("Questions", back_populates="student_answers") 


