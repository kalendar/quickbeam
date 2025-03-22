from leaflock.sqlalchemy_tables.activity import Activity
from leaflock.sqlalchemy_tables.base import Base
from leaflock.sqlalchemy_tables.module import Module
from leaflock.sqlalchemy_tables.textbook import Textbook
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import SETTINGS

__FORCE_USE = [Textbook, Activity, Module]  # type: ignore

__SQLITE_URL = f"sqlite:///{SETTINGS.sqlite_database_path}"
__CONNECT_ARGS = {"check_same_thread": False}
__ENGINE = create_engine(__SQLITE_URL, connect_args=__CONNECT_ARGS)


def create_db_and_tables():
    Base.metadata.create_all(__ENGINE)


def get_session():
    with Session(__ENGINE) as session:
        yield session
