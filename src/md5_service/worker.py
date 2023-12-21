import hashlib
import time

from celery import Celery
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


result_backend = f'db+postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

celery = Celery('worker', broker='redis://localhost:6379', result_backend=result_backend)


@celery.task
def get_md5_hash(file_path):
    with open(file_path, 'rb') as opened_file:
        content = opened_file.read()
        md5 = hashlib.md5()
        md5.update(content)

        return md5.hexdigest()
