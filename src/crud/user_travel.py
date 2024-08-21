"""
CRUD requests for user travels.
"""

from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from src.crud.base import CrudBase
from src.models import Travel, TravelNote, User, UserTravel


class CrudUserTravel(CrudBase[UserTravel]):
    def __init__(self, Model: type[UserTravel]):
        super().__init__(Model)

    def get_by_offset(
        self, db: Session, user: User, offset: int
    ) -> Union[UserTravel, None]:
        """
        Getting user travel by offset.
        Travels are ordered by created_at field.
        """
        return (
            db.query(UserTravel)
            .filter(UserTravel.user_id == user.id)
            .order_by(UserTravel.created_at)
            .offset(offset)
            .first()
        )

    def get_by_user_and_travel(
        self, db: Session, user: User, travel: Travel
    ) -> Union[UserTravel, None]:
        """
        Getting user travel by user and travel.
        None if there is not such user travel.
        """
        return (
            db.query(UserTravel)
            .filter(
                and_(UserTravel.user_id == user.id, UserTravel.travel_id == travel.id)
            )
            .first()
        )
