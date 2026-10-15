import os
import secrets
import smtplib
import hashlib
import hmac
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from email.message import EmailMessage
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, engine
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Auth"])
_executor = ThreadPoolExecutor(max_workers=2)

_HERE = Path(__file__).resolve()
_ENV_CANDIDATES = [_HERE.parents[3] / ".env", _HERE.parents[2] / ".env", Path.cwd() / ".env"]
try:
    from dotenv import load_dotenv
    for _env_file in _ENV_CANDIDATES:
        if _env_file.is_file():
            load_dotenv(_env_file, override=False)
            break
except ImportError:
    pass

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mail.ru").strip().strip("'\"")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465").strip().strip("'\""))
SMTP_USER = os.getenv("SMTP_USER", "").strip().strip("'\"")
SMTP_PASSWORD = (os.getenv("SMTP_PASSWORD") or os.getenv("SMTP_PASS") or "").strip().strip("'\"")
SMTP_FROM = (os.getenv("SMTP_FROM") or SMTP_USER).strip().strip("'\"")

async def ensure_user_profile_columns():
    async with engine.begin() as conn:
        result = await conn.execute(text("PRAGMA table_info(users)"))
        columns = {row[1] for row in result.fetchall()}
        if "nickname" not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN nickname VARCHAR(40)"))
        if "nickname_changed_at" not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN nickname_changed_at DATETIME"))

@router.on_event("startup")
async def auth_startup():
    await ensure_user_profile_columns()

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"pbkdf2_sha256${salt.hex()}${digest.hex()}"

def verify_password(password: str, stored: str) -> bool:
    try:
        if not stored.startswith("pbkdf2_sha256$"):
            return hmac.compare_digest(password, stored)
        _, salt_hex, expected = stored.split("$", 2)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 310_000).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False

def _send_code_sync(address: str, code: str) -> None:
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials are not loaded")
    message = EmailMessage()
    message["Subject"] = "Код подтверждения — Школа.MAX"
    message["From"] = SMTP_FROM
    message["To"] = address
    message.set_content(f"Код подтверждения: {code}\nСрок действия — 10 минут.")
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.ehlo(); server.starttls(); server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)

async def send_code(address: str, code: str) -> None:
    try:
        await asyncio.get_running_loop().run_in_executor(_executor, _send_code_sync, address, code)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Не удалось отправить email ({type(exc).__name__})") from exc

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    grade: str = Field(min_length=1)
    role: str = "student"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)

class NicknameRequest(BaseModel):
    nickname: str = Field(min_length=2, max_length=40)

def public_user(user: User) -> dict:
    now = datetime.utcnow()
    next_change = user.nickname_changed_at + timedelta(days=10) if user.nickname_changed_at else None
    role_norm = str(user.role or "student").strip().lower()
    if role_norm not in {"student", "teacher", "admin"}:
        role_norm = "student"
    return {
        "id": user.id,
        "sferum_id": user.sferum_id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "grade": user.grade,
        "role": role_norm,
        "nickname": user.nickname or f"{user.first_name} {user.last_name}".strip(),
        "nickname_can_change_at": next_change.isoformat() if next_change else None,
        "nickname_can_change": next_change is None or now >= next_change
    }

@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    email = str(data.email).strip().lower()
    role = str(data.role or "student").strip().lower()
    if role not in {"student", "teacher"}:
        role = "student"

    existing = await db.scalar(select(User).where(User.email == email))
    if existing:
        if not existing.is_verified:
            code = f"{secrets.randbelow(1_000_000):06d}"
            await send_code(email, code)
            existing.verification_code = code
            existing.role = role
            await db.commit()
            return {"success": True, "verification_required": True, "message": "Код отправлен повторно"}
        raise HTTPException(status_code=409, detail="Пользователь с такой почтой уже зарегистрирован")

    code = f"{secrets.randbelow(1_000_000):06d}"
    await send_code(email, code)
    user = User(
        email=email,
        password_hash=hash_password(data.password),
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        grade=data.grade.strip(),
        role=role,
        sferum_id=f"{role}_{secrets.token_hex(8)}",
        verification_code=code,
        is_verified=False,
        nickname=data.first_name.strip()
    )
    db.add(user)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return {"success": True, "verification_required": True, "message": "Код отправлен на почту"}

@router.post("/verify-code")
async def verify_code(data: VerifyRequest, db: AsyncSession = Depends(get_db)):
    email = str(data.email).strip().lower()
    user = await db.scalar(select(User).where(User.email == email))
    if not user or user.is_verified or not user.verification_code:
        raise HTTPException(status_code=400, detail="Регистрация не найдена или почта уже подтверждена")
    if not hmac.compare_digest(user.verification_code, data.code.strip()):
        raise HTTPException(status_code=400, detail="Неверный код подтверждения")
    user.is_verified = True
    user.verification_code = None
    await db.commit()
    return {"success": True, "message": "Почта подтверждена. Теперь войдите."}

@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    email = str(data.email).strip().lower()
    user = await db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(data.password, user.password_hash or ""):
        raise HTTPException(status_code=401, detail="Неверная почта или пароль")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Сначала подтвердите почту кодом из письма")
    if not (user.password_hash or "").startswith("pbkdf2_sha256$"):
        user.password_hash = hash_password(data.password)
        await db.commit()
    return {"success": True, "access_token": secrets.token_urlsafe(32), "user": public_user(user)}

@router.patch("/me/nickname")
async def change_nickname(data: NicknameRequest, user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    now = datetime.utcnow()
    if user.nickname_changed_at and now < user.nickname_changed_at + timedelta(days=10):
        next_date = user.nickname_changed_at + timedelta(days=10)
        raise HTTPException(status_code=429, detail=f"Никнейм можно будет изменить {next_date.strftime('%d.%m.%Y %H:%M')}")
    nickname = data.nickname.strip()
    if len(nickname) < 2:
        raise HTTPException(status_code=422, detail="Никнейм должен содержать минимум 2 символа")
    user.nickname = nickname
    user.nickname_changed_at = now
    await db.commit()
    await db.refresh(user)
    return {"success": True, "user": public_user(user)}

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = (await db.execute(select(User))).scalars().all()
    return [public_user(user) for user in users]

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await db.delete(user)
    await db.commit()
    return {"success": True}
