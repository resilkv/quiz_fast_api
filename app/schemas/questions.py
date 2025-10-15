from enum import Enum
from typing import List, Optional
from pydantic import BaseModel,validator


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"

class Question(BaseModel):

    quiz_id : int
    question : str
    type : QuestionType
    options : Optional[List[str]] = None
    correct_answer : Optional[str] = None
    points : int
    metadata_value : Optional[dict]
    



class QuestionCreate(Question):

    @validator('correct_answer')
    def validate_correct_answer(cls,v,values):
        qtype=values.get('type')
        options = values.get('options')

        if qtype == QuestionType.MULTIPLE_CHOICE:
            if not options:
                raise ValueError('Options needs to be provided')
            if v not in options:
                raise ValueError('Correct answer should be in the list')
        return v

class QuestionResponse(Question):
    id : int
    question : str
    type : QuestionType
    options : Optional[List[str]] = None
    correct_answer : Optional[str] = None
    points : Optional[int] = None
    metadata_value : Optional[dict] = None

    pass


class QuestionBulk(BaseModel):

   
    question : str
    type : QuestionType
    options : Optional[List[str]] = None
    correct_answer : Optional[str] = None
    points : int
    metadata_value : Optional[dict] = None

class BulkQuestionCreate(BaseModel):
    quiz_id : int 
    questions : List[QuestionBulk]



class QuestionUpdate(BaseModel):

    quiz_id : Optional[int] = None
    question : Optional[str] = None
    type : Optional[str] = None
    options : Optional[List[str]] = None
    correct_answer : Optional[str] = None
    points : int = None
    metadata_value : Optional[dict] = None