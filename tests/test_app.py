from http import HTTPStatus


def test_read_root(client):
    # AAA parttern
    response = client.get("/")  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {"message": "Hello World!"}  # Assert
