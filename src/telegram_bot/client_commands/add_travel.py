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
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import (
    kbm_main_menu,
    kbm_travels_menu,
    kbm_y_or_n,
)


class TravelAdd(StatesGroup):
    name_input = State()
    description_input = State()
    city_input = State()
    city_check = State()
    city_start_date_input = State()
    city_start_date_input = State()
    city_end_date_input = State()
    add_one_more_city = State()


crud_user = CrudUser(User)
crud_travel = CrudTravel(Travel)
crud_user_travel = CrudUserTravel(UserTravel)
crud_travel_city = CrudTravelCity(TravelCity)

router = Router()

TRAVEL_NAME_REQUEST = message_markdowns.get("travel_name_request")
TRAVEL_NAME_ALREADY_EXISTS = message_markdowns.get("travel_name_already_exists")
TRAVEL_DESCRIPTION_REQUEST = message_markdowns.get("travel_description_request")
TRAVEL_CITY_REQUEST = message_markdowns.get("travel_city_request")
TRAVEL_CITY_CHECK = "Бот правильно определил город: {}?"
TRAVEL_CITY_REREQUEST = message_markdowns.get("travel_city_request")
TRAVEL_CITY_START_DATE_REQUEST = message_markdowns.get("travel_city_start_date_request")
INVALID_DATE_SYNTAX = message_markdowns.get("invalid_date_syntax")
TRAVEL_CITY_END_DATE_REQUEST = message_markdowns.get("travel_city_end_date_request")
ADD_MORE_CITIES_REQUEST = message_markdowns.get("add_more_cities_request")
ADD_MORE_CITIES_REQUEST = message_markdowns.get("add_more_cities_request")
TRAVEL_HAS_BEEN_ADDED = message_markdowns.get("travel_has_been_added")


@router.callback_query(F.data == "add_travel")
async def request_name(query: types.CallbackQuery, state: FSMContext) -> None:
    """The first step of the add travel command: requesting travel name."""
    await state.set_state(TravelAdd.name_input)
    await bot.send_message(query.from_user.id, TRAVEL_NAME_REQUEST)


@router.message(TravelAdd.name_input)
async def request_description(
    message: types.message, state: FSMContext, db: Session
) -> None:
    """Saving entered travel name and requesting travel description."""
    travel_name = message.text
    user = crud_user.get_by_telegram_id(db, message.from_user.id)

    if crud_travel.is_name(db, user, travel_name):
        await bot.send_message(message.from_user.id, TRAVEL_NAME_ALREADY_EXISTS, parse_mode=ParseMode.HTML)
        return

    await state.update_data(travel_name=travel_name)
    await state.set_state(TravelAdd.description_input)
    await bot.send_message(message.from_user.id, TRAVEL_DESCRIPTION_REQUEST, parse_mode=ParseMode.HTML)


@router.message(TravelAdd.description_input)
async def request_city(message: types.message, state: FSMContext, db: Session) -> None:
    """Saving entered travel description and requesting travel cities."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)
    travel_description = message.text
    data = await state.get_data()
    travel = Travel(
        owner_id=user.id, name=data["travel_name"], description=travel_description
    )
    travel = crud_travel.create(db, travel)
    user_travel = UserTravel(user_id=user.id, travel_id=travel.id)
    crud_user_travel.create(db, user_travel)

    await state.update_data(travel_id=travel.id)
    await state.set_state(TravelAdd.city_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_REQUEST, parse_mode=ParseMode.HTML)


@router.message(TravelAdd.city_input)
async def check_city(message: types.message, state: FSMContext) -> None:
    """Getting city and sending check kbm if city is determined correctly."""
    address = geography.get_address(message.text)

    await state.update_data(city=address)
    await state.set_state(TravelAdd.city_check)
    await bot.send_message(
        message.from_user.id,
        TRAVEL_CITY_CHECK.format(address),
        reply_markup=kbm_y_or_n,
    )


@router.callback_query(F.data == "no", TravelAdd.city_check)
async def rerequest_address(message: types.message, state: FSMContext):
    """Reasking user for the adress."""
    await state.set_state(TravelAdd.city_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_REREQUEST, parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "yes", TravelAdd.city_check)
async def save_address(message: types.message, state: FSMContext):
    """Requesting user for start date of the city in travel."""
    await state.set_state(TravelAdd.city_start_date_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_START_DATE_REQUEST, parse_mode=ParseMode.HTML)


@router.message(TravelAdd.city_start_date_input)
async def request_end_date(message: types.message, state: FSMContext):
    """Saving travel city start date and requesting end date."""
    day, month, year = 0, 0, 0
    try:
        day, month, year = map(int, message.text.split("."))
    except:
        await state.set_state(TravelAdd.city_start_date_input)
        await bot.send_message(message.from_user.id, INVALID_DATE_SYNTAX, parse_mode=ParseMode.HTML)
        return

    start_date = datetime(year=year, month=month, day=day)
    await state.update_data(travel_city_start_date=start_date)
    await state.set_state(TravelAdd.city_end_date_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_END_DATE_REQUEST, parse_mode=ParseMode.HTML)


@router.message(TravelAdd.city_end_date_input)
async def save_travel_city(message: types.message, state: FSMContext, db: Session):
    """Saving travel city and requesting user if he wants to add more cities."""
    day, month, year = 0, 0, 0
    try:
        day, month, year = map(int, message.text.split("."))
    except:
        await state.set_state(TravelAdd.city_end_date_input)
        await bot.send_message(message.from_user.id, INVALID_DATE_SYNTAX, parse_mode=ParseMode.HTML)
        return

    travel_city_end_date = datetime(year=year, month=month, day=day)

    data = await state.get_data()
    travel_id = data["travel_id"]
    travel = crud_travel.get(db, travel_id)
    address = data["city"]
    city = geography.get_place_by_address(address)
    travel_city_start_date = data["travel_city_start_date"]

    travel_city = TravelCity(
        travel_id=travel.id,
        address=address,
        city=city,
        start_date=travel_city_start_date,
        end_date=travel_city_end_date,
    )
    travel_city = crud_travel_city.create(db, travel_city)

    await state.set_state(TravelAdd.add_one_more_city)
    await bot.send_message(
        message.from_user.id, ADD_MORE_CITIES_REQUEST, reply_markup=kbm_y_or_n, parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "yes", TravelAdd.add_one_more_city)
async def request_one_more_travel_city(message: types.message, state: FSMContext):
    """Reasking user for the adress."""
    await state.set_state(TravelAdd.city_input)
    await bot.send_message(message.from_user.id, TRAVEL_CITY_REREQUEST)


@router.callback_query(F.data == "no", TravelAdd.add_one_more_city)
async def end_travel_add(message: types.message, state: FSMContext):
    """Requesting user for start date of the city in travel."""
    await state.clear()
    await bot.send_message(
        message.from_user.id, TRAVEL_HAS_BEEN_ADDED, reply_markup=kbm_travels_menu, parse_mode=ParseMode.HTML
    )
