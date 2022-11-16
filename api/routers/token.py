from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.authenticate import get_token
from api.db import get_db

router = APIRouter(prefix="/token")


@router.post("")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict[str, str]:
    return get_token(db, form_data)
