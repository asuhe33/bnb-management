from datetime import datetime, date

from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime, Enum, Text, ForeignKey, Index,
)

from ..database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人")
    guest_name = Column(String(100), nullable=False, comment="客人姓名")
    guest_phone = Column(String(20), default="", comment="客人电话")
    check_in = Column(Date, nullable=False, comment="入住日期")
    check_out = Column(Date, nullable=False, comment="退房日期")
    nights = Column(Integer, nullable=False, comment="入住晚数")
    total_price = Column(Numeric(10, 2), nullable=False, comment="总价")
    status = Column(
        Enum(
            "pending", "confirmed", "checked_in", "checked_out", "cancelled",
            name="booking_status",
        ),
        default="pending",
    )
    remark = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_room_dates", "room_id", "check_in", "check_out"),
    )
