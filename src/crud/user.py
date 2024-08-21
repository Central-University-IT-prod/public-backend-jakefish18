"""
CRUD requests for user.
"""

from typing import Union

from sqlalchemy.orm import Session

from src.crud.base import CrudBase
from src.models import User


class CrudUser(CrudBase[User]):
    def __init__(self, Model: type[User]):
        super().__init__(Model)

    def get_by_telegram_id(self, db: Session, telegram_id: int) -> Union[User, None]:
        """
        Getting user by telegram id.

        Parameters:
            telegram_id: int - telegram id of the user to get user id.

        Returns:
            user: User - user.
            None if there isn't user with the same telegram id.
        """
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    def is_telegram_id(self, db: Session, telegram_id: int) -> bool:
        """
        Checking if there is a user with given telegram_id.

        Arguments:
            telegram_id int - telegram_id to check.

        Returns:
            Bool flag which equals to True if there is user with the same telegram id in database
        """
        return self.get_by_telegram_id(db, telegram_id) != None

    def get_by_login(self, db: Session, login: str) -> Union[User, None]:
        """
        Getting user by login.

        Parameters:
            login: str - login of the user to get.

        Returns:
            user: User - user.
            None if there isn't user with the same login.
        """
        return db.query(User).filter(User.login == login).first()

    def is_login(self, db: Session, login: str) -> bool:
        """
        Checking if there is a user with the given login.

        Arguments:
            login: str - login to check.

        Returns:
            Bool flag which equals to True if there is user with the same login in database
        """
        return self.get_by_login(db, login) != None
