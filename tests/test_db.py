from sqlalchemy import select

from fast_todo.models import User


def test_create_user(session):
    new_user = User(
        username="johndoe", email="QpC7U@example.com", password="secret"
    )
    session.add(new_user)
    session.commit()

    user = session.execute(select(User)).scalars().first()

    assert user.username == "johndoe"
