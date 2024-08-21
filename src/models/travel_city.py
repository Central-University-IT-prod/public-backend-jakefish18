"""Travel city SQLAlchemy model."""

import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class TravelCity(Base):
    __tablename__ = "travel_cities"

    id = Column(Integer, primary_key=True, index=True)
    travel_id = Column(
        Integer, ForeignKey("travels.id", ondelete="cascade"), index=True
    )
    address = Column(String)
    city = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.now)

    travel = relationship("Travel", back_populates="cities", uselist=False)
