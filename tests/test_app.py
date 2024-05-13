from http import HTTPStatus

from fast_todo.schema import UserPublic


def test_read_root(client):
    # AAA parttern
    response = client.get("/")  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {"message": "Hello World!"}  # Assert


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "johndoe",
            "email": "QpC7U@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "johndoe",
        "email": "QpC7U@example.com",
        "id": 1,
    }


def test_create_user_existing_username(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.post(
        "/users/",
        json={
            "username": f"{user_schema.get('username')}",
            "email": "QpC7U@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    # userの値をバリデーションし、dict型にデシリアライズ
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [user_schema],
    }


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f"/users/{user_schema.get('id')}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_not_found(client):
    response = client.get("/users/5")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "hoge",
            "email": "QpC7U@example.com",
            "password": "new secret",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "hoge",
        "email": "QpC7U@example.com",
        "id": user.id,
    }


def test_update_user_parmission_denied(client):
    response = client.put(
        "/users/5",
        json={
            "username": "alice",
            "email": "QpC7U@example.com",
            "password": "new secret",
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/5")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.unhashed_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
