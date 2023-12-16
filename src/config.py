from dotenv import load_dotenv
import os

load_dotenv()


SRC_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.split(SRC_FOLDER_PATH)[0]
UPLOADED_FILES_PATH = os.environ.get("UPLOADED_FILES_PATH")
UPLOADED_FILES_PATH = os.path.join(ROOT_DIR, UPLOADED_FILES_PATH)
