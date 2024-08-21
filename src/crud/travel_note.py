"""
CRUD requests for travel notes.
"""

from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, or_

from src.crud.base import CrudBase
from src.models import Travel, TravelNote, User


class CrudTravelNote(CrudBase[TravelNote]):
    def __init__(self, Model: type[TravelNote]):
        super().__init__(Model)

    def get_note_by_index(
        self, db: Session, user: Travel, travel: Travel, index: int
    ) -> Union[TravelNote, None]:
        """
        Getting travel note by offset.
        Notes are ordered by created_at field.
        """
        return (
            db.query(TravelNote)
            .filter(
                and_(
                    TravelNote.travel_id == travel.id,
                    or_(TravelNote.is_public, TravelNote.owner_id == user.id),
                )
            )
            .order_by(TravelNote.created_at)
            .offset(index - 1)
            .first()
        )

    def get_notes(self, db: Session, user: User, travel: Travel) -> list[TravelNote]:
        """
        Get travel not public notes or user notes.
        """
        return (
            db.query(TravelNote)
            .filter(
                and_(
                    TravelNote.travel_id == travel.id,
                    or_(TravelNote.is_public, TravelNote.owner_id == user.id),
                )
            )
            .order_by(TravelNote.created_at)
            .all()
        )
