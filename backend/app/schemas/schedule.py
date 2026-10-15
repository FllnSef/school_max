from pydantic import BaseModel
from app.models.schedule import LessonType

class ScheduleBase(BaseModel):
    day_of_week: int
    lesson_number: int | None = None
    subject: str
    teacher_name: str
    classroom: str
    start_time: str
    end_time: str
    lesson_type: LessonType = LessonType.LESSON
    material_link: str | None = None
    material_title: str | None = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        from_attributes = True
