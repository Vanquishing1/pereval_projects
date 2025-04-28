from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    email: str
    name: str
    family_name: str
    patronymic: Optional[str] = None
    phone: Optional[str] = None

class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int

class Level(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None

class Image(BaseModel):
    img_url: str

class PerevalData(BaseModel):
    user: User
    coords: Coords
    beauty_title: str
    title: str
    other_titles: str
    connect: str
    add_time: str
    level: Level
    images: List[Image]
