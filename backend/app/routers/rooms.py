from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.room import RoomCreate, RoomUpdate, RoomResp
from ..models import Room
from .auth import get_current_user
from ..models import User

router = APIRouter(prefix="/api/rooms", tags=["房源"])


@router.get("", response_model=list[RoomResp], summary="房源列表")
def list_rooms(
    keyword: str = Query(default="", description="搜索关键词"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Room)
    if keyword:
        query = query.filter(Room.name.contains(keyword))
    offset = (page - 1) * page_size
    return query.order_by(Room.id.desc()).offset(offset).limit(page_size).all()


@router.post("", response_model=RoomResp, status_code=status.HTTP_201_CREATED, summary="新建房源")
def create_room(
    req: RoomCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    room = Room(**req.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.get("/{room_id}", response_model=RoomResp, summary="房源详情")
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="房源不存在")
    return room


@router.put("/{room_id}", response_model=RoomResp, summary="更新房源")
def update_room(
    room_id: int,
    req: RoomUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="房源不存在")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(room, field, value)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除房源")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="房源不存在")
    db.delete(room)
    db.commit()
