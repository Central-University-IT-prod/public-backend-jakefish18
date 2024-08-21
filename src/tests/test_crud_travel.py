"""Travel CRUD testing."""

import sys

from environs import Env

env = Env()
sys.path.append(env("PATH_TO_PROJECT"))
from src.core import settings
from src.crud import CrudTravel, CrudUser
from src.database import SessionLocal, init_db
from src.models import Travel, User
from src.tests.utils import clean_db

if not settings.IS_TEST_SETTINGS:
    exit()

crud_user = CrudUser(User)
crud_travel = CrudTravel(Travel)


def test_create_travel() -> None:
    """Test case for inserting travel into database."""
    # clean_db()
    db = SessionLocal()
    user_create = User(
        telegram_id=100, login="jakefish", address="Уфа", description="Лечу на прод"
    )
    created_user = crud_user.create(db, user_create)
    travel_create: Travel = Travel(
        owner_id=created_user.id, name="PROD", description="Лечу на прод"
    )
    created_travel = crud_travel.create(db, travel_create)

    assert type(created_travel.id) is int
    assert created_travel.id >= 1
    assert created_travel.owner_id == created_user.id
    assert created_travel.name == "PROD"
    assert created_travel.description == "Лечу на прод"

    crud_user.delete(db, created_user.id)
    db.close()


def test_get_travel() -> None:
    """Test case for selecting travel from database."""
    # clean_db()
    db = SessionLocal()
    user_create = User(
        telegram_id=100, login="jakefish", address="Ufa", description="test user"
    )
    created_user: User = crud_user.create(db, user_create)
    travel_create: Travel = Travel(
        owner_id=created_user.id, name="PROD", description="Лечу на прод"
    )
    created_travel = crud_travel.create(db, travel_create)
    gotten_travel = crud_travel.get(db, created_travel.id)

    assert type(gotten_travel.id) is int
    assert gotten_travel.id >= 1
    assert gotten_travel.owner_id == created_user.id
    assert gotten_travel.name == "PROD"
    assert gotten_travel.description == "Лечу на прод"

    crud_user.delete(db, created_user.id)
    db.close()
