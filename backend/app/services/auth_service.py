from sqlalchemy.orm import Session

from ..models import User
from ..utils.security import hash_password, verify_password, create_access_token


def register_user(db: Session, username: str, password: str, full_name: str) -> User:
    """注册新用户，用户名重复时抛出 ValueError"""
    if db.query(User).filter(User.username == username).first():
        raise ValueError("用户名已存在")

    user = User(
        username=username,
        password_hash=hash_password(password),
        full_name=full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> User:
    """验证用户名密码，失败时抛出 ValueError"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("用户名或密码错误")
    return user


def build_token_response(user: User) -> dict:
    token = create_access_token({"sub": str(user.id), "username": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }
