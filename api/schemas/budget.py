from datetime import datetime

from pydantic import BaseModel


class BudgetBase(BaseModel):
    timestamp: datetime
    blob: str


class BudgetIn(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
