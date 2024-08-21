"""User CRUD testing."""

import sys

from environs import Env

env = Env()
sys.path.append(env("PATH_TO_PROJECT"))
from src.core import settings
from src.crud import CrudUser
from src.database import SessionLocal
from src.models import User
from src.tests.utils import clean_db

if not settings.IS_TEST_SETTINGS:
    exit()

crud_user = CrudUser(User)


def test_create_user() -> None:
    """Test case for inserting user into database."""
    # clean_db()
    db = SessionLocal()
    user_create = User(
        telegram_id=100, login="jakefish", address="Ufa", description="test user"
    )

    created_user: User = crud_user.create(db, user_create)

    assert type(created_user.id) is int
    assert created_user.id >= 1
    assert created_user.login == "jakefish"
    assert created_user.telegram_id == 100
    assert created_user.description == "test user"
    assert created_user.address == "Ufa"

    crud_user.delete(db, created_user.id)
    db.close()


def test_get_user() -> None:
    """Test case for selecting user from database."""
    # clean_db()
    db = SessionLocal()
    user_create = User(
        telegram_id=100, login="jakefish", address="Ufa", description="test user"
    )
    created_user: User = crud_user.create(db, user_create)
    gotten_user: User = crud_user.get(db, created_user.id)

    assert type(gotten_user.id) is int
    assert gotten_user.id >= 1
    assert gotten_user.login == "jakefish"
    assert gotten_user.telegram_id == 100
    assert gotten_user.description == "test user"
    assert gotten_user.address == "Ufa"

    crud_user.delete(db, created_user.id)
    db.close()


def test_delete_user() -> None:
    """Test case for deleting user from database."""
    # clean_db()
    db = SessionLocal()
    user_create = User(
        telegram_id=100, login="jakefish", address="Ufa", description="test user"
    )
    created_user: User = crud_user.create(db, user_create)
    user_id = created_user.id
    crud_user.delete(db, created_user.id)
    deleted_user = crud_user.get(db, user_id)

    assert deleted_user == None

    db.close()
