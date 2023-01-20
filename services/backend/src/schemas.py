from pydantic import BaseModel


class MessageBase(BaseModel):
    text: str
    sender_id: str 


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str



class User(UserBase):
    id: int
    is_active: bool
    items: list[Message] = []

    class Config:
        orm_mode = True