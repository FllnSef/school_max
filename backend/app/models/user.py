import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    sferum_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    grade = Column(String, default="11А")
    role = Column(String, default="student")
    school_name = Column(String, default="МБОУ СОШ №154")
    verification_code = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    # Nickname changes are limited by the backend to once per 10 days.
    nickname = Column(String(40), nullable=True)
    nickname_changed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
