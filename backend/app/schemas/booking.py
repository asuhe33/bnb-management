from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class BookingCreate(BaseModel):
    room_id: int
    guest_name: str = Field(..., min_length=1, max_length=100)
    guest_phone: str = ""
    check_in: date
    check_out: date
    remark: str = ""

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("退房日期必须晚于入住日期")
        return self


class BookingUpdate(BaseModel):
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    status: Optional[str] = Field(
        None, pattern="^(pending|confirmed|checked_in|checked_out|cancelled)$"
    )
    remark: Optional[str] = None


class BookingResp(BaseModel):
    id: int
    room_id: int
    user_id: int
    guest_name: str
    guest_phone: str
    check_in: date
    check_out: date
    nights: int
    total_price: Decimal
    status: str
    remark: str
    created_at: datetime
    # 关联信息
    room_name: Optional[str] = None

    class Config:
        from_attributes = True


BOOKING_STATUS_LABELS = {
    "pending": "待确认",
    "confirmed": "已确认",
    "checked_in": "已入住",
    "checked_out": "已退房",
    "cancelled": "已取消",
}
