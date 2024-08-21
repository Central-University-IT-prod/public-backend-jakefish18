from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from src import geography
from src.crud import CrudUser
from src.geography import get_address
from src.models import User
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import kbm_main_menu, kbm_y_or_n
from src.telegram_bot import message_markdowns

crud_user = CrudUser(User)


class Registration(StatesGroup):
    login_input = State()
    address_input = State()
    address_check = State()
    description_input = State()


LOGIN_REQUEST = message_markdowns.get("login_request")
LOGIN_ALREADY_EXISTS = message_markdowns.get("login_already_exists")
ADDRESS_REQUEST = message_markdowns.get("address_request")
ADDRESS_CHECK = "Твой адрес: {}?"
ADDRESS_REREQUEST = "Введите свой адрес:"
DESCRIPTION_REQUEST = message_markdowns.get("description_request")
SUCCESSFUL_REGISTRATION = message_markdowns.get("successful_registration")
ALREADY_REGISTERED = message_markdowns.get("already_registered")


router = Router()


@router.message(Command("start"))
async def start(message: types.message, state: FSMContext, db: Session) -> None:
    """
    Adding user into the database after
    user executes /start command.
    """
    if crud_user.is_telegram_id(db, message.from_user.id):
        await bot.send_message(
            message.from_user.id, ALREADY_REGISTERED, reply_markup=kbm_main_menu, parse_mode=ParseMode.HTML
        )
        return

    await state.set_state(Registration.login_input)
    await bot.send_message(message.from_user.id, LOGIN_REQUEST, parse_mode=ParseMode.HTML)


@router.message(Registration.login_input)
async def save_login(message: types.message, state: FSMContext, db: Session) -> None:
    """
    Getting and saving user login if there is not such login in database.
    """
    login = message.text

    if crud_user.is_login(db, login):
        await bot.send_message(message.from_user.id, LOGIN_ALREADY_EXISTS)
        return

    await state.update_data(login=login)
    await state.set_state(Registration.address_input)
    await bot.send_message(message.from_user.id, ADDRESS_REQUEST, parse_mode=ParseMode.HTML)


@router.message(Registration.address_input)
async def check_address(message: types.message, state: FSMContext):
    """
    Getting and saving user address.
    """
    address = geography.get_address(message.text)

    await state.update_data(address=address)
    await state.set_state(Registration.address_check)
    await bot.send_message(
        message.from_user.id,
        ADDRESS_CHECK.format(address),
        reply_markup=kbm_y_or_n,
    )


@router.callback_query(F.data == "no", Registration.address_check)
async def rerequest_address(message: types.message, state: FSMContext):
    """Reasking user for the adress."""
    await state.set_state(Registration.address_input)
    await bot.send_message(message.from_user.id, ADDRESS_REREQUEST)


@router.callback_query(F.data == "yes", Registration.address_check)
async def save_address(message: types.message, state: FSMContext):
    """Requesting user for description."""
    await state.set_state(Registration.description_input)
    await bot.send_message(message.from_user.id, DESCRIPTION_REQUEST, parse_mode=ParseMode.HTML)


@router.message(Registration.description_input)
async def save_user(message: types.message, state: FSMContext, db: Session):
    """Registering user with all needed data passed."""
    user_data = await state.get_data()
    user = User(
        telegram_id=message.from_user.id,
        login=user_data["login"],
        address=user_data["address"],
        description=message.text,
    )
    user = crud_user.create(db, user)

    await state.clear()
    await bot.send_message(
        message.from_user.id, SUCCESSFUL_REGISTRATION, reply_markup=kbm_main_menu, parse_mode=ParseMode.HTML
    )
