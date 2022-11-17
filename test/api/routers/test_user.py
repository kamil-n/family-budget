from json import loads
from typing import Generator

import fastapi
import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.db import get_db
from api.main import app
from api.models.user import User


def override_get_db(session_local: Session) -> Generator[Session, None, None]:
    try:
        db = session_local()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def with_token() -> dict[str, str]:
    credentials = {
        "username": "test",
        "password": "test",
    }

    # first_user = User(name=credentials["username"], hashed_password=credentials["password"])
    # db = next(get_db())
    # db.add(first_user)
    # db.commit()
    # db.refresh(first_user)

    response = client.post("/token", data=credentials)
    token_data = loads(response.text)
    return {"Authorization": f"Bearer {token_data['access_token']}"}


TEST_USER = {
    "name": "test_name",
    "hashed_password": "hashed_test_password",
}


@pytest.fixture
def clear_test_user(session_local: Session) -> None:
    db = session_local()
    user = db.query(User).filter(User.name == TEST_USER["name"]).first()
    print(user)


def test_create_user(with_token: dict[str, str], clear_test_user: None) -> None:
    try:
        response = client.post("/users/", json=TEST_USER, headers=with_token)
    except HTTPException:
        pytest.fail("create_user raised an exception.")
        response = fastapi.Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    print(response.text)

    assert response.status_code == status.HTTP_201_CREATED
    output_user = loads(response.text)
    for k, v in TEST_USER.items():
        assert v == str(output_user[k])
