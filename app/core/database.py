from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import create_engine

database_url="postgresql://postgres:password@localhost:5432/fast_api_quiz"
engine=create_engine(database_url)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)



def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()