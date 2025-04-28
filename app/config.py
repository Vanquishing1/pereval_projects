from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("FSTR_DB_HOST"),
    "port": os.getenv("FSTR_DB_PORT"),
    "user": os.getenv("FSTR_DB_LOGIN"),
    "password": os.getenv("FSTR_DB_PASS"),
    "dbname": os.getenv("FSTR_DB_NAME"),
}
