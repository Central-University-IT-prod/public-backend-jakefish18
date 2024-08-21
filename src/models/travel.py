"""Travel SQLAlchemy model."""

import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database import Base


class Travel(Base):
    __tablename__ = "travels"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)

    __table_args__ = (UniqueConstraint("owner_id", "name", name="uq_user_travel_name"),)

    cities = relationship("TravelCity", back_populates="travel", cascade="all,delete",)
    notes = relationship("TravelNote", back_populates="travel", cascade="all,delete",)
    owner = relationship("User", back_populates="owned_travels", uselist=False)
    users = relationship("UserTravel", back_populates="travel", cascade="all,delete",)
