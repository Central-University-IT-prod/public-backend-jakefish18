"""Travel note SQLAlchemy model."""

import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class TravelNote(Base):
    __tablename__ = "travel_notes"

    id = Column(Integer, primary_key=True, index=True)
    travel_id = Column(
        Integer, ForeignKey("travels.id", ondelete="cascade"), index=True
    )
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), index=True)
    note = Column(String)
    attached_file = Column(String)
    is_public = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.now)

    travel = relationship("Travel", back_populates="notes", uselist=False)
    owner = relationship("User", back_populates="notes", uselist=False)
