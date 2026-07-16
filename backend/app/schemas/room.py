from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern="^(single|suite|whole)$")
    price: Decimal = Field(..., gt=0)
    capacity: int = Field(default=2, ge=1, le=20)
    amenities: list[str] = Field(default_factory=list)
    description: str = ""
    image_url: str = ""
    status: str = Field(default="available", pattern="^(available|maintenance)$")


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = Field(None, pattern="^(single|suite|whole)$")
    price: Optional[Decimal] = Field(None, gt=0)
    capacity: Optional[int] = Field(None, ge=1, le=20)
    amenities: Optional[list[str]] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(available|maintenance)$")


class RoomResp(BaseModel):
    id: int
    name: str
    type: str
    price: Decimal
    capacity: int
    amenities: list[str] = []
    description: str
    image_url: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


ROOM_TYPE_LABELS = {"single": "单间", "suite": "套房", "whole": "整栋"}
