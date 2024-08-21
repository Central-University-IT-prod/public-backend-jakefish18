import uuid
from datetime import datetime

import aiogram.utils.markdown as fmt
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from src import geography
from src.core import settings
from src.crud import (
    CrudTravel,
    CrudTravelCity,
    CrudTravelNote,
    CrudUser,
    CrudUserTravel,
)
from src.models import Travel, TravelCity, TravelNote, User, UserTravel
from src.telegram_bot import message_markdowns
from src.telegram_bot.client_commands.list_travels import generate_travel_message
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import (
    kbm_main_menu,
    kbm_travel_menu,
    kbm_travel_note_menu,
    kbm_travels_menu,
    kbm_y_or_n,
)


class NoteAddForm(StatesGroup):
    description = State()
    attachment = State()


NOTE_MESSAGE = message_markdowns.get("note_message")


def generate_note_message(
    db: Session, user: User, travel: Travel, note_index: int
) -> str:
    """Getting note message by note index."""
    note = crud_travel_note.get_note_by_index(db, user, travel, note_index)
    notes_count = len(crud_travel_note.get_notes(db, user, travel))
    note_type = "Доступно только тебе" if not note.is_public else "Доступно всем участникам путешествия" 
    message = NOTE_MESSAGE.format(note_index, notes_count, note.note, note.owner.login, note_type)

    return message


REQUEST_NOTE = "Отправь, пожалуйтса, заметку к путешествию:"
REQUEST_ATTACHMENT = "Есть ли у вас приложение к заметке? Если да, то отправьте файл, иначе нажмите /skip"

crud_user = CrudUser(User)
crud_travel = CrudTravel(Travel)
crud_travel_city = CrudTravelCity(TravelCity)
crud_travel_note = CrudTravelNote(TravelNote)
crud_user_travel = CrudUserTravel(UserTravel)

router = Router()


@router.callback_query(F.data == "notes_menu")
async def send_note_menu(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Sending user the notes list with menu."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)
    data = await state.get_data()
    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel

    notes_count = len(crud_travel_note.get_notes(db, user, travel))
    if notes_count == 0:
        return

    note = crud_travel_note.get_note_by_index(db, user, travel, 1)

    await state.update_data(note_index=1)

    if note.attached_file:
        agenda = types.FSInputFile(f"{settings.STORAGE_PATH}/{note.attached_file}")
        message = await bot.send_document(query.from_user.id, agenda)
        await state.update_data(last_document_id=message.message_id)

    await query.message.edit_text(
        generate_note_message(
            db,
            user,
            travel,
            note_index=1,
        ),
        reply_markup=kbm_travel_note_menu,
    )


@router.callback_query(F.data == "next_note")
async def next_note(query: types.CallbackQuery, state: FSMContext, db: Session) -> None:
    """Sending user the next note menu."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)

    data = await state.get_data()
    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel
    note_index = data["note_index"] + 1

    # Going to first element if it's already the latest note.
    notes_count = len(crud_travel_note.get_notes(db, user, travel))
    if note_index > notes_count:
        note_index = 1

    await state.update_data(note_index=note_index)

    if data.get("last_document_id"):
        await bot.delete_message(query.message.chat.id, data["last_document_id"])

    note: TravelNote = crud_travel_note.get_note_by_index(db, user, travel, note_index)
    if note.attached_file:
        agenda = types.FSInputFile(f"{settings.STORAGE_PATH}/{note.attached_file}")
        message = await bot.send_document(query.from_user.id, agenda)
        await state.update_data(last_document_id=message.message_id)
    else:
        await state.update_data(last_document_id=None)

    await query.message.edit_text(
        generate_note_message(
            db,
            user,
            travel,
            note_index=note_index,
        ),
        reply_markup=kbm_travel_note_menu,
    )


@router.callback_query(F.data == "previous_note")
async def previous_note(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Sending user the previous note menu."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)

    data = await state.get_data()
    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel
    note_index = data["note_index"] - 1

    # Going to the last element if it's already the latest note.
    notes_count = len(crud_travel_note.get_notes(db, user, travel))
    if note_index <= 0:
        note_index = notes_count

    await state.update_data(note_index=note_index)

    if data.get("last_document_id"):
        await bot.delete_message(query.message.chat.id, data["last_document_id"])

    note: TravelNote = crud_travel_note.get_note_by_index(db, user, travel, note_index)
    if note.attached_file:
        agenda = types.FSInputFile(f"{settings.STORAGE_PATH}/{note.attached_file}")
        message = await bot.send_document(query.from_user.id, agenda)
        await state.update_data(last_document_id=message.message_id)
    else:
        await state.update_data(last_document_id=None)

    await query.message.edit_text(
        generate_note_message(
            db,
            travel,
            note_index=note_index,
        ),
        reply_markup=kbm_travel_note_menu,
    )
