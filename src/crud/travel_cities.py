"""
CRUD requests for travel cities.
"""

from typing import Union

from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import Travel, TravelCity, User


class CrudTravelCity(CrudBase[TravelCity]):
    def __init__(self, Model: type[TravelCity]):
        super().__init__(Model)

    def get_sorted_by_date(self, db: Session, travel: Travel) -> list[TravelCity]:
        """Getting travel cities sorted by start date."""
        return (
            db.query(TravelCity)
            .filter(TravelCity.travel_id == travel.id)
            .order_by(TravelCity.start_date)
            .all()
        )
