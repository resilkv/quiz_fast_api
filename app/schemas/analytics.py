from pydantic import BaseModel

class QuizAnalytics(BaseModel):

    quiz_id : int
    quiz_title : str
    total_attempts : int
    average_score : float
    highest_score : int
    lowest_score : int


class StudentRankingSchema(BaseModel):

    username: str
    total_score: int
    rank: int


class PlatformPerformance(BaseModel):

    
    total_student : int
    total_quizes : int
    total_attended_quiz : int
