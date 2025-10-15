Quiz API

A FastAPI backend system for a Quiz application.

This application allows users to create quizzes, add questions to each quiz, and enables students to attend quizzes. Based on their performance, students are evaluated and ranked.

Features

# Create and manage quizzes
# Add multiple types of questions to quizzes:
    Multiple Choice
    True/False
    Short Answer
    Long Answer
# Track student performance
# Add feedback for student answers
# Evaluate and rank students based on quiz results

## Technology Stack

Framework: FastAPI
Database: PostgreSQL
ORM & Migrations: SQLAlchemy and Alembic
Containerization: Docker, Docker Compose

Database Design

The application mainly uses four tables:

Quiz Table: Stores different quizzes and their criteria.
Question Table: Stores questions associated with each quiz.
Student Answers Table: Tracks answers submitted by students and allows teachers to add feedback.
Student Quiz Performance Table: Connects all data related to a student for a particular quiz.

Prerequisites

Basic understanding of REST APIs
Knowledge of FastAPI


Docker Setup

To run the application using Docker:

Pull the Docker Image

docker pull kvresil/fast_api_quiz:v.0.1

Build and run containers:


docker-compose --build
docker-compose up

Environment Variables:

Create a .env file inside the app folder with the following values:


DATABASE_URL= postgresql+psycopg2://<username>:<password>@db:5432/<db_name>
SECRET_KEY=''
POSTGRES_USER=''
POSTGRES_PASSWORD=''
POSTGRES_DB=''

DB_HOST=db
DB_PORT=''

APP_PORT=8000

Once the containers are up, access the API documentation at:
http://localhost:8000/docs

Local Development

Clone it from github

git clone https://github.com/resilkv/quiz_fast_api.git
cd quiz_fast_api


Create and configure .env with the same values as in Docker setup.

Install dependencies:

python -m venv venv
source venv/bin/activate  # Ubuntu
venv\Scripts\activate     # Windows

pip install -r requirements.txt

alembic upgrade head

Start the FastAPI server:

uvicorn app.main:app --reload

Access API docs:

http://localhost:8000/docs

Addition :

Authentication Flow
Student Signup & Login

A student can register with their username, and password.

After login, the system returns a JWT Token.

This token must be used in the Authorization Header for all quiz-related requests.

Example:

Authorization: Bearer <your_token_here>
