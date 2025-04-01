from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import SETTINGS

__SQLITE_URL = f"sqlite:///{SETTINGS.sqlite_database_path}"
__CONNECT_ARGS = {"check_same_thread": False}
__ENGINE = create_engine(__SQLITE_URL, connect_args=__CONNECT_ARGS)
__SESSIONMAKER = sessionmaker(bind=__ENGINE)


def get_write_session():
    with __SESSIONMAKER.begin() as session:
        yield session


def get_read_session():
    with __SESSIONMAKER() as session:
        yield session
