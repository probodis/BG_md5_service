import hashlib
from datetime import datetime
import redis
from redlock import Redlock
from celery import Celery
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, LOG_PATH, REDIS_HOST, REDIS_PORT, REDIS_DB_ID

result_backend = f'db+postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
celery = Celery('worker', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}', result_backend=result_backend)

dlm = Redlock([{"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB_ID}, ], retry_count=10, retry_delay=1)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_ID)


@celery.task
def get_md5_hash(file_id, file_name):

    content = redis_client.get(file_id)

    md5 = hashlib.md5()
    md5.update(content)

    write_log(f"{datetime.utcnow()};"
              f"{file_id};"
              f"{file_name};"
              f"{md5.hexdigest()}")

    redis_client.delete(file_id)

    return md5.hexdigest()


def write_log(message: str):
    lock = dlm.lock("log_file", 5)  # Mutex based on https://redis.io/docs/manual/patterns/distributed-locks/

    with open(f"{LOG_PATH}", 'a+') as file:
        file.write(message + "\n")

    if lock:
        dlm.unlock(lock)
