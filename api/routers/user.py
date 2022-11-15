from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from api.authenticate import oauth2_scheme
from api.db import get_db
from api.schemas.user import User, UserIn
from api.schemas.budget import Budget, BudgetIn
from api.services.user import (
    add_user,
    get_user,
    get_user_by_name,
    get_users,
    create_user_budget,
)

router = APIRouter(prefix="/users")


@router.post("/", response_model=User)
def create_user(
    user: UserIn = Body(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    db_user = get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists."
        )
    return add_user(db=db, user=user)


@router.get("", response_model=List[User])
def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int = Path(..., ge=0),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return db_user


@router.post(
    "/{user_id}/budgets/", response_model=Budget, status_code=status.HTTP_201_CREATED
)
def create_budget_for_user(
    user_id: int = Path(..., ge=0),
    budget: BudgetIn = Body(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    return create_user_budget(db=db, budget=budget, user_id=user_id)
