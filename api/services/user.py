from sqlalchemy.orm import Session

from api.models.user import User
from api.models.budget import Budget
from api.schemas.user import UserIn
from api.schemas.budget import BudgetIn


def add_user(db: Session, user: UserIn):
    db_user = User(name=user.name, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_budget(db: Session, budget: BudgetIn, user_id: int):
    db_budget = Budget(**budget.dict(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
