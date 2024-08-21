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
from src.telegram_bot.client_commands.list_travels import generate_travel_message
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import (
    kbm_main_menu,
    kbm_travel_menu,
    kbm_travels_menu,
    kbm_y_or_n,
)


class NoteAddForm(StatesGroup):
    is_public = State()
    description = State()
    attachment = State()


REQUEST_IS_PUBLIC = "Хотите ли вы сделать заметку публичным?"
REQUEST_NOTE = "Отправь, пожалуйтса, заметку к путешествию:"
REQUEST_ATTACHMENT = "Есть ли у вас приложение к заметке? Если да, то отправьте файл, иначе нажмите /skip"

crud_user = CrudUser(User)
crud_travel = CrudTravel(Travel)
crud_travel_city = CrudTravelCity(TravelCity)
crud_travel_note = CrudTravelNote(TravelNote)
crud_user_travel = CrudUserTravel(UserTravel)

router = Router()


@router.callback_query(F.data == "add_note")
async def request_note(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Bot function to add note to the travel."""
    await state.set_state(NoteAddForm.is_public)
    await bot.send_message(
        query.from_user.id, REQUEST_IS_PUBLIC, reply_markup=kbm_y_or_n
    )


@router.callback_query(F.data == "yes")
async def save_public(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Save not public."""
    await state.update_data(is_public=True)
    await state.set_state(NoteAddForm.description)
    await bot.send_message(query.from_user.id, REQUEST_NOTE)


@router.callback_query(F.data == "no")
async def save_not_public(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Save note not public."""
    await state.update_data(is_public=False)
    await state.set_state(NoteAddForm.description)
    await bot.send_message(query.from_user.id, REQUEST_NOTE)


@router.message(NoteAddForm.description)
async def request_attacment(
    messsage: types.Message, state: FSMContext, db: Session
) -> None:
    """Saving entered description and requesting attachment."""
    await state.update_data(description=messsage.text)
    await state.set_state(NoteAddForm.attachment)
    await bot.send_message(messsage.from_user.id, REQUEST_ATTACHMENT)


@router.message(NoteAddForm.attachment, F.content_type.in_({"document"}))
async def save_document(message: types.Message, state: FSMContext, db: Session) -> None:
    """Saving attached document."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)

    file_id = message.document.file_id
    file_name = message.document.file_name
    file_path = await bot.get_file(file_id)
    await message.bot.download(file_path, f"{settings.STORAGE_PATH}/{file_name}")

    data = await state.get_data()
    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel
    travel_note = TravelNote(
        travel_id=travel.id,
        note=data["description"],
        attached_file=file_name,
        is_public=data["is_public"],
        owner_id=user.id,
    )
    travel_note = crud_travel_note.create(db, travel_note)

    await bot.send_message(
        message.from_user.id,
        generate_travel_message(db, user, travel_index=data["travel_index"]),
        reply_markup=kbm_travel_menu,
    )


@router.message(NoteAddForm.attachment, Command("skip"))
async def skip_document(message: types.Message, state: FSMContext, db: Session) -> None:
    """Saving note without document."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)
    data = await state.get_data()
    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel
    travel_note = TravelNote(
        travel_id=travel.id,
        note=data["description"],
        is_public=data["is_public"],
        owner_id=user.id,
    )
    travel_note = crud_travel_note.create(db, travel_note)

    await bot.send_message(
        message.from_user.id,
        generate_travel_message(db, user, travel_index=data["travel_index"]),
        reply_markup=kbm_travel_menu,
    )
