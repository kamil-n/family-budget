# https://fastapi.tiangolo.com/advanced/testing-database/
from typing import Generator, TypeVar

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from typing_extensions import ParamSpec

from api.config import DBSettings
from api.db import Base

T = TypeVar("T")
P = ParamSpec("P")


@pytest.fixture(scope="module")
def session_local() -> Generator[Session, None, None]:
    settings = DBSettings()
    test_db_url = (
        f"postgresql://{settings.db_user}:{settings.db_pass}@"
        f"{settings.db_host}:{settings.db_port}/{settings.db_database}"
    )
    engine = create_engine(test_db_url)

    assert not database_exists(
        test_db_url
    ), "Test database already exists. Aborting tests."
    create_database(test_db_url)

    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)

    yield session_local
    drop_database(test_db_url)


# in the future might need something like
# https://gist.github.com/kissgyorgy/e2365f25a213de44b9a2
