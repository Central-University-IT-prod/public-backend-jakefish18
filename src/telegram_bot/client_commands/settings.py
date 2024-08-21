import aiogram.utils.markdown as fmt
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from src import geography
from src.crud import CrudUser
from src.models import User
from src.telegram_bot import message_markdowns
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import kbm_main_menu, kbm_settings, kbm_y_or_n


class LoginChange(StatesGroup):
    login_input = State()


class AddressChange(StatesGroup):
    address_input = State()
    address_check = State()


class DescriptionChange(StatesGroup):
    desription_input = State()


crud_user = CrudUser(User)

router = Router()

REQUEST_USER_FOR_CHANGE = "Какую настройку вы хотите изменить?"
REQUEST_LOGIN = "Придумайте себе новый логин:"
LOGIN_ALREADY_EXISTS = message_markdowns.get("login_already_exists")
LOGIN_HAS_CHANGED = "✅ Успешно! Ваш логин изменён!"
LOGINS_ARE_THE_SAME = "🚫 У вас уже установлен такой логин"
REQUEST_ADDRESS = "Укажите ваш новый адрес:"
USER_ADDRESS_CHECK = "Твой адрес: {}?"
USER_ADDRESS_REREQUEST = "✍️ Введите ваш адрес:"
ADDRESS_HAS_CHANGED = "✅ Успешно! Ваш адрес изменён!"

REQUEST_DESCRIPTION = "Напишите ваше новое описание:"
DESCRIPTION_HAS_CHANGED = "✅ Успешно! Твоё описание изменено!"


def generate_me_reply(user: User):
    """Generating user data to reply."""
    return fmt.text(
        fmt.text(fmt.hbold("📋 Твои данные\n")),
        fmt.text(f"🆔 Логин: {fmt.hbold(user.login)}\n"),
        fmt.text(f"📔 Адрес: {fmt.hbold(user.address)}\n"),
        fmt.text(f"📝Описание: {fmt.hbold(user.description)}"),
        sep="\n",
    )


@router.callback_query(F.data == "settings")
async def settings(query: types.CallbackQuery, db: Session):
    """Sending settings parameters, which user can change."""
    user = crud_user.get_by_telegram_id(db, query.from_user.id)
    await query.message.edit_text(
        generate_me_reply(user), reply_markup=kbm_settings, parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "change_login")
async def request_login(query: types.CallbackQuery, state: FSMContext):
    """Request user for the login."""
    await state.set_state(LoginChange.login_input)
    await bot.send_message(query.from_user.id, REQUEST_LOGIN)


@router.message(LoginChange.login_input)
async def change_login(message: types.Message, state: FSMContext, db: Session):
    """Changing user login if it's not already exists."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)
    new_login = message.text

    if user.login == new_login:
        await state.clear()
        await bot.send_message(
            message.from_user.id, LOGINS_ARE_THE_SAME, reply_markup=kbm_settings
        )
        return

    if crud_user.is_login(db, new_login):
        await bot.send_message(
            message.from_user.id,
            LOGIN_ALREADY_EXISTS,
            reply_markup=kbm_settings,
            parse_mode=ParseMode.HTML,
        )
        return

    # Updating user login.
    user.login = new_login
    crud_user.update(db, user)

    await state.clear()
    await bot.send_message(
        message.from_user.id,
        LOGIN_HAS_CHANGED + "\n\n" + generate_me_reply(user),
        reply_markup=kbm_settings,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == "change_address")
async def request_address(query: types.CallbackQuery, state: FSMContext):
    """Request user for the address."""
    await state.set_state(AddressChange.address_input)
    await bot.send_message(query.from_user.id, REQUEST_ADDRESS)


@router.message(AddressChange.address_input)
async def check_adress(message: types.Message, state: FSMContext):
    """Getting and saving user address."""
    address = message.text
    address = geography.get_address(address)

    await state.update_data(address=address)
    await state.set_state(AddressChange.address_check)
    await bot.send_message(
        message.from_user.id,
        USER_ADDRESS_CHECK.format(address),
        reply_markup=kbm_y_or_n,
    )


@router.callback_query(F.data == "no", AddressChange.address_check)
async def rerequest_address(message: types.message, state: FSMContext):
    """Reasking user for the adress."""
    await state.set_state(AddressChange.address_input)
    await bot.send_message(message.from_user.id, USER_ADDRESS_REREQUEST)


@router.callback_query(F.data == "yes", AddressChange.address_check)
async def save_address(message: types.message, state: FSMContext, db: Session):
    """Saving new user address."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)

    data = await state.get_data()
    user.address = data["address"]
    crud_user.update(db, user)

    await state.clear()
    await bot.send_message(
        message.from_user.id,
        ADDRESS_HAS_CHANGED + "\n\n" + generate_me_reply(user),
        reply_markup=kbm_settings,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data == "change_description")
async def request_description(query: types.CallbackQuery, state: FSMContext):
    """Request user for the description."""
    await state.set_state(DescriptionChange.desription_input)
    await bot.send_message(query.from_user.id, REQUEST_DESCRIPTION)


@router.message(DescriptionChange.desription_input)
async def change_description(message: types.Message, state: FSMContext, db: Session):
    """Change user description."""
    user = crud_user.get_by_telegram_id(db, message.from_user.id)
    user.description = message.text
    user = crud_user.update(db, user)

    await state.clear()
    await bot.send_message(
        message.from_user.id,
        DESCRIPTION_HAS_CHANGED + "\n\n" + generate_me_reply(user),
        reply_markup=kbm_settings,
        parse_mode=ParseMode.HTML,
    )
