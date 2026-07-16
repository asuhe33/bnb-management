from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), default="")
    role = Column(Enum("host", "admin", name="user_role"), default="host")
    created_at = Column(DateTime, default=datetime.utcnow)
