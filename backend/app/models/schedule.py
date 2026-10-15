import enum
from sqlalchemy import String, Integer, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class LessonType(str, enum.Enum):
    LESSON = "lesson"           
    CONSULTATION = "consult"     
    CIRCLE = "circle"          

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    day_of_week: Mapped[int] = mapped_column(Integer)    
    lesson_number: Mapped[int] = mapped_column(Integer, nullable=True) 
    
    subject: Mapped[str] = mapped_column(String(100))   
    teacher_name: Mapped[str] = mapped_column(String(100)) 
    classroom: Mapped[str] = mapped_column(String(20))   
    
    start_time: Mapped[str] = mapped_column(String(10))   
    end_time: Mapped[str] = mapped_column(String(10))    
    
    lesson_type: Mapped[LessonType] = mapped_column(
        String(20), default=LessonType.LESSON, server_default=LessonType.LESSON.value
    )

    
    material_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    material_title: Mapped[str | None] = mapped_column(String(150), nullable=True) 

    def __repr__(self) -> str:
        return f"<Schedule day={self.day_of_week} subject='{self.subject}' type={self.lesson_type.value}>"
