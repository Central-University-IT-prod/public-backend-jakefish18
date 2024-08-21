from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.crud import CrudUser
from src.models import User
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import kbm_main_menu

crud_user = CrudUser(User)

router = Router()

CANCEL_MESSAGE = "✅ Команда отменена!"


@router.message(Command("cancel"))
async def get_main_menu_by_command(message: types.Message, state: FSMContext):
    """Send main menu to the user."""
    await state.clear()
    await bot.send_message(
        message.from_user.id, CANCEL_MESSAGE, reply_markup=kbm_main_menu
    )
