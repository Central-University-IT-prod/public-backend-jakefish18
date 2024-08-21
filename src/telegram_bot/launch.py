"""
Importing all bot functions from files and launching bot.
"""

from src.telegram_bot.client_commands import (
    add_note,
    add_travel,
    cancel,
    delete_friend,
    info,
    invite_friend,
    list_note,
    list_travels,
    menu,
    settings,
    start,
    travel,
)
from src.telegram_bot.init import bot, bot_dispatcher
from src.telegram_bot.middlewares import DatabaseSessionMiddleware


async def on_startup() -> None:
    """Info that bot has started"""
    print("Start polling for bot.")


async def run_bot() -> None:
    await bot.delete_webhook(drop_pending_updates=True)

    bot_dispatcher.startup.register(on_startup)
    bot_dispatcher.callback_query.outer_middleware(DatabaseSessionMiddleware())
    bot_dispatcher.message.outer_middleware(DatabaseSessionMiddleware())
    bot_dispatcher.include_routers(
        start.router,
        info.router,
        cancel.router,
        settings.router,
        menu.router,
        add_travel.router,
        list_travels.router,
        travel.router,
        add_note.router,
        list_note.router,
        invite_friend.router,
        delete_friend.router
    )

    await bot_dispatcher.start_polling(bot)
