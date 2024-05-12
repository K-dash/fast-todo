# pytestによって自動的に読み込まれるので、testファイル内でimport不要
import pytest
from fastapi.testclient import TestClient

from fast_todo.app import app


@pytest.fixture()
def client():
    return TestClient(app)
