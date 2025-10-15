from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import get_db
from app.core.response_schema import ResponseSchema
from app.models.accounts import Student
from app.schemas.accounts import StudentToken, Token, TokenData, User, UserInDB
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from fastapi import HTTPException, status

import os



SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()

router=APIRouter(
    
    prefix="/account",
    tags=["Authorization"]
)



password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db: Session = Depends(get_db)):

    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_str = credentials.credentials

    try:
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = db.query(Student).filter(Student.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

    

@router.post("/create-student",response_model=ResponseSchema[User],status_code=201)
def create_student(student: UserInDB,db: Session=Depends(get_db)):

    student_db = db.query(Student).filter(Student.username==student.username).first()
    if student_db:
        return ResponseSchema(
            status="error",
            status_code=404,
            message="Username already exists",
            error="Already Exists" 
        )
    hashed_password = get_password_hash(student.password)
    student = Student(
        username=student.username,
        hashed_password=hashed_password
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    return ResponseSchema(
            status="Success",
            status_code=200,
            message="Student added",
            error=None,
            data = student
        )

def authenticate_user(username: str, password: str,db: Session=Depends(get_db)):
    user = get_user(get_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/token",response_model=ResponseSchema[StudentToken],status_code=200)
async def login_for_access_token(student: UserInDB,db: Session = Depends(get_db)):

    user =  db.query(Student).filter(Student.username==student.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = Token(access_token=access_token, token_type="bearer")

    return ResponseSchema(
        status="Success",
        status_code=200,
        message="Login Successful",
        error=None,
        data = token
    )