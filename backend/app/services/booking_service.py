from datetime import date

from sqlalchemy.orm import Session

from ..models import Booking, Room


def has_conflict(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
    exclude_booking_id: int | None = None,
) -> bool:
    """检测指定房源在日期区间内是否有已确认的预订冲突

    经典区间重叠判断: A.start < B.end AND A.end > B.start
    """
    query = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status.notin_(["cancelled"]),
        Booking.check_in < check_out,
        Booking.check_out > check_in,
    )
    if exclude_booking_id is not None:
        query = query.filter(Booking.id != exclude_booking_id)
    return query.count() > 0


def calculate_price(room: Room, check_in: date, check_out: date) -> tuple[int, float]:
    """计算入住晚数和总价"""
    nights = (check_out - check_in).days
    total = float(room.price) * nights
    return nights, total
