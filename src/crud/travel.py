"""
CRUD requests for tavels.
"""

from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from src.crud.base import CrudBase
from src.models import Travel, User


class CrudTravel(CrudBase[Travel]):
    def __init__(self, Model: type[Travel]):
        super().__init__(Model)

    def get_travel_by_name(
        self, db: Session, user: User, name: str
    ) -> Union[Travel, None]:
        """Get user travel by name."""
        return (
            db.query(Travel)
            .filter(and_(Travel.owner_id == user.id, Travel.name == name))
            .first()
        )

    def is_name(self, db: Session, user: User, name: str) -> bool:
        """Check if usre has already used that name for travel."""
        return self.get_travel_by_name(db, user, name) != None
