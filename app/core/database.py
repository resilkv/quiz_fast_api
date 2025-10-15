from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="app/.env") 

database_url=os.environ.get('DATABASE_URL')
engine=create_engine(database_url)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)



def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()