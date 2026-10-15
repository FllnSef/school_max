import os
import httpx
from typing import Dict, Any, List


ESIA_AUTH_URL = os.getenv("ESIA_AUTH_URL", "https://esia.gosuslugi.ru/aas/oauth2/ac")
MY_SCHOOL_API_URL = os.getenv("MY_SCHOOL_API_URL", "https://api.myschool.edu.ru/v1")


MOCK_ESIA_STUDENTS_DATABASE = {
    "10001234567": {  # СНИЛС ученика 1
        "fio": "Савинов Григорий",
        "grade": "11 «Б»",
        "school": "МБОУ СОШ № 1",
        "grades": [
            {"subject": "Алгебра и начала анализа", "average_score": 4.86, "latest_grade": 5, "quarter": 1},
            {"subject": "Физика (профиль)", "average_score": 4.67, "latest_grade": 5, "quarter": 1},
            {"subject": "Информатика", "average_score": 5.00, "latest_grade": 5, "quarter": 1},
            {"subject": "Русский язык", "average_score": 4.33, "latest_grade": 4, "quarter": 1},
            {"subject": "История России", "average_score": 4.75, "latest_grade": 5, "quarter": 1},
            {"subject": "Обществознание", "average_score": 4.50, "latest_grade": 5, "quarter": 1},
            {"subject": "Химия", "average_score": 4.80, "latest_grade": 5, "quarter": 1},
        ]
    },
    "default": {
        "fio": "Ученик Госуслуг",
        "grade": "11 класс",
        "school": "ФГИС Моя Школа",
        "grades": [
            {"subject": "Алгебра", "average_score": 4.75, "latest_grade": 5, "quarter": 1},
            {"subject": "Физика", "average_score": 4.50, "latest_grade": 5, "quarter": 1},
            {"subject": "Информатика", "average_score": 5.00, "latest_grade": 5, "quarter": 1},
            {"subject": "Русский язык", "average_score": 4.25, "latest_grade": 4, "quarter": 1},
        ]
    }
}

async def authenticate_via_esia(snils: str = "10001234567") -> Dict[str, Any]:
    """
    Авторизация через шлюз Госуслуг и получение персонального дневника из ФГИС «Моя Школа»
    """
    profile = MOCK_ESIA_STUDENTS_DATABASE.get(snils, MOCK_ESIA_STUDENTS_DATABASE["default"])
    return {
        "esia_id": f"esia_oid_{snils}",
        "snils": snils,
        "full_name": profile["fio"],
        "grade": profile["grade"],
        "school": profile["school"],
        "grades": profile["grades"]
    }
