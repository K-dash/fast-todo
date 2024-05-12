from http import HTTPStatus


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


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {"id": 1, "username": "johndoe", "email": "QpC7U@example.com"}
        ]
    }


def test_read_user(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "johndoe",
        "email": "QpC7U@example.com",
    }


def test_read_user_not_found(client):
    response = client.get("/users/5")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "alice",
            "email": "QpC7U@example.com",
            "password": "new secret",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "alice",
        "email": "QpC7U@example.com",
        "id": 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        "/users/5",
        json={
            "username": "alice",
            "email": "QpC7U@example.com",
            "password": "new secret",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/5")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
