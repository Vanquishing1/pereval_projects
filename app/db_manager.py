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
        if self.connection:
            self.connection.close()

    def get_pereval_by_id(self, pereval_id):
        query = """
            SELECT p.id, p.beauty_title, p.title, p.other_titles, p.connect, p.add_time, 
                   p.status, u.name, u.family_name, u.patronymic, u.email, u.phone,
                   c.latitude, c.longitude, c.height
            FROM pereval_added p
            JOIN users u ON p.user_id = u.id
            JOIN coords c ON p.coord_id = c.id
            WHERE p.id = %s
        """
        self.cursor.execute(query, (pereval_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return dict(row)

    def update_pereval(self, pereval_id, data):
        try:
            update_query = """
                UPDATE pereval_added
                SET beauty_title = %s,
                    title = %s,
                    other_titles = %s,
                    connect = %s,
                    add_time = %s,
                    winter = %s,
                    summer = %s,
                    autumn = %s,
                    spring = %s
                WHERE id = %s
            """
            self.cursor.execute(update_query, (
                data.beauty_title,
                data.title,
                data.other_titles,
                data.connect,
                data.add_time,
                data.level.winter,
                data.level.summer,
                data.level.autumn,
                data.level.spring,
                pereval_id
            ))

            coord_query = """
                UPDATE coords
                SET latitude = %s,
                    longitude = %s,
                    height = %s
                WHERE id = (SELECT coord_id FROM pereval_added WHERE id = %s)
            """
            self.cursor.execute(coord_query, (
                data.coords.latitude,
                data.coords.longitude,
                data.coords.height,
                pereval_id
            ))

            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating pereval: {e}")
            return False

    def get_perevals_by_email(self, email):
        query = """
            SELECT p.id, p.title, p.status, p.add_time
            FROM pereval_added p
            JOIN users u ON p.user_id = u.id
            WHERE u.email = %s
        """
        self.cursor.execute(query, (email,))
        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]
