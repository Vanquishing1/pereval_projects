from fastapi import FastAPI, HTTPException, Query
from app.models import PerevalData
from app.db_manager import DBManager
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Pereval API",
    description="API для подачи и управления данными о перевалах",
    version="1.0.0"
)

class SubmitResponse(BaseModel):
    status: int
    message: str
    id: Optional[int] = None

@app.post("/submitData/", response_model=SubmitResponse, summary="Отправить данные о перевале")
def submit_data(data: PerevalData):
    db = DBManager()
    try:
        user_id = db.add_user(
            email=data.user.email,
            name=data.user.name,
            family_name=data.user.family_name,
            patronymic=data.user.patronymic,
            phone=data.user.phone
        )
        coord_id = db.add_coords(
            latitude=data.coords.latitude,
            longitude=data.coords.longitude,
            height=data.coords.height
        )
        pereval_id = db.add_pereval(
            user_id, coord_id,
            data.beauty_title, data.title, data.other_titles,
            data.connect, data.add_time,
            data.level.winter, data.level.summer,
            data.level.autumn, data.level.spring
        )
        for img in data.images:
            db.add_image(pereval_id, img.img_url)
        return {"status": 200, "message": "success", "id": pereval_id}
    except Exception as e:
        return {"status": 500, "message": str(e)}
    finally:
        db.close()

@app.get("/submitData/{pereval_id}")
def get_pereval(pereval_id: int):
    db = DBManager()
    try:
        pereval = db.get_pereval_by_id(pereval_id)
        if not pereval:
            raise HTTPException(status_code=404, detail="Pereval not found")
        return pereval
    finally:
        db.close()


@app.patch("/submitData/{pereval_id}")
def update_pereval(pereval_id: int, data: PerevalData):
    db = DBManager()
    try:
        pereval = db.get_pereval_by_id(pereval_id)
        if not pereval:
            return {"state": 0, "message": "Pereval not found"}

        if pereval['status'] != 'new':
            return {"state": 0, "message": "Only records with status 'new' can be updated"}

        update_result = db.update_pereval(pereval_id, data)
        if update_result:
            return {"state": 1, "message": "Pereval updated successfully"}
        else:
            return {"state": 0, "message": "Failed to update pereval"}

    except Exception as e:
        return {"state": 0, "message": str(e)}
    finally:
        db.close()


@app.get("/submitData/")
def get_perevals_by_user_email(user__email: str = Query(...)):
    db = DBManager()
    try:
        perevals = db.get_perevals_by_email(user__email)
        return perevals
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Pereval Project API</title>
        </head>
        <body>
            <h1>Добро пожаловать в Pereval Project API!</h1>
            <p>Перейдите в <a href="/docs">Swagger-документацию</a> для работы с API.</p>
        </body>
    </html>
    """