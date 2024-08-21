"""Travel Notes CRUD testing."""

import sys

from environs import Env

env = Env()
sys.path.append(env("PATH_TO_PROJECT"))
from src.core import settings
from src.crud import CrudTravel, CrudTravelNote, CrudUser
from src.database import SessionLocal
from src.models import Travel, TravelNote, User
from src.tests.utils import clean_db

if not settings.IS_TEST_SETTINGS:
    exit()

crud_user = CrudUser(User)
crud_travel = CrudTravel(Travel)
crud_travel_note = CrudTravelNote(TravelNote)


def test_travel_notes_adding_1() -> None:
    """Test case for inserting travel notes into database."""
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

    notes_data = [
        {
            "travel_id": created_travel.id,
            "note": "1 заметка",
            "owner_id": created_user.id,
            "is_public": True,
        },
        {
            "travel_id": created_travel.id,
            "note": "2 заметка",
            "owner_id": created_user.id,
            "is_public": True,
        },
    ]

    for note_data in notes_data:
        create_note = TravelNote(
            travel_id=note_data["travel_id"],
            note=note_data["note"],
            owner_id=note_data["owner_id"],
            is_public=note_data["is_public"],
        )
        crud_travel_note.create(db, create_note)

    notes = crud_travel_note.get_notes(db, created_user, created_travel)

    assert notes[0].note == notes_data[0]["note"]
    assert notes[1].note == notes_data[1]["note"]

    crud_user.delete(db, created_user.id)
    db.close()


def test_travel_notes_adding_2() -> None:
    """Test case for selecting travel from database."""
    # clean_db()
    db = SessionLocal()
    user_create_1 = User(
        telegram_id=100, login="jakefish", address="Ufa", description="test user"
    )
    created_user_1: User = crud_user.create(db, user_create_1)
    user_create_2 = User(
        telegram_id=101, login="jakefish2", address="Ufa", description="test user"
    )
    created_user_2: User = crud_user.create(db, user_create_2)
    travel_create: Travel = Travel(
        owner_id=created_user_1.id, name="PROD", description="Лечу на прод"
    )
    created_travel = crud_travel.create(db, travel_create)

    notes_data = [
        {
            "travel_id": created_travel.id,
            "note": "1 заметка",
            "owner_id": created_user_1.id,
            "is_public": False,
        },
        {
            "travel_id": created_travel.id,
            "note": "2 заметка",
            "owner_id": created_user_1.id,
            "is_public": False,
        },
    ]

    for note_data in notes_data:
        create_note = TravelNote(
            travel_id=note_data["travel_id"],
            note=note_data["note"],
            owner_id=note_data["owner_id"],
            is_public=note_data["is_public"],
        )
        crud_travel_note.create(db, create_note)

    notes = crud_travel_note.get_notes(db, created_user_2, created_travel)

    assert len(notes) == 0

    crud_user.delete(db, created_user_1.id)
    crud_user.delete(db, created_user_2.id)
    db.close()
