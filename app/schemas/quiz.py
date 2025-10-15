from typing import Optional
from pydantic import BaseModel


class QuizBase(BaseModel):

    title: str
    description : str
    passing_criteria : Optional[str] = None


class QuizCreate(QuizBase):
    pass
    
class QuizResponse(QuizBase):

    id : int

    class Config:
        from_attributes = True

class QuizUpdate(BaseModel):

    title : Optional[str] = None
    description : Optional[str] = None
    passing_criteria : Optional[str] = None
    