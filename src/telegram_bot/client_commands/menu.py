from aiogram import F, Router, types
from aiogram.filters import Command

from src.crud import CrudUser
from src.models import User
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import kbm_main_menu, kbm_travels_menu

crud_user = CrudUser(User)

router = Router()

MAIN_MENU_MESSAGE = "🏠 Главное меню"


@router.message(Command("menu"))
async def get_main_menu_by_command(message: types.Message):
    """Send main menu to the user."""
    await bot.send_message(
        message.from_user.id, MAIN_MENU_MESSAGE, reply_markup=kbm_main_menu
    )


@router.callback_query(F.data == "main_menu")
async def get_main_menu(query: types.CallbackQuery):
    """Send main menu to the user."""
    await query.message.edit_text(MAIN_MENU_MESSAGE, reply_markup=kbm_main_menu)


@router.callback_query(F.data == "travels_menu")
async def get_travels_menu(query: types.CallbackQuery):
    """Send travels menu to the user."""
    await query.message.edit_text("🏝 Меню путешествий", reply_markup=kbm_travels_menu)
