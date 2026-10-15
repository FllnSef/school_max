from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_assistant

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])

class AIAnalyzeRequest(BaseModel):
    text: str

@router.post("/analyze")
async def analyze_task(data: AIAnalyzeRequest):
    if not data.text or len(data.text) < 10:
        raise HTTPException(status_code=400, detail="Текст задания слишком короткий")
    
    analysis = await ai_assistant.analyze_homework(data.text)
    return analysis
