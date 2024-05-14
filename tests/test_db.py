from sqlalchemy import select

from fast_todo.models import Todo, User


def test_create_user(session):
    new_user = User(
        username="johndoe", email="QpC7U@example.com", password="secret"
    )
    session.add(new_user)
    session.commit()

    user = session.execute(select(User)).scalars().first()

    assert user.username == "johndoe"


def test_create_todo(session, user: User):
    todo = Todo(
        title="Todo 1",
        description="Todo 1 description",
        state="draft",
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))
    assert todo in user.todos
