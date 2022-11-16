from json import loads

import fastapi
import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


@pytest.fixture
def with_token() -> dict[str, str]:
    # first should ensure this user exists
    credentials = {
        "username": "test",
        "password": "test",
    }
    response = client.post("/token", data=credentials)
    token_data = loads(response.text)
    return {"Authorization": f"Bearer {token_data['access_token']}"}


def test_create_user(with_token: dict[str, str]) -> None:
    input_user = {
        "name": "test_name",
        "hashed_password": "hashed_test_password",
    }
    try:
        response = client.post("/users", json=input_user, headers=with_token)
    except HTTPException:
        pytest.fail("create_user raised an exception.")
        response = fastapi.Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # !test fails with code 405 - method not allowed
    assert response.request.method == "POST"  # ok

    assert response.status_code == status.HTTP_201_CREATED
    output_user = loads(response.text)
    for k, v in input_user.items():
        assert v == str(output_user[k])
