from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import SETTINGS

__SQLITE_URL = f"sqlite:///{SETTINGS.sqlite_database_path}"
__CONNECT_ARGS = {"check_same_thread": False}
__ENGINE = create_engine(__SQLITE_URL, connect_args=__CONNECT_ARGS)


def get_session():
    with Session(__ENGINE) as session:
        yield session
