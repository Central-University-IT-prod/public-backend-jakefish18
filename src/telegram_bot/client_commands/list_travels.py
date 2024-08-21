from datetime import datetime

import aiogram.utils.markdown as fmt
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from src import geography
from src.crud import CrudTravel, CrudTravelCity, CrudUser, CrudUserTravel
from src.models import Travel, TravelCity, User, UserTravel
from src.telegram_bot import message_markdowns
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import (
    kbm_main_menu,
    kbm_travel_menu,
    kbm_travels_menu,
    kbm_y_or_n,
)

TRAVEL_MESSAGE = message_markdowns.get("travel_message")
NOT_ENOUGH_PERMISSION = "🚫 Вы не являетесь автором путешествия"

crud_user = CrudUser(User)
crud_travel = CrudTravel(Travel)
crud_travel_city = CrudTravelCity(TravelCity)
crud_user_travel = CrudUserTravel(UserTravel)

router = Router()


def generate_travel_message(db: Session, user: User, travel_index: int) -> str:
    """
    Genearting travel info message.

    Parameters:
        eleent_index: int - the index of the user travel to get. Counting starts from 1.

    Returns:
        resposne: str - created message
    """
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel
    total_travels = len(user.travels)
    travel_name = travel.name
    travel_description = travel.description

    travel_cities = ""

    for i, travel_city in enumerate(travel.cities):
        start_date = travel_city.start_date.strftime("%d.%m.%Y")
        end_date = travel_city.end_date.strftime("%d.%m.%Y")
        travel_cities += f"{i + 1}.{travel_city.city} [{start_date} - {end_date}]\n"

    travel_cities = travel_cities.strip()
    travel_users = ""

    for i, travel_user in enumerate(travel.users):
        travel_users += f"{i + 1}.{travel_user.user.login}\n"

    message = TRAVEL_MESSAGE.format(
        travel_index,
        total_travels,
        travel_name,
        travel_description,
        travel_cities,
        travel_users,
    )

    return message


@router.callback_query(F.data == "list_travels")
async def list_travels(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Sending user the travels list with menu."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)

    if len(user.travels) == 0:
        await query.message.edit_text(
            "У вас нет путешествий :(", reply_markup=kbm_travels_menu
        )
        return

    await state.update_data(travel_index=1)
    await query.message.edit_text(
        generate_travel_message(
            db,
            user,
            travel_index=1,
        ),
        reply_markup=kbm_travel_menu,
    )


@router.callback_query(F.data == "next_travel")
async def list_travels(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Sending user the next travel menu."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)

    data = await state.get_data()
    travel_index = data["travel_index"] + 1

    # Check after other user delete.
    if len(user.travels) == 0:
        await state.clear()
        await query.message.edit_text(
            "У вас больше нет путешествий :(", reply_markup=kbm_main_menu
        )
        return

    # Going to first element if it's already the latest travel.
    if travel_index > len(user.travels):
        travel_index = 1

    await state.update_data(travel_index=travel_index)
    await query.message.edit_text(
        generate_travel_message(
            db,
            user,
            travel_index=travel_index,
        ),
        reply_markup=kbm_travel_menu,
    )


@router.callback_query(F.data == "previous_travel")
async def list_travels(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Sending user the previous travel menu."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)

    data = await state.get_data()
    travel_index = max(data["travel_index"] - 1, 1)

    # Check after other user delete.
    if len(user.travels) == 0:
        await state.clear()
        await query.message.edit_text(
            "У вас больше нет путешествий :(", reply_markup=kbm_main_menu
        )
        return

    # Going to last element if it's already the earliest travel.
    if travel_index == data["travel_index"]:
        travel_index = len(user.travels)

    await state.update_data(travel_index=travel_index)
    await query.message.edit_text(
        generate_travel_message(
            db,
            user,
            travel_index=travel_index,
        ),
        reply_markup=kbm_travel_menu,
    )


@router.callback_query(F.data == "delete_travel")
async def delete_travel(
    query: types.CallbackQuery, state: FSMContext, db: Session
) -> None:
    """Deleting travel."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)

    data = await state.get_data()
    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel

    if travel.owner_id != user.id:
        await query.message.edit_text(
            NOT_ENOUGH_PERMISSION
            + "\n\n"
            + generate_travel_message(
                db,
                user,
                travel_index=travel_index,
            ),
            reply_markup=kbm_travel_menu,
        )
        return

    crud_travel.delete(db, travel.id)

    # Case where user has deleted all travels.
    if len(user.travels) == 0:
        await state.clear()
        await query.message.edit_text(
            "У вас больше нет путешествий :(", reply_markup=kbm_main_menu
        )
        return

    # Case where user has deleted the last travel.
    if travel_index > len(user.travels):
        travel_index = len(user.travels)
        await state.update_data(travel_index=travel_index)

    await query.message.edit_text(
        generate_travel_message(
            db,
            user,
            travel_index=travel_index,
        ),
        reply_markup=kbm_travel_menu,
    )
