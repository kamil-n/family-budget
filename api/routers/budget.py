from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.authenticate import oauth2_scheme
from api.db import get_db
from api.models.budget import Budget as BudgetModel
from api.schemas.budget import Budget as BudgetSchema
from api.services.budget import get_budgets

router = APIRouter(prefix="/budgets")


@router.get("", response_model=List[BudgetSchema])
def read_budgets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> list[BudgetModel]:
    budgets = get_budgets(db, skip=skip, limit=limit)
    return budgets
