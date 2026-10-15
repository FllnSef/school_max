from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import date
from app.database import get_db
from app.models.menu import CanteenMenu, MealBooking, MealType
from app.schemas.menu import MenuCreate, MenuResponse, BookingCreate, BookingResponse

router = APIRouter(prefix="/api/menu", tags=["Canteen & Nutrition"])

# 1. Получить меню на конкретную дату (по умолчанию на сегодня)
@router.get("/day/{request_date}", response_model=List[MenuResponse])
async def get_menu_by_date(request_date: date, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CanteenMenu).filter(CanteenMenu.menu_date == request_date)
    )
    return result.scalars().all()

# 2. Записаться на питание
@router.post("/book", response_model=BookingResponse)
async def book_meal(booking_data: BookingCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, нет ли уже такой записи у этого пользователя на эту дату
    existing = await db.execute(
        select(MealBooking).filter(
            MealBooking.user_id == booking_data.user_id,
            MealBooking.booking_date == booking_data.booking_date,
            MealBooking.meal_type == booking_data.meal_type
        )
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Вы уже записаны на этот прием пищи в этот день")

    new_booking = MealBooking(**booking_data.model_dump())
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    return new_booking

# 3. Добавить блюдо в меню (для Админа/Повара)
@router.post("/add-dish", response_model=MenuResponse)
async def create_menu_item(item: MenuCreate, db: AsyncSession = Depends(get_db)):
    new_dish = CanteenMenu(**item.model_dump())
    db.add(new_dish)
    await db.commit()
    await db.refresh(new_dish)
    return new_dish
