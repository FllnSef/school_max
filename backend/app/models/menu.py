import enum
from datetime import date
from sqlalchemy import String, Date, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# Тип приема пищи
class MealType(str, enum.Enum):
    BREAKFAST = "завтрак"
    LUNCH = "обед"
    SNACK = "полдник"

class CanteenMenu(Base):
    __tablename__ = "canteen_menu"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    menu_date: Mapped[date] = mapped_column(Date, index=True)  # Дата меню
    meal_type: Mapped[MealType] = mapped_column(String(20))     # Завтрак/Обед
    dish_name: Mapped[str] = mapped_column(String(200))        # Название блюда (напр. "Суп гороховый")
    description: Mapped[str | None] = mapped_column(String(500), nullable=True) # Состав / КБЖУ

    def __repr__(self) -> str:
        return f"<Menu {self.menu_date} {self.meal_type.value}: {self.dish_name}>"

class MealBooking(Base):
    __tablename__ = "meal_bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    booking_date: Mapped[date] = mapped_column(Date)           # На какую дату запись
    meal_type: Mapped[MealType] = mapped_column(String(20))     # Что именно заказано
    
    # Связь с пользователем
    user = relationship("User")

    def __repr__(self) -> str:
        return f"<Booking user={self.user_id} date={self.booking_date}>"
