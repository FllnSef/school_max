import os
import httpx
import json
from typing import Dict, Any

class HomeworkAIService:
    def __init__(self):
        
        self.api_key = os.getenv("AI_API_KEY", "demo_key")
        self.ai_url = "https://api.proxy.ai/v1/chat/completions" # Пример шлюза

    async def analyze_homework(self, raw_text: str) -> Dict[str, Any]:
        """
        Использует LLM для анализа текста задания и превращения его в структурированный план.
        """
        prompt = f"""
        Ты — интеллектуальный ассистент платформы Школа.MAX. 
        Проанализируй текст домашнего задания и выведи ответ строго в формате JSON.
        Текст задания: "{raw_text}"
        
        Нужный формат JSON:
        {{
          "subject": "Название предмета",
          "title": "Краткое название задачи",
          "essence": "Суть задания одним предложением",
          "steps": ["Шаг 1", "Шаг 2", "Шаг 3"],
          "deadline_suggestion": "Предполагаемый срок (например, 3 дня)"
        }}
        """

        
        if self.api_key == "demo_key":
            return self._get_mock_response(raw_text)

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.ai_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]}
                )
                return resp.json()
        except Exception:
            return self._get_mock_response(raw_text)

    def _get_mock_response(self, text: str) -> Dict[str, Any]:
        """Умная заглушка, если нейросеть не подключена"""
        return {
            "subject": "Физика",
            "title": "Лабораторная работа по динамике",
            "essence": "Изучение законов Ньютона с использованием измерительных приборов.",
            "steps": [
                "Прочитать теорию на стр. 45-50",
                "Выписать формулы ускорения и силы",
                "Заполнить таблицу измерений из приложения №1",
                "Сформулировать вывод по графикам"
            ],
            "deadline_suggestion": "25 сентября"
        }

ai_assistant = HomeworkAIService()
