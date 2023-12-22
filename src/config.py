from dotenv import load_dotenv
import os

load_dotenv()


SRC_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.split(SRC_FOLDER_PATH)[0]

LOG_PATH = os.environ.get("LOG_PATH")
LOG_PATH = os.path.join(ROOT_DIR, LOG_PATH)

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB_ID = os.environ.get("REDIS_DB_ID")

