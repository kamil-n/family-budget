# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.config import AuthSettings
from api.models.user import User
from api.schemas.token import TokenData
from api.schemas.user import UserIn

settings = AuthSettings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> UserIn:
    user = db.query(User).filter(User.name == username).first()
    if user:
        return UserIn(**{"name": user.name, "hashed_password": user.hashed_password})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User '{username}' doesn't exists.",
    )


def authenticate_user(db: Session, username: str, password: str) -> Union[bool, UserIn]:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.auth_secret, algorithm=settings.auth_algo
    )
    return encoded_jwt


def get_token(db: Session, form_data: OAuth2PasswordRequestForm) -> dict[str, str]:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    assert isinstance(user, UserIn)
    access_token_expires = timedelta(days=settings.auth_token_expire_days)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(db: Session, token: str = Depends(oauth2_scheme)) -> UserIn:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.auth_secret, algorithms=[settings.auth_algo]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)  # type: ignore [arg-type]
    if user is None:
        raise credentials_exception
    return user
