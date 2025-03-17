import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Create database engine
database_url = os.getenv('DATABASE_URL')
if not database_url:
    database_url = 'sqlite:///jobs.db'

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    company = Column(String(100))
    salary = Column(String(100))
    requirements = Column(Text)
    link = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100))
    message_id = Column(Integer, unique=True)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создаем подключение к базе данных
def init_db():
    Base.metadata.create_all(engine)

# Функция для создания новой вакансии
def create_job(
    title: str,
    company: str = None,
    salary: str = None,
    requirements: str = None,
    link: str = None,
    source: str = None,
    message_id: int = None
):
    session = SessionLocal()
    try:
        job = Job(
            title=title,
            company=company,
            salary=salary,
            requirements=requirements,
            link=link,
            source=source,
            message_id=message_id
        )
        session.add(job)
        session.commit()
        return job
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Функция для проверки существования вакансии
def job_exists(message_id: int) -> bool:
    session = SessionLocal()
    try:
        exists = session.query(Job).filter_by(message_id=message_id).first() is not None
        return exists
    finally:
        session.close()

def get_all_jobs():
    session = SessionLocal()
    try:
        return session.query(Job).all()
    finally:
        session.close() 