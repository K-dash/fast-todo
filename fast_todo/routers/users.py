from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_todo.models import User
from fast_todo.schemas import Message, UserList, UserPublic, UserSchema
from fast_todo.security import (
    get_current_user,
    get_password_hash,
    get_session,
)

router = APIRouter(prefix="/users", tags=["users"])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
# Dependsにget_sessionを渡す（依存性の注入）
def create_user(user: UserSchema, session: Session):  # type: ignore
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Username already exists",
        )
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", response_model=UserList)
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    return db_user


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session, current_user: CurrentUser
):
    # 認可
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Not enough permissions"
        )
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete("/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Not enough permissions"
        )
    session.delete(current_user)
    session.commit()
    return {"message": "User deleted"}
