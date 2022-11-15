from sqlalchemy.orm import Session

from api.models.budget import Budget


def get_budgets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Budget).offset(skip).limit(limit).all()
