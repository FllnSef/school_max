from datetime import date
from pydantic import BaseModel
from app.models.menu import MealType


class MenuBase(BaseModel):
    menu_date: date
    meal_type: MealType
    dish_name: str
    description: str | None = None

class MenuCreate(MenuBase):
    pass

class MenuResponse(MenuBase):
    id: int
    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    user_id: int
    booking_date: date
    meal_type: MealType

class BookingResponse(BookingCreate):
    id: int
    class Config:
        from_attributes = True
