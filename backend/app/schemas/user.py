from pydantic import BaseModel
from typing import Optional

class SferumAuthRequest(BaseModel):
    init_data: Optional[str] = None  # Строка window.Telegram.WebApp.initData / MAX

class UserResponse(BaseModel):
    id: int
    sferum_id: str
    first_name: str
    last_name: Optional[str]
    grade: str
    role: str
    school_name: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
