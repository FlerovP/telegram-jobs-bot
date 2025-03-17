from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Создаем базовый класс для моделей
Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    description = Column(Text)
    salary = Column(String(255))
    location = Column(String(255))
    requirements = Column(Text)
    contact = Column(String(255))
    telegram_message_id = Column(Integer)
    telegram_chat_id = Column(Integer)
    source_link = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>"

# Создаем подключение к базе данных
engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker(bind=engine)

# Создаем таблицы
def init_db():
    Base.metadata.create_all(engine)

# Функция для создания новой вакансии
def create_job(
    title: str,
    company: str = None,
    description: str = None,
    salary: str = None,
    location: str = None,
    requirements: str = None,
    contact: str = None,
    telegram_message_id: int = None,
    telegram_chat_id: int = None,
    source_link: str = None
):
    session = SessionLocal()
    try:
        job = Job(
            title=title,
            company=company,
            description=description,
            salary=salary,
            location=location,
            requirements=requirements,
            contact=contact,
            telegram_message_id=telegram_message_id,
            telegram_chat_id=telegram_chat_id,
            source_link=source_link
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
def job_exists(telegram_message_id: int, telegram_chat_id: int) -> bool:
    session = SessionLocal()
    try:
        exists = session.query(Job).filter_by(
            telegram_message_id=telegram_message_id,
            telegram_chat_id=telegram_chat_id
        ).first() is not None
        return exists
    finally:
        session.close()

# Функция для получения всех активных вакансий
def get_active_jobs():
    session = SessionLocal()
    try:
        return session.query(Job).filter_by(is_active=True).all()
    finally:
        session.close() 