from json import loads

import fastapi
import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_create_user() -> None:
    input_user = {
        "name": "test_name",
        "hashed_password": "hashed_test_password",
    }

    try:
        response = client.post("/users", json=input_user)
    except HTTPException:
        pytest.fail("create_user raised an exception.")
        response = fastapi.Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    assert response.status_code == status.HTTP_201_CREATED
    output_user = loads(response.text)
    for k, v in input_user.items():
        assert v == str(output_user[k])
