import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_submit_and_get_pereval():
    payload = {
        "user": {
            "email": "testuser@example.com",
            "family_name": "Иванов",
            "name": "Иван",
            "patronymic": "Иванович",
            "phone": "89999999999"
        },
        "beauty_title": "пер.",
        "title": "Тестовый перевал",
        "other_titles": "тест",
        "connect": "связь",
        "add_time": "2023-01-01 10:00:00",
        "coords": {
            "latitude": 45.0,
            "longitude": 7.0,
            "height": 1200
        },
        "level": {
            "winter": "1A",
            "summer": "1A",
            "autumn": "1A",
            "spring": "1A"
        },
        "images": []
    }

    response = client.post("/submitData/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    pereval_id = data["id"]

    get_response = client.get(f"/submitData/{pereval_id}")
    assert get_response.status_code == 200
    result = get_response.json()
    assert result["title"] == "Тестовый перевал"