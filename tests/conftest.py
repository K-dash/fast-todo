# pytestによって自動的に読み込まれるので、testファイル内でimport不要
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_todo.app import app
from fast_todo.models import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    # メモリを保存先にすることで、
    # データベースを使用した場合よりも高速にテストが可能となる
    engine = create_engine("sqlite:///:memory:")
    # sessionを作成する前にテスト用データベースにすべてのテーブルを作成する
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # 各テストケースの終了時に都度データベースを破棄する
    table_registry.metadata.drop_all(engine)
