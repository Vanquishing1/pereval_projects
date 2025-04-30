# Pereval Project

## Описание

**Pereval Project** — это REST API для подачи данных о перевалах.
Проект позволяет добавлять новые перевалы, получать их по идентификатору или email пользователя, а также обновлять информацию о перевале (при условии, что статус записи "new").

## Технологии

- Python 3.11+
- FastAPI
- PostgreSQL
- psycopg2
- Pydantic

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <https://github.com/Vanquishing1/pereval_projects>
   cd pereval_project
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/macOS
   venv\Scripts\activate     # для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте переменные окружения (`.env` файл):
   ```
   FSTR_DB_NAME=ваше_имя_базы
   FSTR_DB_LOGIN=логин
   FSTR_DB_PASS=пароль
   FSTR_DB_HOST=хост
   FSTR_DB_PORT=порт
   ```



## Запуск проекта

```bash
uvicorn app.main:app --reload --host 127.0.0.1
```

Проект будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Документация Swagger автоматически доступна по адресу:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Основные эндпоинты

| Метод | URL                        | Описание |
|:------|:---------------------------|:---------|
| `POST` | `/submitData/` | Добавить новый перевал |
| `GET` | `/submitData/{pereval_id}` | Получить перевал по ID |
| `PATCH` | `/submitData/{pereval_id}` | Обновить информацию о перевале |
| `GET` | `/submitData/?user__email=example@mail.com` | Получить перевалы пользователя по email |

## Структура данных

### Пример отправляемых данных (`POST /submitData/`):

```json
{
  "user": {
    "email": "test@example.com",
    "name": "Иван",
    "family_name": "Иванов",
    "patronymic": "Иванович",
    "phone": "89991112233"
  },
  "coords": {
    "latitude": 45.12345,
    "longitude": 7.12345,
    "height": 1500
  },
  "beauty_title": "перевал",
  "title": "Перевал Весёлый",
  "other_titles": "Весёлый",
  "connect": "соединение долин А и Б",
  "add_time": "2024-04-27 12:00:00",
  "level": {
    "winter": "1A",
    "summer": "1B",
    "autumn": "1A",
    "spring": "1A"
  },
  "images": [
    {
      "img_url": "http://example.com/image1.jpg"
    },
    {
      "img_url": "http://example.com/image2.jpg"
    }
  ]
}
```

---

## Документация API (Swagger)

После запуска проекта Swagger UI доступен по адресу:

```
http://127.0.0.1:8000/docs
```

Альтернатива — ReDoc:
```
http://127.0.0.1:8000/redoc
```

## Примеры работы с API

### POST /submitData/

Добавление нового перевала. Пример тела запроса:

```json
{
  "user": {
    "email": "test@example.com",
    "family_name": "Иванов",
    "name": "Иван",
    "patronymic": "Иванович",
    "phone": "89999999999"
  },
  "beauty_title": "пер.",
  "title": "Пример перевала",
  "other_titles": "",
  "connect": "",
  "add_time": "2023-04-01 12:00:00",
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
```

---

## Тестирование

Для запуска тестов выполните:

```bash
pytest tests/
```

Перед этим убедитесь, что:

- PostgreSQL запущен
- Указаны корректные данные подключения в `.env`
- Таблицы базы данных созданы (см. `fstr_db.sql`)

## Авторы

- Проект выполнен в рамках курса SkillFactory Python-разработчик.
- Автор кода: Глеб Чернов
