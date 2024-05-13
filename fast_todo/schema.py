from pydantic import BaseModel, ConfigDict, EmailStr


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
