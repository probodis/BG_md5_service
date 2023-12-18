from dotenv import load_dotenv
import os

load_dotenv()


SRC_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.split(SRC_FOLDER_PATH)[0]
UPLOADED_FILES_PATH = os.environ.get("UPLOADED_FILES_PATH")
UPLOADED_FILES_PATH = os.path.join(ROOT_DIR, UPLOADED_FILES_PATH)

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

