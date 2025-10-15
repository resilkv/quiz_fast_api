from sqlalchemy import Column, Integer, String, Boolean
from app.models.quiz import Base
from sqlalchemy.orm import relationship

class Student(Base):

    __tablename__="students"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255))
    hashed_password  = Column(String(255))
    username =  Column(String(255),unique=True)
    is_active = Column(Boolean, default=True)

    submissions = relationship("StudentQuizSubmission", back_populates="student")

