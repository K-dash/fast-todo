from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_todo.models import TodoState


class Message(BaseModel):
    message: str


# request_model
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


# response_model
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # UserPublicのインスタンスを辞書で出力できるようにConfigDictを定義
    # from_attributes=True: スキーマに含まれていない属性があっても検証OKにする
    model_config = ConfigDict(from_attributes=True)


# users response_model
class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# ------- ToDos -------
class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


# response model
class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState
    created_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: str | None = None
