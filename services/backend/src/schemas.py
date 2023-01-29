from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    text: str
    sender_id: str 
    sender_user: str




class MessageCreate(MessageBase):
    text: str
    sender_id: str 
    sender_user: str
    pass


class Message(MessageBase):
    id: int
    created_at: datetime




    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
   password: str
   pass



class User(UserBase):
    id: int
    username: str
    is_active: bool
    items: list[Message] = []

    class Config:
        orm_mode = True 
