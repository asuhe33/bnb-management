from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Booking, Room


def get_dashboard_stats(db: Session) -> dict:
    """聚合看板统计数据"""
    today = date.today()
    month_start = today.replace(day=1)

    # 总收益（已退房 + 已确认 + 已入住）
    confirmed_statuses = ["confirmed", "checked_in", "checked_out"]
    total_revenue = (
        db.query(func.coalesce(func.sum(Booking.total_price), 0))
        .filter(Booking.status.in_(confirmed_statuses))
        .scalar()
    )

    # 本月收益
    monthly_revenue = (
        db.query(func.coalesce(func.sum(Booking.total_price), 0))
        .filter(
            Booking.status.in_(confirmed_statuses),
            Booking.check_in >= month_start,
        )
        .scalar()
    )

    # 总预订数
    total_bookings = db.query(Booking).count()

    # 各房型预订占比
    rows = (
        db.query(Room.type, func.count(Booking.id))
        .join(Booking, Booking.room_id == Room.id)
        .group_by(Room.type)
        .all()
    )
    room_type_distribution = {room_type: count for room_type, count in rows}

    # 近 7 日收益趋势
    week_start = today - timedelta(days=6)
    trend_rows = (
        db.query(Booking.check_in, func.coalesce(func.sum(Booking.total_price), 0))
        .filter(
            Booking.status.in_(confirmed_statuses),
            Booking.check_in >= week_start,
            Booking.check_in <= today,
        )
        .group_by(Booking.check_in)
        .order_by(Booking.check_in)
        .all()
    )
    trend_map = {str(d): float(v) for d, v in trend_rows}
    revenue_trend = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        revenue_trend.append(
            {"date": str(d), "revenue": trend_map.get(str(d), 0)}
        )

    # 入住率（近 30 天）
    window_start = today - timedelta(days=29)
    total_rooms = db.query(Room).count()
    occupied_days = (
        db.query(func.count(func.distinct(Booking.check_in)))
        .filter(
            Booking.status.in_(confirmed_statuses),
            Booking.check_in >= window_start,
            Booking.check_in <= today,
        )
        .scalar()
        or 0
    )
    available_days = total_rooms * 30
    occupancy_rate = round(occupied_days / available_days, 2) if available_days > 0 else 0

    return {
        "total_revenue": float(total_revenue),
        "monthly_revenue": float(monthly_revenue),
        "total_bookings": total_bookings,
        "room_type_distribution": room_type_distribution,
        "revenue_trend": revenue_trend,
        "occupancy_rate": occupancy_rate,
    }
