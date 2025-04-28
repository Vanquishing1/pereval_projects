from fastapi import FastAPI
from app.models import PerevalData
from app.db_manager import DBManager

app = FastAPI()

@app.post("/submitData/")
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
