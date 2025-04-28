import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()
class DBManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv('FSTR_DB_NAME', 'fstr_db'),
            user=os.getenv('FSTR_DB_LOGIN'),
            password=os.getenv('FSTR_DB_PASS'),
            host=os.getenv('FSTR_DB_HOST'),
            port=os.getenv('FSTR_DB_PORT')
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def add_user(self, email, name, family_name, patronymic, phone):
        self.cursor.execute(
            "INSERT INTO users (email, name, family_name, patronymic, phone) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (email, name, family_name, patronymic, phone)
        )
        user_id = self.cursor.fetchone()['id']
        self.connection.commit()
        return user_id

    def add_coords(self, latitude, longitude, height):
        self.cursor.execute(
            "INSERT INTO coords (latitude, longitude, height) VALUES (%s, %s, %s) RETURNING id;",
            (latitude, longitude, height)
        )
        coord_id = self.cursor.fetchone()['id']
        self.connection.commit()
        return coord_id

    def add_pereval(self, user_id, coord_id, beauty_title, title, other_titles, connect, add_time, winter, summer, autumn, spring):
        self.cursor.execute(
            """
            INSERT INTO pereval_added 
            (user_id, coord_id, beauty_title, title, other_titles, connect, add_time, winter, summer, autumn, spring, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'new') RETURNING id;
            """,
            (user_id, coord_id, beauty_title, title, other_titles, connect, add_time, winter, summer, autumn, spring)
        )
        pereval_id = self.cursor.fetchone()['id']
        self.connection.commit()
        return pereval_id

    def add_image(self, pereval_id, img_url):
        self.cursor.execute(
            "INSERT INTO pereval_images (pereval_id, img_url) VALUES (%s, %s);",
            (pereval_id, img_url)
        )
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
