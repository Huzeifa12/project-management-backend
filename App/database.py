from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


sqlalchemy_url= f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}"

engine=create_engine(sqlalchemy_url)
sessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()








    