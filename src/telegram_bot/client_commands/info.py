import aiogram.utils.markdown as fmt
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command

from src.telegram_bot import message_markdowns
from src.telegram_bot.init import bot
from src.telegram_bot.keyboard_markups import kbm_main_menu

router = Router()

BOT_INFORMATION = message_markdowns.get("bot_information")


@router.callback_query(F.data == "get_info")
async def info(query: types.CallbackQuery):
    """
    Sending info about bot.
    """
    await query.message.edit_text(
        BOT_INFORMATION,
        reply_markup=kbm_main_menu,
        parse_mode=ParseMode.HTML,
    )
