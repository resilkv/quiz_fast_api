import enum
from pydantic import Json
from sqlalchemy import Column, Integer, String, Text,JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from enum import Enum 
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import ARRAY


Base=declarative_base()

class Quiz(Base):

    __tablename__ = "quiz"

    id = Column(Integer,primary_key=True,index=True)
    title=  Column(String,nullable=False)
    description = Column(Text)  
    passing_criteria = Column(Text)
    questions = relationship("Questions", back_populates="quiz", cascade="all, delete-orphan")
    submissions = relationship("StudentQuizSubmission", back_populates="quiz")


class QuestionType(str, Enum):

    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER ="short_answer"
    LONG_ANSWER = "long_answer"


class Questions(Base):

    __tablename__="questions"

    id = Column(Integer,primary_key=True,index=True)
    quiz_id = Column(Integer,ForeignKey("quiz.id"))
    question = Column(Text, nullable=False)
    type = Column(ENUM(QuestionType), nullable = False)
    options = Column(ARRAY(String), nullable=True)
    correct_answer = Column(Text, nullable=True)
    quiz = relationship("Quiz", back_populates="questions")

    points = Column(Integer,nullable=True)
    metadata_value = Column(JSON,nullable=True)
    student_answers = relationship('StudentAnswer', back_populates="question")
