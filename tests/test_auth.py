from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    """アクセストークンが正しく取得できることを確認"""
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.unhashed_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_token_expired_after_time(client, user):
    """期限切れのトークンは認証できないことを確認"""
    with freeze_time("2024-05-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.email, "password": user.unhashed_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2024-05-14 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "hoge",
                "email": "hogeU@example.com",
                "password": "new secret",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_token_inexistent_user(client):
    """存在しないユーザーの場合は認証できないことを確認"""
    response = client.post(
        "/auth/token",
        data={"username": "no_user@na.com", "password": "asdf"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_invalid_password(client, user):
    """パスワードが正しくない場合は認証できないことを確認"""
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "invalid-passsword"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_reflesh_token(client, user, token):
    """期限が切れていないトークンはリフレッシュできることを確認"""
    response = client.post(
        "/auth/refresh_token",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_token_expired_dont_reflesh(client, user):
    """期限切れのトークンはリフレッシュできないことを確認"""
    with freeze_time("2024-05-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.email, "password": user.unhashed_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2024-05-14 12:31:00"):
        response = client.post(
            "/auth/refresh_token",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
