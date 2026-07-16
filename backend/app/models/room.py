from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, Enum
from sqlalchemy.dialects.mysql import JSON

from ..database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(
        Enum("single", "suite", "whole", name="room_type"),
        nullable=False,
        comment="单间/套房/整栋",
    )
    price = Column(Numeric(10, 2), nullable=False, comment="每晚价格")
    capacity = Column(Integer, default=2, comment="可住人数")
    amenities = Column(JSON, comment="设施列表")
    description = Column(Text)
    image_url = Column(String(500), default="")
    status = Column(
        Enum("available", "maintenance", name="room_status"),
        default="available",
    )
    created_at = Column(DateTime, default=datetime.utcnow)
