from datetime import datetime

import aiogram.utils.markdown as fmt
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from src import geography
from src.crud import CrudTravel, CrudTravelCity, CrudUser, CrudUserTravel
from src.models import Travel, TravelCity, User, UserTravel
from src.telegram_bot import message_markdowns
from src.telegram_bot.client_commands.list_travels import generate_travel_message
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import (
    kbm_main_menu,
    kbm_travel_menu,
    kbm_travels_menu,
    kbm_y_or_n,
)


class AddTravelCity(StatesGroup):
    add_travel_city = State()
    city_check = State()
    city_start_date_input = State()
    city_end_date_input = State()
    add_one_more_city = State()


TRAVEL_CITY_REQUEST = message_markdowns.get("travel_city_extend_request")
TRAVEL_CITY_CHECK = "Бот правильно определил город: {}?"
TRAVEL_CITY_HAS_BEEN_ADDED = "Город был успешно добавлен!"
TRAVEL_CITY_CHECK = "Бот правильно определил город: {}?"
TRAVEL_CITY_START_DATE_REQUEST = message_markdowns.get("travel_city_start_date_request")
INVALID_DATE_SYNTAX = message_markdowns.get("invalid_date_syntax")
TRAVEL_CITY_END_DATE_REQUEST = message_markdowns.get("travel_city_end_date_request")
ADD_MORE_CITIES_REQUEST = message_markdowns.get("travel_cities_has_been_extended")


crud_user = CrudUser(User)
crud_travel = CrudTravel(Travel)
crud_travel_city = CrudTravelCity(TravelCity)
crud_user_travel = CrudUserTravel(UserTravel)

router = Router()


@router.callback_query(F.data == "add_travel_city")
async def request_city(message: types.Message, state: FSMContext, db: Session) -> None:
    """Saving entered travel description and requesting travel cities."""
    await state.set_state(AddTravelCity.add_travel_city)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_REQUEST)


@router.message(AddTravelCity.add_travel_city)
async def add_travel_city(
    message: types.Message, state: FSMContext, db: Session
) -> None:
    """The one more trash handler for address input."""
    address = geography.get_address(message.text)

    await state.update_data(city=address)
    await state.set_state(AddTravelCity.city_check)
    await bot.send_message(
        message.from_user.id,
        TRAVEL_CITY_CHECK.format(address),
        reply_markup=kbm_y_or_n,
    )


@router.callback_query(F.data == "no", AddTravelCity.city_check)
async def rerequest_address(message: types.message, state: FSMContext):
    """Reasking user for the adress."""
    await state.set_state(AddTravelCity.add_travel_city)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_REQUEST)


@router.callback_query(F.data == "yes", AddTravelCity.city_check)
async def save_address(message: types.message, state: FSMContext):
    """Requesting user for start date of the city in travel."""
    await state.set_state(AddTravelCity.city_start_date_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_START_DATE_REQUEST)


@router.message(AddTravelCity.city_start_date_input)
async def request_end_date(message: types.message, state: FSMContext):
    """Saving travel city start date and requesting end date."""
    day, month, year = 0, 0, 0
    try:
        day, month, year = map(int, message.text.split("."))
    except:
        await state.set_state(AddTravelCity.city_start_date_input)
        await bot.send_message(message.from_user.id, INVALID_DATE_SYNTAX)
        return

    start_date = datetime(year=year, month=month, day=day)
    await state.update_data(travel_city_start_date=start_date)
    await state.set_state(AddTravelCity.city_end_date_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_END_DATE_REQUEST)


@router.message(AddTravelCity.city_end_date_input)
async def save_travel_city(message: types.message, state: FSMContext, db: Session):
    """Saving travel city and requesting user if he wants to add more cities."""
    day, month, year = 0, 0, 0
    try:
        day, month, year = map(int, message.text.split("."))
    except:
        await state.set_state(AddTravelCity.city_end_date_input)
        await bot.send_message(message.from_user.id, INVALID_DATE_SYNTAX)
        return

    travel_city_end_date = datetime(year=year, month=month, day=day)

    user = crud_user.get_by_telegram_id(db, message.from_user.id)
    data = await state.get_data()
    travel_index = data["travel_index"]
    travel = crud_user_travel.get_by_offset(db, user, travel_index - 1).travel
    address = data["city"]
    city = geography.get_place_by_address(address)
    travel_city_start_date = data["travel_city_start_date"]

    travel_city = TravelCity(
        travel_id=travel.id,
        city=city,
        address=address,
        start_date=travel_city_start_date,
        end_date=travel_city_end_date,
    )
    travel_city = crud_travel_city.create(db, travel_city)

    await state.set_state(AddTravelCity.add_one_more_city)
    await bot.send_message(
        message.from_user.id, ADD_MORE_CITIES_REQUEST, reply_markup=kbm_y_or_n
    )


@router.callback_query(F.data == "yes", AddTravelCity.add_one_more_city)
async def request_one_more_travel_city(message: types.message, state: FSMContext):
    """Reasking user for the adress."""
    await state.set_state(AddTravelCity.city_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_REQUEST)


@router.callback_query(F.data == "no", AddTravelCity.add_one_more_city)
async def end_travel_add(message: types.message, state: FSMContext, db: Session):
    """Sending the travel message with updated cities."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)
    data = await state.get_data()
    travel_index = data["travel_index"]
    await bot.send_message(
        message.from_user.id,
        generate_travel_message(db, user, travel_index),
        reply_markup=kbm_travel_menu,
    )
