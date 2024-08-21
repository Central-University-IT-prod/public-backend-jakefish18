"""User SQLAlchemy model."""

import datetime

from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    login = Column(String, unique=True, index=True)
    address = Column(String)
    description = Column(String)
    registered_at = Column(DateTime, default=datetime.datetime.now)

    travels = relationship(
        "UserTravel",
        back_populates="user",
        cascade="all,delete",
    )
    owned_travels = relationship(
        "Travel",
        back_populates="owner",
        cascade="all,delete",
    )
    notes = relationship(
        "TravelNote",
        back_populates="owner",
        cascade="all, delete",
    )
