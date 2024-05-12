from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_todo.app import app


def test_read_root():
    # AAA parttern
    client = TestClient(app)  # Arrange
    response = client.get("/")  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {"message": "Hello World!"}  # Assert
