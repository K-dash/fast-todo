from http import HTTPStatus

import factory.fuzzy

from fast_todo.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test todo",
            "description": "Test todo description",
            "state": "draft",
        },
    )
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test todo"
    assert response.json()["description"] == "Test todo description"
    assert response.json()["state"] == "draft"
    assert response.json()["created_at"] is not None


def test_list_todos_should_return_5_todos(session, client, token, user):
    excepted_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(excepted_todos, user_id=user.id)
    )
    session.commit()

    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == excepted_todos


def test_list_todos_pagenation_should_return_2_todos(
    session, client, token, user
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        f"/todos/?offset=1&limit={expected_todos}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_title_should_return_5_todos(
    session, client, token, user
):
    excepted_todos = 5
    total_todos = excepted_todos + 1

    session.bulk_save_objects(
        TodoFactory.create_batch(
            excepted_todos, user_id=user.id, title="Test 5"
        )
    )
    session.add(TodoFactory.build(user_id=user.id, title="Test 6"))
    session.commit()

    # ユーザーに紐づくTODOの数を確認
    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == total_todos

    # filterの確認
    response = client.get(
        "/todos/?title=Test 5",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == excepted_todos


def test_list_todos_filter_description_should_return_5_todos(
    session, client, token, user
):
    excepted_todos = 5
    total_todos = excepted_todos + 1

    session.bulk_save_objects(
        TodoFactory.create_batch(
            excepted_todos, user_id=user.id, description="Test 5"
        )
    )
    session.add(TodoFactory.build(user_id=user.id, description="Test 6"))
    session.commit()

    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == total_todos

    response = client.get(
        "/todos/?description=Test 5",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == excepted_todos


def test_list_todos_filter_state_should_return_5_todos(
    session, client, token, user
):
    excepted_todos = 5
    total_todos = excepted_todos + 1

    session.bulk_save_objects(
        TodoFactory.create_batch(
            excepted_todos, user_id=user.id, state=TodoState.draft
        )
    )
    session.add(TodoFactory.build(user_id=user.id, state=TodoState.done))
    session.commit()

    request = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(request.json()["todos"]) == total_todos

    request = client.get(
        "/todos/?state=draft",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(request.json()["todos"]) == excepted_todos


def test_list_todos_filter_combined_should_return_5_todos(
    session, client, token, user
):
    excepted_todos = 5

    session.bulk_save_objects(
        TodoFactory.create_batch(
            excepted_todos,
            title="Test 5",
            description="desc 5",
            user_id=user.id,
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title="Other title",
            description="other description",
            state=TodoState.todo,
        )
    )
    session.commit()

    respose = client.get(
        "/todos/?title=Test 5&description=desc 5&state=done",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(respose.json()["todos"]) == excepted_todos


def test_patch_todo(client, token, session, user):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        json={"title": "new title"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "new title"


def test_patch_todo_error(client, token):
    response = client.patch(
        "/todos/10",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(client, token, session, user):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f"/todos/{todo.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Todo deleted successfully"}


def test_delete_todo_error(client, token):
    response = client.delete(
        "/todos/10",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
