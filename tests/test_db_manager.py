import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app.db_manager import DBManager

@pytest.fixture
def db():
    db = DBManager()
    yield db
    db.close()

def test_add_and_get_user(db):
    user_id = db.add_user(
        email="testuser2@example.com",
        name="Анна",
        family_name="Петрова",
        patronymic="Ивановна",
        phone="81234567890"
    )
    assert isinstance(user_id, int)

def test_add_coords(db):
    coord_id = db.add_coords(latitude=55.75, longitude=37.61, height=500)
    assert isinstance(coord_id, int)

def test_add_pereval(db):
    user_id = db.add_user(
        email="testuser3@example.com",
        name="Олег",
        family_name="Сидоров",
        patronymic="Викторович",
        phone="80001234567"
    )
    coord_id = db.add_coords(latitude=42.0, longitude=45.0, height=1500)
    pereval_id = db.add_pereval(
        user_id=user_id,
        coord_id=coord_id,
        beauty_title="пер.",
        title="Перевал Тестовый",
        other_titles="Альтернатива",
        connect="связь есть",
        add_time="2023-02-02 12:00:00",
        level_winter="1B",
        level_summer="1A",
        level_autumn="1A",
        level_spring="1B"
    )
    assert isinstance(pereval_id, int)
