from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import UserCreate, LoginRequest, TokenResp, UserResp
from ..services import auth_service
from ..utils.security import decode_token
from ..models import User

router = APIRouter(prefix="/api/auth", tags=["认证"])


def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI 依赖：从 Authorization header 解析 JWT 获取当前用户"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证信息",
        )
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已过期",
        )
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )
    return user


@router.post("/register", response_model=TokenResp, summary="用户注册")
def register(req: UserCreate, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(
            db, req.username, req.password, req.full_name
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return auth_service.build_token_response(user)


@router.post("/login", response_model=TokenResp, summary="用户登录")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.authenticate(db, req.username, req.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )
    return auth_service.build_token_response(user)


@router.get("/me", response_model=UserResp, summary="获取当前用户")
def me(user: User = Depends(get_current_user)):
    return user
