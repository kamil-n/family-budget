import time

from api.db import get_db
from api.schemas.budget import BudgetIn
from api.services.user import create_user_budget, get_user_by_name

db = next(get_db())


def add_budget(username: str) -> None:
    owner = get_user_by_name(db, username)
    if not owner:
        raise Exception(f"Couldn't find owner {username}")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    budget = BudgetIn(timestamp=now, blob="test")
    create_user_budget(db, budget, owner.id)
