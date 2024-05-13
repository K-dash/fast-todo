from jwt import decode

from fast_todo.security import create_access_token
from fast_todo.settings import Settings

settings = Settings()


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)
    decoded = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert decoded["test"] == data["test"]
    assert decoded["exp"]
