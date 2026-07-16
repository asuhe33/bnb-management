from datetime import datetime
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str = ""


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResp(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResp
