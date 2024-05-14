# pytestによって自動的に読み込まれるので、testファイル内でimport不要
import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_todo.app import app
from fast_todo.database import get_session
from fast_todo.models import User, table_registry
from fast_todo.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.LazyAttribute(lambda o: f"{o.username}secret")


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
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    # モンキーパッチで平文のパスワードを返す
    user.unhashed_password = password
    return user


@pytest.fixture()
def other_user(session):
    password = "secret2"
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    # モンキーパッチで平文のパスワードを返す
    user.unhashed_password = password
    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.unhashed_password},
    )
    return response.json().get("access_token")
