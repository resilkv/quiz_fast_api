from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"

class Question(BaseModel):

    quiz_id : int
    question : str
    type : QuestionType
    options : Optional[List[str]]
    correct_answer : Optional[str]



class QuestionCreate(Question):

    pass 

class QuestionResponse(Question):

    pass