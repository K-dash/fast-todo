# pytestによって自動的に読み込まれるので、testファイル内でimport不要
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_todo.app import app
from fast_todo.database import get_session
from fast_todo.models import User, table_registry
from fast_todo.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    # メモリを保存先にすることで、
    # データベースを使用した場合よりも高速にテストが可能となる
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # sessionを作成する前にテスト用データベースにすべてのテーブルを作成する
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # 各テストケースの終了時に都度データベースを破棄する
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    password = "secret"
    new_user = User(
        username="johndoe",
        email="QpC7U@example.com",
        # ハッシュ化されたパスワードをDBに保存する
        password=get_password_hash(password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # モンキーパッチで平文のパスワードを返す
    new_user.unhashed_password = password
    return new_user


@pytest.fixture()
def token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.unhashed_password},
    )
    return response.json().get("access_token")
