from datetime import datetime
from http import HTTPStatus

from pydantic import SecretStr
import pytest
from fastapi.testclient import TestClient

from HW_4.demo_service.api.main import create_app
from HW_4.demo_service.api.utils import initialize
from HW_4.demo_service.core.users import UserInfo, UserRole, UserService, password_is_longer_than_8


@pytest.fixture()
def test_client():
    app = create_app()
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_service.register(
        UserInfo(
            username="admin",
            name="admin",
            birthdate=datetime(2005, 1, 1),
            role=UserRole.ADMIN,
            password=SecretStr("123456789"),
        )
    )
    app.state.user_service = user_service
    return TestClient(app)


def test_correct_register_user(test_client):
    response = test_client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "Joe",
            "birthdate": "2000-05-20",
            "password": "123456789",
        },
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert response_data["username"] == "test_user"
    assert response_data["name"] == "Joe"
    assert response_data["birthdate"] == "2000-05-20T00:00:00"
    assert response_data["role"] == "user"


def test_fails_400_register_user_username_taken(test_client):
    test_client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "Joe",
            "birthdate": "2000-05-20",
            "password": "123456789",
        },
    )
    response = test_client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "John",
            "birthdate": "2002-05-20",
            "password": "1234567890",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fails_400_register_user_password_validator(test_client):
    response = test_client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "Joe",
            "birthdate": "2000-05-20",
            "password": "1234567",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fails_400_get_user_both_params_provided(test_client):
    response = test_client.post(
        "/user-get",
        params={
            "id": 2,
            "username": "test_user",
        },
        auth=("admin", "123456789"),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fails_400_get_user_none_params_provided(test_client):
    response = test_client.post(
        "/user-get",
        auth=("admin", "123456789"),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_correct_user_get_by_id_admin(test_client):
    response = test_client.post(
        "/user-get",
        params={"id": 1},
        auth=("admin", "123456789"),
    )
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data["uid"] == 1
    assert response_data["username"] == "admin"
    assert response_data["name"] == "admin"
    assert response_data["birthdate"] == "2005-01-01T00:00:00"
    assert response_data["role"] == "admin"


def test_fail_401_user_get_by_id_wrong_credentials(test_client):
    response = test_client.post(
        "/user-get",
        params={"id": 1},
        auth=("admin", "123456789000"),
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_correct_user_get_by_username_admin(test_client):
    response = test_client.post(
        "/user-get",
        params={"username": "admin"},
        auth=("admin", "123456789"),
    )
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data["uid"] == 1
    assert response_data["username"] == "admin"
    assert response_data["name"] == "admin"
    assert response_data["birthdate"] == "2005-01-01T00:00:00"
    assert response_data["role"] == "admin"


def test_fails_404_user_get_by_username(test_client):
    response = test_client.post(
        "/user-get",
        params={"username": "admin_1"},
        auth=("admin", "123456789"),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_promote_user_correct_id(test_client):
    response = test_client.post(
        "/user-promote",
        params={"id": 1},
        auth=("admin", "123456789"),
    )
    assert response.status_code == HTTPStatus.OK


def test_fail_400_promote_user_incorrect_id(test_client):
    response = test_client.post(
        "/user-promote",
        params={"id": 10},
        auth=("admin", "123456789"),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_403_promote_user_without_admin(test_client):
    test_client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "Joe",
            "birthdate": "2000-05-20",
            "password": "123456789",
        },
    )

    response = test_client.post(
        "/user-promote",
        params={"id": 1},
        auth=("test_user", "123456789"),
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_initialize():
    app = create_app()
    async with initialize(app):
        user_service = app.state.user_service
        admin = user_service.get_by_username("admin")

        assert admin.uid == 1

        admin_info = admin.info
        assert admin_info.username == "admin"
        assert admin_info.name == "admin"
        assert admin_info.birthdate == datetime.fromtimestamp(0.0)
        assert admin_info.role == UserRole.ADMIN
        assert admin_info.password == SecretStr("superSecretAdminPassword123")
