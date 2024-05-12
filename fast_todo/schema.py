from pydantic import BaseModel, EmailStr


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


class UserDB(UserSchema):
    id: int


# users response_model
class UserList(BaseModel):
    users: list[UserPublic]
