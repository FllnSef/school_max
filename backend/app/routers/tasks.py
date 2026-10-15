from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import Optional

from app.database import get_db, engine
from app.models.task import Task
from app.models.user import User

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

# Автоматически добавляем колонку target_grade в SQLite при запуске, если её нет
async def ensure_target_grade_column():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE tasks ADD COLUMN target_grade VARCHAR DEFAULT 'all'"))
        except Exception:
            pass

class TaskCreateRequest(BaseModel):
    subject: str
    title: str
    description: Optional[str] = ""
    target_grade: str = "all"
    deadline: Optional[str] = "3 дня"
    user_id: Optional[int] = None

@router.on_event("startup")
async def on_startup():
    await ensure_target_grade_column()

# Публикация задачи (доступна учителю и администратору)
@router.post("")
@router.post("/")
async def create_task(data: TaskCreateRequest, db: AsyncSession = Depends(get_db)):
    await ensure_target_grade_column()

    if data.user_id:
        res = await db.execute(select(User).where(User.id == data.user_id))
        author = res.scalars().first()
        if author:
            user_role = str(author.role).lower()
            if "admin" not in user_role and "teacher" not in user_role and "учитель" not in user_role and "админ" not in user_role:
                raise HTTPException(status_code=403, detail="Только учитель или администратор могут публиковать задания")

    task = Task(
        subject=data.subject.strip(),
        title=data.title.strip(),
        description=data.description.strip() if data.description else "",
        target_grade=data.target_grade.strip(),
        deadline=data.deadline.strip() if data.deadline else "3 дня",
        status="pending"
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return {
        "success": True,
        "message": f"Задание успешно опубликовано для класса {task.target_grade}",
        "task": {
            "id": task.id,
            "subject": task.subject,
            "title": task.title,
            "description": task.description,
            "target_grade": task.target_grade,
            "deadline": task.deadline,
            "status": task.status
        }
    }

# Получение задач с фильтрацией по классу ученика
@router.get("")
@router.get("/")
async def get_tasks(grade: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    await ensure_target_grade_column()

    query = select(Task).order_by(Task.id.desc())
    result = await db.execute(query)
    all_tasks = result.scalars().all()

    clean_grade = (grade or "").replace(" ", "").upper()

    output = []
    for t in all_tasks:
        t_grade = getattr(t, "target_grade", "all") or "all"
        t_grade_clean = t_grade.replace(" ", "").upper()

        if not clean_grade or t_grade_clean == "ALL" or clean_grade == "ALL" or t_grade_clean == clean_grade:
            output.append({
                "id": t.id,
                "subject": t.subject,
                "title": t.title,
                "description": t.description or "",
                "target_grade": t_grade,
                "deadline": t.deadline or "3 дня",
                "status": t.status or "pending"
            })
    return output
