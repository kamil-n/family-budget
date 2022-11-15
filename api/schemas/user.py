from typing import List

from pydantic import BaseModel

from api.schemas.budget import Budget


class UserBase(BaseModel):
    name: str


class UserIn(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    budgets: List[Budget] = []

    class Config:
        orm_mode = True
