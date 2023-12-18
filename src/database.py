from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.models import UserFileOrm

URL_DB = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(
    url=URL_DB,
    echo=True
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_table():
    UserFileOrm.metadata.create_all(bind=engine)


def insert_data(file_name: str, file_id: str):
    user_file = UserFileOrm(file_name=file_name, file_id=file_id)
    with session_factory() as session:
        session.add(user_file)
        session.commit()


if __name__ == '__main__':
    create_table()
    insert_data("test_name", "test_id")
