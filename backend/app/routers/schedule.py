from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models.schedule import Schedule, LessonType
from app.schemas.schedule import ScheduleCreate, ScheduleResponse

router = APIRouter(prefix="/api/schedule", tags=["Schedule & Materials"])


@router.get("/{day_id}", response_model=List[ScheduleResponse])
async def get_schedule_by_day(day_id: int, db: AsyncSession = Depends(get_db)):
    if day_id < 1 or day_id > 7:
        raise HTTPException(status_code=400, detail="Неверный день недели (должен быть 1-7)")
        
    result = await db.execute(
        select(Schedule)
        .filter(Schedule.day_of_week == day_id)
        .order_by(Schedule.lesson_number.asc(), Schedule.start_time.asc())
    )
    return result.scalars().all()


@router.get("/extra/all", response_model=List[ScheduleResponse])
async def get_extra_activities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Schedule)
        .filter(Schedule.lesson_type != LessonType.LESSON)
        .order_by(Schedule.day_of_week.asc())
    )
    return result.scalars().all()


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule_item(item: ScheduleCreate, db: AsyncSession = Depends(get_db)):
    new_item = Schedule(**item.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item
