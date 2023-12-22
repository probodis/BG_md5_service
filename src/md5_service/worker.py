import hashlib

from redlock import Redlock
from celery import Celery
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, LOG_PATH, REDIS_HOST, REDIS_PORT

result_backend = f'db+postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
celery = Celery('worker', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}', result_backend=result_backend)

dlm = Redlock([{"host": REDIS_HOST, "port": REDIS_PORT, "db": 0}, ], retry_count=10, retry_delay=1)


@celery.task
def get_md5_hash(file_path):
    with open(file_path, 'rb') as opened_file:
        content = opened_file.read()
        md5 = hashlib.md5()
        md5.update(content)

        write_log(md5.hexdigest())

        return md5.hexdigest()


def write_log(message: str):
    lock = dlm.lock("log_file", 5)

    with open(f"{LOG_PATH}", 'a+') as file:
        file.write(message + "\n")

    if lock:
        dlm.unlock(lock)
