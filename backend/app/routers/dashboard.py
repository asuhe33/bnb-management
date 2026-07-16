from fastapi import APIRouter, Depends

from ..database import get_db
from ..services.stats_service import get_dashboard_stats
from .auth import get_current_user
from ..models import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/dashboard", tags=["数据看板"])


@router.get("/stats", summary="看板统计数据")
def dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return get_dashboard_stats(db)
