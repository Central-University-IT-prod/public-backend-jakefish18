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
    kbm_travel_note_menu,
    kbm_travels_menu,
    kbm_y_or_n,
)


class FriendInviteForm(StatesGroup):
    login = State()


LOGIN_REQUEST = (
    "Отправьте логин пользователя, с которым вы хотите поделиться путешествием:"
)
USER_NOT_FOUND = "🚫 Пользователя с таким логином нет :("
USER_ADDED = "{} был добавлен!"
USER_INVATION_NOTIFICATION = '✅ Вы были добавлены в путешествие "{}" пользователем {}!'

crud_user = CrudUser(User)
crud_user_travel = CrudUserTravel(UserTravel)
crud_travel = CrudTravel(Travel)
crud_travel_city = CrudTravelCity(TravelCity)
crud_travel_note = CrudTravelNote(TravelNote)

router = Router()


@router.callback_query(F.data == "invite_friend")
async def login_request(query: types.CallbackQuery, state: FSMContext) -> None:
    """Requesting user login to invite."""
    await state.set_state(FriendInviteForm.login)
    await bot.send_message(query.from_user.id, LOGIN_REQUEST)


@router.message(FriendInviteForm.login)
async def find_friend(
    message: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Adding inputed user."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)
    login = message.text
    user_to_invite = crud_user.get_by_login(db, login)

    data = await state.get_data()

    if not user_to_invite:
        await bot.send_message(
            message.from_user.id,
            USER_NOT_FOUND
            + "\n\n"
            + generate_travel_message(db, user, travel_index=data["travel_index"]),
            reply_markup=kbm_travel_menu,
        )
        return

    data = await state.get_data()

    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel
    user_travel = UserTravel(user_id=user_to_invite.id, travel_id=travel.id)
    user_travel = crud_user_travel.create(db, user_travel)

    await bot.send_message(
        message.from_user.id,
        USER_ADDED.format(login)
        + "\n\n"
        + generate_travel_message(db, user, travel_index=data["travel_index"]),
        reply_markup=kbm_travel_menu,
    )
    await bot.send_message(
        user_to_invite.telegram_id,
        USER_INVATION_NOTIFICATION.format(travel.name, user.login),
    )
