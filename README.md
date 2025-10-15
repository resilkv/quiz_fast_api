# Quiz API

A FastAPI backend system for a Quiz application.

This application allows users to create quizzes, add questions to each quiz, and enables students to attend quizzes. Based on their performance, students are evaluated and ranked.

**API Documentation:** Complete documentation for all endpoints is available via **Swagger UI**, accessible at `/docs` once the server is running.

## Features

## Create and manage quizzes
### Add multiple types of questions to quizzes:
1. Multiple Choice
2. True/False
3. Short Answer
4. Long Answer
### Track student performance
### Add feedback for student answers
### Evaluate and rank students based on quiz results

## Technology Stack

1. Framework: FastAPI
2. Database: PostgreSQL
3. ORM & Migrations: SQLAlchemy and Alembic
4. Containerization: Docker, Docker Compose

## Database Design

The application mainly uses four tables:

1. Quiz Table: Stores different quizzes and their criteria.
2. Question Table: Stores questions associated with each quiz.
3. Student Answers Table: Tracks answers submitted by students and allows teachers to add feedback.
4. Student Quiz Performance Table: Connects all data related to a student for a particular quiz.

## Prerequisites

1. Basic understanding of REST APIs
2. Knowledge of FastAPI


## Docker Setup

To run the application using Docker:

Pull the Docker Image

docker pull kvresil/fast_api_quiz:v.0.1

Build and run containers:


docker-compose --build
docker-compose up

## Environment Variables:

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

## Local Development

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

## Addition :

Authentication Flow
Student Signup & Login

A student can register with their username, and password.

After login, the system returns a JWT Token.

This token must be used in the Authorization Header for all quiz-related requests.

Example:

Authorization: Bearer <your_token_here>
