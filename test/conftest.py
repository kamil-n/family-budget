from typing import Callable, Generator, TypeVar

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, drop_database
from typing_extensions import ParamSpec

from api.config import SQLALCHEMY_DATABASE_URL
from api.db import Base, get_db
from api.main import app

T = TypeVar("T")
P = ParamSpec("P")


@pytest.fixture(scope="module")
def session_local() -> Generator[Session, None, None]:
    test_db_url = SQLALCHEMY_DATABASE_URL
    engine = create_engine(test_db_url)

    assert not database_exists(
        test_db_url
    ), "Test database already exists. Aborting tests."

    Base.metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield session_local
    drop_database(test_db_url)


def temp_db(f: Callable[P, T]) -> Callable[P, T]:
    def func(  # type: ignore [return]
        session_local: Session, *args: P.args, **kwargs: P.kwargs
    ) -> T:
        def override_get_db() -> Generator[Session, None, None]:
            try:
                db = session_local()
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        f(*args, **kwargs)
        app.dependency_overrides[get_db] = get_db

    return func  # type: ignore [return-value]
