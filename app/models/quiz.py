import enum
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from enum import Enum 
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

Base=declarative_base()

class Quiz(Base):

    __tablename__ = "quiz"

    id = Column(Integer,primary_key=True,index=True)
    title=  Column(String,nullable=False)
    description = Column(Text)  
    passing_criteria = Column(Text)


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
    options = Column(Text, nullable=True)
    correct_answer = Column(Text, nullable=True)
    quiz = relationship("Quiz", back_populates="questions")
