from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    target_grade = Column(String, default="all")
    deadline = Column(String, default="3 дня")
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
