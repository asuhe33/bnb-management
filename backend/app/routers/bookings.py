from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.booking import BookingCreate, BookingUpdate, BookingResp
from ..models import Booking, Room
from ..services.booking_service import has_conflict, calculate_price
from .auth import get_current_user
from ..models import User

router = APIRouter(prefix="/api/bookings", tags=["预订"])


def _attach_room_name(items: list[Booking], db: Session) -> list[BookingResp]:
    """批量附带房源名称"""
    room_ids = {b.room_id for b in items}
    room_map = {}
    if room_ids:
        rooms = db.query(Room.id, Room.name).filter(Room.id.in_(room_ids)).all()
        room_map = {r.id: r.name for r in rooms}

    result = []
    for b in items:
        data = BookingResp.model_validate(b).model_dump()
        data["room_name"] = room_map.get(b.room_id, "")
        result.append(BookingResp(**data))
    return result


@router.get("", response_model=list[BookingResp], summary="预订列表")
def list_bookings(
    status_filter: str = Query(default="", alias="status", description="状态筛选"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Booking)
    if status_filter:
        query = query.filter(Booking.status == status_filter)
    offset = (page - 1) * page_size
    items = query.order_by(Booking.id.desc()).offset(offset).limit(page_size).all()
    return _attach_room_name(items, db)


@router.post("", response_model=BookingResp, status_code=status.HTTP_201_CREATED, summary="创建预订")
def create_booking(
    req: BookingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == req.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="房源不存在")

    if has_conflict(db, req.room_id, req.check_in, req.check_out):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="该日期区间内房源已被预订",
        )

    nights, total = calculate_price(room, req.check_in, req.check_out)
    booking = Booking(
        room_id=req.room_id,
        user_id=user.id,
        guest_name=req.guest_name,
        guest_phone=req.guest_phone,
        check_in=req.check_in,
        check_out=req.check_out,
        nights=nights,
        total_price=total,
        remark=req.remark,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return _attach_room_name([booking], db)[0]


@router.put("/{booking_id}", response_model=BookingResp, summary="更新预订")
def update_booking(
    booking_id: int,
    req: BookingUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="预订不存在")

    update_data = req.model_dump(exclude_unset=True)

    # 如果修改日期，重新校验冲突
    new_check_in = update_data.get("check_in", booking.check_in)
    new_check_out = update_data.get("check_out", booking.check_out)
    if "check_in" in update_data or "check_out" in update_data:
        if has_conflict(db, booking.room_id, new_check_in, new_check_out, exclude_booking_id=booking.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="该日期区间内房源已被预订",
            )

    for field, value in update_data.items():
        setattr(booking, field, value)

    # 日期变更时重新计算价格和晚数
    if "check_in" in update_data or "check_out" in update_data:
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        nights, total = calculate_price(room, booking.check_in, booking.check_out)
        booking.nights = nights
        booking.total_price = total

    db.commit()
    db.refresh(booking)
    return _attach_room_name([booking], db)[0]


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除预订")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="预订不存在")
    db.delete(booking)
    db.commit()
