import enum
from sqlalchemy import String, Integer, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

# Тип занятия
class LessonType(str, enum.Enum):
    LESSON = "lesson"           # Обычный урок
    CONSULTATION = "consult"     # Консультация
    CIRCLE = "circle"           # Кружок / Секция

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    day_of_week: Mapped[int] = mapped_column(Integer)    # 1 - Понедельник, 7 - Воскресенье
    lesson_number: Mapped[int] = mapped_column(Integer, nullable=True) # Номер урока (1-8)
    
    subject: Mapped[str] = mapped_column(String(100))    # Предмет
    teacher_name: Mapped[str] = mapped_column(String(100)) # ФИО учителя
    classroom: Mapped[str] = mapped_column(String(20))    # Кабинет
    
    start_time: Mapped[str] = mapped_column(String(10))   # Время начала (напр. "08:30")
    end_time: Mapped[str] = mapped_column(String(10))     # Время окончания
    
    lesson_type: Mapped[LessonType] = mapped_column(
        String(20), default=LessonType.LESSON, server_default=LessonType.LESSON.value
    )

    # Поля для Медиатеки
    material_link: Mapped[str | None] = mapped_column(String(500), nullable=True) # Ссылка на файл/презентацию
    material_title: Mapped[str | None] = mapped_column(String(150), nullable=True) # Название материала

    def __repr__(self) -> str:
        return f"<Schedule day={self.day_of_week} subject='{self.subject}' type={self.lesson_type.value}>"
