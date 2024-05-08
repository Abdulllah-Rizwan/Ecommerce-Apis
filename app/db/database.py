from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..settings import setting


SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}';

       
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close();
 

