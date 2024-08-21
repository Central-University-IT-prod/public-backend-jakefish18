"""User travel SQLAlchemy model."""

import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database import Base


class UserTravel(Base):
    __tablename__ = "user_travels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"))
    travel_id = Column(Integer, ForeignKey("travels.id", ondelete="cascade"))
    created_at = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="travels", uselist=False)
    travel = relationship("Travel", back_populates="users", uselist=False)
